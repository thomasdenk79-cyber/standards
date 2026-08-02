---
title: Parallel checkpoint discipline
date: 2026-08-02T17:13:28+02:00
agent: github-copilot-cli
model: github-copilot/gpt-5.6-terra
purpose: Keep parallel agent work current, conflict-aware and resumable.
---

# Why: parallel checkpoint discipline

Multiple agents can change a workspace while another agent still holds stale chat context. A
session-end-only handover is insufficient: it leaves both source state and task documentation
behind the actual work, increases merge conflicts and makes recovery uncertain.

Agents must claim a narrow write scope, reread the current diff and target files before editing,
checkpoint after stable packages and before long or risky work, and commit their verified scope
when policy permits. Handover state records owner, timestamp, commit, test evidence and
dependencies. Agents never blindly bundle foreign changes; explicit owner-requested checkpoint
commits remain an exception.
