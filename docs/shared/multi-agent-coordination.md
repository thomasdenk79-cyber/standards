---
title: Multi-Agent-Koordination
doc_type: reference
status: proposed
canonical: true
---

<!--
Agent: GitHub Copilot CLI 1.0.77
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-08-01T14:11:00+02:00
Zweck / Warum: Ein offenes, modulares Zielbild für teamübergreifende Agentenarbeit definieren.
-->

# Multi-Agent-Koordination

## Status und Entscheidung

Dieses Dokument ist ein **Zielbild zur Evaluation**, kein Auftrag zum Eigenbau. Zuerst werden
offene Standards und bestehende Open-Source-/Enterprise-Plattformen praktisch verglichen.
Erst ein Proof of Concept entscheidet über Konfiguration, Integration, Erweiterung oder
gezielten Eigenbau.

Zielszenario sind etwa 150 Entwickler mit mehreren Agenten und mehr als 300 gekoppelten
EDI-Repositories. DB-, Java-, C++-, Test- und Dokumentationsagenten sollen gemeinsame Verträge,
Abhängigkeiten und Blocker kennen, bevor inkompatible Änderungen entstehen.

## Vier getrennte Ebenen

| Ebene | Verbindlicher Inhalt | Beispiel |
|---|---|---|
| Git | Code, Migrationen, Daten-/API-Verträge, ADRs, Tests | Commit und Merge Request |
| lokale Arbeit | private Zwischenschritte eines Agenten | optionaler SQLite-Index |
| Control Plane | aktueller gemeinsamer Arbeitszustand | Task, Claim, Lease, Blocker, Approval |
| Audit/Evidenz | unveränderliche Aktionen und Resultatreferenzen | Event mit Actor, Zeit und Commit-SHA |

Eine Datenbanktransaktion ist sofort konsistent, aber kein Ersatz für Git-Review, Branches und
reproduzierbare Verträge. Git bleibt fachliche und technische Historie; die Control Plane ist
die Wahrheit für flüchtige Koordination.

## Architekturprinzipien

1. **API statt direktem SQL:** Agenten nutzen eine versionierte Control-Plane-API. Direkte
   Schreibrechte auf die Koordinationsdatenbank sind verboten.
2. **Verträge statt freiem Chat:** Agenten tauschen typisierte Commands, Events, Proposals,
   Befunde und Artefaktreferenzen aus. Freitext ergänzt, ersetzt aber keinen Vertrag.
3. **Claims und Leases statt Hoffnung:** Arbeit erhält Owner, Ablaufzeit, Heartbeat und
   monotonen Fencing-Token. Abgelaufene Agenten können nicht weiter schreiben.
4. **Idempotenz:** Jeder Command besitzt eine stabile Request-ID. Wiederholung liefert
   dasselbe Ergebnis oder einen klaren Konflikt.
5. **Optimistische Nebenläufigkeit:** Versionen und kleine Ressourcengrenzen sind Default;
   globale Repo- oder Tabellenlocks sind Ausnahme.
6. **Append-only Audit:** Zustandsänderungen erzeugen unveränderliche Events. Korrekturen sind
   neue Events, kein Umschreiben der Historie.
7. **Human Governance:** Breaking Contracts, Produktion, Rechte, Secrets und irreversible
   Aktionen benötigen risikobasierte Freigaben.
8. **Open Standards und Austauschbarkeit:** Agent, Modell, Workflow-Engine, Eventtransport und
   Persistenz werden durch stabile Verträge entkoppelt.

## Rollen

