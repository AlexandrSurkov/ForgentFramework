# 0. Agent infrastructure organization

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

> This section defines the **standard file structure** and **project conventions**
> that apply to any project using this specification.
> A project file may override or extend any element.

## 0.1 AgentConfig repository structure

For rationale and a Copilot-native “ideal” layout (including an in-repo variant), see:
[guide-copilot-native-multi-agent-repo-structure.md](guide-copilot-native-multi-agent-repo-structure.md).

> Relationship note: treat the guide as the **base shape** (“ideal structure”).
> This §0.1 section **inherits and extends** that structure with **normative requirements** (exact files, conventions, and defaults).
> If there is any conflict between the guide and §0.1, §0.1 wins.

> Naming note: some repos use `.ai/` for portability; this spec uses `.agents/` for runtime artifacts.
> Treat them as the same concepts; the name is a convention.

Each project creates a dedicated agent-configuration repository (`<project>-AgentConfig`):

```text
<project>-AgentConfig/
│
├── AGENTS.md                         ← global context for the whole project
├── llms.txt                          ← LLM-readable project overview
├── PROJECT.md                        ← project-specific details (stack, models, CI)
├── .gitignore                        ← ignores .agents/session/
├── framework/                         ← vendored spec framework (source of truth)
│   ├── 00-multi-agent-development-spec.md ← universal spec entrypoint
│   ├── spec/                           ← spec modules (normative)
│   │   ├── appendices/                 ← standards and references
│   │   └── ...
│   └── templates/                      ← optional: starter templates
│
├── .vscode/
│   ├── <project>.code-workspace      ← one workspace: all project repos
│   ├── settings.json                 ← editor + Copilot discovery settings
│   ├── mcp.json                      ← MCP servers for agents (optional if no MCP)
│   └── extensions.json               ← recommended extensions
│
├── .github/
│   ├── copilot-instructions.md       ← system instructions for all Copilot chats
│   ├── AGENTS_CHANGELOG.md           ← history of agent prompt changes
│   ├── pull_request_template.md      ← PR template (see §0.6)
│   ├── instructions/                 ← optional, folder-specific conventions
│   │   ├── backend.instructions.md
│   │   ├── frontend.instructions.md
│   │   └── docs.instructions.md
│   ├── agents/                       ← all `.agent.md` files
│   │   ├── <project>-orchestrator.agent.md
│   │   ├── <project>-architect.agent.md
│   │   ├── <project>-architect-critic.agent.md
│   │   ├── <project>-backend-dev.agent.md
│   │   ├── <project>-backend-critic.agent.md
│   │   ├── <project>-frontend-dev.agent.md
│   │   ├── <project>-frontend-critic.agent.md
│   │   ├── <project>-qa-engineer.agent.md
│   │   ├── <project>-qa-critic.agent.md
│   │   ├── <project>-devops-engineer.agent.md
│   │   ├── <project>-devops-critic.agent.md
│   │   ├── <project>-security.agent.md
│   │   ├── <project>-security-critic.agent.md
│   │   ├── <project>-documentation-writer.agent.md
│   │   └── <project>-documentation-critic.agent.md
│   ├── prompts/                      ← optional, reusable prompt files (slash commands)
│   │   └── *.prompt.md
│   ├── hooks/                        ← optional, deterministic enforcement
│   │   └── *.hook.jsonc
│   └── decisions/                    ← ADR (Architecture Decision Records)
│       ├── ADR-###-*.md
│       ├── ADR-002-*.md
│       └── ...
│
├── .agents/
│   ├── session/                      ← .gitignore'd: per-session state (.agents/session/<trace_id>/TASK_CONTEXT.md)
│   ├── traces/                       ← JSONL session logs (OTel GenAI format)
│   ├── evals/                        ← golden tests for prompts (JSONL)
│   └── skills/                       ← Agent Skills (SKILL.md format)
│       ├── <project>-backend/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── <project>-frontend/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── <project>-devops/
│       │   ├── SKILL.md
│       │   └── references/
│       └── <project>-<other>/
│           └── SKILL.md
│
└── domain/                           ← domain knowledge
    ├── glossary.md                 ← Ubiquitous Language
    ├── bounded-contexts.md         ← Context Map
    ├── domain-events.md            ← key events
    └── specs/                      ← BDD/Gherkin scenarios
       └── *.feature
```


**`.gitignore` for AgentConfig:**

Traces are always written locally to `.agents/traces/` (see rubrics §3 and observability §4).
Whether traces are committed is defined by `PROJECT.md` **Trace mode**.

**Mode 1 — committed traces (sanitized):**

```text
# Agent temporary sessions (do not commit)
.agents/session/

# Traces are committed in Mode 1. Commit sanitized traces only.
```

**Mode 2 — external / not committed:**

```text
# Agent temporary sessions (do not commit)
.agents/session/

# Traces are NOT committed in Mode 2.
.agents/traces/
```

