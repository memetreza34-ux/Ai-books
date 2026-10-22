# Ai-books — AI Book Studio

**Langfristig erweiterbare KI-Buchfabrik mit Projekt-Gehirn.** Ein einziges Repository; lokal auf dem Mac; kostenbewusst, nachvollziehbar und mit menschlichen Veröffentlichungsfreigaben.

## Für KI-Agenten
Lies [AGENTS.md](AGENTS.md), [gehirn/00-START-HIER.md](gehirn/00-START-HIER.md) und [gehirn/09-STATUS.md](gehirn/09-STATUS.md). Lade weitere Dokumente nur nach Bedarf, um Tokens zu sparen.

## Bereits funktionierende Fähigkeiten
- **Sudoku:** Reproduzierbare Rätsel, jeweils nachgerechnet und eindeutig lösbar, mit Duplikatkontrolle.
- **Innen-PDF:** 8.5 × 11 Zoll, ohne Innen-Beschnitt, mit Lösungsseiten und optionalen Vorschauübersichten.
- **Vollumschlag-PDF (Entwurf):** Rückseite + Buchrücken + Vorderseite mit KDP-Formel für weißes oder cremefarbenes Papier, Cover-Beschnitt und freigehaltenem Barcodebereich.
- **Maschinelle Druckprüfung:** Seitengrößen, Seitenanzahl, tatsächliche Umschlagbreite, eingebettete verwendete Schriftarten und Text-Sicherheitsabstände.
- **Live-Katalogrecherche:** Offizielle Open-Library- und Google-Books-APIs werden nur auf ausdrücklichen Befehl abgefragt; 3 Nischen, begrenzte Anfragen, Zeitstempel/Quell-URLs/Cache/Fehlerdiagnose. Liefert **keine Kaufzahlen und keine belegte Nachfrage**. [Anleitung](docs/LIVE-RESEARCH.md).
- **Ideenbewertung:** Gewichtet Nachfrage, Lesermehrwert, Originalität/Differenzierung, Evergreen, mögliche Marge und Umsetzbarkeit. Ohne aktuelle belegte Marktdaten bleibt eine Idee `HOLD`.
- **Gehirn:** Ziele, Architektur, zehn Bucharten, rechtliche Kontrollpunkte, Entscheidungen, offene Risiken, Roadmap und Fehlergedächtnis.
- **CI:** 17 Python-Tests plus reproduzierbarer Beispielbuchlauf; Test-PDFs in GitHub-Actions-Artefakten.

## Schnellstart auf Mac
```bash
git clone https://github.com/memetreza34-ux/Ai-books.git
cd Ai-books
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev,preview]'
python -m pytest
aibooks sudoku --title "Sudoku Testband" --count 28 --clues 38 --paper white --seed 20261022 --previews --out output/sudoku-test
aibooks evaluate --input examples/opportunities-example.json --out output/research-example.json
aibooks research --input examples/research-niches.json --out output/research-live.json
```

**Beachte:** `output/` ist in Git ignoriert. Bereits gefüllte Zielordner bzw. vorhandene Berichte werden nicht überschrieben.

## Erzeugte Dateien
- `interior-DRAFT.pdf`: PDF-Innenseiten
- `cover-WRAP-DRAFT.pdf`: zusammenhängender Umschlag mit Buchrücken
- `puzzles-and-solutions.json`: maschinenlesbare Rätsel und Lösungen
- `quality-report.json`: Qualitätsprüfungen und verbleibende Freigaben
- `manifest.json`: Seed, Seitenzahl, Papierprofil, Hashwerte, Dateigrößen
- `previews/contact-sheet-*.png`: alle Seiten als Übersicht (optional)
- `output/research-example.json`: vorsichtige Bewertung von **synthetischen** Beispieldaten
- `output/research-live.json`: begrenzte **echte Katalogdaten** mit klarer Trennung von Konkurrenzindikatoren und Nachfrage

## Wichtige Grenzen
Dieses System erstellt aktuell **technisch vorgeprüfte ENTWÜRFE**, keine von Amazon genehmigten Bücher. Vor der echten Veröffentlichung fehlen insbesondere visuelle Vollkontrolle, Abgleich mit dem offiziellen Cover Calculator, KDP Previewer, Probedruck, Rechteprüfung, echte Marktrecherche, professionelle Produktentscheidung und deine ausdrückliche Freigabe. **Kein automatischer Upload, keine Werbeausgaben, keine Gewinnversprechen.**

Mehr: [Schnellstart](docs/QUICKSTART.md) · [Druckvorstufe](docs/PRINT-PREFLIGHT.md) · [Marktevidenz](docs/OPPORTUNITY-RESEARCH.md) · [Roadmap](gehirn/11-ROADMAP.md).
