# Evals (Template)

This directory contains evaluation assets for agents and prompts.

## Policy

- If you maintain eval suites, changes to `.github/agents/`, `.github/prompts/`, `.agents/skills/`, or `.agents/evals/` SHOULD run evals.

Note: running evals usually requires direct access to an LLM provider API supported by promptfoo.

## Running

- Run all eval suites:
	- `npx promptfoo eval -c ".agents/evals/*-promptfooconfig.yaml"`

- Or run one suite:
	- `npx promptfoo eval --config .agents/evals/<agent>-promptfooconfig.yaml`

