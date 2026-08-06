---
title: Agenten-Team
doc_type: explanation
status: active
canonical: false
---

# Das Agenten-Team

Ein Team entsteht durch getrennte Verantwortungen, minimale Kontextpakete und unabhängige
Evidenz – nicht durch viele gleichzeitig gestartete Modelle.

- Der Request-Helper darf relevanten User-Kontext abrufen und erzeugt einen Request-Brief.
- Der Orchestrator erhält den Brief, nicht das vollständige User-Memory.
- Implementierer, Tester und Reviewer erhalten nur ihren Arbeitsvertrag.
- Acceptance bleibt unabhängig.
- Ein optionaler Memory-Curator darf nur den begrenzten Memory-Bereich verändern.

Konflikte werden anhand Requirements, Tests, Architektur und reproduzierbarer Evidenz
entschieden. Details: [Multi-Agent-Koordination](../shared/multi-agent-coordination.md) und
[Portabler Engineering-Workspace](portable-engineering-workspace.md).
