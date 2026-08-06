---
title: Forschungs- und Praxisgrundlagen
doc_type: reference
status: active
canonical: false
---

<!--
Agent: OpenCode
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T00:14:16+02:00
Zweck / Warum: Prüffähige Quellenbasis für Gedächtnis-Architektur und AI-native Engineering.
-->

# Forschungs- und Praxisgrundlagen

Diese Seite belegt, **was extern dokumentiert ist**, und markiert, was nur unsere
Übertragung oder Hypothese ist. Kein einzelner Link beweist das Gesamtsystem.

## Direkt dokumentiert

| Aussage | Quelle |
|---|---|
| `AGENTS.md` ist ein offenes Format; verschachtelte Dateien spezifizieren Teilbäume | [agents.md](https://agents.md/) |
| Codex verkettet Root- bis Arbeitsverzeichnis-Anweisungen; nähere Regeln stehen später | [OpenAI Codex](https://developers.openai.com/codex/guides/agents-md/) |
| OpenCode unterstützt lokale/globale Regeln und explizite, bedarfsgeladenen Referenzen | [OpenCode Rules](https://opencode.ai/docs/rules/) |
| Kleine, hochsignalige Kontexte, Just-in-time Retrieval, schrittweise Offenlegung und Notizen helfen Agenten | [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) |
| Markdown, Git, Reviews und automatisierte Tests bilden Docs as Code | [Write the Docs](https://www.writethedocs.org/guide/docs-as-code/) |
| ADRs halten Kontext, Optionen, Abwägungen, Confidence und Ablösung fest | [Azure ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record), [ADR Community](https://adr.github.io/) |
| Hot/cool/cold/archive optimiert Zugriffskosten nach Nutzung | [Azure Storage Tiers](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview) |

## Forschung, die Teilaspekte stützt

| Arbeit | Relevanz | Grenze |
|---|---|---|
| [CoALA](https://arxiv.org/abs/2309.02427) | modulare Agenten-Gedächtnisse und Aktionen auf externem Gedächtnis | keine Vorgabe für Markdown oder Git |
| [Generative Agents](https://arxiv.org/abs/2304.03442) | vollständige Erfahrungen, Reflexion und dynamischer Abruf | Simulationskontext, kein Coding-Workflow-Standard |
| [PRO-LONG](https://arxiv.org/abs/2607.20064) | strukturiertes Vollprotokoll plus programmatische Suche bei Langzeitaufgaben | Benchmark-spezifisch; kein allgemeiner Sieg über jede Vector-DB |

## Engineering und Governance

| Bereich | Primärquelle |
|---|---|
| Delivery-Messung | [DORA](https://dora.dev/guides/dora-metrics-four-keys/) |
| Zuverlässigkeit, SLOs, Incidents, Postmortems | [Google SRE](https://sre.google/sre-book/table-of-contents/) |
| Softwaretests und AI-Evals | [Google SRE Testing](https://sre.google/sre-book/testing-reliability/), [OpenAI Evals](https://developers.openai.com/api/docs/guides/evaluation-best-practices/) |
| Backup, Wiederherstellung und Datenintegrität | [Google SRE Data Integrity](https://sre.google/sre-book/data-integrity/) |
| Traces, Metriken und Logs | [OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/) |
| Sichere Softwareentwicklung | [NIST SSDF](https://csrc.nist.gov/Projects/ssdf), [SP 800-218A für GenAI](https://csrc.nist.gov/pubs/sp/800/218/a/final) |
| GenAI-/Agentenrisiken | [OWASP GenAI Security](https://genai.owasp.org/llm-top-10/) |
| Software-Lieferkette und Provenienz | [SLSA 1.2](https://slsa.dev/spec/v1.2/), [CISA SBOM](https://www.cisa.gov/sbom) |
| AI-Risikomanagement | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework), [ISO/IEC 42001](https://www.iso.org/standard/81230.html) |
| Digital Product/Service Management | [ITIL](https://www.peoplecert.org/Frameworks-Professionals/ITIL-framework), [ISO/IEC 20000-1](https://www.iso.org/standard/70636.html) |
| Dokumenttypen nach Nutzerbedarf | [Diátaxis](https://diataxis.fr/) |

## Lokale Architekturentscheidungen

Folgende Punkte sind bewusst **unsere** Umsetzung und müssen durch eigene Tests bestätigt werden:

- Projekt-Source-of-Truth, User-Kontext und semantisches Memory als getrennte Domänen;
- Rollen- und Aufgabenbezug als leichtgewichtiger Retriever;
- hot/warm/cold/archive als Analogie für logische Kontext-Temperatur;
- Markdown-Hervorhebung, Wiederholung, Links und Aktualität als kombinierte Salienzindizien;
- Git/Markdown als primäre Lösung und Vector-/Graph-Retrieval erst bei gemessenem Bedarf.

Die Gehirn- und Synapsenmetapher erklärt Verdichtung und Abruf, ist aber keine Behauptung über
biologisches Lernen oder veränderte Modellgewichte.
