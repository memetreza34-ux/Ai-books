# Design-Review v1 – 23.10.2026

**Geprüfte Materialien:** GitHub Actions [#39976542822](https://github.com/memetreza34-ux/Ai-books/actions/runs/39976542822) – 120 Rätsel, 184 Seiten, PDFs/PNG.

## Tatsächlich im gerenderten Output kontrolliert
- `cover-CONCEPT-editorial.pdf`: heller Editorial-Umschlag, Titel und Seitenelemente auf Front/back lesbar, Barcodebereich frei.
- `cover-CONCEPT-blueprint.pdf`: technisch-blaue Variante; im ersten Bau vor allem farblich abweichend, deshalb zusätzliche Noir-Neugestaltung priorisiert.
- `cover-CONCEPT-noir.pdf`: im ersten Bau noch zu ähnlich positionierte Elemente; danach spezifische neue typografische Anordnung mit großer `120` implementiert.
- `previews/contact-sheet-001.png`: neu gestaltete Titelseite, Einführung, Regeln und erste Rätsel.
- Der restliche Innenband wurde automatisiert auf Seitenzahl, Titel/Rätselzählung und technische Sicherheitsränder geprüft; **nicht jede Seite einzeln visuell abgenommen**.

## Befunde und Maßnahmen
- Alte Innenseiten hatten eine unruhige/technisch wirkende „Ai-books Muster / Entwurf“-Fußzeile. Überarbeitet zu sachlichem kleinen Folio und eindeutigem ENTWURF-Vermerk.
- Erstes Cover war auf dunkle Flächen + isoliertes Gitter beschränkt. Revidiert in drei konzeptionelle Farb-/Typorichtungen mit gemeinsamer, ehrlicher Produktinformation.
- Version 1 der Noir-Variante unterschied sich noch zu wenig vom Blueprint-Cover: daher zweite Iteration mit typografischem Großformat-Motiv, kleinem Raster und neuem Rahmen.
- Automatisierte Metadaten- und Inhaltsprüfung erkannte zunächst den neuen Wortlaut für die Buchanzahl nicht; Parser wurde um zwei definierte, mathematisch äquivalente Produktformulierungen erweitert statt Prüfung abzuschalten.
- Layoutansicht auf Kontaktbogen zeigte großen ruhigen Weißraum. Das ist bewusst zweckorientiert, aber reale Leserfreigabe steht aus.

## Kein Qualitätsversprechen
Ein attraktiveres Layout allein ist **kein** Beweis für Marktfit, Originalität, Premiumdruck oder gute Barrierefreiheit. Keine kommerzielle Freigabe. KDP-Cover-Calculator, Printproof, ungeprüfte Sudoku-Isomorphie, Zielgruppe und echte Nachfrage bleiben offene Blocker.
