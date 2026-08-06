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

1. `summary` ist der teilbare Best-Practice-Default: Der Agent erzeugt eine fachlich neutrale
   WHY-Verdichtung im zentralen `chat_shared_dir`. Entwickler werden dadurch nicht zur
   Speicherung ihres vollständigen Chatverlaufs verpflichtet.
2. Nur bei ausdrücklich erlaubtem `transcript` wird der native Session-Export **1:1,
   vollständig und ungefiltert** im `chat_private_dir` gespeichert. Zusätzlich muss die
   Userdaten-Policy private Speicherung dort erlauben. Der Export umfasst Reihenfolge,
   User-/Agent-Turns, Tool-Aufrufe, Tool-Ausgaben sowie vertrauliche, sensible und
   personenbezogene Inhalte.
3. Der Rohchat ist append-only: nichts umformulieren, kürzen, sortieren, still korrigieren oder
   überschreiben. Korrekturen erfolgen als neuer Eintrag; abgeschlossene Exporte bleiben
   unverändert. Ist ein nativer Export verfügbar, wird er nicht manuell rekonstruiert.
4. Die Standards-Empfehlung `transcript_secret_handling: redact` ersetzt echte Zugangsdaten
   sichtbar durch `[REDACTED-SECRET]`. Ein autorisierter User darf in seinem
   `settings.yml` bewusst `preserve` wählen. Dann bleibt das native Original einschließlich
   Secrets unverändert und der User verantwortet Schutz, Zugriff und Aufbewahrung des
   Zielverzeichnisses.
5. Es gibt keine redundante Sidecar-Datei. Typ, Agent, Model-ID, Session-ID und Thema stehen im
   Dateinamen; Schutzklasse und Umgang folgen aus Zielordner und dessen `AGENTS.md`. Secret-
   Redaktionen bleiben im Original als `[REDACTED-SECRET]` sichtbar.
6. `off`, `summary` oder eine strengere lokale Policy können die private Aufzeichnung begrenzen.
   Ohne solchen Override gelten `${ENGINEERING_GOVERNANCE_ROOT}/settings.yml`,
   `${ENGINEERING_REPOS_ROOT}/user-memory/settings.yml` und eine vorhandene
   benutzerspezifische Settings-Datei in dieser Reihenfolge.
7. Die WHY-Verdichtung liegt zentral unter
   `${ENGINEERING_GOVERNANCE_ROOT}/why/conversations`. Das ist notwendig, weil
   eine Session mehrere Repositories betreffen, ihr Fach-Repository erst später bekannt werden
   oder vollständig repo-los sein kann. In jeder Verdichtung entfallen Personenbezug,
   Vertrauliches, Sensibles, interne Pfade und unnötige geschützte Projektdetails.
8. `AI-MEMORY-EXPORT` begrenzt, was die Projektgrenze verlässt. `metadata-only` nennt nur die
   Existenz eines Befunds; `sanitized` erlaubt ausschließlich den bereinigten fachlichen Kern.
9. Materielle Commits verweisen mit `why-ref` auf `governance:why/conversations/<datei>`, ein
   Ticket oder einen ADR. Die aktive Regel oder Entscheidung
   bleibt trotzdem ohne den Chat verständlich.
10. Die Verdichtung beantwortet knapp: Welche Rolle wollte was, warum, seit wann, auf welcher
   Evidenz, welche Alternativen wurden verworfen, welche Konsequenz entstand und wie wurde sie
   geprüft. Unbekanntes bleibt sichtbar unbekannt.
11. Eine gemeinsame fortlaufende Chatnummer verbindet private Snapshots und zentrale
   Verdichtungen. Jeder Dateiname nennt zusätzlich Artefakttyp mit Schutzklasse, Agent-Tool,
   LLM-Modell und Thema. Native Session-IDs bleiben im Originalformat und werden nicht im
   Dateinamen dupliziert.

## Technische Persistenzprüfung

Nur bei effektiver Policy `transcript` prüft der Agent vor substanzieller Arbeit einmal je
Tool-Installation beziehungsweise nach einem Tool-Update:

1. Eine abgeschlossene oder laufende Sitzung erscheint nach einem Prozessneustart weiterhin in
   der nativen Session-Liste oder im dokumentierten lokalen Session-Speicher.
2. Die Sitzung lässt sich nativ fortsetzen oder vollständig exportieren. Für `transcript` muss
   der Export auch Tool-Aufrufe und Tool-Ausgaben enthalten; eine reine Chat-Zusammenfassung
   reicht nicht.
3. Der Speicherort ist lokal, zugriffsbeschränkt und passt zur effektiven
   `DATA-CLASSIFICATION`- und `AI-MEMORY-EXPORT`-Policy.
