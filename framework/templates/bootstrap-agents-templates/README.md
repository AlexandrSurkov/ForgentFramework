# Bootstrap Agents Templates (Group 2)

This template subtree contains **Group 2 (bootstrap) agent definitions**.

## Goal

Provide a ready-to-merge bootstrap agent set that can perform framework **install / upgrade / remove** operations.

## How to use

Copy/merge the contents of:

- `framework/templates/repo-files-templates/root/` (repo artifacts)
- `framework/templates/bootstrap-agents-templates/root/` (bootstrap agents)

…into the target repository root.

## Included agents

These are intended to be placed under `.github/agents/`:

- `bootstrap-orchestrator` (routes operations + runs executor/critic loop)
- `bootstrap-installer` (install)
- `bootstrap-upgrader` (upgrade)
- `bootstrap-remover` (remove)
- `bootstrap-critic` (enforces boundaries + AWESOME-COPILOT gate)
