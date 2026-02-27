# 4. Observability AI Workflow

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

Goal: see what agents do, how much each iteration costs, and where the workflow gets stuck.

## 4.1 Standard: OpenTelemetry GenAI Semantic Conventions (CNCF, v1.40.0, 2025)

Each LLM invocation is a span with attributes:

```text
gen_ai.system                 = "openai" | "anthropic" | "google"
gen_ai.request.model          = "gpt-4o" | "claude-sonnet-4-6"
gen_ai.operation.name         = "chat"
gen_ai.usage.input_tokens     = 1234
gen_ai.usage.output_tokens    = 456
gen_ai.response.finish_reason = "stop" | "length" | "tool_calls"
```

Current extensions (v1.40.0):

| Extension | URL | What it adds |
|---|---|---|
| **Agent Spans** | `semconv/gen-ai/gen-ai-agent-spans/` | Attributes for orchestrator frameworks: `gen_ai.agent.name`, `gen_ai.agent.id`, nested agent→tool spans |
| **MCP Semantic Conventions** | `semconv/gen-ai/mcp/` | Attributes for MCP calls: tool, server, result |
| **GenAI Events** | `semconv/gen-ai/gen-ai-events/` | Events (not spans): prompt, completion, tool_call |

To enable the latest attributes, set:
`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`

Nested calls form a tree:

```text
[orchestrator]         ← root span of the task
   ├── [backend-dev]    iteration 1
   │     └── tool: runTerminal
   ├── [backend-critic] iteration 1 → REQUEST_CHANGES
   └── [backend-dev]    iteration 2 → APPROVE
```

## 4.2 AI Workflow metrics

| Metric | Formula | Signal |
|---|---|---|
| **iteration_count** | iterations per subtask | Always 3 → critic is too strict |
| **needs_human_rate** | NEEDS_HUMAN / total subtasks | > 20% → rubric/tasks issue |
| **approve_on_first** | APPROVE at iter=1 / total | < 30% → executor too weak or tasks too hard |
| **token_cost_per_task** | sum(input+output tokens) | Cost estimate by task type |
| **tool_failure_rate** | failed / total tool calls | Which tools are unstable |
| **severity_distribution** | % of BLOCKER/WARNING/SUGGESTION | Rubric calibration |

## 4.3 DORA metrics (DevOps process)

| Metric | Elite performance |
|---|---|
| **Lead Time for Changes** | < 1 hour |
| **Deployment Frequency** | multiple times per day |
| **MTTR** | < 1 hour |
| **Change Failure Rate** | < 5% |

