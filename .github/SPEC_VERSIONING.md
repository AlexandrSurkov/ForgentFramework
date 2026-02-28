# Spec Versioning Policy (Repository Governance)

This repository is the canonical home of the **Multi-Agent Development Specification**.

This document governs how **this repository** versions and releases changes to the spec.
It is intentionally **not part of the spec** itself.

---

## Source of truth

- The canonical spec version is the **umbrella metadata line** in [framework/00-multi-agent-development-spec.md](../framework/00-multi-agent-development-spec.md).
   - CI extracts the version from the first line that matches:
      - `> **Version:** X.Y.Z · **Updated:** YYYY-MM-DD`
- All modules under `framework/spec/` inherit that umbrella version.

---

## Semantic Versioning rules

We use SemVer: `MAJOR.MINOR.PATCH`.

### MAJOR (breaking)

Bump MAJOR when projects set up with the previous version are likely to break or become non-compliant without an upgrade.

Examples:

- Required paths change (e.g., canonical location of session files).
- Required schemas change (e.g., trace JSONL fields, TASK_CONTEXT header fields).
- Protocol semantics change (iteration limits, verdict meaning, gate logic).

### MINOR (additive)

Bump MINOR for backwards-compatible additions.

Examples:

- New optional module or template.
- New rubric rule that is guidance-only / WARNING-by-default.

### PATCH (fix/clarification)

Bump PATCH for corrections that do not change normative behaviour.

Examples:

- Typos, broken links, small clarifications.
- Better phrasing without new obligations.

---

## Change procedure

When changing any files under `framework/`:

1. Update `framework/CHANGELOG.md` with a release header for the new version.
   - **Required by CI:** a header line starting with `## [X.Y.Z]` (commonly `## [X.Y.Z] - YYYY-MM-DD`).
   - Note: keeping an `[Unreleased]` section is fine, but it does **not** satisfy this check by itself.
2. Decide the version bump using the rules above.
3. Update the umbrella metadata line in `framework/00-multi-agent-development-spec.md`.
   - **Required by CI:** bump `X.Y.Z` in `> **Version:** X.Y.Z · **Updated:** YYYY-MM-DD`
4. Update the pinned references in this repo.
   - **Required by CI:** `PROJECT.md` must contain `vX.Y.Z`.
   - **Required by CI:** `AGENTS.md` must contain `(vX.Y.Z)`.

---

## Enforcement

This policy is enforced by CI.

- Workflow: `.github/workflows/spec-versioning.yml`
- Script: `.github/scripts/check_spec_version_bump.sh`

If a PR changes anything under `framework/` but does not bump the umbrella spec version line, add the corresponding `framework/CHANGELOG.md` release header, and update the pinned references, the workflow fails.
