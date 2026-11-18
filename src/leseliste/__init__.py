
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime


def create_reading_list(topic: str):
    prompt = f"""
Du bist ein wissenschaftlicher Rechercheassistent.

Erstelle eine fundierte, didaktisch sinnvolle Leseliste
zum folgenden wissenschaftlichen Thema:

THEMA:
{topic}

ZIEL:
Eine Person soll das Thema von den theoretischen Grundlagen
bis zum Verständnis aktueller wissenschaftlicher Methoden
systematisch erlernen können.

Erstelle ein JSON mit folgender Struktur:

{{
  "topic": "Thema",
  "learning_objectives": [
    "Lernziel 1"
  ],
  "reading_list": [
    {{
      "order": 1,
      "type": "paper",
      "title": "Titel",
      "authors": ["Autor 1"],
      "year": 2024,
      "source": "Journal oder Konferenz",
      "doi": null,
      "url": null,
      "priority": "essential",
      "estimated_hours": 3,
      "reason": "Warum ist diese Quelle relevant?",
      "sections": [
        {{
          "name": "Kapitel oder Sektion",
          "focus": "Was soll hier gelernt werden?"
        }}
      ],
      "prerequisites": [],
      "understanding_questions": [
        {{
          "question": "Verständnisfrage",
          "answer": "Ausführliche Musterantwort"
        }}
      ]
    }}
  ]
}}

ANFORDERUNGEN:

1. Erstelle eine Lernreihenfolge vom Grundlagenwissen
   bis zu fortgeschrittenen Forschungsarbeiten.

2. Berücksichtige:
   - Grundlagenbücher
   - wissenschaftliche Paper
   - relevante Surveys und Reviews
   - gegebenenfalls einzelne Buchkapitel
   - wichtige ergänzende Forschungsarbeiten

3. Bevorzuge echte, veröffentlichte wissenschaftliche Quellen.
   Erfinde niemals Titel, Autoren, DOI oder URLs.

4. Wenn möglich, gib direkte DOI- oder Verlagslinks an.

5. Nenne konkrete Kapitel oder Sektionen, die gelesen
   werden sollten. Wenn die Gliederung nicht verifiziert
   werden kann, kennzeichne sie entsprechend.

6. Jede Quelle benötigt mindestens drei
   Verständnisfragen mit ausführlichen Antworten.

7. Die Fragen sollen nicht nur Fakten abfragen,
   sondern das konzeptionelle Verständnis prüfen.

8. Die Leseliste soll aufeinander aufbauen.
   Erkläre die Abhängigkeiten zwischen den Quellen.

9. Unterscheide zwischen:
   - essential
   - recommended
   - optional

10. Gib ausschließlich gültiges JSON zurück.
    Keine Markdown-Codeblöcke und keine Erklärungen
    außerhalb des JSON.

WICHTIG:
Recherchiere sorgfältig. Qualität und Verlässlichkeit
sind wichtiger als die Anzahl der Quellen.
"""

    print(f"Erstelle Leseliste für: {topic}")
    print("Claude wird gestartet ...")

    result = subprocess.run(
        [
            "claude",
            "-p",
            "--output-format", "text",
            "--tools", "WebSearch,WebFetch"
        ],
        input=prompt,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=900
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    # JSON aus der Antwort lesen
    data = json.loads(result.stdout.strip())

    # Ausgabeordner erstellen
    output_dir = Path("leselisten")
    output_dir.mkdir(exist_ok=True)

    # Dateinamen aus Thema und Zeitstempel
    filename = (
        f"leseliste_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    output_file = output_dir / filename

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
    print(f"Anzahl Quellen: {len(data.get('reading_list', []))}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Verwendung: python leseliste.py "Dein Thema"')
        sys.exit(1)

    topic = " ".join(sys.argv[1:])

    try:
        create_reading_list(topic)
    except Exception as error:
        print(f"\nFehler: {error}")
        sys.exit(1)
