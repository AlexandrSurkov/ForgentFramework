# framework/00-multi-agent-development-spec.md (Template)

This repository is an **AgentConfig** repo.

This file must contain the **Multi-Agent Development Specification** used by your project.

## How to use

1. Copy the latest spec into this file (umbrella entrypoint).
2. Copy the spec modules next to it under `framework/spec/`.
3. Pin the spec version in PROJECT.md.
4. Treat this file as normative: agents should follow it exactly.

## Source of truth

If you are using ForgentFramework as the upstream spec source, copy:

- `framework/00-multi-agent-development-spec.md`
- `framework/spec/` (all modules)
- `framework/spec/appendices/` (standards and references)

This includes the non-normative repo-structure guide:

- `framework/spec/guide-copilot-native-multi-agent-repo-structure.md`

into your AgentConfig repo under `framework/`.
