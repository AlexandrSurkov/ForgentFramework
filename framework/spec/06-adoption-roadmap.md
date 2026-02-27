# 6. Adoption roadmap

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

Universal roadmap for any new project. Project file extends it with stack-specific tasks.

## 6.pre Before you start: capture project parameters

Before running the roadmap, answer the questions below. Answers go into PROJECT.md and are used by the Bootstrap Installer (§6.agent) while creating files.

Project:
- Project name and short description (what it does, target users)
- Components (repos): how many repos and what types (backend, frontend, infra, etc.)
- Current baseline (existing project / greenfield / legacy+rescue)

Spec pinning is recorded in one canonical place only:
- `PROJECT.md` header line: `> Spec: Multi-Agent Development Specification vX.Y.Z`

Do not add secondary spec-version fields (for example `Spec version: vX.Y.Z`) anywhere in `PROJECT.md`.

Tech stack:
- Languages and frameworks (backend / frontend / mobile)
- Database and ORM/query library
- IaC tool (Terraform / Helm / Pulumi / other)
- CI/CD platform (GitHub Actions / Azure Pipelines / GitLab CI)
- Source control (GitHub / Azure DevOps / GitLab)

AI and models:
- Available AI providers (Azure OpenAI / Anthropic API / GitHub Copilot / other)
- Budget constraints for LLM calls
- Which agent roles are needed (all base / subset / additional) (see PROJECT.md §2.1)

Testing:
- Existing tests (unit / integration / E2E) and frameworks
- Expected thresholds (unit % / mutation %)
- Property-based / fuzz tool (go-fuzz / hypothesis / fast-check / other)

Performance and reliability:
- Target SLAs: RPS, p99 latency, allowed error rate
   (used by Phase 2.5 load tests and QA Critic checks — without these, load tests cannot define pass criteria)

Security and secrets:
- Secret storage (Vault / Key Vault / AWS Secrets Manager / .env + gitignore / other)
- SBOM or SLSA provenance requirements (regulated environment)

Observability:
- Where OTEL spans go (Jaeger endpoint / Phoenix URL / none yet — JSONL only)
- Existing tracing backend in the project

Team:
- Who interacts with AI agents (devs / PM / one person)
- Existing ADRs/architecture docs to consider
- Existing `.feature` specifications

Language:
- Artifact language (default English; override in PROJECT.md §pre)
- User communication language (default English; override in PROJECT.md §pre)

---

## 6.bootstrap Vanilla Copilot pre-install: create Bootstrap (Group 2) agents

When a repo does not yet have the framework’s bootstrap agents (Group 2), you must create them once using vanilla Copilot chat (non-agent mode).
After that, all Install/Upgrade/Remove operations MUST be routed to Group 2 (see [07-framework-operations.md](07-framework-operations.md) §7.1–7.2).

Minimum required bootstrap set (enables two-tier routing for operations):
- `bootstrap-installer` (Install)
- `bootstrap-upgrader` (Upgrade)
- `bootstrap-remover` (Remove)

Template default (shipped in `framework/templates/bootstrap-agents-templates/`):
- `bootstrap-orchestrator` (routes Install/Upgrade/Remove to the executors)
- `bootstrap-installer`
- `bootstrap-upgrader`
- `bootstrap-remover`
- `bootstrap-critic` (reviews bootstrap operations)

For best effectiveness (recommended when available):
- Use `bootstrap-orchestrator` as the Group 2 entrypoint.
- It delegates to the matching executor and then invokes `bootstrap-critic` to enforce the bootstrap safety/boundary rules.

Runnable vanilla-Copilot prompt (copy/paste):

