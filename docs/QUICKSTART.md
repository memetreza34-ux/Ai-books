# Schnellstart für MacBook und KI-Agenten

1. Repo klonen: `git clone https://github.com/memetreza34-ux/Ai-books.git`
2. `cd Ai-books` und `python3 -m venv .venv`
3. `source .venv/bin/activate`
4. `python -m pip install -e '.[dev]'`
5. `pytest`
6. `aibooks sudoku --title "Sudoku Testband" --count 28 --seed 20261022 --out output/sudoku-test`
7. Ergebnis manuell öffnen, alle QA-Berichte prüfen. Technisch erzeugte PDF ist DRAFT, nicht automatisch veröffentlichungsreif.

Agenteneinstieg: AGENTS.md und gehirn/00-START-HIER.md.

**Stand abhängig von Implementierung:** Fehlende Befehle in ROADMAP und STATUS als noch offen behandeln; niemals aus dieser Anleitung allein Funktionsfähigkeit ableiten.
