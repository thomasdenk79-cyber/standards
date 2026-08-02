---
title: Crash consistency check
date: 2026-08-02T17:13:28+02:00
agent: github-copilot-cli
model: github-copilot/gpt-5.6-terra
purpose: Make resume state distinguish planned shutdowns from interrupted work.
---

# Why: crash consistency check

Resume metadata must show whether an agent intentionally finished, prepared a restart, or was
interrupted. Without that distinction, a fresh agent can incorrectly trust an incomplete test,
partially written database state, or an uncommitted diff as completed work.

Project handovers therefore record a closure state: `planned`, `restart`, `crash-recovered`, or
`unknown`. For the latter two states, a new agent must reconcile Git, task and handover state,
validate any SQLite checkpoint, inspect active leases or processes, and treat test evidence as
unknown until confirmed. This extra check is mandatory before further implementation.
