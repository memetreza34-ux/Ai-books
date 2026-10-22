# Dauerhaftes Fehlergedächtnis

Jeden beobachteten Fehler mit Datum, Ursache, Reproduktion, Fix und Regressionstest erfassen.

## Tatsächliche Beobachtung: 2026-10-22
- **Codewarnung:** PyMuPDF meldete die Legacy-Schnittstelle `fitz` als veraltet.
- **Maßnahme:** Vorschaumodul und Vorschau-Test auf `pymupdf` umstellen.
- **Status:** Codeanpassung vorgesehen; CI-Lauf nach Änderung erneut prüfen.
- **Regel:** Bibliotheks-Warnungen nicht verschweigen. Spätere Änderungen auf alte Kontaktbogenqualität regressionsprüfen.

## Vorsorgeregeln, noch keine konkreten Vorfälle
- Keine behauptete eindeutige Sudoku-Lösung ohne unabhängigen Prüflöser.
- Cover-/Titelaussagen stimmen immer mit den echten enthaltenen Aufgaben überein.
- Sprachversionen erneut auf Lösungen, Layout und Rechte prüfen.
- Druckprofil bewusst nach Kosten/Qualität wählen.
- Live-KDP-Regeln vor Veröffentlichung erneut prüfen.
- AGENTS.md, Status und Entscheiderlog schützen Kontext vor Verlust.

## Eintragsvorlage
ID / Datum / Buchtyp / Symptom / Schritte / Ursache / Schwere / Korrektur / Test / Status.
