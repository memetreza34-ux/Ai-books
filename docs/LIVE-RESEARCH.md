# Automatischer Live-Katalog-Researcher – Version 1

Der Recherche-Agent kann **echte Buchkatalog-Daten über offizielle öffentliche Schnittstellen** abrufen, verarbeiten, Quellen und Zeitpunkte protokollieren sowie mehrere Nischen vergleichen.

## Quellen und Grenzen
- [Open Library Search API](https://openlibrary.org/dev/docs/api/search): Werke, Titel, ggf. Erstveröffentlichungsjahr, Editionen. Die `lang`-Angabe bevorzugt Deutsch, garantiert es aber nicht.
- [Apple Books Search API](https://performance-partners.apple.com/search-api): Titel, Autor, ggf. E-Book-Preis und Erscheinungsdatum. Apple liefert **E-Books**, keine Amazon-KDP-Taschenbuchangebote; Preise dürfen nicht als Taschenbuchpreise verwendet werden.
- **Keine Kaufzahlen, kein Suchvolumen, keine KDP-Verkaufsschätzung, keine Store-Preise.** Ein Katalogtreffer ist kein lieferbares Kaufangebot. Die kataloginterne Gesamtzahl ist **keine** aktuelle Konkurrenz- oder Absatzmenge.
- Pro Lauf höchstens drei Nischen, je eine Anfrage pro Anbieter. Kein HTML-Scraping, keine ungeprüften Download-Links. Keine externen KI-API-Kosten.

## Auf MacBook
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
aibooks research --input examples/research-niches.json --out output/research-2026-10-22.json --cache-dir output/catalog-cache
```

Netzwerk wird **nur beim ausdrücklichen `research`-Aufruf** verwendet. Ergebnisse und Zeitstempel landen in JSON. Falls die APIs nicht erreichbar sind, wird der Fehler beim jeweiligen Anbieter dokumentiert, statt erfundene Ergebnisse zu erzeugen. Cache-Haltbarkeit sieben Tage; eine erneute Recherche nach Ablauf benötigt einen neuen Ausgabepfad. Vorhandene Ausgaben werden nicht überschrieben.

Optional für Open Library: `AIBOOKS_CONTACT_EMAIL` als Umgebungsvariable setzen, falls du möchtest, dass bei Anfragen ein Kontakt angegeben wird. Niemals private E-Mail-Adressen oder Zugangsdaten im Git-Repository veröffentlichen.

## Ohne eigenes Terminal
In GitHub: **Actions → Live Book Catalog Research → Run workflow**. Der Testlauf nutzt höchstens sechs API-Anfragen zu drei Ausgangsnischen. Das Resultat liegt als herunterladbares `ai-books-catalog-research`-Artefakt vor. Das ist kein automatisches oder dauerhaft geplantes Monitoring. Enthält keine Veröffentlichung und keine Werbeausgaben.

## Aussagekraft
Alle Nischen bleiben `HOLD`, auch wenn Daten von beiden Quellen erfolgreich eingelesen werden. Für eine Geschäftsentscheidung müssen zusätzlich nachweisbare Such-/Kaufindikatoren, aktuelle Händlerpreise, Rechteklärung und eine nachvollziehbare Tantiemenrechnung erhoben werden. Der vorhandene `aibooks evaluate`-Scorer ist ein **separater** Schritt; dieser Live-Kataloglauf schiebt keine scheinbar verifizierten Nachfragedaten in den Scorer.

## Stabilität/Sicherheit
Abfragezeitbegrenzung, begrenzte Datenmenge, Domain-Allowlist, Open-Library-Drosselung, Cache und Tests mit künstlichen Antworten. Der aktuelle Agent ist eine **autonom laufende Quellenabfrage**, kein vollständiger KI-basierter Browser-Agent und ersetzt keine menschliche Markteinschätzung.
