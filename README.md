# ForgentFramework

A lightweight, technology-agnostic **Multi‑Agent Development Specification** for running real software projects with an Orchestrator/Executor/Critic workflow.

This repository is intentionally minimal: it contains the canonical specification document and (optionally) helper tooling.

## What this is

- A universal, stack-independent spec that defines:
  - Agent roles and responsibilities (Orchestrator / Executors / Critics)
  - A phase-based delivery pipeline (spec-first → implementation → verification)
  - PR quality gates and critique rubrics (including security and documentation)
  - Session memory conventions (`TASK_CONTEXT.md`) and re-entry protocol (`NEEDS_HUMAN`)
  - Observability guidance (JSONL trace structure aligned with OTel GenAI concepts)
  - Upgrade procedures when the spec version changes

It is **not** an application or library. You don’t “run” it; you apply it to other repositories.

## Repository contents

- `MULTI_AGENT_SPEC.md` — the canonical specification (version header inside the file).
- `AGENTS.md` / `llms.txt` — agent-readable repository context.
- `.github/copilot/agents/` — declarative agent definitions (`*.agent.md`) for maintaining this framework.
- `tools/` — small helper scripts (validation/audits).

## Quick start (apply to a project)

1. Open `MULTI_AGENT_SPEC.md` and go to **Quick Start**.
2. Create a project-specific `PROJECT.md` next to the spec using the template referenced in the spec.
3. Run the “Implementation Agent” system instruction from the spec’s Quick Start to execute the adoption roadmap.

After that, your target project should have the required agent files, rubrics, traces, and the working agreements needed for day-to-day use.

## Agents (for maintaining this repository)

This repo includes a minimal agent set that follows the structure defined in `MULTI_AGENT_SPEC.md`:

- Orchestrator: `.github/copilot/agents/forgent-framework-orchestrator.agent.md`
- Executors: spec editing and tooling
- Critics: process consistency and documentation quality

VS Code is configured to discover these agent files via `.vscode/settings.json`.

## Workflow (working on this framework)

Use an orchestrator-first workflow:

1. **Start with the orchestrator** (single entry point) and describe the goal and acceptance criteria.
2. The orchestrator assigns an **executor** (make changes) and then runs the relevant **critic(s)** (review the result).
3. If a critic returns `REQUEST_CHANGES`, iterate (max 3 times per subtask). If still not `APPROVE` after 3 iterations, escalate to `NEEDS_HUMAN`.
4. After all critics `APPROVE`, run **final verification** (see **Validation** below).

## Working on this repository

This repository *is* the framework. Most changes are either spec edits, agent prompt edits, or small maintenance tooling.

### What to change where

- **Canonical specification:** `MULTI_AGENT_SPEC.md`
- **Repo conventions for humans/agents:** `README.md`, `AGENTS.md`, `llms.txt`
- **Agent definitions (VS Code Copilot agents):** `.github/copilot/agents/*.agent.md`
- **Agent prompt changelog:** `.github/AGENTS_CHANGELOG.md`
- **Architecture decisions (long-term memory):** `.github/decisions/ADR-*.md`
- **Helper scripts:** `tools/` (keep dependency-light)

### Suggested change cycle

1. Create a feature branch.
2. Start with `@forgent-framework-orchestrator` and include acceptance criteria.
3. Let the orchestrator run an executor + the relevant critic(s).
4. Run the validation command(s) below.
5. Open a PR using `.github/pull_request_template.md`.

### Examples (copy/paste)

#### 1) Spec change (and validate)

```text
@forgent-framework-orchestrator
Update MULTI_AGENT_SPEC.md:
- Goal: clarify the difference between NEEDS_HUMAN and ESCALATED.
- Constraints: keep meaning consistent with existing sections; minimal diff.
- Done when: process-critic and docs-critic both APPROVE, and python tools/validate_spec.py passes.
```

#### 2) Agent prompt change

```text
@forgent-framework-orchestrator
Update the orchestrator workflow rules in its .agent.md prompt.
Constraints: minimal diff; no unrelated changes.
Done when: process-critic APPROVE and the change is recorded in .github/AGENTS_CHANGELOG.md.
```

#### 3) Tooling change (scripts in tools/)

```text
@forgent-framework-orchestrator
Add a small dependency-free helper in tools/ that checks for broken Markdown links.
Constraints: Windows-friendly; no network calls; clear exit codes.
Done when: process-critic APPROVE and example usage is added to README.
```

#### 4) Run critics explicitly on a prepared change

```text
@forgent-framework-process-critic
Review my changes to MULTI_AGENT_SPEC.md for contradictions and enforceability.
Return a Critique Report with file/section locations.
```

```text
@forgent-framework-docs-critic
Review my changes to MULTI_AGENT_SPEC.md for Markdown structure and documentation quality.
Return a Critique Report with file/section locations.
```

#### 5) Minimal “Definition of Done” check

```bash
python tools/validate_spec.py
```

### Updating agent prompts

If you change any `.github/copilot/agents/*.agent.md` file:

- Keep changes minimal and behavior-focused.
- Record the change in `.github/AGENTS_CHANGELOG.md` (type: behavior/model/tools/fix).
- Run **Validation** (and any additional checks introduced by the prompt change).

## Validation

Run this after changing `MULTI_AGENT_SPEC.md` to catch broken Markdown fences and obvious structural issues:

```bash
python tools/validate_spec.py
```

Optional checks:

```bash
# Lightweight “golden checks” for agent prompts (structure/required rules)
python tools/validate_agents.py

# Audit local Markdown links (no network)
python tools/link_audit.py
```

## Upgrading

When `MULTI_AGENT_SPEC.md` changes, follow the “Upgrade an existing project” procedure in the spec. The expected baseline is recorded in the target project’s `PROJECT.md` as the previously used spec version.

## Contributing

If you evolve the spec:

- Keep changes precise and audit-friendly (this is a process document).
- Update the spec version and “Updated” date in the header.
- Prefer small, reviewable commits (Conventional Commits are referenced by the spec).

## License

No license file is included in this repository snapshot. If you plan to share it publicly, add an explicit `LICENSE` file and align it with your intended usage.
