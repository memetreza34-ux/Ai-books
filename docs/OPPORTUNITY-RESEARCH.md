# Buchideen auswählen: Evidenz statt Verkaufsversprechen

Die CLI `aibooks evaluate --input examples/opportunities-example.json --out output/research.json` bewertet konkrete Buchideen auf Basis **manuell bzw. vom Agenten recherchierter Eingaben**. Das Programm recherchiert NICHT selbst im Internet und prüft keine URLs live. Es darf deshalb keine Nachfrage als bewiesen darstellen.

## Benötigte Scores (0–10, begründet statt geraten)
- demand: 25 %
- reader_value: 20 %
- differentiation: 15 %
- evergreen: 15 %
- profit_potential: 10 %
- production_feasibility: 10 %
- maintenance: 5 %

## Quellen
Mindestens zwei **verschiedene** aktuelle HTTPS-Domains innerhalb von 180 Tagen; eine Quelle zum Nachfrageindikator, eine zur Konkurrenz. Bei fehlenden Belegen bleibt das Ergebnis `HOLD`. Daten zum Umsatz oder Absatz aus Amazon-Rankings nur mit dokumentierter nachvollziehbarer Schätzmethode, sonst unbekannt. Ein subjektiver Score ist niemals eine Umsatzprognose.

`rights_status` = clear/unverified/blocked; `risk_level` = low/medium/high. Bekannte Rechtsblocker führen zu `REJECT`, ungeklärte Quellen, hohe Risiken oder fehlende Nachweise zu `HOLD`. Nur gut belegte und ausreichend bewertete Kandidaten erhalten `CANDIDATE_FOR_HUMAN_REVIEW` – **niemals automatisch GO**.

Ein Agent muss sich bei jeder Angabe auf tatsächliche aktuelle Quellen berufen und diese transparent dokumentieren. Menschen überprüfen die Quellen, die Qualitätskriterien und sämtliche finanziellen/produktrechtlichen Fragen vor der Buchentscheidung.

Beispieldatei ist ausdrücklich **synthetisch** und beschreibt keine reale Marktnachfrage.
