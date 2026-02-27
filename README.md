# ForgentFramework

A lightweight, technology-agnostic **Multi‑Agent Development Specification** for running real software projects with an Orchestrator/Executor/Critic workflow.

This repository is intentionally minimal: it contains the canonical specification document and the VS Code Copilot agent definitions that apply it.

## What this is

- A universal, stack-independent spec that defines:
  - Agent roles and responsibilities (Orchestrator / Executors / Critics)
  - A phase-based delivery pipeline (spec-first → implementation → verification)
  - PR quality gates and critique rubrics (including security and documentation)
  - Session memory conventions (`TASK_CONTEXT.md`) and re-entry protocol (`NEEDS_HUMAN`)
  - Observability guidance (JSONL trace structure aligned with OTel GenAI concepts)
  - Upgrade procedures when the spec version changes

It is **not** an application or library. You don’t “run” it; you apply it to other repositories.

## Repository contents

- `framework/00-multi-agent-development-spec.md` — the canonical specification (version header inside the file).
- `AGENTS.md` / `llms.txt` — agent-readable repository context.
- `.github/agents/` — system prompts for each agent role (Markdown with YAML frontmatter), used as VS Code Copilot agent definitions.
- `.agents/session/` — gitignored per-session state (`.agents/session/<trace_id>/TASK_CONTEXT.md`).
- `.agents/traces/` — JSONL session traces (OTel GenAI format). Retention is defined by `PROJECT.md` → Trace mode.

## Apply to a project

1. Open `framework/00-multi-agent-development-spec.md` and follow **Framework operations** → Install.
2. Create a project-specific `PROJECT.md` next to the spec using the template referenced in the Infrastructure module.
3. Run the “Implementation Agent” system instruction from the Adoption Roadmap module to execute the phases.

After that, your target project should have the required agent files, rubrics, traces, and the working agreements needed for day-to-day use.

## Agents

Four agent roles are defined in `.github/agents/`:

| File | Role |
|---|---|
| `forgent-orchestrator.agent.md` | Decomposes tasks, assigns executor + critic, runs final verification |
| `forgent-spec-editor.agent.md` | Executor — edits `framework/00-multi-agent-development-spec.md` and other docs |
| `forgent-docs-critic.agent.md` | Critic — Markdown structure, links, clarity |
| `forgent-process-critic.agent.md` | Critic — consistency, enforceability, spec alignment |

System prompts are plain Markdown — used directly as VS Code Copilot agent system prompts.

## VS Code Copilot usage

1. Open this repo in VS Code.
2. In Copilot Chat, switch to Agent mode and select `forgent-orchestrator`.
3. Describe your task — the orchestrator decomposes it and delegates to executor + critic agents.

## Workflow (working on this framework)

1. Describe the goal and acceptance criteria (in the terminal or to Copilot).
2. The orchestrator assigns an executor (makes changes) and a critic (reviews).
3. If the critic returns `REQUEST_CHANGES`, the executor iterates (max 5 times). If still not `APPROVE`, escalates to `NEEDS_HUMAN`.
4. After all critics `APPROVE`, final verification runs.

**Session artifacts:**

- `TASK_CONTEXT.md` lives under `.agents/session/<trace_id>/TASK_CONTEXT.md` (gitignored).
- Traces are appended to `.agents/traces/<trace_id>.jsonl`.
- Recommended `trace_id` format: `YYYYMMDDTHHMMSSZ-<task-slug>-<rand4>` (collision-resistant for parallel sessions).

## Working on this repository

Most changes are spec edits, agent prompt edits, or pipeline code changes.

### What to change where

- **Canonical specification:** `framework/00-multi-agent-development-spec.md`
- **Agent system prompts:** `.github/agents/*.agent.md`
- **Repo conventions for humans/agents:** `README.md`, `AGENTS.md`, `llms.txt`
- **Architecture decisions (long-term memory):** `.github/decisions/ADR-*.md`
- **Agent prompt changelog:** `.github/AGENTS_CHANGELOG.md`

### Suggested change cycle

1. Create a feature branch.
2. Describe the task to the `forgent-orchestrator` agent in VS Code Copilot Chat.
3. Review the diff produced by the executor.
4. Open a PR. (This repository does not include a root PR template; the downstream template lives at `framework/templates/repo-files-templates/root/.github/pull_request_template.md`.)

## Upgrading

When `framework/00-multi-agent-development-spec.md` changes, follow **Framework operations** → Upgrade and run the Spec Upgrade Agent prompt from the Adoption Roadmap module. The expected baseline is recorded in the target project's `PROJECT.md` as the previously used spec version.


## Contributing

If you evolve the spec:

- Keep changes precise and audit-friendly (this is a process document).
- Update the spec version and “Updated” date in the header.
- Prefer small, reviewable commits (Conventional Commits are referenced by the spec).

## License

No license file is included in this repository snapshot. If you plan to share it publicly, add an explicit `LICENSE` file and align it with your intended usage.