4. Ist Speicherung deaktiviert, aktiviert der Agent sie über die dokumentierte
   Vendor-Konfiguration. Gibt es keinen Schalter, aber einen vollständigen nativen Export,
   richtet er den Export in `chat_private_dir` ein. Ist beides unmöglich, meldet er die Lücke
   sichtbar statt Persistenz zu behaupten.

Der Agent synchronisiert nicht kontinuierlich. Sinnvolle Punkte sind nach einem materiellen
Meilenstein, vor einer Kompaktierung, unmittelbar vor einem materiellen Commit und beim
Session-Ende. Unveränderte Snapshots werden nicht erneut geschrieben.

`${ENGINEERING_GOVERNANCE_ROOT}/settings.yml` formuliert vendor-neutrale Defaults.
User-Overrides liegen unter `${ENGINEERING_REPOS_ROOT}/user-memory`. Diese Dateien sind keine
OpenCode-, Copilot- oder sonstigen Vendor-Konfigurationsdateien.

### Verifizierte lokale Adapter

| Tool | Nachweis und Vorgehen |
|---|---|
| OpenCode 1.18.9 | Sessions werden automatisch in der lokalen OpenCode-Datenbank gespeichert. Mit `opencode session list` prüfen, mit `opencode --continue` fortsetzen und mit `opencode export <session-id>` nativ exportieren. Die Vendor-Konfiguration liegt unter `~\.config\opencode\opencode.json`; `share: disabled` verhindert externes Teilen und deaktiviert nicht die lokale Persistenz. |
| GitHub Copilot CLI 1.0.75 | Sessions werden automatisch unter `COPILOT_HOME` (standardmäßig `~\.copilot`) gespeichert. Mit `/session` oder `/resume` prüfen und mit `copilot --continue` fortsetzen. Für diese Version ist kein separater Schalter zum Aktivieren lokaler Session-Speicherung dokumentiert; daher keine Konfiguration erfinden. Für den privaten Rohbeleg den nativen Session-Export beziehungsweise die dokumentierte `/share`-Dateiausgabe verwenden und anschließend Vollständigkeit sowie Secret-Redaktion prüfen. |

Versionsangaben dokumentieren den geprüften Stand, nicht eine dauerhafte Garantie. Nach einem
Upgrade muss der Adapter erneut gegen CLI-Hilfe oder offizielle Dokumentation geprüft werden.

## Synchronisation

Das Script `${ENGINEERING_GOVERNANCE_ROOT}/scripts/sync_chat_logs.py` setzt die
Dateibenennung und Sicherheitsgrenzen
um. Ein privater Snapshot ist nur bei effektiver Policy `transcript` erlaubt:

```powershell
python "$env:ENGINEERING_GOVERNANCE_ROOT\scripts\sync_chat_logs.py" archive `
  --user <username> `
  --source copilot `
  --session-id <session-id> `
  --chat-number 002 `
  --topic <fachthema>
```

Für OpenCode wird `--source opencode` verwendet. Der Befehl ist idempotent: Ein identischer
Export bleibt `current`; eine fortgeschriebene Sitzung erzeugt einen neuen append-only Snapshot
mit derselben Chatnummer und der nächsten Snapshotnummer.

Die KI erstellt eine oder mehrere thematische, geprüfte und fachlich neutrale
Markdown-Zusammenfassungen. Das Script veröffentlicht sie zentral; mehrere betroffene oder noch
unbekannte Repositories ändern diesen Speicherort nicht:

```powershell
python "$env:ENGINEERING_GOVERNANCE_ROOT\scripts\sync_chat_logs.py" publish-summary `
  --chat-number 002 `
  --agent "GitHub Copilot CLI 1.0.75" `
  --model "gpt-5.6-sol" `
  --topic <fachthema> `
  --title "<Titel>" `
  --classification public `
  --summary <geprüfte-summary.md> `
  --confirm-sanitized
