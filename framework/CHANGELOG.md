# Changelog — Multi-Agent Development Specification

All notable changes to the **Multi-Agent Development Specification** (the `framework/` package copied into downstream AgentConfig repos) are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

## [0.31.3] - 2026-03-05

### Fixed
- Bootstrap critic enforcement now includes a deterministic BLOCKER when **Sibling Validation Table** rows are not lexicographically ordered by `candidate_path`.
- Bootstrap critic now enforces value-level workspace-first fallback semantics in DRY_RUN topology preflight: workspace scan must be attempted first; user-path validation is allowed only when workspace scan is unavailable, with deterministic candidate-source consistency checks.

## [0.31.2] - 2026-03-05

### Changed
- Safety gate now requires topology intent capture as the first user interaction (`single-repo` or `multi-repo`) and requires persisted `user_topology_intent` before PRE_DISCOVERY.
- PRE_DISCOVERY/DRY_RUN contracts now require `user_topology_intent` carry-forward and, for `multi-repo` intent, deterministic parent-neighbor sibling VCS-root scan evidence plus sibling attach output.
- DRY_RUN gating is now deterministic for multi-repo intent: missing sibling scan evidence or missing sibling attach output is a blocking condition.
- Operations and roadmap canonical modules were synchronized with template mirrors, and bootstrap templates (`bootstrap-orchestrator`, `bootstrap-installer`, `bootstrap-critic`) were aligned to enforce the same intent-first + multi-repo attach contract.

## [0.31.1] - 2026-03-05

### Fixed
- Closed missed sibling repo detection by making parent-directory sibling VCS-root scan mandatory before topology classification, requiring deterministic parent-scan evidence in PRE_DISCOVERY/topology preflight, and blocking DRY_RUN when evidence is missing.
- Added deterministic failure behavior for unreadable/unavailable host parent directories: force `topology_confidence=low`, fail topology preflight, and block DRY_RUN.
- Required topology promotion to `multi-repo` when sibling VCS roots are found, with host-excluded sibling list normalization (relative paths, deterministic lexicographic order).
- Aligned canonical/template spec modules and bootstrap templates (`bootstrap-installer`, `bootstrap-orchestrator`, `bootstrap-critic`) so critic enforcement of the parent-scan/sibling-topology contract is deterministic.

### Changed
- Tightened PRE_DISCOVERY evidence coverage requirements so `identity`, `technology stack`, `database`, and `devops` are each mandatory categories with either evidence rows or explicit `UNKNOWN` + reason, and aligned bootstrap-critic DRY_RUN validation accordingly.

## [0.31.0] - 2026-03-05

### Changed
- Tightened Operations §7.2 (and template mirror) with explicit user-visible PRE_DISCOVERY requirements, deterministic no-DRY_RUN-before-confirmation rule, and clarified handling of unresolved inferred project identity.
- Extended completion/post-apply rules to require `.vscode/project.code-workspace` in baseline host artifacts and to require evidence-based host `domain/**/*.md` TODO fill reporting.
- Aligned bootstrap templates (`bootstrap-orchestrator`, `bootstrap-installer`, `bootstrap-repo-context-bootstrap`, `bootstrap-critic`, `bootstrap-repo-context-bootstrap-critic`) to enforce the same deterministic confirmation gate, confirmed-inventory workspace rewrite, and stronger per-repo/domain evidence BLOCKER checks.
- Clarified shipped `.vscode/project.code-workspace` template expectations so context bootstrap must produce exact confirmed-inventory host/sibling folder alignment with relative paths only.

## [0.30.0] - 2026-03-05

