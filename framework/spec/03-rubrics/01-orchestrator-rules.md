# 3.1 Mandatory rules for the Orchestrator

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

**Rule 0 — Pass the task without paraphrasing**
> Orchestrator must pass the executor the original task text (from the user or `.feature`), not a retelling.
> Paraphrasing distorts acceptance criteria and creates drift between spec and implementation.

**Rule 1 — Check ADRs before decomposition**
> Before creating `TASK_CONTEXT.md`, orchestrator reads `.github/decisions/` and checks for conflicts.
> If there is a conflict — NEEDS_HUMAN before any work starts.

**Rule 2 — Choose the fast-track before starting the pipeline**
> Orchestrator determines the change type (feature / hotfix / docs-only / infra) and records it explicitly in `TASK_CONTEXT.md`.
> The full 9-phase pipeline runs only for feature branches (see §1.3 Fast-tracks).

**Rule 3 — Create the trace first**
> Create `.agents/traces/<trace_id>.jsonl` and write the root span (`operation: "plan"`) before assigning the first subtask.

**Rule 4 — Fill `## Previous Attempts` before returning**
> After each REQUEST_CHANGES, orchestrator must copy findings from the Critique Report into `## Previous Attempts` in `TASK_CONTEXT.md` for the next iteration.
> This is orchestrator responsibility, not executor or critic.
> Format: see the preamble in §1.3.3.
> Without this, the executor will not know why it is back and will repeat the same mistake (sycophancy / anchoring).

**Rule 5 — WONT_FIX: close a subtask before ESCALATED**
> If the user changed their mind, the requirement became obsolete, or is no longer relevant before ESCALATED, orchestrator may close the subtask as WONT_FIX without escalation:
> 1. Update the subtask status in `TASK_CONTEXT.md` → `WONT_FIX`
> 2. Record the reason in `## Decisions made in this session`
> 3. If the subtask blocked others — revise the decomposition plan
> 4. Continue the pipeline with remaining subtasks
>
> Do not bump iteration counters and do not create an ADR (unless an architectural decision is involved).
> WONT_FIX for a BLOCKER subtask related to security or ADR requires explicit user confirmation in `TASK_CONTEXT.md`.

**Rule 6 — Close the task with a complete trace**
> Before writing `operation: "complete"`, orchestrator verifies that `.agents/traces/<trace_id>.jsonl` contains entries from every agent that participated.
> If an agent’s entries are missing, orchestrator adds a synthetic span (`"synthetic": true`) and records a warning in `TASK_CONTEXT.md`.
> The task is not DoD-complete without the final trace entry `operation: "complete"`.
