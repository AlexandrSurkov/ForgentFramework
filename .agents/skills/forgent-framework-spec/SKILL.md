# SKILL: ForgentFramework-Spec

> Maintains and evolves `MULTI_AGENT_SPEC.md` and related documentation in this repository.

## When to Use This Skill
- The task modifies `MULTI_AGENT_SPEC.md`, `README.md`, `AGENTS.md`, or `llms.txt`.
- The task adds/changes the agent definitions in `.github/copilot/agents/`.
- You need to validate Markdown formatting or spec consistency.

## Tech Stack
| Role | Technology | Version | Notes |
|---|---|---|---|
| Primary artifact | Markdown | n/a | Long specification document |
| Tooling | Python | 3.x | Dependency-free helper scripts in `tools/` |

## Build & Test Commands
```bash
# Validate the spec Markdown (fences/headings)
python tools/validate_spec.py

# Optional: validate agent prompt contracts ("golden checks")
python tools/validate_agents.py

# Optional: audit local Markdown links (no network)
python tools/link_audit.py
```

## Key Conventions
- `MULTI_AGENT_SPEC.md` is canonical; edits must be minimal and must not change intent unless explicitly requested.
- Keep committed artifacts in English.
- Avoid large reflows/re-wrapping; prefer targeted edits.
- Prefer adding precise examples/mechanisms over new abstract rules.

## Common Patterns
- For a rule change: update the rule text + update any examples referencing it.
- For formatting issues: fix Markdown structure (lists/headings/fences) without rewriting content.

## Out of Scope
- Implementing product code (this repo is a framework/spec repo).
- Adding networked automation or CI unless explicitly requested.

## References
- [AGENTS.md](../../../AGENTS.md)
- [MULTI_AGENT_SPEC.md](../../../MULTI_AGENT_SPEC.md)
- [README.md](../../../README.md)