Source: [dora.dev](https://dora.dev) (Google).

## 4.4 DORA AI Capabilities Model (2025)

[DORA State of DevOps 2025](https://dora.dev/research/) identifies 7 practices that amplify the impact of AI tools on team outcomes:

| Practice | Implementation in this spec |
|---|---|
| **Strong version control practices** | Feature branches, GitFlow, ADRs committed → §0.5 |
| **Working in small batches** | Orchestrator decomposes: ≤1 day per subtask; hotfix branches → §1.3 fast-tracks |
| **AI-accessible internal data** | AGENTS.md, llms.txt, SKILL.md, domain/ — machine-readable context → §0.1 |
| **User-centric focus** | `.feature` scenarios describe real user flows; Phase 0 fixes the spec → §1.3 |
| **Clear + communicated AI stance** | This spec is an explicit, documented AI stance |
| **Quality internal platform** | MCP servers, CI gates (Gate 1–3), observability pipeline → §0.6, §4 |
| **Healthy data ecosystems** | JSONL traces, AI metrics, golden evals — feedback loop → §4, §5 |

Projects with these practices show higher delivery speed, code quality, developer productivity, and product performance when using AI.

## 4.5 Trace log structure

```text
.agents/
├── session/     ← gitignored: per-session TASK_CONTEXT
│   └── <trace_id>/
│       ├── TASK_CONTEXT.md
│       └── TASK_CONTEXT_archive_<date>.md
└── traces/      ← JSONL session logs
   └── <trace_id>.jsonl
```

Single-record format examples:

```json
{"ts":"2026-02-23T14:32:00Z","trace_id":"abc123","span_id":"s01","parent_span_id":null,
 "agent":"orchestrator","operation":"plan","task":"add bulk endpoint",
 "input_tokens":412,"output_tokens":89,"duration_ms":3200}

{"ts":"2026-02-23T14:32:05Z","trace_id":"abc123","span_id":"s02","parent_span_id":"s01",
 "agent":"backend-dev","operation":"execute","iteration":1,
 "input_tokens":1840,"output_tokens":620,"duration_ms":18400}

{"ts":"2026-02-23T14:33:10Z","trace_id":"abc123","span_id":"s03","parent_span_id":"s01",
 "agent":"backend-critic","operation":"critique","iteration":1,
 "verdict":"REQUEST_CHANGES","blockers":1,"warnings":2,
 "input_tokens":980,"output_tokens":310,"duration_ms":9100}
```

**Span identity and ordering rules:**

- `span_id` MUST be **unique within a trace** (`trace_id`). Never reuse a `span_id` in the same trace.
- `span_id` is an **identifier**, not a timestamp. Do not infer time ordering from it.
- Orchestrator SHOULD allocate `span_id` values (e.g., a monotonic counter like `s01`, `s02`, …) to avoid collisions.
- For ordering, prefer `ts`; if multiple records share the same `ts`, preserve file append order as a stable tie-breaker.

## 4.6 Trace writing protocol (who writes what and when)

There is no automatic instrumentation.

To enforce least-privilege (critics are read-only), only the **orchestrator** writes to `.agents/traces/**`.

- Executors and critics MUST NOT write trace files.
- Executors and critics MUST return a small `trace_event` JSON object as part of their response.
- Orchestrator appends one JSONL record per step to `.agents/traces/<trace_id>.jsonl`, filling `ts`, `trace_id`, `span_id`, and `parent_span_id`.

### 4.6.1 Rules for agents

**Orchestrator** (when creating `TASK_CONTEXT.md`):
1. Assigns `trace_id` (collision-resistant; recommended format: `YYYYMMDDTHHMMSSZ-<task-slug>-<rand4>`, e.g., `20260223T143200Z-bulk-endpoint-9f2c`)
2. Creates `.agents/traces/<trace_id>.jsonl`
3. Writes the root span (`operation: "plan"`) and assigns its `span_id`

**Each executor and critic** (after completing its operation):
1. Returns a `trace_event` object in a `json` code block (no file writes)
2. Includes `agent`, `operation`, `subtask`, `iteration` (when applicable)
3. Critics additionally include `verdict`, `blockers`, `warnings`

Minimal example (executor):

```json
{"trace_event":{"agent":"backend-dev","operation":"execute","subtask":1,"iteration":1,"input_tokens":1840,"output_tokens":620,"duration_ms":18400}}
```

Minimal example (critic):

```json
{"trace_event":{"agent":"backend-critic","operation":"critique","subtask":1,"iteration":1,"verdict":"REQUEST_CHANGES","blockers":1,"warnings":2,"input_tokens":980,"output_tokens":310,"duration_ms":9100}}
```

### 4.6.2 When to write

| Event | Who writes | `operation` |
|---|---|---|
| Orchestrator created the task plan | orchestrator | `"plan"` |
| Executor completed an iteration | orchestrator (records `agent: <executor>`) | `"execute"` |
| Critic produced a verdict | orchestrator (records `agent: <critic>`) | `"critique"` |
| Orchestrator reached NEEDS_HUMAN | orchestrator | `"escalate"` |
| Orchestrator closed the task | orchestrator | `"complete"` |

### 4.6.3 Example: complete trace for one task

```json
{"ts":"2026-02-23T14:32:00Z","trace_id":"20260223T143200Z-bulk-endpoint-9f2c","span_id":"s01","parent_span_id":null,"agent":"orchestrator","operation":"plan","task":"add-bulk-endpoint","input_tokens":412,"output_tokens":89,"duration_ms":3200}
{"ts":"2026-02-23T14:32:05Z","trace_id":"20260223T143200Z-bulk-endpoint-9f2c","span_id":"s02","parent_span_id":"s01","agent":"backend-dev","operation":"execute","iteration":1,"input_tokens":1840,"output_tokens":620,"duration_ms":18400}
{"ts":"2026-02-23T14:33:10Z","trace_id":"20260223T143200Z-bulk-endpoint-9f2c","span_id":"s03","parent_span_id":"s01","agent":"backend-critic","operation":"critique","iteration":1,"verdict":"REQUEST_CHANGES","blockers":1,"warnings":2,"input_tokens":980,"output_tokens":310,"duration_ms":9100}
{"ts":"2026-02-23T14:33:15Z","trace_id":"20260223T143200Z-bulk-endpoint-9f2c","span_id":"s04","parent_span_id":"s01","agent":"backend-dev","operation":"execute","iteration":2,"input_tokens":2100,"output_tokens":540,"duration_ms":16200}
{"ts":"2026-02-23T14:34:05Z","trace_id":"20260223T143200Z-bulk-endpoint-9f2c","span_id":"s05","parent_span_id":"s01","agent":"backend-critic","operation":"critique","iteration":2,"verdict":"APPROVE","blockers":0,"warnings":1,"input_tokens":900,"output_tokens":180,"duration_ms":8400}
{"ts":"2026-02-23T14:34:10Z","trace_id":"20260223T143200Z-bulk-endpoint-9f2c","span_id":"s06","parent_span_id":"s01","agent":"orchestrator","operation":"complete","task":"add-bulk-endpoint","total_iterations":2,"input_tokens":6232,"output_tokens":1739,"duration_ms":127600}
```

### 4.6.4 Analysis with jq (no extra instrumentation)

```powershell
# How many iterations did each task take?
Get-Content .agents\traces\*.jsonl | jq -s '[.[] | select(.operation=="complete")] | .[] | {task, iters: .total_iterations}'

# Where did critics reject most often?
Get-Content .agents\traces\*.jsonl | jq 'select(.operation=="critique" and .verdict=="REQUEST_CHANGES") | .agent'

# Total tokens by agent
Get-Content .agents\traces\*.jsonl | jq -s 'group_by(.agent) | .[] | {agent: .[0].agent, tokens: (map(.input_tokens + .output_tokens) | add)}'

# Tasks where escalation to a human was required
Get-Content .agents\traces\*.jsonl | jq 'select(.operation=="escalate") | .task'
```

## 4.7 Visualization tools

Run on demand — no always-on server required.

| Tool | Run/install | When you need it |
|---|---|---|
| **jq** | `winget install jqlang.jq` (Windows) / `brew install jq` (macOS) | Always — fast JSONL queries |
| **Phoenix (Arize)** | `pip install arize-phoenix && python -m phoenix.server.main` | UI for 10+ sessions |
| **Jaeger all-in-one** | `docker run --rm -p 16686:16686 jaegertracing/all-in-one` | Visualize the span tree |
| **W&B Weave** | `pip install weave` | Tracing + response quality scoring |
| **promptfoo** | `npx promptfoo eval` | Prompt regressions between versions |

Recommended start: JSONL + jq only → add Phoenix after collecting 10+ traces.
