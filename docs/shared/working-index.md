---
title: Optionaler Arbeitsindex
doc_type: reference
status: active
canonical: true
---

<!--
Agent: GitHub Copilot CLI 1.0.77
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-08-01T13:51:47+02:00
Zweck / Warum: Große operative Detailmengen tokenarm und crashfest verwalten.
-->

# Optionaler Arbeitsindex

Markdown und Git bleiben die **Single Source of Truth**. User- und Agent-Memory erweitern sie
für personen- beziehungsweise agentenbezogenes Wissen.

Ein Repository darf zusätzlich SQLite verwenden, wenn strukturierte Detailarbeit davon
profitiert, zum Beispiel für hunderte Schritte, Abhängigkeiten, Testfälle, Hypothesen,
Batchzustände oder temporäre Befunde.

## Regeln

- SQLite ist optional: Für kleine Aufgaben entsteht keine Datenbank.
- Der Index ist Arbeitsgedächtnis, keine zweite fachliche Wahrheit.
- Crash-/Resume-relevante Ergebnisse werden zeitnah in `AGENTS.md`, Handover, TODO,
  Requirements, Decision Log oder das passende User-/Agent-Memory verdichtet.
- Bei Widerspruch gewinnt die kanonische Markdown-Quelle.
- Startup-Agenten laden nur die verdichteten Markdown-Einstiege; SQLite wird erst bei
  passender Detailarbeit abgefragt.
- Datenbankdateien werden standardmäßig nicht committed. Ein Repo dokumentiert Pfad, Schema
  und Nutzung in seiner `AGENTS.md` nur dann, wenn es den Index tatsächlich verwendet.
- Secrets und unnötige Rohchats gehören nicht in den Index.

Der Index darf jederzeit neu aufgebaut, bereinigt oder ersetzt werden. Sein Nutzen ist weniger
Kontextverbrauch bei komplexer Arbeit, nicht zusätzliche Dokumentationspflicht.

## Abgrenzung zur Teamkoordination

| Ebene | Zweck | Typische Technik |
|---|---|---|
| kanonisches Wissen | Code, Verträge, Anforderungen, Entscheidungen | Markdown und Git |
| lokales Arbeitsgedächtnis | viele Schritte eines einzelnen Agenten | optional SQLite |
| gemeinsamer Live-Zustand | Claims, Abhängigkeiten, Blocker und Freigaben vieler Agenten | Control-Plane-API mit zentralem Store |

Die dritte Ebene ist kein größerer SQLite-Index. Sie benötigt Identität, Rechte, Transaktionen,
Leases, Audit und eine definierte API. Das vorgeschlagene Modell steht unter
[Multi-Agent-Koordination](multi-agent-coordination.md).
