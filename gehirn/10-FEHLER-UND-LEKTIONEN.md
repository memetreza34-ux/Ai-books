# Dauerhaftes Fehlergedächtnis

Erfasse nur echte beobachtete Fehler, nicht frei erfundene Beispielvorfälle.

## Schema je Eintrag
- ID, Datum, betroffener Buchtyp und betroffene Version
- Symptom, Reproduktionsschritte, Ursache, Schweregrad
- Korrektur und zugehöriger Commit/Test
- Neuer Regressionstest und Status
- Übertragbarkeit auf andere Genres

## Bekannte Vorsorgeregeln (keine Vorfälle)
- KI behauptet eindeutiges Sudoku ohne Solver: durch algorithmischen Unique-Solution-Check verhindern.
- Titel/Cover versprechen mehr Rätsel oder Seiten als enthalten: Manifest-PDF-Abgleich.
- Übersetzung verändert Aufgaben: in Zielsprache erneut auf Lösbarkeit und Layout prüfen.
- Schwarz-Weiß-Inhalt mit teuren Color-Settings: Druckprofil bewusst wählen.
- Neue Bücher verwenden alte KDP-Regeln: live prüfen vor Freigabe.
- Agenten löschen Kontext: AGENTS.md + Status + ADR verpflichtend.
