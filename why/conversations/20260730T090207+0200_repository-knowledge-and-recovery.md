---
title: WHY – Repository-Wissen und Recovery
doc_type: rationale
status: active
canonical: false
---

<!--
Agent: GitHub Copilot CLI
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T09:02:07+02:00
Zweck / Warum: Öffentliche, bereinigte Begründung der Standards- und Memory-Änderungen.
-->

# WHY – Repository-Wissen und Recovery

## Auftrag

Eine Workspace-Review sollte sicherstellen, dass Agents fachliche Ziele und Anforderungen
zuverlässig finden, nach einem Crash effizient fortsetzen und trotzdem kreative Freiheit bei der
Lösung behalten.

## Problem

- Fachanforderungen, Agentenanweisungen, TODOs und Handovers waren nicht überall klar getrennt.
- Ein veralteter Workspace-TODO konkurrierte mit Projektquellen und gemeinsamem Agent-Memory.
- Vendor-spezifische Rule-Dateien konnten als zweite fachliche Wahrheit missverstanden werden.
- Rohchats, kuratierte Erinnerungen und öffentliche WHY-Belege waren semantisch vermischt.
- Zu viele Startup-Dateien erhöhen Tokenlast und erschweren einfachen Agents die Orientierung.

## Entscheidung

- `AGENTS.md` bleibt vendor-neutraler Router und Arbeitsvertrag.
- Vision und Anforderungen liegen im Fach-Repo; Umfang und Formalität folgen Reifegrad und Risiko.
- Git und native Session-Persistenz sind die erste Recovery-Ebene; ein knapper Handover ist
  optional, `resume.md` wird nicht parallel geführt.
- Projektgebundene Tasks bleiben im Projekt. Nur repoübergreifende oder noch repo-lose Arbeit
  nutzt die gemeinsame Agenten-Inbox.
- Gemeinsames und persönliches Agent-Memory bleiben getrennt.
- Private Rohchats bleiben 1:1 im privaten User-Bereich. Versionierte Repositories erhalten nur
  bereinigte WHY-Verdichtungen ohne Personenbezug, sensible Inhalte oder geschützte Details.

## Verworfene Alternativen

- Eine feste große Dateiliste pro Repo: zu redundant und zu teuer im Startup-Kontext.
- Vollständige Anforderungen in `AGENTS.md`: macht den Router zur schwer wartbaren Superdatei.
- TODOs im persönlichen Agent-Memory: für andere Agents unsichtbar und fachlich falsch verortet.
- Rohchat-Links aus Git: unvereinbar mit Datenschutz und Repository-Grenzen.

## Konsequenzen

- Projekt-Router nennen kanonische Fachanker.
- Eigene Dateien verwenden lowercase-kebab-case; reservierte Ökosystemnamen bleiben unverändert.
- Materielle Commits referenzieren diese oder eine andere bereinigte Begründung per `why-ref`.
- Historische Evidenz bleibt erhalten, wird aber nicht als Hot Startup Context geladen.

## Evidenz und Prüfung

- Offizielle Herstellerdokumentation zu verschachtelten Agentenregeln, Session-Resume und
  progressiver Kontextladung wurde verglichen.
- Forschung zu Context Rot, Long-Context-Retrieval und Software-Agent-Schnittstellen stützt
  kurze Router, strukturierte Anker und gezielten Abruf.
- Dokumentationsbuild, interne Links, Workspace-Schema und eine unabhängige Fresh-Agent-Abnahme
  dienen als Akzeptanzprüfungen.

## Restunsicherheit

Automatische Rohchat-Exporte sind vendorabhängig. Jede Laufzeit braucht einen Adapter, der ihren
nativen unveränderten Export in den privaten Chatbereich überführt; manuelle Rekonstruktion ist
keine zulässige Alternative.