```text
You are working in a repository that does not yet have bootstrap agents.

Task: Create Group 2 bootstrap agents as `.github/agents/*.agent.md` files.

Constraints:
- Use the `.agent.md` format from `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` (A1.1).
- The bootstrap agents MUST follow `framework/spec/07-framework-operations.md`:
   - Two-tier model (Group 2 responsibilities)
   - Safety gate: dry-run → wait for exact token APPLY → apply
   - AWESOME-COPILOT gate: when editing `.github/agents/**` or `.github/prompts/**`, update `.agents/compliance/awesome-copilot-gate.md`.
- Keep bootstrap agents narrowly scoped to framework install/upgrade/remove. Do not add product features.

Create these agents:
1) bootstrap-orchestrator
2) bootstrap-installer
3) bootstrap-upgrader
4) bootstrap-remover
5) bootstrap-critic

After creating the agent files, stop and list the created files.
```

---

## 6.install Install playbook (step-by-step)

This playbook is executed by the **Bootstrap Installer (Group 2)**.

1. Ensure the framework package exists at repo root (`framework/` vendored copy).
2. Create `PROJECT.md` using the template in [00-infrastructure.md](00-infrastructure.md) §0.8 and fill `## §pre: Project parameters` (use the checklist above).
3. Ensure Group 2 bootstrap agents exist (see §6.bootstrap).
4. Run the Bootstrap Installer prompt (next section) and follow phases §6.0–§6.8.

---

## 6.agent Bootstrap Installer prompt (Group 2)

Use this prompt as the system instruction for the agent that will implement this spec in a project.

```text
You — Bootstrap Installer (Group 2). Your task is to install the multi-agent development
system into this repository, following 00-multi-agent-development-spec.md and the answers
in PROJECT.md (`## §pre: Project parameters`).

Rules:
- Work through Roadmap phases §6.0–6.8 sequentially.
- Before each phase: read the corresponding spec section.
- Create files using the templates in the spec (exact section referenced in each phase).
- At each phase: check off items in the checklist. Do not proceed to the next
   phase until all checkboxes are done or explicitly deferred with a reason.
- Ask NEEDS_HUMAN if a parameter requires a team decision you cannot infer
   from PROJECT.md answers.
- Language: create all file content in the configured Artifact language (PROJECT.md §pre; default English).
   Communicate with the user in the configured User communication language (PROJECT.md §pre; default English).
- After each phase: summarise what was created and list any deferred items.

Safety gate (deterministic):
- Step A (dry-run): present a complete file-by-file change plan.
- Step B (confirm): wait for the user to reply with the exact token APPLY.
- Step C (apply): only after APPLY, create/modify files.

Context files to read first (in this order):
   1. 00-multi-agent-development-spec.md (umbrella index)
   2. spec/ (all spec modules linked from 00-multi-agent-development-spec.md)
   3. PROJECT.md (project parameters — must already exist with §pre filled in)

Start: say which phase you are beginning and ask for confirmation.
```

---

## 6.0 Phase 0 — AgentConfig repo

> **Legacy / rescue:** if repos or CI already exist, before Phase 0:
> - Audit existing AGENTS.md, CI configs, ADRs — do not overwrite; merge.
> - Record current metrics (coverage, DORA) in PROJECT.md §pre as a baseline.
> - Mark `baseline: legacy+rescue` in PROJECT.md §pre — implementation agent will use merge mode.

Checklist:

```text
- [ ] Create <project>-AgentConfig repo (or use an existing one)
- [ ] Create .vscode/<project>.code-workspace (all project repos)
- [ ] Create .gitignore (.agents/session/)
- [ ] Open the workspace and confirm all repos are visible as folders
- [ ] Create README.md describing:
      why this repo exists, how to run agents, links to 00-multi-agent-development-spec.md
      and PROJECT.md, and an Observability AI Workflow (§4) section:
        – where traces are stored (.agents/traces/)
        – JSONL format (§4.5)
        – visualization options (§4.7: arize-phoenix / jaeger)
        – key metrics (§4.2, §4.3 DORA)
```

## 6.1 Phase 1 — Context

```text
- [ ] <project>-AgentConfig/AGENTS.md — global (template §0.3)
- [ ] AGENTS.md in each component repo
- [ ] llms.txt in each component repo (template §0.4)
- [ ] .github/copilot-instructions.md — system instructions
- [ ] .github/pull_request_template.md (template §0.6)
- [ ] Configure branch protection for `main` and `develop` in all repos (§0.6.2)
      Required status checks: Gate 1 CI jobs; Minimum 1 reviewer; No direct push
```

## 6.2 Phase 2 — Agent skills

```text
- [ ] SKILL.md for each component: backend, frontend, devops
- [ ] references/ with technology conventions and examples
- [ ] In backend SKILL.md: a "Property-Based / Fuzz Testing" section — run commands
      for the chosen tool from PROJECT.md §pre (go-fuzz / govulncheck / hypothesis / fast-check / other)
      Without this, the first parser/deserializer will immediately trigger a Backend Critic WARNING (§3.4)
- [ ] Verify: the agent loads SKILL.md at the beginning of each task?
```

## 6.3 Phase 3 — Agents

```text
- [ ] <project>-orchestrator.agent.md
- [ ] Each (executor + critic) pair: architect, backend, frontend, qa, devops, security, documentation
- [ ] Verify models using the power/cost matrix (PROJECT.md §2)
- [ ] .pre-commit-config.yaml in each component repo
      (fmt, lint, validate — commands from SKILL.md §Build & Test Commands)
      Without this, DoD "Pre-commit hooks passed" (§3.11) cannot be satisfied
- [ ] Run: pre-commit install — in each component repo after creating .pre-commit-config.yaml
      (without it, hooks are not registered in git and will never run)
```

**Minimal `.pre-commit-config.yaml` (Go/TypeScript — adapt to your stack using SKILL.md):**

```yaml
# .pre-commit-config.yaml  (put in the root of each component repo)
# Install: pip install pre-commit && pre-commit install
repos:
  # ── universal ─────────────────────────────────────────────────────────────
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: detect-private-key        # ← DevOps Critic BLOCKER: secrets in code
      - id: check-added-large-files

  # ── Go (remove if not Go) ─────────────────────────────────────────────────
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: golangci-lint            # requires golangci-lint in PATH

  # ── TypeScript / Node (remove if not TS) ─────────────────────────────────
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
        additional_dependencies: ['eslint@9', 'typescript-eslint']
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0
    hooks:
      - id: prettier
```

> Hook list must be derived from commands `## Build & Test Commands` in the component’s SKILL.md.
> Minimum for any language: formatter + linter + secret scanning (`detect-private-key`).
> Hook registry: [pre-commit.com/hooks](https://pre-commit.com/hooks.html).

- [ ] Run the first real task through the orchestrator

## 6.4 Phase 4 — MCP servers

```text
- [ ] .vscode/mcp.json
- [ ] SCM MCP (GitHub / Azure DevOps / GitLab)
- [ ] Container runtime MCP (docker)
- [ ] IaC tool MCP (terraform / ansible / etc.)
- [ ] Validate: agents use MCP tools during tasks
```

**Minimal `.vscode/mcp.json`:**

```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "docker": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-docker"]
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "${workspaceFolder}"]
    }
  }
}
```

> MCP server registry: [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers).
> Pass secrets only via `${env:VAR}` — do not hard-code in the file (DevOps Critic BLOCKER).
> Project-specific server list goes into PROJECT.md §5.

## 6.5 Phase 5 — ADR and memory

```text
- [ ] First 5 ADRs for key architectural decisions
- [ ] .agents/session/ directory + in .gitignore
- [ ] domain/ directory: glossary.md, bounded-contexts.md, domain-events.md
- [ ] domain/specs/*.feature for core entities (minimum 3)
- [ ] Test workflow: orchestrator → executor → critic → APPROVE on a real task
```

## 6.6 Phase 6 — Observability

```text
- [ ] Trace mode chosen (Mode 1: committed sanitized traces | Mode 2: external / not committed)
- [ ] .gitignore configured to match Trace mode
- [ ] .agents/traces/ directory exists (always written locally)
- [ ] Orchestrator writes a JSONL trace for each session (validate §4 format)
- [ ] After 10+ sessions: use arize-phoenix or jaeger for visualization
```

## 6.7 Phase 7 — Evals (Optional)

```text
- [ ] .agents/evals/ directory (optional)
- [ ] Recommended (if you adopt evals): 3 golden tests per critic in JSONL (approve / request_changes / reject)
- [ ] If you changed a .agent.md and evals exist → run evals: npx promptfoo eval
- [ ] Maintain AGENTS_CHANGELOG.md after each prompt change
```

## 6.8 Phase 8 — Iteration

```text
- [ ] Calibrate rubrics based on real sessions
- [ ] Expand SKILL.md as new conventions appear
- [ ] If needs_human_rate > 20% → simplify tasks or rubrics
- [ ] If approve_on_first < 30% → upgrade executor model or refine SKILL.md
- [ ] Quarterly: review AGENTS_CHANGELOG.md and remove obsolete rules
```

---

## 6.upgrade Upgrade playbook (step-by-step)

This playbook is executed by the **Bootstrap Upgrader (Group 2)**.

1. Identify versions:
  - NEW: `framework/00-multi-agent-development-spec.md` header.
  - OLD: `PROJECT.md` header line `> Spec: Multi-Agent Development Specification vX.Y.Z`.
2. Update the vendored `framework/` package.
3. Run the Bootstrap Upgrader prompt (next section).
4. If any `.github/agents/**/*.agent.md` or `.github/prompts/**/*.prompt.md` changed:
  - Update `.github/AGENTS_CHANGELOG.md` (Prompt Versioning module).
  - Update `.agents/compliance/awesome-copilot-gate.md` (07-framework-operations gate).
  - Run evals/golden tests if your repo uses them.
5. Update `PROJECT.md` header `> Spec:` to the new version.

---

## 6.agent.2 Bootstrap Upgrader prompt (Group 2)

Use this when the framework spec was updated and you need to sync an already configured project.

Prerequisite: the project records the applied spec version in `PROJECT.md` header line `> Spec: Multi-Agent Development Specification vX.Y.Z`.

```text
You — Bootstrap Upgrader (Group 2). 00-multi-agent-development-spec.md has been updated.
Your task is to bring the project's agent configuration up to date with the new version.

