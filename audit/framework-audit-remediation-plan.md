# Framework Audit Remediation Plan (Stages 1–4)

## Purpose

This document is a **remediation plan** for addressing **all findings** in the final audit report:
- `audit/framework-audit-final.md`

It is intentionally **plan-only**: it proposes changes, identifies exact target files, and defines verification steps.
It does **not** implement any fixes.

## Scope

- In scope: remediation work that updates canonical spec content under `framework/**` and shipped template content under `framework/templates/**`.
- Out of scope (for this plan document itself): making any actual edits to `framework/**`, templates, or `.github/agents/**` in this repo.

## Pre-Flight Self-Check

- [x] **Acceptance criteria**: creates `audit/framework-audit-remediation-plan.md`.
- [x] **Coverage**: includes **every** finding from Stages 1–4 inventory and the consolidated Key Findings list (including L1/L2/L3 and T* items).
- [x] **Per-item fields**: each remediation item includes (a) audit identifier reference(s), (b) severity/priority, (c) proposed change(s), (d) exact target file path(s), (e) verification steps, (f) risks/notes.
- [x] **Execution order**: includes a recommended sequencing.
- [x] **No fixes implemented**: this file is a plan only.

## Priority Scale

- **P0 (BLOCKER)**: must be resolved before further template/spec shipping.
- **P1 (WARNING)**: should be resolved in the next release.
- **P2 (SUGGESTION)**: backlog item; resolve during cleanup sweeps.

## Suggested Execution Order

1. **Canonical invariants first (P0)**
   - Fix any contradictions or invariants in canonical modules (e.g., trace-writing responsibility).
2. **Canonical reference correctness (P1)**
   - Fix broken/ambiguous references in canonical modules (esp. `framework/spec/00-infrastructure.md`, `framework/spec/04-observability.md`).
3. **Template self-consistency (P1)**
   - Make shipped templates deterministic and portable (spec modules availability, Operations references, enum correctness).
4. **Template quality and portability (P1/P2)**
   - Fix dead skill links, README portability notes, terminology hygiene.
5. **Sweep and harden (P2)**
   - Replace remaining unqualified cross-module `§` references across canonical modules.

## Release Hygiene (Required When Editing `framework/**`)

Many remediations below require modifying canonical spec content under `framework/**`.
When that happens, apply this hygiene set in the same change series:

- Bump spec version in `framework/00-multi-agent-development-spec.md`.
- Add a release entry in `framework/CHANGELOG.md`.
- Update pinned spec version references in `PROJECT.md` and `AGENTS.md` (repo root).

## Remediation Items (All Findings)

### I1 — Trace-writing responsibility contradicted in architecture

- **Audit reference(s):** Stage 3 item `1) BLOCKER — Trace-writing responsibility contradicted in 01-architecture.md` (consolidated as `I1`)
- **Severity / priority:** BLOCKER / **P0**
- **Target file(s):**
  - `framework/spec/01-architecture.md`
  - (verification cross-check) `framework/spec/04-observability.md`
  - (secondary consistency) `framework/spec/06-adoption-roadmap.md`, `framework/spec/03-rubrics/11-dor-dod-and-adr-format.md`
- **Proposed change(s):**
  - In `framework/spec/01-architecture.md`, update the “Subtask → Output” row that currently instructs executors to “append one trace line to … `.agents/traces/<trace_id>.jsonl`”.
  - Replace with wording consistent with observability:
    - Executors **return** a `trace_event` JSON object in a `json` code block.
    - Only the orchestrator writes `.agents/traces/*.jsonl`.
  - Confirm `framework/spec/06-adoption-roadmap.md` and DoR/DoD rubrics remain consistent (they should describe orchestrator behavior, not executor file writes).
- **Verification:**
  - Text search in `framework/spec/**` for:
    - `append one trace line`
    - `.agents/traces/<trace_id>.jsonl`
    - `Only you (the orchestrator) may write`
  - Ensure all locations describe the same responsibility boundary: executor returns `trace_event`; orchestrator writes JSONL trace.
  - Manually read the updated section in `framework/spec/01-architecture.md` and confirm it matches `framework/spec/04-observability.md` §4.6 intent.
