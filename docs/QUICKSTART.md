# Schnellstart: macOS, Antigravity, Claude Code, Codex

```bash
git clone https://github.com/memetreza34-ux/Ai-books.git
cd Ai-books
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,preview]'
python -m pytest
aibooks sudoku --title "Sudoku Testband" --count 28 --clues 38 --paper white --seed 20261022 --previews --out output/sudoku-test
```

### Ergebnis
- `interior-DRAFT.pdf`: 8.5×11 Zoll Innen-PDF, ohne Beschnitt.
- `cover-WRAP-DRAFT.pdf`: Vorderseite, Rücken und Rückseite, mit 0.125 Zoll Cover-Beschnitt. Covergröße aus realer Seitenzahl und Papierprofil.
- `puzzles-and-solutions.json`: überprüfte Aufgaben.
- `quality-report.json`: automatische Checks plus offene Pflichten.
- `manifest.json`: Parameter, Hashwerte, Buchstatus.
- `previews/contact-sheet-*.png`: optional jede Seite als Kontrollbogen.

### Forschungsbewertung (nur vorhandene Belege)
```bash
aibooks evaluate --input examples/opportunities-example.json --out output/research-example.json
```
Das Beispiel verwendet **KEINE echten Marktbelege** und bleibt auf `HOLD`. Die Software führt noch keine automatische Live-Recherche durch; Quellennachweise müssen geprüft und dokumentiert sein.

### Grenzen
Keine Überschreibung bestehender Ergebnisse; keine KDP-Veröffentlichung, kein Ad-Spend, keine Nutzung von API-Keys. Behandle alle PDFs bis zur manuellen Freigabe als interne **Entwürfe**.

Vor Veröffentlichung offizielle KDP-Seiten und den KDP Cover Calculator/Previewer prüfen. Näheres: [PRINT-PREFLIGHT](PRINT-PREFLIGHT.md).

KI-Agenten lesen `AGENTS.md` → `gehirn/00-START-HIER.md` → `gehirn/09-STATUS.md`.
