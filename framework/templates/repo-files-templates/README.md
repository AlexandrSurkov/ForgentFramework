# Repo Files Templates — Ideal Multi-Agent Repo (Copilot-Native)

This folder contains **standardized templates** for the “ideal” repository structure described in [framework/spec/guide-copilot-native-multi-agent-repo-structure.md](../../spec/guide-copilot-native-multi-agent-repo-structure.md).

## How to use

1. Copy the contents of the [root](root) folder into your repository root.
2. Replace all placeholder values marked as `TODO:`.
3. Keep the directory structure intact; adjust only when you have an explicit reason.

## What is included

- Repo-context files: `AGENTS.md`, `llms.txt`, optional `CLAUDE.md`
- Copilot discovery surface: `.github/agents/`, `.github/prompts/`, `.github/instructions/`, `.github/decisions/`
- Agent runtime artifacts: `.agents/skills/`, `.agents/evals/`, `.agents/traces/`, `.agents/session/`
- A2A profile stub under `.agents/a2a/`
- AgentConfig docs: `framework/00-multi-agent-development-spec.md`, `PROJECT.md`, `.vscode/`, `domain/`

## Notes

- Some formats are platform-dependent (notably MCP and hooks). Where schemas vary across products/versions, the templates are provided as `.jsonc` “fill-in” stubs.
- This library intentionally avoids real secrets, credentials, or logs.