### Changed
- Extended the mandatory bootstrap safety protocol to Upgrade and Remove executor prompts: PRE_DISCOVERY report in chat, deterministic confirmation/corrections gate, and DRY_RUN dependency on `confirmed_discovery_snapshot_id`.
- Added explicit Upgrade/Remove discovery-first requirements in bootstrap templates: topology + full relative repo inventory, inferred project identity, and technologies/databases/devops evidence before any dry-run planning.
- Aligned Adoption Roadmap upgrade/remove playbooks (and template mirror) to the canonical PRE_DISCOVERY → confirm discovery → DRY_RUN → confirm apply → apply sequence, including stale-snapshot re-confirmation guard.
- Updated embedded `6.agent.2` and `6.agent.3` prompt texts to require deterministic PRE_DISCOVERY report fields and confirmation token format (`CONFIRMED` / `CORRECTIONS: ...`) before DRY_RUN.

## [0.29.0] - 2026-03-05

### Changed
- Strengthened Operations §7.2 and template mirror with an explicit PRE_DISCOVERY chat-report contract: required report header + mandatory fields (`snapshot_id`, `generated_at`, `host_repo`, `topology_class`, `topology_confidence`, `topology_signal`, `topology_preflight`) before any DRY_RUN output.
- Added deterministic discovery confirmation token gate (`CONFIRMED` or `CORRECTIONS: ...`) and stale-snapshot guard: DRY_RUN must stop and re-confirm if discovery evidence changes after confirmation.
- Tightened roadmap install guidance (and template mirror) so PRE_DISCOVERY report/confirmation requirements are explicit and workspace alignment is exact-set based against confirmed inventory.
- Updated bootstrap templates (`bootstrap-orchestrator`, `bootstrap-installer`, `bootstrap-critic`) to enforce explicit PRE_DISCOVERY report fields, confirmation gate evidence, and confirmed-snapshot DRY_RUN behavior.
- Updated bootstrap context templates (`bootstrap-repo-context-bootstrap`, `bootstrap-repo-context-bootstrap-critic`) to require exact `.vscode/project.code-workspace` folder rewriting to confirmed repo inventory and deterministic BLOCKERs for missing deep-inspection evidence or inventory mismatch.
- Simplified shipped `.vscode/project.code-workspace` template to inventory-driven baseline (host row only), requiring context bootstrap to materialize the confirmed repo set.

## [0.28.0] - 2026-03-05

### Changed
- Clarified that post-apply context bootstrap processing scope is the confirmed PRE_DISCOVERY snapshot repo inventory (plus explicit user corrections), and mirrored this requirement in template spec modules.
- Tightened install roadmap wording so context bootstrap and `.vscode/project.code-workspace` alignment both reference the confirmed discovery snapshot inventory using relative paths.
- Strengthened bootstrap context-bootstrap templates: executor now MUST emit a deterministic per-repo context quality table and enforce host/sibling unknown-field thresholds; critic now treats missing quality table/threshold failures as deterministic BLOCKERs.
- Aligned bootstrap orchestrator/installer/bootstrap-critic templates so handoff and completion checks explicitly require confirmed-snapshot inventory usage for post-apply context processing.

## [0.27.0] - 2026-03-05

### Changed
- Added a mandatory PRE_DISCOVERY stage before DRY_RUN for bootstrap Install/Upgrade/Remove flows, with explicit user confirmation/correction gating before dry-run can start.
- PRE_DISCOVERY now requires deterministic chat-visible discovery outputs: topology/preflight, full repo inventory with relative paths, inferred project identity, and evidence-backed technology/database/devops detection.
- DRY_RUN is now required to reference and use a confirmed discovery snapshot (`confirmed_discovery_snapshot_id`) and to carry forward confirmed topology assumptions.
- Install roadmap and mirrored template roadmap now require PRE_DISCOVERY confirmation before DRY_RUN and align step ordering accordingly.
- Post-apply context bootstrap requirements now explicitly require deep inspection of every discovered repo, evidence-based AGENTS/llms enrichment quality, host domain-doc TODO fill when evidence exists, and deterministic `.vscode/project.code-workspace` alignment to discovered repo inventory paths.
- Bootstrap template prompts (`bootstrap-orchestrator`, `bootstrap-installer`, `bootstrap-critic`, `bootstrap-repo-context-bootstrap`, `bootstrap-repo-context-bootstrap-critic`) were aligned to enforce PRE_DISCOVERY confirmation, confirmed-snapshot DRY_RUN behavior, and stronger context-bootstrap evidence checks.

