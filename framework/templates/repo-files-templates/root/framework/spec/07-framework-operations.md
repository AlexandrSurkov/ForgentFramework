# 7. Framework Operations

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

This module defines **invariant operational policies and gates** for using the framework.
It MUST NOT duplicate step-by-step procedures; the runnable Install/Upgrade/Remove playbooks live in the Adoption Roadmap module.

Procedures (links only):
- Install: [06-adoption-roadmap.md](06-adoption-roadmap.md) (`## 6.install`)
- Upgrade: [06-adoption-roadmap.md](06-adoption-roadmap.md) (`## 6.upgrade`)
- Remove: [06-adoption-roadmap.md](06-adoption-roadmap.md) (`## 6.remove`)

---

## 7.1 Two-tier operations model (normative)

The framework uses two distinct agent groups:

- **Group 1 — Project-working agents**: orchestrator + domain executors/critics (backend, frontend, devops, security, docs, QA, architect).
  - Purpose: feature work, bugfixes, design, and reviews within the project.
  - Constraint: Group 1 MUST NOT be used for framework installation/upgrade/removal tasks.

- **Group 2 — Bootstrap agents**: bootstrap orchestrator + bootstrap executors + bootstrap critic.
  - Minimum executor set: installer, upgrader, remover.
  - `bootstrap-orchestrator` and `bootstrap-critic` are OPTIONAL but RECOMMENDED (and shipped by default).
  - Template-default set (shipped): `bootstrap-orchestrator`, `bootstrap-installer`, `bootstrap-upgrader`, `bootstrap-remover`, `bootstrap-critic`.
  - Purpose: install/upgrade/remove the framework and the agent system scaffolding.
  - Constraint: Group 2 MUST focus on agent-system and framework integration artifacts (examples: `framework/**` vendoring, `.github/agents/**`, `.github/prompts/**`, `.agents/**`, `PROJECT.md`, `AGENTS.md`, `.github/copilot-instructions.md`, `.vscode/**`).
       Group 2 SHOULD NOT perform unrelated product feature work.

Routing:
- Any task whose primary goal is **Install**, **Upgrade**, or **Remove** MUST be routed to Group 2.
- When a project is not yet bootstrapped (Group 2 does not exist), vanilla Copilot (non-agent chat) MAY be used to create Group 2 once, after which all operations MUST use Group 2.

---

## 7.2 Safety gate for bootstrap operations (dry-run → confirm → apply)

For Install/Upgrade/Remove tasks, the acting bootstrap agent MUST follow this deterministic safety protocol:

1. **Dry-run**: produce a complete change plan.
      - MUST enumerate file operations: create/modify/delete and paths.
      - MUST call out any destructive step.
  - MUST include deterministic artifacts in this exact order:
    1) **Discovery Evidence Table** — each row MUST include: `evidence_id`, `source_path_or_command`, `observation`, `inference`, `confidence`, `fills_todo_id`.
    2) **Unresolved TODO Table** — each row MUST include: `todo_id`, `description`, `why_unresolved_after_discovery`, `blocking_stage`, `required_input`.
    3) **Question Mapping Table** — each row MUST include: `question_id`, `maps_to_todo_id`, `question_text`, `accepted_answer_format`, `unblocks_stage`.
  - MUST use stage markers in the dry-run text exactly as: `[DISCOVERY]`, `[UNRESOLVED]`, `[QUESTIONS]`, `[PLAN]`.
  - MUST maximize autonomous discovery and evidence-based autofill before producing any user question.
  - MUST NOT include user questions for TODOs that were resolved by discovery/autofill.

2. **Confirm**: request explicit user confirmation.
  - MUST wait for the user to respond with the exact token `APPLY` before writing or deleting any **repo artifacts**.
  - Exception: during Dry-run/Confirm (pre-`APPLY`), the orchestrator MAY write **gitignored, local-only runtime artifacts** under `.agents/session/**` and `.agents/traces/*.jsonl`. This exception does not allow any other file writes.