- **Risks / notes:**
  - **Normative spec change** (`framework/**`): requires release hygiene (version bump + changelog + pinned versions).
  - This change affects agent behavior; ensure templates that quote this rule remain aligned.

### F1 — Incorrect target file for “§0.5” cross-reference

- **Audit reference(s):** Stage 1 finding `Finding F1 — Incorrect target file for “§0.5” cross-reference`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - `framework/spec/00-infrastructure.md`
- **Proposed change(s):**
  - Replace the incorrect citation `[See 00-multi-agent-development-spec.md §0.5 for detailed rules]` with a correct and portable reference.
  - Preferred options:
    - Intra-file: change to `See §0.5 below.`
    - Cross-file: link to the actual section in this module (e.g., `See 00-infrastructure.md §0.5 GitFlow + SemVer — detailed rules.`)
- **Verification:**
  - Text search for `00-multi-agent-development-spec.md §0.5` under `framework/**` and confirm no remaining wrong citations.
  - Confirm the final link/ref resolves and points to the intended section.
- **Risks / notes:**
  - **Normative spec change** (`framework/**`): requires release hygiene.

### F2 — Ambiguous “→ §0.5” reference (no file/module specified)

- **Audit reference(s):** Stage 1 finding `Finding F2 — Ambiguous “→ §0.5” reference (no file/module specified)`
- **Severity / priority:** SUGGESTION / **P2**
- **Target file(s):**
  - `framework/spec/04-observability.md`
- **Proposed change(s):**
  - Replace ambiguous table references such as `→ §0.5` with explicit module references (portable outside the upstream repo).
  - Example: replace `→ §0.5` with `→ framework/spec/00-infrastructure.md §0.5` (or an equivalent stable link).
- **Verification:**
  - Text search in `framework/spec/04-observability.md` for `→ §0.5` and confirm replacement is explicit.
  - Spot-check that the linked/mentioned section exists and matches intent.
- **Risks / notes:**
  - **Normative spec change** (`framework/**`): requires release hygiene.

### L1 / Stage 2 #1 / Stage 4 T1 — Templates imply `framework/spec/**` is optional but shipped prompts depend on it

- **Audit reference(s):**
  - Consolidated Key Finding `L1`
  - Stage 2 item `1) WARNING — Template guidance implies framework/spec/** is optional, but template agents rely on it`
  - Stage 4 finding `T1 — Template guidance makes framework/spec/** sound optional, but shipped template prompts depend on it`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - Template guidance that currently implies optional modules:
    - `framework/templates/repo-files-templates/README.md`
    - `framework/templates/repo-files-templates/root/AGENTS.md`
    - `framework/templates/repo-files-templates/root/llms.txt`
  - Template artifacts that *depend* on modules (must remain consistent with guidance):
    - `framework/templates/repo-files-templates/root/.github/agents/project-orchestrator.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-architect.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-architect-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-backend-dev.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-backend-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-frontend-dev.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-frontend-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-devops-engineer.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-devops-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-security.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-security-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-qa-engineer.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-qa-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-documentation-writer.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-documentation-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-techspec-writer.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-techspec-critic.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-installer.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-upgrader.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-remover.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-critic.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-repo-context-bootstrap.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-repo-context-bootstrap-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.agents/traces/README.md`
    - `framework/templates/repo-files-templates/root/.agents/skills/awesome-copilot-navigator/SKILL.md`
- **Proposed change(s):**
  - Make the template install story deterministic by choosing **one** of these approaches:
    - **Option A (recommended): ship modules by default**
      - Update template guidance to say `framework/spec/**` is **required**, not optional, when using the shipped agent prompts.
      - Adjust template packaging/distribution instructions to include copying `framework/spec/**`.
    - **Option B: remove module dependency from shipped prompts**
      - Rewrite shipped template prompts to avoid depending on `framework/spec/**` (and keep them self-contained).
      - This is higher risk because it can duplicate canon and invite drift.
  - Ensure downstream portability: if templates are copied into a repo root, all referenced paths exist.
- **Verification:**
  - In `framework/templates/**`, run a search for `framework/spec/` and confirm:
    - Guidance explicitly requires modules **or** prompts do not reference them.
  - Manual spot-check: copy template `root/` subtree into a temporary folder and verify the referenced paths exist under the intended final structure.