## [0.26.2] - 2026-03-05

### Changed
- Completion gates now include deterministic APPLIED_RESULT postconditions: required baseline host artifacts table, placeholder-free AWESOME-COPILOT gate report enforcement, and explicit approval blocking when postconditions fail.
- Topology requirements now include a hard preflight record and blocking precondition before generation/enrichment, including deterministic sibling-scope handling and self-repo exclusion checks.
- Install playbook and bootstrap templates (`bootstrap-orchestrator`, `bootstrap-installer`, `bootstrap-critic`) were minimally aligned to enforce the same APPLIED_RESULT postconditions, topology preflight gate, and deterministic required-unknown context-quality thresholds.
- Added explicit RC6 mapping for completion postconditions and per-repo AGENTS/llms required-unknown quality thresholds.

## [0.26.1] - 2026-03-04

### Changed
- Bootstrap operations/spec now require deterministic manifest source-inventory counters (`source_rows_repo_templates`, `source_rows_bootstrap_templates`, `source_rows_total`) and enforce `rows_total = source_rows_total`.
- Topology classification now requires a structured observable `topology_signal` (repo roots, host root, sibling roots, detection basis, contradictions, low-confidence reason, topology-question allowance) with deterministic high/low consistency checks.
- Install post-apply context bootstrap now requires critic-verifiable per-repo processing and host aggregation tables, including sibling-repo processing in multi-repo topology.
- Bootstrap templates (`bootstrap-installer`, `bootstrap-orchestrator`, `bootstrap-repo-context-bootstrap`, `bootstrap-repo-context-bootstrap-critic`, `bootstrap-critic`) were aligned to enforce RC1–RC5 behavior deterministically.
- Install/upgrade completion semantics now explicitly prohibit terminal completion when post-apply `context-bootstrap` or `context-bootstrap-critic` is skipped; direct installer/upgrader invocation must return explicit handoff semantics instead of completion.
- Added explicit normative RC1–RC5 mapping in Operations (§7.2.3) and linked Roadmap install playbook references for deterministic audit traceability.

## [0.25.10] - 2026-03-04

### Changed
- Install/operations guidance now enforces autonomy-first execution and asks users only for unresolved `TODO` values.
- Bootstrap workflow/templates/docs were aligned with the new autonomy-first + unresolved-`TODO` policy.
- Repo-files template mirrors were synchronized with the updated canonical spec modules.

## [0.25.9] - 2026-03-04

### Fixed
- Cross-module reference hygiene: qualified pointers to the canonical trace requirements in Observability (§4.5–§4.6) to avoid drift and duplicated restatements.
- Template portability: corrected repo-template path/namespace assumptions (L1/L2/T4/T5) so vendored templates remain copy-safe across downstream repos.

### Changed
- Trace-writing responsibility wording: aligned modules and templates to the rule that only the orchestrator writes `.agents/traces/**` and subagents return `trace_event` only.
- Bootstrap templates: clarified/standardized `fast_track` bootstrap wiring so routing labels remain consistent during install/upgrade flows.

## [0.25.8] - 2026-03-04

### Changed
- Templates (bootstrap installer): AWESOME-COPILOT gate report must include both Operations labels and `bootstrap-critic` alias labels.
- Templates (bootstrap installer): tighten DRY_RUN placeholder rules — use `PENDING`, forbid raw `<...>` placeholders, and require an explicit `APPLY` follow-up with an auto-consult attempt.

## [0.25.7] - 2026-03-03

### Fixed
- Remove/uninstall: keep `.agents/compliance/awesome-copilot-gate.md` until the final cleanup step; delete it only after all other uninstall removals/edits.

## [0.25.6] - 2026-03-03