3. **Apply**: perform the changes and summarize what happened.
      - MUST list modified files.
      - MUST point to any follow-up validations (tests, evals).

### 7.2.1 Deterministic template deployment manifest (install/upgrade)

For `Install` (and for `Upgrade` when replacing shipped framework assets), the executor MUST produce a critic-verifiable deployment manifest that covers shipped framework templates deployed into the **host repo** (the repository that contains `framework/`).

Manifest requirements:

- MUST include one row per intended file operation with columns:
  `manifest_id | source_template_path | destination_path | operation(create|modify|skip|delete) | reason | stage(dry-run|apply)`
- MUST cover at minimum source templates under:
  - `framework/templates/repo-files-templates/root/**`
  - `framework/templates/bootstrap-agents-templates/root/**`
- MUST include a deterministic source inventory summary with exact counters:
  - `source_rows_repo_templates`
  - `source_rows_bootstrap_templates`
  - `source_rows_total`
- MUST resolve each source row to a concrete host destination path.
- MUST include a completeness summary with exact counters:
  - `rows_total`
  - `rows_applied`
  - `rows_skipped`
  - `rows_failed`

Completeness rule:

- `rows_failed` MUST equal `0` for an `APPROVE` decision on `Review stage: APPLIED_RESULT`.
- Any missing source→destination mapping row is a deterministic `BLOCKER`.
- `rows_total` MUST equal `source_rows_total`; mismatch is a deterministic `BLOCKER`.

### 7.2.2 Topology classification and clarifying-question rule

Bootstrap discovery MUST classify topology before asking topology-related questions.

Topology classes:

- `single-repo`: only one in-scope writable repo root is discovered.
- `multi-repo`: more than one in-scope writable repo root is discovered.

Required dry-run fields:

- `topology_class`
- `topology_confidence` (`high` | `low`)
- `topology_signal` (observable evidence string that MUST include discovered repo-root paths and detection basis)

`topology_signal` minimum shape (single-line, deterministic):

- `repo_roots=[...]; host_repo=<path>; sibling_repo_roots=[...]; detection_basis=<vcs|workspace|metadata|fallback>; contradictions=<none|...>; low_confidence_reason=<none|...>; topology_question_allowed=<yes|no>`

Deterministic low-confidence rule:

- `topology_confidence` MUST be `low` if any of the following holds:
  - discovery found conflicting root candidates with no single deterministic winner,
  - fallback heuristic was required and produced 2+ plausible root sets,
  - detected roots contradict explicit repository metadata (`PROJECT.md`, workspace config, or VCS markers).

Clarifying question constraint:

- Topology clarification MAY be asked only when `topology_confidence = low`.
- At most one topology clarifying question is allowed per dry-run.
- The question MUST map to exactly one unresolved TODO row in the Question Mapping Table.
- If `topology_confidence = low`, `topology_signal` MUST include a non-`none` `low_confidence_reason` value.
- If `topology_confidence = high`, `topology_signal` MUST set `low_confidence_reason=none` and `topology_question_allowed=no`.

If `topology_confidence = high`, no topology clarifying question is allowed.

### 7.2.3 Install/upgrade completion gate + RC mapping (normative)

Completion gate (non-bypass):

- For `Install` and `Upgrade`, bootstrap execution MUST NOT be marked complete immediately after `Apply`.
- Completion is allowed only after both post-apply stages succeed:
  1) `bootstrap-repo-context-bootstrap` processed all discovered repos (including sibling repos when topology is `multi-repo`), and
  2) `bootstrap-repo-context-bootstrap-critic` returned `APPROVE`.
- If either stage is skipped, deferred, or not approved, the run MUST remain incomplete (for example `HANDOFF_REQUIRED`), and `TASK_COMPLETE` MUST NOT be emitted.
- This rule applies equally to orchestrated runs and direct `bootstrap-installer` / `bootstrap-upgrader` invocation paths.

Normative RC mapping (audit labels):

