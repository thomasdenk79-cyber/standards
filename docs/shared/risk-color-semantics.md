---
title: Visuelle Risikosemantik
doc_type: reference
status: active
canonical: true
---

<!--
Agent: GitHub Copilot CLI 1.0.77
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-31T11:37:19+02:00
Zweck / Warum: Eine einheitliche Farbsprache für Risiko und Kritikalität festlegen.
-->

# Visuelle Risikosemantik

Farben zeigen Risiko und Kritikalität, wenn die Einordnung zuverlässig und nützlich ist. Eine
Stage liefert die Basis; Systemrolle und Auswirkung dürfen die Einstufung erhöhen.

| Farbe | Bedeutung | Typisches Beispiel |
|---|---|---|
| Grau | unbekannt oder nicht bewertet | Kontext fehlt |
| Grün | niedrig | Entwicklung |
| Blau | normal | Integration |
| Gelb | erhöht | QA oder Pre-Production |
| Orange | hoch | Staging |
| Rot | kritisch | Produktion |
| Violett | außergewöhnlich kritisch | zentrale Produktionskomponente |

## Regeln

- Farbe ergänzt immer Text, Symbol oder Tooltip; sie ist nie das einzige Signal.
- Unbekannt bedeutet nicht sicher und bleibt grau.
- Akzent, Badge, Rahmen, Titel oder Prompt sind einem störenden Vollhintergrund vorzuziehen.
- Ohne belastbare Einordnung keine Kritikalität erfinden; bei Unsicherheit grau verwenden.
