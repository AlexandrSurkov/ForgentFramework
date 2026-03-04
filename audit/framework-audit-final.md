# Framework Audit — Final Consolidated Report (Stages 1–4)

Date: 2026-03-04

This report consolidates findings from:
- [framework-audit-stage1-scope.md](framework-audit-stage1-scope.md)
- [framework-audit-stage2-links.md](framework-audit-stage2-links.md)
- [framework-audit-stage3-invariants.md](framework-audit-stage3-invariants.md)
- [framework-audit-stage4-templates.md](framework-audit-stage4-templates.md)

## What Was Audited

- In scope: canonical content under `framework/**` (umbrella spec, spec modules, templates, tools), as defined in Stage 1 “Audit scope”.
- Out of scope: `Test/Delpoyment/**` treated as a mirror/fixture (explicitly excluded in Stages 1–2).
- Methodology: read-only audit using inventory + targeted searches (links, §-references, normative keywords, invariant enums) and spot-check reads of high-traffic canonical modules and templates, per Stage 1 “Audit methodology” and Stage 2/3 “How coverage was ensured”.
- Note (Stage 2 link interpretation): links inside fenced code blocks are often examples/templates (not “broken links” by default), but they were still audited for misleading copy/paste portability when those blocks are presented as copy-ready.

## Executive Summary

The dominant risk theme is **reference and portability drift**:
- Several documents (including templates) contain **ambiguous or incorrect cross-references**, which becomes high-impact when templates are copied into downstream repos.
- One **direct contradiction** exists between architecture and observability modules about who may write trace files.
- Bootstrap/template prompts contain a few **enum/terminology mismatches** (notably `fast_track` values) that can break deterministic routing.

## Key Findings (Consolidated)

This section is a **prioritized subset** (highest impact / most actionable).

For a complete consolidation across Stages 1–4 (all findings, with severities), see **“All Findings Inventory (Complete Stage 1–4 Rollup)”** below.

| ID | Severity | Impact | Recommended Fix (Summary) | Evidence (Stage) |
|---|---|---|---|---|
| F1 | WARNING | Readers/agents follow a reference that cannot resolve in the umbrella spec; increases drift in branching/versioning rules. | Fix §0.5 cross-reference to point to the correct module/section (or “§0.5 below” if intra-file). | Stage 1 “Finding F1 — Incorrect target file for “§0.5” cross-reference” |
| F2 | SUGGESTION | “§” references without a file/module are non-portable; readers guess the wrong target. | Make cross-module references explicit (module + § or stable link). | Stage 1 “Finding F2 — Ambiguous “→ §0.5” reference (no file/module specified)” |
| L1 | WARNING | Templates imply `framework/spec/**` is optional but shipped prompts depend on it; downstream repos get dead links and missing canon. | Make template guidance deterministic: either require `framework/spec/**` when using shipped prompts or include modules in the template set. | Stage 2 “1) WARNING — Template guidance implies `framework/spec/**` is optional, but template agents rely on it” and Stage 4 “Finding T1 — Template guidance makes `framework/spec/**` sound optional, but shipped template prompts depend on it” |
| L2 | WARNING | Deterministic gate text references “Operations §7.3.3” without naming the canonical file; ambiguous in downstream repos. | Replace with an explicit reference to `framework/spec/07-framework-operations.md §7.3.3` (ideally linkable). | Stage 2 “4) WARNING — Unqualified “Operations §7.3.3” references in template agent prompts” and Stage 4 “Finding T4 — Template agent prompts contain ambiguous references like “Operations §7.3.3”” |
| L3 | WARNING | `framework/spec/00-infrastructure.md` includes umbrella-spec citations and relative module links inside copy/paste blocks; readers follow the wrong source of truth and pasted snippets break in real `.github/agents/**` locations. | Replace umbrella-file `00-multi-agent-development-spec.md §…` citations with explicit module targets (e.g., `spec/01-architecture.md §1.2`, `spec/06-adoption-roadmap.md §6.4`) and rewrite copy/paste snippets to use paths that are correct from the destination directory (or explicitly instruct users to adjust links post-paste). | Verified directly in `framework/spec/00-infrastructure.md`; aligns with Stage 2 findings “6)” and “7)”. |
| I1 | BLOCKER | Violates least-privilege boundary: architecture text implies executors append to `.agents/traces/**`, contradicting observability’s orchestrator-only rule. | Align `framework/spec/01-architecture.md` “Subtask → Output” with `framework/spec/04-observability.md`: executors return `trace_event`; only orchestrator writes trace files. | Stage 3 “1) BLOCKER — Trace-writing responsibility contradicted in `01-architecture.md`” |
| T2 | WARNING | Bootstrap template suggests `fast_track = tooling-only`, which is not in the canonical enum; breaks consistent routing. | Replace `tooling-only` with a valid canonical `fast_track` value after confirming intended semantics. | Stage 4 “Finding T2 — Bootstrap orchestrator template references a non-canonical `fast_track` value (`tooling-only`)” |
| T5 | WARNING | Shipped template skill links to non-shipped skills; dead links reduce usability and can cause silent non-compliance. | Either ship the referenced skills, point to canonical spec locations, or mark as optional/conditional. | Stage 4 “Finding T5 — Shipped template skill references other skills that are not shipped in the template tree” |
| T6 | WARNING | Potential conflict: “no writes before APPLY” vs orchestrator writing `.agents/session/**` and `.agents/traces/**` during dry-run planning. | Clarify an explicit exception for local-only `.agents/**` artifacts or adjust template to conform; verify precedence between operations safety gate and observability. | Stage 4 “Finding T6 — Potential conflict: bootstrap “no file writes before APPLY” vs orchestrator trace/session writes” |