| Rolle | Verantwortung | Darf nicht allein |
|---|---|---|
| Human Owner | Ziel, Priorität, Risiko und finale fachliche Freigabe | technische Evidenz ignorieren |
| Orchestrator | zerlegt, delegiert, verfolgt Abhängigkeiten und eskaliert | Fachverträge eigenmächtig aktivieren |
| Contract Owner | pflegt Daten-/API-Semantik und Versionierung | abhängige Repos übergehen |
| Domain Worker | implementiert DB, Java, C++, UI, Test oder Doku | fremde Ressourcen ohne Claim ändern |
| Reviewer | prüft Diff, Vertrag, Tests, Sicherheit und Migration | eigenen ungeprüften Scope freigeben |
| Release Agent | prüft integrierten Commit und Deployment-Gates | ohne Approval deployen |
| Observer/Auditor | misst Durchsatz, Qualität, Kosten und Policy-Verstöße | Produktzustand verändern |

Eine Agenteninstanz kann mehrere Rollen beherrschen, aber nicht im selben Hochrisikoschritt
Implementierer und alleiniger Freigeber sein.

## Koordinationsmodell

### Kernobjekte

- `principal`: Mensch, Agent, Servicekonto, Team und Berechtigungen;
- `repository` und `component`: Scope, Owner, Klassifizierung und aktueller Commit;
- `work_item`: Ziel, Status, Priorität, Requirement und Akzeptanzsignal;
- `dependency`: blockiert, benötigt oder beeinflusst ein anderes Work Item/Artefakt;
- `claim`: zugewiesene Arbeit mit erwarteter Generation/Version;
- `lease`: kurzlebige Exklusivität mit Ablauf, Heartbeat und Fencing-Token;
- `contract` und `contract_version`: Daten-, API-, Event- oder Policyvertrag samt Git-SHA;
- `proposal`, `review` und `approval`: Änderung, Evidenz, Entscheidung und Begründung;
- `blocker`: Ursache, Owner, Wirkung, Eskalation und Auflösung;
- `event`: append-only Zustandswechsel mit Correlation-/Causation-ID;
- `artifact_ref`: URI, Commit, Hash, Build, Test- oder Reportreferenz, nicht der gesamte Inhalt;
- `idempotency_key` und `outbox`: sichere Wiederholung und zuverlässige Eventausgabe.

### Zustandsfolge

```text
draft -> proposed -> impact-checked -> claimed -> implemented
      -> verified -> approved -> merged -> active
                  \-> blocked / rejected / superseded
```

Jeder Übergang prüft erwartete Version, Rolle, Policy und Evidenz. Ein Merge oder Deployment
erfolgt weiter über die vorhandene Git-/CI-Plattform.

## Vertrag vor paralleler Implementierung

Bevor ein DB-Agent Tabellen und Java-/C++-Agenten schreibende Clients umsetzen:

1. Der Contract Owner schlägt einen versionierten Vertrag in Git vor.
2. Die Control Plane ermittelt betroffene Repositories und erstellt Review-/Umsetzungsarbeit.
3. Der Vertrag definiert mindestens ID-Erzeugung, Typen, Null-Semantik, Zeitbasis,
   Statuswerte, Checks, Ownership, Idempotenz, Retry, Migration und Kompatibilität.
4. Consumer-Agenten bestätigen die Implementierbarkeit gegen denselben Commit-Hash.
5. Ein Human Gate aktiviert Breaking Changes.
6. Erst danach werden Implementierungs-Claims freigegeben.
7. CI prüft Producer und Consumer gegen dieselbe Contract-Version.

So stimmen Agenten nicht durch Mehrheitschat ab; sie verhandeln einen prüfbaren Vertrag.

## Persistenz

Für einen Proof of Concept ist PostgreSQL der bevorzugte Referenzstore: transaktional,
JSON-fähig, Row-Level Security, breite Toolunterstützung und gut automatisierbar. Oracle bleibt
eine zulässige Unternehmensoption, wenn Betrieb, Support oder vorhandene Plattformstandards
dies verlangen.

Die Anwendung darf nicht von PostgreSQL- oder Oracle-SQL abhängen. Eine Service-API und
versionierte Migrationsschicht halten einen späteren Backendwechsel möglich; vollständige
Portabilität wird nicht behauptet.

