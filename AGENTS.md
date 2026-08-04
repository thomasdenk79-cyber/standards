# Router des Standards-Repositorys

- **AI-ACCESS:** allowed
- **AI-SECRET-ACCESS:** denied
- **INHERITS:** `C:\GIT\AGENTS.md`
- **OVERRIDES:** none
- **SCOPE:** dieses Repository

## Zweck

Kanonische gemeinsame Dokumentationsregeln, Konfiguration, Qualitätsprüfungen und Vorlagen.
Diese Datei ist die Single Source of Truth für gemeinsame Abschluss-, Resume- und
Testrelease-Pflichten; Root-/Repo-Router verweisen darauf statt Regeln zu duplizieren.

## Aktueller Stand

- Agent: GitHub Copilot CLI | model: runtime-selected | role: shared instruction maintenance
- Vererbung: `docs\shared\inheritance.md`; Settings-Auflösung: `scripts\settings.py`.
- Runtime/Leases: `scripts\ai_runtime.py`, `scripts\local_model_lease.py`.
- Doku-/Settings-Prüfung: `scripts\test_docs.py`, `scripts\validate_settings.py`.

## Nächster Schritt

- Lokale Worker über `scripts\start_ai_worker.ps1` an Runtime-Guard und `local-llm` anbinden.

## Regeln

- Gemeinsame Defaults einmal hier; Repo-Owner entscheiden lokale Übernahme/Overrides.
- `settings.yml` = vollständige Basis; `user-memory\settings.yml` und optional
  `<username>\settings.yml` = Deltas. Diese Settings-Dateien werden immer geladen.
- `load_user_memory`/`load_agent_memory` steuern nur Memory-Inhalte.
- Projektdateien verweisen auf Standards statt Langregeln zu kopieren.
- Technische Namen: englisches ASCII-Kebab-Case; reservierte/historische Namen nicht umbenennen.
- Repo-Router verweist vor Umsetzung auf kanonische Vision, Ziele und Anforderungen.
- Router-Formänderungen auch in `docs\templates\agents-template.md` nachziehen.
- Nur aufgabenrelevante Doku laden; Änderungen mit vorhandenen Tests validieren.
- Verbindlich für alle Repos: Bei jedem Wartestatus auf den User oder stabilen Meilenstein
  automatisch dokumentieren (Requirements/Acceptance/TODO/Handover aktualisieren).
- Verbindlich für Resume: Projekt muss über Markdown-Stand + `git log` + `git diff` und bei
  Bedarf ergänzenden SQLite-Arbeitsindex wiederanlaufbar sein; letzter Resume-Prompt ins
  Handover schreiben.
- Verbindlich für testbare Zwischenstände: als Git-Commit sichern und als Testversion
  kennzeichnen; Handover referenziert den Commit.

## Bedarfsabhängige Vertiefungen

| Thema | Quelle |
|---|---|
| Router/Repo-Setup | `docs\templates\agents-template.md` |
| Wissensmodell | `docs\shared\repository-knowledge.md` |
| Daten/Sensitives | `docs\shared\data-handling.md` |
| Chat-Logging | `docs\shared\chat-logging.md` |
| Working Index | `docs\shared\working-index.md` |
| Koordination | `docs\shared\multi-agent-coordination.md` |
| Runtime | `docs\shared\ai-runtime.md` |
| Modellwahl | `C:\GIT\.memory\model-routing.md` |

## Routing

- Standards-Entscheidung: relevante Shared-Doku + `C:\GIT\.memory\decisions.md`.
- Wiederverwendbares Agentenverhalten: nur bei aktiviertem/aufgabenrelevantem Agent-Memory über
  `C:\GIT\agent-memory\INDEX.md`.
- Keine personenbezogenen Daten.
