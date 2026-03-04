# Framework Audit — Stage 4 (Templates alignment)

Date: 2026-03-04

## Scope

Audited: `framework/templates/**` only.

Referenced as canonical evidence (read-only): `framework/00-multi-agent-development-spec.md` and `framework/spec/**`.

Out of scope (per this subtask): any edits under `framework/**` or `.github/agents/**`.

## Purpose

Audit `framework/templates/**` for logical consistency and alignment with the canonical spec modules under `framework/spec/**`, with a bias toward **portability** (templates copied into downstream repos should still make sense, and their internal links/references should resolve).

## How coverage was ensured

Read-only exploration over `framework/templates/**`:

- Enumerated all template files (repo-files templates + bootstrap-agents templates).
- Searched for high-risk invariants and portability hotspots:
  - `fast_track`, verdict/status terminology (`APPROVE`, `APPROVED`, `DONE`)
  - trace-writing responsibilities (`.agents/traces`, `trace_event`)
  - AWESOME-COPILOT gate references (`Operations §7.3`, `§7.3.3`)
  - links to spec modules (`framework/spec/`) and links that might break when copied.

---

## Findings

### Finding T1 — Template guidance makes `framework/spec/**` sound optional, but shipped template prompts depend on it

- Severity: **WARNING**
- Location:
  - `framework/templates/repo-files-templates/README.md` → heading `## What is included`
  - `framework/templates/repo-files-templates/root/AGENTS.md` → heading `## What lives here`
  - `framework/templates/repo-files-templates/root/llms.txt` → `Key files`
- What’s wrong:
  - Multiple template “discovery” documents imply that copying `framework/spec/**` is conditional.
  - However, the shipped template agents under `framework/templates/repo-files-templates/root/.github/agents/**` include numerous links/references to `framework/spec/**` (observability, enums, routing) that will be dead if `framework/spec/**` is not present in the downstream repo.
- Evidence:
  - `framework/templates/repo-files-templates/README.md` → `## What is included`:
    - Snippet: `framework/00-multi-agent-development-spec.md (template stub; copy \`framework/spec/**\` too if you need module links)`
  - `framework/templates/repo-files-templates/root/AGENTS.md` → row for `framework/00-multi-agent-development-spec.md`:
    - Snippet: `copy \`framework/spec/**\` too if you need module links referenced from the spec`
  - `framework/templates/repo-files-templates/root/llms.txt` → `Key files`:
    - Snippet: `copy \`framework/spec/**\` too if you need module-linked sections`
  - `framework/templates/repo-files-templates/root/.github/agents/project-orchestrator.agent.md` → `Rule 2 — Choose the fast-track before starting the pipeline`:
    - Snippet: `... canonical enum in [framework/spec/01-architecture.md](../../framework/spec/01-architecture.md#fast-track-enum)`
  - `framework/templates/repo-files-templates/root/.github/agents/project-orchestrator.agent.md` → `### Observability (mandatory)`:
    - Snippet: links to `../../framework/spec/04-observability.md#...`
- Why it matters:
  - Downstream users following the template README literally can end up with a repo where the agent prompts reference missing files.
  - This breaks navigation and increases the chance of drift (agents “guess” rules rather than reading the canonical module).
- Recommended fix:
  - Make the guidance deterministic and self-consistent. Options:
    - **Option A (simplest):** change template docs to say `framework/spec/**` is required when using the shipped `.github/agents/**` prompts.
    - **Option B:** ship the spec modules as part of the installable template (so copying `root/` yields a consistent set).
  - If true optionality is intended, then the prompts must be rewritten so they do not link to files that may be missing (currently they do).

---

### Finding T2 — Bootstrap orchestrator template references a non-canonical `fast_track` value (`tooling-only`)

- Severity: **WARNING**
- Location: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md` → `Rule 2 — Choose the fast-track before starting the pipeline`
- What’s wrong:
  - The template says:
    - Snippet: `For bootstrap operations, \`fast_track\` SHOULD usually be \`tooling-only\`.`
  - But the canonical `fast_track` enum in `framework/spec/01-architecture.md` does not include `tooling-only`.
