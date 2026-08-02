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

Ein Workflow darf zusätzlich SQLite verwenden, wenn strukturierte Detailarbeit davon
profitiert, zum Beispiel für viele Schritte, Abhängigkeiten, Testfälle, Hypothesen,
Batchzustände, lange Modellkampagnen, Migrationen oder temporäre Befunde. Der Index gehört zum
Workflow beziehungsweise zur Kampagne, nicht zur Identität eines Agents. Dadurch kann ein
Nachfolge-Agent denselben Zustand fortsetzen, ohne agentenspezifische Datenbanken
zusammenzuführen.

## Wann SQLite sinnvoll ist

SQLite verwenden, wenn mindestens eines zutrifft:

- ein Lauf dauert so lange, dass Prozess-, Rechner- oder Sessionabbruch realistisch ist;
- Arbeit umfasst viele unabhängige oder abhängige Einheiten;
- einzelne Einheiten müssen idempotent übersprungen oder wiederholt werden;
- strukturierte Test-, Mess-, Artefakt- oder Fehlerdaten würden Markdown aufblähen;
- ein genauer atomarer Checkpoint ist für Resume nötig.

Keine Datenbank anlegen für kurze, zusammenhängende Aufgaben, die aus Git-Diff, Taskquelle und
einem knappen Handover eindeutig rekonstruierbar sind.

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
- Genau ein Prozess besitzt einen Schreibjob beziehungsweise eine klar abgegrenzte
  Transaktion. Für lokale nebenläufige Leser `WAL` und `busy_timeout` verwenden.
- Checkpoints atomar in derselben Transaktion wie der zugehörige Zustandswechsel schreiben.
- Lange Schritte vor Beginn als `in_progress` und nach verifizierter Wirkung als `done`,
  `failed`, `blocked` oder `interrupted` persistieren.
- Nach einem Crash niemals blind einem alten `in_progress` vertrauen: Prozess, Artefakte,
  Git-Zustand und letzten Validierungsbefehl zuerst prüfen.

Der Index darf jederzeit neu aufgebaut, bereinigt oder ersetzt werden. Sein Nutzen ist weniger
Kontextverbrauch bei komplexer Arbeit, nicht zusätzliche Dokumentationspflicht.

## Empfohlenes Referenzmodell

Ein projektspezifisches Schema darf abweichen, sollte aber diese Konzepte abbilden:

| Tabelle/Konzept | Mindestinhalt |
|---|---|
| `schema_meta` | Schema-ID und Version |
| `workflows` | Workflow-/Kampagnen-ID, Status, Scope, Start/Update |
| `work_items` | stabile ID, Requirement, Status, Priorität, Owner-Rolle |
| `dependencies` | Work Item und blockierende Vorgänger-ID |
| `checkpoints` | letzter verifizierter Zustand, nächste Aktion, Validierungsbefehl/-resultat |
| `artifacts` | Pfad, Typ, optional Hash und erzeugender Work Item |
| `events` | knapper append-only Zustandsübergang mit Zeit, Agent und Modell |

Nicht jede Gedanken- oder Toolaktion protokollieren. Native Sessionlogs liefern die
Detailchronik; der Index speichert nur das, was zur deterministischen Fortsetzung oder
Auswertung benötigt wird.

Empfohlener lokaler Pfad:

```text
<repo>\.agent-state\<workflow-id>.sqlite3
```

Das Repository muss `.agent-state\` ignorieren. Kampagnenspezifische Systeme dürfen einen
bereits etablierten Pfad verwenden, etwa
`benchmark_results\agent-helper\<campaign-id>\agent_helper.sqlite3`.

## Checkpoint- und Resume-Vertrag

Vor einem langen oder riskanten Schritt:

1. Work Item, erwartete Eingaben und genaue nächste Aktion persistieren.
2. Handover auf Workflow-ID, DB-Pfad und Resume-Befehl verweisen lassen.
3. Erst danach den externen Prozess starten.

Nach einem verifizierten Meilenstein:

1. Ergebnis und Artefaktpfade atomar persistieren.
2. Validierungsbefehl und knappes Ergebnis speichern.
3. Nächsten ausführbaren Schritt setzen.
4. Dauerhafte Erkenntnisse in Requirements, Decision, Taskquelle oder Handover verdichten.

Nach Crash oder Agentenwechsel:

1. Repo-Router, kanonische Taskquelle und Handover lesen.
2. Git-Status und tatsächlich laufende Prozesse prüfen.
3. Den im Handover genannten SQLite-Workflow abfragen.
4. Alte `in_progress`-Einträge gegen Artefakte und Validierung abgleichen.
5. Nur unvollständige oder explizit wiederholbare Schritte resumieren.
6. Nach erfolgreichem Resume Markdown-Zustand und SQLite wieder synchronisieren.

## Abgrenzung zur Teamkoordination

| Ebene | Zweck | Typische Technik |
|---|---|---|
| kanonisches Wissen | Code, Verträge, Anforderungen, Entscheidungen | Markdown und Git |
| lokales Arbeitsgedächtnis | viele Schritte eines einzelnen Agenten | optional SQLite |
| gemeinsamer Live-Zustand | Claims, Abhängigkeiten, Blocker und Freigaben vieler Agenten | Control-Plane-API mit zentralem Store |

Die dritte Ebene ist kein größerer SQLite-Index. Sie benötigt Identität, Rechte, Transaktionen,
Leases, Audit und eine definierte API. Das vorgeschlagene Modell steht unter
[Multi-Agent-Koordination](multi-agent-coordination.md).
