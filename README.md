# Engineering Governance

Providerunabhängige Engineering-Regeln, Router, Vorlagen und Validatoren für Menschen und
Agents. Gemeinsame Inhalte werden hier einmal gepflegt; Fach-Repositories verweisen darauf.

## Pfade

```text
ENGINEERING_REPOS_ROOT       Root aller lokalen Repositories
ENGINEERING_GOVERNANCE_ROOT Clone dieses Repositories
```

Interaktive Windows-Einrichtung aus dem Governance-Clone:

```powershell
$reposRoot = Read-Host "Repository-Root"
$governanceRoot = (Get-Location).Path
[Environment]::SetEnvironmentVariable("ENGINEERING_REPOS_ROOT", $reposRoot, "User")
[Environment]::SetEnvironmentVariable(
    "ENGINEERING_GOVERNANCE_ROOT",
    $governanceRoot,
    "User"
)
```

Neue Prozesse übernehmen die Werte. Provider-, Benutzer- und Laufwerkspfade gehören nicht in
kanonische Dokumente oder Skripte.

## Inhalt

| Pfad | Inhalt |
|---|---|
| `AGENTS.md` | kanonische Workspace-Policies |
| `docs/` | Konzepte, Referenzen und Vorlagen |
| `settings.yml` | aktuelle Policy-Defaults |
| `scripts/` | Runtime-, Settings- und Dokumentationswerkzeuge |
| `mkdocs-base.yml` | gemeinsame MkDocs-Basis |

## Dokumentation

Repo-Konfigurationen dürfen den Platzhalter `${ENGINEERING_GOVERNANCE_ROOT}` verwenden.
MkDocs selbst verbindet Umgebungsvariable und Dateisuffix nicht; deshalb löst der gemeinsame
Wrapper den Platzhalter vor dem Build auf.

```powershell
python "$env:ENGINEERING_GOVERNANCE_ROOT\scripts\run_mkdocs.py" build --strict
```

## Status

Der portable Bootstrap, Provider-Adapter und das begrenzte semantische User-Memory sind als
Entwurf dokumentiert. Die Implementierung folgt erst nach Review des erweiterten
Rollenkonzepts und der verbindlichen Unternehmens-Blueprints.
