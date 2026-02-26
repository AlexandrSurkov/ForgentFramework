# Changelog — Multi-Agent Development Specification

All notable changes to the **Multi-Agent Development Specification** (the `framework/` package copied into downstream AgentConfig repos) are documented here.

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

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
