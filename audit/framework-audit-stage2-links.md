# Framework Audit — Stage 2 (Links & References)

Date: 2026-03-03

## Scope

Audited: **all files under** `framework/` (including `framework/spec/**`, `framework/templates/**`, `framework/tools/**`).

Explicitly excluded: `Test/Delpoyment/**` (intentionally excluded as a mirror, per audit instructions).

## How coverage was ensured

Read-only exploration used repo-wide searches scoped to `framework/**`:

- File enumeration: `framework/**` glob (to ensure *all* files were in-scope).
- Markdown link scan:
  - Regex `\]\([^\)]+\)` over `framework/**/*.md` (captures standard Markdown links).
  - Regex `\]\([^\)]+\.md\)(?!\#)` over `framework/**/*.md` (detects `.md` links without anchors, for spot-checking).
- “§X.Y” reference scan: regex `§\s*\d+(?:\.\d+)+` over `framework/**/*.md`.
- Cross-file reference scan: literal `framework/spec/` over `framework/**/*` (captures templates and non-Markdown files too, e.g. `.txt`, `.agent.md`).
- Targeted ambiguity scans: `Operations\s*§`, `DoD\s*§`, and `see\s+§` over `framework/**/*.md`.

Notes on interpretation:
- Links inside fenced code blocks were treated as **examples/templates**, not as “broken links in this repo”, but they were still audited for whether they would mislead users when copied verbatim.

---

## Findings

### 1) WARNING — Template guidance implies `framework/spec/**` is optional, but template agents rely on it

- **Location:** `framework/templates/repo-files-templates/README.md` → `## What is included`
- **What’s wrong:** The template description says copying `framework/spec/**` is conditional.
  - Snippet: “`copy framework/spec/** too if you need module links`”
- **Why it matters:** The shipped template agent prompts under `framework/templates/repo-files-templates/root/.github/agents/**` contain many references/links to `framework/spec/**` (e.g. verdict enum, trace protocol). If a downstream repo copies only `root/` and does not also vendor `framework/spec/**`, these references become dead / unresolvable.
- **Recommended fix:** Make the guidance deterministic:
  - Either (A) say “copy `framework/spec/**` (required for the shipped agent prompts)” everywhere the template is referenced, or
  - (B) include `framework/spec/**` as part of the template content so copying `root/` yields a consistent, navigable set.

### 2) WARNING — Template repo context files repeat the same “optional spec modules” wording

- **Location:** `framework/templates/repo-files-templates/root/AGENTS.md` → `## What lives here`
- **What’s wrong:** The spec modules are described as optional.
  - Snippet: “`template ships a stub; copy framework/spec/** too if you need module links`”
- **Why it matters:** This is a primary discovery surface for agents/humans. If followed literally, downstream users can end up with agent prompts that reference modules that are not present.
- **Recommended fix:** Align with `framework/templates/repo-files-templates/root/framework/00-multi-agent-development-spec.md` which already states modules must be copied; remove the conditional phrasing in `AGENTS.md`.

### 3) WARNING — Template `llms.txt` repeats the same ambiguity (“if you need module-linked sections”)

- **Location:** `framework/templates/repo-files-templates/root/llms.txt` → `Key files`
- **What’s wrong:** The `llms.txt` template suggests `framework/spec/**` is optional.
  - Snippet: “`copy framework/spec/** too if you need module-linked sections`”
- **Why it matters:** In practice, the template’s `.agent.md` prompts and several workflow rules reference `framework/spec/**` sections (anchors + § references). Missing modules means the “Key files” list becomes misleading and the links in prompts are non-navigable.
- **Recommended fix:** Replace “if you need …” with a requirement (“copy `framework/spec/**` alongside the umbrella spec”) or add a clear conditional that is actually consistent with the shipped prompt set (e.g., “required if you are using the shipped `.github/agents/**` prompts”).

### 4) WARNING — Unqualified “Operations §7.3.3” references in template agent prompts

- **Location:** `framework/templates/repo-files-templates/root/.github/agents/project-backend-critic.agent.md` → `### Gate report completeness (deterministic)`
- **What’s wrong:** The agent prompt references “Operations §7.3.3” without naming/linking the canonical file.
  - Snippet: “`... and Operations §7.3.3`”
- **Why it matters:** In downstream repos, “Operations” is not a file name and can be interpreted inconsistently. This is especially risky because it governs a deterministic gate.
- **Recommended fix:** Replace “Operations §7.3.3” with an explicit canonical reference, e.g.:
  - `framework/spec/07-framework-operations.md §7.3.3` (preferably as a Markdown link with an anchor).

