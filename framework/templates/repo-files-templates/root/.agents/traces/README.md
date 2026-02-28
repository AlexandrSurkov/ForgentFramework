# .agents/traces/ (Template)

This directory contains JSONL traces for multi-agent runs.

Canonical standard:

- `framework/spec/04-observability.md` (§4.5–§4.6)
- `framework/spec/02-sessions-and-memory.md` (§2.1)

## Policy

Trace JSONL files (`.agents/traces/*.jsonl`, e.g. `.agents/traces/<trace_id>.jsonl`) are **local-only** (gitignored) and MUST NOT be committed (no exceptions).

This file (`.agents/traces/README.md`) may be committed and is intentionally allowlisted.

Ensure your repo ignores `.agents/traces/*.jsonl` in `.gitignore` and allowlists `.agents/traces/README.md` so this policy stays committed.

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
