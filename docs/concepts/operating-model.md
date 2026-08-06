---
title: Betriebsmodell
doc_type: explanation
status: active
canonical: false
---

# Betriebsmodell

Diese Seite erklärt das System. Operative Regeln stehen ausschließlich in den verlinkten
kanonischen Quellen.

## Source of Truth

| Thema | Kanonische Quelle |
|---|---|
| Gemeinsame Policies | `${ENGINEERING_GOVERNANCE_ROOT}/AGENTS.md` |
| Workspace-Einstieg | `${ENGINEERING_REPOS_ROOT}/AGENTS.md` |
| Vererbung | `docs/shared/inheritance.md` |
| Projektregeln und Zustand | nächste anwendbare Repo-`AGENTS.md` plus verlinkte Fachdoku |
| Usergeschriebener Kontext | optionale, in `user-settings.yaml` benannte Datei |
| Agentengepflegte Fakten | optionales, begrenztes `agent-semantic-memory.md` |
| Historie | Git und geschützte Archive; nie globaler Startup-Kontext |

## Ablauf

1. Bootstrap validiert Workspace, Variablen, Settings und Provider-Adapter.
2. Request-Helper lädt nur erlaubten User-Kontext.
3. User bestätigt offene Entscheidungen bei Bedarf.
4. Request-Brief wird zur einzigen Übergabe an den Orchestrator.
5. Rollen erhalten minimale Arbeitsverträge.
6. Tests und unabhängige Acceptance liefern Evidenz.
7. Projektstatus bleibt im Fach-Repo; semantisches Memory enthält nur repoübergreifende
   Benutzerfakten.

## Prinzipien

- kleinster ausreichender Kontext;
- Rollen- und Dateiscope technisch erzwingen;
- keine Erfolgsmeldung nur aufgrund eines Exit-Codes;
- eine Detailquelle pro Information;
- aktuelle Fakten statt Session-Chronik;
- sichere Defaults und sichtbare Owner-Gates.

Der noch zu prüfende Zielentwurf steht im
[portablen Engineering-Workspace](portable-engineering-workspace.md).
