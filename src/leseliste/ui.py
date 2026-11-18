"""Desktop-Oberfläche für die Leseliste (pywebview)."""

import json
import os
import threading
import webbrowser
from datetime import datetime
from pathlib import Path

import webview

from . import CancelledError, OUTPUT_DIR, count_resources, create_reading_list

HTML_FILE = Path(__file__).with_name("ui.html")


class Api:
    """Wird im JavaScript als window.pywebview.api.* verfügbar.

    Alle Attribute beginnen mit "_", damit pywebview sie nicht an JS weiterreicht.
    """

    def __init__(self, output_dir: Path):
        self._output_dir = output_dir.resolve()
        self._window = None
        self._cancel_event: threading.Event | None = None
        self._worker: threading.Thread | None = None

    def _attach(self, window):
        self._window = window

    def _send(self, function: str, payload):
        if self._window is not None:
            self._window.run_js(f"window.{function}({json.dumps(payload, ensure_ascii=False)})")

    # ---------- Gespeicherte Leselisten ----------

    def list_lists(self):
        if not self._output_dir.exists():
            return []
        items = []
        for path in self._output_dir.glob("leseliste_*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            try:
                created = datetime.strptime(path.stem[len("leseliste_"):], "%Y%m%d_%H%M%S")
                created_text = created.strftime("%d.%m.%Y, %H:%M")
            except ValueError:
                created_text = ""
            items.append({
                "file": path.name,
                "topic": data.get("topic") or path.stem,
                "created": created_text,
                "resources": count_resources(data),
            })
        items.sort(key=lambda item: item["file"], reverse=True)
        return items

    def load_list(self, file_name: str):
        path = (self._output_dir / file_name).resolve()
        if path.parent != self._output_dir or path.suffix != ".json":
            raise ValueError("Ungültiger Dateiname.")
        data = json.loads(path.read_text(encoding="utf-8"))
        return {"file": path.name, "path": str(path), "data": data}

    # ---------- Neue Leseliste erstellen ----------

    def start(self, topic: str):
        topic = (topic or "").strip()
        if not topic:
            raise ValueError("Bitte ein Thema eingeben.")
        if self._worker is not None and self._worker.is_alive():
            raise RuntimeError("Es läuft bereits eine Erstellung.")

        self._cancel_event = threading.Event()
        self._worker = threading.Thread(
            target=self._run, args=(topic, self._cancel_event), daemon=True
        )
        self._worker.start()
        return True

    def _run(self, topic: str, cancel_event: threading.Event):
        try:
            output_file = create_reading_list(
                topic,
                on_progress=lambda event: self._send("onProgress", event),
                cancel_event=cancel_event,
                output_dir=self._output_dir,
            )
            self._send("onFinished", {"file": output_file.name})
        except CancelledError as error:
            self._send("onFailed", {"message": str(error), "cancelled": True})
        except Exception as error:  # noqa: BLE001 – Fehler an die UI melden
            self._send("onFailed", {"message": str(error), "cancelled": False})

    def cancel(self):
        if self._cancel_event is not None:
            self._cancel_event.set()
        return True

    # ---------- Hilfsfunktionen ----------

    def open_url(self, url: str):
        if isinstance(url, str) and url.startswith(("http://", "https://")):
            webbrowser.open(url)
        return True

    def open_folder(self):
        self._output_dir.mkdir(exist_ok=True)
        if hasattr(os, "startfile"):
            os.startfile(self._output_dir)
        else:
            webbrowser.open(self._output_dir.as_uri())
        return True


def main():
    api = Api(OUTPUT_DIR)
    window = webview.create_window(
        "Leseliste",
        html=HTML_FILE.read_text(encoding="utf-8"),
        js_api=api,
        width=1200,
        height=820,
        min_size=(800, 560),
        text_select=True,
    )
    api._attach(window)
    webview.start()


if __name__ == "__main__":
    main()
