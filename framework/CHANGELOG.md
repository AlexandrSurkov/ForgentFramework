# Changelog — Multi-Agent Development Specification

All notable changes to the **Multi-Agent Development Specification** (the `framework/` package copied into downstream AgentConfig repos) are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
