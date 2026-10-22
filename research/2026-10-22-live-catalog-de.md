# Live-Katalogrecherche für drei Evergreen-Buchnischen

**Datum:** 22.10.2026
**Quelle:** GitHub Actions [Live Book Catalog Research #39813832909](https://github.com/memetreza34-ux/Ai-books/actions/runs/39813832909)
**Belegart:** Offizielle Katalog-API-Antworten, dokumentiert in `ai-books-catalog-research/report.json`; Artefakt 14 Tage verfügbar
**Bewertung:** ALLE KANDIDATEN `HOLD`, keine Aussagen zu Verkäufen, Nachfrage, Profit oder KDP-Marktfähigkeit.

## Technisches Ergebnis

| Idee | Open Library | Apple Books DE (E-Books) | Gefilterte Beispieldatensätze |
| --- | --- | --- | ---: |
| Sudoku Großdruck | API erreichbar; 10 passende Datensätze | API erreichbar; 0 passende Datensätze | 10 |
| Mathe Grundschule | API erreichbar; 0 passende Datensätze | API erreichbar; 4 passende Datensätze | 4 |
| Kinder-Labyrinthe | API erreichbar; 3 passende Datensätze | API erreichbar; 4 passende Datensätze | 7 |

**Sehr wichtig:** Die Stichprobe pro API ist auf 10 Ergebnisse je Suche begrenzt. 0 Treffer in einer Quelle bedeutet NICHT, dass es keine entsprechenden Bücher gibt. Katalogdatensätze sind keine live verfügbaren Amazon-Taschenbuchangebote. Kein einziger Wert ist ein Verkaufsnachweis.

## Nachprüfbare Beispiele

**Sudoku:**
- [Sudoku Großdruck Leicht – Open Library](https://openlibrary.org/works/OL30723325W)
- [Sudoku Großdruck – Open Library](https://openlibrary.org/works/OL30597810W)

**Mathematik:**
- [Mathebuch Klasse 2 – Apple Books](https://books.apple.com/de/book/mathebuch-klasse-2/id548992274?uo=4)
- [Zahlen schreiben lernen – Mathe 1. Klasse – Apple Books](https://books.apple.com/de/book/zahlen-schreiben-lernen-mathe-1-klasse/id6799550853?uo=4)

**Kinder-Labyrinthe:**
- [Labyrinth Rätselbuch Für Kinder – Open Library](https://openlibrary.org/works/OL27192255W)
- [Große Labyrinth Buch Für Kinder – Open Library](https://openlibrary.org/works/OL30498229W)

## Technische Quellenentscheidung
Der allererste Testlauf [#39813366853](https://github.com/memetreza34-ux/Ai-books/actions/runs/39813366853) bestätigte Open-Library-Daten, während die Google Books API wiederholt `HTTP 429` ausgab. Daraufhin wurde der zusätzliche Anbieter auf Apple Books umgestellt. Der zweite Test [#39813832909](https://github.com/memetreza34-ux/Ai-books/actions/runs/39813832909) bestätigte beide Endpunkte als erreichbar.

Apple Books listet **E-Books**, nicht KDP-Taschenbücher; mögliche E-Book-Preise dürfen **nicht** für Taschenbuch-Tantiemen oder Print-Margen eingesetzt werden. Katalog-Rohdaten werden nicht automatisch dauerhaft im Git-Repository abgelegt.

## Geschäftsentscheidung (keine Siegerkategorie)
- Für Sudoku gibt es grundsätzlich vorhandene katalogisierte Produkte, aber das erklärt weder Verkäufe noch ein tragfähiges Nischenangebot.
- Grundschulmathematik und Kinder-Labyrinthe haben ebenfalls katalogisierte Beispiele, jedoch keine belegten Suchvolumina.
- **Kein belastbares Ranking nach Geldpotenzial möglich.** Eine Auswahl allein nach Trefferanzahl wäre sachlich falsch.

## Nächster Prüfschritt
Manuelle/agentengestützte Untersuchung einer repräsentativen Stichprobe echter deutscher Amazon-/Buchhandelsangebote mit Datum, Titel, Format, Seiten, Preis, Zielgruppe, Bewertungen und konkreten Schwächen; daneben ein unabhängiger Nachfrageindikator. Anschließend pro Buchidee KDP-Druckkosten und Tantiemen über den offiziellen Rechner. Bis dahin `HOLD`.
