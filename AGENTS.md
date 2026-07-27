# Standards repository router

- **AI-ACCESS:** allowed
- **INHERITS:** `C:\GIT\AGENTS.md`
- **OVERRIDES:** none
- **SCOPE:** this repository

> Read after `C:\GIT\AGENTS.md` at every session start.

## Purpose

This repository is the canonical source for shared documentation rules, MkDocs configuration, quality checks, and project templates.

## Current state

- Agent: GitHub Copilot CLI | llm: runtime-selected model | role: shared instruction maintenance
- Hierarchical `AGENTS.md` inheritance, explicit overrides, AI-access markers, and
  live memory routing are reflected in the canonical template.
- `scripts\test_docs.py` validates the active calling repository when used through
  a standards submodule and skips MkDocs only when that repository has no config.

## Next step

- Apply `docs\templates\AGENTS-template.md` when a permitted project needs a new
  router; do not create one in owner-controlled repositories without checking policy.

## Required reads

1. Read `README.md` for the repository map.
2. Read only the task-relevant file below:
   - Agent hierarchy or new repository: `docs\templates\AGENTS-template.md`
   - Documentation structure: `docs\shared\` and the relevant template
   - Docs validation: `scripts\test_docs.py`
   - MkDocs inheritance: `mkdocs-base.yml`

## Rules

- Shared behavior belongs here once; project-specific behavior belongs in the project.
- Project files should reference standards instead of copying large shared sections.
- Hierarchy is inherited by default; the deepest applicable `AGENTS.md` may explicitly override parent project/workflow rules for its subtree.
- Repository-owner restrictions take precedence. Support `AI-ACCESS: allowed`, `read-only`, or `denied`.
- Child overrides must name the superseded rule; unmentioned parent rules continue to apply.
- A child cannot weaken platform safety, law, privacy, secret handling, or explicit user constraints.
- When the required shape of project `AGENTS.md` changes, update `docs\templates\AGENTS-template.md` in the same change.
- Do not load all `docs\` at startup. Follow explicit links for the active task.
- Validate documentation changes with the existing docs test when applicable.

## Memory routing

- Standards decisions affecting multiple repositories: update the relevant shared document and `C:\GIT\.memory\decisions.md`.
- New reusable agent behavior: route through `C:\GIT\agent-memory\INDEX.md`.
- Do not store personal information here.
