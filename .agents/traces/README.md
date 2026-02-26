# .agents/traces/

JSONL traces for multi-agent runs.

Canonical standard: the Multi-Agent Development Specification modules:

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

Example:

```text
.agents/traces/20260226T091530Z-fix-heading-levels-9f2c.jsonl
```

## Record schema

Each line is one JSON object (append-only). Required top-level fields:

```jsonc
{
	"ts": "<ISO8601>",
	"trace_id": "YYYYMMDDTHHMMSSZ-task-slug-rand4",
	"span_id": "s<N>",
	"parent_span_id": "s<N>" | null,
	"agent": "<agent-name>",
	"operation": "plan" | "execute" | "critique" | "escalate" | "complete"
}
```

Additional fields depend on `operation` (see spec §4.5–§4.6):

- `plan`: `task`
- `execute`: `iteration`, optionally `subtask`, `input_tokens`, `output_tokens`, `duration_ms`
- `critique`: `iteration`, `verdict`, optionally `blockers`, `warnings`, `duration_ms`
- `escalate`: `reason`
- `complete`: optionally `total_iterations`, `duration_ms`