- Evidence (canonical):
  - `framework/spec/01-architecture.md` → `#### 1.3.8 Shortened Pipeline Paths (Fast-Track)`:
    - Snippet (canonical enum/table rows): `fast_track: feature | lightweight-feature | hotfix | docs-only | docs+feature | infra | security-patch | agent-prompt-update`
  - `framework/spec/01-architecture.md` → `#### 1.3.9 Canonical pipeline vocabulary (normative)`:
    - Snippet (status terminology): `Status := TODO | IN_PROGRESS | BLOCKED | DONE | WONT_FIX | NEEDS_HUMAN | ESCALATED` (and `DONE — completed successfully (do not use \`APPROVED\`)`)
- Why it matters:
  - If a downstream orchestrator follows the bootstrap template literally, it will record a `fast_track` value that is not in the canonical enum, undermining deterministic routing and any policy keyed off the enum.
- Recommended fix:
  - Replace `tooling-only` with a value from the canonical enum.
  - Needs verification: decide which canonical value best fits bootstrap operations (likely `infra` or `agent-prompt-update`, depending on the intended semantics).
    - Verify by reviewing the intended mapping in `framework/spec/01-architecture.md` (fast-track definitions) and `framework/spec/06-adoption-roadmap.md` (bootstrap operations).

---

### Finding T3 — Template prompts use `APPROVED`/`APPROVE` inconsistently with canonical terminology guidance

- Severity: **SUGGESTION**
- Location: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md` → near `Mandatory post-install/upgrade phase`
- What’s wrong:
  - The template uses all-caps `APPROVED` in a way that can be misread as a formal status:
    - Snippet: `runs automatically after apply is APPROVED`
  - Canonical terminology explicitly warns not to use `APPROVED` as a formal enum value (Status uses `DONE`; verdict uses `APPROVE`).
- Evidence (canonical):
  - `framework/spec/01-architecture.md` → `#### 1.3.9 Canonical pipeline vocabulary (normative)`:
    - Snippet: `DONE — completed successfully (do not use \`APPROVED\`).`
    - Snippet: `verdict := APPROVE | REQUEST_CHANGES | REJECT`
- Why it matters:
  - Bootstrap templates are likely to be copied verbatim into new repos; ambiguous terminology tends to propagate and then becomes hard to enforce deterministically.
- Recommended fix:
  - Rephrase to a canonical form, e.g.:
    - “after apply completes and the critic returns verdict `APPROVE`”, or
    - “after the apply step is accepted (critic verdict `APPROVE`)”.

---

### Finding T4 — Template agent prompts contain ambiguous references like “Operations §7.3.3”

- Severity: **WARNING**
- Locations (representative; multiple files):
  - `framework/templates/repo-files-templates/root/.github/agents/project-*-critic.agent.md` → heading `### Gate report completeness (deterministic)`
  - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-critic.agent.md` → sections `## Role` and `#### Review stage: APPLIED_RESULT`
  - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-upgrader.agent.md` → gate checklist area
  - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md` → AWESOME-COPILOT gate area
- What’s wrong:
  - The phrase `Operations §7.3` / `Operations §7.3.3` is used without naming the canonical file.
  - In a downstream repo, “Operations” is not a filename and may be interpreted inconsistently.
- Evidence:
  - `framework/templates/repo-files-templates/root/.github/agents/project-backend-critic.agent.md` → `### Gate report completeness (deterministic)`:
    - Snippet: `... aligns with ... Rule 8 and Operations §7.3.3`.
  - `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-critic.agent.md` → `#### Review stage: APPLIED_RESULT`:
    - Snippet: `... evidence is missing or invalid (Operations §7.3.3)`.
- Why it matters:
  - These references appear inside deterministic gate logic; ambiguity increases drift risk and makes enforcement brittle.
- Recommended fix:
  - Replace “Operations §7.3/§7.3.3” with an explicit reference:
    - `framework/spec/07-framework-operations.md §7.3` / `§7.3.3` (preferably as a Markdown link whose relative path resolves from the `.agent.md` location).

---

### Finding T5 — Shipped template skill references other skills that are not shipped in the template tree

- Severity: **WARNING**
- Location: `framework/templates/repo-files-templates/root/.agents/skills/awesome-copilot-navigator/SKILL.md` → heading `## References`
- What’s wrong:
  - The template skill links to:
    - `.agents/skills/agent-file-standards/SKILL.md`
    - `.agents/skills/ai-security/SKILL.md`
  - But those skills are not present under `framework/templates/repo-files-templates/root/.agents/skills/`.