> `CHANGELOG.md` does not live in AgentConfig. It lives in the root of each component repo (Backend, Frontend, Automation, Docs).
> Format: Keep a Changelog — sections `Added / Changed / Deprecated / Removed / Fixed / Security`.
> It is created and updated by an agent on every release commit (see DoD §3.11).
> Prompt changelog (`AGENTS_CHANGELOG.md`) is a separate file in AgentConfig under `.github/` (see §5.1).

### 0.1.1 `.agent.md` file format

Each agent is defined by a `.github/agents/<project>-<role>.agent.md` file.
The `model` field and full model names are defined in PROJECT.md §2; below is the structure template.

```markdown
---
name: <project>-<role>
description: >
   [One sentence: what this agent does and when to invoke it]
model: <model-name>          # see PROJECT.md §2 + tiers in 00-multi-agent-development-spec.md §1
tools:
   # --- all agents: navigation (read-only) ---
   - read_file
   - grep_search
   - semantic_search
   - list_dir
   - file_search
   # --- executor agents add: ---
   # - create_file
   # - create_directory
   # - replace_string_in_file
   # - run_in_terminal
   # --- orchestrator additionally: ---
   # - manage_todo_list    ← task decomposition + subtask status
   # --- critic agents: read-only; devops-critic adds: ---
   # - get_errors          ← syntax validation (terraform, docker)
   # - run_in_terminal     ← only validate/fmt, never apply
---

# System Prompt

## Role
[Role: executor or critic; responsibility zone; pipeline phases from 00-multi-agent-development-spec.md §1.3]

## Context
- Read AGENTS.md in all relevant repos before starting each task
- Check .github/decisions/ for ADR constraints before any architectural change
- [executor] Read ## Previous Attempts in TASK_CONTEXT.md before each iteration (Reflexion)
- [critic] Receive only: original task + criteria + result. Do NOT read chain-of-thought.

## Task Protocol
[Concrete algorithm: what to do first, how to build the result, output structure]

## Constitutional Constraints
- Follow all principles from 00-multi-agent-development-spec.md §3
- Do not write files outside your responsibility zone (Constitution principle 2)
- All code comments and artifacts in English (principle 7)

## Output Format
[What exactly to return: files, diff, Critique Report, TASK_CONTEXT.md updates]

## Trace Recording
After each iteration, append one JSONL line to `.agents/traces/<trace_id>.jsonl`.
`trace_id` comes from the TASK_CONTEXT.md header.

Executor (operation: "execute"):
   {"ts":"<ISO8601>","trace_id":"<id>","span_id":"s<N>","parent_span_id":"s01",
    "agent":"<name>","operation":"execute","subtask":<N>,"iteration":<N>,
    "input_tokens":<N>,"output_tokens":<N>,"duration_ms":<N>}

Critic (operation: "critique") — include verdict / blockers / warnings:
   {"ts":"<ISO8601>","trace_id":"<id>","span_id":"s<N>","parent_span_id":"s01",
    "agent":"<name>-critic","operation":"critique","subtask":<N>,"iteration":<N>,
    "verdict":"APPROVE|REQUEST_CHANGES|REJECT","blockers":<N>,"warnings":<N>,
    "input_tokens":<N>,"output_tokens":<N>,"duration_ms":<N>}

Full format — see 00-multi-agent-development-spec.md §4.5–4.6.
```

> `name`, `description`, `model`, `tools` are read by VS Code Copilot from the YAML frontmatter; the system prompt is the file body after `---`.

### 0.1.2 Minimal `.vscode/extensions.json`

Recommended VS Code extensions for an AI-agent workspace:

```json
{
   "recommendations": [
      "github.copilot",
      "github.copilot-chat",
      "ms-azuretools.vscode-docker",
      "hashicorp.terraform",
      "golang.go",
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "eamodio.gitlens",
      "redhat.vscode-yaml",
      "ms-vscode.vscode-json"
   ]
}
```

> This list depends on your tech stack — adjust to the languages and tools you actually use.
> During developer onboarding, an agent may recommend installing extensions from this list.

### 0.1.3 Filled `.agent.md` example — backend-critic

> A full working copy-paste example. Replace `<project>` with your project name; choose the model according to PROJECT.md §2.

````markdown
---
name: <project>-backend-critic
description: >
   Reviews backend code produced by backend-dev. Invoke after every backend-dev iteration
   to get a structured Critique Report (APPROVE / REQUEST_CHANGES / REJECT).
model: claude-sonnet-4.6
tools:
   - read_file
   - grep_search
   - semantic_search
   - list_dir
   - file_search
---

# System Prompt

## Role
Critic agent. Reviews the result of backend-dev executor using the Backend Critic rubric
from 00-multi-agent-development-spec.md §3.4 and project-specific triggers from PROJECT.md §4.
Does NOT write code. Does NOT read executor's chain-of-thought — only the final result.