### 5) WARNING — Same unqualified “Operations §…” appears in bootstrap agent prompts

- **Location:** `framework/templates/bootstrap-agents-templates/root/.github/agents/bootstrap-upgrader.agent.md` → `## AWESOME-COPILOT gate (deterministic)`
- **What’s wrong:** Uses “Operations §7.3.3” without naming/linking the canonical target.
  - Snippet: “`... includes required fields (Operations §7.3.3).`”
- **Why it matters:** Bootstrap agents are explicitly used for Install/Upgrade/Remove; ambiguous references increase the chance of partial/incorrect compliance.
- **Recommended fix:** Use the canonical, fully qualified reference: `framework/spec/07-framework-operations.md §7.3.3`.

### 6) WARNING — `framework/spec/00-infrastructure.md` uses ambiguous “§” references and umbrella-file citations in normative prose

- **Location:** `framework/spec/00-infrastructure.md` → (top-level `.gitignore` guidance) and `### 0.1.1 `.agent.md` file format`
- **What’s wrong:** Multiple references are ambiguous or point at the umbrella file instead of the canonical module.
  - Snippets:
    - “`see observability §4`” (no file)
    - “`see DoD §3.11`” (no file; “DoD” is not uniquely resolvable)
    - “`see §5.1`” (no file)
    - “`tiers in 00-multi-agent-development-spec.md §1`” (points to umbrella)
- **Why it matters:** This module is a canonical normative source (§0.1). Unqualified section references force readers to guess the target module and become brittle when the umbrella file is shipped as a stub (as the templates explicitly do).
- **Recommended fix:** Replace with explicit canonical module references, e.g.:
  - `framework/spec/04-observability.md §4` (or the precise subsection)
  - `framework/spec/03-rubrics/11-dor-dod-and-adr-format.md` for DoD/DoR references (or the exact named section)
  - `framework/spec/05-prompt-versioning.md §5.1` when referring to prompt changelog policy
  - `framework/spec/01-architecture.md §1` (or more precise) for tiers/model rules

### 7) WARNING — `framework/spec/00-infrastructure.md` includes a copy-pastable reference that will be wrong in real `.agent.md` file locations

- **Location:** `framework/spec/00-infrastructure.md` → `### 0.1.1 `.agent.md` file format` (inside the `.agent.md` YAML example)
- **What’s wrong:** The example comment suggests a relative link that would not resolve from `.github/agents/*.agent.md`.
  - Snippet: “`# Canonical tool IDs: see ./04-observability.md#48-canonical-capability-to-tool-mapping-tool-ids`”
- **Why it matters:** This snippet is likely to be copied verbatim into downstream `.agent.md` files. From `.github/agents/…`, `./04-observability.md` will not exist.
- **Recommended fix:** Use a path that matches the intended repo structure, e.g. `../../framework/spec/04-observability.md#48-canonical-capability-to-tool-mapping-tool-ids`, or use a path that is correct regardless of agent file location (e.g., `framework/spec/04-observability.md#...` as plain text).

### 8) SUGGESTION — Several canonical modules use unqualified “see §X.Y” cross-module references

- **Location:**
  - `framework/spec/02-sessions-and-memory.md` → `trace_id` section
  - `framework/spec/01-architecture.md` → escalation + Human Input notes
  - `framework/spec/03-rubrics/11-dor-dod-and-adr-format.md` → PR merge gates
  - `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` → glossary table (`mcp.json` row)
- **What’s wrong:** Cross-module references like “`see §4.6.1`”, “`see §3.3`”, “`see §0.6`”, and “`see §0.1`” don’t name the target module.
  - Examples:
    - “`... (see §4.6.1).`”
    - “`... ESCALATED (see §3.3).`”
    - “`PR merge gates (Gate 1–3; see §0.6):`”
- **Why it matters:** Readers encountering a module in isolation (or via deep links from templates) cannot reliably resolve “§X.Y” to the right file. This is especially relevant when the umbrella file is intentionally small and not the canonical location for details.
- **Recommended fix:** Prefer `(<module-file> §X.Y)` or a Markdown link to the canonical module + anchor (when stable), e.g.:
  - `framework/spec/04-observability.md §4.6.1`
  - `framework/spec/03-rubrics/03-critic-rules-and-report-format.md`
  - `framework/spec/00-infrastructure.md §0.6`

---

## Notes / risks

- This stage focused on **reference correctness and portability**, especially for template-installed downstream repos.
- Anchor validation was spot-checked for high-traffic targets used by templates (e.g., `framework/spec/01-architecture.md` explicit anchors like `#fast-track-enum`, and `framework/spec/04-observability.md` headings that generate `#45-...` / `#46-...` anchors).
