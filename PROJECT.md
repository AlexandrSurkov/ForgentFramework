# PROJECT.md — ForgentFramework

> Spec: Multi-Agent Development Specification v0.21.23

## §pre: Project parameters

```
Project:
   Name and description:        ForgentFramework — canonical home of 00-multi-agent-development-spec.md,
                                 applied via VS Code Copilot agents.
   Artifact language:           English
   User communication language: English
   Components (repositories):   single repo
   Codebase baseline:           greenfield


Tech stack:
   Languages and frameworks:    none (pure Markdown + VS Code Copilot agents)
   Database / ORM:              none
   IaC tool:                    none
   CI/CD platform:              GitHub Actions (governance guard only — no build/test/deploy pipelines)
   Version control:             GitHub (personal)

AI and models:
   Available AI providers:      GitHub Copilot (VS Code)
   Budget constraints:          none — served through VS Code Copilot subscription
   Required agent roles:        orchestrator, spec-editor, docs-critic, process-critic

Testing:
   Existing tests:              none (evals/golden tests are optional; not configured in this repo)
   Test framework:              n/a (no runtime code)
   Coverage thresholds:         n/a

Performance and reliability:
   Target SLA:                  n/a (interactive tool, not a service)

Security and secrets:
   Secrets store:               none (no code; no credentials needed — models served via VS Code Copilot)
   SBOM / SLSA requirements:    none

Observability:
   OTEL backend:                none (JSONL traces only — .agents/traces/)
   Trace mode:                  Mode 1 (committed sanitized traces)

Team:
   Agent interaction model:     single person
   Existing ADR:                none (.github/decisions/ — to be populated)
   Existing .feature specs:     none
```

## 1. Stack

No runtime code. All tooling is VS Code Copilot agents.

| Component | Technology |
|---|---|
| LLM provider | GitHub Copilot (VS Code) |
| Model | configured in VS Code Copilot |
| Agent runtime | VS Code Copilot Chat (agent mode) |

## 2. Agent models

| Agent | Model | Tier | Note |
|---|---|---|---|
| `forgent-orchestrator` | configured in VS Code Copilot | — | |
| `forgent-spec-editor` | configured in VS Code Copilot | — | |
| `forgent-docs-critic` | configured in VS Code Copilot | — | |
| `forgent-process-critic` | configured in VS Code Copilot | — | |

### 2.3 Model policy override

```
Providers in use:  GitHub Copilot (VS Code)
Model selection:   configured in VS Code Copilot settings
```

## 3. Responsibility zones

| Change type | Executor | Critic(s) |
|---|---|---|
| Docs-only edits (non-normative) | `spec-editor` | `docs-critic` |
| Tooling-only (repo tooling / CI scripts / workflows; no `framework/**`) | `spec-editor` | `process-critic` |
| Framework normative changes (`framework/**`) | `spec-editor` | `process-critic` (+ `docs-critic` if Markdown-heavy) |
| Agent prompt changes (`.github/agents/*.agent.md`) | `spec-editor` | `process-critic` (+ `docs-critic` if Markdown-heavy) |
| Analysis / audit (read-only) | `docs-critic` (Mode B) | `process-critic` |

## 4. Known constraints

- `.agents/session/` is gitignored — `TASK_CONTEXT.md` lives under `.agents/session/<trace_id>/`, never committed.
- Trace mode: Mode 1 — `.agents/traces/` is committed (sanitized traces only).
- No app CI/CD — changes are applied manually via VS Code Copilot agents. A governance CI guard exists: `.github/workflows/spec-versioning.yml`.
