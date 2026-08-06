---
title: Repository-Modell
doc_type: explanation
status: active
canonical: false
---

<!-- Agent: OpenCode | Model: github-copilot/gpt-5.6-sol | Auftraggeber: [private user] | Datum + Uhrzeit: 2026-07-30T00:14:16+02:00 | Zweck / Warum: Öffentliche Übersicht ohne private oder interne Repository-Details. -->

# Repository-Modell

Jedes Repository besitzt seinen technischen Zustand und seine Owner-Policies. Gemeinsame
Best-Practice-Defaults werden nicht kopiert, sondern über Router und Links eingebunden. Der
autorisierte Repository-Owner entscheidet, welche Defaults gelten: Er darf sie übernehmen,
konkretisieren, ersetzen, deaktivieren oder AI-Agenten vollständig ausschließen. Repo-Archetypen
helfen nur bei Empfehlungen; sie erzeugen keine Pflichtprofile.

| Bereich | Verantwortung |
|---|---|
| Projekt-Repository | Code, aktueller Zustand, lokale Regeln, Tests und Entscheidungen |
| `engineering-governance` | gemeinsame Policies, Vorlagen, Konzepte und Validatoren |
| `.workspace` | optionale lokale User Settings und begrenzter Kontext; nicht Teil öffentlicher Dokumentation |

Konkrete interne oder private Repositories werden hier bewusst nicht inventarisiert. Der
aktuelle Workspace-Router ist die kanonische lokale Projektkarte.
