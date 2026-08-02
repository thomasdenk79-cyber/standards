---
title: AI runtime guard
date: 2026-08-02T17:07:19+02:00
agent: github-copilot-cli
model: github-copilot/gpt-5.6-terra
purpose: Enforce cost-aware context and exclusive local model use across OpenCode and benchmarks.
---

# Why: AI runtime guard

Workspace routing was documented but not technically enforced. OpenCode accepted native model
contexts up to one million tokens, and locally started workers could compete with benchmarks or
an interactive game for the same GPU.

The shared runtime policy now caps OpenCode operating windows at 98,304 context and 8,192 output
tokens. It warns at 65,536 projected tokens and requires a new session at the cap. A local worker
must acquire the existing `local-llm` lease through the runtime wrapper. Manual blockers and
`TL.exe` prevent new local work; a wrapper that sees the game start terminates only its own
worker and unloads only its own Ollama model.

Copilot Auto remains an orchestrator inside the Copilot model pool. It cannot transparently
redirect a live request to Siemens or Ollama, so selected OpenCode workers are launched
explicitly through the wrapper. Siemens workers stay available whenever the local GPU is blocked.

For owner usability, the manual gaming blocker also has a double-click command-menu entrypoint;
it avoids memorized CLI arguments while keeping the automatic `TL.exe` blocker independent.
