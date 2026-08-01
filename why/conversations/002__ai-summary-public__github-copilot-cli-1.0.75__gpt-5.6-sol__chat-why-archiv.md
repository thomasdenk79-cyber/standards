---
title: "Chat-Protokollierung und dauerhaftes WHY-Archiv"
doc_type: conversation-summary
status: accepted
classification: public
chat_number: 002
agent: "GitHub Copilot CLI 1.0.75"
model: "gpt-5.6-sol"
---

# Chat-Protokollierung und dauerhaftes WHY-Archiv

## Warum

Native Agent-Sessions sind technische Quellen, aber kein dauerhaft auffindbarer und
versionierter WHY-Beleg. Gleichzeitig darf ein gemeinsamer Standard Entwickler nicht zur
Speicherung vollständiger privater Gespräche verpflichten.

## Entscheidung

- Private Originale liegen ausschließlich unter `user-memory/why/conversations`.
- Neutrale KI-Zusammenfassungen liegen zentral unter `standards/why/conversations`, weil eine
  Session mehrere, noch unbekannte oder gar keine Fach-Repositories betreffen kann.
- Eine gemeinsame fortlaufende Chatnummer verbindet Original und Zusammenfassung.
- Dateinamen nennen Schutzklasse, Agent, Modell beziehungsweise Modelle und ein sinnvolles Thema;
  Datum, Hash, native Session-ID und Sidecars entfallen.
- Copilot-Originale bleiben im nativen JSONL-Format; Zusammenfassungen sind lesbare
  Markdown-Dateien.
- Standards empfehlen Secret-Redaktion. Ein autorisierter User darf für sein geschütztes
  privates Archiv bewusst die unveränderte Aufbewahrung wählen und übernimmt dafür die
  Verantwortung.
- Materielle Commits referenzieren ausschließlich die zentrale bereinigte Zusammenfassung.

## Ergebnis

Standards-Defaults, persönliche User-Overrides, zentrale WHY-Dokumentation und das
Synchronisationsscript bilden diese Trennung technisch und dokumentarisch ab.
