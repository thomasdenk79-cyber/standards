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
- Das vendor-neutrale Repository-Wissensmodell trennt Fachanforderungen, Entscheidungen,
  Arbeitsstatus und Agentenanweisungen und skaliert vom Project Brief bis zur Traceability.
- `scripts\test_docs.py` validiert das aufrufende Repository und überspringt MkDocs nur, wenn
  dort keine Konfiguration existiert.

## Nächster Schritt

- `docs\templates\agents-template.md` verwenden, wenn ein erlaubtes Projekt einen neuen Router
  benötigt. In fremden oder owner-kontrollierten Repositories vorher die Policy prüfen.

## Bedarfsabhängige Vertiefungen

- Agenten-Hierarchie oder neues Repository: `docs\templates\agents-template.md`
- Vision, Anforderungen, Changes oder Vendor-Instructions:
  `docs\shared\repository-knowledge.md`
- Dokumentationsstruktur: relevante Datei unter `docs\shared\` oder `docs\templates\`
- Klassifizierung oder sensible Daten: `docs\shared\data-handling.md`
- Gesprächsbelege: `docs\shared\chat-logging.md`
- Doku-Validierung: `scripts\test_docs.py`
- MkDocs-Vererbung: `mkdocs-base.yml`

## Regeln

- Gemeinsame Best-Practice-Defaults einmal hier pflegen; Projektspezifisches und die endgültige
  Entscheidung über Übernahme, Override oder Deaktivierung bleiben beim Repository-Owner.
- Vor fachlicher Umsetzung muss die Repo-`AGENTS.md` auf die kanonischen Quellen für Vision,
  Ziele/Nicht-Ziele und Anforderungen/Changes verweisen. Der Umfang folgt Risiko und Reifegrad;
  unklare frühe Wünsche dürfen mit sichtbaren Annahmen beginnen.
- Sprachdefaults kommen ausschließlich aus `C:\GIT\workspace-settings.yml`.
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
