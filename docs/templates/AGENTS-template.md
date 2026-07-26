# AGENTS.md — {REPO-NAME}

> **Für jeden Agent der hier arbeitet — PFLICHTLEKTÜRE vor jeder Aktion:**
> Lies diese Datei vollständig → verstehe den Aktuellen Stand → handle. Keine Rückfragen vorher.
> Globale Regeln + Infrastruktur: `C:\GIT\AGENTS.md` | Thomas als Mensch: `C:\GIT\user-memory\profile.md`

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
