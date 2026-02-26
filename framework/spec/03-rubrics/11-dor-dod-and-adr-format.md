# 3.11 Definition of Ready / Definition of Done

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

**Definition of Ready (DoR)** — what a task must contain before starting an executor:

```text
- [ ] Task is specific (not “improve”, but “endpoint < 50ms”)
- [ ] Impacted files/modules are listed
- [ ] No ADR conflicts
- [ ] Acceptance criteria are defined
- [ ] Dependencies between subtasks are explicit
```

**Definition of Done (DoD)** — what must be true at APPROVE:

```text
For code (backend):
- [ ] Tests are written and passing
- [ ] Formatting applied
- [ ] API spec updated if API changed
- [ ] No new BLOCKER or WARNING

For code (frontend):
- [ ] Lint clean
- [ ] Build succeeds
- [ ] No new BLOCKER or WARNING
- [ ] Manual test plan created/updated if a critical user flow was added/changed (§1.4)

For IaC:
- [ ] validate passes
- [ ] No secrets outside secret storage
- [ ] fmt applied
- [ ] CHANGELOG.md updated if a release commit exists (Added/Changed/Fixed/Security)
- [ ] No new BLOCKER or WARNING

For documentation (documentation-writer):
- [ ] README created/updated per §0.7 (Root or Component, depending on scope)
- [ ] API Reference matches real schema (OpenAPI / GraphQL schema)
- [ ] `.feature` updated if observable behavior changed
- [ ] Manual test plan created/updated for all impacted user flows (§1.4)
- [ ] CHANGELOG.md updated if a release commit exists
- [ ] AGENTS.md updated if conventions or repo structure changed
- [ ] No new BLOCKER or WARNING

For any change:
- [ ] Commit follows Conventional Commits
- [ ] Pre-commit hooks passed: fmt, lint, validate (before commit)
- [ ] TASK_CONTEXT.md updated with APPROVED status
- [ ] CHANGELOG.md updated if a release commit exists
- [ ] Trace entry `operation: "complete"` added to .agents/traces/<trace_id>.jsonl

PR merge gates (Gate 1–3; see §0.6):
- [ ] CI: all tests green; build succeeds
- [ ] Critic agent performed review and left comments
- [ ] All BLOCKER threads are RESOLVED
- [ ] All other threads are RESOLVED | ACKNOWLEDGED | DEFERRED (SUGGESTION only)
- [ ] At least 1 human reviewer → APPROVE
```

## 3.11.1 When to create an ADR

```text
ADR is mandatory when:
- Choosing a technology/library with long-term architecture impact
- Any decision that contradicts or changes an existing ADR (must mark SUPERSEDES)
- Breaking change in public API or DB schema
- ESCALATED option A: executor position is accepted against critic — exception must be documented
- New dependency on an external service with a documented resilience strategy (timeout/retry/fallback)

ADR is optional but recommended when:
- Non-trivial pattern choice (why this approach?)
- Conscious deviation from a convention for a specific trade-off

Author: architect or orchestrator.
Format: §3.12.
```

## 3.12 ADR file format

Path: `.github/decisions/ADR-NNN-title.md`

```markdown
# ADR-NNN: Decision title

**Date:** YYYY-MM-DD
**Status:** PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED
**Author:** [agent or human]

## Context
[What happened, what problem exists, why a decision is needed]

## Considered alternatives
| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| Option A | ... | ... | ... |
| Option B | ... | ... | Selected |

## Decision
[What exactly was decided — bullet points]

## Consequences
[What changes in the project: files, processes, constraints]

## What NOT to do
[Explicit prohibitions implied by the decision]
```
