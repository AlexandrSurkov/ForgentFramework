# 6. Adoption roadmap

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

Universal roadmap for any new project. Project file extends it with stack-specific tasks.

## 6.pre Before you start: capture project parameters

Before running the roadmap, answer the questions below. Answers go into PROJECT.md and are used by the Bootstrap Installer (§6.agent) while creating files.

Project:
- Project name and short description (what it does, target users)
- Components (repos): how many repos and what types (backend, frontend, infra, etc.)
- Current baseline (existing project / greenfield / legacy+rescue)

Spec pinning invariant: see Operations 07 §7.4: [07-framework-operations.md](07-framework-operations.md).

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
After that, see Operations 07 for two-tier routing and the safety gate: [07-framework-operations.md](07-framework-operations.md) §7.1–7.2.

### Bootstrap pre-install playbook (vanilla Copilot → install Group 2)

1. Confirm you are using **vanilla Copilot chat** (non-agent mode) and that the target repo does not already contain Group 2 agents.
2. Ask the user for the minimal required inputs:
   - Which bootstrap entrypoint they want to run later: `bootstrap-orchestrator` (recommended) or direct executors.
   - Which model IDs to set for each created bootstrap agent (`model: ...` in frontmatter) and any tool restrictions.
   - Whether `.github/agents/` already exists and contains repurposed (non-framework) agents that must be preserved.
