# AGENTS.md — {REPO-NAME}

- **AI-ACCESS:** inherit
- **AI-EXECUTION:** inherit
- **AI-NETWORK:** inherit
- **AI-SECRET-ACCESS:** inherit
- **AI-DEPENDENCY-CHANGE:** inherit
- **AI-EXTERNAL-COST:** inherit
- **AI-GIT-COMMIT:** inherit
- **AI-GIT-PUSH:** inherit
- **AI-EXTERNAL-WRITE:** inherit
- **AI-DEPLOY:** inherit
- **AI-DESTRUCTIVE:** inherit
- **AI-CHAT-LOGGING:** inherit
- **AI-MEMORY-EXPORT:** inherit
- **DATA-CLASSIFICATION:** inherit
- **INHERITS:** `${ENGINEERING_GOVERNANCE_ROOT}/AGENTS.md`
- **OVERRIDES:** none
- **SCOPE:** this repository

> Erst den kanonischen Governance-Router, dann diese Datei und danach engere Modul-Router
> lesen. Agents verändern ihre eigenen Rechte nicht.

## Aktueller Stand

### Stand: YYYY-MM-DD HH:MM | agent: tool | model: provider/model | role: role

- Fertig: `{Commit oder Ergebnis mit Evidenz}`
- In Arbeit: `{klarer Zustand}`
- Blockiert: `{Grund oder none}`
- Nächster Schritt: `{genaue Aktion}`

## Repo-Kontext

| Was | Detail |
|---|---|
| Zweck | {Kurzbeschreibung} |
| Stack | {Technologien} |
| Remote | {Canonical Remote oder none} |
| Docs | {Befehl oder none} |
| Tests | {Befehl} |

Lokale absolute Pfade werden nicht dokumentiert. Der Repo-Pfad wird aus Git und
`ENGINEERING_REPOS_ROOT` ermittelt.

## Fachliche Anker

| Thema | Kanonische Quelle |
|---|---|
| Vision, Ziele und Nicht-Ziele | `{Project Brief oder gleichwertig}` |
| Fachanforderungen | `{Requirements oder Project Brief}` |
| Architektur und Grenzen | `{Architekturquelle}` |
| Entscheidungen | `{ADR/Decision Log/Git}` |
| Arbeitsstatus | `{Issue/TODO/Handover}` |
| Tests und Acceptance | `{Testplan/Runbook/Acceptance}` |

Keine zweite TODO-, Requirements- oder Entscheidungsquelle anlegen.

## Lokale Regeln

- {Nur echte Abweichungen oder Ergänzungen zur Governance}

## Wiederaufnahme

- **Workflow-ID:** `{none oder stabile ID}`
- **Checkpoint:** `{Zeit und verifizierter Zustand}`
- **Resume:** `{genauer Schritt oder none}`

Für komplexe oder unterbrechbare Arbeit Handover/TODO aktualisieren. SQLite nur für lange
transaktionale Workflows; Markdown und Git bleiben kanonisch.

## Abschluss

- Anforderungen, Acceptance, TODO und Handover konsistent halten.
- Relevante Tests und bekannte Lücken belegen.
- Fremde Änderungen erhalten und Git-Status verstehen.
- Commit/Push nur gemäß Policy und User-Auftrag.

## Commit-Format

```text
<type>(<scope>): <what> -- <why>

why-ref: <sanitized summary, ticket or ADR>
agent: <tool> | model: <provider/model> | role: <role>
```

Private Originale und Secrets nie referenzieren.