## All Findings Inventory (Complete Stage 1–4 Rollup)

This section lists **every** finding recorded in Stages 1–4, using the **exact** stage report section titles.

### Stage 1 — Scope & sanity-check

| Stage 1 finding (exact heading) | Severity | Included in “Key Findings”? |
|---|---:|:---:|
| Finding F1 — Incorrect target file for “§0.5” cross-reference | WARNING | Yes |
| Finding F2 — Ambiguous “→ §0.5” reference (no file/module specified) | SUGGESTION | Yes |

### Stage 2 — Links & references

| Stage 2 finding (exact heading) | Severity | Included in “Key Findings”? |
|---|---:|:---:|
| 1) WARNING — Template guidance implies `framework/spec/**` is optional, but template agents rely on it | WARNING | Yes (as L1) |
| 2) WARNING — Template repo context files repeat the same “optional spec modules” wording | WARNING | No |
| 3) WARNING — Template `llms.txt` repeats the same ambiguity (“if you need module-linked sections”) | WARNING | No |
| 4) WARNING — Unqualified “Operations §7.3.3” references in template agent prompts | WARNING | Yes (as L2) |
| 5) WARNING — Same unqualified “Operations §…” appears in bootstrap agent prompts | WARNING | No |
| 6) WARNING — `framework/spec/00-infrastructure.md` uses ambiguous “§” references and umbrella-file citations in normative prose | WARNING | Yes (as L3) |
| 7) WARNING — `framework/spec/00-infrastructure.md` includes a copy-pastable reference that will be wrong in real `.agent.md` file locations | WARNING | Yes (as L3) |
| 8) SUGGESTION — Several canonical modules use unqualified “see §X.Y” cross-module references | SUGGESTION | No |

### Stage 3 — Canonical invariants

| Stage 3 finding (exact heading) | Severity | Included in “Key Findings”? |
|---|---:|:---:|
| 1) BLOCKER — Trace-writing responsibility contradicted in `01-architecture.md` | BLOCKER | Yes (as I1) |
| 2) SUGGESTION — Potential terminology drift: `APPROVED` used in bootstrap orchestrator prompt | SUGGESTION | No |
| 3) SUGGESTION — Template file name collides with canonical spec entrypoint but contains placeholder content | SUGGESTION | No |

### Stage 4 — Templates alignment

| Stage 4 finding (exact heading) | Severity | Included in “Key Findings”? |
|---|---:|:---:|
| Finding T1 — Template guidance makes `framework/spec/**` sound optional, but shipped template prompts depend on it | WARNING | Yes (as L1) |
| Finding T2 — Bootstrap orchestrator template references a non-canonical `fast_track` value (`tooling-only`) | WARNING | Yes |
| Finding T3 — Template prompts use `APPROVED`/`APPROVE` inconsistently with canonical terminology guidance | SUGGESTION | No |
| Finding T4 — Template agent prompts contain ambiguous references like “Operations §7.3.3” | WARNING | Yes (as L2) |
| Finding T5 — Shipped template skill references other skills that are not shipped in the template tree | WARNING | Yes |
| Finding T6 — Potential conflict: bootstrap “no file writes before APPLY” vs orchestrator trace/session writes | WARNING | Yes |
| Finding T7 — Template README uses upstream-framework paths that won’t exist in downstream repos | SUGGESTION | No |

