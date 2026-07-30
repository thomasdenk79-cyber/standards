---
title: WT Command Center Python-Referenzdemo
doc_type: conversation-summary
status: active
canonical: true
classification: public
---

<!--
Agent: OpenCode 1.18.9
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T17:00:00+02:00
Zweck / Warum: Produktanforderungen und technische Entscheidungen für eine visuelle Terminal-Steuerzentrale nachvollziehbar sichern.
-->

# WT Command Center Python-Referenzdemo

## Auftrag

Eine kompakte visuelle Steuerzentrale für Windows Terminal und ein kompatibles intelligentes
Terminal als KI-Coding-Demo entwerfen. Das Werkzeug soll Pane-Steuerung, Texteingabe, History,
Favoriten, Session-Import, Scripts, Layoutideen und Companion-Docking verbinden.

## Warum

Intensive Terminal- und Agentenarbeit verteilt zusammengehörige Shells, Agenten, Datenbank-CLIs,
Remote-Sessions und Monitoring auf viele Panes. Häufige Aktionen sollen sichtbar und mit wenigen
Klicks erreichbar sein, ohne das Terminal selbst zu forken.

## Entscheidungen

- Python und PySide6 dienten als schnell iterierbare Desktop-Referenz.
- Terminalprodukte werden anhand ihrer Paketidentität statt nur am gemeinsamen Prozessnamen
  unterschieden.
- Dokumentierte CLI- beziehungsweise Protokollfunktionen haben Vorrang vor Hotkeys und UI-
  Automation.
- Sessiondaten werden nur gelesen; Passwörter, Tokens und Schlüsselmaterial werden nicht
  persistiert.
- Datenbankfachlogik bleibt außerhalb der GUI und ist später für Skills und kontrollierte
  Werkzeugschnittstellen vorgesehen.
- Nach zwei UX-Runden wird der Python-Stand als funktionale Referenzdemo eingefroren. Die
  endgültige Fluent-Oberfläche wird erst nach einem separaten C#-/WinUI-Spike entschieden.

## Verworfene Alternativen

- Ein vollständiger C++-Terminalfork war für eine externe Steuerzentrale unverhältnismäßig.
- PowerShell/WPF wurde wegen wachsender UI- und Zustandskomplexität verworfen.
- Eine sofortige Qt-Quick-/QML-Migration wurde zurückgestellt, um zunächst die Windows-native
  C#-/WinUI-Alternative praktisch zu vergleichen.
- Sichtbare Command-Palette-Automation bleibt nur Demo-Fallback; die Produktlösung soll direkte
  Aktionen oder konfliktarme, einmalig konfigurierte Keybindings verwenden.

## Ergebnis

- Dokumentierter Project Brief, Anforderungskatalog, Architektur, Decisions, Testplan und Handover.
- Python-/Qt-GUI mit Terminalerkennung, Pane-Aktionen, History, Favoriten, Session-Import, Scripts,
  Logging und Debug-Ansicht.
- Direkte Protokollsteuerung für Pane-Erkennung, Split, Input und Close im unterstützten Terminal.
- Automatisierte Tests sowie ein kontrollierter Integrationscheck mit temporärer Probe-Pane.

## Validierung

- Python-Quellen kompiliert.
- Automatisierte Tests erfolgreich.
- Probe-Pane erzeugt, Markertext gelesen und Pane anschließend geschlossen.
- GUI unter dem echten Windows-Qt-Backend gestartet und manuell durch den Auftraggeber bewertet.

why-ref: standards/why/conversations/004__ai-summary-public__opencode-1.18.9__github-copilot-gpt-5.6-sol__wt-command-center-python.md
