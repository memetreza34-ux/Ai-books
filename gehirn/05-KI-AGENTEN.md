# Agenten, Rollen und Token-Kosten

## Grundsystem
Antigravity ist primärer Orchestrator. Claude Code und Codex dürfen im selben Repository ergänzen und prüfen. Genau ein zuständiger Schreib-Agent pro Arbeitsstrang; andere können reviewen. Kein Agent darf fehlende Live-Daten erfinden oder ungefragt API-Keys einsetzen.

## Effizienter Kontext
1. Immer AGENTS.md, gehirn/00, gehirn/09.
2. Für die konkrete Aufgabe nur relevante Gehirn-Dateien, Code und Tests.
3. Für Änderungen: Diff, Tests und kurze Statusübergabe.
4. Nach jeder substanziellen Änderung Status + Fehlerlog + ADR aktualisieren.
5. Niemals gesamtes Repository ohne Bedarf in einen Prompt kopieren.

## Rollen
- Research: Quellen, Nachfragehypothesen, Konkurrenzvergleich; Beleg versus Annahme.
- Producer: Inhalte, Aufgaben, Layout und Varianten.
- Critic: Lesbarkeit, Originalität, Schwächen; keine Scheinvalidierung.
- Deterministic QA: mathematische Korrektheit, Lösungen, Dateien, Seiten.
- Compliance reviewer: Checkliste für Lizenz, KDP, EU, Minderjährige.
- Human owner: finale Freigabe, Ausgaben, Plattformzugang, Upload.

## Kosten und Wiederaufnahme
- Lokale Generatoren vor bezahlten KI-Aufrufen.
- Kostenkalkulation vor API-Einsatz; falls nicht bewilligt, nicht ausführen.
- Persistente Seeds/Manifeste, Schritte idempotent, Fehler klar kennzeichnen.
- Erst nach geprüftem Buch nächste Produktion.