## Context
- Read AGENTS.md in the backend repo before reviewing.
- Check .github/decisions/ for active ADR constraints.
- Receive from orchestrator: original task + acceptance criteria + result (files changed).

## Task Protocol
1. Read the changed files listed in the task.
2. For each file: apply Backend Critic checklist (§3.4 + PROJECT.md §4 triggers).
3. Check Constitutional principles §3.0: zone violations, hardcoded config, skipped tests.
4. Compose Critique Report (see Output Format below).
5. Append one JSONL line to .agents/traces/<trace_id>.jsonl (trace_id from TASK_CONTEXT.md).

## Constitutional Constraints
- Follow 00-multi-agent-development-spec.md §3.0 and §3.3 (all critic rules).
- Only read_file / grep_search — no write operations.
- Findings without file:line reference are not valid — do not include them.
- 0 findings is valid only if the implementation is genuinely correct;
   if you suspect sycophancy, re-read the rubric and check one more time.

## Output Format

### Critique Report

**VERDICT:** APPROVE | REQUEST_CHANGES | REJECT

| Severity | Category | Location | Issue | Recommendation |
|---|---|---|---|---|
| BLOCKER | security | handlers/host.go:45 | Input not validated | Add validation middleware |
| WARNING  | performance | services/bulk.go:120 | N+1 query | Batch IDs, one bulk query |
| SUGGESTION | conventions | models/host.go:33 | No godoc | Add comment |

### Trace Recording
After issuing the verdict, append to .agents/traces/<trace_id>.jsonl:
{"ts":"<ISO8601>","trace_id":"<id>","span_id":"s<N>","parent_span_id":"s01",
 "agent":"<project>-backend-critic","operation":"critique","subtask":<N>,"iteration":<N>,
 "verdict":"<APPROVE|REQUEST_CHANGES|REJECT>","blockers":<N>,"warnings":<N>,
 "input_tokens":<N>,"output_tokens":<N>,"duration_ms":<N>}
````

---

## 0.2 Multi-root workspace

All project repositories are combined into a single VS Code workspace via `.vscode/<project>.code-workspace`:

```json
{
   "folders": [
      { "path": ".",                       "name": "<project>-AgentConfig" },
      { "path": "../<project>-Backend",    "name": "<project>-Backend" },
      { "path": "../<project>-Frontend",   "name": "<project>-Frontend" },
      { "path": "../<project>-Automation", "name": "<project>-Automation" },
      { "path": "../<project>-Docs",       "name": "<project>-Documentation" }
   ],
   "settings": {
      "chat.agentFilesLocations": {
        ".github/agents": true
      }
   }
}
```

> AgentConfig is the entry point: the workspace is opened from here, and agents see all repos through a single unified context.

AGENTS.md distribution across repositories:

```text
<project>-AgentConfig/AGENTS.md    ← global: product, repo map, conventions
<project>-Backend/AGENTS.md        ← backend language/framework: build, tests, structure
<project>-Frontend/AGENTS.md       ← UI framework: build, tests, structure
<project>-Automation/AGENTS.md     ← IaC / CI/CD: environments, clouds, conventions
<project>-Docs/AGENTS.md           ← documentation standards
```

---

## 0.3 AGENTS.md in every repository

### 0.3.1 Required contents of the global AGENTS.md

```markdown
## Product Overview
[3–5 sentences: what the product does, for whom, key entities]

## Repository Map
| Repo | Contents |
|---|---|
| <project>-AgentConfig | Agent files, skills, domain, ADR |
| <project>-Backend     | Server-side code |
| <project>-Frontend    | Client-side code |
| <project>-Automation  | IaC, CI/CD, deploy scripts |
| <project>-Docs        | User and API documentation |

## Commit Conventions (Conventional Commits)
- feat(<scope>): — MINOR version bump
- fix(<scope>):  — PATCH version bump
- chore:         — dependencies/config (no version bump)
- refactor:      — no behavior change (no bump)
- docs:          — documentation only
- BREAKING CHANGE (footer) — MAJOR version bump

## Branching Strategy: GitFlow
[See 00-multi-agent-development-spec.md §0.5 for detailed rules]
- main: production-ready, tagged vX.Y.Z
- develop: integration branch
- feature/<task-id>-<description>: from develop → develop
- release/X.Y.Z: from develop → main + develop
- hotfix/<description>: from main → main + develop

## PR Policy
Every merge via Pull Request. See .github/pull_request_template.md.
Squash merge. Feature branch deleted after merge.

## ADR Index
[Links to .github/decisions/ADR-*.md]
```

### 0.3.2 Required contents of a component repository AGENTS.md

```markdown
## Build & Run
[Commands: build, test, lint, format — with exact script names]

## Structure
[Key directories: where business logic lives, where tests live, what is generated and must not be edited manually]

## Conventions
[Naming, error handling, configuration, forbidden patterns]
```

