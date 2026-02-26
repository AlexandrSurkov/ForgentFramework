# ForgentFramework — AI Instructions

## Project Overview

ForgentFramework is the canonical home of `framework/00-multi-agent-development-spec.md` (a technology-agnostic
multi-agent development specification), applied via VS Code Copilot agents.

See: [AGENTS.md](../AGENTS.md) for full repo map and agent roles.

## Agent Workflow

All multi-step tasks go through the orchestrator (select `forgent-orchestrator` in Copilot Chat agent mode).

Fast-tracks:
- **analysis/audit** → `docs-critic` (executor, Mode B) + `process-critic` (reviewer)
- **spec/doc changes** → `spec-editor` + `docs-critic` + `process-critic`
- **agent prompt changes** → `spec-editor` + `process-critic`; record in `AGENTS_CHANGELOG.md`

Pipeline writes session state to `.agents/session/<trace_id>/TASK_CONTEXT.md` (gitignored; supports multiple parallel sessions).
Traces are written to `.agents/traces/<trace_id>.jsonl` (see `framework/spec/04-observability.md`).

## Key Constraints

- **No secrets in committed files.**
- **TASK_CONTEXT.md** is gitignored (`.agents/session/`). Never commit it.
- **Traces**: retention is defined by `PROJECT.md` → Trace mode. If committed, commit sanitized traces only.
- **Critic isolation**: critics receive only original task + criteria + executor result.
  Do not forward full chat history to critics.
- **Reflexion**: executors MUST read `## Previous Attempts` in `TASK_CONTEXT.md` before each iteration.
- **AGENTS_CHANGELOG.md** must be updated after every change to `.github/agents/*.agent.md`.
- **Spec maintenance (this repo):** any change under `framework/**` must follow `.github/SPEC_VERSIONING.md` and must update `framework/CHANGELOG.md`.

## Active Decisions

- None.

## Universal Skill

When creating or editing any standard repo file (`.agent.md`, `AGENTS.md`, `SKILL.md`, ADR, trace, `mcp.json`, `llms.txt`), load:
`.agents/skills/agent-file-standards/SKILL.md`

When creating, editing, or reviewing Markdown documentation (`*.md`), also load:
`.agents/skills/markdown-writer/SKILL.md`

## Current Focus

- Orchestrator Executor→Critic loop correctness: TASK_CONTEXT Reflexion, critic isolation
- Evals/golden tests are optional; see `framework/templates/repo-files-templates/root/.agents/evals/`
