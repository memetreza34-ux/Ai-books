# Qualitätssystem und Freigabe-Gates

## Harte Blocker (nicht durch Punktzahl überstimmbar)
- Beschädigte PDF / fehlende Seiten / ungültige Spezifikation.
- Doppelte Aufgaben, falsche Lösungen, ungültige oder nicht eindeutige Rätsel.
- Ungeklärte Lizenz, Autorenschaft, irreführende Behauptung oder KI-Deklaration.
- Nicht geprüfte Fach-/Sicherheits-/Gesundheitsangaben.
- Nicht verifizierter Plattformstatus bei geplanter Veröffentlichung.
- Fehlende menschliche Freigabe.

## Individuelle Qualitätsskala
Für jedes Buch wird vor der Erstellung eine auf Genre und Leser abgestimmte Bewertungsmatrix definiert. Startvorschlag:
- Funktion/Nutzwert 30
- Fachliche Richtigkeit 25
- Layout/Lesbarkeit 20
- Originalität 15
- Marktpositionierung/Metadaten 10

Score >=90/100 ist Entwicklungsziel, **kein** Ersatz für harte Gates. KI-Selbsteinschätzung gilt nicht als unabhängiger Nachweis. Automatische Tests und menschliche visuelle Prüfung sind getrennt dokumentiert.

## Veröffentlichungszustände
IDEA → RESEARCHED → PLANNED → GENERATED → MACHINE_VALIDATED → REVIEW_REQUIRED → HUMAN_APPROVED → KDP_PREVIEWED → PROOF_REVIEWED → PUBLISHING_READY → PUBLISHED.

Die technische MVP-Ausgabe ist maximal MACHINE_VALIDATED; niemals automatisch PUBLISHING_READY.

## Nach jedem Buch
Fehlerursachen analysieren, Tests ergänzen, Vorlagen nur kontrolliert ändern, Regressionstest mit früheren Beispielen laufen lassen.
