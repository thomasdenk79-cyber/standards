# WHY — Read-only migration analysis before API writes

| Feld | Wert |
|---|---|
| Agent | GitHub Copilot CLI 1.0.77 |
| Model | github-copilot/gpt-5.6-sol |
| Auftraggeber | private user |
| Datum | 2026-07-31T20:30:00+02:00 |
| Zweck | Eine relationale Change-Management-Quelle belastbar auf ein Issue-System abbilden, ohne vorzeitig Daten zu verändern. |

## Warum

Das Quellmodell enthält Hierarchien, kategorisierte Historie, mehrere Personen je Rolle und
wesentlich mehr Lookup-Werte als das Zielsystem. Ein scheinbar einfaches Feld-zu-Feld-Mapping
würde deshalb unbemerkt Semantik und Historie verlieren.

## Was

- Quell- und Zielmetadaten wurden ausschließlich lesend untersucht.
- Ein lokaler, nicht versionierter Analysesnapshot macht die Untersuchung reproduzierbar.
- Versioniert werden nur Schema, Transformationsregeln und reproduzierbare Exportskripte.
- Ein read-only Import-Manifest trennt Extraktion/Transformation von späteren API-Schreibvorgängen.
- Nicht abbildbare Optionen, Nutzer und Status werden als explizite Validierungsfehler ausgegeben.

## Entscheidungen

- Keine ungeordneten First-row-Regeln für 1:n-Beziehungen.
- Keine stillen Defaults für unbekannte Zieloptionen.
- Ursprüngliche Rollen bleiben semantisch getrennt; vorhandene Zielfelder werden nicht
  zweckentfremdet.
- Personen werden über einen stabilen Zielsystem-Identifier aufgelöst; fehlende Konten bleiben
  sichtbar blockiert.
- Binäre Nutzlasten gehören in einen separaten Migrationsschritt.
- Schreibvorgänge folgen erst nach fachlicher Abnahme eines fehlerfreien Manifests und zunächst
  ausschließlich in einer Testumgebung.

## Verworfene Alternativen

- Direkter Produktivimport während der Schemaerkundung.
- Beliebige Auswahl einer Person aus mehreren Bearbeitern.
- Ablage interner Rohdaten oder Zugangsdaten im Repository.
- Reduktion vieler Quell-Workflows auf einen Zielworkflow ohne sichtbare Verlustanalyse.

## Validierung

- Beide Systeme wurden erfolgreich read-only abgefragt.
- Der lokale Snapshot und das Manifest wurden auf erwartete Objektmengen geprüft.
- Alle Python-Skripte wurden kompiliert.
- Ignorierregeln und Diff wurden auf Rohdaten sowie Zugangsdaten geprüft.