3. Create the Group 2 bootstrap agent files under `.github/agents/` by copying/adapting the shipped templates:
   - Template source: `framework/templates/bootstrap-agents-templates/root/.github/agents/`
   - Expected outputs:
     - `.github/agents/bootstrap-orchestrator.agent.md` (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`)
     - `.github/agents/bootstrap-installer.agent.md` (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-installer.agent.md`)
     - `.github/agents/bootstrap-upgrader.agent.md` (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-upgrader.agent.md`)
     - `.github/agents/bootstrap-remover.agent.md` (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-remover.agent.md`)
     - `.github/agents/bootstrap-critic.agent.md` (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-critic.agent.md`)
4. Apply the required framework-operation checks/gates for agent/prompt edits by following (link only):
   - Two-tier routing and scope boundary: [07-framework-operations.md](07-framework-operations.md) §7.1
   - AWESOME-COPILOT gate (because you are creating `.github/agents/**`): [07-framework-operations.md](07-framework-operations.md) §7.3
5. Create the minimal gate artifact expected by Operations when the AWESOME-COPILOT trigger fires:
   - Expected output: `.agents/compliance/awesome-copilot-gate.md` (template: `framework/templates/repo-files-templates/root/.agents/compliance/awesome-copilot-gate.md`)
6. Stop and list the created files.
7. Run the next stage using Group 2 (not Group 1) per [07-framework-operations.md](07-framework-operations.md) §7.1:
   - Recommended: run `.github/agents/bootstrap-orchestrator.agent.md` and request **Install**.
   - Alternatively: run `.github/agents/bootstrap-installer.agent.md` directly.

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
- Follow Operations 07 for all framework-operation invariants and gates (routing, safety gate, AWESOME-COPILOT, spec pinning): [07-framework-operations.md](07-framework-operations.md) (§7.1–7.4).
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

Normative remediation policy for bootstrap operations (Install/Upgrade/Remove):
- Bootstrap agents MUST maximize autonomous repository discovery before asking the user for additional inputs.
- Bootstrap agents MUST use evidence-based autofill for inferred values (from files, repository layout, and existing configuration artifacts).
- Bootstrap agents MAY ask user questions only for TODOs that remain unresolved after exhaustive discovery.
- Each user question MUST map to a single unresolved TODO and MUST state the blocking step that cannot continue without that answer.
- Bootstrap agents MUST NOT ask broad or redundant questionnaires when the answer is derivable from repository evidence.

Normative RC mapping labels for this playbook are defined in Operations 07 §7.2.3: [07-framework-operations.md](07-framework-operations.md) §7.2.3.

1. Run the Group 2 entrypoint:
   - Recommended: run `.github/agents/bootstrap-orchestrator.agent.md` (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`) and request **Install**.
  - Alternatively: run `.github/agents/bootstrap-installer.agent.md` directly (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-installer.agent.md`) ONLY if the direct path preserves the mandatory post-apply handoff/gates in steps 7–8 (no completion before those gates pass).
2. Run a mandatory PRE_DISCOVERY stage before any DRY_RUN planning:
  - Ask the user FIRST to choose topology intent (`single-repo` or `multi-repo`) and persist this as `user_topology_intent` before PRE_DISCOVERY.
  - Discover whether the framework package is already available at repo root as `framework/` (vendored copy) and infer source/update strategy from repository evidence.
  - Discover whether `PROJECT.md` exists and whether `## §pre: Project parameters` is complete using the §6.pre checklist.
  - Discover repository topology (single-repo vs multi-repo AgentConfig + components) and in-scope writable repositories for this run, and record `topology_class`, `topology_confidence`, and `topology_signal` per [07-framework-operations.md](07-framework-operations.md) §7.2.2.
  - If `user_topology_intent=multi-repo`, before topology classification run a parent-directory sibling VCS-root scan relative to `host_repo` and record deterministic parent-scan evidence plus sibling attach output.
  - If `user_topology_intent=multi-repo`, PRE_DISCOVERY MUST include a deterministic sibling scan/attach table with rows sorted lexicographically by sibling relative path.
  - Produce a deterministic full repo inventory (relative paths) for all discovered in-scope repos.
  - Produce deterministic evidence for inferred project identity, technologies, databases, and devops tooling.
  - Run topology preflight before generation/enrichment and record: `topology_class`, `host_repo`, `sibling_repo_roots`, `parent_scan_status`, `parent_scan_evidence`, `sibling_attach_output`, `self_repo_exclusion_applied`, `preflight_verdict`, `fail_reason`.
  - Topology preflight is blocking: if `preflight_verdict=fail`, if `self_repo_exclusion_applied!=yes`, or if `sibling_repo_roots` includes `host_repo`, STOP and return an incomplete state (no generation/enrichment in steps 6–8).
  - If `user_topology_intent=multi-repo`, topology preflight is also blocking when parent-scan evidence is missing (`parent_scan_status!=ok` or `parent_scan_evidence=none`) or sibling attach output is missing (`sibling_attach_output=none`).
  - If host parent directory is unreadable/unavailable, force `topology_confidence=low`, set `preflight_verdict=fail`, and block DRY_RUN.
  - If sibling VCS roots are detected by parent scan, classify topology as `multi-repo` and include sibling paths as host-excluded, relative, lexicographically ordered rows.
  - Discover existing `.github/agents/**`, `.agents/**`, `AGENTS.md`, `llms.txt`, and `.github/copilot-instructions.md` and infer merge/preserve requirements from current usage.
  - Record discovery evidence and autofilled decisions in PRE_DISCOVERY artifacts per [07-framework-operations.md](07-framework-operations.md) §7.2.
3. Require explicit user confirmation/correction of PRE_DISCOVERY output before DRY_RUN:
  - PRE_DISCOVERY MUST be printed as an explicit chat report section titled `## PRE_DISCOVERY Report` and include required fields: `snapshot_id`, `generated_at`, `host_repo`, `user_topology_intent`, `topology_class`, `topology_confidence`, `topology_signal`, `topology_preflight`, plus the deterministic inventory/evidence tables.
  - Show PRE_DISCOVERY output in chat and request confirmation/corrections.
  - The confirmation gate token format is deterministic: user replies `CONFIRMED` or `CORRECTIONS: ...`.
  - Persist a confirmed discovery snapshot (including user corrections) and reference it in DRY_RUN.
  - DRY_RUN is blocked until PRE_DISCOVERY is confirmed.
  - When DRY_RUN is blocked for missing prerequisites, emit `## PRE_DRY_RUN_BLOCK` with deterministic fields from [07-framework-operations.md](07-framework-operations.md) §7.2 and do not emit dry-run stage markers.
4. Ask user questions only for unresolved TODOs after confirmed discovery:
  - Emit one question per unresolved TODO.
  - For each question, include TODO ID, blocking phase/step, and accepted answer format.
  - Topology clarification is special-cased: ask at most one topology question, and only when `topology_confidence = low`.
5. Apply the operational invariants (link only) before and during execution:
   - Two-tier routing + Group 2 scope boundary: [07-framework-operations.md](07-framework-operations.md) §7.1
   - Safety gate (dry-run → confirm → apply): [07-framework-operations.md](07-framework-operations.md) §7.2
   - AWESOME-COPILOT gate when editing `.github/agents/**` or `.github/prompts/**`: [07-framework-operations.md](07-framework-operations.md) §7.3
   - Spec pinning location (`PROJECT.md` header only): [07-framework-operations.md](07-framework-operations.md) §7.4
6. Dry-run: produce a complete phase-by-phase plan for §6.0–§6.8 and enumerate every create/modify/delete operation with paths (per [07-framework-operations.md](07-framework-operations.md) §7.2).
  - Dry-run MUST use and reference the confirmed discovery snapshot from step 3.
  - Dry-run MUST stop and request re-confirmation if PRE_DISCOVERY evidence changed after confirmation (stale snapshot guard).
  - The dry-run MUST include a deterministic source→destination deployment manifest for host repo outputs per [07-framework-operations.md](07-framework-operations.md) §7.2.1.
  - The dry-run MUST include the source inventory summary counters from [07-framework-operations.md](07-framework-operations.md) §7.2.1 and ensure planned `rows_total = source_rows_total`.
  - The dry-run MUST include the topology preflight record and MUST show `preflight_verdict=pass` before any planned generation/enrichment operations.
  - If `user_topology_intent=multi-repo`, DRY_RUN MUST be blocked unless topology preflight includes parent-scan evidence (`parent_scan_status=ok` and `parent_scan_evidence!=none`) and sibling attach output (`sibling_attach_output!=none`).
  - If DRY_RUN is blocked before planning, output `## PRE_DRY_RUN_BLOCK` and stop before `[DISCOVERY]`.
7. Apply (only after the Operations safety confirmation per §7.2), using shipped templates as the baseline:
   - Template sources:
     - Repo context files: `framework/templates/repo-files-templates/root/**`
     - Bootstrap agents (Group 2): `framework/templates/bootstrap-agents-templates/root/**`
   - Expected outputs (minimum; merge instead of overwrite when files already exist):
     - `PROJECT.md` (includes `> Spec: ...` header pin)
     - `AGENTS.md` and `llms.txt` (at repo root; and per-component when applicable)
     - `.github/copilot-instructions.md`
     - `.github/agents/` (Group 1 project agents + Group 2 bootstrap agents)
     - `.agents/skills/**` (project/component skills)
     - `.agents/compliance/awesome-copilot-gate.md` (create/update when [07-framework-operations.md](07-framework-operations.md) §7.3 triggers)
     - `.vscode/mcp.json` (when adopting MCP in §6.4)
    - Deployment completeness requirement: after APPLY, all manifest rows from §7.2.1 MUST resolve to host destinations with `rows_failed = 0`.
    - Deployment accounting requirement: after APPLY, `rows_total` MUST equal `source_rows_total`.
    - APPLIED_RESULT MUST include a Baseline Host Artifacts Table (`artifact_path | required(yes|conditional) | exists_after_apply(yes|no) | evidence`) and MUST fail if any required row has `exists_after_apply=no`.
    - APPLIED_RESULT MUST fail if `.agents/compliance/awesome-copilot-gate.md` contains any placeholder marker (`TODO`, `PENDING`, `TBD`, `<...>`).
  8. Post-apply context bootstrap (mandatory for install):
    - Run `bootstrap-repo-context-bootstrap` across ALL repos in the confirmed discovery snapshot inventory (not only missing-file repos).
    - Include host-level sibling discovery in scope: when topology is `multi-repo`, confirmed sibling repo roots MUST be processed in the same run.
    - Context bootstrap MUST deeply inspect every discovered repo root and use discovered evidence to enrich AGENTS/llms context quality.
    - Host `domain/**/*.md` context documents MUST be filled from discovered evidence when evidence exists (not left TODO-only when evidence exists).
    - Host `.vscode/project.code-workspace` folder inventory MUST deterministically align to the confirmed discovery snapshot repo inventory using relative paths.
    - Workspace alignment is exact-set based: rewrite `folders` entries to the confirmed inventory (relative paths only) and do not preserve stale/extraneous repo rows.
    - For each discovered repo, non-destructively enrich existing sparse `AGENTS.md` and `llms.txt` where placeholders/TODO gaps exist; do not overwrite already-concrete values.
    - Produce a critic-verifiable per-repo processing table with one row per discovered repo root and columns:
      `repo_root | agents_action(created|enriched|unchanged|skipped) | llms_action(created|enriched|unchanged|skipped) | reason`.
    - Aggregate discovered per-repo metadata into the host repo context files (`AGENTS.md`, `llms.txt`, and other allowlisted host context files) to fill host-level missing context.
    - Produce a host aggregation table with one row per aggregated item and columns:
      `source_repo_root | source_artifact | extracted_fact | host_destination | apply_action`.
    - If host `.github/agents/**` or `.github/prompts/**` are enriched during this step, enforce AWESOME-COPILOT gate compliance and ensure no placeholders remain in the gate report.
    - Produce a per-repo context quality table with columns:
      `repo_root | required_fields_total | required_fields_unknown | unknown_ratio | quality_verdict(pass|fail)`.
    - Required unknown-fields policy:
      - host repo MUST have `required_fields_unknown = 0` and `quality_verdict=pass`;
      - each sibling repo MUST have `unknown_ratio <= 0.10` and `quality_verdict=pass`.
  9. Verify the installation results at the roadmap level:
   - Follow phases §6.0–§6.8 checklists and stop with a summary of created/modified files and any deferred items.
    - Install completion is prohibited unless step 8 ran and `bootstrap-repo-context-bootstrap-critic` approved the post-apply context result.
    - Install completion is prohibited if APPLIED_RESULT baseline host artifacts failed, the gate report has placeholders, or any per-repo context quality row fails the required unknown-fields policy.
    - If install was invoked directly via `bootstrap-installer`, the executor MUST return an explicit handoff for step 7 critic-gated completion (for example `HANDOFF_REQUIRED`) and MUST NOT emit completion status.

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
- Before asking the user for any missing parameter, run exhaustive repository discovery and evidence-based autofill.
- Ask user questions ONLY for TODOs unresolved after discovery, and map each question to one unresolved TODO with a blocking step.
- Ask NEEDS_HUMAN if a parameter requires a team decision you cannot infer
   from PROJECT.md answers.
- Language: create all file content in the configured Artifact language (PROJECT.md §pre; default English).
   Communicate with the user in the configured User communication language (PROJECT.md §pre; default English).
- After each phase: summarise what was created and list any deferred items.

Safety gate: follow Operations 07 §7.2 (link only): [07-framework-operations.md](07-framework-operations.md).

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
- [ ] .gitignore ignores `.agents/traces/*.jsonl` (trace files are local-only; not committed) and allowlists `.agents/traces/README.md`
- [ ] .agents/traces/ directory exists (always written locally)
- [ ] Orchestrator writes a JSONL trace for each session (validate §4 format)
- [ ] After 10+ sessions: use arize-phoenix or jaeger for visualization
```

## 6.7 Phase 7 — Evals (Optional)

```text
- [ ] .agents/evals/ directory (optional)
- [ ] Recommended (if you adopt evals): 3 golden tests per critic in JSONL (approve / request_changes / reject)
- [ ] If you changed a .agent.md and evals exist → run evals: npx promptfoo eval
- [ ] Maintain .github/AGENTS_CHANGELOG.md after each prompt change
```

## 6.8 Phase 8 — Iteration

```text
- [ ] Calibrate rubrics based on real sessions
- [ ] Expand SKILL.md as new conventions appear
- [ ] If needs_human_rate > 20% → simplify tasks or rubrics
- [ ] If approve_on_first < 30% → upgrade executor model or refine SKILL.md
- [ ] Quarterly: review .github/AGENTS_CHANGELOG.md and remove obsolete rules
```

---

## 6.upgrade Upgrade playbook (step-by-step)

This playbook is executed by the **Bootstrap Upgrader (Group 2)**.

1. Run the Group 2 entrypoint:
   - Recommended: run `.github/agents/bootstrap-orchestrator.agent.md` and request **Upgrade**.
   - Alternatively: run `.github/agents/bootstrap-upgrader.agent.md` directly (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-upgrader.agent.md`).
2. Run a mandatory PRE_DISCOVERY stage before any DRY_RUN planning:
  - Discover whether the new framework package contents are available (updated `framework/` vendored copy).
  - Discover the project’s current pinned spec version from `PROJECT.md` header (`> Spec: Multi-Agent Development Specification vX.Y.Z`).
  - Discover repository topology (single-repo vs multi-repo) and produce deterministic full repo inventory using relative repo-root paths.
  - Produce deterministic evidence for inferred project identity, technologies, databases, and devops tooling.
  - Run topology preflight and record: `topology_class`, `host_repo`, `sibling_repo_roots`, `self_repo_exclusion_applied`, `preflight_verdict`, `fail_reason`.
  - Discover repository policy constraints for `.github/agents/**` and `.github/prompts/**` changes from existing governance artifacts.
  - Record discovery evidence and autofilled decisions in PRE_DISCOVERY artifacts per [07-framework-operations.md](07-framework-operations.md) §7.2.
3. Require explicit user confirmation/correction of PRE_DISCOVERY output before DRY_RUN:
  - PRE_DISCOVERY MUST be printed as a chat report section titled exactly `## PRE_DISCOVERY Report`.
  - PRE_DISCOVERY report MUST include required fields: `snapshot_id`, `generated_at`, `host_repo`, `topology_class`, `topology_confidence`, `topology_signal`, `topology_preflight`, plus deterministic inventory/evidence tables.
  - User response format is deterministic: `CONFIRMED` or `CORRECTIONS: ...`.
  - Persist a confirmed discovery snapshot and require DRY_RUN to reference `confirmed_discovery_snapshot_id`.
  - DRY_RUN is blocked until PRE_DISCOVERY is confirmed.
4. Ask user questions only for unresolved TODOs after confirmed discovery:
  - Emit one question per unresolved TODO.
  - For each question, include TODO ID, blocking upgrade step, and accepted answer format.
5. Apply the operational invariants (link only) before and during execution:
   - Two-tier routing + Group 2 scope boundary: [07-framework-operations.md](07-framework-operations.md) §7.1
   - Safety gate (dry-run → confirm → apply): [07-framework-operations.md](07-framework-operations.md) §7.2
   - AWESOME-COPILOT gate when editing `.github/agents/**` or `.github/prompts/**`: [07-framework-operations.md](07-framework-operations.md) §7.3
   - Spec pinning and mandatory update of `PROJECT.md` header: [07-framework-operations.md](07-framework-operations.md) §7.4
6. Identify versions:
   - NEW: `framework/00-multi-agent-development-spec.md` header.
   - OLD: `PROJECT.md` header line `> Spec: Multi-Agent Development Specification vX.Y.Z`.
7. Dry-run: enumerate every file create/modify/delete and explicitly call out destructive steps (per [07-framework-operations.md](07-framework-operations.md) §7.2).
  - Dry-run MUST use and reference the confirmed discovery snapshot from step 3.
  - Dry-run MUST stop and request re-confirmation if PRE_DISCOVERY evidence changed after confirmation (stale snapshot guard).
8. Apply (only after the Operations safety confirmation per §7.2):
   - Update the vendored `framework/` package.
   - Run the Bootstrap Upgrader procedure (next section).
   - Update `PROJECT.md` header `> Spec:` to the new version.
9. After apply, perform required follow-ups when the AWESOME-COPILOT trigger fired (link only):
   - Update `.agents/compliance/awesome-copilot-gate.md` per [07-framework-operations.md](07-framework-operations.md) §7.3.
   - If your repo maintains prompt version history and/or evals, run the project’s configured process (Prompt Versioning / Evals modules).

Expected outputs/files (after APPLY):
- `framework/` updated (vendored copy)
- `PROJECT.md` header pin updated (`> Spec: Multi-Agent Development Specification vNEW`)
- `.github/agents/**` updated as required (Group 1 project agents; and Group 2 bootstrap agents if bootstrap templates changed)
- `.agents/compliance/awesome-copilot-gate.md` updated when [07-framework-operations.md](07-framework-operations.md) §7.3 triggers
- `.github/AGENTS_CHANGELOG.md` updated when prompt-versioning is in use and any `.github/agents/**` prompts changed

---

## 6.agent.2 Bootstrap Upgrader prompt (Group 2)

Use this when the framework spec was updated and you need to sync an already configured project.

Prerequisite: the project records the applied spec version in `PROJECT.md` header line `> Spec: Multi-Agent Development Specification vX.Y.Z`.

```text
You — Bootstrap Upgrader (Group 2). 00-multi-agent-development-spec.md has been updated.
Your task is to bring the project's agent configuration up to date with the new version.

Safety gate: follow Operations 07 §7.2 (link only): [07-framework-operations.md](07-framework-operations.md).

Before DRY_RUN, you MUST run PRE_DISCOVERY and confirmation:
- Print a chat section titled exactly `## PRE_DISCOVERY Report` including required fields: `snapshot_id`, `generated_at`, `host_repo`, `topology_class`, `topology_confidence`, `topology_signal`, `topology_preflight`.
- Include topology/preflight evidence, full repo inventory with relative repo-root paths, inferred project identity, and technologies/databases/devops evidence.
- Ask for deterministic confirmation (`CONFIRMED` or `CORRECTIONS: ...`) and persist a confirmed snapshot.
- DRY_RUN MUST include `confirmed_discovery_snapshot_id` and use only confirmed PRE_DISCOVERY assumptions.

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
  - Before asking the user for any missing parameter, run exhaustive repository discovery and evidence-based autofill.
  - Ask user questions ONLY for TODOs unresolved after discovery, and map each question to one unresolved TODO with a blocking upgrade step.
  - Additive changes that require significant effort may be deferred:
    record as TODO in PROJECT.md §6 Roadmap with spec version reference
  - Language: create all file content in the configured Artifact language (PROJECT.md §pre; default English).
    Communicate with the user in the configured User communication language (PROJECT.md §pre; default English).
  - After completing: summarise what was changed, what was deferred, what requires human decision
```

---

## 6.remove Remove playbook (step-by-step)

This playbook is executed by the **Bootstrap Remover (Group 2)**.

1. Run the Group 2 entrypoint:
   - Recommended: run `.github/agents/bootstrap-orchestrator.agent.md` and request **Remove**.
   - Alternatively: run `.github/agents/bootstrap-remover.agent.md` directly (template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-remover.agent.md`).
2. Run a mandatory PRE_DISCOVERY stage before any DRY_RUN planning:
  - Discover the likely removal mode based on repository state (**Minimal removal** vs **Full cleanup**) and mark it as autofilled if unambiguous.
  - Discover repository topology (single-repo vs multi-repo) and produce deterministic full repo inventory using relative repo-root paths.
  - Produce deterministic evidence for inferred project identity, technologies, databases, and devops tooling.
  - Run topology preflight and record: `topology_class`, `host_repo`, `sibling_repo_roots`, `self_repo_exclusion_applied`, `preflight_verdict`, `fail_reason`.
  - Discover whether target paths are repurposed for non-framework use and must be preserved/merged instead of deleted:
    `.github/agents/**`, `.github/prompts/**`, `.agents/**`, `PROJECT.md`, `AGENTS.md`, `llms.txt`, `.github/copilot-instructions.md`, `.vscode/**`.
  - Discover repository component structure and in-scope component boundaries for this run.
  - Record discovery evidence and autofilled decisions in PRE_DISCOVERY artifacts per [07-framework-operations.md](07-framework-operations.md) §7.2.
3. Require explicit user confirmation/correction of PRE_DISCOVERY output before DRY_RUN:
  - PRE_DISCOVERY MUST be printed as a chat report section titled exactly `## PRE_DISCOVERY Report`.
  - PRE_DISCOVERY report MUST include required fields: `snapshot_id`, `generated_at`, `host_repo`, `topology_class`, `topology_confidence`, `topology_signal`, `topology_preflight`, plus deterministic inventory/evidence tables.
  - User response format is deterministic: `CONFIRMED` or `CORRECTIONS: ...`.
  - Persist a confirmed discovery snapshot and require DRY_RUN to reference `confirmed_discovery_snapshot_id`.
  - DRY_RUN is blocked until PRE_DISCOVERY is confirmed.
4. Ask user questions only for unresolved TODOs after confirmed discovery:
  - Emit one question per unresolved TODO.
  - For each question, include TODO ID, blocking removal step, and accepted answer format.
5. Apply the operational invariants (link only) before and during execution:
   - Two-tier routing + Group 2 scope boundary: [07-framework-operations.md](07-framework-operations.md) §7.1
   - Safety gate (dry-run → confirm → apply): [07-framework-operations.md](07-framework-operations.md) §7.2
   - AWESOME-COPILOT gate when editing `.github/agents/**` or `.github/prompts/**`: [07-framework-operations.md](07-framework-operations.md) §7.3
6. Dry-run: enumerate all files that will be deleted or modified, and list all references/links that must be updated to avoid broken paths.
  - Dry-run MUST use and reference the confirmed discovery snapshot from step 3.
  - Dry-run MUST stop and request re-confirmation if PRE_DISCOVERY evidence changed after confirmation (stale snapshot guard).
7. Apply (only after the Operations safety confirmation per §7.2):
   - Remove framework-owned agent prompts (unless confirmed as repurposed by the user):
     - Group 2 (bootstrap) agents: `.github/agents/bootstrap-*.agent.md`
     - Group 1 (project) agents installed for this framework (enumerate from `AGENTS.md` and the current `.github/agents/` contents)
   - Minimal removal (spec-only): delete `framework/` and update any links that reference `framework/**` paths.
   - Full cleanup (spec + agent system): additionally remove framework-introduced scaffolding under `.github/prompts/**`, `.agents/**`, `.vscode/**`, and framework-owned docs/config files, while preserving any repurposed files confirmed by the user.
     - Ordering rule: when removing `.agents/**`, keep `.agents/compliance/awesome-copilot-gate.md` until the very end so the bootstrap critic can verify the AWESOME-COPILOT gate on the applied change set; delete `.agents/compliance/awesome-copilot-gate.md` only as the final cleanup step after all other removals.
8. Stop and summarize what was deleted/changed, and list any preserved files that were treated as repurposed.

Expected outputs/files:
- Minimal removal (spec-only):
  - Deleted: `framework/`
  - Deleted: `.github/agents/bootstrap-*.agent.md`
  - Deleted: Group 1 framework agent prompts under `.github/agents/` (exact list enumerated in the dry-run)
  - Updated: any references/links to `framework/**` paths
- Full cleanup (spec + agent system):
  - Everything in Minimal removal, plus deleted framework-introduced scaffolding under `.github/prompts/**`, `.agents/**`, `.vscode/**`, and other framework-owned docs/config files (as enumerated in the dry-run)

Recommended removal modes:

- Minimal removal (spec-only): remove vendored `framework/` package and fix links.
- Full cleanup (spec + agent system): remove files introduced solely for this framework.

If the repo has repurposed any files (e.g., `.github/agents/**` used for non-framework agents), removal MUST preserve them.

---

## 6.agent.3 Bootstrap Remover prompt (Group 2)

```text
You — Bootstrap Remover (Group 2). Your task is to remove the framework and framework-introduced agent scaffolding from this repository.

Constraints:
- Follow `framework/spec/07-framework-operations.md` safety gate: PRE_DISCOVERY → confirm discovery → dry-run → wait for exact token APPLY → apply.
- PRE_DISCOVERY chat report is mandatory before DRY_RUN and MUST use header `## PRE_DISCOVERY Report` with required fields: `snapshot_id`, `generated_at`, `host_repo`, `topology_class`, `topology_confidence`, `topology_signal`, `topology_preflight`.
- Ask user to confirm/correct PRE_DISCOVERY with deterministic tokens: `CONFIRMED` or `CORRECTIONS: ...`.
- DRY_RUN MUST include `confirmed_discovery_snapshot_id` and MUST stop for re-confirmation if PRE_DISCOVERY evidence changed after confirmation.
- Default to the safest interpretation: never delete a file unless it was introduced solely for this framework.
- Before asking the user for any missing parameter, run exhaustive repository discovery and evidence-based autofill.
- Ask user questions ONLY for TODOs unresolved after discovery, and map each question to one unresolved TODO with a blocking removal step.
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
3. Creates .agents/traces/<trace_id>.jsonl
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

backend-critic verdict (iter 2): `APPROVE` — no open BLOCKERs and no open WARNINGs.

**Step 4 — CI Gate 1 (auto) → Gate 2 (critic) → Gate 3 (human) → merge**

```text
Gate 1: tests green, lint pass
Gate 2: backend-critic reviewed; no open BLOCKERs or WARNINGs
Gate 3: PM verifies description appears in API response — approved (human)
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
{"ts":"2026-02-23T14:34:05Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s07","parent_span_id":"s01","agent":"backend-critic","operation":"critique","subtask":2,"iteration":2,"verdict":"APPROVE","blockers":0,"warnings":0,"input_tokens":900,"output_tokens":180,"duration_ms":8400}
{"ts":"2026-02-23T14:34:10Z","trace_id":"20260223T143200Z-add-host-desc-7f3a","span_id":"s08","parent_span_id":"s01","agent":"orchestrator","operation":"complete","task":"add-host-description","total_iterations":2,"input_tokens":7940,"output_tokens":2095,"duration_ms":127600}
```

---

# G. Glossary

| Term | Definition |
|---|---|
| **APPROVE** | Critic verdict (canonical): see §1.3.9 in [01-architecture.md](01-architecture.md#verdict-enum) |
| **REQUEST_CHANGES** | Critic verdict (canonical): see §1.3.9 in [01-architecture.md](01-architecture.md#verdict-enum) |
| **REJECT** | Critic verdict (canonical): see §1.3.9 in [01-architecture.md](01-architecture.md#verdict-enum) |
| **NEEDS_HUMAN** | Subtask status (canonical): see §1.3.9 in [01-architecture.md](01-architecture.md#subtask-status-enum) |
| **BLOCKER** | Severity that blocks moving to the next phase |
| **WARNING** | Severity that MUST yield REQUEST_CHANGES; it must be fixed before APPROVE |
| **SUGGESTION** | Severity that does not block; optional |
| **ACKNOWLEDGED** | Closes a SUGGESTION thread (executor declines) or records that the critic withdrew the finding; does not unblock WARNING |
| **DEFERRED** | Fix is postponed to a future sprint (SUGGESTION-only) |
| **ESCALATED** | Subtask status (canonical): see §1.3.9 in [01-architecture.md](01-architecture.md#subtask-status-enum) |
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
