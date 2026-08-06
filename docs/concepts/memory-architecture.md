---
title: Kontext- und Gedächtnisarchitektur
doc_type: explanation
status: proposed
canonical: false
---

# Kontext- und Gedächtnisarchitektur

Das Ziel ist nützlicher Langzeitkontext ohne globale Chronik.

```mermaid
flowchart LR
  U[user-settings.yaml] --> R[Request-Helper]
  C[custom_user.md optional] --> R
  M[agent-semantic-memory.md optional] --> R
  R --> B[Request-Brief]
  B --> O[Orchestrator]
  O --> F[Fachrollen]
  P[Projekt-Source-of-Truth] --> F
```

## Ebenen

| Ebene | Zweck | Laden |
|---|---|---|
| User Settings | Sprache, Stil, erlaubte Kontextquellen | primärer Agent |
| Custom User | freiwilliger, userverwalteter Kontext | nur berechtigte Rollen |
| Semantic Memory | kurze bestätigte Fakten und Candidates | rollen- und budgetabhängig |
| Request-Brief | aufgabenrelevante Verdichtung | Orchestrator und Fachrollen |
| Projektwissen | Requirements, Code, Tests, Entscheidungen | zuständiges Fach-Repo |
| Archiv | Rohchats und Historie | niemals automatisch |

Aktuelle User-Aussage und Fach-Source-of-Truth haben Vorrang. Git bewahrt frühere Werte;
Memory wird aktualisiert und verdichtet statt chronologisch erweitert.

Das vollständige vorgeschlagene Format steht im
[portablen Workspace-Konzept](portable-engineering-workspace.md#semantisches-memory).
