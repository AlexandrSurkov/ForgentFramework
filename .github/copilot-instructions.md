# ForgentFramework — AI Instructions

## Project Overview

ForgentFramework is the canonical home of `framework/00-multi-agent-development-spec.md` (a technology-agnostic
multi-agent development specification), applied via VS Code Copilot agents.

See: [AGENTS.md](../AGENTS.md) for full repo map and agent roles.

## Agent Workflow

All multi-step tasks go through the orchestrator (select `forgent-orchestrator` in Copilot Chat agent mode).

Fast-tracks:
- **analysis/audit** → `docs-critic` (executor, Mode B) + `process-critic` (critic)
- **docs-only** (non-normative Markdown/text edits) → `spec-editor` + `docs-critic`
- **tooling-only** (repo tooling / CI scripts / workflows; no `framework/**`) → `spec-editor` + `process-critic`
- **spec/process-change** (normative change under `framework/**`) → `spec-editor` + `process-critic` (+ `docs-critic` if Markdown-heavy)
- **agent-prompt-change** (`.github/agents/*.agent.md`) → `spec-editor` + `process-critic` (+ `docs-critic` if Markdown-heavy); record in `.github/AGENTS_CHANGELOG.md`

Pipeline writes session state to `.agents/session/<trace_id>/TASK_CONTEXT.md` (gitignored; supports multiple parallel sessions).
Traces are written to `.agents/traces/<trace_id>.jsonl` (see `framework/spec/04-observability.md`).

## Key Constraints

- **No secrets in committed files.**
- **TASK_CONTEXT.md** is gitignored (`.agents/session/`). Never commit it.
- **Traces**: `.agents/traces/**` is gitignored in this repo. Never commit traces.
- **Critic isolation**: critics receive only original task + criteria + executor result.
  Do not forward full chat history to critics.
- **Reflexion**: executors MUST read `## Previous Attempts` in `TASK_CONTEXT.md` before each iteration.
- **.github/AGENTS_CHANGELOG.md** must be updated after every change to `.github/agents/*.agent.md`.
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
