# 3.0 Constitutional principles for agents (Constitutional AI, Anthropic, 2022)

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

Every agent follows these principles regardless of the task:

1. **Do not violate ADRs** — a decision that contradicts an ADR requires a new ADR or NEEDS_HUMAN.
2. **Do not edit files outside your area** — e.g., backend-dev must not touch IaC; devops must not touch business logic.
3. **Do not propose breaking changes without explicit justification** — public API changes require a concrete rationale (at minimum: why + which consumers are affected).
4. **Do not hard-code secrets and configuration** — not “for tests”, not “temporarily”.
5. **Do not bypass tests** — do not delete tests, do not add Skip()/ignore without justification, do not comment out assertions.
6. **Do not add dependencies without justification** — a new import requires an explicit rationale in the commit or PR.
7. **Language policy: default English; override in PROJECT.md**

   | Artifact | Language |
   |---|---|
   | Code, code comments | Artifact language (PROJECT.md §pre; default: English) |
   | `README`, `AGENTS.md`, `llms.txt`, `SKILL.md` | Artifact language (PROJECT.md §pre; default: English) |
   | API Reference, OpenAPI descriptions | Artifact language (PROJECT.md §pre; default: English) |
   | `.feature` (Gherkin) scenarios | Artifact language (PROJECT.md §pre; default: English) |
   | `ADR`, `CHANGELOG` | Artifact language (PROJECT.md §pre; default: English) |
   | Commit messages | Artifact language (PROJECT.md §pre; default: English) |
   | Agent messages to the user (chat, NEEDS_HUMAN, questions) | User communication language (PROJECT.md §pre; default: English) |
   | `TASK_CONTEXT.md` (internal session file) | User communication language (PROJECT.md §pre; default: English) |

   > **Rationale:** English is the lowest-friction default for tooling (grep, IDE, CI) and cross-team collaboration.
   > PROJECT.md allows teams to override the user-facing language (and, if needed, artifact language) explicitly.
   >
   > **Critic check:** artifacts must follow PROJECT.md §pre "Artifact language" (default: English). If artifacts contain mixed languages without explicit override — BLOCKER.

8. **Work in small batches** (DORA AI Capabilities, 2025)

   During decomposition, orchestrator must ensure:
   - Each subtask is ≤ ~1 day of work (≈1–3 hours of LLM time)
   - Each subtask produces a self-contained atomic commit (one PR per feature branch)
   - Large tasks are decomposed vertically (end-to-end slices), not horizontally (“all tests” → “all code”)
   - If the task cannot be split — NEEDS_HUMAN with justification

   > **Rationale:** DORA 2025 reports the strongest AI impact for teams that practice small batches.
   > Smaller tasks speed up Reflexion loops, reduce accumulated debt in `TASK_CONTEXT.md`, and lower the risk of context loss.