Empfohlene logische Schemas sind `coordination`, `contracts`, `audit` und `integration` –
nicht ein Schema pro Agent oder Entwickler. Die Control Plane liegt getrennt von produktiven
EDI-Fachdatenbanken.

Für einen kleinen Proof of Concept genügt PostgreSQL mit Transactional Outbox und Polling oder
`LISTEN/NOTIFY`. Kafka, zusätzliche Consensus-Systeme, Graphdatenbanken und Redis werden erst
bei gemessenem Bedarf eingeführt.

## Standards und technische Rollen

Kein einzelner Standard und kein einzelnes Framework deckt die Control Plane ab:

| Ebene | Standard / Baustein | Rolle |
|---|---|---|
| Agent zu Tool/Context | MCP | Ressourcen, Prompts und Tools standardisiert bereitstellen |
| Agent zu eigenstaendigem Agent | A2A | Faehigkeiten entdecken, Aufgaben delegieren und Resultate austauschen |
| synchrone API | OpenAPI | Control-Plane-Kommandos und Abfragen beschreiben |
| asynchrone API / Event | AsyncAPI + CloudEvents | Ereignisvertraege und Event-Huelle beschreiben |
| Telemetrie | OpenTelemetry | Traces, Metriken und Logs korrelieren |
| dauerhafter Workflow | Temporal oder gleichwertig | Wiederanlauf, Timer, Signale und Langlaeufer |
| Agentlogik | genau ein SDK im ersten POC | Microsoft Agent Framework fuer .NET/Python oder LangGraph fuer Python |
| Zustand | PostgreSQL | Claims, Leases, Fencing, Outbox, Freigaben und Audit |

MCP und A2A sind komplementaer. Sie ersetzen weder Durable Execution noch
Git-, Vertrags-, Datenbank- oder Freigaberegeln.

## Plattformklassen nicht vermischen

| Klasse | Beispiele | Bewertung fuer den Start |
|---|---|---|
| Durable Workflow Engine | Temporal | POC-Kandidat fuer teamuebergreifende Langlaeufer |
| Agent Runtime | Microsoft Agent Framework, LangGraph | einen Kandidaten nach Sprachfit waehlen |
| visuelles Prototyping | Langflow, Flowise | fuer Demo/Entwurf, nicht als Recovery-Control-Plane |
| allgemeine Workflow-Automation | n8n, Dify | Lizenz und Grenzen pruefen; nicht Kern der Codekoordination |
| Batch-Orchestrierung | Kestra, Airflow | fuer geplante Jobs, nicht erster Agenten-POC |
| Daten-/RAG-Plattform | RavenDB | kein Orchestrator; nur bei gemessenem Datenvorteil evaluieren |

Lizenzlage fuer die Vorauswahl:

- Temporal, LangGraph, Microsoft Agent Framework und Langflow sind MIT-lizenziert.
- Flowise ist im Kern Apache 2.0; gekennzeichnete Enterprise-Dateien sind kommerziell.
- Dify nutzt eine modifizierte Apache-2.0-Lizenz.
- n8n nutzt die Sustainable Use License und ist nicht als vollstaendig offene
  Kernplattform zu behandeln.
- RavenDB-Server ist AGPLv3 oder kommerziell lizenziert. Vor internem
  Netzbetrieb und Aenderungen ist eine Rechtspruefung noetig.

## POC-Shortlist

1. PostgreSQL mit Transactional Outbox und zunaechst Polling oder `LISTEN/NOTIFY`.
2. Temporal fuer einen mehrstuendigen, absichtlich unterbrochenen
   DB-/Java-/C++-Vertragsworkflow.
3. Genau ein Agent-SDK:
   - Microsoft Agent Framework bei .NET-Schwerpunkt;
   - LangGraph bei Python-Schwerpunkt.
