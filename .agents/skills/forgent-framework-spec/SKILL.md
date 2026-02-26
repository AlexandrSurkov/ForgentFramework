---
name: forgent-framework-spec
description: "Index + fast lookup map for the framework spec (framework/00-multi-agent-development-spec.md and framework/spec/*). Use to locate the right module/section quickly; still open the exact file/section to confirm current wording. Trigger phrases: framework spec, 00-multi-agent-development-spec, spec module, where is the rule, rubrics, observability, sessions/memory, prompt versioning, adoption roadmap."
---

# SKILL: Forgent Framework Spec Map

## When to Load This Skill

Load this skill when the user asks:

- “Where in the spec is …?” / “Which file defines …?”
- Anything explicitly referencing `framework/00-multi-agent-development-spec.md`
- How to find a rule across `framework/spec/*` modules (infrastructure, sessions, observability, rubrics)
- Which rubric governs a critic/executor/orchestrator behaviour

Do NOT use this skill as a substitute for reading: use it to jump to the right file, then open the relevant section and quote/verify.

---

## Umbrella vs Modules

- **Umbrella index (entrypoint):** `framework/00-multi-agent-development-spec.md`
  - Use for: table of contents, quick links, and canonical module locations.
  - Not the place for full details (intentionally short).

- **Normative modules:** `framework/spec/`
  - Use for: the actual rules, templates, and protocols.

---

## Fast Lookup: “If the question is about X, open Y”

| Topic | Canonical file/directory |
|---|---|
| Repo layout, AgentConfig structure, workspaces, README/AGENTS/llms.txt requirements, PR policy | `framework/spec/00-infrastructure.md` |
| System architecture diagrams, role boundaries (conceptual) | `framework/spec/01-architecture.md` |
| Sessions, memory rules, `TASK_CONTEXT.md`, Reflexion loop mechanics | `framework/spec/02-sessions-and-memory.md` |
| Rubrics: constitutional principles + critic report format + specific critic checklists | `framework/spec/03-rubrics/` |
| Tracing / spans / `trace_id`, trace retention, OTel-GenAI-ish JSONL format | `framework/spec/04-observability.md` |
| Prompt versioning, `AGENTS_CHANGELOG.md`, change control | `framework/spec/05-prompt-versioning.md` |
| Adoption steps, setup interview, glossary, upgrade guidance | `framework/spec/06-adoption-roadmap.md` |
| “Ideal Copilot-native repo layout” guidance (non-normative) | `framework/spec/guide-copilot-native-multi-agent-repo-structure.md` |

---

## Common Questions → Canonical Section

Use this as a fast “jump table”. After jumping, always open the exact section and verify wording.

