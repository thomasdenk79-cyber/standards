---
title: Owner-controlled repository defaults
doc_type: conversation-summary
status: accepted
classification: public
---

# Owner-controlled repository defaults

## Why

A shared standard was described too easily as a mandatory repository profile. That would
contradict the intended inheritance model and could remove authority from repository owners.

## Decision

- `standards` defines coherent, vendor-neutral best-practice defaults so every team does not
  reinvent the same foundations differently.
- Defaults apply through explicit inheritance only while no authorized local override replaces
  them.
- The repository owner has the final decision for the repository scope and may adopt, refine,
  replace or disable defaults.
- The repository owner may permit read/write access, restrict agents to read-only operation or
  prohibit AI agents completely.
- Repository archetypes can suggest useful defaults but never create mandatory profiles.
- Agents cannot grant themselves permissions or override owner policy.
- Higher-level legal, security, privacy and secret-protection boundaries remain effective.

## Result

The repository knowledge model, router template, standards router and repository overview now
state owner control and complete opt-out explicitly.