### Fixed
- Templates (bootstrap): made the AWC gate stage-aware to prevent bootstrap deadlocks; auto-consult `bootstrap-critic` when `APPLY` is invoked.

## [0.25.5] - 2026-03-03

### Changed
- Removed legacy `excludeAgent: true` from agent YAML frontmatter across shipped templates and repo agents.

## [0.25.4] - 2026-03-02

### Changed
- Templates: Bootstrap repo-context fill improvements: avoid invention; ask user for missing values; include an unfilled-items table; add a deterministic no-response fallback.

## [0.25.3] - 2026-03-02

### Changed
- Editorial / Templates: Normalized agent `name:` fields in `framework/templates/repo-files-templates/` from `<project>-*` template placeholder to concrete `project-*` prefix. Affects `name:` frontmatter, `agents:` list entries, inline body references, and `trace_event` examples in all 17 Group 1 agent `.agent.md` templates and 3 SKILL.md files. No normative MUST/SHOULD/MAY obligations changed.

## [0.25.2] - 2026-03-02

### Changed
- `framework/tools/bootstrap.ps1` and `framework/tools/bootstrap.sh`: added Step 5 that automatically replaces `model: TODO` with `model: gpt-4.1` in all copied `.github/agents/*.agent.md` files after bootstrapping. Removed the corresponding manual instruction from the "Next steps" block.

## [0.25.1] - 2026-03-02

### Fixed
- Added `user-invokable: false` to all non-orchestrator bootstrap agent templates (`bootstrap-installer`, `bootstrap-critic`, `bootstrap-remover`, `bootstrap-upgrader`, `bootstrap-repo-context-bootstrap`, `bootstrap-repo-context-bootstrap-critic`) so that only `bootstrap-orchestrator` appears in the VS Code agent picker.

## [0.25.0] - 2026-03-02

### Changed
- `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-installer.agent.md`: added `## Auto-discovery: fill PROJECT.md` phase that runs before the dry-run safety gate. The installer now scans the target repo using `fileSearch`, `textSearch`, and `readFile` to detect all §pre fields (project name/desc, languages/frameworks, database/ORM, IaC, CI/CD, source control host, test framework, secrets store, AI provider, observability, components (repos)). Detected values are tagged `[auto]`, `[inferred]`, or `TODO`. The user is only prompted for `[inferred]` / `TODO` fields. Install workflow step 2 updated accordingly.

## [0.24.0] - 2026-03-02

### Added
- `framework/tools/bootstrap.ps1` — PowerShell bootstrap script for Windows; copies bootstrap agents, `.vscode/settings.json`, `.gitignore`, and `.agents/compliance/awesome-copilot-gate.md` from vendored templates into the target repo root.
- `framework/tools/bootstrap.sh` — Bash bootstrap script for Linux/macOS; same behaviour as the PowerShell counterpart. Accepts `--force` to overwrite existing files.

## [0.23.4] - 2026-03-02

### Added
- Added `project-techspec-writer` and `project-techspec-critic` to the shipped `repo-files-templates` agent group.
  - Writer drafts structured TZ documents (Purpose & Goals, Scope, Stakeholders, FR, NFR, Constraints, Acceptance Criteria, Open Questions).
  - Critic reviews for completeness, testability, and non-ambiguity; returns APPROVE / REQUEST_CHANGES / REJECT with deterministic findings.

## [0.23.3] - 2026-03-01

### Fixed
- Completed bootstrap-template protocol guidance so shipped bootstrap templates match the canonical workflow requirements.
- Centralized `trace_event` guidance and updated shipped templates to reference the canonical observability requirements.
- Updated template observability pointers/references to align with the current spec module locations.

## [0.23.2] - 2026-03-01

### Changed
- Gate 3: updated the dispute-summary escalation artifact guidance and references to match the canonical dispute-summary artifact.

## [0.23.1] - 2026-03-01

### Changed
- Canonicalized capability→tool mapping references (canonical tool IDs) and updated spec pointers to that canonical location.
- Aligned prompt versioning guidance to treat tool changes in terms of canonical tool IDs.
- Aligned shipped templates and agent prompts with the updated pointers and gate-related requirements.

