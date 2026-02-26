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
| `.github/decisions/` | ADRs (architecture decisions) |
| `.agents/skills/` | Agent Skills (`SKILL.md`) |
| `.agents/evals/` | Agent/prompt evaluation assets |
| `.agents/traces/` | Traces (JSONL; sanitize before committing) |
| `.agents/session/` | Ephemeral scratch/session files (gitignored) |
| `framework/00-multi-agent-development-spec.md` | Universal multi-agent spec (normative) |
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
