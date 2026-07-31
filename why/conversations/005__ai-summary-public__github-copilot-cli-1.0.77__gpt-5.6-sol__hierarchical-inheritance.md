---
title: Hierarchisches Vererbungsmodell
doc_type: conversation-summary
status: active
canonical: true
classification: public
---

<!--
Agent: GitHub Copilot CLI 1.0.77
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-31T09:18:22+02:00
Zweck / Warum: Die kontextbezogene Vererbung von Regeln, Einstellungen und Dokumentation widerspruchsfrei vereinheitlichen.
-->

# Hierarchisches Vererbungsmodell

## Auftrag

Ein gemeinsames Vererbungsprinzip fuer Markdown, YAML und andere hierarchische
Konfigurations- und Wissensdateien definieren. Pfade sollen den Kontext tragen; Dateinamen und
Inhalte wiederholen ihn nur, wenn Verstaendlichkeit, Werkzeugkonvention oder Eindeutigkeit es
erfordern.

## Warum

Spezielle Dateinamen und getrennte Ladealgorithmen hatten dieselbe Kontextinformation mehrfach
abgebildet. Dadurch konnten Agenten vorhandene Einstellungen uebersehen, unterschiedliche
Prioritaeten annehmen oder Defaults faelschlich als benutzerspezifische Entscheidung ausgeben.

## Entscheidung

- Allgemeine Ebenen werden vor spezifischen Ebenen geladen.
- Kindebenen erben schweigend, ergaenzen neue Aussagen und ueberschreiben oder negieren
  bestehende Aussagen nur explizit.
- Pfad und Dateiname gehoeren zur Information und folgen gemeinsam DRY und SSOT.
- Gleichartige Dateien verwenden nach Moeglichkeit denselben knappen Namen, beispielsweise
  `settings.yml`, waehrend reservierte oder werkzeuggebundene Namen unveraendert bleiben.
- Die kanonische Standards-Dokumentation beschreibt das Modell einmal; Router und
  Menschenansichten verweisen darauf.

## Verworfene Alternativen

- Ein Settings-Sondermodell wurde verworfen, weil dieselbe Vererbungslogik auch fuer
  `AGENTS.md`, weitere Markdown-Dateien und andere Konfigurationen gilt.
- Kontextpraefixe in jedem Dateinamen wurden verworfen, weil der Verzeichnispfad den Kontext
  bereits traegt und bei Umbenennungen sonst widerspruechlich werden kann.
- Implizites Zusammenkopieren aller gleichnamigen Dateien wurde verworfen, weil Authority,
  Scope und Negation sichtbar bleiben muessen.

## Konsequenz

Die Settings-Kette wird auf `settings.yml` vereinheitlicht. Das allgemeine Modell erhaelt drei
konkrete Beispiele und einen eindeutigen Merge-Vertrag. Bestehende Dokument- und
Werkzeugkonventionen bleiben erhalten, wenn eine Umbenennung keinen belastbaren Nutzen bringt.

## Validierung

Die Settings-Aufloesung wird mit gezielten Tests fuer Vererbung, Override, fehlende
Benutzerebene und ungueltige Schluessel geprueft. Dokumentationslinks und verbleibende alte
Dateinamen werden automatisiert gesucht.

why-ref: standards/why/conversations/005__ai-summary-public__github-copilot-cli-1.0.77__gpt-5.6-sol__hierarchical-inheritance.md
