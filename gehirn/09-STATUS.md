# Aktueller Projektstatus

**Stand: 2026-10-22; zuletzt bestätigter Build: GitHub Actions #39810381569 (20 Tests bestanden).**

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
2. Noch keine autonome Live-Recherche, KI-API-Integration oder Multi-Agent-Orchestrierung.
3. Noch keine qualitätsgeprüften und implementierten Generatoren für weitere neun Bucharten.
4. Nur [visuelle Teilprüfung](../quality/2026-10-22-sudoku-review.md) am älteren Artefakt; noch keine vollständige visuelle Freigabe oder Probedruck.
5. Kein Abgleich des Covers mit dem konkreten offiziellen KDP Cover Calculator Template, keine KDP-Preview und keine Amazon-Freigabe.
6. Keine selbstständige Veröffentlichung, kein Werbekonto.
7. Verlage/Pseudonyme/Mehrsprachigkeit/weitere Plattformen erst später.

## Nächste Entwicklungsprioritäten
1. Neues Cover und **alle** Innen-Seiten aus dem aktuellen GitHub-Artefakt kontrollieren; Abgleich mit offizieller KDP-Template-Vorlage.
2. Externe aktuelle Nachfrageinformationen **tatsächlich** erheben, Quellen lesen und `evaluate` mit geprüften Daten füttern.
3. Ein kaufwürdiges Pilotbuch mit eigenständiger Marken- und Designqualität erstellen; nicht nur Testseiten.
4. Weitere Generatoren nach belegtem Bedarf hinzufügen.
5. Analyse realer Verkäufe, Verbesserungsprotokoll und sichere Skalierung.

**Letzter bestätigter CI-Lauf vor diesem Dokumentations-Commit:** https://github.com/memetreza34-ux/Ai-books/actions/runs/39810381569
