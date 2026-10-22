# Roadmap mit überprüfbaren Meilensteinen

## P0: Richtige Ausgangsbasis
Gehirn/Agentenregeln, Projektstruktur, saubere Abhängigkeiten, Tests, CI. Akzeptanz: Dokumente auffindbar, Setup nachvollziehbar.

## P1: Sudoku-Referenz
Reproduzierbarer Generator, Unique-Solution-Solver, verschiedene Schwierigkeitsprofile, keine Dubletten, Lösungen, Innen-PDF, Qualitätsbericht, Testdatensatz, Fehlerfälle. Akzeptanz: lokal reproduzierbar, Test-Suite grün, visuelle Durchsicht protokolliert. **Erstes Nutzer-Erfolgskriterium: hochwertige Datei.**

## P2: Layout- und Cover-System
Mehrere echte Designsysteme, Coverentwürfe, berechnetes KDP-Wrap-Cover auf Grundlage offizieller Vorlage, automatisierte Druckchecks und Seitenvorschau.

## P3: Marktprüfung und Buchentscheidung
Nachfrage- und Konkurrenzdaten mit Quellen/Daten; GO/HOLD/REJECT. Fokus wirtschaftlich begründen, nicht nach Bau-Leichtigkeit wählen.

## P4: Weitere Generatoren
Mathematik, Labyrinthe, Wortsuche, Kinderaktivitäten, ABC; danach übrige Bucharten entsprechend Nachfrage/QA-Kosten. Je Modul eigene Tests und Rechteprüfung.

## P5: Mehrsprachigkeit, Marken, Plattformen
Sprachvarianten mit lokaler Neuprüfung; Marken/Pseudonyme; Adapter für rechtlich zulässige Kanäle.

## P6: Analytik und Verbesserung
Import echter Verkaufsberichte, Deckungsbeiträge, Lager/Versionen, Preis-/Cover-Hypothesen, retrospektives Lernen. Werbeausgaben nur mit manueller Freigabe.


### Erledigt am 2026-10-22 (technisch)
- Sudoku-Referenzgenerator, 17 grüne Tests, 40-Seiten-Beispielbuch.
- Full-Wrap-Cover als Entwurf für 8.5×11 B&W (weiß/creme), automatische PDF-Preflight-Gates.
- Evidenzbasierte lokale Buchideen-Bewertung mit transparenten Quellenanforderungen und konservativer HOLD/REJECT/REVIEW-Logik.

### Weiter offen
- Echte Nachfrage-/Konkurrenz-**Recherche**, visuelle Qualitätsabnahme, KDP-Vorlage/Previewer und Probedruck.
- Buchgestaltung bis real verkaufsreife Qualität, Copywriting/Metadaten/Marke.
- Zusätzliche Generatoren und echte Multi-Agent-Anbindung.

## Visuelle Kontrolle und Evidenz (Fortschritt 22.10.2026)
- Alte PDF stichprobenartig visuell geprüft; Titelmismatch und leere letzte Notizseite korrigiert.
- PDF-Textabgleich als verbindliches technisches Gate, längere Titel zweizeilig.
- Aktuelle Sudoku-Konkurrenzangebote aus Thalia/Hugendubel dokumentiert; **kommerzieller Status HOLD**.
- Researcher-Runbook ergänzt; echte autonome Webrecherche weiterhin NICHT implementiert.
- Nächste Abnahme: neues Artefakt optisch überprüfen, KDP-Vorlage/Previewer und echte Nachfrageindikatoren.


## 22.10.2026 – P3 Fortschritt: autonome Katalogabfrage
- Python-Recherchelauf mit zwei **öffentlichen Katalogquellen**, überprüfbaren Request-URLs, Abrufzeit, SHA256 und übersichtlicher Trefferliste implementiert.
- Offen dokumentierte Einschränkungen: Keine Verkäufe, keine Suche nach tatsächlichen KDP-Händlerpreisen und keine Nachfragemetriken.
- GitHub-Actions-Workflow als manuell startbare Recherche. Keine automatische tägliche Überwachung oder kostenpflichtige API.
- Nächste P3-Stufe: unabhängig belastbare Nachfrageindizien, Händler- und Druckkostenbelege, echte qualitative Differenzierung sowie geprüfte Übergabe zum `evaluate`-Scorer.
