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


## 2026-10-22 – Unbenutzte Helvetica-Ressourcen (lokal reproduziert)
- **Symptom:** Ein erster PDF-Preflight markierte die von ReportLab automatisch deklarierte Helvetica-Ressource als nicht eingebettet, obwohl sie keinen sichtbaren Text zeichnet.
- **Ursache:** Ressourcentabelle /Font enthält auch unbenutzte Fonts; reiner Ressourcentest ist zu streng.
- **Korrektur:** Fonts der tatsächlich gerenderten Text-Spans mit PyMuPDF ermitteln und deren eingebettete Font-Daten unabhängig prüfen.
- **Regression:** Absichtlich tatsächlich mit Helvetica gezeichneter Text wird blockiert; korrekt eingebettete Vera-Zeichen passieren.
- **Lehre:** QA-Checks brauchen Positiv- **und** Negativtests, um Scheinsperren und Scheinerfolge zu vermeiden.

## 2026-10-22 – Reale Sichtprüfung fand PDF-Titelmismatch
- **Symptom:** Variable Buchtitel erschienen auf dem Umschlag, im Innenteil nur fest eingebautes „SUDOKU“.
- **Ursache:** Cover/Innenlayout nutzten unterschiedliche Titelquellen und die Maschine verglich nur Dateimaße.
- **Fix:** Innen-Cover vereinheitlicht, lesbarer zweizeiliger Titelsatz, getrennte Frontcover-Extraktion (Textsortierung in kompletten Umschlägen verschachtelt Rück-/Fronttext).
- **Regression:** Custom-Titel wird in beiden PDFs nachgewiesen; erwartete Anzahl Rätsel und Lösungsüberschriften automatisiert abgeglichen.
- **Nebenbefund:** Die letzte Notizseite war ohne Schreiblinien; nun auf beiden Notizseiten Linien.
- **Lehre:** Qualität ist nicht nur lesbare PDF, sondern inhaltliche und grafische Einheitlichkeit; automatische Positiv-/Negativtests erforderlich.

## 2026-10-22 – Pflicht-Abhängigkeit falsch klassifiziert
- **Symptom:** PDF-Prüfer und Editorialmodul verwenden PyMuPDF; Paket war nur im Preview-Extra gelistet.
- **Fix:** PyMuPDF als erforderliche Abhängigkeit festgelegt; separater CI-Basisinstallations-Smoke-Test.
- **Lehre:** CI muss nicht nur mit sämtlichen Extras, sondern auch mit dokumentierter Minimalinstallation laufen.
