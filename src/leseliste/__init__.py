import json
import subprocess
import sys
import threading
import time
from pathlib import Path
from datetime import datetime


def _describe_tool_use(block: dict) -> str:
    """Kurze, lesbare Beschreibung eines Tool-Aufrufs."""
    name = block.get("name", "?")
    tool_input = block.get("input", {})
    if name == "WebSearch":
        return f"Suche: {tool_input.get('query', '')}"
    if name == "WebFetch":
        return f"Lese:  {tool_input.get('url', '')}"
    return f"Tool:  {name}"


def run_claude(prompt: str, timeout: int = 900) -> str:
    """Startet Claude, zeigt den Fortschritt live an und gibt den Ergebnistext zurück."""
    process = subprocess.Popen(
        [
            "claude",
            "-p",
            "--output-format", "stream-json",
            "--verbose",
            "--include-partial-messages",
            "--tools", "WebSearch,WebFetch",
            "--allowedTools", "WebSearch,WebFetch",
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    # stderr parallel einsammeln, damit der Prozess nicht blockiert
    stderr_lines: list[str] = []
    stderr_thread = threading.Thread(
        target=lambda: stderr_lines.extend(process.stderr), daemon=True
    )
    stderr_thread.start()

    # Nach Ablauf des Timeouts den Prozess beenden
    timed_out = threading.Event()

    def _kill():
        timed_out.set()
        process.kill()

    timer = threading.Timer(timeout, _kill)
    timer.start()

    process.stdin.write(prompt)
    process.stdin.close()

    start = time.monotonic()
    final_event = None

    # Status für die sich aktualisierende Fortschrittszeile
    status_label = None   # "schreibt" oder "denkt nach"
    status_chars = 0
    status_open = False   # steht gerade eine Zeile ohne Zeilenumbruch da?
    last_update = 0.0

    def elapsed() -> str:
        return f"[{int(time.monotonic() - start):>4}s]"

    def show_status(force: bool = False):
        nonlocal status_open, last_update
        now = time.monotonic()
        if not force and now - last_update < 1:
            return
        last_update = now
        print(
            f"\r{elapsed()} Claude {status_label} ... {status_chars:,} Zeichen".replace(",", "."),
            end="", flush=True,
        )
        status_open = True

    def println(message: str):
        nonlocal status_open
        if status_open:
            print()
            status_open = False
        print(f"{elapsed()} {message}", flush=True)

    try:
        for line in process.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            event_type = event.get("type")

            if event_type == "stream_event":
                inner = event.get("event", {})
                inner_type = inner.get("type")
                if inner_type == "content_block_start":
                    block_type = inner.get("content_block", {}).get("type")
                    if block_type in ("text", "thinking"):
                        if status_open:
                            print()
                            status_open = False
                        status_label = "schreibt" if block_type == "text" else "denkt nach"
                        status_chars = 0
                        show_status(force=True)
                elif inner_type == "content_block_delta":
                    delta = inner.get("delta", {})
                    piece = delta.get("text") or delta.get("thinking") or ""
                    if piece and status_label:
                        status_chars += len(piece)
                        show_status()
                elif inner_type == "content_block_stop" and status_label:
                    show_status(force=True)
                    status_label = None

            elif event_type == "assistant":
                for block in event.get("message", {}).get("content", []):
                    if block.get("type") == "tool_use":
                        println(_describe_tool_use(block))

            elif event_type == "result":
                final_event = event
    finally:
        if status_open:
            print()
        timer.cancel()
        process.wait()
        stderr_thread.join(timeout=5)

    if timed_out.is_set():
        raise RuntimeError(f"Abbruch nach {timeout} Sekunden (Timeout).")

    if final_event is None:
        raise RuntimeError(
            f"Kein Ergebnis von Claude erhalten (Exit-Code {process.returncode}).\n"
            + "".join(stderr_lines)
        )

    if final_event.get("is_error"):
        raise RuntimeError(
            f"Claude meldet einen Fehler ({final_event.get('subtype')}): "
            f"{final_event.get('result', '')}"
        )

    duration = time.monotonic() - start
    turns = final_event.get("num_turns", "?")
    print(f"\nFertig nach {duration:.0f}s, {turns} Schritte.")

    return (final_event.get("result") or "").strip()


def create_reading_list(topic: str):
    prompt = f"""
Du bist mein persönlicher Lerncoach und technischer Mentor.

Ich möchte das folgende Thema wirklich verstehen und
praktisch anwenden können:

THEMA:
{topic}

DEINE ROLLE

Stelle mir einen individuellen Lernpfad zusammen.
Denke dabei wie ein guter Mentor, der mich Schritt für
Schritt an ein Thema heranführt.

Ich möchte nicht einfach eine akademische Literaturliste,
sondern einen angenehmen, abwechslungsreichen und
praxisorientierten Lernprozess.

QUELLEN UND LERNMATERIALIEN

Sei bei der Auswahl bewusst offen:

- Praxisorientierte Fachbücher, z.B. von O'Reilly,
  Manning, No Starch Press oder Addison-Wesley.
- Gute technische Blogs und Tutorials.
- Offizielle Dokumentationen.
- Online-Kurse und interaktive Lernressourcen.
- GitHub-Repositories und praktische Beispiele.
- Wissenschaftliche Paper, wenn sie wirklich wichtig sind.
- Surveys und Übersichtsarbeiten, wenn sie beim Einstieg helfen.
- Einzelne Buchkapitel oder Paper-Sektionen, wenn nicht
  das gesamte Werk gelesen werden muss.

Bevorzuge gut geschriebene, verständliche und didaktisch
starke Materialien.

Ein gutes Buch oder Tutorial ist mir häufig lieber als
fünf schwer verständliche wissenschaftliche Paper.

LERNDIDAKTIK

Baue den Lernpfad so auf, dass ich kontinuierlich Fortschritte
mache und nicht von Anfang an mit komplexer Theorie
überfordert werde.

Orientiere dich an dieser Struktur:

1. Einstieg:
   Was ist das Thema? Warum ist es relevant?
   Welche grundlegenden Konzepte sollte ich kennen?

2. Grundlagen:
   Verständliche Bücher, Tutorials und Erklärungen.

3. Praktischer Einstieg:
   Erste kleine Projekte, Experimente oder Übungen.

4. Vertiefung:
   Fortgeschrittene Konzepte, technische Hintergründe
   und ausgewählte wissenschaftliche Arbeiten.

5. Expertenwissen:
   Aktuelle Forschungsansätze, offene Probleme und
   weiterführende Ressourcen.

Passe diese Struktur an das jeweilige Thema an.
Nicht jedes Thema benötigt alle fünf Phasen.

COACHING

Ich möchte nicht nur lesen, sondern verstehen.

Erstelle deshalb zu jeder wichtigen Ressource:

- Warum sollte ich sie lesen oder durcharbeiten?
- Was sollte ich daraus mitnehmen?
- Welche Kapitel, Abschnitte oder Seiten sind besonders relevant?
- Was kann ich überspringen?
- Welche praktischen Übungen bieten sich an?
- Welche Verständnisfragen sollte ich beantworten können?

Formuliere mindestens drei Verständnisfragen pro
wichtiger Ressource und gib jeweils eine ausführliche
Musterantwort.

Die Fragen sollen zum Nachdenken anregen und Zusammenhänge
prüfen, nicht nur Definitionen abfragen.

QUALITÄT DER QUELLEN

- Verwende möglichst aktuelle und etablierte Ressourcen.
- Bevorzuge nachvollziehbare, tatsächlich existierende Quellen.
- Erfinde keine Titel, Autoren, Veröffentlichungsjahre,
  Kapitel oder URLs.
- Verlinke Quellen möglichst direkt.
- Kennzeichne Unsicherheiten transparent.
- Unterscheide zwischen verifizierten und nicht verifizierten
  Kapitel- und Abschnittsangaben.
- Achte auf einen guten Mix aus Theorie und Praxis.

JSON-AUSGABE

Gib ausschließlich gültiges JSON zurück.
Keine Markdown-Codeblöcke und keine Erklärungen
außerhalb des JSON.

Verwende folgende Struktur:

{{
  "topic": "Thema",
  "introduction": "Kurze Einführung und Einordnung",
  "learning_objectives": [],
  "assumed_knowledge": [],
  "learning_path": [
    {{
      "phase": 1,
      "title": "Einstieg",
      "description": "Was ich in dieser Phase lernen soll",
      "resources": [
        {{
          "type": "book",
          "title": "Titel",
          "authors": [],
          "publisher": null,
          "year": null,
          "url": null,
          "priority": "essential",
          "estimated_hours": 3,
          "reason": "Warum diese Ressource hilfreich ist",
          "recommended_sections": [
            {{
              "name": "Kapitel oder Abschnitt",
              "focus": "Worauf ich achten soll",
              "verified": false
            }}
          ],
          "takeaways": [],
          "practical_exercises": [],
          "understanding_questions": [
            {{
              "question": "Frage",
              "answer": "Ausführliche Musterantwort"
            }}
          ]
        }}
      ],
      "milestone": "Woran ich erkenne, dass ich diese Phase verstanden habe"
    }}
  ],
  "final_project_ideas": [],
  "further_exploration": [],
  "glossary": []
}}

WEITERE REGELN

- Verwende für type passende Werte wie:
  book, blog, tutorial, documentation, course,
  paper, repository oder video.
- priority kann essential, recommended oder optional sein.
- Plane lieber wenige gute Ressourcen als eine riesige Liste.
- Passe die Schwierigkeit an einen Lernenden an, der
  das Thema systematisch erschließen möchte.
- Erkläre Fachbegriffe, wenn sie erstmals auftauchen.
- Gib mir einen roten Faden durch die Materialien.
- Achte darauf, dass die Lernzeit realistisch bleibt.
- Die Antworten auf Verständnisfragen sollen fachlich
  fundiert und verständlich sein.
- Gib keine erfundenen URLs aus.
- Bevorzuge eine Mischung aus Lesen, Ausprobieren und
  eigenständigem Erklären.

Dein Ziel ist nicht, möglichst viele Quellen aufzulisten.
Dein Ziel ist, mich tatsächlich in die Lage zu versetzen,
das Thema zu verstehen und selbstständig damit zu arbeiten.
    """

    print(f"Erstelle Leseliste für: {topic}")
    print("Claude wird gestartet ...")

    text = run_claude(prompt, timeout=900)

    # Ausgabeordner erstellen
    output_dir = Path("leselisten")
    output_dir.mkdir(exist_ok=True)

    # Dateinamen aus Zeitstempel
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = output_dir / f"leseliste_{timestamp}.json"
    raw_file = output_dir / f"leseliste_{timestamp}_raw.txt"

    # Rohantwort sichern, damit nichts verloren geht
    raw_file.write_text(text, encoding="utf-8")

    # JSON aus der Antwort lesen (toleriert Codeblöcke/Text drumherum)
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise RuntimeError(
            f"Keine JSON-Antwort erhalten. Rohantwort: {raw_file.resolve()}"
        )
    try:
        data = json.loads(text[start:end + 1])
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Ungültiges JSON ({error}). Rohantwort: {raw_file.resolve()}"
        ) from error

    # JSON speichern
    output_file.write_text(
        json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ),
        encoding="utf-8"
    )

    print("\nLeseliste erfolgreich erstellt!")
    print(f"Datei: {output_file.resolve()}")
    count = sum(
        len(phase.get("resources", []))
        for phase in data.get("learning_path", [])
    )
    print(f"Anzahl Quellen: {count}")


def main():
    if len(sys.argv) < 2:
        print('Verwendung: leseliste "Dein Thema"')
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    try:
        create_reading_list(topic)
    except Exception as error:
        print(f"\nFehler: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()