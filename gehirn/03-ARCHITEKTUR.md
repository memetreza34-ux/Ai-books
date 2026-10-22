# Architektur

## Prinzip
Lokales CLI-first-System für macOS, Python 3.11+, ohne erzwungene KI-API. Einheitliche Buchprojekt-Daten, austauschbare Generatoren, unabhängige Validatoren, Renderer und Publishing-Adapter.

```text
CLI / Buchbriefing
    -> Research Gate (Beleg-/Annahme-Register)
    -> BookSpec (Typ, Sprache, Zielgruppe, Format, Seed, Lizenz-Angaben)
    -> Generator (je Genre separat)
    -> Validator (deterministische Fachtests + KI-Review + Rechteprotokoll)
    -> Layout/Renderer -> PDF/Preview -> QA-Report
    -> Menschliche Freigabe -> Plattform-Paket / manueller Upload
    -> Vertriebsauswertung -> kontinuierliche Verbesserungen
```

## Strukturen
- `src/aibooks/`: Anwendungslogik und CLI.
- `tests/`: schnelle reproduzierbare Tests.
- `gehirn/`: versionierte Entscheidungen, Standards und Status.
- `booktypes/`: Standards je Buchart.
- `examples/`: Test-Briefings ohne Kundendaten.
- `output/`: lokal generierte Dateien, nicht im Git.
- `docs/`: technische Howtos und überprüfbare Quellen.

## Schnittstellen und spätere Erweiterung
- `BookSpec` mit strukturiertem Metadatenvertrag und Versionsfeld.
- Separate Generatoren für Sudoku, Labyrinth, Mathematik, Wortsuche etc.; keine universelle KI-Erfindung von Sudoku-Lösungen.
- Keine hardcodierten Schlüssel, keine Zugriffe auf Konten im Kern.
- Jede Produktion erhält Manifest, Seed, Hashes, Qualitätsbericht, Umgebungs-/Versionsangaben und Audit-Historie.
- Kein 'READY' bei unvollständiger Rechtsprüfung, Marktprüfung oder ausstehendem Probedruck.
- Neue Libraries auf Lizenz, Wartung und Lieferkette prüfen; möglichst wenige Abhängigkeiten.
