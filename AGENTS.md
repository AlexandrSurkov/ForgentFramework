# AGENTS.md — ForgentFramework

> Machine-readable repository context. In VS Code Copilot agent mode, the orchestrator reads this file explicitly as its first action.

## Repository purpose

The canonical home of a technology-agnostic Multi-Agent Development Specification
(`framework/00-multi-agent-development-spec.md`), applied via VS Code Copilot agents.

## What lives here

| Path | Description |
|---|---|
| `framework/00-multi-agent-development-spec.md` | Canonical spec — source of truth for all agent behaviour rules (v0.21.9) |
| `framework/CHANGELOG.md` | Spec release notes shipped with the spec package |
| `PROJECT.md` | Project parameters: stack, models, rate limits, §pre answers |
| `AGENTS.md` | This file — pinned into orchestrator context on every run |
| `llms.txt` | LLM-friendly repo overview with links (for external context or new chats) |
| `.github/agents/*.agent.md` | System prompts: YAML frontmatter + Markdown body. VS Code Copilot agent definitions. |
| `.vscode/settings.json` | Registers agent file location for VS Code Copilot (`chat.agentFilesLocations`) |
| `.agents/traces/` | JSONL traces — one file per orchestrator run (`.agents/traces/<trace_id>.jsonl`); retention per `PROJECT.md` Trace mode |
| `.agents/session/` | **.gitignored** — session state (`.agents/session/<trace_id>/TASK_CONTEXT.md`) |
| `.github/copilot-instructions.md` | VS Code always-on Copilot context (~300 words) |
| `.github/AGENTS_CHANGELOG.md` | History of all agent prompt and pipeline behaviour changes |
| `.github/SPEC_VERSIONING.md` | Repo governance for versioning the spec (not part of the spec) |
| `.github/workflows/spec-versioning.yml` | CI guard: fails PRs that change `framework/` without bumping spec version + changelog |
| `.github/decisions/` | ADR records — checked by orchestrator before every decomposition |

## Agent roles

| Name | File | Mode | Role |
|---|---|---|---|
| `forgent-orchestrator` | `.github/agents/forgent-orchestrator.agent.md` | — | Decomposes tasks, routes executor + critic, issues TASK_COMPLETE / NEEDS_HUMAN. Reads AGENTS.md explicitly on every run. |
| `forgent-spec-editor` | `.github/agents/forgent-spec-editor.agent.md` | Executor | Edits spec, docs, agent prompts, README, llms.txt |
| `forgent-docs-critic` | `.github/agents/forgent-docs-critic.agent.md` | Critic / Audit executor | **Mode A** — critic for Markdown quality. **Mode B** — audit executor for read-only analysis tasks |
| `forgent-process-critic` | `.github/agents/forgent-process-critic.agent.md` | Critic | Consistency, enforceability, spec alignment, safety |
| `forgent-agent-architect` | `.github/agents/forgent-agent-architect.agent.md` | Advisor + Executor | AI agent systems architect: multi-agent patterns, agent file standards, AI security/governance. Reads `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` as primary reference. Can edit files. Call directly from Copilot Chat. |

## Responsibility zones

| Change type | Executor | Critic(s) |
|---|---|---|
| Spec / doc edits | `spec-editor` | `docs-critic` + `process-critic` |
| Agent prompt changes | `spec-editor` | `process-critic` (+ `docs-critic` if Markdown-heavy); update `AGENTS_CHANGELOG.md` |
| Analysis / audit (read-only) | `docs-critic` (Mode B) | `process-critic` |

## Orchestrator fast-track types

| Fast-track | When | Agents involved |
|---|---|---|
| `analysis/audit` | Read-only inspection, no file changes | `docs-critic` (Mode B) + `process-critic` |
| `docs-only` | Only `.md`/`.txt` changed | `spec-editor` + `docs-critic` |
| `spec/process-change` | Logic or rules in 00-multi-agent-development-spec.md changed | `spec-editor` + `process-critic` |
| `agent-prompt-change` | Any `.github/agents/*.agent.md` changed | `spec-editor` + `process-critic`; AGENTS_CHANGELOG required |

## Execution Workflow

### Overview

Every task follows a single canonical sequence:

```
User
 │
 ▼
Orchestrator  ──── classifies fast-track type
 │                 decomposes into subtasks (max 6)
 │
 └── for each subtask ──────────────────────────────────────────┐
      │                                                          │
      ▼  [agent call 1]                                         │
    Executor                                                     │
      │ receives: subtask + criteria + TASK_CONTEXT.md (iter>1) │
      │ produces: result (edited files / findings report)        │
      ▼                                                          │
    Orchestrator                                                 │
      │ collects result; does NOT evaluate it                    │
      ▼  [agent call 2]                                         │
    Critic                                                       │
      │ receives: original task verbatim + criteria +            │
      │           executor result ONLY (no history)              │
      │ returns: APPROVE / REQUEST_CHANGES / REJECT              │
      ▼                                                          │
    ┌─ APPROVE ────────────────────────────────────► next subtask┤
    │                                                            │
    ├─ REQUEST_CHANGES ─► Orchestrator writes findings to        │
    │                      TASK_CONTEXT.md § Previous Attempts   │
    │                      re-invoke Executor (max 3 iterations) ┘
    │
    └─ REJECT / 3 iterations without APPROVE ──► NEEDS_HUMAN
```

