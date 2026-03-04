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

2. **Confirm**: request explicit user confirmation.
  - MUST wait for the user to respond with the exact token `APPLY` before writing or deleting any **repo artifacts**.
  - Exception: during Dry-run/Confirm (pre-`APPLY`), the orchestrator MAY write **gitignored, local-only runtime artifacts** under `.agents/session/**` and `.agents/traces/*.jsonl`. This exception does not allow any other file writes.

3. **Apply**: perform the changes and summarize what happened.
      - MUST list modified files.
      - MUST point to any follow-up validations (tests, evals).

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