## [0.23.0] - 2026-03-01

### Changed
- Aligned shipped templates with updated spec modules (protocol + pointers).
- Observability: clarified required `trace_event` keys and added a synthetic-span fallback when a subagent output is missing `trace_event` or contains an invalid `trace_event`.
- Standardized `ESCALATED` semantics and cleaned up related vocabulary to avoid overload.

## [0.22.1] - 2026-02-28

### Changed
- Moved the workspace repo-context bootstrapper to bootstrap templates.
- Removed the workspace repo-context bootstrapper from project templates.
- `bootstrap-orchestrator` now routes the workspace repo-context bootstrapper.

## [0.22.0] - 2026-02-28

### Added
- Shipped project-template agent prompts under `framework/templates/repo-files-templates/root/.github/agents/`:
  - `project-orchestrator.agent.md`
  - `project-repo-context-bootstrap.agent.md` + `project-repo-context-bootstrap-critic.agent.md`
  - Role templates: `project-architect*`, `project-backend-*`, `project-frontend-*`, `project-devops-*`, `project-security*`, `project-documentation-*`, `project-qa-*`
- Orchestrator wiring for the new project-template agents.

## [0.21.27] - 2026-02-28

### Changed
- Added a canonical plan-output formatting rule.

### Fixed
- Aligned shipped templates with the canonical plan-output formatting rule.

## [0.21.26] - 2026-02-28

### Fixed
- Resolved spec example drift against the current canonical workflow.
- Resolved shipped template drift against the current canonical workflow.

## [0.21.25] - 2026-02-28

### Changed
- Canonical trace policy: traces `.agents/traces/*.jsonl` are never committed (local-only); removed "modes".
- WARNING semantics are strict: any WARNING ⇒ `REQUEST_CHANGES` (no approve-with-warning).

## [0.21.24] - 2026-02-28

### Fixed
- Canonicalized trace ignore semantics: ignore `.agents/traces/*.jsonl` (local-only; not committed) while allowing `.agents/traces/README.md` to be committed.

## [0.21.23] - 2026-02-27

### Fixed
- Clarified orchestrator re-entry semantics for executor↔critic iteration loops (avoid ambiguous cap resets).
- Aligned shipped observability templates with the canonical observability workflow and required trace/report fields.

### Changed
- Normalized `max_iterations: 5` across spec modules and shipped templates (consistency sweep).

## [0.21.22] - 2026-02-27

### Changed
- Raised the executor↔critic iteration cap to `max_iterations: 5` across spec modules and shipped templates.

## [0.21.21] - 2026-02-27

### Changed
- Tightened orchestrator chat output protocol to explicitly include critic calls (subagent name + minimal context) and aligned shipped templates accordingly.

## [0.21.20] - 2026-02-27

### Changed
- Improved clarity of the Adoption Roadmap playbooks.

## [0.21.19] - 2026-02-27

### Changed
- Made the orchestrator chat output protocol (Group 1 orchestrators) a MUST-level requirement: plan + pre-subagent invocation context + post-subagent result summary.
- Updated the Group 2 bootstrap orchestrator template to implement the same chat output protocol.

## [0.21.18] - 2026-02-27

### Fixed
- AWESOME-COPILOT gate report template now matches canonical required-fields formatting (deterministic enforcement).

## [0.21.17] - 2026-02-27

### Changed
- Made awesome-copilot consultation mandatory and auditable for any changes to `.github/agents/**` or `.github/prompts/**` (gate report updated; “no external sources” is not a valid substitute).
- Tightened executor/critic rubrics so missing or invalid consultation evidence is a deterministic BLOCKER.
- Updated bootstrap agent templates to explicitly follow Adoption Roadmap playbooks (install/upgrade/remove).
- Updated the shipped `AGENTS.md` template to mention two-tier routing for operations.

## [0.21.16] - 2026-02-27

