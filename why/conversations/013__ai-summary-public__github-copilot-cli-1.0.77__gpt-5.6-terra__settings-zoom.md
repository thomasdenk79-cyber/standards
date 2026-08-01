---
title: "Atomare Settings und Zoom-Konsistenz"
doc_type: conversation-summary
status: accepted
classification: public
chat_number: 013
agent: "GitHub Copilot CLI 1.0.77"
model: "gpt-5.6-terra"
---

# Atomare Settings und Zoom-Konsistenz

# Atomare Settings und Zoom-Konsistenz

## Anlass

Die Settings-Persistenz verwendete eine feste Tempdatei und konnte bei parallelen UI-Ereignissen
mit dem eigenen Schreibvorgang kollidieren. Zoomgrenzen, Rundung und Prozentanzeige waren an
mehreren Stellen definiert.

## Entscheidung

Settings-Saves werden serialisiert, in eindeutige Tempdateien geschrieben, auf Datenträger
geflusht und mit atomarem Replace samt rotierender Sicherung übernommen. Eine kleine gemeinsame
Zoom-Hilfe definiert Grenzen, Rundung und Anzeige.

## Verifikation

Gezielte Persistenz- und Zoomregressionen, die vollständige Core-Suite, der WinUI-Build und die
Dokumentationsprüfung liefen erfolgreich.
