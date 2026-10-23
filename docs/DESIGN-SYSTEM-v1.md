# Designsystem v1 – Sudoku im Großdruck

**Status:** Gestaltungsexperiment, nicht fertiges Marken- oder KDP-Druckdesign. Aktualisiert 23.10.2026.

## Leitidee
Der Leser sieht ein ordentliches, ruhiges und korrekt gestaltetes **Arbeitsbuch**, keine generisch erzeugte KI-Bildfläche. Inhalt, Cover und Listing müssen exakt dieselben überprüfbaren Vorteile benennen. Keine erfundenen Imprintnamen, Testimonials, Schwierigkeitslabels oder Erfolgsversprechen.

## Drei unterschiedlich positionierte Cover

| Code | Richtung | Farbkonzept | Komposition | Positionierung |
|---|---|---|---|---|
| `editorial` | Helle Edition | Papierweiß, dunkles Petrol, Terrakotta | Bewusst viel Weißraum; klare Typohierarchie, klassisches Gittermotiv | Ruhige hochwertige Anmutung |
| `blueprint` | Technischer Rastersatz | Tiefblau, Himmelblau, warmer Akzent | Technische Rasterlinien als dezente Konstruktion, helle Aufgabenkarte | Logik/Präzision |
| `noir` | Typografischer Sammlerlook | Graphit, warmes Weiß, Kupfer | **120** groß als Fokus, kleineres Raster darunter, Outline-Rahmen | Reduziertes, markantes Premiumgefühl |

**Wichtig:** Die Varianten sind tatsächlich unterschiedliche Layouts, nicht nur dieselben Pixel in anderen Farben. Der neue PDF-Generator nutzt für den typografischen Noir-Entwurf eine eigene Kompositionsfunktion. Keiner der Entwürfe wird ohne Nutzerentscheidung zum finalen Marken-Cover erklärt.

## Reproduzierbarkeit

```bash
python -m pip install -e '.[dev,preview]'
python -m aibooks book \
  --spec projects/pilot-grossdruck-sudoku-120-de/book-spec.json \
  --out output/design-study-120 \
  --previews
```

Die Ausgabe enthält:
- `cover-WRAP-DRAFT.pdf` – momentan ausgewählter Entwurf
- `cover-CONCEPT-editorial.pdf`, `cover-CONCEPT-blueprint.pdf`, `cover-CONCEPT-noir.pdf`
- `previews/cover-concept-*.png` – gerenderte vollständige Umschläge
- `previews/cover-comparison.png` – zugeschnittene Vorderseiten nebeneinander
- `interior-DRAFT.pdf`, 31 kontaktbogenartige Vorschauen aller 184 Seiten
- `quality-report.json`, `manifest.json`, `production-plan-DRAFT.json`

Die drei Cover nutzen **denselben** verifizierten Rätselsatz und dieselbe Seitenanzahl. Varianten, PDF-Dimensionen, Einbettung und Titel werden pro Cover technisch geprüft. Ein neues Cover ändert niemals stillschweigend den Buchinhalt.

## Satzsystem für Innenseiten
- Endformat 8,5 × 11 Zoll, schwarz-weiß, ohne Beschnitt – Druckprofil exakt dokumentiert.
- Rand-/Bindungssicherheit wird über `preflight.py` maschinell geprüft.
- Links ausgerichtete Titelseite: kleines Editionslabel, klares Titelraster, sichtbare Rätselanzahl, **keine** fiktive Schwierigkeitsbewertung.
- Ein standardisierter Seitenkopf: schmale Akzentlinie, Bereichsbezeichnung und darunter zurückhaltende Trennlinie.
- Kleiner, sachlicher Seitenfuß: laufende Seitenzahl und `ENTWURF`; keine künstliche Marke.
- **Ein großes 9×9-Rätsel pro Seite**; ohne unnötige Bilddekorationen im Schreibbereich.
- Für Großdruck: zwei Lösungen je Seite, größere Ziffern; die konkreten Rasterabstände sind Regressionstests unterworfen.
- Eingangsseiten vermeiden unnötige AI-Selbstdarstellung und enthalten echte Sudoku-Regeln.
- Platz für handschriftliche Lösungen und Notizen nicht von Zierelementen belegen.

## Qualitätsgates (automatisiert)
1. PDF öffnet sich und alle Seiten weisen Format/Seitenzahl auf.
2. Verwendete Fonts im PDF eingebettet.
3. Keine außerhalb der Sicherheitsränder liegende Textelemente.
4. Vorderseite, Titelblatt, Manifest und Metadaten stimmen bei Buchname und Rätselanzahl überein.
5. Jede Aufgabenüberschrift und jede Lösungsnummer genau einmal in der richtigen Reihenfolge.
6. Gleiche Buchseitenzahl / Rückenbreite bei jeder Covervariante.
7. PDF-Cover unterscheiden sich technisch und haben eigene Preview-Dateien; der Sammelvergleich wird erzeugt.
8. Kein `GO`, keine Werbung, kein automatischer KDP-Upload; `HOLD` und Probedruck bleiben verbindliche Sperren.

## Qualitätsgates (ausdrücklich **nicht** automatisiert)
- Thumbnail-Lesbarkeit bei echten 120–200 Pixel Breite, in Schwarz-Weiß/Vorschauansichten.
- Deutsche Sprache, Orthografie, Wortwahl und tatsächliche Leserpräferenz.
- Farbwirkung auf realem Papier, Drucktoleranzen, ISBN-Barcode und Rücken.
- Vorlagen-Abgleich im KDP Cover Calculator und KDP Previewer.
- Prüfung **jeder** Buchseite und **jeder** Covervariante durch einen Menschen; aktuell nur Stichprobenvisibilität.
- Prüfen, ob Titel, Erscheinungsbild und Logo frei von Rechteverletzungen sind; tatsächliche KDP-KI-Offenlegung.
- Konkurrenzdifferenzierung, Qualitäts-Rückmeldungen und Umsatzpotenzial.

## Prüfmaßstab für Anti-Slop
Für jede neue Buchart durch Agenten prüfen:
1. **Zweck:** Jeder grafische Bestandteil muss Lesen, Orientierung, Marke oder Inhalt dienen.
2. **Konsistenz:** Abstände, Hierarchien, Schriften und Seitenränder bleiben reproduzierbar.
3. **Echtheit:** Keine erfundenen „Bestseller“, Schwierigkeitsversprechen, echten Rezensionen oder Verlagsangaben.
4. **Produktqualität:** Rätsel/Lösungen separat sachlich verifiziert; Design ersetzt keine Qualität.
5. **Auswahl:** Mindestens drei ernsthaft unterschiedliche Entwürfe, nicht nur Farbvarianten.
6. **Abnahme:** Menschliche Freigabe vor jeder Veröffentlichung und Geldausgabe.

## Nächste gestalterische Iteration
Den Sammelvergleich auf Mobilgröße testen und schwächere Entwürfe gezielt nacharbeiten. Ein stimmiges Imprint und echte Markenidentität fehlen noch; diese nicht ohne Eigentümerfreigabe erfinden.
