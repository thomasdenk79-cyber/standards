---
title: AI runtime control plane
---

# AI runtime control plane

`scripts\ai_runtime.py` is the workspace control plane for AI workers. It
stores only usage metadata (provider, model, token counts, cost, phase and
event) in `C:\GIT\.runtime\ai-runtime\ledger.sqlite3`; it never stores prompts,
responses or credentials.

The policy is `C:\GIT\.memory\ai-runtime-policy.json`:

| Threshold | Action |
|---|---|
| Under 65,536 projected tokens | continue |
| 65,536 or more | warn and finish the current phase |
| 98,304 or more | block the next request; start a fresh session |

## Local-resource protection

Local workers must use `start_ai_worker.ps1`. It acquires the canonical
`local-llm` lease and checks both manual blockers and configured game processes
before and while it runs. If `TL.exe` starts, the wrapper terminates only its
own worker, releases its lease, and unloads its own Ollama model. It never
terminates another agent's process or a shared llama.cpp server.

For manual gaming mode, double-click
`C:\GIT\standards\scripts\ai-runtime-control.cmd` and select **1** to pause
or **2** to resume local AI. The menu requires no parameters. A running
`TL.exe` remains an independent automatic blocker and cannot be overridden by
the resume entry.

```powershell
# Inspect the current context decision and local blockers.
python C:\GIT\standards\scripts\ai_runtime.py status --input-tokens 65536

# Reserve the GPU for a game or other interactive workload.
python C:\GIT\standards\scripts\ai_runtime.py block --reason gaming
python C:\GIT\standards\scripts\ai_runtime.py unblock --reason gaming

# Start a local OpenCode worker through the lease and game guard.
C:\GIT\standards\scripts\start_ai_worker.ps1 `
  -Provider ollama -Model qwen3-coder:30b -Owner "opencode:wtcc" -- `
  opencode -m ollama/qwen3-coder:30b
```

Siemens workers do not consume local GPU capacity and run through the same
wrapper without a local lease:

```powershell
C:\GIT\standards\scripts\start_ai_worker.ps1 `
  -Provider siemens -Model qwen-3.6-27b -Owner "opencode:wtcc" -- `
  opencode -m siemens/qwen-3.6-27b
```

## OpenCode and Copilot boundaries

Run once after changing the policy to cap every configured OpenCode model to
the operating context and output limits. A backup is created next to the
configuration, and provider credentials remain untouched.

```powershell
python C:\GIT\standards\scripts\ai_runtime.py cap-opencode-config
```

OpenCode and GitHub Copilot CLI are separate host runtimes. Neither exposes a
supported API that can transparently replace a running Copilot `Auto` request
with a Siemens or local request. Use Copilot Auto for orchestration and launch
the selected OpenCode worker through the wrapper. The wrapper is the enforced
boundary for local work; direct `opencode` or raw Ollama calls deliberately
bypass it and are not compliant with the workspace routing policy.
