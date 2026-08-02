# Router des Standards-Repositorys

- **AI-ACCESS:** allowed
- **AI-SECRET-ACCESS:** denied
- **INHERITS:** `C:\GIT\AGENTS.md`
- **OVERRIDES:** none
- **SCOPE:** dieses Repository

> Nach `C:\GIT\AGENTS.md` bei jedem Session-Start lesen.

## Zweck

Dieses Repository ist die kanonische Quelle für gemeinsame Dokumentationsregeln,
MkDocs-Konfiguration, Qualitätsprüfungen und Projektvorlagen.

## Aktueller Stand

- Agent: GitHub Copilot CLI | model: runtime-selected | role: shared instruction maintenance
- Hierarchische Vererbung, explizite Overrides, Zugriffsmarker und Memory-Routing sind in der
  kanonischen Vorlage abgebildet.
- `docs\shared\inheritance.md` vereinheitlicht Erben, Ergänzen, Überschreiben und Negieren für
  Markdown, YAML und weitere hierarchische Dateien; `scripts\settings.py` setzt die
  Settings-Kette zentral um.
- Das vendor-neutrale Repository-Wissensmodell trennt Fachanforderungen, Entscheidungen,
  Arbeitsstatus und Agentenanweisungen und skaliert vom Project Brief bis zur Traceability.
- `scripts\sync_chat_logs.py` verbindet optional erlaubte private Rohsnapshots und zentrale,
  neutrale WHY-Verdichtungen über eine gemeinsame fortlaufende Chatnummer.
- `scripts\local_model_lease.py` koordiniert lokale Ollama-/llama.cpp-Ressourcen
  workspaceübergreifend mit atomarer Lease, Expiry, Wait und owner-sicherem Release.
- `scripts\ai_runtime.py` erzwingt das wirtschaftliche Kontextbudget, protokolliert nur
  Nutzungsmetadaten und blockiert lokale Worker bei Lease-, manuellen oder Gaming-Blockern.
- `scripts\test_docs.py` validiert das aufrufende Repository und überspringt MkDocs nur, wenn
  dort keine Konfiguration existiert.

## Nächster Schritt

- Lokale Modell-Entrypoints über `scripts\start_ai_worker.ps1` an Runtime-Guard und
  Resource-ID `local-llm` anbinden; Siemens-Modelle bleiben für freigegebene
  Routine-Codepakete bevorzugt.
- `docs\templates\agents-template.md` für neue erlaubte Projekt-Router verwenden.

## Bedarfsabhängige Vertiefungen

- Agenten-Hierarchie oder neues Repository: `docs\templates\agents-template.md`
- Vision, Anforderungen, Changes oder Vendor-Instructions:
  `docs\shared\repository-knowledge.md`
- Dokumentationsstruktur: relevante Datei unter `docs\shared\` oder `docs\templates\`
- Klassifizierung oder sensible Daten: `docs\shared\data-handling.md`
- Gesprächsbelege: `docs\shared\chat-logging.md`
- Große operative Detailmengen/SQLite: `docs\shared\working-index.md`
- Teamübergreifende Agentenkoordination: `docs\shared\multi-agent-coordination.md`
- Modellwahl, Delegation oder kostenintensive Langzeitaufgabe:
  `C:\GIT\.memory\model-routing.md`
- Runtime-Guard, OpenCode-Cap oder lokale Gaming-Blocker: `docs\shared\ai-runtime.md`
- Doku-Validierung: `scripts\test_docs.py`
- MkDocs-Vererbung: `mkdocs-base.yml`

## Regeln

- Gemeinsame Best-Practice-Defaults einmal hier pflegen; Projektspezifisches und die endgültige
  Entscheidung über Übernahme, Override oder Deaktivierung bleiben beim Repository-Owner.
- Markdown, YAML und andere hierarchische Dateien folgen
  `docs\shared\inheritance.md`; Sonderregeln pro Dateityp nur bei technischem Bedarf.
- Vor fachlicher Umsetzung muss die Repo-`AGENTS.md` auf die kanonischen Quellen für Vision,
  Ziele/Nicht-Ziele und Anforderungen/Changes verweisen. Der Umfang folgt Risiko und Reifegrad;
  unklare frühe Wünsche dürfen mit sichtbaren Annahmen beginnen.
- Generische Defaults kommen aus `settings.yml`; globale User-Abweichungen aus
  `C:\GIT\user-memory\settings.yml`, optionale persönliche Abweichungen aus
  `C:\GIT\user-memory\<username>\settings.yml`.
- Technische Datei- und Verzeichnisnamen verwenden englisches ASCII-Kebab-Case. Historische
  Artefakte und extern vorgegebene/reservierte Namen wie `AGENTS.md`, `README.md`, `LICENSE`
  oder `CODEOWNERS` werden nicht nur aus Stilgründen umbenannt.
- Projektdateien verweisen auf Standards, statt gemeinsame Langregeln zu kopieren.
- Lokale Owner-Restriktionen und die Policy-Semantik aus dem Root-Router gelten.
- Ändert sich die erforderliche Form eines Projekt-Routers, wird die kanonische Vorlage in
  derselben Änderung aktualisiert.
- Nicht alle `docs\` beim Startup laden; nur aufgabenrelevanten Verweisen folgen.
- Dokumentationsänderungen mit den vorhandenen Tests validieren.



## Memory-Routing

- Repositoryübergreifende Standards-Entscheidung: relevante Shared-Doku und
  `C:\GIT\.memory\decisions.md`.
- Wiederverwendbares Agentenverhalten: über `C:\GIT\agent-memory\INDEX.md` routen.
- Keine personenbezogenen Daten in diesem Repository speichern.