```

`--chat-number` darf beim Original entfallen. Das Script erkennt eine bereits archivierte native
Session und verwendet deren Nummer erneut; nur für eine neue Session vergibt es die nächste
workspaceweit freie Nummer. Die Zusammenfassung verwendet die ausgegebene Nummer ausdrücklich.

Die Summary-Ausgabe enthält die exakte Zeile
`why-ref: governance:why/conversations/<eindeutige-datei>.md` für die Commit-Message. Eine Session
kann mehrere thematische Verdichtungen erhalten; die Chatnummer hält sie zusammen.

`public` ist für den aktuellen Governance-`why`-Scope verbindlich. Eine interne
Installation darf den Scope auf `internal` verschärfen und den Export entsprechend
kennzeichnen; `confidential` und `restricted` gehören ausschließlich in den privaten
User-Memory-Bereich und werden vom Summary-Befehl nicht akzeptiert.

Bei `transcript_secret_handling: preserve` schreibt `archive` den nativen Export bytegleich.
Bei `redact` gelten die eingebauten und optionalen zusätzlichen Secret-Muster.

Klassifizierung, Ableitungsvererbung und Userdaten-Grenzen stehen ausschließlich in
[`data-handling.md`](data-handling.md).

## Verbindliche Dateisyntax

Diese Syntax ist mechanisch anzuwenden. Keine Segmente ergänzen, entfernen, umstellen oder
umbenennen:

```text
NNN-RR__original-restricted__TOOL__MODELLE__THEMA.NATIV
NNN__ai-summary-KLASSE__TOOL__MODELL__THEMA.md
```

| Segment | Exakte Regel |
|---|---|
| `NNN` | Drei Ziffern, workspaceweit fortlaufend; verbindet Original und Summary. |
| `RR` | Zwei Ziffern, bei Originalen immer vorhanden; erster Snapshot `01`, danach `02` usw. |
| `KLASSE` | Im Governance-`why` ausschließlich `public` oder bei entsprechendem Router `internal`. |
| `TOOL` | Agent/Tool in Kleinbuchstaben; Version anhängen, wenn bekannt. |
| `MODELLE` | Alle Modelle des Originals, verbunden mit `-and-`. |
| `MODELL` | Exaktes Modell, das die Summary erzeugt hat. |
| `THEMA` | Aussagekräftiges Kebab-Case, maximal 30 Zeichen. Nur frühe Originale dürfen `topic-pending` verwenden. |
| `NATIV` | Quellformat unverändert: Copilot `.jsonl`, OpenCode `.json`, Plaintext nur `.log`. |

Normalisierung für `TOOL`, `MODELL` und `THEMA`: Kleinbuchstaben; `/`, Leerzeichen und sonstige
Trennzeichen durch `-` ersetzen; keine Schrägstriche im Ergebnis. Datum, Hash, native
Session-ID und Sidecar sind verboten.

### Erlaubte Kombinationen

| Ziel | Erlaubter Typ |
|---|---|
| `${ENGINEERING_REPOS_ROOT}/user-memory/why/conversations/` | `original-restricted` im nativen Format |
| `${ENGINEERING_GOVERNANCE_ROOT}/why/conversations/` | `ai-summary-public.md`; `ai-summary-internal.md` nur bei internem Router |

`ai-summary-restricted` ist im zentralen Standards-Verzeichnis verboten. Kann ein Chat nicht
ausreichend neutralisiert werden, wird dort keine Summary veröffentlicht und kein Commit darf
auf das private Original verweisen.

### Beispiel 1: GitHub Copilot CLI

```text
${ENGINEERING_REPOS_ROOT}/user-memory/why/conversations/002-01__original-restricted__github-copilot-cli-1.0.75__claude-sonnet-5-and-gpt-5.6-sol__chat-why-archiv.jsonl
${ENGINEERING_GOVERNANCE_ROOT}/why/conversations/002__ai-summary-public__github-copilot-cli-1.0.75__gpt-5.6-sol__chat-why-archiv.md
```

```text
why-ref: governance:why/conversations/002__ai-summary-public__github-copilot-cli-1.0.75__gpt-5.6-sol__chat-why-archiv.md
```

### Beispiel 2: OpenCode

```text
${ENGINEERING_REPOS_ROOT}/user-memory/why/conversations/003-01__original-restricted__opencode-1.18.9__siemens-deepseek-v4-flash__git-windows-pfade.json
${ENGINEERING_GOVERNANCE_ROOT}/why/conversations/003__ai-summary-public__opencode-1.18.9__siemens-deepseek-v4-flash__git-windows-pfade.md
```

Wenn nur ein Dateiname angefordert ist, gibt der Agent ausschließlich den Dateinamen aus.
Er erfindet weder Zeitstempel, Hash, Session-ID, Sidecar, Schutzklasse noch Dateiendung.

## Aufbewahrung

- Private Rohchats: lokal, Git-ignoriert und zugriffsbeschränkt gemäß gewählter Secret-
  Behandlung aufbewahren.
- Bereinigte Verdichtungen: zentral und versioniert unter
  `${ENGINEERING_GOVERNANCE_ROOT}/why/conversations/`
  aufbewahren und aus den zugehörigen materiellen Commits per exaktem Pfad referenzieren.
- Private Originale werden niemals aus Git-Commits referenziert.
- Verdichtung ersetzt oder verändert niemals den privaten Rohbeleg.

Das Verfahren übernimmt analog die GoBD-Ordnungsprinzipien Vollständigkeit,
Nachvollziehbarkeit, Ordnung und erkennbare Korrektur. Es behauptet keine rechtliche
GoBD-Konformität. Lokale Git-Historie ist kein sicherer Ort für Secrets: Ein späteres Löschen
aus der Arbeitskopie entfernt sie nicht zuverlässig aus früheren Commits.
