---
title: Chat-Protokollierung
doc_type: reference
status: active
canonical: true
---

<!--
Agent: OpenCode
Model: github-copilot/gpt-5.6-sol
Auftraggeber: [private user]
Datum + Uhrzeit: 2026-07-30T00:14:16+02:00
Zweck / Warum: Sichere kanonische Policy für Gesprächsevidenz ohne Root-Kontext zu überladen.
-->

# Chat-Protokollierung

## Zweck

Chats sind das vollständige Arbeitsjournal und damit Rohbeleg, aber nicht die primäre aktuelle
Wahrheit. Kanonische Entscheidungen, Projektzustand und dauerhafte Erkenntnisse werden während
der Arbeit zusätzlich in ihre Zieldateien geroutet.

## Regeln

1. Bei `transcript` wird der native Session-Export **1:1, vollständig und ungefiltert** im
   `chat_private_dir` gespeichert. Das umfasst Reihenfolge, User-/Agent-Turns, Tool-Aufrufe,
   Tool-Ausgaben sowie vertrauliche, sensible und personenbezogene Inhalte.
2. Der Rohchat ist append-only: nichts umformulieren, kürzen, sortieren, still korrigieren oder
   überschreiben. Korrekturen erfolgen als neuer Eintrag; abgeschlossene Exporte bleiben
   unverändert. Ist ein nativer Export verfügbar, wird er nicht manuell rekonstruiert.
3. Einzige Inhaltsausnahme sind echte Zugangsdaten wie Passwörter, Tokens und private Schlüssel.
   Sie werden sichtbar als `[REDACTED-SECRET]` ersetzt und bei Exposition rotiert. Vertrauliche
   oder sensible Fach- und Personendaten sind keine Secrets und bleiben im privaten Rohchat.
4. Metadaten werden nicht in den Originalexport geschrieben, sondern in einer Sidecar-Datei.
   Sie enthält Agent, exakte Model-ID, Session-ID, Zeitraum, Format, Klassifizierung, Zweck und
   nach Abschluss den SHA-256-Hash des unveränderten Exports.
5. `off`, `summary` oder eine strengere lokale Policy können die private Aufzeichnung begrenzen.
   Ohne solchen Override gilt der Workspace-Default aus `workspace-settings.yml`.
6. Im `chat_shared_dir` liegt **kein zweites Rohprotokoll**, sondern eine bereinigte fachliche
   WHY-Verdichtung für jede Session, die versionierte Artefakte ändert oder eine dauerhafte
   Entscheidung trifft. Dort entfallen Personenbezug, Vertrauliches, Sensibles, interne Pfade
   und geschützte Projektdetails; Redaktionen werden sichtbar gekennzeichnet.
7. `AI-MEMORY-EXPORT` begrenzt, was die Projektgrenze verlässt. `metadata-only` nennt nur die
   Existenz eines Befunds; `sanitized` erlaubt ausschließlich den bereinigten fachlichen Kern.
8. Materielle Commits verweisen mit `why-ref` auf die passende bereinigte Verdichtung, ein Ticket
   oder einen ADR. Die aktive Regel oder Entscheidung bleibt trotzdem ohne den Chat verständlich.
9. Die Verdichtung beantwortet knapp: Wer beziehungsweise welche Rolle wollte was, warum, seit
   wann, auf welcher Evidenz, welche Alternativen wurden verworfen, welche Konsequenz entstand
   und wie wurde sie geprüft. Unbekanntes bleibt sichtbar unbekannt.

Klassifizierung, Ableitungsvererbung und Userdaten-Grenzen stehen ausschließlich in
[`data-handling.md`](data-handling.md).

## Mindestmetadaten

Rohdatei: `YYYYMMDDTHHMMSS+HHMM_{session-id}.{jsonl|log}`

Sidecar: `YYYYMMDDTHHMMSS+HHMM_{session-id}.meta.yml`

Verdichtung: `YYYYMMDDTHHMMSS+HHMM_{session-id}_{topic}.md`

Dateinamen sind Windows-sicher und enthalten das Modell nicht redundant; die exakte Model-ID
steht einmal in der Sidecar-Datei beziehungsweise im Metadatenblock der Verdichtung.

## Aufbewahrung

- Private Rohchats: lokal, Git-ignoriert, zugriffsbeschränkt und unverändert aufbewahren.
- Bereinigte Verdichtungen: versioniert im `chat_shared_dir` aufbewahren und aus den zugehörigen
  materiellen Commits referenzieren.
- Verdichtung ersetzt oder verändert niemals den privaten Rohbeleg.

Das Verfahren übernimmt analog die GoBD-Ordnungsprinzipien Vollständigkeit,
Nachvollziehbarkeit, Ordnung und erkennbare Korrektur. Es behauptet keine rechtliche
GoBD-Konformität. Lokale Git-Historie ist kein sicherer Ort für Secrets: Ein späteres Löschen
aus der Arbeitskopie entfernt sie nicht zuverlässig aus früheren Commits.