Safety gate (deterministic):
- Step A (dry-run): present a complete file-by-file change plan.
- Step B (confirm): wait for the user to reply with the exact token APPLY.
- Step C (apply): only after APPLY, create/modify files.

Input:
  - 00-multi-agent-development-spec.md new version (umbrella index)
  - spec/ (all spec modules linked from 00-multi-agent-development-spec.md)
  - PROJECT.md (header line: Spec: Multi-Agent Development Specification vX.Y.Z — the version the project was set up with)

Step 1 — Identify version delta.
  Read the new spec version from 00-multi-agent-development-spec.md header.
  Read the project's current spec version from PROJECT.md.
  State: "Updating from vOLD to vNEW".
  If versions are equal — report "No update needed" and stop.

Step 2 — Audit each major section. Compare new spec with project files:
  §0.3  AGENTS.md global + component — new required fields?
  §0.8  PROJECT.md template — new required sections?
  §0.9  copilot-instructions.md — new required sections?
  §1.2  Model tiers — models removed or reclassified? Check PROJECT.md §2.2 for affected agents.
  §1.3  Pipeline — new phases, gates or protocols?
  §3.x  Critic rubrics — new BLOCKER/WARNING triggers? Update .agent.md critic prompts.
  §5    Golden tests — new required test cases?
  §6    Roadmap — new phases or checklist items?

