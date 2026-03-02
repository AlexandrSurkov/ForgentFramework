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
> Trace-writing protocol and `trace_event` required keys are defined in [04-observability.md](../04-observability.md) §4.5–§4.6.
> Executors MUST comply with those requirements.

Example (non-normative):

```json
{"trace_event":{"agent":"backend-dev","operation":"execute","subtask":1,"iteration":1,"input_tokens":1840,"output_tokens":620,"duration_ms":18400}}
```

**Rule 4 — AWESOME-COPILOT gate for agent/prompt changes (deterministic)**

Trigger:
- Any change to `.github/agents/**/*.agent.md` OR `.github/prompts/**/*.prompt.md`.

Requirements:
- Executor MUST create or update the gate report artifact at `.agents/compliance/awesome-copilot-gate.md` in the same change set.
- The report MUST include an explicit list of the changed agent/prompt artifacts so a critic can deterministically verify it.
- When the trigger fires, executor MUST consult `awesome-copilot` (unless unable) and record the consultation evidence in the report.
- The report MUST include all required sections/fields defined in `framework/spec/07-framework-operations.md` §7.3.3, including the consultation section.
- This gate is additive: it does not replace the per-artifact `## Provenance` requirements in Appendix A1.1.

Details and required fields are defined in: `framework/spec/07-framework-operations.md`.
