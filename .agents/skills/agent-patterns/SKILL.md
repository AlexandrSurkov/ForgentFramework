---
name: agent-patterns
description: "Action-oriented checklists for multi-agent pipeline design: Reflexion, critic isolation, Constitutional AI rubrics, Plan-and-Execute decomposition, Context Engineering. Load when designing or reviewing executor/critic/orchestrator roles, pipeline iteration rules, or critique rubrics."
---

# SKILL: Agent Patterns

> Load this skill when the task concerns executor/critic/orchestrator design, pipeline iteration rules,
> BLOCKER/WARNING/SUGGESTION rubric calibration, or any question about Reflexion, LLM-as-Judge,
> Constitutional AI, or Context Engineering.

## When to Load This Skill

- Designing or modifying an executor or critic agent prompt
- Reviewing orchestrator decomposition or routing rules
- Calibrating a critique rubric (BLOCKER / WARNING / SUGGESTION thresholds)
- Any question about critic isolation, context contracts, or iteration limits
- Implementing or debugging the Reflexion loop (`## Previous Attempts`)

---

## Patterns Quick Reference (A1.2)

| Pattern | When to Apply |
|---|---|
| **ReAct** | All executors: Reason → Act → Observe before answering |
| **Plan-and-Execute** | Orchestrator decomposing a multi-step task |
| **Reflexion** | Executor reading past failures on iteration 2+ |
| **Self-Refine** | Format for every critic finding (location + root cause + fix) |
| **LLM-as-Judge** | Justification for critic agent isolation design |
| **CRITIC** | Critic is allowed only read-only tools — no web calls, no writes |
| **AutoGen** | Termination rule: `max_iterations: 5` → `NEEDS_HUMAN` |
| **Self-Consistency** | High-stakes verdict → run critic twice; escalate on disagreement |
| **Constitutional AI** | BLOCKER/WARNING/SUGGESTION severity definitions |

---

## Reflexion (Shinn et al., 2023 — A1.2)

**Executor prompt checklist (iteration 2+):**
- [ ] Instruction to read `## Previous Attempts` in `TASK_CONTEXT.md` **before** touching files
- [ ] Instruction to explicitly acknowledge each BLOCKER/WARNING before acting
- [ ] `TASK_CONTEXT.md` path passed as argument — NOT the content inlined into the prompt

**Orchestrator checklist:**
- [ ] Append critic findings verbatim to `## Previous Attempts` (no paraphrase — A1.6)
- [ ] Pass file path, not inline findings
- [ ] Counter: if iteration == 5 and no APPROVE → escalate `NEEDS_HUMAN`

**Red flags:**
- Executor repeats the same mistake on iter 2 → `## Previous Attempts` missing or skipped
- Orchestrator summarises critic findings for the executor → violates no-paraphrase rule
- `TASK_CONTEXT.md` is gitignored (session file) but orchestrator tries to commit it → see `AGENTS.md`

---

## Critic Isolation / LLM-as-Judge (Zheng et al., 2023 — A1.2; A1.6)

**Critic must receive ONLY:**
- Original user task text — verbatim, not paraphrased
- Acceptance criteria
- Executor's final output or precise summary of changed files

**Critic must NOT receive:**
- [ ] Executor's reasoning or chain-of-thought
- [ ] Conversation history or orchestrator commentary
- [ ] Previous iteration context
- [ ] Orchestrator's interpretation or summary of the task

**Why:** executor reasoning causes anchoring bias → critic evaluates the reasoning path, not the result.

**Red flag:** critic returns APPROVE on a clearly incomplete result → likely received executor
reasoning, not just output.

---

## Constitutional AI / Rubric Design (Anthropic, 2022 — A1.2, A1.4)

**Severity definitions:**

| Severity | Meaning | Pipeline action |
|---|---|---|
| **BLOCKER** | Must be fixed before APPROVE. Spec contradiction, broken logic, security violation, missing required section. | `REQUEST_CHANGES` |
| **WARNING** | Should be fixed; can be deferred with `ACKNOWLEDGED`. Likely confusion for adopters, weak rules, missing example. | `REQUEST_CHANGES` or `APPROVE` if acknowledged |
| **SUGGESTION** | Optional. Style, clarity, minor improvement. | Does not block APPROVE |

**Rubric calibration checklist:**
- [ ] Is the rule testable by a critic with read-only tools?
- [ ] Is the BLOCKER threshold proportional to the cost of the mistake?
- [ ] Does the rubric have at least one golden test per BLOCKER category?
- [ ] After changing a rubric: run golden tests before merging (A1.5, eval-before-merge)

**ACKNOWLEDGED pattern** (executor defers a WARNING):
```
ACKNOWLEDGED: WARNING | <category> | <file/section> | <issue> | Deferred: <reason>
```
Critic must honour this on next review — do not re-raise as REQUEST_CHANGES.

---

## Plan-and-Execute Decomposition (Wang et al., 2023 — A1.2)

**Checklist:**
- [ ] Max 6 subtasks per task
- [ ] Each subtask: deliverable, verification method, executor + critic assigned
- [ ] Subtasks ordered by dependency (dependent subtask waits for APPROVE on prerequisite)
- [ ] Fast-track applied where eligible (`analysis/audit`, `docs-only`, `agent-prompt-change`)

**Anti-patterns:**
- Single subtask "do everything" → executor scope creep, critic unfocused verdict
- Subtasks not ordered → executor B edits file that executor A hasn't finished yet
- No verification method → orchestrator can't determine APPROVE criteria

---

## Context Engineering (A1.6 derived principle)

**Rule: no more context than needed.**

| Context type | Include | Omit |
|---|---|---|
| `AGENTS.md` | Every orchestrator run | — |
| `TASK_CONTEXT.md` | Executor on iter 2+ | Iter 1 |
| `SKILL.md` | Task matches skill trigger | All other tasks |
| Full file contents | Only if editing that file | Browsing |
| Conversation history | — | Always — especially never to critic |

**Violation signals:**
- Prompt >~3000 tokens before the actual task → trim
- Executor pastes full file "for context" → scope creep
- Critic receives executor chain-of-thought → isolation violation

---

## Self-Refine Finding Format (Madaan et al., 2023 — A1.2)

Every critic finding must have all three:
1. **Location** — file path or section name
2. **Root cause** — why this is a problem
3. **Actionable fix** — exactly what to change

❌ Bad: `WARNING: unclear prose in §3.2`
✅ Good: `WARNING §3.2 "Iteration rules": "iterate as needed" has no termination condition → specify max_iterations: 5 per AutoGen pattern`

---

## References

- [framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md — A1.2, A1.6](../../../framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md)
- [AGENTS.md — Execution Workflow](../../../AGENTS.md)
- [framework/00-multi-agent-development-spec.md — §3 Critique rubrics](../../../framework/00-multi-agent-development-spec.md)