- **Risks / notes:**
  - Template changes are **shipped behavior**; treat as high-impact even if not strictly “normative spec”.
  - If Option A is chosen, ensure this repo’s own bootstrap/install docs don’t contradict it.

### Stage 2 #2 — Template repo context files repeat the same “optional spec modules” wording

- **Audit reference(s):** Stage 2 item `2) WARNING — Template repo context files repeat the same “optional spec modules” wording`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - `framework/templates/repo-files-templates/root/AGENTS.md`
  - (also referenced in guidance) `framework/templates/repo-files-templates/README.md`
- **Proposed change(s):**
  - Align wording with the decision made in `L1`:
    - If modules are required: remove “optional/if you need” phrasing.
    - If modules remain optional: remove hard dependencies in template prompts.
- **Verification:**
  - Re-scan `framework/templates/repo-files-templates/root/AGENTS.md` for the phrase `copy framework/spec/** too if you need ...` and confirm it is consistent with the chosen approach.
- **Risks / notes:**
  - This finding is a subset of `L1`; keep changes consolidated to avoid drifting guidance.

### Stage 2 #3 — Template `llms.txt` repeats the same ambiguity (“if you need module-linked sections”)

- **Audit reference(s):** Stage 2 item `3) WARNING — Template llms.txt repeats the same ambiguity (“if you need module-linked sections”)`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - `framework/templates/repo-files-templates/root/llms.txt`
- **Proposed change(s):**
  - Align the `llms.txt` guidance with `L1`.
- **Verification:**
  - Search for `module-linked` in the file and confirm the final wording is deterministic and non-ambiguous.
- **Risks / notes:**
  - Subset of `L1`; keep consistent with chosen approach.

### L2 / Stage 2 #4 + #5 / Stage 4 T4 — Unqualified “Operations §7.3.3” references in prompts

- **Audit reference(s):**
  - Consolidated Key Finding `L2`
  - Stage 2 item `4) WARNING — Unqualified “Operations §7.3.3” references in template agent prompts`
  - Stage 2 item `5) WARNING — Same unqualified “Operations §…” appears in bootstrap agent prompts`
  - Stage 4 finding `T4 — Template agent prompts contain ambiguous references like “Operations §7.3.3”`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - Repo-file template prompts (Group 1 critics):
    - `framework/templates/repo-files-templates/root/.github/agents/project-techspec-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-security-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-qa-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-frontend-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-documentation-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-devops-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-backend-critic.agent.md`
    - `framework/templates/repo-files-templates/root/.github/agents/project-architect-critic.agent.md`
  - Bootstrap templates:
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-upgrader.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-critic.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-installer.agent.md`
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-remover.agent.md`
  - Canonical rubric text that also uses the same unqualified reference (keep consistent):
    - `framework/spec/03-rubrics/03-critic-rules-and-report-format.md`
- **Proposed change(s):**
  - Replace unqualified `Operations §7.3.3` with an explicit, portable reference:
    - Prefer: ``framework/spec/07-framework-operations.md §7.3.3``
    - If using links, ensure the link is correct from the file’s location.
  - For templates, prefer a path reference that remains correct after copying into a repo root (usually `framework/spec/...`).
- **Verification:**
  - Workspace text search for `Operations §7.3.3` across `framework/**` and confirm:
    - Every occurrence is now qualified with `framework/spec/07-framework-operations.md` (or equivalent explicit link).
  - Spot-check at least one template prompt to ensure the link path is correct relative to `.github/agents/**`.
- **Risks / notes:**
  - Canonical spec edits require release hygiene.
  - Template prompt edits may trigger the AWESOME-COPILOT gate in downstream repos (expected).

### L3 / Stage 2 #6 + #7 — `framework/spec/00-infrastructure.md` citations and copy/paste portability drift

- **Audit reference(s):**
  - Consolidated Key Finding `L3`
  - Stage 2 item `6) WARNING — framework/spec/00-infrastructure.md uses ambiguous “§” references and umbrella-file citations in normative prose`
  - Stage 2 item `7) WARNING — framework/spec/00-infrastructure.md includes a copy-pastable reference that will be wrong in real .agent.md file locations`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - `framework/spec/00-infrastructure.md`
