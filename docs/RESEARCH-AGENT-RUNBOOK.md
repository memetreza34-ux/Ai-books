# Forschungs-Agent: tatsächliche Evidenz vor Bücherproduktion

## Rollen
- **Researcher** (Antigravity mit geeignetem Browser/Recherchewerkzeug): finde aktuelle Zielmarkt-Daten, verlinke Primärseiten, protokolliere Abrufdatum und Quelle.
- **Independent reviewer** (zweites Modell oder menschliche Prüfung): Öffne und verifiziere kritische Quellen und Zahlen unabhängig.
- **Decision engine** (`aibooks evaluate`): bewerte *vorher belegte* Hypothesen, nicht erfundene Suchvolumina.
- **Owner**: Freigabe oder Ablehnung. Keine Veröffentlichung oder Anzeigen ohne Freigabe.

## Pro Buchidee
1. Zielgruppe, Sprache, Land, Evergreen-/Saisonprofil, konkreten Nutzen definieren.
2. Mindestens fünf relevante bestehende Buchangebote suchen (nach Möglichkeit mehrere Händler); unveränderliche URL, Buchformat, Seitenzahl, Preis, Inhalt, Abrufdatum erfassen. Keine unerlaubte Massenabfrage/Scraping.
3. Nachfrageindizien getrennt erheben, etwa Trends über Jahre, unabhängige Rezensionsthemen und Suchintentionen. **Keine Verkaufszahlen aus Rankings erfinden.**
4. Tatsächliche Unterscheidungsmerkmale beschreiben, nicht nur anderes Cover.
5. Druckprofil und aktuelle KDP-Tantiemen rechnen; Gewinne als Szenarien kennzeichnen.
6. Rechte, sensible Inhalte und rechtliche Anforderungen prüfen; KDP-Normen am Tag der Freigabe erneut öffnen.
7. Beweisdossier erstellen und mit einer Datenqualität markieren: `verified`, `partial`, `assumption`, `unknown`.
8. Score-Datei erstellen, `aibooks evaluate` ausführen und Ergebnis **maximal als überprüfungsbedürftigen Kandidaten** interpretieren. Ohne harte Nachfrageindizien bleibt HOLD.
9. Alle Quellen und Entscheidungen im Repository-Gehirn dokumentieren; nach 180 Tagen Quellen neu prüfen.

## Rote Linien
- Der aktuelle Python-Scorer **besucht URLs nicht selbst**. Dass zwei HTTPS-Domains eingetragen sind, beweist NICHT, dass dort Inhalte gelesen wurden.
- Keine angeblichen KDP-Verkäufe, Umsatzschätzungen ohne nachvollziehbare Methodik, Fake-Rezensionen oder Keyword-Suchvolumen ohne Quelle.
- Kein autonomes Kaufen, Anzeigen-Buchen, Uploaden oder rechtliche Freigaben.
- Kein Marketing auf Basis eines rein technischen Testbuchs.

Referenz: [Sudoku-Marktprüfung Oktober 2026](../research/2026-10-22-sudoku-de.md).


## Ausführbarer Agent (erstes Online-Modul; 22.10.2026)
`aibooks research --input examples/research-niches.json --out output/research-live.json` kann Open Library und Apple Books mit **echten** Katalog-API-Anfragen recherchieren, drei Nischen vergleichen, Quellen-URLs und Abrufzeiten aufzeichnen, Treffer nach Titelbegriffen filtern sowie Ausfälle/Cache behandeln.

**Wichtig:** Dieser Kataloglauf liefert **keine** aktuellen Händlerpreise, Nachfrage-, Absatz- oder Profitabilitätsdaten. Er übergibt bewusst keine generierten Nachfragebelege an den Offline-Scorer. Bis weitere unabhängige Daten vorliegen, lautet die Entscheidung für jede Nische `HOLD`.

[Live-Recherche-Anleitung](LIVE-RESEARCH.md). GitHub Actions erlaubt manuelle Ausführung und speichert das Ergebnis als Artefakt. Kein Dauerbetrieb, keine ungefragten kostenpflichtigen APIs.

**2026-10-22, Quellen-Fallback:** Google Books antwortete im ersten Live-Lauf mit HTTP 429; daher auf Apple Books Store Search API für E-Book-Wettbewerb umgestellt. Beide Plattformen sind für Verkäufe nur **indirekte** Anhaltspunkte. Keine ungeprüfte Druckpreis-Übernahme.
