# AGENTS.md — Repository Context (Template)

> Purpose: a **machine-readable** map of this repository for AI agents and humans.

## Repository purpose

TODO: One sentence describing what this repo builds.

## How to run

- Build: `TODO`
- Test: `TODO`
- Lint/Format: `TODO`
- Dev server: `TODO`

## What lives here

| Path | Description |
|---|---|
| `.github/agents/` | Custom Copilot agents (`.agent.md`) |
| `.github/prompts/` | Reusable prompt files (`.prompt.md`) |
| `.github/instructions/` | Scoped instructions (`*.instructions.md`) |
| `.github/decisions/` | ADRs (optional; create this folder only if you use ADRs) |
| `.agents/skills/` | Agent Skills (`SKILL.md`) |
| `.agents/evals/` | Agent/prompt evaluation assets |
| `.agents/traces/` | Traces (local-only; gitignored; not committed) |
| `.agents/session/` | Runtime scratch/session files (created at runtime; gitignored; not committed) |
| `framework/00-multi-agent-development-spec.md` | Universal multi-agent spec (**template ships a stub**; copy `framework/spec/**` too if you need module links referenced from the spec) |
| `PROJECT.md` | Project parameters: stack, models, CI, critic triggers |
| `domain/` | Domain knowledge: glossary, contexts, events, specs |

## Conventions

- Languages/frameworks: `TODO`
- Directory conventions: `TODO`
- Branch/PR policy: `TODO`
- Security invariants: `TODO`

## Agent operating model

- Orchestrator/planner: `TODO`
- Implementer/executor: `TODO`
- Reviewer/critic: `TODO`

Two-tier operations model (recommended):
- Group 1 agents do project feature work.
- Group 2 bootstrap agents handle framework Install/Upgrade/Remove.
- Routing rule: any task whose primary goal is Install/Upgrade/Remove must be routed to Group 2 (see `framework/spec/07-framework-operations.md`).
