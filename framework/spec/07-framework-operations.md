# 7. Framework Operations

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

This module describes how to use the framework in three operational tasks:

- Install (apply the spec to a repo)
- Upgrade (sync a repo to a newer spec version)
- Remove (stop using the framework)

For the detailed, phase-by-phase implementation workflow, see the Adoption Roadmap module: [06-adoption-roadmap.md](06-adoption-roadmap.md).

---

## Install

Goal: apply the framework to a repository (typically an AgentConfig repo) so agents have consistent prompts, skills, and governance.

Checklist:

```text
- [ ] Add the `framework/` package to the repo root (vendored copy of the spec modules).
- [ ] Create `PROJECT.md` at the repo root (next to `framework/`) using the template in the Infrastructure module: [00-infrastructure.md §0.8](00-infrastructure.md#08-projectmd--project-file-template).
- [ ] Fill `PROJECT.md` → `## §pre: Project parameters` (see the questions in the Adoption Roadmap module).
- [ ] Run the Implementation Agent prompt from the Adoption Roadmap module to create the agent system files.
- [ ] Review diffs before committing; commit the resulting file set.
```

Notes:

- Templates for `PROJECT.md`, `AGENTS.md`, `llms.txt`, and other baseline files are defined in [00-infrastructure.md](00-infrastructure.md).
- The Implementation Agent prompt is defined in [06-adoption-roadmap.md](06-adoption-roadmap.md) under “Implementation Agent prompt”.

---

## Upgrade

Goal: update an existing repo that already uses the framework so it matches a newer spec version.

Checklist:

```text
- [ ] Identify versions:
      - NEW: `framework/00-multi-agent-development-spec.md` header.
      - OLD: `PROJECT.md` header and `PROJECT.md` §pre (“Spec version: vX.Y.Z”).
- [ ] Read `framework/CHANGELOG.md` and summarize the delta (BREAKING vs ADDITIVE).
- [ ] Update the vendored `framework/` package (replace it with the newer version).
- [ ] Run the Spec Upgrade Agent prompt from the Adoption Roadmap module.
- [ ] If any `.github/agents/*.agent.md` changed:
      - record changes in `.github/AGENTS_CHANGELOG.md`
      - run golden tests if your repo has them configured (see the Prompt Versioning module)
- [ ] Update `PROJECT.md` to record the new spec version.
```

References:

- Upgrade procedure prompt: [06-adoption-roadmap.md](06-adoption-roadmap.md) (“Spec upgrade agent prompt”).
- Change control for agent prompts: [05-prompt-versioning.md](05-prompt-versioning.md).

---

## Remove

Goal: stop using the framework in a repo.

Safety rules:

- Review diffs before deleting files.
- Prefer committing removals as a single, reviewable change.
- Only delete files that were introduced solely for this framework (keep anything that your repo has repurposed).

### Minimal removal (spec-only)

Use this mode when you only want to remove the spec package, but you are intentionally keeping existing agent files.

Checklist:

```text
- [ ] Remove the vendored spec package:
      - delete `framework/` (or the subset of `framework/` that you introduced).
- [ ] Remove any repo governance files that were introduced solely to manage the vendored spec (if present).
      Examples: `.github/SPEC_VERSIONING.md`, `.github/workflows/spec-versioning.yml`.
- [ ] Audit retained repo artifacts for references to removed `framework/` paths; remove or update those references to avoid broken links.
      Examples: `.github/copilot-instructions.md`, `.github/agents/**`, `.agents/skills/**`, `PROJECT.md`, `AGENTS.md`, `llms.txt`, `.vscode/**`.
- [ ] Remove or update any documentation that points to `framework/` paths (README, runbooks).
```

### Full cleanup (spec + agent system files)

Use this mode when you want to remove both the spec package and the agent system scaffolding it introduced.

Checklist:

```text
- [ ] Do the “Minimal removal (spec-only)” steps.

- [ ] Remove agent system scaffolding (only if introduced solely for this framework; keep anything your repo repurposed):
      - Root files:
         - `PROJECT.md`
         - `AGENTS.md`
         - `llms.txt`
      - `.gitignore`:
         - remove or update ignore entries related to the agent system (commonly `.agents/session/`; and `.agents/traces/` if you are no longer using it).
      - `.vscode/` workspace files:
         - `.vscode/<project>.code-workspace` (remove workspace folder entries / settings that reference removed folders)
         - `.vscode/settings.json` (remove `chat.agentFilesLocations` entries that point to `.github/agents`)
         - `.vscode/extensions.json` (if it was introduced solely for the agent workspace)
         - `.vscode/mcp.json` (if it was introduced solely for agent MCP servers)
      - `.github/` agent + governance files:
         - `.github/copilot-instructions.md`
         - `.github/AGENTS_CHANGELOG.md`
         - `.github/agents/` (all `*.agent.md`)
         - `.github/instructions/` (if present)
         - `.github/prompts/` (if present)
         - `.github/hooks/` (if present)
         - `.github/decisions/` (if present)
         - `.github/pull_request_template.md` (if introduced by the framework)
      - `.agents/` runtime + skills:
         - `.agents/skills/`
         - `.agents/traces/` (only remove if your trace mode does not use committed traces)
         - `.agents/evals/` (if you adopted golden tests)
         - `.agents/a2a/` (optional; if adopted)
      - `domain/` (only if it was introduced solely for this framework)

- [ ] Optional local cleanup:
      - `.agents/session/` is usually gitignored; you MAY delete it locally to remove `TASK_CONTEXT.md` history.
```
