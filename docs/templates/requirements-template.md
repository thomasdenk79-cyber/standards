---
title: "{PROJECT-NAME} – Anforderungen"
doc_type: template
status: draft
canonical: true
---

<!--
Agent: {AGENT}
Model: {PROVIDER/MODEL-ID}
Auftraggeber: {ROLE OR [private user]}
Datum + Uhrzeit: {ISO-8601}
Zweck / Warum: Rückverfolgbare fachliche Anforderungen und akzeptierte Änderungen.
-->

# {PROJECT-NAME} – Anforderungen

Diese Datei wird nur verwendet, wenn Anforderungen nicht mehr übersichtlich im Project Brief
geführt werden können. Implementierungsdetails gehören in Architektur oder ADRs.

## Statusmodell

`proposed` → `accepted` → `implemented`; alternative Endzustände sind `rejected` und
`superseded`.

## REQ-001 – {Kurztitel}

| Feld | Inhalt |
|---|---|
| Status | proposed |
| Quelle | {Rolle, Ticket oder Gesprächsreferenz} |
| Erfasst | {YYYY-MM-DD} |
| Ziel/Nutzen | {warum} |
| Anforderung | {gewünschtes beobachtbares Ergebnis} |
| Akzeptanzkriterien | {Given/When/Then, Beispiel oder messbares Signal} |
| Grenzen | {Nicht-Ziele, Kompatibilität, Sicherheit, Kosten} |
| Annahmen | {sichtbare Interpretation} |
| Offene Fragen | {noch zu klären} |
| Verweise | {Task, ADR, Test, Release oder ablösende REQ-ID} |

## Änderungshistorie

| Datum | Anforderung | Änderung und Grund | Status |
|---|---|---|---|
| {YYYY-MM-DD} | REQ-001 | {neu, präzisiert oder abgelöst – warum} | proposed |
