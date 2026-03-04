# 3.3 Mandatory rules for all Critics

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

**Rule 1 — Context isolation (anchoring bias prevention)**
> Critic sees only the final result.
> Critic must not rely on chain-of-thought, intermediate steps, or the author’s explanations.
> Critic knows only: original task + acceptance criteria + produced result.

**Rule 2 — Finding format (Self-Refine format)**

```text
1. What is wrong:     specific location (file:line)
2. Why:              root cause
3. How to fix:       actionable recommendation
```

> Findings without a specific location do not count.

**Rule 3 — Iteration limit (AutoGen / LangGraph)**

```text
max_iterations: 5

After the 5th iteration without APPROVE:
   → NEEDS_HUMAN: describe the disagreement in 2–3 sentences
   → stop and hand off to the user
```

Canonical terminology: verdicts and subtask statuses are defined in [01-architecture.md](../01-architecture.md#pipeline-vocabulary).

Healthy-critic signal:
- 1–2 BLOCKER findings for a medium task
- 0 findings → critic is too soft (sycophancy)
- 5+ BLOCKER findings → rubric is too strict/unclear; needs calibration

**Rule 4 — Critic tools (CRITIC paper)**

```text
All critics: read-only tools only (readFile, fileSearch, textSearch)
Exception: devops-critic is additionally allowed syntax validators
   (e.g., terraform validate, docker compose config --quiet)
Without tools, critics hallucinate syntax checks.
```

Canonical tool IDs: see ../04-observability.md#48-canonical-capability-to-tool-mapping-tool-ids.

**Rule 5 — Conflicts between multiple critics on one PR**

```text
If multiple critics review one PR and their verdicts disagree:
   - Any REJECT from any critic → PR must not be merged
   - Any open BLOCKER blocks merging (Gate 3)
   - APPROVE from one + REQUEST_CHANGES from another →
         executor addresses REQUEST_CHANGES; both must reach APPROVE
   - architect-critic REJECT for ADR violation overrides other APPROVE verdicts:
         requires a new ADR or NEEDS_HUMAN, not just a code patch
```

**Rule 6 — ESCALATED: repeated NEEDS_HUMAN on the same subtask**

ESCALATED status is set by orchestrator when:
- NEEDS_HUMAN occurs a second time on the same subtask (after re-entry).

Determinism rule:
- The first non-convergence within `max_iterations` (5) is always `NEEDS_HUMAN` (Rule 3).
- `ESCALATED` is only used if the orchestrator runs re-entry and the same subtask still ends in `NEEDS_HUMAN`.

What orchestrator records in `TASK_CONTEXT.md`:

```markdown
## Blockers / NEEDS_HUMAN
- ESCALATED: Subtask #N — <disagreement summary>
   Attempts: iter 1–5 + re-entry (1 loop) — APPROVE not reached
  Expected: product owner / tech lead decision
```

Difference between NEEDS_HUMAN and ESCALATED:
- NEEDS_HUMAN — quick developer clarification
- ESCALATED — exceeds team competence; requires owner / tech lead

What happens after ESCALATED:

1. Orchestrator stops the subtask.
   - Subtask status in `TASK_CONTEXT.md` → ESCALATED (not BLOCKED, not IN_PROGRESS).
   - Pipeline does not progress on this subtask.
   - Independent subtasks continue (parallel branches are not blocked).

2. Orchestrator notifies the user.

   Message format:
   ```text
   ESCALATED: Subtask #N "<name>"
   Disagreement: <2–3 sentences>
   Attempts: <N> iterations including re-entry after Human Input
   Executor position: <brief>
   Critic position: <brief>
   Decision needed: <a concrete question>
   ```

3. A human (tech lead / product owner) decides.
   - A. Accept executor’s position → write an ADR documenting the exception; critic accepts the documented decision; subtask continues with iter=1.
   - B. Accept critic’s position → rephrase the subtask with the critic requirement; executor gets updated task statement; iter=1.
   - C. Change the requirement (new ADR or `.feature` change) → update `.feature` or create an ADR; affected pipeline phases restart.
   - D. Close as WONT_FIX → close subtask and record reason in `TASK_CONTEXT.md`; pipeline continues without it; orchestrator revises the plan if it blocked other subtasks.

4. Orchestrator records the decision.

   ```markdown
   ## Human Input — [date]
   ### ESCALATED — Subtask #N
   Decision: <A|B|C|D> — <rationale>
   Orchestrator action: <what is restarted>
   ```

After recording, the pipeline resumes per the chosen option. If ESCALATED repeats for the same subtask, pause the task until an out-of-band architecture review.

**Rule 7 — Trace reporting (critic)**
> Trace-writing protocol and `trace_event` required keys are defined in [04-observability.md](../04-observability.md) §4.5–§4.6.
> Critics MUST comply with those requirements.

Example (non-normative; `operation: "critique"`):

```json
{"trace_event":{"agent":"backend-critic","operation":"critique","subtask":1,"iteration":1,"verdict":"REQUEST_CHANGES","blockers":1,"warnings":2,"input_tokens":980,"output_tokens":310,"duration_ms":9100}}
```

Full JSONL format (written by orchestrator): [04-observability.md](../04-observability.md) §4.5–§4.6.

**Rule 8 — AWESOME-COPILOT gate enforcement (deterministic BLOCKER)**

If the produced result includes any changes to `.github/agents/**/*.agent.md` or `.github/prompts/**/*.prompt.md`, the critic MUST return `REQUEST_CHANGES` with a `BLOCKER` finding when any of the following are true:

- The required gate report `.agents/compliance/awesome-copilot-gate.md` is missing.
- The report exists but does not list all changed agent/prompt artifacts (stale report).
- The report exists but is missing one or more required sections/fields defined in `framework/spec/07-framework-operations.md` §7.3.3.
- The report exists but the **Awesome-copilot consultation** evidence is invalid:
   - Consultation performed is neither `yes` nor `unable`, OR
   - Consultation performed is `yes` but any of: consulted material, immutable reference, or license verification is missing, OR
   - Consultation performed is `unable` but the explicit reason and concrete fallback are missing.
- The report uses the deprecated pattern `## External sources used` → `- none` (framework/spec/07-framework-operations.md §7.3.3).

Reference: `framework/spec/07-framework-operations.md` (gate trigger + required report fields).

---

Critic returns a structured response:

````markdown
## Critique Report

**VERDICT:** APPROVE | REQUEST_CHANGES | REJECT

> Canonical meanings: [01-architecture.md](../01-architecture.md#verdict-enum).
>
> **APPROVE** — no BLOCKER findings and no WARNING findings. SUGGESTION findings are allowed.
> **REQUEST_CHANGES** — there is any BLOCKER or WARNING: fixable in the next iteration.
> **REJECT** — fundamental constitutional violation (ADR violated without new ADR; work performed outside the agent’s responsibility boundary; executor reinterpreted the task without coordination). Not fixable via patch — requires orchestrator rephrasing.

**Example of correct ACKNOWLEDGED** (SUGGESTION-only; recorded in `## Previous Attempts` or PR thread):

```markdown
ACKNOWLEDGED: SUGGESTION | conventions | models/host.go:34 | Missing godoc | Not doing in this PR
```

> `ACKNOWLEDGED` is not a verdict override. A WARNING cannot be “accepted” via `ACKNOWLEDGED`/`DEFERRED`.

### Findings

| Severity | Category | Location | Issue | Recommendation |
|---|---|---|---|---|
| BLOCKER | security | handlers/host.go:45 | Input not validated | Add validation middleware |
| WARNING | performance | services/bulk.go:120 | N+1 query | Collect IDs; do one bulk query |
| SUGGESTION | conventions | models/host.go:33 | Missing godoc | Add a comment |
````
