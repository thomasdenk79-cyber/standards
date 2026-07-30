---
title: WHY – Memory-Temperatur und Workspace-Taxonomie
doc_type: rationale
status: active
canonical: false
---

<!--
Agent: GitHub Copilot CLI
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T09:55:00+02:00
Zweck / Warum: Öffentliche Begründung der fließenden Retrieval-Temperatur und der anstehenden Workspace-Strukturierung.
-->

# WHY – Memory-Temperatur und Workspace-Taxonomie

## Anlass

Die bisherige Tabelle konnte so gelesen werden, als sei Git-Historie grundsätzlich cold/archive
und als gäbe es vier harte Behälter.

## Entscheidung

- Filesystem-Stand, uncommittierter Diff und jüngste relevante Commits sind normalerweise hot.
- Git-Historie kann abhängig von Aufgabe und Evidenzbedarf hot, warm, cold oder archive sein.
- Die vier Namen bleiben verständliche Anker auf einem Kontinuum.
- Zwischenbegriffe wie `very warm`, `very cold` oder `deep archive` sind beschreibend erlaubt,
  erzeugen aber keine zusätzlichen Pflichtklassen.
- Es gelten keine starren globalen Tagesgrenzen; Agents bestimmen die Lesetiefe nach
  Änderungsrate, Risiko, Widerspruch und Aufgabe.

## Evidenz

AWS, Azure und Google verwenden wenige diskrete Zugriffsklassen und automatisierte
Lifecycle-Regeln statt immer feinerer manueller Stufen. Bei lokalen Textdateien ist nicht
Speicherlatenz, sondern Kontext-/Tokenbudget die relevante Kostenachse.

## Folgearbeit

Die vielen lokalen Repositories sollen bibliotheksartig über stabile Kategorien und einen
kleinen Katalog auffindbar werden. Vor einer Umstrukturierung werden Git-Grenzen, Tool-Discovery,
Owner, Pfadabhängigkeiten und Junctions geprüft; diese Verdichtung trifft noch keine
Verschiebeentscheidung.
