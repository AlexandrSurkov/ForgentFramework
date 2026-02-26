# 3.2 Mandatory rules for all Executors

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

**Rule 0 — Reflexion: read the past before each iteration (Shinn et al., 2023)**
> Before starting each iteration, executor must read `## Previous Attempts` in `TASK_CONTEXT.md`.
> If the section is absent — it is the first iteration.
> If present — executor explicitly acknowledges the prior critique and states what will be changed to address it.

**Rule 1 — ReAct: explicit reasoning before action (Yao et al., 2022)**
> Before each tool call, executor explains why it is needed.
> After the call, executor records the observation and decides the next step.

**Rule 2 — Responsibility boundary**
> Executor must not edit files outside their role (see principle 2).
> If changes are needed in another area, executor requests orchestrator action rather than editing directly.

**Rule 3 — Trace writing**
> After completing each iteration (execute or critique), append one JSONL line to `.agents/traces/<trace_id>.jsonl`.