> For the Frontend repo, additionally: `docs/test-plans/` — manual test plans (§1.4).
> The directory is committed; it is created by `frontend-dev` on the first user flow.

---

## 0.4 llms.txt format

Each component repository contains `llms.txt` — a short LLM-friendly overview (llmstxt.org):

```markdown
# <project>-<Component>

> One-sentence description of this component.

Language/framework: X. Key constraints: Y.

## Key Files
- [entry-point](path/to/entry): what it does
- [config/](config/): configuration directory
- [swagger-api/](swagger-api/): API source of truth (if applicable)

## Documentation
- [README.md](README.md): overview
- [AGENTS.md](AGENTS.md): AI agent instructions
```

---

## 0.5 GitFlow + SemVer — detailed rules

### 0.5.1 Branches

| Branch | Purpose | Branches off | Merges into |
|---|---|---|---|
| `main` | Production-ready, tagged `vX.Y.Z` | `release/*` | — |
| `develop` | Integration branch, base for features | `main` (init) | `release/*` |
| `feature/<task-id>-<description>` | New feature work | `develop` | `develop` |
| `release/X.Y.Z` | Release preparation, bugfix-only | `develop` | `main` + `develop` |
| `hotfix/<description>` | Urgent production fix | `main` | `main` + `develop` |

> Agents work **only** in `feature/*` branches. They do not push directly to `develop` or `main`.

### 0.5.2 SemVer + automated versioning

```text
Commit type      → Version bump
feat:            → MINOR bump  (X.Y+1.0)
fix:             → PATCH bump  (X.Y.Z+1)
chore/docs/refactor → no bump
BREAKING CHANGE  → MAJOR bump  (X+1.0.0)

Tool: gitversion (gitversion.yml in the root of each component repo).
CI pipeline reads the version via gitversion and tags the image/artifact.
```

> When creating a commit, an executor agent must choose the correct Conventional Commit type — it drives the release version.
> If a change breaks a public API, the `BREAKING CHANGE` footer is mandatory (Constitution principle 3).

### 0.5.3 Feature branch naming

```text
feature/<task-id>-<short-kebab-description>

Examples:
   feature/PROJ-123-add-bulk-endpoint
   feature/PROJ-456-fix-auth-token-refresh
   feature/PROJ-789-update-helm-values
```

---

## 0.6 Pull request policy

**Required template `.github/pull_request_template.md`:**

```markdown
## Summary
<!-- What changed and why (1–3 sentences) -->

## Related Work
<!-- Task/issue ID: PROJ-NNN -->
<!-- Related ADR: ADR-NNN (if applicable) -->

## Type of Change
- [ ] feat: new feature (MINOR bump)
- [ ] fix: bug fix (PATCH bump)
- [ ] chore/refactor/docs: no version change
- [ ] BREAKING CHANGE: incompatible change (MAJOR bump)

## Checklist
- [ ] Tests pass locally
- [ ] Linter / formatter clean
- [ ] No secrets or hardcoded config in code
- [ ] AGENTS.md updated if conventions changed
- [ ] CHANGELOG.md updated (if release commit)
- [ ] ADR created or referenced if architectural decision made
```

### 0.6.1 Merge gates (PR gates)

Any merge into `main` / `release` requires passing three sequential gates.

### 0.6.1.1 Gate 1 — CI: all tests are green

Every PR runs a full test suite automatically. Merging is blocked until all checks pass.

```text
Required CI run:
   - Static analysis (linter, vet/typecheck)
   - Unit tests (coverage must not drop below project threshold)
   - Integration tests (real dependencies — DB, cache)
   - Contract tests (if public API changed)
   - Build: artifact must build with no errors and no warnings

No exceptions:
   - Temporarily disabling a test requires BLOCKER justification in the PR description
   - A flaky test does not count as passing — fix it first or skip + link an issue (Constitution principle 5)

Exact commands and pipeline files are defined in the project file.
```

### 0.6.1.2 Gate 2 — Review by a Critic agent

The appropriate critic agent must review the PR and leave structured comments as PR threads.

```text
Critic assignment by change type:
   Backend changes (business logic, API)        → backend-critic
   Frontend changes (components, pages)        → frontend-critic
   IaC / CI/CD / Dockerfile changes            → devops-critic
   Test scripts (smoke, E2E, load)             → qa-critic
   Documentation changes                       → documentation-critic
   New service / cross-service contract / ADR  → architect-critic (in addition)

PR touches multiple areas → run all relevant critics in parallel.

Format for each critic comment in the PR:
   **[BLOCKER|WARNING|SUGGESTION]** `file:line`
   Issue: what is wrong and why (root cause)
   Recommendation: a concrete fix

Critic does NOT press "Approve" — it leaves thread comments.
Final APPROVE is done by the orchestrator after all threads are resolved.

How the critic is invoked (webhook, manual Copilot Chat, CI job) is defined in PROJECT.md §3.x.
Without a working mechanism, Gate 2 does not function.
```

