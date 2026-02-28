# .agents/traces/

This directory is the conventional location for per-run JSONL traces produced by the orchestrator.

Canonical standard:

- `framework/spec/04-observability.md` (§4.5–§4.6)
- `framework/spec/02-sessions-and-memory.md` (§2.1)

## Policy

- Trace files (`.agents/traces/*.jsonl`) are **local-only** and are **never committed**.
- This README (`.agents/traces/README.md`) **may be committed** to keep the trace policy discoverable.

Ensure your repo ignores `.agents/traces/*.jsonl` in `.gitignore` and allowlists `.agents/traces/README.md`.

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

Example:

```text
.agents/traces/20260226T091530Z-fix-heading-levels-9f2c.jsonl
```
