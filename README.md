# standards

Zentrale Standards, Templates und gemeinsame Docs für alle Repos von Thomas Denk.

> **Dieses Repo ist der einzige Ort wo gemeinsame Dinge gepflegt werden.**
> Alle anderen Repos referenzieren es — nie kopieren, immer referenzieren.

## Was hier drin ist

| Pfad | Inhalt |
|---|---|
| `mkdocs-base.yml` | MkDocs Theme-Config — alle Repos erben davon |
| `docs/shared/` | Gemeinsame Docs (KI-Konzept, SOTA, Guidelines) |
| `docs/templates/` | Vorlagen: AGENTS.md, Changelog, Runbook |
| `scripts/test_docs.py` | Docs-Qualitätstest für alle Repos |

## Neues Repo einrichten

```bash
# 1. standards als Submodule einbinden
cd C:\GIT\mein-neues-repo
git submodule add https://github.com/thomasdenk79-cyber/standards.git standards

# 2. mkdocs.yml anlegen die von standards erbt
# (siehe docs/templates/mkdocs-repo.yml)

# 3. AGENTS.md aus Template kopieren
copy standards\docs\templates\agents-template.md AGENTS.md
```

## Update standards in allen Repos

```bash
# In jedem Repo das standards als Submodule hat:
git submodule update --remote standards
git add standards && git commit -m "chore: standards aktualisiert"
```
