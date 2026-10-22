# Schnellstart (macOS)

```bash
git clone https://github.com/memetreza34-ux/Ai-books.git
cd Ai-books
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,preview]'
pytest
aibooks sudoku --title "Sudoku Testband" --count 28 --clues 38 --seed 20261022 --previews --out output/sudoku-test
```

Standardausgabe (im ignorierten `output/`-Ordner):
- `interior-DRAFT.pdf`: Innenseiten im Format 8.5 x 11 Zoll, ohne Beschnitt.
- `cover-CONCEPT-front-only.pdf`: reine Vorderseiten-Idee, **nicht** als KDP-Cover hochladen.
- `puzzles-and-solutions.json`: generierte Aufgaben mit verifizierten Antworten.
- `quality-report.json`: technische Prüfungen und gesperrte menschliche Schritte.
- `manifest.json`: Produktionsparameter, Dateihashes und Entwurfsstatus.
- `previews/contact-sheet-*.png`: visuelle Übersicht **aller** Seiten, wenn `--previews` genutzt wurde.

Du kannst Vorschauen optional weglassen und `python -m pip install -e '.[dev]'` benutzen.

**Sicherheit:** Ausgabeordner muss neu oder leer sein; nichts wird überschrieben. Es erfolgen keine API-Aufrufe, kein Upload, keine Werbeausgaben und keine Verkaufstransaktionen. Vor Veröffentlichung [KDP-Checkliste](../gehirn/08-KDP-VEROEFFENTLICHUNG.md) abarbeiten.

## Agenten
Antigravity, Claude Code und Codex: **zuerst** `AGENTS.md`, `gehirn/00-START-HIER.md` und `gehirn/09-STATUS.md` lesen. Danach nur relevante Dateien, um Tokens zu sparen.

## Fehleranalyse
- `ModuleNotFoundError`: virtuelle Umgebung aktivieren; Installation wiederholen.
- Keine Vorschaubilder: Preview-Extras `.[preview]` installieren.
- `Output folder must be empty`: anderen `--out`-Ordner oder bewusst selbst archivieren.
- Prüfung rot: keine Datei als fertig bezeichnen; Fehler mit reproduzierbarem Test beheben.
