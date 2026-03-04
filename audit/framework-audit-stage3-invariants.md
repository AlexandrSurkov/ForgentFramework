# Framework Audit — Stage 3 (Canonical invariants)

Date: 2026-03-03  
Scope: `framework/**` only  
Out of scope: anything outside `framework/**` (including `Test/**`).

## Purpose

Audit `framework/**` for logical consistency and contradictions around **canonical invariants**, specifically:

- Canonical enums / vocabulary (`fast_track`, critic `verdict`, subtask `Status`, severity labels)
- Role boundaries (orchestrator vs executor vs critic; critic isolation; Reflexion; iteration caps)
- Observability protocol (JSONL traces, `trace_event` contract, “who writes traces”) and canonical tool IDs
- AWESOME-COPILOT deterministic gate (trigger, single canonical report path, required fields)

This report is **read-only**: it proposes fixes but does not change `framework/**`.

## Canonical invariants (sources of truth)

- **Enums / vocabulary**
  - `fast_track` enum, `verdict` enum, subtask `Status` enum: `framework/spec/01-architecture.md`
  - Terminology rule: do not mix verdict vs status vs human approval: `framework/spec/01-architecture.md` (Terminology section near the enums)

- **Observability**
  - Required JSONL keys and `trace_event` required keys: `framework/spec/04-observability.md` §4.5
  - Trace writing protocol: “only orchestrator writes `.agents/traces/**`”: `framework/spec/04-observability.md` §4.6
  - Canonical tool IDs for agent frontmatter `tools:`: `framework/spec/04-observability.md` §4.8

- **Role rules / gates**
  - Critic isolation and executor↔critic iteration cap: `framework/spec/03-rubrics/*`
  - AWESOME-COPILOT deterministic gate + required gate report fields: `framework/spec/07-framework-operations.md` §7.3 (also enforced by `framework/spec/03-rubrics/03-critic-rules-and-report-format.md` Rule 8)

## Coverage (how “all files under framework/” were checked)

1) **Inventory sweep**
- Enumerated all files under `framework/**` (spec modules, templates, tools scripts).

2) **Cross-cutting text searches over `framework/**`**
- Observability / trace-writing: `\.agents/traces`, `trace_event`, `span_id`, `only the orchestrator writes`, `append one trace line`
- Enums / vocabulary: `fast_track`, `verdict :=`, `Status :=`, `APPROVED`, `REQUEST_CHANGE`
- Tool IDs: `tools:`, `readFile`, `fileSearch`, `textSearch`, `editFiles`, `createFiles`, `runTerminal`, `problems`, `changes`, `fetch`, `webSearch`, `githubRepo`
- AWESOME-COPILOT gate: `AWESOME-COPILOT`, `.agents/compliance/awesome-copilot-gate.md`, `.github/agents/**/*.agent.md`, `.github/prompts/**/*.prompt.md`

3) **Targeted reads of canonical sections**
- `framework/spec/01-architecture.md`: enums/vocab; pipeline definition; iteration/NEEDS_HUMAN + re-entry semantics
- `framework/spec/02-sessions-and-memory.md`: `TASK_CONTEXT.md` structure; re-entry protocol
- `framework/spec/04-observability.md`: required keys; orchestrator-only trace writing; tool IDs
- `framework/spec/07-framework-operations.md`: AWESOME-COPILOT gate definition and required fields
- Spot checks in `framework/templates/**` and `framework/tools/bootstrap.*` for drift in tool IDs, gate path, and trace-writing responsibilities.

## Findings

### 1) BLOCKER — Trace-writing responsibility contradicted in `01-architecture.md`

- **Severity:** BLOCKER
- **Location:** `framework/spec/01-architecture.md` → `### 1.3.1 Three levels of work`
- **What’s wrong**
  - `01-architecture.md` describes **Subtask output** as including writing directly to `.agents/traces/<trace_id>.jsonl`:

    > “commit code/deliverables; **append one trace line** to a local-only `.agents/traces/<trace_id>.jsonl` file …”

  - This conflicts with the observability invariant that **only the orchestrator writes trace files**, and executors/critics must return `trace_event` objects only:

    > “To enforce least-privilege (critics are read-only), only the **orchestrator** writes to `.agents/traces/**`.”
    > “Executors and critics **MUST NOT write trace files**.”
    > “Executors and critics MUST return a small `trace_event` JSON object …”