After all subtasks are approved → Orchestrator runs final verification → `TASK_COMPLETE`.

### Context contracts

What is passed to each agent role — these rules are absolute and must never be violated:

| Agent | Receives | Does NOT receive |
|---|---|---|
| **Executor (iter 1)** | Subtask description, acceptance criteria | Previous attempts, conversation history |
| **Executor (iter 2+)** | Subtask description, acceptance criteria, path to `TASK_CONTEXT.md` with `## Previous Attempts` | Full conversation history, critic reasoning |
| **Critic** | Original task text verbatim, acceptance criteria, executor's final output or precise summary of changed files | Conversation history, executor reasoning, previous iteration details |

> **Critic isolation rule**: the orchestrator MUST NOT forward any reasoning, chain-of-thought, or
> conversation history to the critic. Only: task + criteria + result.

### Iteration rules

| State | Action |
|---|---|
| Critic returns `APPROVE` | Move to next subtask |
| Critic returns `REQUEST_CHANGES` | Write each BLOCKER/WARNING to `TASK_CONTEXT.md` → re-invoke executor |
| Critic returns `REJECT` | Treat as `REQUEST_CHANGES` for iteration 1–2; escalate to `NEEDS_HUMAN` on iteration 3 |
| 3 iterations without `APPROVE` | Escalate: output `NEEDS_HUMAN` with disagreement summary |

Format for `TASK_CONTEXT.md` entries (used by Reflexion loop):
```
- [BLOCKER|WARNING] <location>: <issue> → <recommendation>
```

Executor MUST read `## Previous Attempts` in `TASK_CONTEXT.md` before starting each iteration.

### Routing: executor + critic by fast-track type

| Fast-track | Executor | Critic |
|---|---|---|
| `analysis/audit` | `docs-critic` (Mode B — read-only, produces findings) | `process-critic` |
| `docs-only` | `spec-editor` | `docs-critic` |
| `spec/process-change` | `spec-editor` | `process-critic` |
| `agent-prompt-change` | `spec-editor` | `process-critic` (+ `docs-critic` if Markdown-heavy); AGENTS_CHANGELOG.md must be updated |

---

## Active constraints

- **Max 3 iterations** per subtask → `NEEDS_HUMAN` if unresolved.
- **Reflexion**: executors MUST read `## Previous Attempts` in `TASK_CONTEXT.md` before each iteration.
- **Critic isolation**: critics receive only original task + criteria + result. No chain-of-thought forwarding.
- **ACKNOWLEDGED**: executor may write `ACKNOWLEDGED: WARNING | <category> | <location> | <reason>` to defer a WARNING; critic must honour it on next review.
- **AGENTS.md explicit read**: orchestrator MUST read this file as its first action on every VS Code Copilot run.
- **ADR check**: before any durable architectural decision, check `.github/decisions/`.
- **No secrets** in any committed file.
- **All committed artifacts in English.**
- **Parallel sessions**: short-term session state is per run at `.agents/session/<trace_id>/TASK_CONTEXT.md` (gitignored).
- **trace_id format**: recommended `YYYYMMDDTHHMMSSZ-<task-slug>-<rand4>` to avoid collisions.
- **Traces**: written to `.agents/traces/<trace_id>.jsonl`; operations: `plan` / `execute` / `critique` / `escalate` / `complete`.

## Active ADRs

No active ADRs.

## Universal Skills

All agents SHOULD consult this skill when creating or reviewing any standard repo file:

| Skill | File | Load when |
|---|---|---|
| `agent-file-standards` | [.agents/skills/agent-file-standards/SKILL.md](.agents/skills/agent-file-standards/SKILL.md) | Creating/editing `.agent.md`, `AGENTS.md`, `SKILL.md`, ADR, trace file, `mcp.json`, `llms.txt`, `.prompt.md` |
| `markdown-writer` | [.agents/skills/markdown-writer/SKILL.md](.agents/skills/markdown-writer/SKILL.md) | Creating/editing/reviewing any Markdown (`*.md`) documentation: README, ADRs, AGENTS.md, llms.txt, SKILL.md |

Domain-specific skills (loaded only by `forgent-agent-architect` on relevant tasks):

| Skill | File | Load when |
|---|---|---|
| `copilot-vscode` | [.agents/skills/copilot-vscode/SKILL.md](.agents/skills/copilot-vscode/SKILL.md) | VS Code Copilot features: `.agent.md` fields, tool names, agent types, subagents, handoffs, MCP config |
| `agent-patterns` | [.agents/skills/agent-patterns/SKILL.md](.agents/skills/agent-patterns/SKILL.md) | Designing executor/critic/orchestrator; calibrating rubrics; Reflexion/critic-isolation questions |
| `ai-security` | [.agents/skills/ai-security/SKILL.md](.agents/skills/ai-security/SKILL.md) | Security review, tool access policy, trust boundary design, compliance |

## Config and credentials

No credentials required — models are served through VS Code Copilot.
