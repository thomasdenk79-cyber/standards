# AGENTS.md — {REPO-NAME}

- **AI-ACCESS:** allowed
- **INHERITS:** `C:\GIT\AGENTS.md`
- **OVERRIDES:** none
- **SCOPE:** this repository

> **Für jeden Agent der hier arbeitet — PFLICHTLEKTÜRE vor jeder Aktion:**
> Lies diese Datei vollständig → verstehe den Aktuellen Stand → handle. Keine Rückfragen vorher.
> Vorher verpflichtend: `C:\GIT\AGENTS.md`, `C:\GIT\user-memory\profile.md`,
> `C:\GIT\agent-memory\INDEX.md` und `C:\GIT\standards\AGENTS.md`.
> Bei Projekt-/Themenwechsel diese Hierarchie für das neue Projekt erneut laden.

Die tiefste passende `AGENTS.md` gilt für ihren Unterbaum. Benenne lokale Overrides
oben explizit; nicht erwähnte Parent-Regeln werden geerbt. Repository-Owner können
mit `AI-ACCESS: read-only` Änderungen verbieten oder mit `AI-ACCESS: denied`
Agent-Arbeit vollständig untersagen.

---

## 🔴 AKTUELLER STAND

### Stand: YYYY-MM-DD HH:MM | Agent: X | llm: Y | role: Z

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

## Cross-Referenzen (andere Repos die relevant sind)

> Wenn dieses Repo Code, Konzepte oder Daten aus anderen Repos braucht — hier verlinken.
> Agent lädt nur was für die aktuelle Aufgabe relevant ist.

| Repo | Warum relevant | Was dort lesen |
|---|---|---|
| *(leer wenn keine Cross-Refs)* | | |

Beispiele:
- `C:\GIT\postgre` → DB-Schema das dieses Repo nutzt → dort AGENTS.md Abschnitt "Schema"
- `D:\git\llm-evaluation-workbench` → Benchmark-Ergebnisse die diese Entscheidung begründen

## Gedächtnis-Routing

Nach jedem bedeutenden Befund, Meilenstein, Themenwechsel und vor Abschluss/Kompaktierung:

| Information | Ziel |
|---|---|
| Technischer Stand, Befehle, TODOs, Fallstricke | Diese `AGENTS.md` oder verlinktes Handover |
| Persönlicher Kontext über Thomas | `C:\GIT\user-memory\profile.md` |
| Cross-Repo-Session-Handoff | `C:\GIT\user-memory\session-log.md` |
| Wiederverwendbare Agent-Erkenntnis | Über `C:\GIT\agent-memory\INDEX.md` routen |

Nicht auf die Aufforderung "merk dir das" oder ein erkennbares Session-Ende warten.

## Offene TODOs

| Prio | Aufgabe | Kontext |
|---|---|---|
| 🔴 | {erste Aufgabe} | {Details} |

## Quickstart

```bash
cd C:\GIT\{repo-name}
{start-befehl}
```

## Bekannte Fallstricke

- {Fallstrick 1 — warum und wie vermeiden}