### Added
- Two-tier bootstrap workflow assets (install/upgrade) and related bootstrap templates to make the recommended adoption path copy/pasteable.

### Changed
- Rewrote the adoption guidance to reflect the two-tier bootstrap workflow and to make the install vs. upgrade responsibilities explicit.
- Strengthened `awesome-copilot` usage as an explicit gate in the workflow (license verification + provenance requirements are treated as enforceable checks when sourcing external examples).

## [0.21.15] - 2026-02-27

### Fixed
- Scoped the `## Provenance` MUST requirement to Markdown-based artifacts and defined an adjacent `.provenance.md` file convention for non-Markdown artifacts.

### Changed
- Clarified provenance placement guidance to explicitly include `.prompt.md`.

## [0.21.14] - 2026-02-27

### Added
- Appendix A1 policy for using `awesome-copilot` as an external prompt/example source, including per-material license verification and standardized provenance placement.
- New skill package: `.agents/skills/awesome-copilot-navigator/SKILL.md`.

## [0.21.13] - 2026-02-27

### Changed
- Moved the umbrella file’s setup/upgrade guidance into a dedicated operations module.

### Added
- New module: `spec/07-framework-operations.md` (Install / Upgrade / Remove), including minimal removal and full cleanup modes.

## [0.21.12] - 2026-02-27

### Fixed
- Aligned hotfix Phase 1 iteration cap with `max_iterations: 3`.
- Clarified docs+feature wording so Phase 0 roles don’t contradict Phase 6 documentation work.
- Fixed broken Markdown code fences in the golden-tests section.
- Aligned orchestrator golden-test examples for `docs-only` and `docs+feature` with the shortened pipeline paths (Phase 6 and Phase 0+6).


## [0.21.11] - 2026-02-26

### Fixed
- Clarified the canonical location of `PROJECT.md` (AgentConfig repo root) and updated Quick Start guidance/links.
- Clarified `span_id` uniqueness and ordering rules for JSONL traces.
- Aligned escalation/iteration wording to `max_iterations: 3` across spec modules.
- Marked the GitHub Actions critic-review workflow example as pseudocode/non-authoritative.

## [0.21.10] - 2026-02-26

### Fixed
- Normalized VS Code Copilot tool names in spec examples and templates.

## [0.21.9] - 2026-02-26

### Changed
- Removed the superseded AutoGen + FastMCP ADR and all references to it from the spec/docs/templates.

## [0.21.8] - 2026-02-26

### Changed
- Removed `agent-evals` SKILL entirely (not shipped in repo root or templates).

## [0.21.7] - 2026-02-26

### Changed
- Deleted the root `agent-evals` SKILL from this repo; eval guidance no longer ships as a SKILL.
- Updated Appendix A1 to remove `agent-evals` SKILL references.

## [0.21.6] - 2026-02-26

### Changed
- Removed spec version suffixes from appendix headers (appendices now link to the umbrella spec file without duplicating the version).

## [0.21.5] - 2026-02-26

### Changed
- Clarified that evals/golden tests are optional because they typically require access to an external LLM provider API supported by promptfoo.

## [0.21.4] - 2026-02-26

### Changed
- Made evals/golden tests optional-by-choice: projects MAY adopt them; if adopted, they MUST pass before merging agent prompt / rubric changes.

## [0.21.3] - 2026-02-26

### Changed
- Added CI enforcement (repo governance) to require a spec version bump + changelog update whenever `framework/` changes.

## [0.21.2] - 2026-02-26

### Changed
- Updated the template `.agents/evals/README.md` to include concrete promptfoo run commands.
- Updated promptfoo guidance in `framework/spec/05-prompt-versioning.md` to document multi-config (`-c`/glob) runs.

## [0.21.1] - 2026-02-26

### Added
- `framework/CHANGELOG.md` to ship spec release notes alongside the spec modules.

## [0.21.0] - 2026-02-24

### Added
- Baseline spec release (see repository history for details).
