# Framework Audit — Stage 1 (Scope & Sanity-Check)

Date: 2026-03-03

Goal: validate already-reported issues (at minimum the “§0.5 cross-link” problem) and define a clear, reproducible audit scope + methodology for checking **all** canonical files under `framework/` for logical consistency and internal contradictions.

Constraints (this stage):
- This Stage 1 deliverable is **report-only**.
- No edits to `framework/**`, any `.github/agents/**`, or any mirror directories.

---

## 1) Confirmed findings so far

### Finding F1 — Incorrect target file for “§0.5” cross-reference

- Severity: **WARNING**
- Location: `framework/spec/00-infrastructure.md` → heading **“0.3.1 Required contents of the global AGENTS.md”** (sample `AGENTS.md` snippet) → subheading **“Branching Strategy: GitFlow”**.
- What’s wrong:
  - The sample `AGENTS.md` text says:
    - `"[See 00-multi-agent-development-spec.md §0.5 for detailed rules]"`
  - However, the umbrella doc `framework/00-multi-agent-development-spec.md` is intentionally a small index and does **not** enumerate `§0.5` as a subsection; it points readers to modules under `framework/spec/`.
  - The detailed GitFlow/SemVer rules actually exist as `## 0.5 GitFlow + SemVer — detailed rules` **inside the same file** `framework/spec/00-infrastructure.md`.
- Why it matters:
  - Readers (and automation/agents) following this instruction will navigate to the umbrella spec and fail to find the referenced subsection, increasing the chance of inconsistent branching/versioning practice.
  - This is especially high-impact because it appears in “required contents” for a global `AGENTS.md` (i.e., it is intended for frequent copying).
- Recommended fix (for Stage 2/3):
  - Replace the bracket note with a reference that actually resolves:
    - simplest: `"[See §0.5 below for detailed rules]"` (if the snippet is meant to be read in the context of `00-infrastructure.md`)
    - or explicit: `"[See spec/00-infrastructure.md §0.5 for detailed rules]"`
    - ideally as a real link: `"[See §0.5 GitFlow + SemVer — detailed rules](#05-gitflow--semver--detailed-rules)"` (anchor text may need verification)

Evidence (stable references):

- `framework/spec/00-infrastructure.md` → heading **“0.3.1 Required contents of the global AGENTS.md”** (sample `AGENTS.md`)
  - Quote:
    - `"## Branching Strategy: GitFlow"`
    - `"[See 00-multi-agent-development-spec.md §0.5 for detailed rules]"`

- `framework/spec/00-infrastructure.md` → heading **“0.5 GitFlow + SemVer — detailed rules”**
  - Quote: `"## 0.5 GitFlow + SemVer — detailed rules"`

- `framework/00-multi-agent-development-spec.md` → heading **“Spec modules”**
  - Quote: `"§0 Infrastructure → spec/00-infrastructure.md"`

---

### Finding F2 — Ambiguous “→ §0.5” reference (no file/module specified)

- Severity: **SUGGESTION**
- Location: `framework/spec/04-observability.md` → heading **“4.4 DORA AI Capabilities Model (2025)”**, table row **“Strong version control practices”**.
- What’s wrong:
  - The table uses `"→ §0.5"` without identifying which document the section belongs to.
  - In this repo, `§0.5` exists in `framework/spec/00-infrastructure.md`, not in the umbrella `framework/00-multi-agent-development-spec.md`.
- Why it matters:
  - This is a navigational footgun during onboarding and audits, and it increases the chance that the reader assumes a different `§0.5` (or searches the wrong file).
- Recommended fix (for Stage 2/3):
  - Make cross-module references explicit and linkable, e.g. `"→ spec/00-infrastructure.md §0.5"` or a Markdown link to the exact section.

Evidence (stable references):

- `framework/spec/04-observability.md` → heading **“4.4 DORA AI Capabilities Model (2025)”**
  - Quote (table row): `"| **Strong version control practices** | Feature branches, GitFlow, ADRs committed → §0.5 |"`

---

## 2) Audit scope

### In scope (canonical)

Audit target is **all canonical content under `framework/`**, including:

1) Umbrella spec entrypoint
- `framework/00-multi-agent-development-spec.md`

2) Spec modules (normative + guidance)
- `framework/spec/**` (including `appendices/**` and `03-rubrics/**`)

3) Shipped templates
- `framework/templates/**` (both template READMEs and template `root/` trees)
  - Includes template agent files that ship to downstream repos (these are still “framework artifacts” and must remain logically consistent with the spec modules).

4) Shipped tooling
- `framework/tools/**` (e.g., bootstrap scripts)

### Out of scope / treated as mirrors

- `Test/Delpoyment/**` (note the “Delpoyment” spelling): treated as a **mirror / test fixture** unless explicitly promoted to canonical.
  - Rationale: it appears to duplicate `framework/**` content and would otherwise double-count findings. If it is meant to be authoritative, that should be clarified before Stage 2.

### Out of scope (non-framework)

