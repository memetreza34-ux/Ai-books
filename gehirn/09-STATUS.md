# Aktueller Projektstatus

**Stand: 2026-10-23; erster vollständiger 120-Sudoku-Buchentwurf produziert. Kommerziell HOLD.**

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

## Verifizierter Abschluss des Entwicklungsblocks 2026-10-23
- Live-Katalog-Recherche (Open Library / Apple Books) bleibt von echtem Händler-Preisvergleich unterschieden.
- [Händleranalyse mit 7 Produktbeobachtungen](../research/2026-10-23-retailer-market-de.md) und offizieller KDP-Druck-/Tantiemenmodellierung ergänzt.
- CLI `aibooks market --input examples/retailer-observations-de.json --out output/market-review.json` funktioniert; Ergebnisse im CI-Testartefakt hinterlegt.
- **46 Python-Tests grün, inklusive 14 neuer/erweiterter Markt-/Preisprüfungen**, zwei GitHub-Jobs erfolgreich. [Actions #39896777677](https://github.com/memetreza34-ux/Ai-books/actions/runs/39896777677).
- **Kommerzieller Entscheid: HOLD für alle Kategorien; Sudoku bleibt nur technischer Referenz-Pilot.**
- Weiter offen: selbstständige genehmigte Händlerdatenquellen ohne manuelle Quelleingabe, belastbare Nachfragemessung, echte Leserbefragung, publikationsfähige KDP-Datei, Volumen-/Designqualität und manuelle Freigaben.

## Erster vollständiger Buch-Produktionspilot (23.10.2026)
- **Entwickelt:** versionskontrolliertes Briefing `projects/pilot-grossdruck-sudoku-120-de/book-spec.json` und neues CLI `aibooks book --spec ... --out ... --previews`.
- **Fertig gebaut:** 120 einmalig lösbare Sudoku, 184 Innenseiten, 60 größere Lösungsseiten (2 Lösungen pro Seite), Großformat, Cover-Wrap als DRAFT, JSON-Inhalt, Manifest, QA-Bericht, Metadaten und Produktionsplan.
- **Geprüfte CI:** [#39933627153](https://github.com/memetreza34-ux/Ai-books/actions/runs/39933627153) **60 Tests bestanden**; [vollständiger Buch-Build #39933627185](https://github.com/memetreza34-ux/Ai-books/actions/runs/39933627185) erfolgreich und als 14-Tage-Artefakt auf GitHub hochgeladen.
- **Visuelle Teilprüfung:** finale Cover-Linien und Lösungsseiten abgenommen, ursprüngliche Kollisionen korrigiert; [Audit](../quality/2026-10-23-sudoku-120-review.md). Nicht jede Seite wurde einzeln durch Menschen kontrolliert.
- **Geschäftlich:** [Pilotentscheidung](../research/2026-10-23-pilot-sudoku-grossdruck.md) stützt nur technischen Start, kein Nachweis höheren Verkaufspotenzials gegenüber vielen Angeboten mit 200–420 Rätseln.
- **Keine neue Freigabe:** Marktstatus HOLD, keine KDP/Ads, keine Marken-/Imprintfreigabe, kein finaler Veröffentlichungstext, kein Probedruck.
- **Wichtigster nächster Block:** Nicht wahllos weitere Bucharten erzeugen, sondern diesen realen Entwurf systematisch qualitativ verbessern, Marktfeedback einholen, Schwierigkeit und strukturelle Sudoku-Originalität prüfen und KDP-Vorlagenvalidierung.

## 23.10.2026 – Design-Reset für Sudoku (v1)
- Neuer dreiteiliger Umschlag-Generator, `editorial` / `blueprint` / `noir`, mit verschiedenen Kompositionsprinzipien, kontrollierter Typografie und definierten Farbpaletten. Für jede Variante gültige KDP-Geometrie als **Entwurf**, keine KDP-Freigabe.
- Innenlayout: typografisches Titelblatt, klare Zwischenüberschriften, präzisere Einführung und Nutzungserklärung, zurückhaltende Folios.
- `aibooks book` erzeugt 3 separate Cover-PDFs, drei Vorschaubilder und eine Vergleichsgrafik, ohne die 120 Sudoku dreifach zu generieren.
- Schrift, Geometrie, Zählung und Inhalt werden bei **jeder** Covervariante geprüft. Code/Tests/Review und bekannte Einschränkungen in [Designsystem](../docs/DESIGN-SYSTEM-v1.md) sowie [Designaudit](../quality/2026-10-23-design-review.md).
- **Offen:** alle Seiten visuell abnehmen; tatsächlichen KDP-Cover-Calculator-Vergleich/Proof; Auswahl eines finalen Designs, Rechte-/Imprint-Prüfung und echte Zielgruppentests. Markt weiterhin HOLD.
