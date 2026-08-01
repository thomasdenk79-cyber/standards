# WHY — EDI-Oracle→PostgreSQL-Benchmark-Lauf (claude-sonnet-5) samt unabhängiger Verifikation

| Feld | Wert |
|---|---|
| Agent | GitHub Copilot CLI 1.0.77 |
| Model | github-copilot/claude-sonnet-5 |
| Auftraggeber | private user |
| Datum | 2026-07-31T17:08+02:00 bis 2026-07-31T18:53+02:00 |
| Zweck | Einen weiteren Multi-LLM-Benchmark-Datenpunkt (Modell `claude-sonnet-5`) für den EDI-Repository-/Oracle→PostgreSQL-Analyseauftrag erzeugen, unabhängig verifizieren und gefundene Mängel beheben. |

## Warum

Der Master-Prompt `C:\git\OpenCode_EDI_Multi-LLM_Benchmark_Prompt.md` verlangt einen
reproduzierbaren, read-only Analyselauf über `C:\git\edi` (>250 verschachtelte Repos) plus einen
lokal funktionierenden HTML-Bericht, um verschiedene LLMs auf Qualität, Vollständigkeit,
Ehrlichkeit und Kosten vergleichbar zu machen. Dieser Lauf ergänzt bereits vorhandene Runs anderer
Modelle (`gpt-5.6-sol`, `gpt-5.3-codex`, `qwen3.6-35b-a3b-q4_k_m`, `qwen3`, `qwen-3.6-27b`,
`gpt-oss-120b`) unter `C:\GIT\llm-benchmarks\` um einen weiteren vergleichbaren Datenpunkt.

## Was

- Nicht ersetzte Platzhalter (`MODEL_ID`, `PROVIDER`, `RUN_ID`, Preise) interaktiv mit dem
  Auftraggeber geklärt, statt sie zu erfinden oder zu erraten.
- Phase 0 (globale Anweisungshierarchie `C:\git\AGENTS.md` inkl. aller Referenzen) vollständig
  gelesen, bevor irgendeine Analyse begann.
- Den eigentlichen, sehr umfangreichen Analyse- und Berichtslauf an einen Hintergrund-Agenten
  delegiert (deterministische Python-Pipeline, LOC/SQL-/PLSQL-/Oracle-Feature-Scan, Migrations-
  Scoring-Modell, lokal funktionierender HTML-Bericht ohne CDN, Benchmark-Telemetrie, lokale
  Git-Commit-Serie) unter `C:\GIT\llm-benchmarks\claude-sonnet-5__20260731-171545__edi-analysis`.
- Nach Abschluss das Ergebnis **unabhängig** (nicht nur den Selbstbericht) geprüft:
  - Repo-Zahl per eigenem `Get-ChildItem -Filter .git -Recurse` gegengezählt (327 = 327).
  - Repo-Summen (Dateien, Netto-LOC, Bytes, SQL-Dateien) gegen `totals` in `metrics.json`
    aufsummiert und exakt abgeglichen.
  - LOC zweier kleiner Repos manuell nachgezählt (3 und 93 Zeilen) — exakte Übereinstimmung.
  - Alle JSON-Dateien, die CSV-Datei und die SQLite-Integrität eigenständig geprüft.
  - Quell- und Designreferenz-Root auf Schreibfreiheit während des Laufs geprüft (keine
    Änderungen).
  - Git-Historie, Remote-Freiheit und sauberen Working Tree im Arbeitsverzeichnis geprüft.
  - `report.js` unabhängig mit `node --check` validiert und auf CDN-/externe URLs sowie
    absolute Quellpfade durchsucht (keine gefunden).
  - Ein erster Verdacht (Oracle-Feature-Unterzählung durch eine Datei-Leselimite bei sehr
    großen SQL-Dateien) durch eine zweite, methodisch identische Gegenprobe (inkl. Kommentar-
    Entfernung) selbst widerlegt, statt eine Vermutung ungeprüft als Fehler zu melden.
  - Ein zweiter, tatsächlich bestätigter Mangel gefunden: `report.js` fügte aus
    Repository-/Analysedaten stammende Strings ungeprüft per `innerHTML` ein (Verstoß gegen die
    Master-Prompt-Vorgabe "keine ungeprüfte Einfügung von Repository-Inhalten per innerHTML").

## Entscheidungen

- Erst nach expliziter Klärung aller Platzhalter mit dem Auftraggeber begonnen; keine
  eigene Modell-ID erfunden.
- Für den sehr umfangreichen, klar abgegrenzten Analyselauf einen separaten Hintergrund-Agenten
  mit vollständigem Kontext eingesetzt, statt ihn im selben Kontextfenster zu erledigen.
- Den Selbstbericht des Hintergrund-Agenten nicht ungeprüft übernommen, sondern mit eigenen,
  unabhängigen Methoden (Gegenzählung, Stichproben, Syntax-/Integritätsprüfung) verifiziert.
- Eine widerlegte erste Fehlervermutung transparent als "geprüft und nicht bestätigt"
  dokumentiert, statt sie stillschweigend fallen zu lassen oder unbegründet zu "reparieren".
- Den bestätigten `innerHTML`-Mangel direkt behoben (escape-Helfer `esc()` eingeführt) und die
  vorher fehlende Dokumentation des 8-MB-Lesefensters für inhaltlich erkannte SQL-Kandidaten
  nachträglich in `ASSUMPTIONS.md` ergänzt.
- Ausschließlich lokale Commits im Arbeits-Repository erzeugt; kein Remote, kein Push, keine
  Änderung an `SOURCE_ROOT` oder `DESIGN_REFERENCE_ROOT`.

## Verworfene Alternativen

- Eine geratene oder selbst erfundene Modell-/Run-ID anstelle einer Rückfrage.
- Den Selbstbericht des Hintergrund-Agenten unkritisch als "geprüft" an den Nutzer weiterreichen.
- Den ersten (letztlich falschen) Verdacht der Datei-Leselimite ungeprüft als Bugfix umsetzen und
  Metrik-/Report-Daten ohne Beleg neu berechnen.
- Größere, nicht angeforderte Refactorings der Analyse-Pipeline anlässlich einer kleinen,
  bestätigten Report-Korrektur.

## Validierung

- `python -m unittest tests.test_analysis` (3/3 bestanden) vor und nach der Korrektur.
- `node --check report\assets\report.js` vor und nach der Korrektur bestanden.
- `git status` im Arbeitsverzeichnis nach dem Fix-Commit: sauber, keine Reste.
- `C:\git\edi` und die Design-Referenz nach Lauf und Fix ohne neue/geänderte Dateien seit
  Laufbeginn (`Get-ChildItem -Recurse | Where LastWriteTime > Laufbeginn`: 0 Treffer).
- Repo-Zahl, Datei-, Byte- und LOC-Summen sowie SQL-Dateizahl unabhängig gegengeprüft und exakt
  bestätigt (327 / 59.748 / 2.754.181.992 Bytes / 13.649.938 Netto-LOC / 27.853 SQL-Dateien).

## Follow-up

- `agent-memory\inbox.md` (INBOX-003) um diesen weiteren Modell-Datenpunkt ergänzt; das
  vollständige Multi-Modell-Vergleichs-Rollup über alle `llm-benchmarks\*__edi-analysis`-Läufe
  steht noch aus.
- Kein Bedarf für einen erneuten Analyselauf; nur `report/assets/report.js` und `ASSUMPTIONS.md`
  wurden nach der Verifikation geändert und neu committet (Commit `7918701`).
