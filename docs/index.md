---
title: Workspace-Dokumentation
doc_type: explanation
status: active
canonical: false
---

<!--
Agent: OpenCode
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-29T23:20:33+02:00
Zweck / Warum: Einstieg in die abgeleitete MkDocs-Sicht auf das Workspace-Memory-System.
-->

# Workspace-Dokumentation

Ein adaptives externes Gedächtnis für KI-Agenten auf Basis von Markdown und Git.

## Einstieg

- [Konzepte](concepts/index.md)
- [Betriebsmodell](concepts/operating-model.md)
- [AI-native Engineering](concepts/ai-native-engineering.md)
- [Repository-Wissensmodell](shared/repository-knowledge.md)
- [Forschungs- und Praxisgrundlagen](shared/research-foundations.md)
- [Repos](repos/index.md)
- [Agents](agents/index.md)

## Grundidee

`AGENTS.md`-Dateien bilden vererbte, verzeichnisspezifische Router. Knappe Indizes und
`READ-WHEN` laden Details erst bei Bedarf. Git bewahrt Historie und Begründungen; Projekt-,
User- und Agent-Memory trennen die Zuständigkeit. Hot/warm/cold/archive und kombinierte
Salienzsignale steuern,
welcher Kontext wahrscheinlich benötigt wird.

Diese Site ist eine **abgeleitete Menschenansicht**, keine zweite Regelquelle. Die kanonischen
Quellen sind im [Betriebsmodell](concepts/operating-model.md#kanonische-quellen) aufgeführt.
