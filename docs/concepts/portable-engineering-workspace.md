---
title: Portabler Engineering-Workspace
doc_type: architecture
status: proposed
canonical: false
---

# Portabler Engineering-Workspace

## Ziel

Ein plattform- und providerunabhängiger Workspace für Menschen und Agents:

- keine festen Benutzer-, Laufwerks- oder Providerpfade;
- eine kanonische Governance-Quelle;
- reproduzierbare Einrichtung nach Neuinstallation;
- minimale, rollenabhängige Kontexte;
- bestehende Providerkonfiguration nur nach sichtbarer Zustimmung ändern.

Der Entwurf wird vor Implementierung mit dem erweiterten Rollenkonzept und verbindlichen
Unternehmens-Blueprints abgeglichen.

## Zwei persistente Variablen

| Variable | Inhalt |
|---|---|
| `ENGINEERING_REPOS_ROOT` | Root aller lokalen Repository-Checkouts |
| `ENGINEERING_GOVERNANCE_ROOT` | Pfad zum Governance-Clone |

Der aktuelle Workspace wird zusätzlich durch `.engineering-workspace.yaml` markiert.

Auflösung:

1. expliziter CLI-Parameter;
2. nächste Markerdatei oberhalb des Arbeitsverzeichnisses;
3. persistente Umgebungsvariable;
4. andernfalls Repo-only-Modus.

Der primäre Agent löst Pfade einmal auf. Subagenten erhalten sie im Run-Vertrag und suchen
nicht erneut.

## Bootstrap

Geplanter CLI-Name: `engws`.

```text
engws ensure --quiet
engws init --interactive
engws configure --interactive
engws doctor
engws reset --scope adapters
```

- Launcher führen `ensure`, nicht `init`, vor dem Modellstart aus.
- `ensure` ist idempotent, headless und bei gültigem Zustand still.
- Nur fehlende oder veraltete Konfiguration startet einen interaktiven Dialog.
- Subagenten dürfen keinen Setup-Dialog öffnen.
- Ein Cache aus Versionen und Hashes verhindert wiederholte Vollprüfungen.

Erster Lauf:

1. eigenen Governance-Pfad erkennen und anzeigen;
2. Repositories-Root erfragen oder erkennen;
3. Variablen persistent und im aktuellen Prozess setzen;
4. Settings erzeugen und gegen Schema validieren;
5. installierte Agent-CLIs und Versionen erkennen;
6. geplante Provideränderungen mit Backup und Diff anzeigen;
7. nur bestätigte Änderungen anwenden und anschließend laden lassen.

## Provider-Adapter

Adapter sind für Copilot, OpenCode, Claude, Codex und Gemini getrennt. Sie verwenden zuerst
offizielle Include-/Instruction-Mechanismen, danach einen kleinen generierten Router. Symlinks
sind optionaler Fallback, kein universeller Standard.

Copilot unterstützt beispielsweise:

- `$HOME/.copilot/copilot-instructions.md`;
- `$HOME/.copilot/instructions/**/*.instructions.md`;
- `COPILOT_CUSTOM_INSTRUCTIONS_DIRS`;
- Repo-`AGENTS.md`, `CLAUDE.md` und `GEMINI.md`.

Regeln:

- keine Providerdatei ungefragt ersetzen;
- Auth-, Token- und Credential-Felder niemals verändern;
- vorhandene Inhalte sichern und Diff anzeigen;
- Managed Blocks oder Includes statt kopierter Langregeln;
- `CLAUDE.md`, `GEMINI.md`, globale Copilot-/Codex-/OpenCode-Dateien sind nur Router auf
  `${ENGINEERING_GOVERNANCE_ROOT}`;
- Provideradapter prüfen nach der Änderung, was tatsächlich geladen wurde.

## Benutzerdateien

```text
<workspace>/.workspace/
  user-settings.yaml
  custom_user.md              optional, userverwaltet
  agent-semantic-memory.md    optional, agentverwaltet
```

Minimalbeispiel:

```yaml
schema_version: 1
chat_language: de
response_style: concise
source_user_md: custom_user.md

semantic_memory:
  enabled: true
  source: agent-semantic-memory.md
  mode: suggest
  read_roles: [request-helper, general-helper, memory-curator]
  propose_roles: [request-helper, general-helper]
  promote_roles: [memory-curator]
  compact_roles: [memory-curator]
  max_bytes: 8192
  max_tokens_soft: 1500
  compact_at_percent: 80
  max_candidates: 10
  compaction_requires_approval: true
```

