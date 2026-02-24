# ForgentFramework — AI Instructions

## Project Overview
This repository contains the canonical multi-agent workflow specification. See [AGENTS.md](../AGENTS.md) for repo conventions and policies.

## Agent Workflow
All multi-step tasks go through the orchestrator.
Pipeline: Phase 0 (specs) -> 1 (code) -> 2 (tests) -> 2.5 (deploy) -> 3 (refactor) -> 3.5 (regression) -> 4 (arch) -> 5 (security) -> 6 (docs).
See: `MULTI_AGENT_SPEC.md` for the full protocol.

## Key Constraints
- Language: all committed artifacts and code comments in English. Chat with the user in Russian.
- Treat `MULTI_AGENT_SPEC.md` as the canonical source of truth; avoid changing meaning unintentionally.
- Keep edits surgical; do not reflow/reformat unrelated sections.
- No hardcoded secrets or credentials in any committed file.

## Active ADR
None in this repository.

## Current Sprint / Focus
- Maintain internal consistency (terminology, iteration rules, trace examples).
- Improve maintainability (validation scripts, clear agent roles).
