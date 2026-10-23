# Preis-/Konkurrenzanalyse (DE): KDP-Buchideen mit echten Händlerbeobachtungen

## Ausführung

```bash
aibooks market --input examples/retailer-observations-de.json --out output/market-review.json
```

Die Beispieldatei enthält **am 23.10.2026 einzeln überprüfte öffentliche Händlerangebote** für die drei Pilotnischen. Originalseiten stehen in jedem Datensatz. Im CI liegt der JSON-Bericht als `market-REVIEW.json` im normalen Buch-Testartefakt.

Die Software prüft strukturell Produkt-URLs, Preis, Seitenzahl, Dubletten, Altersgrenze (90 Tage) und die Eingabemethode. **Sie lädt diese Händlerwebseiten nicht automatisch herunter und prüft keine tatsächliche Verfügbarkeit.** Browser-/Agenten-Recherche muss Angebote neu öffnen, Daten lesen, den Beobachtungszeitpunkt dokumentieren und erst dann Eingabedaten aktualisieren. Keine automatisierten Scraping-Zugriffe auf Händlershops.

## Wert der Quellen
- **Händlerpreise (Brutto inkl. MwSt.)**: tatsächliche sichtbare Konkurrenz-Listenpreise, keine Verkaufszahlen.
- **Rang auf Händlerseite**: schwacher, momentaner Proxy, plattformspezifisch, niemals in Absatz oder Umsatz umrechnen.
- **Open Library und Apple Books**: Bibliografische bzw. E-Book-Kataloge, nicht automatisch aktuelle gedruckte KDP-Angebote.
- **Tantiemen-Szenarien**: illustrative KDP-Selbstpreise **exkl. Umsatzsteuer**, keine Konkurrenzpreisübernahme. Es gilt für Amazon.de, Schwarz-Weiß, Großformat, weißes Papier, direktes Marketplace-Modell.
- **Keine unabhängigen Suchvolumina, Bestellungen, Conversion Rates oder Nettogewinne**.

## Offizielle Kostenformel, Momentaufnahme 23.10.2026
- Große Taschenbücher 24–110 Seiten Schwarz-Weiß, weiß/creme: **2,48 € Druckkosten** auf Amazon.de.
- Ab 111 Seiten im Modell: **0,75 € + 0,016 € je Seite**.
- Amazon.de direkte Standardtantiemen: bis **9,98 € Netto-Listenpreis 50 %**, ab **9,99 € 60 %**; danach Druckkosten abziehen.
- KDP-Einstellungen, Steuern, Anzeigen und Betriebskosten können das Ergebnis verändern.
- Quellen: [KDP Druckkosten](https://kdp.amazon.com/de_DE/help/topic/G201834340) und [KDP Tantiemen](https://kdp.amazon.com/de_DE/help/topic/G201834330), zusätzlich [KDP Rechner](https://kdp.amazon.com/de_DE/royalty-calculator).
- **Vor echtem Upload alles erneut prüfen**; die Druckkostenmodellierung gilt *nur* für dieses Profil. Niedrigere Verkaufs-/Listenpreise müssen den aktuellen Mindestlistenpreis bei KDP erfüllen.

## Auswahlregeln
Der Report sortiert nach **technischer Umsetzungsmöglichkeit**, weil aus Händlerpreisen und einzelnen Rangpositionen kein belastbarer Nachfragescore berechnet werden kann.
Das bedeutet NICHT, dass Sudoku die profitabelste Kategorie ist.

Jede Kategorie bleibt `HOLD` für eine Verkaufs-/Veröffentlichungsentscheidung. Eine Freigabe braucht mindestens belastbare, unabhängige Nachfrageindikatoren, klare Differenzierung, prüfbare Druckmarge, geprüfte Lizenz-/Sicherheitslage, echte Seiten-/Druckkontrolle und die Entscheidung des Eigentümers.

## Eingabedaten aus dem aktuellen Quellenlauf
- Sudoku: [Thalia 200 Rätsel](https://www.thalia.de/shop/home/artikeldetails/A1081911915), [Hugendubel 365 Rätsel](https://www.hugendubel.de/de/taschenbuch/k_d_thomas-sudoku_leicht_365_raetsel-52705806-produkt-details.html), [Thalia Sudoku Großdruck Band 1](https://www.thalia.de/shop/home/artikeldetails/A1069945023)
- Mathe Klasse 2: [Thalia Mathe üben](https://www.thalia.de/shop/home/artikeldetails/A1078755140), [Thalia Basiswissen Mathematik 2](https://www.thalia.de/shop/home/artikeldetails/A1035225126)
- Kinder-Labyrinthe: [Thalia Durch den Wald](https://www.thalia.de/shop/home/artikeldetails/A1074829632), [Hugendubel Rätselblock](https://www.hugendubel.de/de/taschenbuch/agnes_spiecker-raetselblock_ab_4_jahre-42380895-produkt-details.html)

### Next
Verbesserte und rechtlich freigegebene Handels-API-Konnektoren nur dort ergänzen, wo offizielle APIs/Partnerbedingungen die Abfrage erlauben. Eigene Verkaufszahlen ausschließlich aus vom Eigentümer erlaubten KDP-Berichten importieren; öffentliche Händler-Rankings nicht zu fiktiven Bestellzahlen konvertieren.
