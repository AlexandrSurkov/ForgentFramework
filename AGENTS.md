# ForgentFramework — AGENTS

## Product Overview

ForgentFramework is a technology-agnostic Multi-Agent Development Specification for running real software projects with an Orchestrator/Executor/Critic workflow. It defines roles, phase gates, critique rubrics, memory conventions, and observability practices that can be applied to any stack. This repository is the source of truth for the spec itself and the agent setup used to maintain it.

## Repository Map

| Repo             | Contents                                                                                           |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| ForgentFramework | The canonical spec (`MULTI_AGENT_SPEC.md`), repo-level agent setup, and helper scripts             |

## Commit Conventions (Conventional Commits)

- `feat(<scope>):` — MINOR version bump
- `fix(<scope>):`  — PATCH version bump
- `chore:`         — dependencies/config (no version bump)
- `refactor:`      — no behavior change (no bump)
- `docs:`          — documentation only
- `BREAKING CHANGE` (footer) — MAJOR version bump

## Branching Strategy: GitFlow

[See MULTI_AGENT_SPEC.md §0.5 for detailed rules]

- `main`: production-ready, tagged `vX.Y.Z`
- `develop`: integration branch
- `feature/<task-id>-<description>`: from `develop` → `develop`
- `release/X.Y.Z`: from `develop` → `main` + `develop`
- `hotfix/<description>`: from `main` → `main` + `develop`

## PR Policy

Every merge via Pull Request. See `.github/pull_request_template.md`.
Squash merge. Feature branch deleted after merge.

## ADR Index

No ADRs yet in this repository.

- Create new ADRs under `.github/decisions/` as `ADR-XXX-title.md` when a spec change introduces a durable architectural/process decision.