| Question / intent | Open |
|---|---|
| “How do I apply the spec to a new project?” | `framework/00-multi-agent-development-spec.md` → Quick Start; then `framework/spec/06-adoption-roadmap.md` |
| “What is the AgentConfig repo supposed to contain?” | `framework/spec/00-infrastructure.md` → §0.1 |
| “How do multi-root workspaces work?” | `framework/spec/00-infrastructure.md` → §0.2 |
| “Do we need AGENTS.md in every repo?” | `framework/spec/00-infrastructure.md` → §0.3 |
| “What is llms.txt and what must it include?” | `framework/spec/00-infrastructure.md` → §0.4 |
| “What are GitFlow + SemVer rules here?” | `framework/spec/00-infrastructure.md` → §0.5 |
| “PR policy / required PR template?” | `framework/spec/00-infrastructure.md` → §0.6 |
| “README requirements (root vs module)?” | `framework/spec/00-infrastructure.md` → §0.7 |
| “What must PROJECT.md contain?” | `framework/spec/00-infrastructure.md` → §0.8 |
| “What is the 9-phase development pipeline?” | `framework/spec/01-architecture.md` → §1.3.3 |
| “When does the user intervene / NEEDS_HUMAN flow?” | `framework/spec/01-architecture.md` → §1.3.5; plus `framework/spec/02-sessions-and-memory.md` → §2.3 |
| “Fast-tracks (docs-only, hotfix, infra-only, etc.)?” | `framework/spec/01-architecture.md` → §1.3.8 |
| “Test failure protocol (RED, coverage, REJECT handling)?” | `framework/spec/01-architecture.md` → §1.3.6 |
| “What is TASK_CONTEXT.md and what’s inside?” | `framework/spec/02-sessions-and-memory.md` → §2.1 |
| “How do parallel sessions work / where is TASK_CONTEXT stored?” | `framework/spec/02-sessions-and-memory.md` → §2.1–§2.2 |
| “What are memory tiers (session vs ADR vs AGENTS.md)?” | `framework/spec/02-sessions-and-memory.md` → §2.2 |
| “Critic isolation rule / what can critics see?” | `framework/spec/03-rubrics/03-critic-rules-and-report-format.md` → Rule 1; also `framework/spec/01-architecture.md` (overview notes) |
| “Critique report format / verdict rules / ACKNOWLEDGED?” | `framework/spec/03-rubrics/03-critic-rules-and-report-format.md` → Verdict rules + ACKNOWLEDGED example |
| “What must the orchestrator do (no paraphrase, trace first, previous attempts)?” | `framework/spec/03-rubrics/01-orchestrator-rules.md` |
| “What is the trace format / fields / where files live?” | `framework/spec/04-observability.md` → §4.5 |
| “Who writes traces and when? trace_id format?” | `framework/spec/04-observability.md` → §4.6 (especially §4.6.1–§4.6.2) |
| “Trace retention / committed vs not committed?” | `framework/spec/00-infrastructure.md` (Trace mode in `.gitignore` guidance); plus `framework/spec/06-adoption-roadmap.md` (trace mode checklist) |
| “How do we version agent prompts / where to log changes?” | `framework/spec/05-prompt-versioning.md` → §5.1 |
| “Do we need golden tests after changing a critic prompt?” | `framework/spec/05-prompt-versioning.md` → §5.2 |
| “What’s the procedure for changing an agent prompt?” | `framework/spec/05-prompt-versioning.md` → §5.3 |

---

## Rubrics Directory Map (03-rubrics)

Use this to jump to the right checklist first:

- `framework/spec/03-rubrics/00-constitutional-principles.md` — global principles (cross-cutting)
- `framework/spec/03-rubrics/01-orchestrator-rules.md` — orchestrator constraints and workflow requirements
- `framework/spec/03-rubrics/02-executor-rules.md` — executor constraints
- `framework/spec/03-rubrics/03-critic-rules-and-report-format.md` — critic report schema + severity rules
- `framework/spec/03-rubrics/04-backend-critic.md` — backend critic checklist
- `framework/spec/03-rubrics/05-devops-critic.md` — devops critic checklist
- `framework/spec/03-rubrics/06-frontend-critic.md` — frontend critic checklist
- `framework/spec/03-rubrics/07-qa-critic.md` — QA critic checklist
- `framework/spec/03-rubrics/08-architect-critic.md` — architect critic checklist
- `framework/spec/03-rubrics/09-security-critic.md` — security critic checklist
- `framework/spec/03-rubrics/10-documentation-critic.md` — documentation critic checklist
- `framework/spec/03-rubrics/11-dor-dod-and-adr-format.md` — DoR/DoD gates + ADR format

---

## Standard Operating Procedure (Spec Lookup)

1. Identify the topic using the table above.
2. Open the canonical module and search within that file (or read the relevant section range).
3. When answering, cite the module/section name (e.g., “Infrastructure §0.7” or “Observability §4.6”).
4. If a conflict exists between guide and module: treat `framework/spec/00-infrastructure.md` §0.1 as normative (it explicitly overrides the guide on conflict).

---

## References

- `framework/00-multi-agent-development-spec.md` (umbrella index)
- `framework/spec/` (normative modules)
