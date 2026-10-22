# Ai-books — AI Book Studio

**KI-gestützte Buchfabrik mit dauerhaftem Projektgedächtnis.** Lokal auf dem Mac, modular, kostenschonend und kontrollierbar. Recherche und wirtschaftliche Entscheidungen sind eigene Schritte; PDF-Erzeugung garantiert keine Verkäufe.

## Start hier
1. Für Antigravity / Claude Code / Codex: [AGENTS.md](AGENTS.md) → [gehirn/00-START-HIER.md](gehirn/00-START-HIER.md) → [gehirn/09-STATUS.md](gehirn/09-STATUS.md).
2. Für Entwickler: [Schnellstart](docs/QUICKSTART.md).
3. Für Produktentscheidungen: [Vision](gehirn/01-VISION.md), [Bucharten](gehirn/04-BUCHARTEN.md), [Qualitätsregeln](gehirn/06-QUALITAET.md), [Roadmap](gehirn/11-ROADMAP.md).

## Bereits ausführbar: Sudoku-Prototyp
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,preview]'
pytest
aibooks sudoku --title "Sudoku Testband" --count 28 --seed 20261022 --previews --out output/sudoku-test
```

Der Befehl erzeugt eine **Innen-PDF als DRAFT**, ein **Frontcover-Konzept (kein fertiger KDP-Umschlag)**, alle Aufgaben/Lösungen als JSON, QA-Bericht, Manifest mit Checksums sowie Kontaktbögen sämtlicher Seiten. Keine KI-API erforderlich. Nur in einen leeren Ausgabeordner schreiben; bestehende Ergebnisse werden nicht überschrieben.

## Projektaufbau
- `gehirn/`: Entscheidungen, Status, Qualitätsregeln, Finanzlogik, KI-Kosten und langfristiges Gedächtnis
- `booktypes/`: Qualitätsanforderungen und spätere Generator-Erweiterungen pro Buchart
- `src/aibooks/`: ausführbarer Python-Kern
- `tests/`: algorithmische und PDF-Regressionstests
- `docs/`: Nutzung und Quellen
- `output/`: **lokal erzeugt und .gitignored**, niemals Kundendaten/Geheimnisse in Git

## Grenzen
**Nicht automatisch veröffentlichbar.** KDP fordert weitere Live-Regelprüfung, exaktes Vollumschlag-Cover mit Rücken/Beschnitt, endgültige Marke/Metadaten, Rechteprüfung, echte Marktvalidierung, Sichtprüfung, KDP-Vorschau und gegebenenfalls Probedruck. Die CI erzeugt einen internen Beispielband als Workflow-Artefakt, keine Veröffentlichungsfreigabe.

Nach jeder wichtigen Änderung: Code testen, [Status](gehirn/09-STATUS.md) aktualisieren, neue Entscheidungen und systemische Fehler dauerhaft festhalten. Ein Repository, keine Doppel-Fabriken.
