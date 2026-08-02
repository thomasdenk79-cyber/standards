---
title: "{PROJECT-NAME} – Handover"
doc_type: template
status: draft
canonical: true
---

<!--
Agent: {AGENT}
Model: {PROVIDER/MODEL-ID}
Auftraggeber: {ROLE OR [private user]}
Datum + Uhrzeit: {ISO-8601}
Zweck / Warum: Knapper Wiederaufsetzpunkt für aktive, unvollständige Arbeit.
-->

# {PROJECT-NAME} – Handover

> Nur führen, solange Arbeit aktiv und nicht zuverlässig aus Git plus Taskquelle ableitbar ist.

| Feld | Stand |
|---|---|
| Task/Requirement | {ID oder Link} |
| Status | in_progress / blocked |
| Letztmals verifiziert | {Test/Befehl und Ergebnis, ISO-8601} |
| Betroffene Dateien | {nur relevante Pfade; vollständiger Diff bleibt in Git} |
| Blocker/Annahmen | {knapp und entscheidungsrelevant} |
| Nächste Aktion | `{genau ein ausführbarer Befehl oder Schritt}` |

## Crash-/Resume-Zustand

> Diesen Abschnitt nur für einen SQLite-gestützten langen Workflow führen.

| Feld | Stand |
|---|---|
| Workflow-ID | `{stabile ID}` |
| SQLite | `{repo-relativer Pfad}` |
| Schema-Version | `{Version}` |
| Letzter Checkpoint | `{Work Item, Status und ISO-8601}` |
| Resume-Befehl | `{exakter, idempotenter Befehl}` |

## Noch offen

- [ ] {kleinste verifizierbare Einheit}