- **Proposed change(s):**
  - Replace umbrella-file citations like `00-multi-agent-development-spec.md §...` with explicit module targets.
  - Replace ambiguous references like `see observability §4` with explicit `framework/spec/04-observability.md §4`.
  - In copy/paste blocks intended to be moved into `.github/agents/**` (or other locations), ensure referenced paths are correct from the destination context:
    - Prefer absolute-from-repo-root paths in prose (e.g., `framework/spec/04-observability.md`).
    - Or explicitly instruct the user to adjust relative links after pasting.
  - Specific high-confidence replacements (based on current occurrences):
    - `00-multi-agent-development-spec.md §0.5` → `00-infrastructure.md §0.5` (or `See §0.5 below`).
    - `00-multi-agent-development-spec.md §1.2` (model selection policy) → `framework/spec/01-architecture.md §1.2`.
    - Tiers definition references → `framework/spec/06-adoption-roadmap.md` (where T1/T2/T3 is currently defined).
    - “pipeline phases” references → `framework/spec/01-architecture.md` §1.3.
    - Critic/executor rules references → `framework/spec/03-rubrics/02-executor-rules.md` and `framework/spec/03-rubrics/03-critic-rules-and-report-format.md`.
- **Verification:**
  - Search within `framework/spec/00-infrastructure.md` for `00-multi-agent-development-spec.md §` and confirm each one is either:
    - removed (intra-file reference), or
    - replaced with a module path under `framework/spec/**`.
  - Search for `see observability §` / `see DoD §` and confirm module qualification.
  - Spot-check copy/paste blocks by evaluating links as if pasted into `.github/agents/<name>.agent.md`.
- **Risks / notes:**
  - **Normative spec change** (`framework/**`): requires release hygiene.
  - This is a high-impact portability fix: prioritize correctness over minimal diff.

### Stage 2 #8 — Sweep: unqualified “see §X.Y” cross-module references in canonical modules

- **Audit reference(s):** Stage 2 item `8) SUGGESTION — Several canonical modules use unqualified “see §X.Y” cross-module references`
- **Severity / priority:** SUGGESTION / **P2**
- **Target file(s):** (current known occurrences; re-run search to confirm full set)
  - `framework/spec/04-observability.md` (multiple `→ §...` references)
  - `framework/spec/02-sessions-and-memory.md` (e.g., `see §4.6.1`)
  - `framework/spec/03-rubrics/11-dor-dod-and-adr-format.md` (e.g., `see §0.6`)
  - `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` (e.g., `see §0.1 repository structure`)
  - `framework/spec/01-architecture.md` (e.g., `template → §2.3`, `see §3.3`)
  - `framework/spec/00-infrastructure.md` (multiple `see §...` occurrences)
- **Proposed change(s):**
  - Establish a consistent style rule for cross-module references in canonical docs:
    - If intra-file: `see §X.Y` is allowed.
    - If cross-file: MUST include the module file path (and optionally a link).
  - Run a targeted sweep:
    - Search pattern: `see §` and `→ §` across `framework/spec/**`.
    - For each match, decide intra-file vs cross-file, then qualify cross-file references.
- **Verification:**
  - Ensure no remaining cross-module references omit the target file.
  - Manual spot-check: pick 5 random updated references and confirm they resolve unambiguously.
- **Risks / notes:**
  - Likely broad edits across canonical modules; plan for a focused “reference hygiene” release.
  - **Normative spec change** (most of these are in `framework/**`): requires release hygiene.

### T2 — Bootstrap orchestrator template uses non-canonical `fast_track` value (`tooling-only`)

