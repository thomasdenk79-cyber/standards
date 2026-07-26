# 🔬 SOTA-REFERENZ: KI-Agenten-Gedächtnis & Team-Protokolle

> **Zielgruppe:** NUR für den wöchentlichen Review-LLM (Memory Curator).
> **Zweck:** Prüfen ob unser System noch Stand der Technik ist. Bei Verbesserungen → AGENTS.md aktualisieren.
> **Nicht lesen müssen:** Normale Coding-Agents (zu viel, zu lang → Context Bloat Anti-Pattern)

**Letzte Recherche:** 2026-07-26 | Agent: GitHub Copilot CLI | LLM: Claude Sonnet 4.6

---

## ✅ BESTÄTIGUNG: Unser Ansatz ist State of the Art (Juli 2026)

Unser selbst entwickeltes System stimmt mit dem überein, was Anthropic, OpenAI, Google
und akademische Forschung 2026 als Standard etablieren. Ohne alle Tools zu kennen.

| Unser Ansatz | Wissenschaftlicher Name | Etabliert durch |
|---|---|---|
| `AGENTS.md` Hierarchie (Global→Repo→Subdir) | Hierarchical Working Memory | Claude Code, Codex CLI, Cursor |
| `.memory/session-log.md` | Episodic Memory Store | CoALA Framework (Stanford 2023) |
| `.memory/decisions.md` | Procedural Memory / ADR | Software Engineering Best Practice |
| `.memory/user-profile.md` | Semantic User Memory | Mem0, Generative Agents |
| Agents lesen nur was sie brauchen | Selective Retrieval / Lazy Loading | Ensemble QSP, HOMER (2026) |
| Git als unveränderliches Gedächtnis | Immutable Episodic Store | PRO-LONG (2026) |
| Wöchentlicher Review-Agent | Reflection Mechanism | Generative Agents (Park et al. 2023) |
| `agent: X | llm: Y | role: Z` in Commits | Agent Provenance Tracking | Neu/eigene Entwicklung |

---

## 📚 KERN-PAPERS (nach Wichtigkeit)

### 1. CoALA — Die kanonische Gedächtnis-Taxonomie
**Paper:** "Cognitive Architectures for Language Agents"
**Autoren:** Sumers, Yao, Narasimhan, Griffiths (Princeton/Google, Sep 2023)
**URL:** https://arxiv.org/abs/2309.02427
**Warum wichtig:** Meistzitierteste Taxonomie für Agent-Memory. Direkt aus Kognitionspsychologie.

| Memory Type | In unserem System |
|---|---|
| Working Memory (aktiver Kontext) | AGENTS.md Hierarchie (Ebene 0-2) |
| Episodic Memory (vergangene Events) | Git History + .memory/session-log.md |
| Semantic Memory (Faktenwissen) | .memory/user-profile.md + decisions.md |
| Procedural Memory (Wie-Wissen) | Code + Kommentare + AGENTS.md Regeln |

---

### 2. Generative Agents — Reflection Mechanism
**Paper:** "Generative Agents: Interactive Simulacra of Human Behavior"
**Autoren:** Park et al. (Stanford, Apr 2023)
**URL:** https://arxiv.org/abs/2304.03442
**Warum wichtig:** Erfand Memory Stream + Reflection. Unser Review-Agent = Reflection.

Drei Operationen (wir implementieren alle):
1. **Retrieval:** `recency × importance × relevance` → wir: Git-Log + AGENTS.md lesen
2. **Reflection:** Rohe Beobachtungen → höhere Muster → wir: Review-Agent synthetisiert Woche
3. **Planning:** Reflections → Zukunftsverhalten → wir: `.memory/decisions.md` + Empfehlungen

---

### 3. MemGPT/Letta — Virtuelles Memory-OS
**Paper:** "MemGPT: Towards LLMs as Operating Systems"
**URL:** https://arxiv.org/abs/2310.08560 | https://github.com/letta-ai/letta
**Was sie machen:** LLM verwaltet Kontext wie OS-Prozesse RAM verwalten.
**Unterschied zu uns:** Sie brauchen laufenden Server + DB. Wir: reines Git + Markdown.
**Unser Vorteil:** Kein extra Tool, keine Abhängigkeit, jeder Agent kann es nutzen.

---

### 4. Mem0 — Multi-Level Memory API
**URL:** https://github.com/mem0ai/mem0 | https://mem0.ai
**Benchmark (April 2026):** LoCoMo 92.5, LongMemEval 94.4
**Was sie besser machen:** Semantische Suche über Memories, Temporal Reasoning, Entity-Linking.
**Was wir stattdessen nutzen:** Git-Log (grep-bar), strukturiertes Markdown (human-readable).
**Bewertung:** Für größere Teams + viele Repos könnte Mem0 sinnvoll sein. Für uns: Overkill.

---