Step 3 — Classify each delta:
  BREAKING — project cannot function correctly without this update
    (e.g. verdict type renamed, gate logic changed, new mandatory TASK_CONTEXT field)
  ADDITIVE — project works without it but quality improves
    (e.g. new WARNING trigger, new recommended tool)

Step 4 — Apply changes (BREAKING first, then ADDITIVE):
  - Update .agent.md files that reference changed rubrics or pipeline logic
  - Update PROJECT.md sections that gained new required fields (merge — do NOT overwrite
    project-specific values: §pre answers, custom rubrics, model choices)
  - Update copilot-instructions.md if §0.9 changed
  - Leave explicitly project-customised sections untouched unless BREAKING

Step 5 — After any `.github/agents/**` or `.github/prompts/**` change:
  - Update `.agents/compliance/awesome-copilot-gate.md` (required by 07-framework-operations).
  - Maintain `.github/AGENTS_CHANGELOG.md` per the Prompt Versioning module.
  - If evals exist → run evals: npx promptfoo eval

Step 6 — Update PROJECT.md header:
  > Spec: Multi-Agent Development Specification vNEW

Rules:
  - NEEDS_HUMAN if a BREAKING change requires a team decision
    (e.g. model removed from an available tier, new mandatory gate requiring CI reconfiguration)
  - Additive changes that require significant effort may be deferred:
    record as TODO in PROJECT.md §6 Roadmap with spec version reference
  - Language: create all file content in the configured Artifact language (PROJECT.md §pre; default English).
    Communicate with the user in the configured User communication language (PROJECT.md §pre; default English).
  - After completing: summarise what was changed, what was deferred, what requires human decision
