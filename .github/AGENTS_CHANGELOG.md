# AGENTS_CHANGELOG

All changes to `.github/agents/*.agent.md` files and core pipeline behaviour must be recorded here.

| Date | Component | Type | Description | Author |
|---|---|---|---|---|
| 2026-02-25 | all agents | structure | Moved all agent prompts from `agents/*.md` to `.github/agents/forgent-*.agent.md`; updated `.vscode/settings.json` (`chat.agentFilesLocations`) for Copilot discovery | human |
| 2026-02-25 | `forgent-orchestrator` | behavior | Added `analysis/audit` fast-track type and routing rule; explicit `## Previous Attempts` rule; critic framing requirement | human |
| 2026-02-25 | `forgent-docs-critic` | behavior | Added Mode B (Audit executor) — agent can now act as primary executor for read-only analysis tasks | human |
| 2026-02-25 | `forgent-spec-editor` | behavior | Added Reflexion rule: read `TASK_CONTEXT.md` `## Previous Attempts` before each iteration | human |
| 2026-02-25 | `forgent-process-critic` | behavior | Added explicit critic isolation rule: do not read executor chain-of-thought | human |
| 2026-02-25 | `forgent-docs-critic` | behavior | Add ACKNOWLEDGED pattern to output format: APPROVE allowed when WARNINGs explicitly ACKNOWLEDGED; added format definition for ACKNOWLEDGED lines | human |
| 2026-02-25 | `forgent-process-critic` | behavior | Add ACKNOWLEDGED pattern to output format; explicit APPROVE/REQUEST_CHANGES/REJECT conditions; ACKNOWLEDGED line format | human |
| 2026-02-25 | `forgent-orchestrator` | behavior | Add context window management rule (§2.2 item 4): summarise `TASK_CONTEXT.md` at ~200 lines, archive full file | human |
| 2026-02-25 | `forgent-orchestrator` | tools | EDIT TOOL RESTRICTION added: orchestrator writes its own JSONL traces — edit access expanded to `.agents/traces/`; Step 1 now creates `<TRACE_FILE>` alongside `<SESSION_FILE>`; `execute`/`critique`/`complete`/`escalate` spans appended at each pipeline stage | human |
| 2026-02-26 | `forgent-orchestrator` | behavior | Trace format aligned to OTel §4.5–4.6: added `span_id`/`parent_span_id` (span tree), unified `agent` field (dropped separate `executor`/`critic` keys), `iteration` on execute spans, `blockers`/`warnings` on critique spans, `total_iterations` on complete/escalate; trace filename prefix `trace-` removed; orchestrator tracks `<TRACE_ID>` and `<SPAN_SEQ>` counter across the run | human |
| 2026-02-26 | `forgent-advisor` | behavior | New user-invokable advisor agent: multi-agent systems expert for design consultation, spec tradeoff analysis, and framework evolution support. Read-only tools; does not produce executor/critic verdicts. |
| 2026-02-26 | `forgent-advisor` → `forgent-agent-architect` | behavior | Renamed and redesigned: focus shifted from framework consultant to applied AI agent systems architect. Primary knowledge base: `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` (patterns A1.2, file formats A1.1, security A1.3, governance A1.4). Can edit files. Explicit edit-vs-advise protocol and AGENTS_CHANGELOG update obligation added. |
| 2026-02-26 | `forgent-agent-architect` | docs | Updated appendix reference filenames to numeric-prefixed `framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md` (appendices folder aligned with `framework/spec` naming conventions). |
| 2026-02-26 | `forgent-agent-architect` | tools | Added `createFiles` to tools list; updated description to reflect file creation capability. |
| 2026-02-26 | `forgent-agent-architect` | knowledge | Created 2 SKILL.md knowledge packages: `agent-patterns` (A1.2+A1.6 checklists), `ai-security` (A1.3+A1.4 checklists). Activation triggers table updated to reference each SKILL. Fixed A1.5→A1.6 typo in derived principles row. |
| 2026-02-26 | all agents | knowledge | Created universal SKILL `agent-file-standards` (A1.1 operational checklists): `.agent.md`, `AGENTS.md`, `SKILL.md`, ADR, OTel trace, `mcp.json`, `llms.txt`. Registered in `AGENTS.md` § Universal Skills and `copilot-instructions.md`. Added to `forgent-agent-architect` primary knowledge base and activation triggers. |
| 2026-02-26 | `forgent-agent-architect` | knowledge | Created `copilot-vscode` SKILL from VS Code Copilot documentation: all `.agent.md` frontmatter fields, built-in tool names, agent types, subagents, handoffs, MCP config, context engineering, SKILL.md integration. Updated agent description to include VS Code Copilot platform expertise. Added to primary knowledge base and activation triggers. |
| 2026-02-26 | `forgent-agent-architect` | tools | Added network read tools (`fetch`, `webSearch`, `githubRepo`) so the agent can retrieve and verify online Copilot documentation when needed. | |
| 2026-02-26 | all agents | knowledge | Added `markdown-writer` SKILL and updated all `.github/agents/*.agent.md` prompts to load it when creating/editing/reviewing Markdown (`*.md`). | |
| 2026-02-26 | `forgent-agent-architect` | fix | Updated Appendix A1 reference path after moving appendices into `framework/spec/appendices/`. | copilot |
| 2026-02-26 | `forgent-agent-architect` | fix | Updated agent prompt + SKILL references to new Appendix A path under `framework/spec/appendices/`. | copilot |
| 2026-02-26 | `forgent-agent-architect` | knowledge | Removed the root eval SKILL reference; eval guidance relies on A1.5 in the spec. | copilot |
| 2026-02-26 | `forgent-spec-editor`, `forgent-agent-architect` | behavior | Renamed canonical umbrella spec entrypoint to `framework/00-multi-agent-development-spec.md`; updated modules/templates/agents accordingly; removed the legacy umbrella entrypoint file. | copilot |
| 2026-02-26 | `forgent-orchestrator` | behavior | Aligned session file naming to the umbrella spec: uses `.agents/session/TASK_CONTEXT.md` (not per-run suffixed filenames) and records `trace_id`/`trace_file` in the header; long-term trace retention deferred to `PROJECT.md` Trace mode. | copilot |
| 2026-02-26 | `forgent-orchestrator` | behavior | Updated sessions for parallel runs: create per-session `.agents/session/<trace_id>/TASK_CONTEXT.md`, and use collision-resistant `trace_id` (recommended `YYYYMMDDTHHMMSSZ-<slug>-<rand4>`); TASK_CONTEXT header now includes `task_context_file`. | copilot |
| 2026-02-26 | `forgent-spec-editor` | behavior | Updated Reflexion rule to read `TASK_CONTEXT.md` from the orchestrator-provided session file path (typically `.agents/session/<trace_id>/TASK_CONTEXT.md`) rather than a fixed `.agents/session/TASK_CONTEXT.md`. | copilot |
| 2026-02-26 | `forgent-agent-architect` | knowledge | Added `forgent-framework-spec` SKILL: fast lookup index for `framework/00-multi-agent-development-spec.md` and `framework/spec/*` modules; wired into activation triggers for spec location questions. | copilot |

## Change Types

| Type | When to use |
|---|---|
| `behavior` | System prompt/rubric/rule changed — agent behavior changes |
| `model` | Agent model changed |
| `tools` | A tool was added/removed |
| `fix` | Typos/clarifications without behavior change |
| `spec-upgrade` | Sync to a new spec version |