### 5. Zep/Graphiti — Temporale Knowledge Graphs
**Paper:** "Zep: A Temporal Knowledge Graph Architecture for Agent Memory"
**URL:** https://arxiv.org/abs/2501.13956 | https://github.com/getzep/graphiti
**Innovation:** Jede Entscheidung hat Gültigkeitsfenster ("galt bis YYYY-MM-DD").
**MCP-Server:** Funktioniert direkt mit Claude, Cursor.
**Bewertung:** Interessant für unsere decisions.md — könnten Validity-Windows ergänzen.
**TODO für Review:** decisions.md-Einträge mit `valid_until:` erweitern?

---

### 6. PRO-LONG — Programmatisches Gedächtnis
**Paper:** arxiv.org/abs/2607.20064
**Repo:** https://github.com/alexisfox7/PRO-LONG
**Kernaussage:** `log.txt` + `grep` schlägt komplexe Vector-DBs bei 5x weniger Token-Kosten.
**ARC-AGI-3:** +18pp über Baseline.
**Bestätigt unseren Ansatz:** Git-Log + Markdown = grep-bares, strukturiertes Log. Richtig.

---

### 7. MOSAIC — Entity-Graph + Conflict Detection (Juli 2026, neu)
**URL:** arxiv Suche bestätigt, Juli 2026
**Innovation:** Erkennt Widersprüche in neuen Infos gegen bestehenden Graphen (66% vs. 14% Baseline).
**Für uns relevant:** Review-Agent könnte Widersprüche in decisions.md automatisch flaggen.
**Score:** 89.35% LoCoMo (SOTA Juli 2026).

---

### 8. Configuration Smells in AGENTS.md Files (Juni 2026)
**Paper:** Santos et al., arxiv bestätigt Juni 2026
**Analysiert:** 100 populäre Open-Source-Repos mit AGENTS.md / CLAUDE.md

**6 Anti-Pattern — wir prüfen uns dagegen:**

| Anti-Pattern | Häufigkeit | Unser Status |
|---|---|---|
| Context Bloat (zu lang) | 42% | ⚠️ Risiko — global AGENTS.md komprimiert halten |
| Lint Leakage (Linter-Regeln drin) | 62% | ✅ Linter-Regeln in pyproject.toml etc. |
| Skill Leakage (unmögliche Fähigkeiten) | 35% | ✅ Nur reale Fähigkeiten |
| Conflicting Instructions | häufig | ✅ Review-Agent bereinigt wöchentlich |
| Stale Instructions | häufig | ✅ Review-Agent markiert veraltetes |

---

### 9. Claude Code Memory Hierarchy (Produktions-Standard)
**Docs:** https://code.claude.com/docs/en/memory
**Loading Order:**
```
Managed policy:  C:\Program Files\ClaudeCode\CLAUDE.md  (IT-Policy)
User:            ~/.claude/CLAUDE.md                    (persönlich)
Project:         ./CLAUDE.md oder ./.claude/CLAUDE.md   (Team, im VCS)
Local:           ./CLAUDE.local.md                      (persönlich, gitignored)
Subdir:          {subdir}/CLAUDE.md                     (lazy, nur bei Bedarf)
```
**Import-Syntax:** `@AGENTS.md` in CLAUDE.md → beide Tools teilen eine Datei.
**Auto-Memory:** Claude Code schreibt eigene Learnings (erste 200 Zeilen / 25KB).
**Bestätigt:** Unsere Hierarchie = exakt dieses Muster.

---

## 🔄 REVIEW-CHECKLISTE (wöchentlich)

```
□ Gibt es neue SOTA-Papers die unser System verbessern würden?
□ Sind alle AGENTS.md-Dateien < 300 Zeilen? (Context Bloat)
□ Gibt es widersprüchliche Regeln in verschiedenen AGENTS.md? (Conflicting)
□ Sind decisions.md-Einträge noch gültig? (Stale)
□ Hat Thomas neue Präferenzen gezeigt → user-profile.md?
□ Gibt es neue Siemens-Modelle die im Benchmark fehlen?
□ Ist Trunk-Based Development noch sinnvoll für die Teamgröße?
□ Sollte Mem0/Graphiti/Letta eingeführt werden? (derzeit: Nein — Overkill)
```

---

## 📊 BENCHMARKS & VERGLEICH (Stand Juli 2026)

| System | LoCoMo | Ansatz | Für uns? |
|---|---|---|---|
| MOSAIC | 89.35% | Entity-Graph + Hash-Retrieval | Zu komplex |
| Mem0 (April 2026) | 92.5% | Multi-signal RAG + Temporal | Overkill |
| MIRIX | 85.4% | 6-Typ Taxonomie, Multi-Agent | Overkill |
| **Unser Ansatz** | **n/a** | **Git + Markdown + Grep** | **✅ Richtig** |
| PRO-LONG | +18pp | Log.txt + grep | Bestätigt uns |

**Fazit:** Für Einzelentwickler + kleines Team mit bis zu ~5 Repos:
Git + Markdown > komplexe Memory-Systeme (weniger Overhead, mehr Transparenz, grep-bar).
Ab ~20 Repos oder >5 parallelen Agents: Mem0 oder Graphiti evaluieren.