```

---

## 6.remove Remove playbook (step-by-step)

This playbook is executed by the **Bootstrap Remover (Group 2)**.

1. Dry-run: enumerate all files that will be deleted or modified.
2. Confirm: wait for exact token APPLY.
3. Apply: remove framework integration artifacts.

Recommended removal modes:

- Minimal removal (spec-only): remove vendored `framework/` package and fix links.
- Full cleanup (spec + agent system): remove files introduced solely for this framework.

If the repo has repurposed any files (e.g., `.github/agents/**` used for non-framework agents), removal MUST preserve them.

---

## 6.agent.3 Bootstrap Remover prompt (Group 2)

```text
You — Bootstrap Remover (Group 2). Your task is to remove the framework and framework-introduced agent scaffolding from this repository.

Constraints:
- Follow `framework/spec/07-framework-operations.md` safety gate: dry-run → wait for exact token APPLY → apply.
- Default to the safest interpretation: never delete a file unless it was introduced solely for this framework.
- If unsure whether a file is repurposed, ask NEEDS_HUMAN.

Dry-run output MUST include:
- A list of files to delete
- A list of files to modify (and why)
- A list of references/links that must be updated to avoid broken paths

After the user replies APPLY, perform the removals and then summarise the result.
```

---

## 6.9 End-to-end example: full cycle for a minimal feature

> Task: "Add field `description` to Host entity in the backend."

**Step 0 — Orchestrator reads ADRs and chooses fast-track**

```text
1. Reads .github/decisions/ — no conflicts
2. Type: feature/* → full pipeline
3. Creates .agents/traces/20260223-add-host-desc.jsonl
4. Writes TASK_CONTEXT.md decomposition:
   #1 architect: .feature + ADR (if schema change)
   #2 backend-dev: model + migration + tests
```

**Step 1 — architect writes Gherkin scenario**

```gherkin
# domain/specs/host.feature
Scenario: Host has description
  Given a host exists with id "host-1"
  When I GET /hosts/host-1
  Then the response body contains field "description"
  And "description" is a string or null
```

architect-critic: `APPROVE` — scenario is unambiguous and does not violate ADRs.

**Step 2 — backend-dev implements (iteration 1)**

```text
- models/host.go: add Description *string
- migration: ALTER TABLE hosts ADD COLUMN description TEXT
- test: TestGetHost_Description
```

backend-critic verdict (iter 1): `REQUEST_CHANGES`

```text
BLOCKER: handlers/host.go:78 — Description is not included in GET /hosts/:id response
WARNING:  models/host.go:34 — missing godoc for the field
```

**Step 3 — backend-dev implements (iteration 2)**

```text
- handlers/host.go: add Description to JSON response
- models/host.go: add godoc
```

backend-critic verdict (iter 2): `APPROVE` — BLOCKERs closed.

**Step 4 — CI Gate 1 (auto) → Gate 2 (critic) → Gate 3 (human) → merge**

```text
Gate 1: tests green, lint pass
Gate 2: backend-critic reviewed; no open BLOCKERs
Gate 3: PM verifies description appears in API response — APPROVED
Merge → main + tag v1.4.7
```

**Session trace** (format §4.5: separate spans for executor and critic, verdict — only in critique spans):

```json
{"ts":"2026-02-23T14:32:00Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s01","parent_span_id":null,"agent":"orchestrator","operation":"plan","task":"add-host-description","fast_track":"feature","input_tokens":320,"output_tokens":75,"duration_ms":2800}
{"ts":"2026-02-23T14:32:05Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s02","parent_span_id":"s01","agent":"architect","operation":"execute","subtask":1,"iteration":1,"input_tokens":1100,"output_tokens":280,"duration_ms":9200}
{"ts":"2026-02-23T14:32:20Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s03","parent_span_id":"s01","agent":"architect-critic","operation":"critique","subtask":1,"iteration":1,"verdict":"APPROVE","blockers":0,"warnings":0,"input_tokens":700,"output_tokens":90,"duration_ms":5100}
{"ts":"2026-02-23T14:32:28Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s04","parent_span_id":"s01","agent":"backend-dev","operation":"execute","subtask":2,"iteration":1,"input_tokens":1840,"output_tokens":620,"duration_ms":18400}
{"ts":"2026-02-23T14:33:10Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s05","parent_span_id":"s01","agent":"backend-critic","operation":"critique","subtask":2,"iteration":1,"verdict":"REQUEST_CHANGES","blockers":1,"warnings":1,"input_tokens":980,"output_tokens":310,"duration_ms":9100}
{"ts":"2026-02-23T14:33:15Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s06","parent_span_id":"s01","agent":"backend-dev","operation":"execute","subtask":2,"iteration":2,"input_tokens":2100,"output_tokens":540,"duration_ms":16200}
{"ts":"2026-02-23T14:34:05Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s07","parent_span_id":"s01","agent":"backend-critic","operation":"critique","subtask":2,"iteration":2,"verdict":"APPROVE","blockers":0,"warnings":1,"input_tokens":900,"output_tokens":180,"duration_ms":8400}
{"ts":"2026-02-23T14:34:10Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s08","parent_span_id":"s01","agent":"orchestrator","operation":"complete","task":"add-host-description","total_iterations":2,"input_tokens":7940,"output_tokens":2095,"duration_ms":127600}
```

---

# G. Glossary

| Term | Definition |
|---|---|
| **APPROVE** | Critic verdict: no BLOCKERs; WARNING allowed |
| **REQUEST_CHANGES** | Critic verdict: there is a BLOCKER; executor fixes and repeats |
| **REJECT** | Critic verdict: fundamental constitutional violation; not patch-fixable |
| **NEEDS_HUMAN** | Reached max_iterations=3 or human input is required |
| **BLOCKER** | Severity that blocks moving to the next phase |
| **WARNING** | Severity that can still allow APPROVE with explicit ACKNOWLEDGED |
| **SUGGESTION** | Severity that does not block; optional |
| **ACKNOWLEDGED** | A warning is consciously deferred in the PR thread; unblocks APPROVE |
| **DEFERRED** | Fix is postponed to a future sprint |
| **ESCALATED** | Blocker escalated to a higher-level human without waiting for resolution |
| **TASK_CONTEXT** | File `.agents/session/<trace_id>/TASK_CONTEXT.md`; short-term session memory |
| **Fast-Track** | Shortened pipeline for hotfix / docs-only / infra |
| **Critique Report** | Critic’s structured response (verdict + findings) |
| **Previous Attempts** | TASK_CONTEXT section with REQUEST_CHANGES history for Reflexion |
| **DoR** | Definition of Ready: criteria before starting the work |
| **DoD** | Definition of Done: completion criteria |
| **executor** | Agent that produces work: code, tests, documentation |
| **critic** | Agent that reviews executor output against the rubric |
| **orchestrator** | Agent that decomposes tasks, assigns roles, and controls TASK_CONTEXT |
| **Tier (T1/T2/T3)** | Model level: T1=reasoning-heavy, T2=strong general, T3=efficient |
| **golden tests** | Fixed tests {input, expected_verdict} to detect prompt regressions |
| **trace_id** | Unique session ID (recommended: `YYYYMMDDTHHMMSSZ-task-slug-rand4`); used in JSONL traces and session directory names |