4. OpenTelemetry fuer Korrelation von Auftrag, Agent, Modell, Tool, Commit und Kosten.
5. GitHub Copilot fuer konkrete Repositoryarbeit, nicht als abteilungsweite Control Plane.

Kein Kafka, Redis, Graphspeicher, RavenDB oder zweites Agent-SDK ohne gemessenen Bedarf.

## Sicherheit und Betrieb

- Workload-Identität statt gemeinsamem API-Key; kurze Tokens und Least Privilege.
- Repository-, Team- und Klassifizierungsgrenzen werden serverseitig erzwungen.
- Secrets liegen in einem Secret Store, nicht in Prompts, Events, SQLite oder PostgreSQL.
- Unvertrauenswürdige Repo-/Issue-Inhalte können keine Systempolicy überschreiben.
- Rohprompts und Modellantworten folgen Klassifizierung, Aufbewahrung und Redaction.
- Metriken unterscheiden Modellantwort, Toolaktion, deterministischen Test und Human Approval.
- Backup, Restore, RPO/RTO und Failover werden praktisch getestet.

## Plattform-Evaluationsgates

Eine Plattform kommt nur in die Shortlist, wenn sie:

1. offene Agent-/Tool-/API-Verträge unterstützt;
2. selbst betrieben oder kontrolliert integrierbar ist;
3. langlebige Workflows, Retry, Timeout und Human Approval beherrscht;
4. Rollen, Audit, Secrets und Mandantengrenzen abbildet;
5. Git, CI und mehrere Sprachen integriert, ohne Codebesitz zu übernehmen;
6. eigene Services, Policies und Datenmodelle modular ergänzen lässt;
7. Export und Exit ohne Verlust von Verträgen und Audit ermöglicht.

## Proof of Concept

Der erste POC koordiniert genau einen additiven DB-Vertrag, einen Java- und einen C++-Consumer:

1. Contract Proposal und Impact-Analyse;
2. parallele Claims ohne Dateikonflikt;
3. simuliertes Agentensterben mit Lease/Fencing;
4. doppelte Events und Commands;
5. Breaking-Change-Blocker plus Human Approval;
6. Git-Merge nur bei übereinstimmendem Contract-Hash;
7. vollständige Audit- und Kosten-/Qualitätsauswertung.

Kein POC-Agent erhält Produktionszugriff oder führt reale EDI-Deployments aus.

## Primaerquellen

- [MCP-Spezifikation](https://modelcontextprotocol.io/specification/latest)
- [A2A: Rolle und Abgrenzung zu MCP](https://a2a-protocol.org/latest/)
- [OpenAPI-Spezifikation](https://spec.openapis.org/oas/latest.html)
- [AsyncAPI-Spezifikation](https://www.asyncapi.com/docs/reference/specification/latest)
- [CloudEvents](https://cloudevents.io/)
- [OpenTelemetry-Spezifikationen](https://opentelemetry.io/docs/specs/)
- [Temporal-Dokumentation](https://docs.temporal.io/)
- [Temporal-Lizenz](https://github.com/temporalio/temporal/blob/main/LICENSE)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Microsoft Agent Framework Lizenz](https://github.com/microsoft/agent-framework/blob/main/LICENSE)
- [LangGraph-Uebersicht](https://docs.langchain.com/oss/python/langgraph/overview)
- [LangGraph-Lizenz](https://github.com/langchain-ai/langgraph/blob/main/LICENSE)
- [Flowise-Lizenz](https://github.com/FlowiseAI/Flowise/blob/main/LICENSE.md)
- [Langflow-Lizenz](https://github.com/langflow-ai/langflow/blob/main/LICENSE)
- [Dify-Lizenz](https://github.com/langgenius/dify/blob/main/LICENSE)
- [n8n-Lizenz](https://github.com/n8n-io/n8n/blob/master/LICENSE.md)
- [RavenDB-Lizenz](https://github.com/ravendb/ravendb/blob/v6.0/LICENSE.txt)
