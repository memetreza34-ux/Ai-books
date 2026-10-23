# Händler- und Wirtschaftlichkeitsprüfung: drei Buchnischen in Deutschland

**Datum:** 2026-10-23 · **Datenstatus:** Händlershop-Seiten am 2026-10-23 manuell mit öffentlicher Recherche eingesehen; Analyse durch Code in GitHub Actions.
**CI-Beweis:** [Actions #39896777677](https://github.com/memetreza34-ux/Ai-books/actions/runs/39896777677), Artefakt \`ai-books-sudoku-draft\`, darin \`market-REVIEW.json\`.
**Code/Datendatei:** [MARKET-REVIEW](../docs/MARKET-REVIEW.md) und [retailer-observations-de.json](../examples/retailer-observations-de.json).

## Verifizierte Produktstichprobe – kein Marktquerschnitt

| Buchnische | Öffentliche Händlerangebote und Beobachtung | Angebote | Endkundenpreis inkl. Steuer |
| --- | --- | --- | --- |
| Sudoku Großdruck | [Thalia 200 Rätsel](https://www.thalia.de/shop/home/artikeldetails/A1081911915) 144 S., 12,90 €; [Hugendubel 365 Rätsel](https://www.hugendubel.de/de/taschenbuch/k_d_thomas-sudoku_leicht_365_raetsel-52705806-produkt-details.html) 240 S., 19,99 €; [Thalia Großdruck Band 1](https://www.thalia.de/shop/home/artikeldetails/A1069945023) 224 S., 3,99 € | 3 | 3,99–19,99 € |
| Mathematik, Klasse 2 | [Thalia Mathe üben](https://www.thalia.de/shop/home/artikeldetails/A1078755140) 48 S., 6,95 €; [Thalia Basiswissen Mathematik 2](https://www.thalia.de/shop/home/artikeldetails/A1035225126) 64 S., 8,90 € | 2 | 6,95–8,90 € |
| Kinder-Labyrinthe | [Thalia Durch den Wald](https://www.thalia.de/shop/home/artikeldetails/A1074829632) 64 S., 8,95 €; [Hugendubel Rätselblock ab 4](https://www.hugendubel.de/de/taschenbuch/agnes_spiecker-raetselblock_ab_4_jahre-42380895-produkt-details.html) 64 S., 8,90 € | 2 | 8,90–8,95 € |

Rangangaben einzelner Händler (z. B. Thalia-Basiswissen 952 oder Labyrinthe „Durch den Wald“ 43240 bei Abruf) sind **Momentaufnahmen ohne ableitbare monatliche Verkaufszahlen**. Angebote sind nicht zwingend KDP-Bücher; Aufmachung, Papier, Bindung, farbiger Inhalt und Druckumfang sind verschieden. Die Stichprobe ist klein und nicht zufällig.

## KDP-Szenarien – keine Verkaufsvorhersage

Offizielle Quellen, Abruf 23.10.2026: [Amazon.de Druckkosten](https://kdp.amazon.com/de_DE/help/topic/G201834340), [Tantiemen](https://kdp.amazon.com/de_DE/help/topic/G201834330).

| Entwurfsformat | Seiten | Rechnerischer Druckkostenwert für große Schwarz-Weiß-Prints | Beispielhafter eigener Netto-Listenpreis (vor ggf. MwSt.) | Rechnerische KDP-Tantieme nach Druckkosten |
| --- | ---: | ---: | ---: | ---: |
| Sudoku | 144 | 3,05 € | 12,99 € | 4,74 € |
| Mathematik | 96 | 2,48 € | 11,99 € | 4,71 € |
| Kinder-Labyrinthe | 96 | 2,48 € | 11,99 € | 4,71 € |

**Achtung:** Rein rechnerische **Tantieme je Direktverkauf vor Steuern, Werbung und sonstigen Kosten**, keine Gewinn-/Absatzschätzung. Nettoeigene Listenpreise sind **nicht** direkt vergleichbar mit Brutto-Endkundenpreisen der anderen Bücher. Druckkosten gelten für **Amazon.de, großes 8,5×11-Zoll-Taschenbuch, Schwarz-Weiß auf weißem Papier**, nicht etwa für Farbbücher, kleine Formate oder Fremdverlage. Für die echten KDP-Einstellungen die Formeln vor Veröffentlichung erneut prüfen.

## Was der Agent jetzt kann
1. Datierten, manuell recherchierten Händlershop-Datensatz einlesen und plausibilisieren.
2. Dubletten, falsche Domains, fehlerhafte Preise und veraltete Beobachtungen ablehnen.
3. Händlerpreise getrennt von KDP-eigenen Netto-Szenarien auswerten.
4. Mathematische KDP-Printkosten und beispielhafte Tantiemen berechnen.
5. Bucharten ausschließlich nach **vorhandener Produktionsbereitschaft** für den **technischen** Pilot sortieren; keine automatisch behauptete Absatzprognose.
6. Bericht im GitHub-Testartefakt hinterlegen und Qualitätsprüfung in CI ausführen.

## Entscheidung
- **Technisches Referenzprojekt:** Sudoku bleibt Platz 1; bereits weitgehend funktionsfähiger, deterministisch prüfbarer Generator. Das sagt **nichts** über tatsächliche Nachfrage.
- **Kommerzielles Siegerbuch:** derzeit **nicht seriös festlegbar**. Die Marktdaten belegen Angebote und Preise, nicht eine robuste Erwartung an Verkäufe.
- **Kommerzieller Status:** alle drei Kategorien **HOLD**.

## Nächste Forschung
- Reale aktuelle Nachfrageindikatoren aus geeigneten und zulässigen Datenquellen ergänzen. Minderwertige Rankings ausdrücklich nicht in Bestellungen umrechnen.
- Überprüfbare Leserprobleme, Nischenpositionierung, Qualitätslücken und starke Differenzierungsmerkmale statt massenhafter Nachahmung identifizieren.
- Für den gewählten Pilottitel Druck-/Coverdesign, altersspezifische Nutzbarkeit, rechtsklare Assets, Qualität, Probedruck und offizielle KDP-Freigaben nachvollziehen.
- Händlerdaten lassen sich mit künftigen **genehmigten** offiziellen Datenanbindungen aktualisieren; automatisiertes HTML-Scraping ist nicht implementiert.