## Evidence Highlights (Quoted)

These are short, high-signal snippets copied from the stage reports to avoid restating findings ambiguously.

### Incorrect/ambiguous references

- Stage 1, “Finding F1 — Incorrect target file for “§0.5” cross-reference”:
  - Quote: `"[See 00-multi-agent-development-spec.md §0.5 for detailed rules]"`
  - Quote: `"## 0.5 GitFlow + SemVer — detailed rules"` (exists in `framework/spec/00-infrastructure.md`, not the umbrella index)

- Stage 2, “6) WARNING — `framework/spec/00-infrastructure.md` uses ambiguous “§” references and umbrella-file citations in normative prose”:
  - Quote: `"see observability §4"` (no file)
  - Quote: `"see DoD §3.11"` (no file)

- Verified directly in `framework/spec/00-infrastructure.md` (Key Finding L3):
  - Under `## Branching Strategy: GitFlow`:
    - Quote: `[See 00-multi-agent-development-spec.md §0.5 for detailed rules]`
    - Quote: `## 0.5 GitFlow + SemVer — detailed rules`
  - Under `### 0.1.1 .agent.md file format` (copy/paste block intended to become `.github/agents/<...>.agent.md`):
    - Quote: `# Canonical tool IDs: see ./04-observability.md#48-canonical-capability-to-tool-mapping-tool-ids`
    - Quote: `Trace-writing protocol and \`trace_event\` required keys are defined in [04-observability.md](04-observability.md) §4.5–§4.6.`
  - Under `### 0.8.1 Required sections of PROJECT.md` (copy/paste comments inside the sample):
    - Quote: `<!-- The baseline agent set is defined in 00-multi-agent-development-spec.md §1.`
    - Quote: `<!-- Universal model selection rules are in 00-multi-agent-development-spec.md §1.2.`
    - Quote: `Example structure — 00-multi-agent-development-spec.md §6.4.`

### Canonical invariant contradiction (trace writing)

- Stage 3, “1) BLOCKER — Trace-writing responsibility contradicted in `01-architecture.md`”:
  - Quote (as reported): `"append one trace line to a local-only .agents/traces/<trace_id>.jsonl"`
  - Quote (as reported): `"only the orchestrator writes to .agents/traces/**"`

### Template portability hazards

- Stage 2, “1) WARNING — Template guidance implies `framework/spec/**` is optional, but template agents rely on it”:
  - Quote: `"copy framework/spec/** too if you need module links"`

- Stage 4, “Finding T2 — Bootstrap orchestrator template references a non-canonical `fast_track` value (`tooling-only`)”:
  - Quote: ``For bootstrap operations, `fast_track` SHOULD usually be `tooling-only`.``

## Recommended Fix Plan (Ordered)

1) Resolve the BLOCKER invariant contradiction (I1): make trace-writing responsibilities consistent across modules.
2) Make template installs self-consistent (L1): remove “optional spec modules” ambiguity or package modules with templates.
3) Fix ambiguous references in deterministic gates (L2): qualify “Operations §7.3.3” references.
4) Fix enum/value mismatches in templates (T2) and tighten terminology to match canonical enums.
5) Address template dead links (T5) and clarify pre-APPLY write exceptions (T6) once verified.
6) Sweep remaining “see §X.Y” references and replace with fully qualified module references (F2 + Stage 2 “SUGGESTION” set).

## Notes And Risks

- Many findings are about **downstream portability**: they may not break the upstream repo immediately, but they do break navigability and deterministic behavior once templates are copied.
- One item (T6) is explicitly labeled “needs verification” in Stage 4; treat it as a policy-clarification task before changing wording.

## Verification

- This consolidated report is derived strictly from Stages 1–4 and does not introduce new audit stages.
- This file is the intended output for audit-report updates in this repo. This environment/tooling cannot provide repo-authoritative proof (via `git`) of “no changes under `framework/**`”; treat that as an intended-scope statement and verify locally with `git status --porcelain` and `git diff --name-only`.

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