- **Audit reference(s):** Stage 4 finding `T2 — Bootstrap orchestrator template references a non-canonical fast_track value (tooling-only)`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`
  - (canonical reference) `framework/spec/01-architecture.md` (`fast_track` enum)
- **Proposed change(s):**
  - Replace the non-canonical value `tooling-only` with one of the canonical enum values from `framework/spec/01-architecture.md`.
  - Suggested default for bootstrap operations (confirm intended semantics):
    - Use `fast_track: agent-prompt-update` when the operation changes `.github/agents/**` or `.github/prompts/**`.
    - Use `fast_track: infra` for purely config/IaC-like operations (if applicable).
  - Ensure any downstream bootstrap playbook references remain consistent.
- **Verification:**
  - Text search in templates for `tooling-only` and confirm it is eliminated.
  - Manual read: confirm the chosen replacement is present in the canonical enum table in `framework/spec/01-architecture.md`.
- **Risks / notes:**
  - Template behavior change; confirm that bootstrap workflows that do not fit `agent-prompt-update` still have a canonical classification.
  - If none of the existing canonical values are appropriate, adding a new enum value would be a **normative spec change** (requires release hygiene and wider review).

### T5 — Shipped template skill references other skills that are not shipped

- **Audit reference(s):** Stage 4 finding `T5 — Shipped template skill references other skills that are not shipped in the template tree`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - `framework/templates/repo-files-templates/root/.agents/skills/awesome-copilot-navigator/SKILL.md`
  - (template tree where missing skills would live)
    - `framework/templates/repo-files-templates/root/.agents/skills/agent-file-standards/SKILL.md` (missing today)
    - `framework/templates/repo-files-templates/root/.agents/skills/ai-security/SKILL.md` (missing today)
- **Proposed change(s):**
  - Choose one approach:
    - **Option A (recommended): ship the referenced skills** into the template skill tree so the links resolve in downstream repos.
    - **Option B:** rewrite the references in the shipped `awesome-copilot-navigator` skill to point to canonical spec locations under `framework/spec/appendices/**` (only works if `framework/spec/**` is required per `L1`).
    - **Option C:** mark references as conditional: “If present, load …” and remove them from “References” if not shipped.
- **Verification:**
  - Validate that all referenced paths under `.agents/skills/**` exist in the shipped template tree.
  - Quick link check: open each referenced skill path from the template skill file.
- **Risks / notes:**
  - If you ship additional skills, ensure they are consistent with the canonical versions (avoid drift).

### T6 — Potential conflict: “no writes before APPLY” vs orchestrator `.agents/**` writes

- **Audit reference(s):** Stage 4 finding `T6 — Potential conflict: bootstrap “no file writes before APPLY” vs orchestrator trace/session writes`
- **Severity / priority:** WARNING / **P1**
- **Target file(s):**
  - Canonical operations safety gate:
    - `framework/spec/07-framework-operations.md` (§7.2)
  - Canonical observability protocol:
    - `framework/spec/04-observability.md` (§4.6)
  - Bootstrap orchestrator prompt (documented exception):
    - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`
- **Proposed change(s):**
  - Clarify precedence and allowed exceptions in `framework/spec/07-framework-operations.md`:
    - During Dry-run/Confirm (pre-`APPLY`), bootstrap agents MUST NOT write **repo artifacts**, but MAY write local-only runtime artifacts under:
      - `.agents/session/**`
      - `.agents/traces/*.jsonl`
  - Ensure `framework/spec/04-observability.md` uses compatible wording (“no file writes” for executors should not conflict with orchestrator’s allowed local-only artifacts).
  - Ensure bootstrap templates reflect the clarified rule (they already mention an exception; align with canonical).
- **Verification:**
  - Manual read: `framework/spec/07-framework-operations.md` §7.2 should explicitly allow local-only `.agents/**` artifacts prior to `APPLY`.
  - Confirm there is no longer a plain-text contradiction between operations and observability.
- **Risks / notes:**
  - **Normative spec change** (`framework/**`): requires release hygiene.
  - Be explicit that the exception is limited to gitignored local-only artifacts, not arbitrary file writes.

### Stage 3 #2 / Stage 4 T3 — Terminology drift: `APPROVED`/`APPROVE` inconsistent with canonical vocabulary

- **Audit reference(s):**
  - Stage 3 item `2) SUGGESTION — Potential terminology drift: APPROVED used in bootstrap orchestrator prompt`
  - Stage 4 finding `T3 — Template prompts use APPROVED/APPROVE inconsistently with canonical terminology guidance`
- **Severity / priority:** SUGGESTION / **P2**
- **Target file(s):**
  - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md`
  - (canonical terminology source) `framework/spec/01-architecture.md` (§1.3.9 “Canonical pipeline vocabulary”)
- **Proposed change(s):**
  - Replace the uppercase token usage `apply is APPROVED` with terminology aligned to canonical meanings:
    - Use **plain-English** “approved” only for human PR approvals.
    - Use `APPROVE` only for critic verdicts.
    - For the safety gate, refer to the user’s explicit `APPLY` confirmation (not `APPROVED`).
  - Re-scan templates for misuse of `APPROVED` and correct as needed.
- **Verification:**
  - Search in templates for `\bAPPROVED\b` and confirm no incorrect token usage remains.
  - Spot-check updated wording aligns with `framework/spec/01-architecture.md` §1.3.9.
- **Risks / notes:**
  - Mostly terminology/documentation; low functional risk but improves deterministic interpretation.

### Stage 3 #3 — Template file name collides with canonical spec entrypoint but contains placeholder content

- **Audit reference(s):** Stage 3 item `3) SUGGESTION — Template file name collides with canonical spec entrypoint but contains placeholder content`
- **Severity / priority:** SUGGESTION / **P2**
- **Target file(s):**
  - `framework/templates/repo-files-templates/root/framework/00-multi-agent-development-spec.md`
  - (supporting guidance) `framework/templates/repo-files-templates/README.md`
  - (supporting repo context templates) `framework/templates/repo-files-templates/root/AGENTS.md`, `framework/templates/repo-files-templates/root/llms.txt`
- **Proposed change(s):**
  - Align with the decision made for `L1`:
    - If templates require modules, consider shipping a **real** umbrella spec file instead of a placeholder stub.
    - If keeping a stub, make it unambiguously a placeholder:
      - Include clear “TEMPLATE / PLACEHOLDER” language at top.
      - Include a minimal checklist for what must be copied (umbrella + modules).
  - Avoid user confusion between canonical spec and template stub.
- **Verification:**
  - Manual read: ensure the template spec file cannot be mistaken for the actual canonical spec.
  - Confirm template guidance (`README.md`, `AGENTS.md`, `llms.txt`) is consistent.
- **Risks / notes:**
  - Primarily a usability/clarity issue; impacts downstream adoption quality.

### Stage 4 T7 — Template README uses upstream-framework paths that won’t exist in downstream repos

- **Audit reference(s):** Stage 4 finding `T7 — Template README uses upstream-framework paths that won’t exist in downstream repos`
- **Severity / priority:** SUGGESTION / **P2**
- **Target file(s):**
  - `framework/templates/bootstrap-agents-templates/README.md`
  - (potentially) `framework/templates/repo-files-templates/README.md`
- **Proposed change(s):**
  - Rewrite “How to use” sections to avoid assuming the user has the upstream repo layout.
  - Prefer instructions that refer to paths **inside the template package itself**, e.g.:
    - “Copy the contents of `repo-files-templates/root/` into your repo root”
    - “Copy the contents of `bootstrap-agents-templates/root/` into your repo root”
  - If keeping upstream-relative paths, add a clarifying sentence: “Paths below are relative to the upstream ForgentFramework repo; adjust when consuming the template bundle.”
- **Verification:**
  - Manual read: ensure instructions remain clear when the templates are consumed as a zip/package without the full upstream repository structure.
- **Risks / notes:**
  - Doc-only change; low risk.

## Coverage Checklist (Audit Inventory → Planned Item)

- [x] Stage 1: F1 → **F1**
- [x] Stage 1: F2 → **F2**
- [x] Stage 2: #1 → **L1**
- [x] Stage 2: #2 → **Stage 2 #2** (aligned with **L1**)
- [x] Stage 2: #3 → **Stage 2 #3** (aligned with **L1**)
- [x] Stage 2: #4 → **L2**
- [x] Stage 2: #5 → **L2**
- [x] Stage 2: #6 → **L3**
- [x] Stage 2: #7 → **L3**
- [x] Stage 2: #8 → **Stage 2 #8**
- [x] Stage 3: #1 → **I1**
- [x] Stage 3: #2 → **Stage 3 #2 / T3**
- [x] Stage 3: #3 → **Stage 3 #3**
- [x] Stage 4: T1 → **L1**
- [x] Stage 4: T2 → **T2**
- [x] Stage 4: T3 → **Stage 3 #2 / T3**
- [x] Stage 4: T4 → **L2**
- [x] Stage 4: T5 → **T5**
- [x] Stage 4: T6 → **T6**
- [x] Stage 4: T7 → **T7**

## Trace

```json
{
  "trace_event": {
    "agent": "GitHub Copilot",
    "operation": "execute",
    "subtask": 1,
    "iteration": 1
  }
}
```
