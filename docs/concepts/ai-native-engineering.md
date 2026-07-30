---
title: AI-native Engineering
doc_type: explanation
status: active
canonical: false
---

<!--
Agent: OpenCode
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T00:14:16+02:00
Zweck / Warum: Risikobasiertes Zielbild für moderne Zusammenarbeit von Menschen und KI-Agenten.
-->

# AI-native Engineering

Ziel ist moderne Softwareentwicklung, in der Menschen und spezialisierte Agenten gemeinsam
planen, implementieren, prüfen, betreiben und lernen. Kein Framework wird blind übernommen;
Kontrollen richten sich nach Risiko und Nutzen.

## Leitprinzipien

1. **Kleine reversible Änderungen:** geringe Paketgröße, klare Diffs, getesteter Rückweg.
2. **Evidenz vor Vertrauen:** Code, Agentenantworten und Dokumentation werden durch Tests,
   Evals, Messwerte oder Review bestätigt.
3. **Minimale Rechte (Least Privilege):** Agenten erhalten nur notwendige Dateien, Tools, Netzwerkziele und
   Berechtigungen.
4. **Eine Wahrheit:** Code, Konfiguration und Entscheidungen haben je eine kanonische Quelle;
   andere Sichten werden erzeugt oder verlinkt.
5. **Beobachtbar und lernfähig:** Fehler werden korreliert, Ursachen beseitigt und als Test,
   Eval oder Regel dauerhaft abgesichert.

## Risikobasierte Freigabe

| Risiko | Beispiel | Mindestkontrolle |
|---|---|---|
| Niedrig | lokale, reversible Doku- oder Codeänderung | Agent-Selbstprüfung + relevante Tests |
| Mittel | gemeinsam genutzte Bibliothek, Schema oder Ablauf | unabhängiger Review + CI + Rollback |
| Hoch | Produktion, Secrets, personenbezogene Daten, destruktive Aktion | menschliche Freigabe + minimale Rechte + Audit + getesteter Rückweg |

Agenten sind weder pauschal Junioren noch pauschal autonom. Befugnis folgt Aufgabe,
nachgewiesener Fähigkeit, Repository-Policy und Auswirkung.

Repository-Owner steuern Codezugriff, Commit und Push getrennt. Ein erlaubter Commit impliziert
keinen Push; eine Schreibfreigabe impliziert weder Deployment noch Produktionszugriff.

## Engineering-Fähigkeiten

| Fähigkeit | Praktische Umsetzung | Anerkannte Grundlage |
|---|---|---|
| Architektur | knappe ADRs für folgenreiche Entscheidungen | [ADR](https://adr.github.io/), [Azure ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record) |
| Dokumentation | Markdown/Git, Review, Tests, generierte MkDocs-Sicht | [Docs as Code](https://www.writethedocs.org/guide/docs-as-code/), [Diátaxis](https://diataxis.fr/) |
| Tests und Evals | risikobasierte Unit-, Integrations-, System- und Regressionstests; Referenzfälle und menschliche Kalibrierung für variable AI-Ausgaben | [Google SRE Testing](https://sre.google/sre-book/testing-reliability/), [OpenAI Evals](https://developers.openai.com/api/docs/guides/evaluation-best-practices/) |
| Delivery | kleine Änderungen, automatisierter Build/Test, kontextbezogene DORA-Metriken | [DORA](https://dora.dev/guides/dora-metrics-four-keys/) |
| Zuverlässigkeit | SLI/SLO, Monitoring, Incident Response, Postmortems, Recovery-Tests | [Google SRE](https://sre.google/sre-book/table-of-contents/), [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) |
| Sicherer SDLC | Anforderungen, sichere Umgebung, Schutz, Tests, Schwachstellenbehandlung | [NIST SSDF](https://csrc.nist.gov/Projects/ssdf), [SSDF für GenAI](https://csrc.nist.gov/pubs/sp/800/218/a/final) |
| Agentensicherheit | Prompt Injection, Output-Validierung, Datenabfluss, Excessive Agency | [OWASP GenAI](https://genai.owasp.org/llm-top-10/) |
| Software-Lieferkette | Abhängigkeiten, SBOM, Build-Provenienz, Signaturen | [CISA SBOM](https://www.cisa.gov/sbom), [SLSA 1.2](https://slsa.dev/spec/v1.2/) |
| AI-Governance | Risiken und Wirkung steuern, messen und verbessern | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [ISO/IEC 42001](https://www.iso.org/standard/81230.html) |
| Service Management | Knowledge, Change, Configuration, Incident, Problem, Improvement | [ITIL](https://www.peoplecert.org/Frameworks-Professionals/ITIL-framework), [ISO/IEC 20000-1](https://www.iso.org/standard/70636.html) |
| Wiederherstellung und Integrität | RPO/RTO nach Risiko, getrennte Backups/Archive und regelmäßig getestete Restores | [Google SRE Data Integrity](https://sre.google/sre-book/data-integrity/) |

## Agentenspezifische Qualität

- Modell, Provider, Version, Prompt/Instructions, Tools und relevante Parameter sind
  nachvollziehbar.
- Prompt- oder Modellwechsel durchlaufen dieselben Referenzfälle und Regression-Evals.
- Softwaretests und AI-Evals werden getrennt behandelt: deterministische Komponenten brauchen
  klassische Tests; variable Agentenentscheidungen brauchen task-spezifische Evals für Output,
  Toolwahl, Argumente und Handoffs sowie stichprobenartige menschliche Kalibrierung.
- Tool-Aufrufe und Ergebnisse werden korreliert protokolliert; Secrets und unnötige
  personenbezogene Daten gelangen nicht in Kontext oder Logs.
- Unvertrauenswürdige Inhalte dürfen Regeln nicht überschreiben. Schreib-, Netzwerk- und
  Ausführungsrechte bleiben begrenzt; hochriskante Aktionen benötigen Approval.
- Ein Agentenfehler gilt erst als nachhaltig behoben, wenn Ursache, Korrektur und passende
  Regression festgehalten sind.

## Fertig-Kriterium (Definition of Done)

Eine Änderung ist fertig, wenn Verhalten und Geltungsbereich klar sind, relevante Tests/Evals bestehen,
Sicherheits- und Datenfolgen geprüft sind, Doku und ADR bei Bedarf aktualisiert wurden und ein
realistischer Rückweg existiert. Welche Kontrollen gelten, definiert das jeweilige Projekt.

Backups gelten erst als belastbar, wenn die Wiederherstellung mit definiertem RPO/RTO praktisch
getestet wurde. Replikation und Git-Historie allein ersetzen kein Wiederherstellungskonzept.

## Einordnung

Dieses Modell ist **ITIL-, NIST- und ISO-informiert**, aber weder ITIL-zertifiziert noch ein
Nachweis der Konformität mit ISO/IEC 20000-1 oder ISO/IEC 42001. Zertifizierbar wäre ein
vollständiges Managementsystem einer Organisation mit festgelegtem Scope, Kontrollen,
Messungen und Audit, nicht diese Markdown-Struktur allein.
