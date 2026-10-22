# Entscheidungen (ADR light)

Jede neue Entscheidung erhält Datum, Kontext, Entscheidung, Grund, Alternativen, Folgen.

| ID | Datum | Entscheidung | Grund |
| --- | --- | --- | --- |
| D001 | 2026-10-22 | Ein Repository: Ai-books | Doppelarbeit vermeiden |
| D002 | 2026-10-22 | Zentrale Gehirn-Dateien + AGENTS.md | Wiederanlauf mit Kontext |
| D003 | 2026-10-22 | Modularer Python-Kern und deterministische Generatoren | Niedrige Kosten, prüfbare Ergebnisse |
| D004 | 2026-10-22 | Als Erstes ein funktionierender Sudoku-Referenzgenerator | Geringer fachlicher Risiko-/Prüfaufwand, klare Tests |
| D005 | 2026-10-22 | Erst Deutsch und ein Paperback-Profil als MVP; andere Sprachen/Plattformen offen | Qualität vor zu frühem Ausbau |
| D006 | 2026-10-22 | Antigravity zuerst, Claude Code/Codex optional | vorhandene Werkzeuge verwenden |
| D007 | 2026-10-22 | Keine autonomen Verkäufe, Publikationen oder Ausgaben | menschliche Kontrolle |
| D008 | 2026-10-22 | Eine Buchproduktion nach der anderen | Qualitätskontrolle und Debugging |
| D009 | 2026-10-22 | Versionskontrollierte Quellen, generierte Artefakte ignorieren | Datenschutz und saubere Historie |
| D010 | 2026-10-22 | Statische KDP-Regeln nur als Momentaufnahme, vor Veröffentlichung live prüfen | Regeln können sich ändern |

### Delegierte Entscheidungen
Die KI darf Vorschläge für Genres, Märkte, Sprachen, Altersgruppen, Formate, Cover, Varianten und die Reihenfolge der Buchtypen anhand einer dokumentierten Bewertung treffen. Die Bewertung ist eine **Hypothese**, falls kein verifizierter Live-Marktnachweis vorliegt. Menschliche Zustimmung ist für Freigaben nötig.

### Offene Entscheidungen
- Produktionsbudget über kostenlose lokale Werkzeuge hinaus (Freigabe pro Ausnahme)
- Öffentlicher Verlagsname und Pseudonyme (später)
- Zusätzliche Plattformen und Schnittstellen (später)
- Werbung und Marketingbudget (später)
- Verfügbarkeit verifizierbarer Verkaufs-/Keyword-Daten