**Configuration examples (PROJECT.md §3.x):**

**Option A — Manual via Copilot Chat** *(recommended to start — requires no additional setup)*

PR is open → developer opens Copilot Chat and writes:

```text
@backend-critic perform a Code Review of this PR
```

**Option B — GitHub Actions job**

```yaml
# .github/workflows/critic-review.yml
on:
   pull_request:
      types: [opened, synchronize]
jobs:
   critic:
      runs-on: ubuntu-latest
      steps:
         - uses: actions/checkout@v4
         - name: Run critic review
            run: gh copilot suggest --agent backend-critic "Review this PR"
```

**Option C — MCP webhook (if SCM MCP is configured)**

PR opened event → MCP server → automatically runs the `.agent.md` critic.

### 0.6.1.3 Gate 3 — Discussion: executor responds to every comment

The executor who created the PR must reply to every open critic thread.
Silence is not a response — an unresolved thread blocks merging.

**Option A — Executor disagrees with critic:**

```text
Executor replies in the thread:
   DISPUTE: <argument>
   - Link to a standard / ADR / test that proves the point
   - If needed — a quote from the spec or documentation

Critic replies:
   - Withdraws the finding → closes the thread with ACKNOWLEDGED
   - Insists              → strengthens the argument (iteration +1)

If a BLOCKER/WARNING is not resolved within 2 iterations → orchestrator escalates: NEEDS_HUMAN
SUGGESTION may be rejected by the executor without escalation (ACKNOWLEDGED is sufficient).
```

**Option B — Executor agrees:**

```text
Executor fixes the code, then replies:
   FIXED: <what changed> — commit <sha>
   Reason: <why this fix addresses the root cause>

Critic closes the thread:
   RESOLVED
```

**Thread states:**

| Status | Meaning | Blocks merge |
|---|---|---|
| `RESOLVED` | Fix applied, critic agrees | No |
| `ACKNOWLEDGED` | Executor proved the point, critic withdrew | No |
| `DEFERRED` | Tech debt; issue created — **SUGGESTION-only** | No |
| `ESCALATED` | Disagreement on BLOCKER/WARNING → NEEDS_HUMAN | Yes |
| *(open)* | No response or discussion in progress | Yes |

> `DEFERRED` is allowed **only for SUGGESTION**.
> A thread that contains an **active** BLOCKER finding must be `RESOLVED`.
> If the critic withdraws the finding (i.e., it is no longer a BLOCKER), `ACKNOWLEDGED` is valid.

**Final merge condition:**

```text
Gate 1:  CI → all tests green, build successful
Gate 2:  Critic agent left a review (at least one thread, or explicit "No findings")
Gate 3:  All threads are RESOLVED | ACKNOWLEDGED | DEFERRED(SUGGESTION-only)
             All threads with active BLOCKER findings are RESOLVED only
             ≥ 1 human reviewer → APPROVE
             → orchestrator issues the final APPROVE to merge
```

**Gate summary table:**

| Gate | What is checked | Who checks | Blocks merge |
|---|---|---|---|
| CI | All tests green; build succeeds | CI system | Yes |
| Critic review | Structured review present | critic agent | Yes |
| Thread resolution | All threads closed | executor + critic | Yes |
| BLOCKER resolved | All BLOCKER → RESOLVED | executor + critic | Yes |
| Human review | ≥ 1 human APPROVE | human | Yes |

> The critic agent already ran the checklist (BLOCKER/WARNING/SUGGESTION). Human checks what the agent cannot evaluate:
> - Business logic matches stakeholder intent (not only the spec)
> - Changes don’t produce unintended side effects for adjacent systems
> - UX/DX is acceptable: the intended outcome is truly delivered
> - Product/strategy appropriateness
>
> Human does NOT re-run OWASP/STRIDE/ADR checklists — agents already did.

---

### 0.6.2 Branch protection setup

Gates (§0.6.1) work only if direct pushes to protected branches are technically blocked.
Without branch protection, Gates 1–3 can be bypassed by merging without a PR.

**Required platform-level settings for `main` and `develop` (GitHub / Azure DevOps / GitLab):**

| Rule | Setting | Applies to |
|---|---|---|
| PR-only | Require pull request reviews | `main`, `develop` |
| CI required | Require status checks (Gate 1 jobs) | `main`, `develop`, `release/*` |
| Min 1 reviewer | Require 1 approved human review | `main` |
| No direct pushes | Restrict direct pushes (everyone except CI bot) | `main`, `develop` |
| Linear history | Squash merge or rebase | `main` |
| Auto-delete branches | Auto-delete head branch after merge | `feature/*`, `hotfix/*` |