- Repo-level meta docs and agent system files not under `framework/` (e.g., `.agents/**`, root `AGENTS.md`, `PROJECT.md`, `.github/**`) unless a Stage explicitly expands scope.

---

## 3) Audit methodology (how we will cover “all files”)

This methodology is designed to be **systematic, reproducible, and coverage-oriented**.

### 3.1 Inventory-first pass (complete coverage)

1) Enumerate all files under `framework/` by category:
- Umbrella: `framework/00-multi-agent-development-spec.md`
- Modules: `framework/spec/**`
- Templates: `framework/templates/**`
- Tools: `framework/tools/**`

2) Build a “reference map” of:
- the canonical location for each major topic (routing, gates, severities, trace format, etc.)
- any statements declaring “single normative source” (e.g., observability sections that claim canonicality)

### 3.2 Systematic scan patterns (search-first)

For the entire `framework/` tree, run targeted searches for:

- **Section references**: `§`, `→ §`, `"See .* §"`, `"Section"`, `"Appendix"`
  - Verify every reference resolves to a unique target (correct module + existing heading).

- **Markdown links**: `](...)`, including:
  - intra-file anchors: `#...`
  - relative module links: `../`, `../../`
  - template-relative links (must resolve from within template `root/` context).

- **Normative keywords**: `MUST`, `MUST NOT`, `SHOULD`, `MAY`, `single normative source`, `canonical`
  - Identify conflicts where two different files both claim canonical authority for the same requirement.

- **Enums / invariants / numerals**:
  - severities: `BLOCKER`, `WARNING`, `SUGGESTION`
  - gates: `Gate 1`, `Gate 2`, `Gate 3`
  - iteration limits, routing labels, file paths and required filenames
  - any explicitly-versioned identifiers (spec version strings, trace schema keys)

### 3.3 Spot-check reads (contradiction hunting)

After the scan, perform focused reads on:

- each file that introduces an enum, protocol, or “must” rule
- any file with high cross-link density (likely to contain drift)
- any template file that re-states requirements from a module (to ensure it’s not stale)

For each candidate contradiction, record:
- both locations (paths + headings)
- the conflicting statements side-by-side (short quotes)
- a recommended resolution strategy (choose a single canonical source; convert the other to a pointer)

### 3.4 Reporting discipline

All findings will be reported with:
- Severity: BLOCKER / WARNING / SUGGESTION
- Location: path + heading
- What’s wrong, why it matters, recommended fix
- Minimal quoted snippet(s) only

---

## 4) Coverage checklist for next stages

Use this checklist to ensure Stage 2+ covers “all files” and the right contradiction classes.

### Links and references

- [ ] Every `§X.Y` reference names the correct module (or links directly)
- [ ] Every Markdown link resolves (relative paths correct for file location)
- [ ] Every anchor link (`#...`) matches a real heading (watch for heading renames)
- [ ] No references point to the umbrella file for module-only subsections (like the §0.5 case)

### Enums and invariants

- [ ] Severity set is consistent everywhere: `BLOCKER/WARNING/SUGGESTION` (no alternate spellings)
- [ ] Gate names/numbers are consistent (Gate 1–3 definitions match across modules)
- [ ] Routing/fast-track labels are consistent across spec + templates
- [ ] Trace schema keys and required fields are not duplicated with drift

### Canonical vs duplicated content

- [ ] Any “single normative source” claim is respected (other modules point to it, do not restate)
- [ ] Templates do not restate requirements that drift from modules
- [ ] Umbrella file remains index-like; detailed rules live in modules

### Templates and tooling

- [ ] Template `root/` relative links work when copied into a downstream repo
- [ ] Bootstrap scripts reference paths that exist in the shipped template layout
- [ ] Any instructions in templates that cite `framework/spec/**` reflect current module headings

### Mirrors / fixtures

- [ ] Mirror directories (e.g., `Test/Delpoyment/**`) are either explicitly excluded or explicitly verified for parity
- [ ] If mirrors are used for tests, define the “source of truth” direction (canonical → mirror) to prevent double maintenance

---

## 5) Verification (Stage 1 report-only; changed-files evidence)

This stage is report-only.

Verification performed (strongest reproducible evidence available in this environment):

1) Write-scope evidence
- The only write-capable operation available/used for this subtask is `apply_patch`.
- In this iteration, I applied patches only to this file: `audit/framework-audit-stage1-scope.md`.
- All other tool actions were read-only (file reads/searches).

Limitations (stated explicitly):

- I cannot obtain a definitive changed-files listing here (e.g., `git diff --name-only` / `git status --porcelain`) because those commands are not available through the provided tools in this executor environment.
- Therefore, I cannot embed repository-authoritative proof of "only this file changed" beyond the write-scope constraint above.

Independent verification (recommended follow-up outside this executor):

- From repo root, run:
  - `git status --porcelain`
  - `git diff --name-only`
- Expected: only `audit/framework-audit-stage1-scope.md` appears; nothing under `framework/**` or `.github/agents/**`.