- **Why it matters**
  - This is a direct contradiction of a least-privilege boundary. If an executor follows `01-architecture.md` literally, it violates `04-observability.md` and undermines the “critics are read-only” model.
  - It also creates ambiguity for downstream agent prompts/templates that link to both modules.

- **Recommended fix**
  - Update `framework/spec/01-architecture.md` row “Subtask → Output” to align with `framework/spec/04-observability.md`:
    - Replace “append one trace line …” with: “commit code/deliverables; include `trace_event` JSON in response (no file writes)”
    - Optionally add an explicit cross-reference: “Trace writing protocol: `framework/spec/04-observability.md` §4.6”.
  - Keep “trace files are local-only and gitignored” guidance, but scope it to orchestrator behavior.

---

### 2) SUGGESTION — Potential terminology drift: `APPROVED` used in bootstrap orchestrator prompt

- **Severity:** SUGGESTION
- **Location:** `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md` → early “Role” section
- **What’s wrong**
  - The prompt says:

    > “Mandatory post-install/upgrade phase (runs automatically after apply is **APPROVED** — do NOT skip)”

  - Canonical vocabulary guidance in `framework/spec/01-architecture.md` warns against using `APPROVED` as a status/label:
    - `verdict := APPROVE | REQUEST_CHANGES | REJECT`
    - Status uses `DONE`, and it explicitly says “do not use `APPROVED`”.

- **Why it matters**
  - This is likely intended as plain-English past tense, but the all-caps formatting makes it easy to misread as a formal enum value.
  - Bootstrap is a “first touch” experience; terminology ambiguity here tends to propagate.

- **Recommended fix**
  - Rephrase to avoid all-caps `APPROVED`, for example:
    - “after the apply step completes and the critic returns `APPROVE`”
    - or “after apply is accepted (critic verdict `APPROVE`)”.

---

### 3) SUGGESTION — Template file name collides with canonical spec entrypoint but contains placeholder content

- **Severity:** SUGGESTION
- **Location:** `framework/templates/repo-files-templates/root/framework/00-multi-agent-development-spec.md` (entire file)
- **What’s wrong**
  - The template file has the same path/name as the canonical umbrella spec, but it is explicitly a placeholder:

    > “This file must contain the **Multi-Agent Development Specification** used by your project.”
    > “1. Copy the latest spec into this file …”

- **Why it matters**
  - In downstream repos, a file at `framework/00-multi-agent-development-spec.md` strongly signals “this is the normative spec”. A placeholder at that path can cause accidental partial installs where agents follow a non-spec stub.
  - This is not a contradiction inside `framework/**` itself, but it is an **invariant hazard** because the template’s path matches the canonical spec entrypoint.

- **Recommended fix**
  - Make the placeholder unambiguous and harder to misapply, e.g. one of:
    - Rename template file to `framework/00-multi-agent-development-spec.TEMPLATE.md` (and update any references), or
    - Add a top-level, high-visibility WARNING block stating “NOT THE SPEC — INSTALLER MUST OVERWRITE THIS FILE WITH THE REAL SPEC”, or
    - Ensure the installer/upgrade playbooks never copy this template into place unless also copying the full spec in the same change set.

## Non-findings (consistency confirmed)

- Canonical tool IDs in agent templates match `framework/spec/04-observability.md` §4.8 (`readFile`, `fileSearch`, `textSearch`, `editFiles`, `createFiles`, `runTerminal`, `problems`, `changes`, `agent`, etc.).
- AWESOME-COPILOT gate trigger and canonical report path are consistent across spec + templates:
  - Trigger: edits to `.github/agents/**/*.agent.md` or `.github/prompts/**/*.prompt.md`
  - Canonical report path: `.agents/compliance/awesome-copilot-gate.md`

## Trace

```json
{"trace_event":{"agent":"forgent-process-critic","operation":"critique","subtask":3,"iteration":4,"verdict":"APPROVE","blockers":0,"warnings":0}}
```
