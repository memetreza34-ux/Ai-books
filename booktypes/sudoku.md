# Sudoku-Modul

**Status:** erste Referenzimplementierung, nicht Beweis für Marktnachfrage.

Ein gültiges Sudoku hat 9x9 Felder, Ziffern 1–9, gültige vorgegebene Werte und exakt eine Lösung.

## Pflichtprüfungen
- Solver findet exakt eine Lösung; Antwort stimmt mit gespeicherter Lösung überein.
- Keine identischen Puzzles in einem Buch; nicht nur zufällig umbenannte Dateien.
- Klare Schwierigkeitsangabe nur nach überprüfbarer Metrik; Clue-Anzahl allein ist kein seriöser Schwierigkeitsnachweis.
- Ausreichend große Zellen, klare Kontrastwerte, eindeutige Zuordnung von Rätselnummern/Lösungen.
- Titel/Metadaten dürfen Anzahl und Schwierigkeit nicht übertreiben.
- Reproduzierbarkeit durch Seed, Solver-Version, Generatorversion und Hash.
