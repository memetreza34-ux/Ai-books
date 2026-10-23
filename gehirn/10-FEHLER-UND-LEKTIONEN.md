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


## 2026-10-22 – Präventive Schutzmaßnahme: Katalogtreffer sind keine Nachfrage
- Bibliografische Suchtreffer dürfen niemals als tatsächliche Verkäufe, aktuelle Shop-Verfügbarkeit, Kundeninteresse oder Profitabilität interpretiert werden.
- Deshalb automatische Entscheidung immer `HOLD`, inklusive Quellenstatus, Zeitstempel, Query, Filter und Rückmeldungen fehlgeschlagener Anbieter.
- Alle Provider-Zugriffe sind auf zwei feste APIs eingeschränkt. Keine HTML-Scraper oder Anbindung an KDP-Konten.


## 2026-10-22 – Google Books HTTP 429 in echtem API-Lauf
- Symptom: Alle drei Google Books-Kataloganfragen lieferten HTTP 429 (Rate Limit), Open Library hingegen funktionierte.
- Ursache: kostenloser anonymer API-Zugang nicht zuverlässig, möglicherweise auch durch geteilte Runner-IP.
- Korrektur: Google Books durch die offizielle Apple Books Search API ersetzt; Schutzmechanismus stoppt Folgeanfragen nach HTTP 403/429.
- Nachweis: Workflow #39813832909, beide neuen Katalogquellen antworteten erfolgreich.
- Erkenntnis: Bibliografische Treffer sind keine Verkaufsmengen und keine Nachfrageindikatoren. Providerfehler dürfen nicht als 0 Marktangebot interpretiert werden.

## Präventionsregel 2026-10-23 – Preisbeobachtung vs. KDP-Tantieme
- **Risiko:** Vergleich von Händler-Endkundenpreisen inkl. MwSt. mit eigenem KDP-Netto-Listenpreis ohne Steuerumrechnung.
- **Schutz:** Datenfeld `consumer_price_eur_including_vat` getrennt von `list_price_before_vat_eur`; alle Szenarien als hypothetisch markieren.
- Händler-Rankings sind relative, zeitabhängige Plattformwerte und dürfen nicht in Monatsumsatz umgerechnet werden.
- Eingeschränkte Domain-Allowlist, Nachweise höchstens 90 Tage alt, keine implizite URL-Live-Verifikation und keine Überschreibung alter Berichte.

## 2026-10-23 – Markt-Modul Regressionstests / datentypische Fehler
- **Beobachtung im ersten CI:** zwei Tests rot, weil Python-`Decimal` mit binärem `float` statt `Decimal` verglichen wurde und ein Feld-Schlüssel gegen das Dictionary selbst statt via Key abgefragt wurde.
- **Korrektur:** Decimal-Vergleiche mit dezimalgenauen Literalen, korrektes Feld `consumer_price_eur_including_vat`; zusätzliche Mindestpreis-Regressionssperre gegen negativen Printkostenbeitrag.
- **Nachweis:** [GitHub Actions #39896777677](https://github.com/memetreza34-ux/Ai-books/actions/runs/39896777677) erfolgreich, **46 Tests bestanden**, Base-Install ebenfalls.
- **Lehre:** Finanztests keine binären Floating-Point-Vergleiche; für KDP-Druckrechnung Decimal + explizite Steuerbasis benutzen. Testfehler korrigieren, ohne das Verhalten schönzurechnen.

## 2026-10-23 – Reale Druckvorschau fand typografischen Konflikt
- Ausgangsversion 120-Rätsel-Pilot hatte auf dem Full-Wrap-Cover eine Überlappung von ca. 2,85 pt zwischen zweiter Titelzeile und Untertitel.
- Bei Lösungsseiten standen Beschriftungen ca. 4 pt vom Raster entfernt, visuell fast berührend.
- **Ursache:** Der erste automatische Preflight kontrollierte nur Text-Ränder, nicht **Text-/Text- oder Text-/Illustrationskollisionen** innerhalb der sicheren Seite.
- **Lösung:** Cover-Zeilen umpositioniert (aktuell ca. 21 pt vertikaler Abstand), Lösungsraster auf 268 pt mit freiem Titelbereich und ausreichend Seitenzwischenraum gestaltet.
- **Regressionstests:** `tests/test_typography.py` testet auf reale Textkoordinaten und Grid-Beschriftung; 60 Tests grün im CI.
- **Weiterer Systembedarf:** Allgemeine grafische Kollisionsprüfung für *alle* Bucharten ergänzen; aktuelle Tests decken die neuen bekannten Konfliktarten ab, nicht sämtliche denkbaren Designfehler.

## 2026-10-23 – Designprüfung zu stark auf PDF-Margins konzentriert
- Der erste öffentliche 120-Rätsel-Band war technisch fehlerfrei, wirkte aber generisch – besonders dunkles Cover, Typografie und Produktionshinweise.
- Maßnahmen: drei visuell vergleichbare Designrichtungen, reale Covers als PDF/PNG, Typo/Lesbarkeit, richtiger Inhalt statt dekorativen Fülltexten.
- Korrektur am Inhalts-Gate: Zwei äquivalente erlaubte Textformulierungen für die Rätselanzahl werden erkannt; falsche Zahlen bleiben Blocker.
- Der Vergleich enthüllte, dass Farbvarianten allein noch keine drei Coverkonzepte ergeben. Die Noir-Variante wurde typografisch neu aufgebaut.
- Prävention: Render-basierte Designprüfung und strukturierter `cover-comparison.png`-Export; kein PUBLISHING_READY aus bloßem CI-Erfolg ableiten.

## 2026-10-23 – Thumbnail-Audit: kleine Sudoku-Ziffern beim Noir-Cover unlesbar
- Fehlermuster: PDF-Preflight vollständig grün, aber im `cover-comparison.png` sind die einzelnen Zahlen des 152-pt-Sudoku-Gitters optisch zu gedrängt.
- Fix: Für die typografische Coverrichtung Noir bewusst **leeres Gittermotiv** statt eines scheinbar lesbaren Mini-Puzzles; echte Beispiele bleiben in den zwei anderen Entwürfen.
- Regressionstest `test_noir_motif.py` liest ausschließlich den relevanten Gitterbereich – Zahlen aus `9 × 9`-Beschriftungen dürfen keinen Fehlalarm auslösen.
- Langfristige Lehre: Motive müssen in Thumbnailgröße funktionieren; automatisierte Geometrieprüfungen ersetzen keine visuelle Abnahme.
