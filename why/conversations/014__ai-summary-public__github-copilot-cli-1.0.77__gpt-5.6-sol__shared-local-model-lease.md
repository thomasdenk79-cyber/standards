---
title: "Shared local-model lease and explicit routing boundaries"
classification: public
agent: "GitHub Copilot CLI 1.0.77"
model: "github-copilot/gpt-5.6-sol"
date: "2026-08-02"
---

# Why

An internal engineering role requested reliable cross-workspace routing so independent agents
and benchmarks cannot load competing local models, while remote routine coding remains
available without consuming local accelerator capacity.

## Decision

- Copilot Auto is defined only as selection inside the GitHub Copilot model pool.
- OpenCode and Codex invocations are explicit runtime/provider/model choices, never aliases for
  Copilot Auto.
- Approved Siemens models are preferred for routine coding; local models require the shared
  `local-llm` lease.
- Internal model inventory and routing evidence remain in the restricted workspace policy,
  not in the public documentation tree.
- A dependency-free Python lease uses an OS guard lock, atomic metadata replacement, unique
  lease IDs, expiry, heartbeat renewal, bounded waiting, and owner-checked release.
- Benchmark local-model entrypoints use the same lease and wait rather than creating a
  repository-private blocker.

## Alternatives and verification

A PID-only lock was rejected because PID reuse and unbounded stale files are unsafe. Blindly
deleting expired metadata was rejected because it can race with a newer owner. A third-party
locking dependency was unnecessary. Focused contention, release-ownership, concurrent-winner,
and stale-recovery tests cover the lease; benchmark tests use fake transports and never call a
model.

why-ref: standards/why/conversations/014__ai-summary-public__github-copilot-cli-1.0.77__gpt-5.6-sol__shared-local-model-lease.md
