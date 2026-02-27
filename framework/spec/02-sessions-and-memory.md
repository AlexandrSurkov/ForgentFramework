# 2. Work Protocol: Sessions and Memory

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

## 2.1 `TASK_CONTEXT.md` structure

Orchestrator creates this file at the beginning of each session:

```markdown
# Task Context — [date] [task-slug]

**trace_id:** YYYYMMDDTHHMMSSZ-task-slug-rand4  
**trace_file:** .agents/traces/YYYYMMDDTHHMMSSZ-task-slug-rand4.jsonl  
**task_context_file:** .agents/session/YYYYMMDDTHHMMSSZ-task-slug-rand4/TASK_CONTEXT.md
**fast_track:** feature | lightweight-feature | hotfix | docs-only | docs+feature | infra | security-patch | agent-prompt-update
<!-- Canonical meanings: 01-architecture.md#fast-track-enum -->

## Task
[Full description from the user — ORIGINAL text, not a paraphrase]

## Decomposition
| # | Subtask | Role | Depends on | Iteration | Status |
|---|---|---|---|---|---|
| 1 | ... | backend-dev | — | 1/5 | IN_PROGRESS |
| 2 | ... | backend-dev | — | 0/5 | TODO |
| 3 | ... | frontend-dev | #2 | 0/5 | BLOCKED |

## Previous Attempts
<!-- Filled after each REQUEST_CHANGES (Reflexion pattern). -->

### Task #N — Iteration M
**Critique:**
- BLOCKER: path/to/file.go:45 — description

**What the executor will change in the next iteration:**
- ...

## Decisions made in this session
- [critic, iter 2]: description (APPROVED)

## Blockers / NEEDS_HUMAN
- none
```

`trace_id` must be **unique per session**. It is used as the key for both:
- the trace file: `.agents/traces/<trace_id>.jsonl`
- the session directory: `.agents/session/<trace_id>/TASK_CONTEXT.md`

Recommended `trace_id` format: `YYYYMMDDTHHMMSSZ-<task-slug>-<rand4>` (see §4.6.1).

Parallel agents and `TASK_CONTEXT.md`:
- When multiple executors run concurrently, each executor updates only its own row in `## Decomposition` and must not edit other agents’ rows.
- Shared sections (`## Blockers`, `## Decisions made in this session`) are updated only by the orchestrator.
- Race condition handling: if two agents finish at the same time, orchestrator applies both updates sequentially, keyed by subtask number.

---

## 2.2 Memory rules

1. **Short-term memory (session):** `.agents/session/<trace_id>/TASK_CONTEXT.md`
   - Created by the orchestrator; updated by all agents during the session
   - Must be added to `.gitignore`
   - Supports multiple parallel sessions in one working tree: each session uses its own `<trace_id>` directory

2. **Long-term memory (ADR):** `.github/decisions/`
   - Architectural decisions that must not be violated
   - Orchestrator and architect must check before making decisions
   - Committed to the repo and reviewed like code

3. **Repository context (persistent):** `AGENTS.md` in each repo
   - Automatically read by the agent on each task
   - Updated when conventions change

4. **Context Window Management**
   - If `TASK_CONTEXT.md` exceeds ~200 lines / ~4000 words, or orchestrator observes planning quality degradation, create a summarized version (replace detailed history of completed phases with a short recap).
   - The summary must contain: the current plan + the last 2 entries from `## Previous Attempts`.
   - Archive the full file as `.agents/session/<trace_id>/TASK_CONTEXT_archive_<date>.md` (gitignored). Long-term memory remains in ADRs and traces (retained according to `PROJECT.md` Trace mode).
   - Agents use `textSearch` (or `search`) to jump to the needed section.

Example summary version (replaces a verbose TASK_CONTEXT after ~200 lines):

```markdown
## Summary (archived: .agents/session/<trace_id>/TASK_CONTEXT_archive_2026-02-23.md)
Phases 0–2: COMPLETED. Key decisions: ADR-003 (bulk endpoint), ADR-004 (rate limiting).
Current position: Phase 3, Cycle 1 (Refactor)

## Decomposition (active only)
| # | Subtask | Role | Status |
|---|---|---|---|
| 5 | Refactor handlers/bulk.go | backend-dev | IN_PROGRESS |

## Previous Attempts (last 2)
...
```

---

## 2.3 Re-entry protocol after NEEDS_HUMAN

```markdown
## Human Input — [date]

### Decision on the blocker
[Decision text — a concrete instruction]

### Updated acceptance criteria (if needed)
- [new criterion]

### Permission for the next iteration
- [ ] Allow re-entry (one additional executor↔critic loop after NEEDS_HUMAN)
- [x] Rephrase the subtask and restart at iter=0
- [ ] Close the subtask as WONT_FIX
```

Orchestrator upon receiving Human Input:
1. Appends `## Human Input` to `TASK_CONTEXT.md`.
2. If “rephrase” was chosen, resets the subtask iteration counter to 0.
3. If “re-entry” was chosen, runs exactly one additional executor→critic loop for the same subtask.
4. Continues the workflow with the updated criteria.
