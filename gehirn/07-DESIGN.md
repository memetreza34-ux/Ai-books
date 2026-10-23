# Gestaltung und Druckgestaltung

- Jedes Buch benötigt genrepassendes Designsystem: Typografie, Kontrast, Seitengitter, Schrifthierarchie, visuelle Abwechslung und echte Nutzbarkeit.
- Mehrere Covervorschläge für kommerzielle Projekte; Auswahl auf Lesbarkeit in Thumbnail-Größe, Genre-Signale, Originalität und korrektes Titelversprechen.
- Schwarz-Weiß-Innenausgabe ist nicht zwingend: Farbe, Papier, Umfang und Format werden nach Nutzen/Kosten gewählt.
- Farben und Abbildungen brauchen geeignete Druckauflösung, sichere Lizenzen und klare Quellen.
- Für Print: einseitige PDF-Seiten, innen/außen gespiegelte Sicherheitsabstände, eingebettete Fonts, Beschnitt nur wenn vorgesehen.
- Kein automatisch generiertes Cover als KDP-konform markieren, bevor die **exakte** KDP-Covervorlage für Papierart, Drucktyp und tatsächliche Seitenzahl bestätigt ist.
- Immer digitale Ganzbuch-Vorschau und visuelle Auffälligkeitskontrolle; erforderlichenfalls Probedruck.
- Nie Layout mit auf dem Mac nicht verfügbaren Schriftarten stillschweigend als druckfertig deklarieren.

## Designsystem v1 (23.10.2026)
Aktuelle Implementierung: [DESIGN-SYSTEM-v1.md](../docs/DESIGN-SYSTEM-v1.md). Alle Nachfolgeagenten **müssen** die Regeln gegen einen gerenderten PDF-Vorschaubogen prüfen. Palette und Layout in `cover.py`; Satzsystem in `layout.py`. Drei Varianten: `editorial`, `blueprint`, `noir`; dafür dieselben Sudoku und dieselbe Umschlaggeometrie. **Keine automatisierte Verkaufsfreigabe.**
