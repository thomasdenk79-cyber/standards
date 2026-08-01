---
title: Kostenbewusstes Modellrouting
status: accepted
classification: public
chat_number: 011
agent: "GitHub Copilot CLI 1.0.77"
model: "gpt-5.6-sol"
---

# Kostenbewusstes Modellrouting

## Warum

Premium-Modelle wurden auch fuer Routine, Implementierung und wiederholte Toolausgaben
eingesetzt. Das erhoeht Kosten und Kontextverbrauch, ohne die Engineering-Qualitaet
automatisch zu verbessern. Gleichzeitig sollen lokale und guenstigere Modelle nicht fuer
Aufgaben eingesetzt werden, deren Risiko oder Komplexitaet sie nicht verlaesslich abdecken.

## Entscheidung

- `qwen-3.6-27b` via `code.siemens.com` bearbeitet klar begrenzte Implementierung,
  Testentwurf, Diagnose und Routine-Fixes. Dieser Providerzugang verursacht fuer den Owner
  derzeit keine zusaetzlichen Modellkosten.
- GPT-5.6 Terra orchestriert, zerlegt und integriert Aufgaben und fuehrt Routine-Reviews aus.
- GPT-5.6 Sol oder Claude Sonnet 5 bearbeitet Architektur, Security, kritische Reviews,
  irreversible Entscheidungen und Eskalationen.
- Nach zwei belegten Fehlversuchen derselben Stufe wird nicht weiter geloopt. Der Agent
  verdichtet die Evidenz und eskaliert eine Modellstufe.
- Deterministische Tools fuehren Tests aus. Ein LLM ersetzt weder Test-Runner noch
  beobachtbare Abnahmesignale.
- Datenklassifizierung, Providerfreigabe und Netz-/Secret-Policies gehen stets vor Preis.
  Maximal ein lokales LLM darf gleichzeitig laufen.

## Abnahme

Die Kurzregel steht im globalen Router. Die ausfuehrliche Auswahlmatrix, Kontextgrenzen und
Eskalationsleiter stehen in `.memory/model-routing.md`. Neue reproduzierbare Benchmarks duerfen
einzelne Modelle ersetzen, nicht aber die risikobasierte Eskalationslogik oder die Quality
Gates.
