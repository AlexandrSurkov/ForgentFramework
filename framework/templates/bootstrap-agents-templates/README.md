# Bootstrap Agents Templates (Group 2)

This template subtree contains **Group 2 (bootstrap) agent definitions**.

## Goal

Provide a ready-to-merge bootstrap agent set that can perform framework **install / upgrade / remove** operations.

The `bootstrap-orchestrator` template is designed to be chat-transparent: it always prints an upfront plan, and prints a short pre/post message around each subagent invocation.

This includes calls to the critic (`bootstrap-critic`): the orchestrator must emit both the pre-call context line and the post-call result summary for every subagent call.

## How to use

Copy/merge the contents of:

- `framework/templates/repo-files-templates/root/` (repo artifacts)
- `framework/templates/bootstrap-agents-templates/root/` (bootstrap agents)

…into the target repository root.

Then, in the merged `.github/agents/**/*.agent.md` files:

- Replace every `model: TODO` with an actual model identifier.

## Included agents

These are intended to be placed under `.github/agents/`:

- `bootstrap-orchestrator` (routes operations + runs executor/critic loop)
- `bootstrap-installer` (install)
- `bootstrap-upgrader` (upgrade)
- `bootstrap-remover` (remove)
- `bootstrap-critic` (enforces boundaries + AWESOME-COPILOT gate)
