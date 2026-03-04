# 3.1 Mandatory rules for the Orchestrator

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

**Rule 0 — Pass the task without paraphrasing**
> Orchestrator must pass the executor the original task text (from the user or `.feature`), not a retelling.
> Paraphrasing distorts acceptance criteria and creates drift between spec and implementation.

**Rule 1 — Check ADRs before decomposition**
> Before creating `TASK_CONTEXT.md`, orchestrator reads `.github/decisions/` and checks for conflicts.
> If there is a conflict — NEEDS_HUMAN before any work starts.

**Rule 2 — Choose the fast-track before starting the pipeline**
> Orchestrator chooses a single `fast_track` value from the canonical enum in [01-architecture.md](../01-architecture.md#fast-track-enum) and records it explicitly in `TASK_CONTEXT.md`.
> `.feature` classification rule: if the change set would otherwise be `docs-only` but includes one or more `.feature` files, `fast_track` MUST be `docs+feature` (never `docs-only`); otherwise keep `feature` / `lightweight-feature` as applicable.
> The full 9-phase pipeline runs only for `fast_track: feature` (see [01-architecture.md](../01-architecture.md#fast-track-enum)).

**Rule 2.1 — User-visible plan and progress (Group 1 orchestrators)**
> Scope: this rule applies to **Group 1** orchestrators as defined in [07-framework-operations.md](../07-framework-operations.md#71-two-tier-operations-model-normative).
>
> Group 1 orchestrators MUST always produce the following **in the user-facing chat** for the task:
>
> 1. **Before starting execution** (before invoking the first subagent), publish a plan that lists **all** tasks/subtasks.
>    - **Plan output format (normative):** the plan MUST be printed as a stable Markdown numbered list using `1.` / `2.` / `3.` with real line breaks (one list item per line).
>    - The orchestrator MUST NOT output literal `\\n` (or `\n`) sequences as text in the plan (or any other user-visible list/progress formatting).
>      - Exception: literal `\\n` (or `\n`) is allowed only inside fenced code blocks when quoting raw text verbatim (debugging/fidelity).
>    - Each task/subtask entry MUST include: (a) the goal, and (b) which subagent(s) will handle it.
> 2. **Before each subagent invocation** (executor or critic), announce:
>    - The called subagent name,
>    - Which task/subtask the subagent is being called for,
>    - Minimal relevant context (inputs, constraints, success criteria), and
>    - The subagent’s assigned job.
> 3. **After each subagent completes** (executor or critic), publish a concise result summary.
>    - If the subagent is an executor: summary MUST include the key outcome and which files changed (or “no files changed”).
>    - If the subagent is a critic: summary MUST include the verdict and the top finding(s) that drive next actions.
>
> Enforceability constraint: the plan published in chat MUST be consistent with the decomposition recorded in `TASK_CONTEXT.md` (names and intended owners). If the plan changes, the orchestrator MUST update both and explicitly note the change in chat.

**Rule 3 — Create the trace first**
> Trace creation and the root span requirements are defined in [04-observability.md](../04-observability.md) §4.6.
> Orchestrator MUST comply with those requirements.

**Rule 3.1 — Trace writing (least-privilege)**
> Trace-writing protocol, `trace_event` handling, and synthetic spans are defined in [04-observability.md](../04-observability.md) §4.5–§4.6.
> Orchestrator MUST comply with those requirements.

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

Canonical meanings for `Status` values: [01-architecture.md](../01-architecture.md#subtask-status-enum).

Do not bump iteration counters and do not create an ADR (unless an architectural decision is involved).
WONT_FIX for a BLOCKER subtask related to security or ADR requires explicit user confirmation in `TASK_CONTEXT.md`.

**Rule 6 — Close the task with a complete trace**
> Before closing the task, orchestrator MUST ensure the trace is structurally complete per [04-observability.md](../04-observability.md) §4.6.
