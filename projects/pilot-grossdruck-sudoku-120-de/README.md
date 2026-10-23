# Erstes vollständiges Pilotbuch: Sudoku im Großdruck

**Produktstatus:** bewusst **HOLD / INTERNER ENTWURF**. Ein vollständiges Buch-PDF wird als technisches Produkt geliefert; das ist **keine Freigabe zur Veröffentlichung**.

## Festgelegtes Konzept
- 120 deterministisch generierte Sudoku, eindeutige Lösungen (jedes durch Algorithmus geprüft).
- Format 8,5 × 11 Zoll, ein großes 9×9-Rätsel pro Seite.
- Je Lösungsseite nur **zwei** größere Lösungsraster statt vier kleinen.
- Deutsch, Schwarz-Weiß, weißes Papier; Buchrücken und Umschlaggröße dynamisch.
- **184 Innenseiten** geplant: drei Einstiegseiten + 120 Rätsel + 60 Lösungsseiten + eine Notizseite.
- Zielgruppe: Erwachsene mit Wunsch nach lesbarem, großzügigem Layout. **Keine unbewiesene Einstufung als "leicht", "Anfänger" oder "barrierefrei".**
- Wettbewerb stark (u. a. 200-Rätsel-Band für 12,90 € und 420-Rätsel-Band für 12,99 €). Kein Nachfrage-/Verkaufsvorsprung nachgewiesen.

## Start mit Antigravity, Codex oder Terminal

```bash
python -m pip install -e '.[dev,preview]'
python -m aibooks book \
  --spec projects/pilot-grossdruck-sudoku-120-de/book-spec.json \
  --out output/pilot-grossdruck-120 \
  --previews
```

Für GitHub: [Actions → Full-Length Editorial Pilot Book](../../actions/workflows/pilot-book.yml) (bei Änderung am Workflow automatisch, danach mit `Run workflow` manuell). Vollständige PDFs, Cover, Metadatenentwurf, Produktionsplan, JSON-Sudoku, Qualitätsbericht, Manifest, Vorschaubilder werden als Artefakt hochgeladen.

## Wirtschaftlichkeit – ausdrücklich hypothetisch

Druckkosten für großes SW-Taschenbuch auf Amazon.de laut KDP-Richtwert vom 23.10.2026: `0,75 € + 0,016 € × 184` = **3,694 €**. Bei **12,99 € KDP-Netto-Listenpreis** und **60 %** Tantiemen ergibt sich `0,60 × 12,99 – 3,694` = ca. **4,10 € je verkauftem Exemplar** vor übrigen Kosten und Steuern. Keine Aussage darüber, ob und wie häufig jemand kauft. KDP-Werte vor Upload live bestätigen, ggf. MwSt. berücksichtigen.

## Explizite Blocker
1. Vollständige redaktionelle und visuelle Prüfung **aller** 184 Seiten, Cover-Preview und ggf. Probedruck.
2. Echte Nachfrage-Indikatoren und klarer, nicht bloß generischer Käufernutzen. Bestehende Konkurrenz kann größer und günstiger sein.
3. Sicherer Nachweis, dass 120 Puzzles hinreichend verschieden sind; bisher nur exakter Puzzle-Hash, keine umfassende Prüfung der strukturellen Isomorphie.
4. Schwierigkeitsbewertung, falls später beworben; Anzahl Vorgaben ist **kein** valider Schwierigkeitsbeweis.
5. Vollständiger offizieller KDP-Cover-Calculator-Abgleich, KDP Previewer, Recht und AI-Offenlegung, Autor/Imprint und Preisfreigabe.
6. Kein automatischer Amazon-Upload und keine bezahlte Werbung.

## Wartung
Jeder Agent liest zunächst `AGENTS.md`, `gehirn/00-START-HIER.md` und `gehirn/09-STATUS.md`; verbessert das Modul nachvollziehbar, behebt Ursachen und ergänzt Tests. Buch-Spec ist versioniert; PDFs stehen nur in GitHub Actions oder lokal `output/`, nicht im Git-Quellcode.
