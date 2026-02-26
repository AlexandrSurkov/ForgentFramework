---
name: agent-file-standards
description: "Operational checklists for every repo file format defined in A1.1: .agent.md, AGENTS.md, llms.txt, SKILL.md, ADR, OTel trace, mcp.json, .prompt.md, CLAUDE.md. Load when creating or reviewing any of these file types."
---

# SKILL: Agent File Standards (A1.1)

> Universal skill. Load whenever creating, editing, or reviewing any standard repo file:
> `.agent.md`, `AGENTS.md`, `llms.txt`, `SKILL.md`, `ADR`, trace files, `mcp.json`, `.prompt.md`, `CLAUDE.md`.

## When to Load This Skill

- Creating a new agent (`.agent.md`)
- Modifying `AGENTS.md`, `llms.txt`, or `copilot-instructions.md`
- Adding or reviewing a SKILL.md knowledge package
- Recording an architecture decision (ADR)
- Adding an MCP server (`mcp.json`)
- Writing or reviewing OTel trace output
- Any question about which file format to use for a given purpose

---

## `.agent.md` — Creating or Modifying an Agent

**Required frontmatter fields:**
```yaml
---
description: <one-line summary of the agent's role and capability>
name: <kebab-case name matching the file name>
tools: ['readFile', ...]   # minimal set — see least-privilege below
---
```

**Checklist:**
- [ ] `description` is one sentence: role + what it can do (not what it cannot)
- [ ] `tools` is the minimal set for this agent's specific role (least-privilege — A1.6)
- [ ] Critics have read-only tools only: `['readFile', 'fileSearch', 'textSearch']`
- [ ] File name matches `name:` field exactly
- [ ] `AGENTS.md` agent table updated: name, file, mode, role
- [ ] `AGENTS_CHANGELOG.md` entry added
- [ ] `llms.txt` updated if agent is externally visible

**Tool reference by role:**

| Role | Allowed tools |
|---|---|
| Orchestrator | `readFile`, `editFiles` (traces only) |
| Executor (editor) | `readFile`, `editFiles`, `createFiles`, `fileSearch`, `textSearch` |
| Critic | `readFile`, `fileSearch`, `textSearch` |
| Architect / advisor | `readFile`, `editFiles`, `createFiles`, `fileSearch`, `textSearch` |

---

## `AGENTS.md` — Updating the Repo Map

**Checklist (any change to agents or repo structure):**
- [ ] Agent table row: `name`, `file`, `mode`, `role` — all four columns filled
- [ ] Responsibility zones table updated if routing changes
- [ ] `## What lives here` path table updated if files moved
- [ ] `## Active ADRs` section updated if new ADR created
- [ ] No secrets or credentials in the file
- [ ] File is in English

---

## `SKILL.md` — Creating a Knowledge Package

**Required frontmatter:**
```yaml
---
name: <kebab-case>
description: "<one line: what domain + explicit trigger phrases>"
---
```

**Content checklist:**
- [ ] Has `## When to Load This Skill` section (explicit trigger conditions)
- [ ] Content is action-oriented: checklists, tables, examples — not prose summaries
- [ ] Each checklist item is testable (not "write good code")
- [ ] References back to relevant `01-appendix-a1-ai-and-llm-standards.md` section(s)
- [ ] Does NOT duplicate content already in the agent's core prompt
- [ ] Lazy-loading: agent loads this file only when trigger condition is met

---

## `ADR` — Recording an Architecture Decision

**When to create an ADR:**
- Decision is durable (hard to reverse)
- Decision affects more than one agent or file type
- Future agents might repeat this decision without context

**File location:** `.github/decisions/ADR-XXX-<slug>.md`

**Required sections:**
```markdown
# ADR-XXX — <title>

## Status
Proposed | Accepted | Superseded by ADR-YYY

## Context
<Why this decision was needed>

## Decision
<What was decided — one sentence>

## Consequences
<What changes, what becomes easier, what becomes harder>
```

**Checklist:**
- [ ] Status is one of: Proposed / Accepted / Superseded
- [ ] Context explains the problem, not the solution
- [ ] `AGENTS.md` `## Active ADRs` table updated
- [ ] Linked from relevant agent prompts or spec sections if it changes behaviour

---

## OTel Trace Files — Writing Spans

**File naming:** `.agents/traces/<YYYYMMDD>-<slug>.jsonl`

**Required span fields:**
```jsonl
{"ts": "<ISO8601>", "trace_id": "<YYYYMMDD>-<slug>", "span_id": "s<NN>", "parent_span_id": "<s<NN>|null>", "agent": "<name>", "operation": "plan|execute|critique|escalate|complete", ...}
```

**Checklist:**
- [ ] `trace_id` = filename without `.jsonl`
- [ ] Root span has `parent_span_id: null`; all child spans reference root
- [ ] `span_id` increments: `s01`, `s02`, … (zero-padded)
- [ ] `operation` is one of: `plan` / `execute` / `critique` / `escalate` / `complete`
- [ ] Execute spans include `iteration`; critique spans include `blockers` + `warnings`
- [ ] Complete/escalate spans include `total_iterations`
- [ ] Trace file is committed (`.agents/traces/` is NOT gitignored)

---

## `mcp.json` — Adding an MCP Server

**File location:** `.vscode/mcp.json`

**Checklist:**
- [ ] Server name is kebab-case and unique
- [ ] Transport is `stdio` (preferred) or `http`
- [ ] No secrets or API keys inline — use environment variable references
- [ ] `AGENTS.md` `## What lives here` updated if new server is part of the repo
- [ ] Supply chain review: who publishes this server? (OWASP LLM06 — see ai-security SKILL)

---

## `llms.txt` — Updating the LLM Overview

**Update `llms.txt` when:**
- A new agent is added or renamed
- A key file moves or is deleted
- A new SKILL.md is added
- The spec version changes

**Checklist:**
- [ ] All links resolve to actual files in the repo
- [ ] Agent names match `name:` fields in `.agent.md` frontmatter
- [ ] File paths use forward slashes
- [ ] Under ~500 words (it's a quick-reference, not documentation)

---

## File Format Selection Guide

| I want to... | Use |
|---|---|
| Define an agent with tools and system prompt | `.agent.md` |
| Give all agents shared workspace context | `copilot-instructions.md` |
| Give the orchestrator the repo map | `AGENTS.md` |
| Package reusable domain knowledge | `SKILL.md` |
| Share a reusable parametrized prompt | `.prompt.md` |
| Record a durable architectural decision | `ADR` in `.github/decisions/` |
| Connect an external tool to agents | MCP server + `mcp.json` |
| Write an LLM-friendly repo overview | `llms.txt` |
| Log agent execution for audit | OTel trace in `.agents/traces/` |
| Support Claude-based workflows | `CLAUDE.md` |

---

## References

- [framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md — A1.1](../../../framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md)
- [AGENTS.md](../../../AGENTS.md)
- [.agents/traces/README.md](../../traces/README.md)
