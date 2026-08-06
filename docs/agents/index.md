---
title: Agenten
doc_type: explanation
status: active
canonical: false
---

# Agenten

Agenten arbeiten in explizit zugewiesenen Rollen. Rolle, Evidenz und erlaubter Scope sind
wichtiger als Modellname oder Selbsteinschätzung.

| Rolle | Hauptauftrag |
|---|---|
| Request-Helper | unscharfen Auftrag mit relevantem User-Kontext klären |
| Orchestrator | freigegebenen Request zerlegen, routen und überwachen |
| Architekt | Anforderungen, Verträge und Risiken prüfen |
| Implementierer | begrenzten Arbeitsblock umsetzen |
| Tester | Verhalten unabhängig prüfen und Evidenz erzeugen |
| Reviewer | Diff gegen Requirements und Architektur bewerten |
| Acceptance-Reviewer | Endabnahme ohne Implementierungskontext |
| Memory-Curator | bestätigtes semantisches Memory begrenzt verdichten |

Rollenregeln liegen in `AGENTS.md` und
[Multi-Agent-Koordination](../shared/multi-agent-coordination.md). Dauerhafte
modellbezogene Identitäten sind keine Governance-Quelle.