| RC label | Required clause(s) |
|---|---|
| **RC1 — Template deployment completeness** | §7.2.1 deterministic deployment manifest + counters (`rows_total = source_rows_total`, `rows_failed = 0` for `APPLIED_RESULT`) |
| **RC2 — Topology determination behavior** | §7.2.2 topology classification + deterministic low-confidence rule + single-question constraint |
| **RC3 — Multi-repo per-repo context fill** | §7.2.3 completion gate item (1): `bootstrap-repo-context-bootstrap` MUST process all discovered repos, including siblings in `multi-repo` |
| **RC4 — Host aggregation from sibling context** | [06-adoption-roadmap.md](06-adoption-roadmap.md) §6.install step 7 host-aggregation requirements (source→host aggregation table) |
| **RC5 — Agent enrichment + AWESOME-COPILOT gate** | §7.3 trigger + required gate artifact/fields + enforcement mechanism; plus §7.2.3 completion gate when post-apply host enrichment is in scope |

---

## 7.3 AWESOME-COPILOT gate (deterministic)

This gate makes **awesome-copilot consultation** auditable and critic-enforceable.

Rationale:
- Agent/prompt files are high-leverage and easy to regress.
- Mandatory consultation provides a repeatable baseline of quality and prevents “invented” conventions.

### 7.3.1 Trigger

The gate triggers on **any** change to either path pattern:

- `.github/agents/**/*.agent.md`
- `.github/prompts/**/*.prompt.md`

### 7.3.2 Required artifact

When the trigger fires, the change set MUST include the gate report:

- `.agents/compliance/awesome-copilot-gate.md`

The report MUST be updated in the same change set as the agent/prompt edits.

### 7.3.3 Required fields (minimum)

The report MUST include the following sections so a critic can verify it deterministically:

```markdown
# AWESOME-COPILOT Gate Report

## Trigger
- Changed agent/prompt artifacts: yes

## Changed artifacts (MUST be complete)
- .github/agents/...
- .github/prompts/...

## Awesome-copilot consultation (MUST when trigger fires)
- Consultation performed: yes
  Source collection: awesome-copilot
  Consulted material: <url>
  Immutable reference: <commit SHA or release tag>
  License: <SPDX> (verified at <path>)
  Result: used | not used
  OR
- Consultation performed: unable
  Reason: <explicit reason>
  Fallback: <what you did instead>

## External material incorporated (optional)
- n/a
  OR
- <url>
  Immutable reference: <commit SHA or release tag>
  License: <SPDX> (verified at <path>)

## Actions taken
- Injection review performed: yes|no
- Per-artifact Provenance updated: yes|no (Appendix A1.1)
- Attribution/notice handling: n/a|done
```

Additional constraints (deterministic):
- When the trigger fires, the report MUST NOT claim “no external sources used” as a substitute for consultation.
- When the trigger fires, the report MUST NOT contain the deprecated pattern `## External sources used` → `- none`.
- “Unable” is allowed only with an explicit reason and a concrete fallback.

### 7.3.4 Enforcement mechanism

- Executors MUST follow `framework/spec/03-rubrics/02-executor-rules.md` Rule 4.
- Critics MUST enforce `framework/spec/03-rubrics/03-critic-rules-and-report-format.md` Rule 8 as a `BLOCKER`.

Note: this gate complements (and does not replace) the per-artifact provenance rules in Appendix A1.1: [appendices/01-appendix-a1-ai-and-llm-standards.md](appendices/01-appendix-a1-ai-and-llm-standards.md).

---

## 7.4 Spec version pinning (PROJECT.md header only)

Projects using this framework MUST record the applied spec version in a single canonical place:

- `PROJECT.md` header line: `> Spec: Multi-Agent Development Specification vX.Y.Z`

Projects MUST NOT use secondary spec-version fields (for example `Spec version: vX.Y.Z`) anywhere in `PROJECT.md`.

During an upgrade, the upgrader MUST update the `> Spec:` header line to the new version.

---

## 7.5 Playbooks (links only)

Detailed procedures and runnable prompts:
- [06-adoption-roadmap.md](06-adoption-roadmap.md)
