# Aktueller Projektstatus

Stand: 2026-10-22; fortlaufend nach jedem substantiellen Arbeitsschritt aktualisieren.

## Ziel
Verlässliche modulare Buchfabrik auf Basis des einzigen Repositories `Ai-books`.

## Bestätigt
- Eigentümer-Prioritäten aus 55 Antworten dokumentiert.
- Altprojekt nicht blind kopieren; neues Repository gezielt aufgebaut.
- Erste referenzielle Buchart: Sudoku (technischer Test, nicht behauptete Marktsieger-Kategorie).
- Vor erster realer Veröffentlichung alle relevanten Regeln live überprüfen.

## Implementierung
- Projektgedächtnis: im Aufbau.
- CLI, Generator, Layout und Tests: im Aufbau, erst nach tatsächlicher Verifikation als funktionsfähig markieren.
- Kein veröffentlichtes Buch, keine realen Marktdaten.
- Keine realen Kauf-/KDP-Konten verbunden.

## Akzeptanzkriterien Phase 1
1. `python -m pytest` grün.
2. Beispiel-Sudoku mit eindeutigen Lösungen und Duplikatkontrolle.
3. Reproduzierbare Innen-PDF plus Maschinen-QA und Manifest.
4. PDF-Maße, Seitenzahl und Schrifteinbettung prüfen.
5. Menschliche Sichtprüfung bleibt offen; Ausgabe als DRAFT markieren.

## Offene Risiken
- Echte Marktnachfrage nicht validiert.
- Regeln können sich ändern; keine automatische Rechtsgarantie.
- Produktionsabhängigkeiten/Schriftdateien zwischen Macs verschieden.
- Nutzungsrechte externer Assets kontrollieren.
