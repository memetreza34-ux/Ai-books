# Aktueller Projektstatus

**Stand: 2026-10-22; Vorhaben Live-Katalogrecherche implementiert, aktueller CI-Nachweis siehe Actions.**

## Neu: Live-Katalogrecherche (Phase P3, Teil 1)
- Offizielle Katalog-APIs Open Library + Apple Books, maximal drei Themen pro Lauf, Quellenzeitstempel, Hash, Cache, Drosselung und sicheres Fehlermanagement.
- CLI: `aibooks research --input examples/research-niches.json --out output/research-live.json`.
- GitHub Actions: `Live Book Catalog Research` startet beim erstmaligen Hinzufügen der Workflow-Datei und später manuell per `Run workflow`.
- **Keine Nachfrageschätzung**: Ergebnisse bleiben ausdrücklich `HOLD`.
- CI-Tests mit simulierten API-Antworten sind vorgesehen; tatsächliche Laufzeitdaten aus dem GitHub-Workflow gesondert prüfen.

## Bestätigt und getestet
- Dynamische Innen-/Covertitel und automatischer Abgleich von Titel, Rätselanzahl, Aufgaben- und Lösungsköpfen.
- Cover-PNG und zusätzliche Linien auf der letzten Notizseite.
- 20 grüne Tests (inklusive Positiv- und Negativtests für Editorial-Metadaten).
- Erste echte Konkurrenzprüfung für deutschsprachige Sudoku-Bücher: [Research](../research/2026-10-22-sudoku-de.md), kommerzielles Ergebnis HOLD.
- Projekt-Gehirn, `AGENTS.md`, genrebezogene Vorgaben für zehn Bucharten.
- Sudoku-Generator mit mathematisch eindeutigen Lösungen und Dupplikatprüfung.
- Innen-PDF und **echter vollständiger Umschlag** (Rückseite/Rücken/Vorderseite) als DRAFT.
- Cover für B&W 8.5×11 Zoll auf **weißem und cremefarbenem Papier**, Cover-Beschnitt, Barcode-Freiraum, kein Rücken-Text.
- Technische Vorprüfung: Seitenformate, Seitenzahl, tatsächliche Rückenbreite, Textabstände, verwendete eingebettete Schriften.
- Negativtests: falsches Cover-Papierprofil und nicht eingebettete Schriften werden blockiert.
- Kontaktbogen aller Seiten, QA-Report und Manifest mit Dateihashes.
- Lokaler Evidenz-Bewertungsprozess `aibooks evaluate`: GO/HOLD-Alternativen ohne erfundene Umsatzzahlen; nur `CANDIDATE_FOR_HUMAN_REVIEW`, `HOLD`, `REJECT`.
- Vorheriger GitHub-CI-Testlauf: **17 Tests bestanden**, Testband mit **28 Rätseln, 40 Innenseiten** erzeugt und als Workflow-Artefakt hochgeladen.

## Offene Punkte – keinesfalls als erledigt darstellen
1. Keine reale Nachfrage/Marktstudie, keine verifizierten Verkäufe.
2. Katalog-API-Recherche implementiert, aber **kein autonomer vollständiger KI-Browser-Rechercheagent**, keine KI-API-Anbindung oder Multi-Agent-Orchestrierung. Keine unabhängigen Nachfragedaten.
3. Noch keine qualitätsgeprüften und implementierten Generatoren für weitere neun Bucharten.
4. [Visuelle Teilprüfung und Nachkontrolle](../quality/2026-10-22-sudoku-review.md) an altem und korrigiertem Artefakt; keine vollständige visuelle Freigabe oder Probedruck.
5. Kein Abgleich des Covers mit dem konkreten offiziellen KDP Cover Calculator Template, keine KDP-Preview und keine Amazon-Freigabe.
6. Keine selbstständige Veröffentlichung, kein Werbekonto.
7. Verlage/Pseudonyme/Mehrsprachigkeit/weitere Plattformen erst später.