- Evidence:
  - `framework/templates/repo-files-templates/root/.agents/skills/awesome-copilot-navigator/SKILL.md` → `## References`:
    - Snippet: `- File format rules: .agents/skills/agent-file-standards/SKILL.md`
    - Snippet: `- Prompt injection / supply chain: .agents/skills/ai-security/SKILL.md`
- Why it matters:
  - When copied into a downstream repo, these references become dead links and reduce the usefulness of the shipped skill.
  - This is a portability issue that can also cause “silent non-compliance” (agents can’t load the referenced checklists).
- Recommended fix:
  - Either:
    - Include the referenced skills in the template root tree, or
    - Change the references to canonical spec locations under `framework/spec/**` (if the intent is “read the canonical standard”), or
    - Mark them explicitly as optional (“if present in your repo”).

---

### Finding T6 — Potential conflict: bootstrap “no file writes before APPLY” vs orchestrator trace/session writes

- Severity: **WARNING** (needs verification)
- Location:
  - Template: `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-orchestrator.agent.md` → near top `Clarification`
  - Canonical: `framework/spec/07-framework-operations.md` → `## 7.2 Safety gate for bootstrap operations (dry-run → confirm → apply)`
  - Canonical: `framework/spec/04-observability.md` → `### 4.6.1 Rules for agents` (orchestrator creates trace/session artifacts at plan time)
- What’s wrong (interpretation-dependent):
  - The safety gate says the bootstrap agent MUST wait for `APPLY` before “writing or deleting files”.
  - The bootstrap orchestrator template explicitly permits writing `.agents/session/**` and `.agents/traces/*.jsonl` regardless of dry-run vs apply:
    - Snippet: `You (the orchestrator) MAY write .agents/session/** and .agents/traces/*.jsonl regardless of dry-run vs apply.`
  - Canonical observability instructs the orchestrator to create trace/session artifacts as part of planning.
- Why it matters:
  - If `07-framework-operations.md` §7.2 is interpreted strictly (no file writes at all), the template’s behavior is non-compliant.
  - If local-only `.agents/**` artifacts are intended as an exception, the exception is not stated in §7.2, so downstream readers can reach conflicting conclusions.
- Recommended fix (needs verification):
  - Decide and document whether `.agents/session/**` and `.agents/traces/*.jsonl` are exempt from the “no writes before APPLY” constraint.
  - Verification method:
    - Re-read `framework/spec/07-framework-operations.md` §7.2 alongside `framework/spec/04-observability.md` §4.6.1–§4.6.2 and confirm intended precedence.
    - If an exemption is intended, update §7.2 (canonical) to state it explicitly, or adjust the bootstrap template to conform.

---

### Finding T7 — Template README uses upstream-framework paths that won’t exist in downstream repos

- Severity: **SUGGESTION**
- Location: `framework/templates/bootstrap-agents-templates/README.md` → `## How to use`
- What’s wrong:
  - The README instructs copying/merging:
    - Snippet: `framework/templates/repo-files-templates/root/`
    - Snippet: `framework/templates/bootstrap-agents-templates/root/`
  - In downstream repos, these paths will not exist (users will likely be looking at a copied template directory).
- Why it matters:
  - This is a portability footgun: instructions become confusing once the templates are vendored or copied.
- Recommended fix:
  - Use paths relative to the README location (e.g. `../repo-files-templates/root/` and `./root/`) or clarify “these paths are relative to the upstream ForgentFramework repo”.

---

## Non-findings (alignment confirmed)

- `.agents/compliance/awesome-copilot-gate.md` template matches the canonical required fields block in `framework/spec/07-framework-operations.md` §7.3.3.
- Template `.gitignore` correctly ignores `.agents/session/` and `.agents/traces/*.jsonl` while allowlisting `.agents/traces/README.md`.

---

## Verification (report-only)

- Write scope: this stage creates a single report file under `audit/` and proposes fixes only; no changes were made under `framework/**` or `.github/agents/**`.
- Manual link sanity: all file paths quoted in this report exist in the current workspace.

## Trace

```json
{"trace_event":{"agent":"GitHub Copilot","operation":"execute","subtask":2,"iteration":1}}
```
