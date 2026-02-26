# .agents/traces/ (Template)

This directory contains JSONL traces for multi-agent runs.

Canonical standard:

- `framework/spec/04-observability.md` (§4.5–§4.6)
- `framework/spec/02-sessions-and-memory.md` (§2.1)

## Policy

Trace retention is defined by `PROJECT.md` → **Trace mode**:

- **Mode 1 (committed):** commit **sanitized** traces only.
- **Mode 2 (external / not committed):** keep traces local only and add `.agents/traces/` to `.gitignore`.

Security baseline (always):

- Never commit secrets, API keys, raw env dumps, or large tool outputs.

## Naming

One file per orchestrator run:

```text
.agents/traces/<trace_id>.jsonl
```

Where `trace_id` is:

```text
YYYYMMDDTHHMMSSZ-<task-slug>-<rand4>
```