## Nächste Entwicklungsprioritäten
1. Neues Cover und **alle** Innen-Seiten aus dem aktuellen GitHub-Artefakt kontrollieren; Abgleich mit offizieller KDP-Template-Vorlage.
2. Katalog-Ergebnis prüfen, anschließend **echte Nachfrage- und Preisbelege** recherchieren; `evaluate` nur mit überprüften Daten füttern.
3. Ein kaufwürdiges Pilotbuch mit eigenständiger Marken- und Designqualität erstellen; nicht nur Testseiten.
4. Weitere Generatoren nach belegtem Bedarf hinzufügen.
5. Analyse realer Verkäufe, Verbesserungsprotokoll und sichere Skalierung.

**Letzter bestätigter CI-Lauf vor diesem Dokumentations-Commit:** https://github.com/memetreza34-ux/Ai-books/actions/runs/39810964648

## API-Live-Test am 22.10.2026
- Erste echte Recherche lieferte über Open Library verifizierbar abgerufene Katalogdatensätze, aber Google Books antwortete dreimal mit HTTP 429 (Rate Limit).
- Dauerhafte Korrektur: Google ohne API-Key **nicht weiter abfragen**; Apple Books als zweiter öffentlicher Katalog, mit Schutz gegen wiederholte 429-Anfragen.
- **Keine** aus Katalogzahlen abgeleiteten Verkaufs-/Nachfrageangaben. Apple-Preise gelten nur für E-Books, nicht KDP-Print.


## Erfolgreiche API-Recherche nach Anbieterwechsel (22.10.2026)
- [Workflow #39813832909](https://github.com/memetreza34-ux/Ai-books/actions/runs/39813832909) lief erfolgreich mit Open Library **und** Apple Books.
- Sudoku Großdruck: 10 passende Katalogdatensätze; Mathe Grundschule: 4; Kinder-Labyrinthe: 7. **Keine** Rangfolge nach Kaufnachfrage möglich.
- [Persistenter Kurzbericht](../research/2026-10-22-live-catalog-de.md) angelegt. Vollständiger Quellen-JSON-Bericht liegt im Workflow-Artefakt.
- [CI #39813832724](https://github.com/memetreza34-ux/Ai-books/actions/runs/39813832724): **32 Tests bestanden**, Buchproduktion und minimale Installation ebenfalls erfolgreich.
- Weitere Belege zu realer Nachfrage, Preisen und Buchqualität fehlen weiterhin. Kein GO.

## 2026-10-23 – Händlerstichprobe und KDP-Kostenmodell
- Echte Einzelangebote bei Thalia und Hugendubel für Sudoku, Grundschul-Mathe und Kinder-Labyrinthe geprüft, mit Produktlink, inkl.-MwSt.-Preis, Seitenzahl und Erfassungsdatum.
- Neue CLI `aibooks market`: Eingabefelder/Quellen prüfen, Brutto-Händlerpreise vergleichen, KDP-Printszenarien mit explizit **netto** angesetzten eigenen Listenpreisen kalkulieren. Daten werden im Code nicht live nachgeladen.
- `engineering_readiness` ordnet nur technischen Pilotnutzen, **keine** Verkaufs-/Gewinnrangfolge. Alle drei kommerziell `HOLD`.
- KDP-Kosten vom 23.10.2026: großes Schwarz-Weiß-Buch Amazon.de 24–110 Seiten 2,48 €, darüber 0,75 € + 0,016 €/Seite. 50/60-%-Tantiemen nach aktuellem KDP-Listenpreis. Dokumentation: [MARKET-REVIEW](../docs/MARKET-REVIEW.md).
- Weiter **nicht erledigt:** unabhängige Nachfragemessung, automatisch lizenzierter Händler-API-Zugang, vollständige Rentabilitätsrechnung, fertiger Verkaufsband, Veröffentlichungsfreigabe.