> Agents work in `feature/*` — restrictions on `main`/`develop` do not block their workflow.
> Setting names depend on the platform:
> GitHub: Settings → Branches → Branch protection rules;
> Azure DevOps: Project Settings → Repositories → Policies → Branch Policies.
> PROJECT.md §3 must declare which CI status checks are required (Gate 1 jobs + critic jobs if automated).

---

## 0.7 README in code

> Based on: [Standard Readme](https://github.com/RichardLitt/standard-readme) (RichardLitt, 2016), [Make a README](https://www.makeareadme.com).
> A README in code is a set of technical signposts for developers and agents working with a particular repository or module.
> It differs from public documentation (Diataxis Tutorial/How-to/Reference): the goal is not to teach end users,
> but to explain the structure and intent to someone opening the repo for the first time.

### 0.7.1 Three types of in-code README

| Type | Location | Audience | Goal |
|---|---|---|---|
| Root README | Repo root | New developer / agent / contributor | Quick start: where, what, how to run |
| Component README | Each package/service in a monorepo | Developer working with the module | Purpose, public interface, scope constraints |
| AGENTS.md | Next to Root/Component README | AI agent | Machine-readable context: commands, conventions |

> AGENTS.md and README are different documents: README is for humans; AGENTS.md is for agents.
> Avoid duplication: AGENTS.md should link to README for narrative context.

### 0.7.2 Root README — required sections

Matches the Standard Readme spec:

```markdown
# <Name>

> <One sentence: what it does, for whom>

## Background
[Why it exists; what problem it solves — 3–5 sentences]

## Requirements
[Prerequisites: runtime versions, system dependencies]

## Install
[Exact install/build commands with expected output]

## Usage
[Minimal working example: command + expected output]

## API
[Brief overview of the public interface. Full reference lives in documentation.]

## Contributing
[Link to AGENTS.md and/or CONTRIBUTING.md]

## License
[SPDX license identifier]
```

### 0.7.3 Component / Module README — required sections

````markdown
# <Module name>

> <One sentence: what this module does>

## Purpose
[Why it exists in the system; what breaks without it]

## Dependencies
[What it depends on and WHY — not a list of imports, but justification for each dependency]

## Public Interface
[Key exported types/functions/endpoints — brief list]

## Usage Example
```go
// Minimal compilable / runnable example
```

## Out of Scope
[What this module intentionally does NOT do — explicit responsibility boundaries]

## Related
[ADR: ADR-NNN. Specs: domain/specs/*.feature]
````

### 0.7.4 README-first principle

Component README is written **before** implementing the module (SDD, Phase 0).
Describing `Public Interface` and `Out of Scope` before code helps surface scope and dependency ambiguities
before spending iterations on a wrong implementation.

**Phase 0 owners:** `architect` initiates Component README as part of the specification (`Public Interface` and `Out of Scope`),
`documentation-writer` formats it using the template. Without Component README, the transition to Phase 1 is blocked
(Documentation Critic §3).

---

## 0.8 PROJECT.md — project file template

> The project file applies this universal specification to a specific stack, platform, and team.
> It is created in `<project>-AgentConfig/` next to 00-multi-agent-development-spec.md.
> This spec contains principles; PROJECT.md contains concrete project facts: stack, agent models, environments, CI commands.

### 0.8.1 Required sections of PROJECT.md

````markdown
# PROJECT.md — <Project name>

> Version: X.Y.Z · Stack: [Go / TS / ...] · Platform: [K8s / Azure / ...] · Spec: Multi-Agent Development Specification vX.Y.Z

## 1. Stack and environments

### Languages and frameworks
| Component | Language | Framework / Runtime |
|---|---|---|
| Backend  | Go X.Y | go-swagger / Chi / ... |
| Frontend | TypeScript | Next.js X / React X / ... |
| IaC      | Terraform X | Azure RM / Helm X / ... |

### Environments
| Name | Purpose | URL / cluster | Branch |
|---|---|---|---|
| dev     | Development / smoke | ... | develop |
| staging | E2E / load tests    | ... | release/* |
| prod    | Production          | ... | main |

## 2. Project agents

### 2.1 Customize the agent set

<!-- The baseline agent set is defined in 00-multi-agent-development-spec.md §1.
       Record deviations here: added/removed/renamed roles.
       All changes must also be logged in AGENTS_CHANGELOG.md. -->

| Action | Agent | Rationale |
|---|---|---|
| added  | `data-engineer` | Project uses ETL pipelines |
| removed | `qa-engineer` | No separate QA; role covered by backend-dev |
| renamed | `infra-engineer` (← `devops-engineer`) | Team domain terminology |

<!-- If there are no changes, keep a single row “none” or remove the section. -->

### 2.2 Agent models

<!-- Fill during setup. Tiers T1/T2/T3 are defined in 00-multi-agent-development-spec.md §1.
       List only the agents actually used in this project after customization (§2.1). -->

| Agent | Model | Tier | Rationale |
|---|---|---|---|
| orchestrator         | ... | T? | ... |
| architect            | ... | T? | ... |
| architect-critic     | ... | T? | ≥ tier of architect |
| backend-dev          | ... | T? | ... |
| backend-critic       | ... | T? | ≥ tier of backend-dev |
| frontend-dev         | ... | T? | ... |
| frontend-critic      | ... | T? | ≥ tier of frontend-dev |
| qa-engineer          | ... | T? | ... |
| qa-critic            | ... | T? | ≥ tier of qa-engineer |
| devops-engineer      | ... | T? | ... |
| devops-critic        | ... | T? | ≥ tier of devops-engineer |
| security             | ... | T? | ... |
| security-critic      | ... | T? | ≥ tier of security |
| documentation-writer | ... | T? | ... |
| documentation-critic | ... | T? | ≥ tier of documentation-writer |

### 2.3 Override the model selection policy

<!-- Universal model selection rules are in 00-multi-agent-development-spec.md §1.2.
       Record only deviations here: budget constraints, provider policy, missing models.
      Orchestrator reads this section and applies it with higher priority than 00-multi-agent-development-spec.md §1.2.
       If empty, §1.2 applies as-is. -->

```text
Providers in use: ...          (e.g., Anthropic + OpenAI / Anthropic only)
Max tier: T?                  (e.g., T2 — T1 models unavailable / budget)
Forbidden models: ...         (e.g., Claude Opus 4.6 — 30x, do not use)
Prefer 0x models: yes|no      (yes — prefer GPT-4.1/GPT-4o/GPT-5 mini/Raptor mini when quality is equal)
```

**Custom assignments (if different from §2.2):**

| Rule | Model | Rationale |
|---|---|---|
| Orchestration instead of T1 | ... | ... |
| Fallback on T1 rate limit | ... | ... |
| Planning tasks without T1 | ... | ... |
| Documentation without T3 | ... | ... |

> If there are no custom rules — delete the table above. Everything else is governed by the lines above + 00-multi-agent-development-spec.md §1.2.

---

## 3. CI/CD

### Pipeline files
| File | Platform | Purpose |
|---|---|---|
| ... | GitHub Actions / Azure Pipelines / GitLab CI | ... |

### Gate 2: how the critic is invoked on PRs
<!-- Describe: webhook / manual Copilot Chat / CI job.
       Without a configured mechanism, Gate 2 does not work — see §0.6. -->

### Coverage thresholds
| Type | Threshold | Blocks CI |
|---|---|---|
| Unit test coverage | ≥ ?% | Yes |
| Mutation score     | ≥ 70% | Yes (< 50% = BLOCKER) |
| Static analysis    | 0 errors | Yes |

**Mutation tool:** `...` — run command: `...`
*(go-mutesting / pitest / mutmut / stryker / fast-check — fill per project)*

## 4. Technology-specific rubric triggers (add-on to 00-multi-agent-development-spec.md §3)

> Concrete triggers for this project’s stack. Do not duplicate universal rules from the spec.

### Backend Critic — additional triggers
```text
BLOCKER:
- [ ] ...
WARNING:
- [ ] ...
```

### Frontend Critic — additional triggers
```text
BLOCKER:
- [ ] ...
WARNING:
- [ ] ...
```

### DevOps Critic — additional triggers
```text
BLOCKER:
- [ ] ...
WARNING:
- [ ] ...
```

## 5. MCP servers

> Concrete servers configured in `.vscode/mcp.json`. Example structure — 00-multi-agent-development-spec.md §6.4.

| Server | Tools | Purpose |
|---|---|---|
| SCM (GitHub / Azure DevOps) | create_pr, get_issues | PRs and issues from an agent |
| Docker | docker_build, docker_run | Containers |
| IaC (Terraform / Helm) | tf_plan, tf_apply | IaC without switching context |

## 6. Project roadmap

> Complements the universal roadmap (§6) with stack-specific tasks.

| Phase | Task | Status |
|---|---|---|
| AgentConfig | ... | [ ] |
| Context | ... | [ ] |

## §pre: Project parameters

> Filled **before starting the Roadmap** (§6.pre) — answers to the implementation agent’s questions.
> The implementation agent (§6.agent) reads this section first; without it, it cannot set up files correctly.

```text
Project:
   Name and description:        ...
   Artifact language:           English (default)
   User communication language: English (default)
   Components (repositories):   ...
   Codebase baseline:           greenfield | legacy+rescue | old-project
   Spec version:               vX.Y.Z  (spec version at project setup — see §6.agent.2)

Tech stack:
   Languages and frameworks:    ...
   Database / ORM:              ...
   IaC tool:                    ...
   CI/CD platform:              ...
   Version control:             GitHub | Azure DevOps | GitLab

AI and models:
   Available AI providers:      ...
   Budget constraints:          ...
   Required agent roles:        all | ...

Testing:
   Existing tests:              none | unit | integration | E2E
   Test framework:              ...
   Coverage thresholds:         unit ≥ ?%  mutation ≥ ?%
   PBT/Fuzz tool:               go-fuzz | hypothesis | fast-check | other

Performance and reliability:
   Target SLA:                  RPS=?  p99=?ms  error_rate≤?%

Security and secrets:
   Secrets store:               Vault | Key Vault | .env+gitignore | other
   SBOM / SLSA requirements:    none | SLSA L1 | SLSA L2

Observability:
   OTEL backend:                none (JSONL only) | Jaeger | Phoenix | other

Team:
   Agent interaction model:     developers | PM | single person
   Existing ADR:                none | path to directory
   Existing .feature specs:     none | path to directory
```
````

---

## 0.9 copilot-instructions.md — system instructions

> `.github/copilot-instructions.md` contains instructions automatically applied to **all** Copilot chats
> in the workspace (VS Code). This is “always-on” background context.
> Size: **no more than ~500 words** — a practical Context Engineering limit: a larger block rarely improves quality
> (the LLM assigns lower priority to distant instructions) and slows down every call.
> Target 300–500 words. If you approach 500, move details into SKILL.md (lazy-loaded) or AGENTS.md, and keep here only
> “active memory” (ADR, sprint focus).

### 0.9.1 Required sections

```markdown
# <Project> — AI Instructions

## Project Overview
[1–2 sentences: product, stack, audience. Do not duplicate AGENTS.md — link to it.]
See: <project>-AgentConfig/AGENTS.md

## Agent Workflow
All multi-step tasks go through the orchestrator.
Pipeline: Phase 0 (specs) -> 1 (code) -> 2 (tests) -> 2.5 (deploy) -> 3 (refactor)
-> 3.5 (regression) -> 4 (arch) -> 5 (security) -> 6 (docs).
See: 00-multi-agent-development-spec.md for full protocol.

## Key Constraints
- Language: all code artifacts and comments in English by default (override in PROJECT.md §pre: "Artifact language").
   Communicate with the user in English by default (override in PROJECT.md §pre: "User communication language").
- Do not modify auto-generated files (see AGENTS.md -> Structure).
- No hardcoded secrets or config values (12-Factor III).
- Every new feature requires .feature spec before Phase 1 (SDD).

## Active ADR
[Key ADRs every agent must know:]
- ADR-###-*: [short title]
- ADR-002-*: ...

## Current Sprint / Focus
[Optional: max 3 items — what is currently in progress]
```

> `## Active ADR` is the most important section: long-term memory visible in every chat.
> `## Current Sprint` is updated once per sprint; do not copy the entire `TASK_CONTEXT.md` into it.

---

## 0.10 SKILL.md — a technology knowledge package

> Agent Skills format — portable knowledge about a specific technology.
> Agents “lazy-load” the relevant SKILL.md per task instead of loading the entire repo context.
> Size: **no more than ~800 words per file**; split by components (backend / frontend / devops).

### 0.10.1 Required SKILL.md sections

````markdown
# SKILL: <Project>-<Component>

> One-sentence summary: what this skill covers and when to use it.

## When to Use This Skill
[3–5 signals: when the agent should load this skill]
- The task concerns [component/technology]
- You need to change [files/modules]

## Tech Stack
| Role | Technology | Version | Notes |
|---|---|---|---|
| Runtime | Go | 1.23 | modules enabled |
| API spec | OpenAPI | 3.0 | swagger-api/ is the source of truth |
| DB | PostgreSQL | 16 | via pgx/v5 |
| Test | testify | v1.9 | suite pattern |

## Build & Test Commands
```bash
# Build
go build ./...

# Test (unit)
go test ./... -race -count=1

# Test (integration) — requires DB
go test ./... -tags=integration

# Lint
golangci-lint run

# Generate (OpenAPI -> handlers)
swagger generate server -f swagger-api/swagger.yaml
```

## Key Conventions
- Error handling: wrap with fmt.Errorf("context: %w", err) — never `_ = err`
- Config: env vars only; viper reads .env in dev, real env in prod
- Generated files: gen/restapi/** — DO NOT edit manually
- Forbidden patterns: global mutable state, init() with side effects

## Common Patterns
[2–3 real examples from the codebase — how to do things correctly in this project]

## Out of Scope
[What this skill does NOT cover — applicability boundaries]

## References
- [AGENTS.md](../AGENTS.md)
- ADRs: `/.github/decisions/`
- swagger-api/swagger.yaml (if applicable)
````

> `## Build & Test Commands` is critical: agents use it to run tests.
> `## Key Conventions` helps prevent violating Constitutional principles 2, 4, 5, 6.

---
