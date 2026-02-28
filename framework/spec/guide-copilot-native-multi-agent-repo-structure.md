# Copilot-native multi-agent repo structure (guide)

This document describes an “ideal” repository structure for VS Code Copilot Agent Mode projects.
It is **Copilot-native** (i.e., built around `.agent.md`, prompt files, and custom instructions).

This repo uses this guide as a **non-normative reference**; the normative rules live in the infrastructure module.

## Relationship to the umbrella spec

The canonical umbrella spec entrypoint is [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md).

This guide is **integrated into the spec** via the infrastructure module:

- §0.1 ([00-infrastructure.md](00-infrastructure.md)) **inherits and extends** the structure described here.
- This file remains **non-normative** (a human-friendly reference). When something must be enforced, §0.1 is the source of truth.

This guide exists to:

- Provide a concrete, human-friendly “ideal structure” reference.
- Offer a template library for bootstrapping new repos.
- Keep the spec focused on enforceable rules, not directory aesthetics.

---

## Ideal structure

```text
.
├─ AGENTS.md
├─ llms.txt
├─ PROJECT.md
├─ framework/
│  ├─ 00-multi-agent-development-spec.md
│  ├─ spec/
│  │  ├─ appendices/
│  │  └─ ...
│  └─ templates/
├─ .github/
│  ├─ agents/
│  ├─ instructions/
│  ├─ prompts/
│  ├─ hooks/
│  ├─ decisions/
│  └─ copilot-instructions.md
├─ .agents/
│  ├─ skills/
│  ├─ evals/
│  ├─ traces/
│  └─ session/   # gitignored
└─ .vscode/
   └─ settings.json
```

Notes:

- `.github/agents/` contains all `.agent.md` definitions.
- `.github/prompts/` contains reusable `.prompt.md` prompts.
- `.github/instructions/` contains scoped instruction files.
- `.agents/` contains skills, evals, traces, and runtime session state.

---

## Standard Template Library

This repo includes templates under:

- [framework/templates/repo-files-templates/](../templates/repo-files-templates/)

These templates are intentionally “boring” and standardised:

- Root context files (`AGENTS.md`, `llms.txt`, `PROJECT.md`)
- `.github/` structure (`agents/`, `instructions/`, `prompts/`, `hooks/`, `decisions/`)
- `.agents/` folders (`skills/`, `evals/`, `traces/`)

---

## Prompt and instruction conventions

### Agent definitions (`.agent.md`)

Store agents in `.github/agents/`.

Minimum conventions:

- Use explicit tool lists.
- Include a clear “edit vs advise” protocol when needed.
- Keep system prompts short and enforceable.

### Prompt files (`.prompt.md`)

Store prompts in `.github/prompts/`.

Prompt files should:

- Be reusable and parameterized.
- Avoid embedding secrets or environment-specific content.
- Prefer linking to repo files over pasting large text blobs.

### Custom instructions (`copilot-instructions.md`)

Store workspace-level instructions in `.github/copilot-instructions.md`.

Keep it short:

- Repo purpose
- Non-negotiable constraints
- Links to key files

---

## Trace, eval, and session artifacts

This guide assumes:

- **Skills** live in `.agents/skills/`.
- **Golden tests** live in `.agents/evals/`.
- **Traces** live in `.agents/traces/`.
- **Session state** lives in `.agents/session/` (gitignored).

Do not commit trace JSONL files (`.agents/traces/*.jsonl`).

Minimum trace hygiene:

- Required fields aligned with OTel/GenAI conventions (timestamps, trace/span ids, agent name, operation, tool name where applicable)
- Redaction rules (never record secrets, API keys, full env dumps, or raw tool output that may contain sensitive data)
- Retention/rotation policy (e.g., keep last N traces or last N days)
- Export policy (if needed): keep traces local-only or export to an external secure log store

If you must retain traces for compliance, prefer an external secure log store.

## Suggested `.gitignore` additions

```gitignore
# Copilot / agent runtime artifacts
.agents/session/
.agents/traces/*.jsonl
!.agents/traces/README.md
```

## References

- VS Code Copilot documentation (Customization):
  - [Customization overview](https://code.visualstudio.com/docs/copilot/customization/overview)
  - [Custom instructions](https://code.visualstudio.com/docs/copilot/customization/custom-instructions)
  - [Prompt files](https://code.visualstudio.com/docs/copilot/customization/prompt-files)
  - [Custom agents](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
  - [Agent Skills](https://code.visualstudio.com/docs/copilot/customization/agent-skills)
  - [MCP servers](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
  - [Hooks](https://code.visualstudio.com/docs/copilot/customization/hooks)
  - [Language models](https://code.visualstudio.com/docs/copilot/customization/language-models)
- Agent Skills standard: [agentskills.io](https://agentskills.io)
- Repository context formats:
  - [agents.md](https://agents.md)
  - [llmstxt.org](https://llmstxt.org)
