# Bootstrap Agents Templates (Group 2)

This template subtree contains **Group 2 (bootstrap) agent definitions**.

## Goal

Provide a ready-to-merge bootstrap agent set that can perform framework **install / upgrade / remove** operations.

Bootstrap behavior is remediation-aligned:

- **Discovery-first**: executors must exhaust repository discovery before asking user questions.
- **Evidence-based autofill**: dry-run/apply outputs must use canonical DRY_RUN markers and required tables from Operations §7.2.
- **Ask only unresolved TODOs**: user questions are allowed only for TODO items that remain unresolved after exhaustive discovery.

The `bootstrap-orchestrator` template is designed to be chat-transparent: it always prints an upfront plan, and prints a short pre/post message around each subagent invocation.

This includes calls to the critic (`bootstrap-critic`): the orchestrator must emit both the pre-call context line and the post-call result summary for every subagent call.

Stage markers for critic reviews are deterministic and exact:

- `Review stage: DRY_RUN`
- `Review stage: APPLIED_RESULT`

DRY_RUN artifacts are deterministic and MUST follow canonical Operations §7.2 exactly:

- Stage markers in exact order: `[DISCOVERY]` → `[UNRESOLVED]` → `[QUESTIONS]` → `[PLAN]`
- Required table schemas in exact order:
	1. Discovery Evidence Table: `evidence_id | source_path_or_command | observation | inference | confidence | fills_todo_id`
	2. Unresolved TODO Table: `todo_id | description | why_unresolved_after_discovery | blocking_stage | required_input`
	3. Question Mapping Table: `question_id | maps_to_todo_id | question_text | accepted_answer_format | unblocks_stage`

No alternative marker names, table names, column sets, or ordering are allowed.

The critic rejects ambiguous/missing stage markers and dry-runs that ask unnecessary user questions or omit unresolved/evidence artifacts.

## How to use

Copy/merge the contents of:

- `repo-files-templates/root/` (repo artifacts)
- `bootstrap-agents-templates/root/` (bootstrap agents)

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
