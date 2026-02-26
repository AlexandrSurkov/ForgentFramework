---
name: markdown-writer
description: "Write and review Markdown (.md) files with consistent structure, correct links, and repo-friendly conventions. Use when editing README, ADRs, AGENTS.md, llms.txt, SKILL.md, copilot-instructions.md, or any documentation page."
---

# SKILL: Markdown Writer

> Purpose: help agents reliably author and review Markdown with correct structure, links, and minimal ambiguity.
> This skill is intended to be used by any agent that creates/edits/reviews `.md` content.

## When to Load This Skill

Load this skill when you:

- Create or edit any `*.md` file
- Write documentation changes (README, guides, design docs)
- Create or update ADRs in `.github/decisions/`
- Maintain repo context files such as `AGENTS.md`, `llms.txt`, or `copilot-instructions.md`
- Create or update `SKILL.md` packages or `.agent.md` prompts (Markdown structure still applies)
- Review documentation as a critic (links, headings, formatting)

---

## Requirements (Must-Haves)

Agents writing or editing Markdown in this repo must satisfy all of the following:

### R1 — Language and permanence

- All committed Markdown must be **English**.
- Avoid time-sensitive phrasing (“today/now”) unless a date is explicitly stated.

### R2 — Document structure

- Exactly one top-level title: a single `# ...` heading.
- Headings are hierarchical and ordered: `#` → `##` → `###` (no skipped levels).
- Headings are unique (avoid duplicates that may break anchors).

### R3 — Links

- Prefer **relative links** for repo files.
- Do not introduce broken links; if you add/change a link, verify the target exists in the workspace.
- Use `/` as a path separator (never `\`).
- Use descriptive link text (avoid dumping raw URLs unless the URL itself is the reference).

### R4 — Anchors

- Avoid deep anchor links unless the section is stable.
- Keep heading titles simple to reduce renderer-specific anchor differences.

### R5 — Code blocks

- Fenced code blocks must be balanced (opening/closing fences match).
- Add a language tag when possible (e.g. `yaml`, `json`, `bash`, `text`).

### R6 — Frontmatter

- Only use YAML frontmatter when the file format expects it.
- If frontmatter exists, it must be valid YAML wrapped in `---` lines.

### R7 — Safety and hygiene

- Do not include secrets, tokens, credentials, or sensitive logs.
- Keep edits minimal: do not rewrite unrelated sections.

### R8 — Lists and readability

- Use `-` for unordered lists.
- Keep bullets short and scannable; avoid deep nesting unless it improves clarity.

### R9 — Tables

- Prefer tables only when they improve comparison; avoid very wide tables (use bullets instead).

---

## Common Markdown Pitfalls (Avoid)

- Broken relative links after renames/moves (always re-check targets).
- Inconsistent heading casing that creates near-duplicates (hurts search and navigation).
- Over-wide tables (hard to read in GitHub; prefer bullets if the table exceeds typical width).
- Copy-pasted logs containing secrets, tokens, or internal URLs.

## Templates (Use When Applicable)

### Documentation page template

```markdown
# <Title>

## Purpose
<What this document is for, in 1–3 sentences>

## Audience
<Who should read this>

## Workflow / Process
1. <Step>
2. <Step>

## References
- <links>
```

### ADR template (minimal)

```markdown
# ADR-XXXX — <Title>

## Status
Proposed | Accepted | Superseded by ADR-YYYY

## Context
<Why we needed to decide>

## Decision
<What we decided, one sentence>

## Consequences
<What changes; what becomes easier/harder>
```

---

## Review Checklist (For Critics and Self-Review)

- [ ] One `#` title at top; headings are unique and ordered.
- [ ] No broken links to repo files; link paths use `/`.
- [ ] Fenced code blocks are balanced; language tags are present where relevant.
- [ ] The doc is skimmable: short sections, short bullets, minimal redundancy.
- [ ] No secrets, tokens, or sensitive logs embedded.
- [ ] Changes are minimal and do not rewrite unrelated sections.

---

## Standard Checks (Optional, Recommended)

Use these when you want a repeatable “doc QA” pass. If the repo does not have these tools configured, treat this section as guidance (do a manual check instead).

- **Markdown lint**: catch common Markdown style issues (headings, fences, spacing).
- **Spell check**: catch typos and inconsistent terminology (especially in headings).
- **Link check**: validate external URLs (best-effort) and internal relative links.

Suggested tooling (choose one set; do not require all):

- `markdownlint-cli2` (Markdown lint)
- `cspell` (spell check)
- `lychee` (link check)

Minimum manual equivalent if you cannot run tools:

- Re-scan headings: one `#`, no skipped levels, no duplicates.
- Re-scan all new/edited links: open targets; fix path separators and casing.
- Re-scan code fences: ensure opening/closing fences match; add language tags.

---

## References

- Agent file and repo context standards: `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` (A1.1)
- VS Code Copilot customization overview: https://code.visualstudio.com/docs/copilot/customization/overview
