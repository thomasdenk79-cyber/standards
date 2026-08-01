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
- **INHERITS:** `C:\GIT\AGENTS.md`
- **OVERRIDES:** none
- **SCOPE:** this repository

> Der Startsequenz in `C:\GIT\AGENTS.md` folgen und danach diesen Router vollständig lesen,
> bevor substanzielle Arbeit in seinem Geltungsbereich beginnt.

Die Policy-Semantik steht ausschließlich in `C:\GIT\AGENTS.md`. `inherit` übernimmt den
Workspace- oder Parent-Wert. Der autorisierte Repository-Owner kann Defaults übernehmen,
konkretisieren, ersetzen oder deaktivieren und Agentenzugriff bis `AI-ACCESS: denied`
ausschließen; lokale Overrides werden oben sichtbar benannt. Agents dürfen diese Rechte nicht
selbst verändern.

---

## 🔴 AKTUELLER STAND

### Stand: YYYY-MM-DD HH:MM | Agent: X | model: provider/model-id | role: Z

- ✅ Fertig: `{commit-hash}` — {1 Satz was und warum}
- 🔄 In Arbeit: `{copy-paste Befehl für nächsten Agent}`
- ❌ Blockiert: {was + warum}
- 👉 Nächster Schritt: `{exakter Befehl}`

---

## Repo-Kontext

| Was | Detail |
|---|---|
| **Zweck** | {Kurzbeschreibung} |
| **Stack** | {Technologien} |
| **Pfad lokal** | `C:\GIT\{repo-name}` |
| **Remote** | `https://github.com/thomasdenk79-cyber/{repo-name}` |
| **Docs** | `python -m mkdocs gh-deploy` |
| **Tests** | `python standards\scripts\test_docs.py` |

## Fachliche Anker

> Vor fachlicher Umsetzung die passenden Quellen lesen. Pro Thema genau eine kanonische Quelle
> nennen; kleine Repos dürfen mehrere Themen in einem Project Brief bündeln. Keine Platzhalter
> in einem aktiven Router stehen lassen.

| Thema | Kanonische Quelle |
|---|---|
| Vision, Zweck, Ziele und Nicht-Ziele | `{docs/project/project-brief.md oder gleichwertig}` |
| Fachanforderungen und akzeptierte Changes | `{Project Brief oder docs/project/requirements.md}` |
| Architektur und technische Grenzen | `{docs/project/architecture.md oder gleichwertig}` |
| Entscheidungen und verworfene Alternativen | `{Decision Log, ADR-Verzeichnis oder Git-Historie}` |
| Aktueller Arbeitsstatus | `{Taskboard, Issue-Tracker oder Handover}` |
| Tests und Abnahmesignale | `{Testpfad, Runbook oder Abnahmeplan}` |

Die gemeinsame Trennung und das skalierbare Anforderungsmodell stehen in
`C:\GIT\standards\docs\shared\repository-knowledge.md`.

## Cross-Referenzen

> Nur Repositories verlinken, die für dieses Projekt tatsächlich relevant sind.

| Repo | Warum relevant | Was dort lesen |
|---|---|---|
| *(leer wenn keine Cross-Refs)* | | |

## Gedächtnis-Routing

Nach jedem bedeutenden Befund, Meilenstein, Themenwechsel und vor Abschluss/Kompaktierung:

| Information | Ziel |
|---|---|
| Technischer Stand, Befehle, TODOs, Fallstricke | Diese `AGENTS.md` oder verlinktes Handover |
| Fachlich neutrales WHY für materielle Änderungen | Zentral `C:\GIT\standards\why\conversations\`; Commit nennt den exakten `why-ref` |
| Persönlicher User-Kontext | `C:\GIT\user-memory\profile.md` |
| Cross-Repo-Session-Handoff | `C:\GIT\user-memory\session-log.md` |
| Wiederverwendbare Agent-Erkenntnis | Über `C:\GIT\agent-memory\INDEX.md` routen |

Nicht auf die Aufforderung "merk dir das" oder ein erkennbares Session-Ende warten.

## Offene Arbeit (optional)

> Nur verwenden, wenn kein verlinkter Issue-Tracker oder Taskboard die kanonische Quelle ist.
> Keine zweite TODO-Liste führen.

| Prio | Aufgabe | Kontext |
|---|---|---|
| 🔴 | {erste Aufgabe} | {Details} |

## Quickstart

```powershell
Set-Location -LiteralPath C:\GIT\{repo-name}
{start-befehl}
```

## Bekannte Fallstricke

- {Fallstrick 1 — warum und wie vermeiden}

## Commit-Format

```text
<type>(<scope>): <what> -- <why>

why-ref: <sanitized conversation summary, ticket or ADR>
agent: <tool-name> | model: <provider/model-id> | role: <role>
```

Mehrere Belege mit ` · ` trennen. Bei materieller Agent-Arbeit die zentrale bereinigte
Zusammenfassung als exakten Workspace-relativen Pfad unter `standards/why/conversations`
angeben. Private Originale aus `user-memory` niemals in Git referenzieren.