`custom_user.md` ist informativ und nicht normativ. Es darf Benutzerkontext, Hardware,
Arbeitsumgebung und Secret-Referenzen enthalten, aber keine Secretwerte.

## Semantisches Memory

```markdown
# Agent Semantic Memory

## Preferences
- `preferences.communication` [confirmed|user]: kurz und direkt

## Work and Expertise
- `work.primary_fields` [confirmed|user]: ...

## Planned or Uncertain
- `hardware.planned` [planned|user]: ...

## Candidates
- `C-001` ADD `preferences.example` [suggested]: ...
```

Regeln:

- nur vorhandene Themenüberschriften, höchstens fünf Fakten pro Thema;
- eindeutiger Schlüssel und genau ein aktueller Eintrag je Fakt;
- Candidates gelten nie als Fakten;
- direkte User-Aussage oder explizite Freigabe ist für Promotion erforderlich;
- bestätigte Fakten nicht ohne Freigabe löschen oder semantisch verändern;
- Details bleiben in ihrer Source of Truth; Memory enthält Zusammenfassung oder Verweis;
- Projektinformationen bleiben im Projekt;
- Fakten aus `custom_user.md` werden nicht dupliziert;
- keine Secrets, Chroniken, Rohchats oder Agenten-Selbsterzählungen;
- Git ersetzt eine zusätzliche Änderungshistorie.

`max_bytes` ist das harte, modellunabhängige Limit. Tokens sind ein weiches Modellbudget.
Verdichtung startet am konfigurierten Schwellenwert und läuft nur über eine erlaubte
Memory-Curator-Rolle.

## Rollenbasierter Kontext

| Rolle | Kontext |
|---|---|
| Request-Helper | Settings, relevanter User-Kontext und Memory |
| Orchestrator | freigegebener Request-Brief |
| Architekt | Requirements, Constraints, Architektur |
| Implementierer | Arbeitsblock, Repo-Router, relevante Dateien |
| Tester | Testvertrag und erwartetes Verhalten |
| Reviewer | Requirements, Diff und Evidenz |
| Infrastruktur-Agent | freigegebene Environment-/Secret-Referenzen bei Bedarf |
| Memory-Curator | Semantic Memory, Budget und Kandidaten |

Der Request-Brief enthält Ziel, Kontext, Scope, Non-Scope, Anforderungen, Annahmen, offene
Entscheidungen und Acceptance Criteria. Persönliche Details werden nur übernommen, wenn sie für
den Auftrag erforderlich sind.

## Technische Erzwingung

Promptregeln allein reichen nicht:

- Rollen-ID kommt aus dem vertrauenswürdigen Launcher, nicht aus Selbstauskunft.
- Memory-Schreibzugriffe laufen über ein späteres `memoryctl`.
- `memoryctl` erzwingt Rollen, Budgets, stabile Schlüssel, Lock und atomaren Write.
- Launcher prüft Abschlussantwort, Toolfehler, Dateiscope, Tests und erwartete Artefakte.
- Token-/Kontextgrenzen stoppen Läufe hart.
- Mehrdeutige oder nicht erlaubte Modell-Fallbacks benötigen Owner-Freigabe.

## Plattformen

- gemeinsamer Python-Core;
- Textual-TUI nur für `init/configure`;
- schnelle headless CLI für Launcher und CI;
- Windows-Paket als `.exe`;
- Linux/macOS als native ausführbare Datei;
- `.ps1`- und `.sh`-Dateien bleiben dünne Starter.

## Abnahme

- Neuinstallation lässt sich aus Governance-Clone und Userkonfiguration reproduzieren.
- Alle Provider laden denselben kanonischen Router.
- Direkter und Wrapper-Start liefern dieselbe effektive Policy.
- Keine Providerdatei wird ohne Zustimmung verändert.
- Subagenten starten keinen Setup-Dialog.
- Verschieben beider Rootpfade erfordert nur Variablenänderung und `engws ensure`.
- Memory überschreitet weder Rollen- noch Größenlimits.
