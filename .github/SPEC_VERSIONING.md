# Spec Versioning Policy (Repository Governance)

This repository is the canonical home of the **Multi-Agent Development Specification**.

This document governs how **this repository** versions and releases changes to the spec.
It is intentionally **not part of the spec** itself.

---

## Source of truth

- The canonical spec version is the `Version:` header in [framework/00-multi-agent-development-spec.md](../framework/00-multi-agent-development-spec.md).
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

1. Add an entry under `[Unreleased]` in `framework/CHANGELOG.md`.
2. Decide the version bump using the rules above.
3. Update the umbrella header in `framework/00-multi-agent-development-spec.md`:
   - `Version: X.Y.Z`
   - `Updated: YYYY-MM-DD`
4. If the change impacts this repo’s own configuration, align `PROJECT.md` (it pins a spec version for this repository).

---

## Enforcement

This policy is enforced by CI.

- Workflow: `.github/workflows/spec-versioning.yml`
- Script: `.github/scripts/check_spec_version_bump.sh`

If a PR changes anything under `framework/` but does not bump the umbrella spec `Version:` header and update `framework/CHANGELOG.md`, the workflow fails.
