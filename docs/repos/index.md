---
title: Repository-Modell
doc_type: explanation
status: active
canonical: false
---

<!-- Agent: OpenCode | Model: github-copilot/gpt-5.6-sol | Auftraggeber: [private user] | Datum + Uhrzeit: 2026-07-30T00:14:16+02:00 | Zweck / Warum: Öffentliche Übersicht ohne private oder interne Repository-Details. -->

# Repository-Modell

Jedes Repository besitzt seinen technischen Zustand und seine Owner-Policies. Gemeinsame
Regeln werden nicht kopiert, sondern über Router und Links eingebunden.

| Bereich | Verantwortung |
|---|---|
| Projekt-Repository | Code, aktueller Zustand, lokale Regeln, Tests und Entscheidungen |
| `standards` | gemeinsame Vorlagen, Engineering-Konzepte und Doku-Prüfungen |
| `user-memory` | privater User-Kontext; nicht Teil öffentlicher Dokumentation |
| `agent-memory` | Agenten-Erkenntnisse und Selbstkorrektur; selektiv über `READ-WHEN` |

Konkrete interne oder private Repositories werden hier bewusst nicht inventarisiert. Der
aktuelle Workspace-Router ist die kanonische lokale Projektkarte.
