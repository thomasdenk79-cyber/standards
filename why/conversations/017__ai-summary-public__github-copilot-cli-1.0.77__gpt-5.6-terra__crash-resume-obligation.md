---
title: Crash-resume obligation
date: 2026-08-02T17:13:28+02:00
agent: github-copilot-cli
model: github-copilot/gpt-5.6-terra
purpose: Make all substantial workspace work recoverable after a restart or crash.
---

# Why: crash-resume obligation

A closed terminal or system restart must not require Thomas to reconstruct agent intent from
memory. The root router now makes checkpointing an automatic agent responsibility after verified
milestones, before risky work, at topic changes, and immediately when a restart is announced.

Each active project records its current task, handover, known status, test result, Git state,
risks, next action and resume command in canonical project files. SQLite is reserved for
transactional high-volume state; Markdown and Git remain canonical. Private conversation
evidence follows the configured chat and secret policy, while public WHY records contain only
sanitized decisions.

On the next `Lies C:\GIT\AGENTS.md ein.`, the agent must reconstruct all active topics itself,
report a concise status and ask Thomas which one to resume. Foreign parallel changes are
preserved and made visible rather than blindly committed.
