# Multi-Agent Development Specification

> **Version:** 0.21.0 · **Updated:** 2026-02-24

> This is a universal specification: it defines principles, protocols, and critique rubrics **independent of technology**.
> Project-specific application (stack, models, prompts, technology-specific rubric triggers) lives in a separate file placed next to it (e.g., `PROJECT.md`).
> The critical rubrics in this file define **principles**; the project file complements them with **concrete triggers** for the technologies in use and implements everything marked in this spec as “defined in the project file”.

---

## 🚀 Quick Start

### Apply the spec to a new project

**Step 1.** Create a `PROJECT.md` file in the same folder as this file (`<project>-AgentConfig/PROJECT.md`).
Copy the template from §0.8.1 into it and fill the `## §pre: Project parameters` section using the questions from §6.pre.
Replace `...` with real values for your project.

> **Don’t want to fill it manually?** Use the prompt interview below — paste it into Copilot Chat:
>
> ```
> You are a Project Setup Interviewer. Ask me the questions from section §6.pre of MULTI_AGENT_SPEC.md
> one by one (or in small groups). Based on my answers, create PROJECT.md using the template in §0.8.1
> in the <project>-AgentConfig/ folder next to MULTI_AGENT_SPEC.md and fill the §pre section.
> Speak with me in Russian. Start with the first question.
> ```

**Step 2.** Copy the prompt below and run it as the system instruction for Copilot Chat / an agent:

```
You are an Implementation Agent. Read MULTI_AGENT_SPEC.md (this specification) and PROJECT.md
(§pre answers are already filled). Execute Roadmap §6.0–6.8 sequentially.
Start with Phase 0 and ask for confirmation before each next step.
The full prompt with rules is in §6.agent of this file.
```

> Result: all agents, SKILL.md, MCP, golden tests, and traces are set up — the project is ready to work.

---

### Upgrade an existing project to a new spec version

> Use this when `MULTI_AGENT_SPEC.md` has changed, but your project was set up using an older version.
> The setup baseline is recorded in `PROJECT.md` → field `MULTI_AGENT_SPEC version: vX.Y.Z`.

**Step 1.** Ensure `PROJECT.md §pre` includes `MULTI_AGENT_SPEC version: vOLD`.
If it doesn’t, set the current spec version manually as a baseline before upgrading.

**Step 2.** Copy the prompt below and run it as the system instruction for Copilot Chat / an agent:

```
You are a Spec Upgrade Agent. MULTI_AGENT_SPEC.md has been updated.
Read the new MULTI_AGENT_SPEC.md and PROJECT.md (the field MULTI_AGENT_SPEC version: is the old version).
Follow the upgrade procedure in §6.agent.2: identify the delta, classify changes
(BREAKING / ADDITIVE), apply updates to project files, run golden tests, and update the version in PROJECT.md.
```

> Result: agents, rubrics, and configs are synchronized with the new spec; changes are recorded in `AGENTS_CHANGELOG.md`.

---

## Table of Contents

- [A. Standards and References](#a-standards-and-references)
  - [A.1 Agent file-structure standards](#a1-agent-file-structure-standards)
  - [A.2 Academic Executor/Critic patterns](#a2-academic-executorcritic-patterns)
  - [A.3 Engineering standards and conventions](#a3-engineering-standards-and-conventions)
  - [A.4 Security standards](#a4-security-standards)
  - [A.5 Documentation standards](#a5-documentation-standards)
  - [A.6 Domain knowledge standards](#a6-domain-knowledge-standards)
  - [A.7 Process, research, and observability standards](#a7-process-research-and-observability-standards)
  - [A.8 Principles derived from standards](#a8-principles-derived-from-standards)
- [0. Agent infrastructure organization](#0-agent-infrastructure-organization)
  - [0.1 AgentConfig repository structure](#01-agentconfig-repository-structure)
  - [0.2 Multi-root workspace](#02-multi-root-workspace)
  - [0.3 AGENTS.md in every repository](#03-agentsmd-in-every-repository)
  - [0.4 llms.txt format](#04-llmstxt-format)
  - [0.5 GitFlow + SemVer (detailed rules)](#05-gitflow-semver-detailed-rules)
  - [0.6 Pull request policy](#06-pull-request-policy)
  - [0.6.1 Merge gates (PR gates)](#061-merge-gates-pr-gates)
  - [0.6.2 Branch protection setup](#062-branch-protection-setup)
  - [0.7 README in code](#07-readme-in-code)
  - [0.8 PROJECT.md (project file template)](#08-projectmd-project-file-template)
  - [0.9 copilot-instructions.md (system instructions)](#09-copilot-instructionsmd-system-instructions)
  - [0.10 SKILL.md (technology knowledge package)](#010-skillmd-a-technology-knowledge-package)
- [1. Agent system architecture](#1-agent-system-architecture)
  - [1.1 Orchestrator agent assignment rules](#11-orchestrator-agent-assignment-rules)
  - [1.2 Model selection policy](#12-model-selection-policy)
  - [1.3 Development pipeline (from spec to production)](#13-development-pipeline-from-spec-to-production)
  - [1.3.6 Test failure protocol](#136-what-to-do-when-tests-are-failing-red)
  - [1.3.8 Pipeline fast-tracks](#138-fast-tracks-shortened-pipelines)
  - [1.4 Manual test plans](#14-manual-test-plans)
- [2. Work Protocol: Sessions and Memory](#2-work-protocol-sessions-and-memory)
  - [2.1 TASK_CONTEXT.md structure](#21-task_contextmd-structure)
  - [2.2 Memory rules](#22-memory-rules)
  - [2.3 Re-entry protocol after NEEDS_HUMAN](#23-re-entry-protocol-after-needs_human)
- [3. Critique rubrics (Constitutional Checklists)](#3-critique-rubrics-constitutional-checklists)
  - [3.0 Constitutional principles for agents](#30-constitutional-principles-for-agents-constitutional-ai-anthropic-2022)
  - [3.1 Mandatory rules for the Orchestrator](#31-mandatory-rules-for-the-orchestrator)
  - [3.2 Mandatory rules for Executors](#32-mandatory-rules-for-all-executors)
  - [3.3 Mandatory rules for Critics](#33-mandatory-rules-for-all-critics)
  - [3.4 Backend Critic rubric](#34-backend-critic-rubric)
  - [3.5 DevOps Critic rubric](#35-devops-critic-rubric)
  - [3.6 Frontend Critic rubric](#36-frontend-critic-rubric)
  - [3.7 QA Critic rubric](#37-qa-critic-rubric)
  - [3.8 Architect Critic rubric](#38-architect-critic-rubric)
  - [3.9 Security Critic rubric](#39-security-critic-rubric)
  - [3.10 Documentation Critic rubric](#310-documentation-critic-rubric)
  - [3.11 Definition of Ready / Definition of Done](#311-definition-of-ready-definition-of-done)
  - [3.12 ADR file format](#312-adr-file-format)
- [4. Observability AI workflow](#4-observability-ai-workflow)
  - [4.1 OTel GenAI Semantic Conventions v1.40.0](#41-standard-opentelemetry-genai-semantic-conventions-cncf-v1400-2025)
  - [4.2 AI workflow metrics](#42-ai-workflow-metrics)
  - [4.3 DORA metrics](#43-dora-metrics-devops-process)
  - [4.4 DORA AI Capabilities Model (2025)](#44-dora-ai-capabilities-model-2025)
  - [4.5 Trace log structure](#45-trace-log-structure)
  - [4.6 Trace writing protocol (who and when)](#46-trace-writing-protocol-who-writes-what-and-when)
  - [4.7 Visualization tools](#47-visualization-tools)
- [5. Agent prompt versioning policy](#5-agent-prompt-versioning-policy)
  - [5.1 Agent changelog](#51-agent-changelog)
  - [5.2 Golden tests after changing a Critic](#52-golden-tests-after-a-critic-change)
  - [5.3 Procedure for changing an agent](#53-agent-change-procedure)
- [6. Adoption roadmap](#6-adoption-roadmap)
  - [6.pre Before you start: capture project parameters](#6pre-before-you-start-capture-project-parameters)
  - [6.agent Implementation Agent prompt](#6agent-implementation-agent-prompt)
  - [6.0 Phase 0 — AgentConfig repo](#60-phase-0-agentconfig-repo)
  - [6.1 Phase 1 — Context](#61-phase-1-context)
  - [6.2 Phase 2 — Agent Skills](#62-phase-2-agent-skills)
  - [6.3 Phase 3 — Agents](#63-phase-3-agents)
  - [6.4 Phase 4 — MCP servers](#64-phase-4-mcp-servers)
  - [6.5 Phase 5 — ADR and memory](#65-phase-5-adr-and-memory)
  - [6.6 Phase 6 — Observability](#66-phase-6-observability)
  - [6.7 Phase 7 — Evals](#67-phase-7-evals)
  - [6.8 Phase 8 — Iteration](#68-phase-8-iteration)
  - [6.9 End-to-end example: full cycle for a minimal feature](#69-end-to-end-example-full-cycle-for-a-minimal-feature)
- [G. Glossary](#g-glossary)

---

## A. Standards and References

### A.1 Agent file-structure standards

| Standard | Source | What it provides |
|---|---|---|
| **AGENTS.md** | [agents.md](https://agents.md) | Machine-readable repository context: build commands, conventions, structure. Automatically read by agents for every task. |
| **llms.txt** | [llmstxt.org](https://llmstxt.org) | A short LLM-friendly repository overview with hyperlinks to key files. |
| **SKILL.md** | [agentskills.io](https://agentskills.io) | Packaged technology knowledge in a portable format. Agents load the relevant skill for a task. |
| **.agent.md** | [awesome-copilot](https://github.com/github/awesome-copilot) | Declarative agent format: name, model, tools, system prompt. |
| **copilot-instructions.md** | VS Code Copilot | System instructions applied to all Copilot chats within the workspace. |
| **MCP** | [Model Context Protocol](https://modelcontextprotocol.io) (Anthropic, 2024; open standard adopted by OpenAI/Google/Microsoft, 2025) | Standard for connecting external tools to agents through a single protocol. |
| **ADR** | [Michael Nygard, 2011](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | Architecture Decision Records — documenting architecture decisions that agents must follow. |
| **OTel GenAI Semantic Conventions** | [OpenTelemetry GenAI SIG](https://opentelemetry.io/docs/specs/semconv/gen-ai/), CNCF, v1.40.0, 2025 | Standard span attributes for LLM calls (agent spans, MCP, events). Foundation for AI workflow tracing. |

### A.2 Academic Executor/Critic patterns

| Pattern | Source | Where it is used |
|---|---|---|
| **Chain-of-Thought (CoT)** | Wei et al., Google, 2022 | Agent explicitly writes intermediate reasoning steps before the final answer. Basis for ReAct and Reflexion. |
| **ReAct** | Yao et al., Google/Princeton, 2022 | Base pattern for executor agents: Reasoning → Acting → Observation. |
| **Plan-and-Execute** | Wang et al., 2023 | Orchestrator creates a full dependency plan, then runs executors. |
| **Reflexion** | Shinn et al., MIT/Northeastern, 2023 | Executor reads `## Previous Attempts` before each attempt — learns from past errors. |
| **Self-Refine** | Madaan et al., CMU/AI2, 2023 | Format of each critic finding: (1) location file:line, (2) root cause, (3) actionable fix. |
| **CRITIC** | Gou et al., Tsinghua/Microsoft, 2023 | Critic is allowed a limited set of tools (syntax validators) — otherwise it hallucinates. |
| **AutoGen** | Microsoft Research, Wu et al., 2023 | Explicit termination conditions: `max_iterations: 3` → `NEEDS_HUMAN`. |
| **Spec-Driven Development (SDD)** | Böckeler/Fowler, Thoughtworks 2025; Kiro (AWS) | Specification (.feature, API contract) is created and approved **before** implementation. Pipeline Phase 0 is the SDD phase. Executor does not start Phase 1 until .feature is ready. |

### A.3 Engineering standards and conventions

| Standard | Source | Where it is used |
|---|---|---|
| **Conventional Commits** | [conventionalcommits.org](https://www.conventionalcommits.org) | Commit message format: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`. Basis for SemVer auto-releases. |
| **Semantic Versioning** | [semver.org](https://semver.org) | MAJOR.MINOR.PATCH versioning. Agents must account for breaking changes. |
| **GitFlow** | Vincent Driessen, 2010 | main → develop → feature/id → release/X.Y.Z → hotfix/. Agents work only in feature/*. |
| **12-Factor App** | [12factor.net](https://12factor.net) | III: Config via env. XI: Logs to stdout. IX: Fast startup/shutdown. Critical for portability across environments. |
| **Keep a Changelog** | [keepachangelog.com](https://keepachangelog.com) | Added / Changed / Deprecated / Removed / Fixed / Security. |
| **Pre-commit hooks** | [pre-commit.com](https://pre-commit.com) | Mandatory gates before commits: fmt, lint, validate. |
| **TDD** | Kent Beck, 2002 | Red→Green→Refactor. Executor follows it in Pipeline Phases 1–2. |
| **ATDD** | Ward Cunningham, [Cucumber](https://cucumber.io) | BDD scenarios are acceptance criteria. Executor does not finish until covered. |
| **Quality Gates** | Watts Humphrey, CMMI | Explicit gates between phases: no phase transition without APPROVE. |
| **Shift-Left Testing** | Larry Smith, 2001 | Tests are written before code or in parallel. |
| **Shift-Right / Smoke Testing** | Cindy Sridharan, 2017 | Verification on a real deployed system (Phase 2.5). |
| **Contract Testing (CDC)** | [Pact.io](https://pact.io), 2013 | Consumer defines expected API contract; provider verifies it. |
| **Mutation Testing** | R. Lipton, 1971 | Mutates code logic to ensure tests catch it. score ≥70% WARNING, <50% BLOCKER. |
| **Property-Based / Fuzz Testing** | QuickCheck (Hughes, 1999) | Generative data for validation and parsing. |
| **Load Testing** | [k6.io](https://k6.io), Grafana Labs | Load tests: SLA, RPS, p99 latency. |
| **IEEE 829** | IEEE, 2008 | Test documentation standard: Test Case Specification, Test Procedure Specification. Basis for manual test plan format (§1.4). |
| **Session-Based Test Management (SBTM)** | James Bach, Jonathan Bach, 2000 | Structured exploratory testing: charters, time-boxed sessions, debrief. Used for edge cases in §1.4. |
| **C4 Model** | [c4model.com](https://c4model.com), Simon Brown | 4 architecture levels: System Context, Containers, Components, Code. |

### A.4 Security standards

| Standard | Source | Where it is used |
|---|---|---|
| **OWASP Top 10** | [owasp.org](https://owasp.org/www-project-top-ten/) | Rubric for security critic. A01–A10. |
| **OWASP LLM Top 10** | [owasp.org/www-project-top-10-for-large-language-model-applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/) | AI-specific vulnerabilities: LLM01 Prompt Injection (BLOCKER), LLM06 Supply Chain (BLOCKER), LLM09 Misinformation (BLOCKER). |
| **STRIDE** | Microsoft, Shostack | Threat modeling methodology: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege. |
| **SLSA** | [slsa.dev](https://slsa.dev) (OpenSSF / Linux Foundation, v1.2) | Supply-chain Levels for Software Artifacts: build provenance, isolated build environments. Protects supply chain from compromise and artifact tampering. |
| **SBOM** | SPDX / CycloneDX (CISA, NIST) | Software Bill of Materials — machine-readable manifest of image dependencies. Required in regulated environments (FedRAMP, ISO 27001). |

### A.5 Documentation standards

| Standard | Source | Where it is used |
|---|---|---|
| **Diataxis** | [diataxis.fr](https://diataxis.fr) | Tutorial (learn), How-to (solve), Reference (lookup), Explanation (understand). |
| **Standard Readme** | [github.com/RichardLitt/standard-readme](https://github.com/RichardLitt/standard-readme) (RichardLitt, 2016) | Required README sections: Background, Install, Usage, API, Contributing, License. Basis for §0.7. |

### A.6 Domain knowledge standards

| Standard | Source | Where it is used |
|---|---|---|
| **Domain-Driven Design (DDD)** | Eric Evans, 2003 | Ubiquitous Language, Bounded Contexts, Domain Events. Agents use terms from `domain/glossary.md`. |
| **BDD / Gherkin** | [Cucumber](https://cucumber.io/docs/gherkin/) | `Given/When/Then` scenarios are readiness criteria for executors. |

### A.7 Process, research, and observability standards

| Standard | Source | Where it is used |
|---|---|---|
| **DORA** | [dora.dev](https://dora.dev), Google / DORA Research Program, 2019–2025 | 4 key DevOps metrics (§4); AI Capabilities Model 2025 — 7 practices to amplify AI impact (§4, §3 principle 8). |
| **Constitutional AI** | Anthropic, Bai et al., 2022 | Basis for critique rubrics: 8 constitutional principles; BLOCKER/WARNING/SUGGESTION severity (§3). |

### A.8 Principles derived from standards

- **Critic isolation** — Critic sees only the result + task + criteria. It does not see executor chain-of-thought (anchoring bias prevention).
- **Constitutional checklists** — rubrics with BLOCKER / WARNING / SUGGESTION severities (inspired by Constitutional AI, 2022).
- **Orchestration without paraphrasing** — orchestrator passes the original user task text to executors.
- **Long-term memory via ADR** — architecture decisions live in `.github/decisions/` and are checked before decisions.
- **ReAct inside every executor** — (1) reasoning, (2) tool call, (3) observation.
- **Conventional Commits are mandatory for agents** — commit type controls version bumps.
- **Context Engineering** — discipline of controlling what the agent sees. AGENTS.md / llms.txt / SKILL.md / subagents / MCP are context engineering tools. Principle: **no more context than needed**; skills are lazy-loaded based on relevance; context is built iteratively (do not paste large templates without need).

---

## 0. Agent infrastructure organization

> This section defines the **standard file structure** and **project conventions**
> that apply to any project using this specification.
> A project file may override or extend any element.

### 0.1 AgentConfig repository structure

Each project creates a dedicated agent-configuration repository (`<project>-AgentConfig`):

```
<project>-AgentConfig/
│
├── .vscode/
│   ├── <project>.code-workspace     ← one workspace: all project repos
│   ├── mcp.json                     ← MCP servers for agents
│   └── extensions.json              ← recommended extensions
│
├── .github/
│   ├── copilot-instructions.md      ← system instructions for all Copilot chats
│   ├── AGENTS_CHANGELOG.md          ← history of agent prompt changes
│   ├── pull_request_template.md     ← PR template (see §0.6)
│   ├── copilot/
│   │   └── agents/                  ← all .agent.md files
│   │       ├── <project>-orchestrator.agent.md
│   │       ├── <project>-architect.agent.md
│   │       ├── <project>-architect-critic.agent.md
│   │       ├── <project>-backend-dev.agent.md
│   │       ├── <project>-backend-critic.agent.md
│   │       ├── <project>-frontend-dev.agent.md
│   │       ├── <project>-frontend-critic.agent.md
│   │       ├── <project>-qa-engineer.agent.md
│   │       ├── <project>-qa-critic.agent.md
│   │       ├── <project>-devops-engineer.agent.md
│   │       ├── <project>-devops-critic.agent.md
│   │       ├── <project>-security.agent.md
│   │       ├── <project>-security-critic.agent.md
│   │       ├── <project>-documentation-writer.agent.md
│   │       └── <project>-documentation-critic.agent.md
│   └── decisions/                   ← ADR (Architecture Decision Records)
│       ├── ADR-001-*.md
│       ├── ADR-002-*.md
│       └── ...
│
├── .agents/
│   ├── session/                     ← .gitignore'd: temporary TASK_CONTEXT.md
│   ├── traces/                      ← JSONL session logs (OTel GenAI format)
│   ├── evals/                       ← golden tests for prompts (JSONL)
│   └── skills/                      ← Agent Skills (SKILL.md format)
│       ├── <project>-backend/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── <project>-frontend/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── <project>-devops/
│       │   ├── SKILL.md
│       │   └── references/
│       └── <project>-<other>/
│           └── SKILL.md
│
├── MULTI_AGENT_SPEC.md              ← universal spec (this file)
├── PROJECT.md                       ← project-specific details (stack, models, CI)
├── AGENTS.md                        ← global context for the whole project
├── llms.txt                         ← LLM-readable project overview
├── .gitignore                       ← ignores .agents/session/
└── domain/                          ← domain knowledge
      ├── glossary.md                  ← Ubiquitous Language
      ├── bounded-contexts.md          ← Context Map
      ├── domain-events.md             ← key events
      └── specs/                       ← BDD/Gherkin scenarios
            └── *.feature
```

**`.gitignore` for AgentConfig:**

```gitignore
# Agent temporary sessions (do not commit)
.agents/session/

# .agents/traces/ — do NOT ignore: traces are committed as AI workflow history
```

> `CHANGELOG.md` does not live in AgentConfig. It lives in the root of each component repo (Backend, Frontend, Automation, Docs).
> Format: Keep a Changelog — sections `Added / Changed / Deprecated / Removed / Fixed / Security`.
> It is created and updated by an agent on every release commit (see DoD §3.11).
> Prompt changelog (`AGENTS_CHANGELOG.md`) is a separate file in AgentConfig under `.github/` (see §5.1).

#### 0.1.1 `.agent.md` file format

Each agent is defined by a `.github/copilot/agents/<project>-<role>.agent.md` file.
The `model` field and full model names are defined in PROJECT.md §2; below is the structure template.

```markdown
---
name: <project>-<role>
description: >
   [One sentence: what this agent does and when to invoke it]
model: <model-name>          # see PROJECT.md §2 + tiers in MULTI_AGENT_SPEC.md §1
tools:
   # --- all agents: navigation (read-only) ---
   - read_file
   - grep_search
   - semantic_search
   - list_dir
   - file_search
   # --- executor agents add: ---
   # - create_file
   # - create_directory
   # - replace_string_in_file
   # - run_in_terminal
   # --- orchestrator additionally: ---
   # - manage_todo_list    ← task decomposition + subtask status
   # --- critic agents: read-only; devops-critic adds: ---
   # - get_errors          ← syntax validation (terraform, docker)
   # - run_in_terminal     ← only validate/fmt, never apply
---

# System Prompt

## Role
[Role: executor or critic; responsibility zone; pipeline phases from MULTI_AGENT_SPEC.md §1.3]

## Context
- Read AGENTS.md in all relevant repos before starting each task
- Check .github/decisions/ for ADR constraints before any architectural change
- [executor] Read ## Previous Attempts in TASK_CONTEXT.md before each iteration (Reflexion)
- [critic] Receive only: original task + criteria + result. Do NOT read chain-of-thought.

## Task Protocol
[Concrete algorithm: what to do first, how to build the result, output structure]

## Constitutional Constraints
- Follow all principles from MULTI_AGENT_SPEC.md §3
- Do not write files outside your responsibility zone (Constitution principle 2)
- All code comments and artifacts in English (principle 7)

## Output Format
[What exactly to return: files, diff, Critique Report, TASK_CONTEXT.md updates]

## Trace Recording
After each iteration, append one JSONL line to `.agents/traces/<trace_id>.jsonl`.
`trace_id` comes from the TASK_CONTEXT.md header.

Executor (operation: "execute"):
   {"ts":"<ISO8601>","trace_id":"<id>","span_id":"s<N>","parent_span_id":"s01",
    "agent":"<name>","operation":"execute","subtask":<N>,"iteration":<N>,
    "input_tokens":<N>,"output_tokens":<N>,"duration_ms":<N>}

Critic (operation: "critique") — include verdict / blockers / warnings:
   {"ts":"<ISO8601>","trace_id":"<id>","span_id":"s<N>","parent_span_id":"s01",
    "agent":"<name>-critic","operation":"critique","subtask":<N>,"iteration":<N>,
    "verdict":"APPROVE|REQUEST_CHANGES|REJECT","blockers":<N>,"warnings":<N>,
    "input_tokens":<N>,"output_tokens":<N>,"duration_ms":<N>}

Full format — see MULTI_AGENT_SPEC.md §4.5–4.6.
```

> `name`, `description`, `model`, `tools` are read by VS Code Copilot from the YAML frontmatter; the system prompt is the file body after `---`.

#### 0.1.3 Filled `.agent.md` example — backend-critic

> A full working copy-paste example. Replace `<project>` with your project name; choose the model according to PROJECT.md §2.

````markdown
---
name: <project>-backend-critic
description: >
   Reviews backend code produced by backend-dev. Invoke after every backend-dev iteration
   to get a structured Critique Report (APPROVE / REQUEST_CHANGES / REJECT).
model: claude-sonnet-4.6
tools:
   - read_file
   - grep_search
   - semantic_search
   - list_dir
   - file_search
---

# System Prompt

## Role
Critic agent. Reviews the result of backend-dev executor using the Backend Critic rubric
from MULTI_AGENT_SPEC.md §3.4 and project-specific triggers from PROJECT.md §4.
Does NOT write code. Does NOT read executor's chain-of-thought — only the final result.

## Context
- Read AGENTS.md in the backend repo before reviewing.
- Check .github/decisions/ for active ADR constraints.
- Receive from orchestrator: original task + acceptance criteria + result (files changed).

## Task Protocol
1. Read the changed files listed in the task.
2. For each file: apply Backend Critic checklist (§3.4 + PROJECT.md §4 triggers).
3. Check Constitutional principles §3.0: zone violations, hardcoded config, skipped tests.
4. Compose Critique Report (see Output Format below).
5. Append one JSONL line to .agents/traces/<trace_id>.jsonl (trace_id from TASK_CONTEXT.md).

## Constitutional Constraints
- Follow MULTI_AGENT_SPEC.md §3.0 and §3.3 (all critic rules).
- Only read_file / grep_search — no write operations.
- Findings without file:line reference are not valid — do not include them.
- 0 findings is valid only if the implementation is genuinely correct;
   if you suspect sycophancy, re-read the rubric and check one more time.

## Output Format

### Critique Report

**VERDICT:** APPROVE | REQUEST_CHANGES | REJECT

| Severity | Category | Location | Issue | Recommendation |
|---|---|---|---|---|
| BLOCKER | security | handlers/host.go:45 | Input not validated | Add validation middleware |
| WARNING  | performance | services/bulk.go:120 | N+1 query | Batch IDs, one bulk query |
| SUGGESTION | conventions | models/host.go:33 | No godoc | Add comment |

### Trace Recording
After issuing the verdict, append to .agents/traces/<trace_id>.jsonl:
{"ts":"<ISO8601>","trace_id":"<id>","span_id":"s<N>","parent_span_id":"s01",
 "agent":"<project>-backend-critic","operation":"critique","subtask":<N>,"iteration":<N>,
 "verdict":"<APPROVE|REQUEST_CHANGES|REJECT>","blockers":<N>,"warnings":<N>,
 "input_tokens":<N>,"output_tokens":<N>,"duration_ms":<N>}
````

---

#### 0.1.2 Minimal `.vscode/extensions.json`

Recommended VS Code extensions for an AI-agent workspace:

```json
{
   "recommendations": [
      "github.copilot",
      "github.copilot-chat",
      "ms-azuretools.vscode-docker",
      "hashicorp.terraform",
      "golang.go",
      "dbaeumer.vscode-eslint",
      "esbenp.prettier-vscode",
      "eamodio.gitlens",
      "redhat.vscode-yaml",
      "ms-vscode.vscode-json"
   ]
}
```

> This list depends on your tech stack — adjust to the languages and tools you actually use.
> During developer onboarding, an agent may recommend installing extensions from this list.

### 0.2 Multi-root workspace

All project repositories are combined into a single VS Code workspace via `.vscode/<project>.code-workspace`:

```json
{
   "folders": [
      { "path": ".",                       "name": "<project>-AgentConfig" },
      { "path": "../<project>-Backend",    "name": "<project>-Backend" },
      { "path": "../<project>-Frontend",   "name": "<project>-Frontend" },
      { "path": "../<project>-Automation", "name": "<project>-Automation" },
      { "path": "../<project>-Docs",       "name": "<project>-Documentation" }
   ],
   "settings": {
      "github.copilot.chat.agentFiles": [".github/copilot/agents"]
   }
}
```

> AgentConfig is the entry point: the workspace is opened from here, and agents see all repos through a single unified context.

AGENTS.md distribution across repositories:

```
<project>-AgentConfig/AGENTS.md    ← global: product, repo map, conventions
<project>-Backend/AGENTS.md        ← backend language/framework: build, tests, structure
<project>-Frontend/AGENTS.md       ← UI framework: build, tests, structure
<project>-Automation/AGENTS.md     ← IaC / CI/CD: environments, clouds, conventions
<project>-Docs/AGENTS.md           ← documentation standards
```

---

### 0.3 AGENTS.md in every repository

#### 0.3.1 Required contents of the global AGENTS.md

```markdown
## Product Overview
[3–5 sentences: what the product does, for whom, key entities]

## Repository Map
| Repo | Contents |
|---|---|
| <project>-AgentConfig | Agent files, skills, domain, ADR |
| <project>-Backend     | Server-side code |
| <project>-Frontend    | Client-side code |
| <project>-Automation  | IaC, CI/CD, deploy scripts |
| <project>-Docs        | User and API documentation |

## Commit Conventions (Conventional Commits)
- feat(<scope>): — MINOR version bump
- fix(<scope>):  — PATCH version bump
- chore:         — dependencies/config (no version bump)
- refactor:      — no behavior change (no bump)
- docs:          — documentation only
- BREAKING CHANGE (footer) — MAJOR version bump

## Branching Strategy: GitFlow
[See MULTI_AGENT_SPEC.md §0.5 for detailed rules]
- main: production-ready, tagged vX.Y.Z
- develop: integration branch
- feature/<task-id>-<description>: from develop → develop
- release/X.Y.Z: from develop → main + develop
- hotfix/<description>: from main → main + develop

## PR Policy
Every merge via Pull Request. See .github/pull_request_template.md.
Squash merge. Feature branch deleted after merge.

## ADR Index
[Links to .github/decisions/ADR-*.md]
```

#### 0.3.2 Required contents of a component repository AGENTS.md

```markdown
## Build & Run
[Commands: build, test, lint, format — with exact script names]

## Structure
[Key directories: where business logic lives, where tests live, what is generated and must not be edited manually]

## Conventions
[Naming, error handling, configuration, forbidden patterns]
```

> For the Frontend repo, additionally: `docs/test-plans/` — manual test plans (§1.4).
> The directory is committed; it is created by `frontend-dev` on the first user flow.

---

### 0.4 llms.txt format

Each component repository contains `llms.txt` — a short LLM-friendly overview (llmstxt.org):

```markdown
# <project>-<Component>

> One-sentence description of this component.

Language/framework: X. Key constraints: Y.

## Key Files
- [entry-point](path/to/entry): what it does
- [config/](config/): configuration directory
- [swagger-api/](swagger-api/): API source of truth (if applicable)

## Documentation
- [README.md](README.md): overview
- [AGENTS.md](AGENTS.md): AI agent instructions
```

---

### 0.5 GitFlow + SemVer — detailed rules

#### 0.5.1 Branches

| Branch | Purpose | Branches off | Merges into |
|---|---|---|---|
| `main` | Production-ready, tagged `vX.Y.Z` | `release/*` | — |
| `develop` | Integration branch, base for features | `main` (init) | `release/*` |
| `feature/<task-id>-<description>` | New feature work | `develop` | `develop` |
| `release/X.Y.Z` | Release preparation, bugfix-only | `develop` | `main` + `develop` |
| `hotfix/<description>` | Urgent production fix | `main` | `main` + `develop` |

> Agents work **only** in `feature/*` branches. They do not push directly to `develop` or `main`.

#### 0.5.2 SemVer + automated versioning

```
Commit type      → Version bump
feat:            → MINOR bump  (X.Y+1.0)
fix:             → PATCH bump  (X.Y.Z+1)
chore/docs/refactor → no bump
BREAKING CHANGE  → MAJOR bump  (X+1.0.0)

Tool: gitversion (gitversion.yml in the root of each component repo).
CI pipeline reads the version via gitversion and tags the image/artifact.
```

> When creating a commit, an executor agent must choose the correct Conventional Commit type — it drives the release version.
> If a change breaks a public API, the `BREAKING CHANGE` footer is mandatory (Constitution principle 3).

#### 0.5.3 Feature branch naming

```
feature/<task-id>-<short-kebab-description>

Examples:
   feature/PROJ-123-add-bulk-endpoint
   feature/PROJ-456-fix-auth-token-refresh
   feature/PROJ-789-update-helm-values
```

---

### 0.6 Pull request policy

**Required template `.github/pull_request_template.md`:**

```markdown
## Summary
<!-- What changed and why (1–3 sentences) -->

## Related Work
<!-- Task/issue ID: PROJ-NNN -->
<!-- Related ADR: ADR-NNN (if applicable) -->

## Type of Change
- [ ] feat: new feature (MINOR bump)
- [ ] fix: bug fix (PATCH bump)
- [ ] chore/refactor/docs: no version change
- [ ] BREAKING CHANGE: incompatible change (MAJOR bump)

## Checklist
- [ ] Tests pass locally
- [ ] Linter / formatter clean
- [ ] No secrets or hardcoded config in code
- [ ] AGENTS.md updated if conventions changed
- [ ] CHANGELOG.md updated (if release commit)
- [ ] ADR created or referenced if architectural decision made
```

### 0.6.1 Merge gates (PR gates)

Any merge into `main` / `release` requires passing three sequential gates.

#### 0.6.1.1 Gate 1 — CI: all tests are green

Every PR runs a full test suite automatically. Merging is blocked until all checks pass.

```
Required CI run:
   - Static analysis (linter, vet/typecheck)
   - Unit tests (coverage must not drop below project threshold)
   - Integration tests (real dependencies — DB, cache)
   - Contract tests (if public API changed)
   - Build: artifact must build with no errors and no warnings

No exceptions:
   - Temporarily disabling a test requires BLOCKER justification in the PR description
   - A flaky test does not count as passing — fix it first or skip + link an issue (Constitution principle 5)

Exact commands and pipeline files are defined in the project file.
```

#### 0.6.1.2 Gate 2 — Review by a Critic agent

The appropriate critic agent must review the PR and leave structured comments as PR threads.

```
Critic assignment by change type:
   Backend changes (business logic, API)        → backend-critic
   Frontend changes (components, pages)        → frontend-critic
   IaC / CI/CD / Dockerfile changes            → devops-critic
   Test scripts (smoke, E2E, load)             → qa-critic
   Documentation changes                       → documentation-critic
   New service / cross-service contract / ADR  → architect-critic (in addition)

PR touches multiple areas → run all relevant critics in parallel.

Format for each critic comment in the PR:
   **[BLOCKER|WARNING|SUGGESTION]** `file:line`
   Issue: what is wrong and why (root cause)
   Recommendation: a concrete fix

Critic does NOT press "Approve" — it leaves thread comments.
Final APPROVE is done by the orchestrator after all threads are resolved.

How the critic is invoked (webhook, manual Copilot Chat, CI job) is defined in PROJECT.md §3.x.
Without a working mechanism, Gate 2 does not function.
```

**Configuration examples (PROJECT.md §3.x):**

**Option A — Manual via Copilot Chat** *(recommended to start — requires no additional setup)*

PR is open → developer opens Copilot Chat and writes:

```
@backend-critic perform a Code Review of this PR
```

**Option B — GitHub Actions job**

```yaml
# .github/workflows/critic-review.yml
on:
   pull_request:
      types: [opened, synchronize]
jobs:
   critic:
      runs-on: ubuntu-latest
      steps:
         - uses: actions/checkout@v4
         - name: Run critic review
            run: gh copilot suggest --agent backend-critic "Review this PR"
```

**Option C — MCP webhook (if SCM MCP is configured)**

PR opened event → MCP server → automatically runs the `.agent.md` critic.

#### 0.6.1.3 Gate 3 — Discussion: executor responds to every comment

The executor who created the PR must reply to every open critic thread.
Silence is not a response — an unresolved thread blocks merging.

**Option A — Executor disagrees with critic:**

```
Executor replies in the thread:
   DISPUTE: <argument>
   - Link to a standard / ADR / test that proves the point
   - If needed — a quote from the spec or documentation

Critic replies:
   - Withdraws the finding → closes the thread with ACKNOWLEDGED
   - Insists              → strengthens the argument (iteration +1)

If a BLOCKER/WARNING is not resolved within 2 iterations → orchestrator escalates: NEEDS_HUMAN
SUGGESTION may be rejected by the executor without escalation (ACKNOWLEDGED is sufficient).
```

**Option B — Executor agrees:**

```
Executor fixes the code, then replies:
   FIXED: <what changed> — commit <sha>
   Reason: <why this fix addresses the root cause>

Critic closes the thread:
   RESOLVED
```

**Thread states:**

| Status | Meaning | Blocks merge |
|---|---|---|
| `RESOLVED` | Fix applied, critic agrees | No |
| `ACKNOWLEDGED` | Executor proved the point, critic withdrew | No |
| `DEFERRED` | Tech debt; issue created — **SUGGESTION-only** | No |
| `ESCALATED` | Disagreement on BLOCKER/WARNING → NEEDS_HUMAN | Yes |
| *(open)* | No response or discussion in progress | Yes |

> `DEFERRED` is allowed **only for SUGGESTION**.
> A thread that contains an **active** BLOCKER finding must be `RESOLVED`.
> If the critic withdraws the finding (i.e., it is no longer a BLOCKER), `ACKNOWLEDGED` is valid.

**Final merge condition:**

```
Gate 1:  CI → all tests green, build successful
Gate 2:  Critic agent left a review (at least one thread, or explicit "No findings")
Gate 3:  All threads are RESOLVED | ACKNOWLEDGED | DEFERRED(SUGGESTION-only)
             All threads with active BLOCKER findings are RESOLVED only
             ≥ 1 human reviewer → APPROVE
             → orchestrator issues the final APPROVE to merge
```

**Gate summary table:**

| Gate | What is checked | Who checks | Blocks merge |
|---|---|---|---|
| CI | All tests green; build succeeds | CI system | Yes |
| Critic review | Structured review present | critic agent | Yes |
| Thread resolution | All threads closed | executor + critic | Yes |
| BLOCKER resolved | All BLOCKER → RESOLVED | executor + critic | Yes |
| Human review | ≥ 1 human APPROVE | human | Yes |

> The critic agent already ran the checklist (BLOCKER/WARNING/SUGGESTION). Human checks what the agent cannot evaluate:
> - Business logic matches stakeholder intent (not only the spec)
> - Changes don’t produce unintended side effects for adjacent systems
> - UX/DX is acceptable: the intended outcome is truly delivered
> - Product/strategy appropriateness
>
> Human does NOT re-run OWASP/STRIDE/ADR checklists — agents already did.

---

### 0.6.2 Branch protection setup

Gates (§0.6.1) work only if direct pushes to protected branches are technically blocked.
Without branch protection, Gates 1–3 can be bypassed by merging without a PR.

**Required platform-level settings for `main` and `develop` (GitHub / Azure DevOps / GitLab):**

| Rule | Setting | Applies to |
|---|---|---|
| PR-only | Require pull request reviews | `main`, `develop` |
| CI required | Require status checks (Gate 1 jobs) | `main`, `develop`, `release/*` |
| Min 1 reviewer | Require 1 approved human review | `main` |
| No direct pushes | Restrict direct pushes (everyone except CI bot) | `main`, `develop` |
| Linear history | Squash merge or rebase | `main` |
| Auto-delete branches | Auto-delete head branch after merge | `feature/*`, `hotfix/*` |

> Agents work in `feature/*` — restrictions on `main`/`develop` do not block their workflow.
> Setting names depend on the platform:
> GitHub: Settings → Branches → Branch protection rules;
> Azure DevOps: Project Settings → Repositories → Policies → Branch Policies.
> PROJECT.md §3 must declare which CI status checks are required (Gate 1 jobs + critic jobs if automated).

---

### 0.7 README in code

> Based on: [Standard Readme](https://github.com/RichardLitt/standard-readme) (RichardLitt, 2016), [Make a README](https://www.makeareadme.com).
> A README in code is a set of technical signposts for developers and agents working with a particular repository or module.
> It differs from public documentation (Diataxis Tutorial/How-to/Reference): the goal is not to teach end users,
> but to explain the structure and intent to someone opening the repo for the first time.

#### 0.7.1 Three types of in-code README

| Type | Location | Audience | Goal |
|---|---|---|---|
| Root README | Repo root | New developer / agent / contributor | Quick start: where, what, how to run |
| Component README | Each package/service in a monorepo | Developer working with the module | Purpose, public interface, scope constraints |
| AGENTS.md | Next to Root/Component README | AI agent | Machine-readable context: commands, conventions |

> AGENTS.md and README are different documents: README is for humans; AGENTS.md is for agents.
> Avoid duplication: AGENTS.md should link to README for narrative context.

#### 0.7.2 Root README — required sections

Matches the Standard Readme spec:

```markdown
# <Name>

> <One sentence: what it does, for whom>

## Background
[Why it exists; what problem it solves — 3–5 sentences]

## Requirements
[Prerequisites: runtime versions, system dependencies]

## Install
[Exact install/build commands with expected output]

## Usage
[Minimal working example: command + expected output]

## API
[Brief overview of the public interface. Full reference lives in documentation.]

## Contributing
[Link to AGENTS.md and/or CONTRIBUTING.md]

## License
[SPDX license identifier]
```

#### 0.7.3 Component / Module README — required sections

````markdown
# <Module name>

> <One sentence: what this module does>

## Purpose
[Why it exists in the system; what breaks without it]

## Dependencies
[What it depends on and WHY — not a list of imports, but justification for each dependency]

## Public Interface
[Key exported types/functions/endpoints — brief list]

## Usage Example
```go
// Minimal compilable / runnable example
```

## Out of Scope
[What this module intentionally does NOT do — explicit responsibility boundaries]

## Related
[ADR: ADR-NNN. Specs: domain/specs/*.feature]
````

#### 0.7.4 README-first principle

Component README is written **before** implementing the module (SDD, Phase 0).
Describing `Public Interface` and `Out of Scope` before code helps surface scope and dependency ambiguities
before spending iterations on a wrong implementation.

**Phase 0 owners:** `architect` initiates Component README as part of the specification (`Public Interface` and `Out of Scope`),
`documentation-writer` formats it using the template. Without Component README, the transition to Phase 1 is blocked
(Documentation Critic §3).

---

### 0.8 PROJECT.md — project file template

> The project file applies this universal specification to a specific stack, platform, and team.
> It is created in `<project>-AgentConfig/` next to MULTI_AGENT_SPEC.md.
> This spec contains principles; PROJECT.md contains concrete project facts: stack, agent models, environments, CI commands.

#### 0.8.1 Required sections of PROJECT.md

````markdown
# PROJECT.md — <Project name>

> Version: X.Y.Z · Stack: [Go / TS / ...] · Platform: [K8s / Azure / ...] · Spec: MULTI_AGENT_SPEC vX.Y.Z

## 1. Stack and environments

### Languages and frameworks
| Component | Language | Framework / Runtime |
|---|---|---|
| Backend  | Go X.Y | go-swagger / Chi / ... |
| Frontend | TypeScript | Next.js X / React X / ... |
| IaC      | Terraform X | Azure RM / Helm X / ... |

### Environments
| Name | Purpose | URL / cluster | Branch |
|---|---|---|---|
| dev     | Development / smoke | ... | develop |
| staging | E2E / load tests    | ... | release/* |
| prod    | Production          | ... | main |

## 2. Project agents

### 2.1 Customize the agent set

<!-- The baseline agent set is defined in MULTI_AGENT_SPEC.md §1.
       Record deviations here: added/removed/renamed roles.
       All changes must also be logged in AGENTS_CHANGELOG.md. -->

| Action | Agent | Rationale |
|---|---|---|
| added  | `data-engineer` | Project uses ETL pipelines |
| removed | `qa-engineer` | No separate QA; role covered by backend-dev |
| renamed | `infra-engineer` (← `devops-engineer`) | Team domain terminology |

<!-- If there are no changes, keep a single row “none” or remove the section. -->

### 2.2 Agent models

<!-- Fill during setup. Tiers T1/T2/T3 are defined in MULTI_AGENT_SPEC.md §1.
       List only the agents actually used in this project after customization (§2.1). -->

| Agent | Model | Tier | Rationale |
|---|---|---|---|
| orchestrator         | ... | T? | ... |
| architect            | ... | T? | ... |
| architect-critic     | ... | T? | ≥ tier of architect |
| backend-dev          | ... | T? | ... |
| backend-critic       | ... | T? | ≥ tier of backend-dev |
| frontend-dev         | ... | T? | ... |
| frontend-critic      | ... | T? | ≥ tier of frontend-dev |
| qa-engineer          | ... | T? | ... |
| qa-critic            | ... | T? | ≥ tier of qa-engineer |
| devops-engineer      | ... | T? | ... |
| devops-critic        | ... | T? | ≥ tier of devops-engineer |
| security             | ... | T? | ... |
| security-critic      | ... | T? | ≥ tier of security |
| documentation-writer | ... | T? | ... |
| documentation-critic | ... | T? | ≥ tier of documentation-writer |

### 2.3 Override the model selection policy

<!-- Universal model selection rules are in MULTI_AGENT_SPEC.md §1.2.
       Record only deviations here: budget constraints, provider policy, missing models.
       Orchestrator reads this section and applies it with higher priority than MULTI_AGENT_SPEC §1.2.
       If empty, §1.2 applies as-is. -->

```
Providers in use: ...          (e.g., Anthropic + OpenAI / Anthropic only)
Max tier: T?                  (e.g., T2 — T1 models unavailable / budget)
Forbidden models: ...         (e.g., Claude Opus 4.6 — 30x, do not use)
Prefer 0x models: yes|no      (yes — prefer GPT-4.1/GPT-4o/GPT-5 mini/Raptor mini when quality is equal)
```

**Custom assignments (if different from §2.2):**

| Rule | Model | Rationale |
|---|---|---|
| Orchestration instead of T1 | ... | ... |
| Fallback on T1 rate limit | ... | ... |
| Planning tasks without T1 | ... | ... |
| Documentation without T3 | ... | ... |

> If there are no custom rules — delete the table above. Everything else is governed by the lines above + MULTI_AGENT_SPEC §1.2.

---

## 3. CI/CD

### Pipeline files
| File | Platform | Purpose |
|---|---|---|
| ... | GitHub Actions / Azure Pipelines / GitLab CI | ... |

### Gate 2: how the critic is invoked on PRs
<!-- Describe: webhook / manual Copilot Chat / CI job.
       Without a configured mechanism, Gate 2 does not work — see §0.6. -->

### Coverage thresholds
| Type | Threshold | Blocks CI |
|---|---|---|
| Unit test coverage | ≥ ?% | Yes |
| Mutation score     | ≥ 70% | Yes (< 50% = BLOCKER) |
| Static analysis    | 0 errors | Yes |

**Mutation tool:** `...` — run command: `...`
*(go-mutesting / pitest / mutmut / stryker / fast-check — fill per project)*

## 4. Technology-specific rubric triggers (add-on to MULTI_AGENT_SPEC §3)

> Concrete triggers for this project’s stack. Do not duplicate universal rules from the spec.

### Backend Critic — additional triggers
```
BLOCKER:
- [ ] ...
WARNING:
- [ ] ...
```

### Frontend Critic — additional triggers
```
BLOCKER:
- [ ] ...
WARNING:
- [ ] ...
```

### DevOps Critic — additional triggers
```
BLOCKER:
- [ ] ...
WARNING:
- [ ] ...
```

## 5. MCP servers

> Concrete servers configured in `.vscode/mcp.json`. Example structure — MULTI_AGENT_SPEC.md §6.4.

| Server | Tools | Purpose |
|---|---|---|
| SCM (GitHub / Azure DevOps) | create_pr, get_issues | PRs and issues from an agent |
| Docker | docker_build, docker_run | Containers |
| IaC (Terraform / Helm) | tf_plan, tf_apply | IaC without switching context |

## 6. Project roadmap

> Complements the universal roadmap (§6 MULTI_AGENT_SPEC) with stack-specific tasks.

| Phase | Task | Status |
|---|---|---|
| AgentConfig | ... | [ ] |
| Context | ... | [ ] |

## §pre: Project parameters

> Filled **before starting the Roadmap** (§6.pre) — answers to the implementation agent’s questions.
> The implementation agent (§6.agent) reads this section first; without it, it cannot set up files correctly.

```
Project:
   Name and description:        ...
   Components (repositories):   ...
   Codebase baseline:           greenfield | legacy+rescue | old-project
   MULTI_AGENT_SPEC version:    vX.Y.Z  (spec version at project setup — see §6.agent.2)

Tech stack:
   Languages and frameworks:    ...
   Database / ORM:              ...
   IaC tool:                    ...
   CI/CD platform:              ...
   Version control:             GitHub | Azure DevOps | GitLab

AI and models:
   Available AI providers:      ...
   Budget constraints:          ...
   Required agent roles:        all | ...

Testing:
   Existing tests:              none | unit | integration | E2E
   Test framework:              ...
   Coverage thresholds:         unit ≥ ?%  mutation ≥ ?%
   PBT/Fuzz tool:               go-fuzz | hypothesis | fast-check | other

Performance and reliability:
   Target SLA:                  RPS=?  p99=?ms  error_rate≤?%

Security and secrets:
   Secrets store:               Vault | Key Vault | .env+gitignore | other
   SBOM / SLSA requirements:    none | SLSA L1 | SLSA L2

Observability:
   OTEL backend:                none (JSONL only) | Jaeger | Phoenix | other

Team:
   Agent interaction model:     developers | PM | single person
   Existing ADR:                none | path to directory
   Existing .feature specs:     none | path to directory
```
````

---

### 0.9 copilot-instructions.md — system instructions

> `.github/copilot-instructions.md` contains instructions automatically applied to **all** Copilot chats
> in the workspace (VS Code). This is “always-on” background context.
> Size: **no more than ~500 words** — a practical Context Engineering limit: a larger block rarely improves quality
> (the LLM assigns lower priority to distant instructions) and slows down every call.
> Target 300–500 words. If you approach 500, move details into SKILL.md (lazy-loaded) or AGENTS.md, and keep here only
> “active memory” (ADR, sprint focus).

#### 0.9.1 Required sections

```markdown
# <Project> — AI Instructions

## Project Overview
[1–2 sentences: product, stack, audience. Do not duplicate AGENTS.md — link to it.]
See: <project>-AgentConfig/AGENTS.md

## Agent Workflow
All multi-step tasks go through the orchestrator.
Pipeline: Phase 0 (specs) -> 1 (code) -> 2 (tests) -> 2.5 (deploy) -> 3 (refactor)
-> 3.5 (regression) -> 4 (arch) -> 5 (security) -> 6 (docs).
See: MULTI_AGENT_SPEC.md for full protocol.

## Key Constraints
- Language: all code artifacts and comments in English. Chat with user in Russian.
- Do not modify auto-generated files (see AGENTS.md -> Structure).
- No hardcoded secrets or config values (12-Factor III).
- Every new feature requires .feature spec before Phase 1 (SDD).

## Active ADR
[Key ADRs every agent must know:]
- ADR-001-*: [short title]
- ADR-002-*: ...

## Current Sprint / Focus
[Optional: max 3 items — what is currently in progress]
```

> `## Active ADR` is the most important section: long-term memory visible in every chat.
> `## Current Sprint` is updated once per sprint; do not copy the entire TASK_CONTEXT.md into it.

---

### 0.10 SKILL.md — a technology knowledge package

> Agent Skills format — portable knowledge about a specific technology.
> Agents “lazy-load” the relevant SKILL.md per task instead of loading the entire repo context.
> Size: **no more than ~800 words per file**; split by components (backend / frontend / devops).

#### 0.10.1 Required SKILL.md sections

````markdown
# SKILL: <Project>-<Component>

> One-sentence summary: what this skill covers and when to use it.

## When to Use This Skill
[3–5 signals: when the agent should load this skill]
- The task concerns [component/technology]
- You need to change [files/modules]

## Tech Stack
| Role | Technology | Version | Notes |
|---|---|---|---|
| Runtime | Go | 1.23 | modules enabled |
| API spec | OpenAPI | 3.0 | swagger-api/ is the source of truth |
| DB | PostgreSQL | 16 | via pgx/v5 |
| Test | testify | v1.9 | suite pattern |

## Build & Test Commands
```bash
# Build
go build ./...

# Test (unit)
go test ./... -race -count=1

# Test (integration) — requires DB
go test ./... -tags=integration

# Lint
golangci-lint run

# Generate (OpenAPI -> handlers)
swagger generate server -f swagger-api/swagger.yaml
```

## Key Conventions
- Error handling: wrap with fmt.Errorf("context: %w", err) — never `_ = err`
- Config: env vars only; viper reads .env in dev, real env in prod
- Generated files: gen/restapi/** — DO NOT edit manually
- Forbidden patterns: global mutable state, init() with side effects

## Common Patterns
[2–3 real examples from the codebase — how to do things correctly in this project]

## Out of Scope
[What this skill does NOT cover — applicability boundaries]

## References
- [AGENTS.md](../AGENTS.md)
- [ADR-001](../.github/decisions/ADR-001-*.md)
- [swagger-api/swagger.yaml](../swagger-api/swagger.yaml)
````

> `## Build & Test Commands` is critical: agents use it to run tests.
> `## Key Conventions` helps prevent violating Constitutional principles 2, 4, 5, 6.

---

## 1. Agent system architecture

```
User
       │
       ▼
[orchestrator]                  ← single entry point for any task
       │                             reads ADR + TASK_CONTEXT before every decision
       ├──► [architect]           ─┐
       ├──► [backend-dev]         ─┤
       ├──► [frontend-dev]        ─┤
       ├──► [qa-engineer]         ─┤  executor → critic → [iteration, max 3]
       ├──► [devops-engineer]     ─┤       ↑___________________________|
       ├──► [security]            ─┤  if iter=3 and VERDICT≠APPROVE → NEEDS_HUMAN
       └──► [documentation-writer]─┘
                     │
                     ▼
             .agents/session/TASK_CONTEXT.md   ← memory: plan + previous attempts
                     │
                     ▼
             .github/decisions/ADR-*.md        ← long-term memory
```

**Why each agent exists:**

| Agent | Pipeline phase | What it does |
|---|---|---|
| `architect` | 0, 4 | BDD specs, ADR, C4 Model, cross-service contracts |
| `backend-dev` | 1, 2, 3 | Code + unit/integration/contract tests next to code (TDD) |
| `frontend-dev` | 1, 2, 3 | UI components + Jest/RTL tests next to components |
| `qa-engineer` | 2.5, 3.5 | Deployed-system tests: smoke, E2E, load. Does not write business logic code. |
| `devops-engineer` | 2.5, 3.5 + CI | IaC, CI/CD, deploy to test envs for Phases 2.5 and 3.5; CI support across all phases |
| `security` | 5 | OWASP/STRIDE, image CVE scanning, threat modeling |
| `documentation-writer` | 0 (Component README), 6 | Phase 0: Component README (§0.7) with `architect`; Phase 6: API reference, How-to (Diataxis), updates to `.feature`, manual test plans |

> Extensibility: the agent set is the spec baseline.
> PROJECT.md §2 may add roles, remove unused roles, or rename them to match domain terminology.
> Changes must be recorded in `AGENTS_CHANGELOG.md`.

**Patterns:**
- Plan-and-Execute — orchestrator builds the full plan before execution
- ReAct — every executor: Reasoning → Acting → Observation
- Reflexion — executor reads critique from previous attempts before the next iteration
- Critic isolation — critic sees only the result, not chain-of-thought; escalate to human if iter=3 without APPROVE

---

### 1.1 Orchestrator agent assignment rules

Orchestrator selects agents using two signals: **change area** (what changes in code/infra) and **task type** (design, implementation, tests, docs).

#### 1.1.1 Assignment matrix by area

| Change area | Primary agent | When to add `architect` |
|---|---|---|
| Server code, API, business logic, DB schema | `backend-dev` | New public API or new service |
| UI components, pages, hooks, styles | `frontend-dev` | New user-facing flow without `.feature` |
| Dockerfile, docker-compose, Helm, IaC | `devops-engineer` | — |
| CI/CD pipeline, deploy scripts | `devops-engineer` | — |
| Test scripts: smoke, E2E, load, benchmark | `qa-engineer` | — |
| Security audit, CVE, threat model, auth | `security` | — |
| README, `.feature`, How-to, API Reference | `documentation-writer` | If `.feature` changes |
| New service / cross-service contract / ADR | `architect` | Primary |

#### 1.1.2 Mandatory `architect` first

Orchestrator must invoke `architect` **before** any other executor if at least one condition holds:

```
- The task creates a new service or standalone module
- The task introduces or changes a public cross-service API
- The task crosses more than one bounded context boundary
- There are no `.feature` specifications for the task
- The task contradicts an active ADR or requires a new ADR
```

#### 1.1.3 Mandatory `security` involvement

Run in parallel with the primary executor (or as a separate subtask) if:

```
- AuthN/AuthZ is added or changed
- A new public endpoint is added that accepts external input
- The task processes PII or financial data
- A new external dependency is added with unknown CVE status
- Network/firewall/TLS configuration changes
```

#### 1.1.4 Parallel execution

Independent parts of a task (no mutual dependencies) should be given to multiple executors **concurrently**.
Orchestrator marks them in TASK_CONTEXT.md (`Depends on: —`).

```
Example: "Add filtering by status"
   Condition: API contract is fixed in `.feature`
   ├── backend-dev (Phase 1): endpoint + unit tests
   └── frontend-dev (Phase 1): filter UI component + unit tests
```

> Parallelism cap: no more than 4 executor agents concurrently for one task.
> Beyond that, orchestrator loses reliable control over TASK_CONTEXT.md and traces.
> If you have more than 4 independent parts — group them into prioritized batches.

#### 1.1.5 Orchestrator anti-patterns

```
✗ Assign backend-dev without `.feature` → run architect first
✗ Assign frontend-dev if API contract is not fixed yet
✗ Combine executor and critic in the same agent for the same task
✗ Run independent parts sequentially instead of in parallel
✗ Skip architect when changing a cross-service contract
```

---

### 1.2 Model selection policy

> Concrete model names are defined in the project file: availability depends on platform and budget.
> This spec defines task types and required characteristics; PROJECT.md maps them to specific models.

#### 1.2.1 Task types and required characteristics

| Task type | Required characteristics | Preferred | Alternative |
|---|---|---|---|
| Orchestration / Planning | Deep reasoning, task decomposition, ADR + TASK_CONTEXT work. Strong instruction following. | Gemini 2.5 Pro · Claude Opus 4.6 | GPT-5.1 · Claude Opus 4.5 |
| Architecture / ADR | Contradiction analysis, domain modeling, threat modeling. Multi-step reasoning about consequences. | Gemini 2.5 Pro · Claude Opus 4.6 | GPT-5.1 · Claude Opus 4.5 |
| Code generation (executor) | Producing code, tool use, writing tests. High instruction-following precision. | Claude Sonnet 4.6 · GPT-5.3-Codex | GPT-4.1 · GPT-4o · Gemini 3 Pro · GPT-5.1-Codex |
| IaC / DevOps | Terraform/Helm/CI generation. Syntax accuracy is critical: IaC mistakes become production incidents. | Claude Sonnet 4.6 · GPT-5.2-Codex | GPT-4.1 · Gemini 3 Pro |
| Critique (critic agents) | Strict checklist adherence, structured output, catching violations in code. | Never below the executor tier in the same task | — |
| Security review | Broad OWASP/CVE knowledge, STRIDE/SLSA reasoning. | Claude Sonnet 4.6 · Gemini 2.5 Pro | GPT-5.1 |
| Documentation | README, How-to, test plans. Moderate complexity. | Claude Haiku 4.5 | GPT-5 mini · GPT-4o · GPT-4.1 · Gemini 3 Flash |

#### 1.2.2 Critic/executor parity rule

```
A critic must NEVER be weaker than the executor it reviews.
A weaker critic model systematically misses executor mistakes — sycophancy effect.
```

#### 1.2.3 Model tier hierarchy

> Used to apply the parity rule: choose a critic from tier ≥ executor tier.
>
> 0x multiplier (GPT-4.1 · GPT-4o · GPT-5 mini · Raptor mini): included in GitHub Copilot subscription with no additional token billing. When quality is equal, prefer 0x.

| Tier | Models | Characteristics |
|---|---|---|
| T1 — Frontier | Gemini 2.5 Pro (1x) · GPT-5.1 (1x) · GPT-5.1-Codex-Max (1x) · Claude Opus 4.6 (3x) · Claude Opus 4.5 (3x) | Deep reasoning, complex planning, threat modeling |
| T2 — Balanced | Claude Sonnet 4.6 (1x) · Claude Sonnet 4.5 (1x) · Claude Sonnet 4 (1x) · GPT-5.3-Codex (1x) · GPT-5.2-Codex (1x) · GPT-5.1-Codex (1x) · GPT-5.2 (1x) · GPT-4.1 (0x) · GPT-4o (0x) · Gemini 3 Pro (1x) · Gemini 3.1 Pro (1x) · Grok Code Fast 1 (0.25x) | High-accuracy code gen / tool use at moderate cost |
| T2+ — Balanced (fast) | Claude Opus 4.6 fast mode (30x) | T1-like reasoning quality but ~30x cost; use only with hard time budget and short tasks |
| T3 — Efficient | Claude Haiku 4.5 (0.33x) · GPT-5 mini (0x) · Gemini 3 Flash (0.33x) · GPT-5.1-Codex-Mini (0.33x) · Raptor mini (0x) | Fast/economic; unambiguous tasks with clear I/O |

```
Application rule:
   Executor T1 → Critic T1
   Executor T2 → Critic T2 or T1
   Executor T3 → Critic T3, T2, or T1 (minimum T3)
```

#### 1.2.4 When a reasoning-heavy model is required

```
Required (T1 — Gemini 2.5 Pro / GPT-5.1 / GPT-5.1-Codex-Max / Claude Opus 4.6 / Claude Opus 4.5):
   - Task decomposition with implicit dependencies
   - Creating/reviewing a new ADR: alternatives, trade-offs, consequences
   - Resolving NEEDS_HUMAN: identify the root disagreement between executor and critic
   - Threat modeling (STRIDE): systematic attack-vector analysis
   - Circular dependency or bounded context analysis

Not required (T2 is enough: Claude Sonnet 4.6 / GPT-5.3-Codex / GPT-4.1 / Gemini 3 Pro):
   - Typical endpoints, CRUD, simple tests
   - Familiar tasks with clear `.feature` and established ADR
   - README, How-to, test plans
   - Critic review for straightforward checklists
```

#### 1.2.5 Using an efficient model instead of an expensive one

```
Use an efficient model if ALL conditions hold:
   - Task is unambiguous: inputs/outputs are clearly defined
   - No multiple interdependent decisions
   - Agent is not decomposing the task (orchestrator already produced a clear plan)
   - Large output (code/docs) with moderate context

Prefer 0x models (no extra billing): GPT-4o, GPT-4.1, GPT-5 mini, Raptor mini.
When quality is equal — choose 0x over 0.33x or paid models.

> GPT-4o and GPT-4.1 are T2 (Balanced) in capability and 0x in cost.
> For the conditions above, their quality is sufficient for doc and unambiguous tasks.
> Critic tier must still be ≥ executor tier (parity rule §1.2.2).
```

#### 1.2.6 Fallback when a model is unavailable

If the preferred model is unavailable (rate limit, quota, outage):

```
1. Use the Alternative from the same row in §1.2.1
2. If Alternative is also unavailable — choose another model from the same tier (§1.2.3)
3. If tier is downgraded — record in TASK_CONTEXT.md:
    “Replacement used: <model> instead of <preferred> because: <reason>”
4. Never downgrade critic tier below executor tier (parity rule §1.2.2)
```

---

## 1.3 Development Pipeline — from spec to production

> Based on: ATDD (Cunningham), TDD (Kent Beck, 2002), Quality Gates (CMMI),
> Shift-Left Testing (L. Smith, 2001).
> Each phase is a Quality Gate: without critic APPROVE, you cannot move forward.

### 1.3.1 Three levels of work

| Level | Prepared by | Example input | Output |
|---|---|---|---|
| Specs (requirements) | User + architect | feature described in words | `.feature` + `glossary.md` |
| Feature | User formulates | `feature/<id>-desc` | `TASK_CONTEXT.md` |
| Subtask | Orchestrator during decomposition | a row from TASK_CONTEXT Decomposition | commit + one trace line |

Task statement template:

```markdown
## Task
What to do: [1–3 sentences]

## Scenarios (from .feature or inline)
- Scenario: ...

## Area
[ ] Backend / Frontend / DevOps / IaC

## Exceptions / constraints
if any: ...
```

> Multi-sprint rule: if a task takes > 5 days, orchestrator must split it into multiple sprint-sized tasks before running the pipeline.
> Each sprint becomes a separate `TASK_CONTEXT.md`. Indicators the task is too big: decomposition yields > 10 subtasks or total estimate > 5 days.
> Action: NEEDS_HUMAN — “Task is too large for one TASK_CONTEXT; propose a sprint breakdown.”

---

### 1.3.2 Who writes which tests and when

> Tests are written **before or alongside code** (TDD/ATDD) — not after.
> Each test type belongs to a specific agent and phase.

| Test type | Who writes | When written | Who runs / verifies |
|---|---|---|---|
| `.feature` scenarios (Gherkin) | `architect` (or user) | Phase 0 — before implementation | `architect-critic` checks completeness |
| Unit tests (from `.feature`) | `backend-dev` / `frontend-dev` | Phase 1a — before code (Red) | critic checks: all Given/When/Then covered |
| Edge cases + Property-Based/Fuzz | `backend-dev` / `frontend-dev` | Phase 2, Cycle 2 | critic checks: no uncovered edge cases |
| Integration tests | `backend-dev` | Phase 2, Cycle 3 | critic checks: real DB/HTTP, no stub bypass |
| Contract tests (CDC) | `backend-dev` (provider) + `frontend-dev` (consumer) | Phase 2, Cycle 4 | critic checks: pact file is valid |
| E2E tests | `qa-engineer` | Phase 2, Cycles 1–3 — written in parallel; executed in Phase 2.5 | `qa-critic` checks: real user flow |
| Load tests (k6 / locust) | `qa-engineer` | Phase 2, Cycle 3 — after Integration; executed in Phase 2.5 | `qa-critic` checks: SLA RPS/p99/error rate recorded |
| Benchmarks (function perf) | `backend-dev` | Phase 3, Cycle 2 — only when optimizing a specific algorithm/query | critic checks: benchmark improves vs baseline |
| Regression run | `backend-dev` / `frontend-dev` + `qa-engineer` | Phase 3.5 — run existing tests; do not write new ones | critic checks: mutation score did not degrade |

> Rule: if a test type is not written by the time it is needed, that is a BLOCKER for moving to the next phase.
> E2E and Load tests are written ahead of time (Phase 2) and committed; in Phase 2.5 they are only executed.

---

### 1.3.3 Development Pipeline (9 steps: phases 0, 1, 2, 2.5, 3, 3.5, 4, 5, 6)

> Parallel execution: `backend-dev` and `frontend-dev` may work in Phases 1–2 concurrently if their subtasks do not depend on each other.
> Orchestrator explicitly marks independence in TASK_CONTEXT.md (`Depends on: —`).
> Critics operate independently per branch; orchestrator waits for APPROVE from both before entering Phase 2.5.
>
> Handing off results when going back a phase:
> every time you go backwards, orchestrator creates a new “fix” subtask and must carry over concrete findings
> from the completed phase’s Critique Report:
>
> ```
> ## Previous Attempts
> Returned from Phase N after [architect-critic / security-critic / qa-critic]:
> - BLOCKER | <category> | <file>:<line> | <issue> | <recommendation>
> - ...
> What we already tried and it did not work: [if this is not the first return]
> ```
>
> Executor starts with specific locations and problems — not “fix something”, but “fix X in file Y:Z”.
> Without `## Previous Attempts`, executor does not know why it is here and will repeat the same mistake (sycophancy / anchoring).

```
▼ PHASE 0 — Requirements (source of truth) — SDD: spec before code
┌─────────────────────────────────────────────────────────┐
│  User writes/updates domain/specs/*.feature              │
│  architect reviews: completeness, contradictions         │
│  architect-critic: APPROVE / REQUEST_CHANGES             │
│  max iter: 3 → if .feature not agreed → NEEDS_HUMAN      │
│    (requirements contradictory or incomplete —           │
│     user clarifies before Phase 1)                       │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE → specs are fixed →

▼ PHASE 1 — Development (TDD Red→Green loop)
┌─────────────────────────────────────────────────────────┐
│  1a. Executor writes tests from .feature (sets Red)      │
│  1b. Executor writes code (all tests Green)              │
│  Critic: are all Given/When/Then covered?                │
│  max iter: 3 per subtask                                 │
│  If tests not Green after iter=3 → NEEDS_HUMAN            │
│    (spec is contradictory or task statement needs edits) │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 2 — In-code tests (5 cycles)
┌─────────────────────────────────────────────────────────┐
│  Cycle 1: Unit — all .feature scenarios have coverage    │
│  Cycle 2: Edge cases — empty input, boundaries, 4xx/5xx  │
│           Property-Based/Fuzz — parsers, deserializers,  │
│           and external data formats                      │
│  Cycle 3: Integration — real DB/HTTP                     │
│  Cycle 4: Contract — Consumer-Driven Contract            │
│  Cycle 5: Mutation — score ≥70%                          │
│  If Cycle 1/2/3/4 fails (code issue) → return to Phase 1 │
│    (code-fix subtask, iter+1)                            │
│  Mutation < 50% after iter=3 → BLOCKER → NEEDS_HUMAN     │
│  Mutation 50–70% → WARNING: transition allowed;          │
│    executor adds coverage in the same PR                 │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 2.5 — Deployed-system tests (Shift-Right)
┌─────────────────────────────────────────────────────────┐
│  devops-engineer: deploy to target environments          │
│    (configs — see project file)                          │
│  ↓ deploy APPROVE → qa-engineer takes over               │
│  Smoke: GET /health — all 200?                           │
│  E2E: automated tests against a live stack               │
│  Load: SLA RPS / p99 latency / error rate                │
│  If smoke fails → NEEDS_HUMAN (to devops, not QA)         │
│  If E2E fails (code issue) → return to Phase 1           │
│  If Load misses SLA → return to Phase 3 (performance)    │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 3 — Optimization / Refactor (2 cycles)
┌─────────────────────────────────────────────────────────┐
│  Cycle 1: Refactor (readability, structure)              │
│    → no new tests; existing tests must stay GREEN        │
│  Cycle 2: Optimization (performance)                     │
│    → if optimizing a specific algorithm/query:           │
│      executor writes a benchmark with baseline + target  │
│      (example: BenchmarkBulkInsert — was 500ms, target   │
│       <100ms); without benchmark there is no proof       │
│      of improvement → critic: BLOCKER                    │
│    → if optimization is systemic (Load→Phase 2.5):       │
│      benchmark not required; Phase 2 Load test is the    │
│      metric; rerun in Phase 3.5                          │
│  Cycles 1 and 2: mutation score must not degrade          │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 3.5 — Regression after optimization
┌─────────────────────────────────────────────────────────┐
│  Cycle 1: Unit + Integration — nothing broken?           │
│    backend-dev + frontend-dev run in-code tests          │
│  devops-engineer: redeploy optimized code                │
│  Cycle 2: Smoke on deployed system (again)               │
│    qa-engineer: smoke + critical E2E                     │
│  If tests fail → return to Phase 3 (iter+1)              │
│  Mutation score did not degrade?                         │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 4 — Architecture (1 pass)
┌─────────────────────────────────────────────────────────┐
│  architect + critic: does code comply with ADR?          │
│  bounded contexts respected?                             │
│  C4 model up to date after changes?                      │
│  BLOCKER (ADR violated / bounded context / circular dep  │
│    / public API without contract):                       │
│    → return to Phase 1 (code fix, iter+1)                │
│    → after fix: rerun Phase 4                            │
│  WARNING (C4 not updated / .feature outdated):           │
│    → architect updates docs in Phase 4                   │
│    → rerun Phase 4 (no return to Phase 1)                │
│  iter=3 without APPROVE → NEEDS_HUMAN                    │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 5 — Security (1 pass)
┌─────────────────────────────────────────────────────────┐
│  security + critic: OWASP Top 10, STRIDE                 │
│  Container images have no Critical CVEs?                 │
│  No secrets leaked into code?                            │
│  BLOCKER in code (OWASP injection / auth / secret):      │
│    → return to Phase 1 (code fix, iter+1)                │
│    → after fix: rerun Phase 5                            │
│  BLOCKER in image/infra (Critical CVE):                  │
│    → devops-engineer updates image within Phase 5        │
│    → rerun Phase 5 (no return to Phase 1)                │
│  iter=3 without APPROVE → NEEDS_HUMAN                    │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 6 — Documentation (1 pass)
┌─────────────────────────────────────────────────────────┐
│  documentation-writer + critic:                          │
│  README, API reference, How-to (Diataxis)                │
│  .feature updated if API changed?                        │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE → merge feature → develop
```

### 1.3.4 Why these cycle counts

| Phase | Cycles | Rationale |
|---|---|---|
| Development | max 3 iter/subtask | AutoGen rule: after 3 → NEEDS_HUMAN |
| In-code tests | 5 | unit; edge cases; integration; contracts (CDC); mutation score |
| Deployed tests | 1 | smoke+E2E+load: system is alive under load |
| Optimization | 2 | Cycle 1: Refactor; Cycle 2: Performance |
| Regression | 2 | Cycle 1: unit+integration; Cycle 2: smoke again |
| Architecture | 1 | ADR compliance is binary |
| Security | 1 | OWASP/STRIDE is binary: BLOCKER found or not |
| Documentation | 1 | API reference updates are binary |

### 1.3.5 When the user intervenes

```
Position A (normal):
   User states the task for the orchestrator once per sprint.
   Orchestrator runs the Pipeline autonomously.
   User receives the result after Phase 6.

Position B (NEEDS_HUMAN):
   Orchestrator is stuck at iter=3 without APPROVE.
   User receives NEEDS_HUMAN with a description of the disagreement.
   User decides and provides Human Input (see template below).
   Pipeline continues from the stuck point.

Position C (spec correction):
   During work, `.feature` is discovered to be incomplete.
   User updates `.feature`.
   Orchestrator reruns only the affected phases.
```

What happens after Human Input (Position B):

```
User adds ## Human Input to TASK_CONTEXT.md (template → §2.3):

   ## Human Input — [date]
   ### Decision on the blocker: <concrete instruction>
   ### Permission: [x] Rephrase subtask and restart at iter=0

Orchestrator reads the entry and then:
   1. If “Rephrase” — resets iter to 0 and updates subtask description in TASK_CONTEXT.md.
   2. If “Iteration 4” — continues the same subtask with iter=4, routed to the same executor.
   3. If “WONT_FIX” — closes the subtask; records the reason in ADR or TASK_CONTEXT.md Decisions; pipeline continues without it.

After re-entry, one executor loop runs: executor → critic → (APPROVE | NEEDS_HUMAN again).
If NEEDS_HUMAN occurs a second time on the same subtask — ESCALATED (see §3.3).
```

> The full `## Human Input` template and orchestrator details are in §2.3.

---

### 1.3.6 Test Failure Protocol

> Applies to any test failure in Phases 1, 2, 2.5, 3.5.
> Executor must record in `TASK_CONTEXT.md`: what failed (test, file:line), root cause (hypothesis), what was changed in the current iteration.

#### 1.3.6.1 Tests are failing (RED)

| Phase | Situation | Action | After iter=3 |
|---|---|---|---|
| **Phase 1** | Tests are not Green (code does not compile or assertions fail) | Executor fixes code → critic → repeat | NEEDS_HUMAN: "tests do not match the spec — `.feature` may be contradictory" |
| **Phase 2, Cycles 1–4** | Unit / Edge / Integration / Contract failed | Executor fixes code → return to Phase 1 (subtask: code-fix, iter+1) | NEEDS_HUMAN after 3 attempts in Phase 1 |
| **Phase 2.5** | E2E failed (code issue, not env) | qa traces the failure → orchestrator returns to Phase 1 (code-fix) | NEEDS_HUMAN after iter=3 |
| **Phase 2.5** | Smoke failed (env / deploy issue) | NEEDS_HUMAN immediately to devops-engineer (not to qa) | — |
| **Phase 3.5** | Unit / Integration failed after refactor | Return to Phase 3 (iter+1) | NEEDS_HUMAN after iter=3 |
| **Phase 3.5** | Smoke failed after re-deploy | NEEDS_HUMAN to devops-engineer | — |

#### 1.3.6.2 Insufficient coverage

| Situation | Severity | Action | After iter=3 |
|---|---|---|---|
| Mutation score **< 50%** (Phase 2, Cycle 5) | BLOCKER | Executor adds tests → critic → repeat | NEEDS_HUMAN: "coverage is unreachable without refactoring code or extending the test plan" |
| Mutation score **50–70%** (Phase 2, Cycle 5) | WARNING | Transition to Phase 3 is allowed; executor **must** add coverage in the same PR before merge | If WARNING is not resolved before merge → ACKNOWLEDGED thread in PR |
| Mutation score **degraded** after refactor (Phase 3.5) | BLOCKER | Return to Phase 3 to restore coverage | NEEDS_HUMAN after iter=3 |
| Not all `.feature` scenarios have a Unit test (Phase 2, Cycle 1) | BLOCKER | Executor adds missing tests | NEEDS_HUMAN after iter=3 |

> **Goal of return:** executor must ensure that **all tests pass** (GREEN) before
> the orchestrator initiates transition to the next phase again. Return means not "take a look",
> but "fix until fully passing".
>
> **Recording rule:** see "Passing results on return" in the Pipeline preamble —
> each `## Previous Attempts` line is populated from the findings of the completed phase's `Critique Report`.
> This ensures the Reflexion cycle and prevents repeating the same mistakes.

#### 1.3.6.3 REJECT verdict

| Situation | Action |
|---|---|
| Critic issued `REJECT` (fundamental constitutional violation) | Orchestrator **immediately** stops iterations; retry is impossible without reconsidering the task |
| — | Records a span `operation: "escalate"` in the JSONL trace (§4.6.2) |
| — | Sets `TASK_CONTEXT.md` status to `NEEDS_HUMAN` with the critic's explanation |
| — | Task is returned to the human: reason for REJECT + what needs to change in the problem statement |

> **Difference from NEEDS_HUMAN due to iter=3:** REJECT does not depend on the number of iterations — it is a qualitative assessment,
> not an exhausted limit. The task is not resumed without explicit human approval.

---
### 1.3.7 Alignment with Reflexion loop

The Pipeline does not replace the internal executor→critic loop (max 3 iter) — it is built **on top of** it.
Each phase consists of one or more subtasks, each going through a Reflexion cycle.

```
[Pipeline]
  └─ Phase 1: Development
       └─ subtask: write tests       [executor → critic, max 3]
       └─ subtask: implement handlers [executor → critic, max 3]
  └─ Phase 2: Tests
       └─ subtask: cycle 1 unit      [executor → critic, max 3]
       └─ subtask: cycle 2 edge cases [executor → critic, max 3]
```

---

### 1.3.8 Shortened Pipeline Paths (Fast-Track)

The full 9-phase pipeline is intended for **feature work** on `feature/*` branches.
For other types of changes — shortened paths:

| Change type | Branch | Active phases | Skip |
|---|---|---|---|
| **Feature** (default) | `feature/*` | 0 → 1 → 2 → 2.5 → 3 → 3.5 → 4 → 5 → 6 | — |
| **Lightweight feature** (atomic change with no architectural impact) | `feature/*` | 1 → 2 (unit+edge) → 5 | 0, 2.5, 3, 3.5, 4, 6 |
| **Hotfix** (urgent bug in `main`) | `hotfix/*` | 1 → 2 (unit+regression only) → CI Gate 1 → 5 | 0, 2.5, 3, 3.5, 4, 6 |
| **Docs-only** | `docs/*` | 6 → CI Gate 1 | 0, 1, 2, 2.5, 3, 3.5, 4, 5 |
| **Docs + `.feature` changed** | `docs/*` | 0 → 6 → CI Gate 1 | 1, 2, 2.5, 3, 3.5, 4, 5 |
| **IaC/Config-only** | `infra/*` | 1 → 2 (integration) → 2.5 (smoke) → 5 | 0, 3, 3.5, 4, 6 |
| **Security-patch** (dependency update due to CVE, no logic change) | `hotfix/*` or `infra/*` | 2 (unit+regression) → 5 (CVE-scan) → CI Gate 1 | 0, 2.5, 3, 3.5, 4, 6 |
| **Agent prompt update** | `feature/*` | §5 procedure → CI Gate 1 | 0–6 pipeline |

**Hotfix procedure:**

```
1. branch: hotfix/<id>-<slug> from main
2. Phase 1: executor → quick fix (max 2 iter, no full TDD)
3. Phase 2: unit tests only — existing tests are not broken, regression test for the bug
4. CI Gate 1: all tests green
5. Phase 5: security-critic — no secrets leaked?
6. PR → merge to main + tag vX.Y.(Z+1)
7. Backmerge: main → develop (required)
```

**Rollback procedure (when the hotfix will take > 30 minutes):**

```
1. git revert <last-good-commit> --no-edit
2. Additional PR → fast-merge into main (CI Gate 1, skip Gate 2/3)
3. tag: vX.Y.Z-rollback
4. Backmerge: main → develop
5. Hotfix continues in the hotfix/* branch in parallel
```

> **Rule:** orchestrator checks the change type before starting the pipeline.
> Hotfix criterion: bug is reproducible in `main`, no time for the full cycle.
> Docs-only criterion: only `*.md`, `*.txt`, `*.rst`, `*.feature` files changed, no code/IaC changes.
> **Lightweight feature criterion** (ALL conditions must be met):
>   - Change is isolated within one module / package; no cross-module API changes
>   - No new external dependencies and no database schema migrations
>   - No conflict with ADR and no new ADR required
>   - No public API changes (adding a field to an internal type / method is allowed)
>   - Change does not touch authentication, authorization, or PII
>   If any condition is not met — run the full feature pipeline.
> **Exception:** if docs-only includes changes to `.feature` files — architect-critic is **required** (Phase 0 is not skipped because the observable behaviour specification has changed).
> **Docs + `.feature`: roles in Phase 0** — `architect` reviews the modified `.feature` files; `architect-critic` issues the verdict (APPROVE / REQUEST_CHANGES). Other executors are not involved in this Fast-Track.

---

### 1.4 Manual Test Plans

> Based on: [IEEE 829-2008](https://standards.ieee.org/ieee/829/) (Test Case Specification, Test Procedure Specification),
> [Session-Based Test Management](https://www.satisfice.com/sbtm) (James Bach, 2000), ISTQB Foundation.
>
> A manual test plan is a **step-by-step guide** for a human (QA, product owner, developer)
> to verify UI and user scenarios.
> It complements automated tests: covers visual layout, complex UX flows,
> cross-browser behaviour, accessibility — everything that is expensive or impossible to fully automate.

#### 1.4.1 Who creates it and when

`frontend-dev` creates a manual test plan when:

```
- Implementing a new critical user flow (any scenario from .feature)
- Changing the observable behaviour of an existing flow
- Adding a form with validation, a multi-step wizard, a new state (empty, error, loading)
- Adding a new page or navigation route
```

The test plan **must be updated** whenever the observable behaviour changes — just like `.feature`.
Stored at: `docs/test-plans/<feature-name>.md` (canonical path).

#### 1.4.2 Format (IEEE 829 Test Procedure Specification + Gherkin scenarios)

```markdown
# Manual Test Plan: <Feature Name>
<!-- Scenario ref: domain/specs/<file>.feature -->

**Target environment:** staging | dev | local
**App version:** X.Y.Z
**Last updated:** YYYY-MM-DD

## Prerequisites
- [ ] Environment deployed: <URL>
- [ ] Account with role: <role / permissions>
- [ ] Test data: <what must exist in the system>
- [ ] Browser / device: <list if cross-browser test>

## TC-001: <Test Case Name>
**Scenario ref:** `<file>.feature : Scenario: <name>`
**Goal:** <what we are verifying — one sentence>

| # | Action | Expected result |
|---|--------|-----------------|
| 1 | Open <URL> | Page loads; heading <X> is visible |
| 2 | Click the "<Label>" button | <Y> opens; URL becomes <Z> |
| 3 | Enter "<value>" in the "<Field>" field | Field accepts input; no validation error appears |
| 4 | Click "Submit" | Form closes; a new entry appears in the table |

**Pass criteria:** <observable sign of success — without the word "works">
**Fail criteria:** <observable sign of failure>
**Edge cases to probe:** <boundary conditions for exploratory testing (SBTM charter)>

## TC-002: ...
```

#### 1.4.3 Composition rules

```
- Each step = one action + one expected result
- Expected result: only what the tester sees (not the internal state of the system)
- Preconditions are specific: not "log in" but "log in as role=admin"
- Each TC is linked to a .feature scenario via Scenario ref
- Pass/Fail criteria do not contain "works" / "does not work" — only observable signs
- Test plan is understandable by the product owner without knowledge of the code
```

---

## 2. Work Protocol: Sessions and Memory

### 2.1 `TASK_CONTEXT.md` structure

Orchestrator creates this file at the beginning of each session:

```markdown
# Task Context — [date] [task-slug]

**trace_id:** YYYYMMDD-task-slug  
**trace_file:** .agents/traces/YYYYMMDD-task-slug.jsonl
**fast_track:** feature | hotfix | docs-only | docs+feature | infra | security-patch | agent-prompt-update

## Task
[Full description from the user — ORIGINAL text, not a paraphrase]

## Decomposition
| # | Subtask | Role | Depends on | Iteration | Status |
|---|---|---|---|---|---|
| 1 | ... | backend-dev | — | 1/3 | IN_PROGRESS |
| 2 | ... | backend-dev | — | 0/3 | TODO |
| 3 | ... | frontend-dev | #2 | 0/3 | BLOCKED |

## Previous Attempts
<!-- Filled after each REQUEST_CHANGES (Reflexion pattern). -->

### Task #N — Iteration M
**Critique:**
- BLOCKER: path/to/file.go:45 — description

**What the executor will change in the next iteration:**
- ...

## Decisions made in this session
- [critic, iter 2]: description (APPROVED)

## Blockers / NEEDS_HUMAN
- none
```

Parallel agents and `TASK_CONTEXT.md`:
- When multiple executors run concurrently, each executor updates only its own row in `## Decomposition` and must not edit other agents’ rows.
- Shared sections (`## Blockers`, `## Decisions made in this session`) are updated only by the orchestrator.
- Race condition handling: if two agents finish at the same time, orchestrator applies both updates sequentially, keyed by subtask number.

---

### 2.2 Memory rules

1. **Short-term memory (session):** `.agents/session/TASK_CONTEXT.md`
   - Created by the orchestrator; updated by all agents during the session
   - Must be added to `.gitignore`

2. **Long-term memory (ADR):** `.github/decisions/`
   - Architectural decisions that must not be violated
   - Orchestrator and architect must check before making decisions
   - Committed to the repo and reviewed like code

3. **Repository context (persistent):** `AGENTS.md` in each repo
   - Automatically read by the agent on each task
   - Updated when conventions change

4. **Context Window Management**
   - If `TASK_CONTEXT.md` exceeds ~200 lines / ~4000 words, or orchestrator observes planning quality degradation, create a summarized version (replace detailed history of completed phases with a short recap).
   - The summary must contain: the current plan + the last 2 entries from `## Previous Attempts`.
   - Archive the full file as `.agents/session/TASK_CONTEXT_archive_<date>.md` (gitignored). Long-term memory remains in ADRs and `.agents/traces/` (committed).
   - Agents use `grep_search` to jump to the needed section.

Example summary version (replaces a verbose TASK_CONTEXT after ~200 lines):

```markdown
## Summary (archived: TASK_CONTEXT_archive_2026-02-23.md)
Phases 0–2: COMPLETED. Key decisions: ADR-003 (bulk endpoint), ADR-004 (rate limiting).
Current position: Phase 3, Cycle 1 (Refactor)

## Decomposition (active only)
| # | Subtask | Role | Status |
|---|---|---|---|
| 5 | Refactor handlers/bulk.go | backend-dev | IN_PROGRESS |

## Previous Attempts (last 2)
...
```

---

### 2.3 Re-entry protocol after NEEDS_HUMAN

```markdown
## Human Input — [date]

### Decision on the blocker
[Decision text — a concrete instruction]

### Updated acceptance criteria (if needed)
- [new criterion]

### Permission for the next iteration
- [ ] Start iteration 4 (exception to max=3)
- [x] Rephrase the subtask and restart at iter=0
- [ ] Close the subtask as WONT_FIX
```

Orchestrator upon receiving Human Input:
1. Appends `## Human Input` to `TASK_CONTEXT.md`.
2. Resets the subtask iteration counter to 0 (if “rephrase” was chosen).
3. Continues the workflow with the updated criteria.

---

## 3. Critique Rubrics (Constitutional Checklists)

### 3.0 Constitutional principles for agents (Constitutional AI, Anthropic, 2022)

Every agent follows these principles regardless of the task:

1. **Do not violate ADRs** — a decision that contradicts an ADR requires a new ADR or NEEDS_HUMAN.
2. **Do not edit files outside your area** — e.g., backend-dev must not touch IaC; devops must not touch business logic.
3. **Do not propose breaking changes without explicit justification** — public API changes require a concrete rationale (at minimum: why + which consumers are affected).
4. **Do not hard-code secrets and configuration** — not “for tests”, not “temporarily”.
5. **Do not bypass tests** — do not delete tests, do not add Skip()/ignore without justification, do not comment out assertions.
6. **Do not add dependencies without justification** — a new import requires an explicit rationale in the commit or PR.
7. **Artifact language is English; user communication language is Russian**

   | Artifact | Language |
   |---|---|
   | Code, code comments | English |
   | README, AGENTS.md, llms.txt, SKILL.md | English |
   | API Reference, OpenAPI descriptions | English |
   | `.feature` (Gherkin) scenarios | English |
   | ADR, CHANGELOG | English |
   | Commit messages | English (Conventional Commits) |
   | Agent messages to the user (chat, NEEDS_HUMAN, questions) | Russian |
   | `TASK_CONTEXT.md` (internal session file) | Russian |

   > **Rationale:** artifacts are committed to the repo and processed by tools (grep, IDE, CI) — English is required for compatibility. Communicating with the user in Russian reduces cognitive load and avoids meaning loss.
   >
   > **Critic check:** code comments and docs must not contain Russian text. If Russian text is found in code or documentation — BLOCKER.

8. **Work in small batches** (DORA AI Capabilities, 2025)

   During decomposition, orchestrator must ensure:
   - Each subtask is ≤ ~1 day of work (≈1–3 hours of LLM time)
   - Each subtask produces a self-contained atomic commit (one PR per feature branch)
   - Large tasks are decomposed vertically (end-to-end slices), not horizontally (“all tests” → “all code”)
   - If the task cannot be split — NEEDS_HUMAN with justification

   > **Rationale:** DORA 2025 reports the strongest AI impact for teams that practice small batches.
   > Smaller tasks speed up Reflexion loops, reduce accumulated debt in `TASK_CONTEXT.md`, and lower the risk of context loss.

---

### 3.1 Mandatory rules for the Orchestrator

**Rule 0 — Pass the task without paraphrasing**
> Orchestrator must pass the executor the original task text (from the user or `.feature`), not a retelling.
> Paraphrasing distorts acceptance criteria and creates drift between spec and implementation.

**Rule 1 — Check ADRs before decomposition**
> Before creating `TASK_CONTEXT.md`, orchestrator reads `.github/decisions/` and checks for conflicts.
> If there is a conflict — NEEDS_HUMAN before any work starts.

**Rule 2 — Choose the fast-track before starting the pipeline**
> Orchestrator determines the change type (feature / hotfix / docs-only / infra) and records it explicitly in `TASK_CONTEXT.md`.
> The full 9-phase pipeline runs only for feature branches (see §1.3 Fast-tracks).

**Rule 3 — Create the trace first**
> Create `.agents/traces/<trace_id>.jsonl` and write the root span (`operation: "plan"`) before assigning the first subtask.

**Rule 4 — Fill `## Previous Attempts` before returning**
> After each REQUEST_CHANGES, orchestrator must copy findings from the Critique Report into `## Previous Attempts` in `TASK_CONTEXT.md` for the next iteration.
> This is orchestrator responsibility, not executor or critic.
> Format: see the preamble in §1.3.3.
> Without this, the executor will not know why it is back and will repeat the same mistake (sycophancy / anchoring).

**Rule 5 — WONT_FIX: close a subtask before ESCALATED**
> If the user changed their mind, the requirement became obsolete, or is no longer relevant before ESCALATED, orchestrator may close the subtask as WONT_FIX without escalation:
> 1. Update the subtask status in `TASK_CONTEXT.md` → `WONT_FIX`
> 2. Record the reason in `## Decisions made in this session`
> 3. If the subtask blocked others — revise the decomposition plan
> 4. Continue the pipeline with remaining subtasks
>
> Do not bump iteration counters and do not create an ADR (unless an architectural decision is involved).
> WONT_FIX for a BLOCKER subtask related to security or ADR requires explicit user confirmation in `TASK_CONTEXT.md`.

**Rule 6 — Close the task with a complete trace**
> Before writing `operation: "complete"`, orchestrator verifies that `.agents/traces/<trace_id>.jsonl` contains entries from every agent that participated.
> If an agent’s entries are missing, orchestrator adds a synthetic span (`"synthetic": true`) and records a warning in `TASK_CONTEXT.md`.
> The task is not DoD-complete without the final trace entry `operation: "complete"`.

---

### 3.2 Mandatory rules for all Executors

**Rule 0 — Reflexion: read the past before each iteration (Shinn et al., 2023)**
> Before starting each iteration, executor must read `## Previous Attempts` in `TASK_CONTEXT.md`.
> If the section is absent — it is the first iteration.
> If present — executor explicitly acknowledges the prior critique and states what will be changed to address it.

**Rule 1 — ReAct: explicit reasoning before action (Yao et al., 2022)**
> Before each tool call, executor explains why it is needed.
> After the call, executor records the observation and decides the next step.

**Rule 2 — Responsibility boundary**
> Executor must not edit files outside their role (see principle 2).
> If changes are needed in another area, executor requests orchestrator action rather than editing directly.

**Rule 3 — Trace writing**
> After completing each iteration (execute or critique), append one JSONL line to `.agents/traces/<trace_id>.jsonl`.

---

### 3.3 Mandatory rules for all Critics

**Rule 1 — Context isolation (anchoring bias prevention)**
> Critic sees only the final result.
> Critic must not rely on chain-of-thought, intermediate steps, or the author’s explanations.
> Critic knows only: original task + acceptance criteria + produced result.

**Rule 2 — Finding format (Self-Refine format)**

```
1. What is wrong:     specific location (file:line)
2. Why:              root cause
3. How to fix:       actionable recommendation
```

> Findings without a specific location do not count.

**Rule 3 — Iteration limit (AutoGen / LangGraph)**

```
max_iterations: 3

After the 3rd iteration without APPROVE:
   → NEEDS_HUMAN: describe the disagreement in 2–3 sentences
   → stop and hand off to the user
```

Healthy-critic signal:
- 1–2 BLOCKER findings for a medium task
- 0 findings → critic is too soft (sycophancy)
- 5+ BLOCKER findings → rubric is too strict/unclear; needs calibration

**Rule 4 — Critic tools (CRITIC paper)**

```
All critics: read-only tools only (read_file, grep_search)
Exception: devops-critic is additionally allowed syntax validators
   (e.g., terraform validate, docker compose config --quiet)
Without tools, critics hallucinate syntax checks.
```

**Rule 5 — Conflicts between multiple critics on one PR**

```
If multiple critics review one PR and their verdicts disagree:
   - Any REJECT from any critic → PR must not be merged
   - Any open BLOCKER blocks merging (Gate 3)
   - APPROVE from one + REQUEST_CHANGES from another →
         executor addresses REQUEST_CHANGES; both must reach APPROVE
   - architect-critic REJECT for ADR violation overrides other APPROVE verdicts:
         requires a new ADR or NEEDS_HUMAN, not just a code patch
```

**Rule 6 — ESCALATED: repeated NEEDS_HUMAN on the same subtask**

ESCALATED status is set by orchestrator when:
- NEEDS_HUMAN occurs a second time on the same subtask (after re-entry), OR
- During a dispute on a BLOCKER, executor and critic do not converge after 2 iterations

What orchestrator records in `TASK_CONTEXT.md`:

```markdown
## Blockers / NEEDS_HUMAN
- ESCALATED: Subtask #N — <disagreement summary>
  Attempts: iter 1–3 + re-entry iter 1–3 — APPROVE not reached
  Expected: product owner / tech lead decision
```

Difference between NEEDS_HUMAN and ESCALATED:
- NEEDS_HUMAN — quick developer clarification
- ESCALATED — exceeds team competence; requires owner / tech lead

What happens after ESCALATED:

1. Orchestrator stops the subtask.
   - Subtask status in `TASK_CONTEXT.md` → ESCALATED (not BLOCKED, not IN_PROGRESS).
   - Pipeline does not progress on this subtask.
   - Independent subtasks continue (parallel branches are not blocked).

2. Orchestrator notifies the user.

   Message format:
   ```text
   ESCALATED: Subtask #N "<name>"
   Disagreement: <2–3 sentences>
   Attempts: <N> iterations including re-entry after Human Input
   Executor position: <brief>
   Critic position: <brief>
   Decision needed: <a concrete question>
   ```

3. A human (tech lead / product owner) decides.
   - A. Accept executor’s position → write an ADR documenting the exception; critic accepts the documented decision; subtask continues with iter=1.
   - B. Accept critic’s position → rephrase the subtask with the critic requirement; executor gets updated task statement; iter=1.
   - C. Change the requirement (new ADR or `.feature` change) → update `.feature` or create an ADR; affected pipeline phases restart.
   - D. Close as WONT_FIX → close subtask and record reason in `TASK_CONTEXT.md`; pipeline continues without it; orchestrator revises the plan if it blocked other subtasks.

4. Orchestrator records the decision.

   ```markdown
   ## Human Input — [date]
   ### ESCALATED — Subtask #N
   Decision: <A|B|C|D> — <rationale>
   Orchestrator action: <what is restarted>
   ```

After recording, the pipeline resumes per the chosen option. If ESCALATED repeats for the same subtask, pause the task until an out-of-band architecture review.

**Rule 7 — Trace writing (critic)**
> After each verdict, append a JSONL line to `.agents/traces/<trace_id>.jsonl`.
> `trace_id` comes from `TASK_CONTEXT.md`.
> Set `parent_span_id` to the orchestrator’s `span_id`.
>
> Example critic line (`operation: "critique"`):
> ```jsonl
> {"ts":"2026-02-24T10:00:00Z","trace_id":"20260224-task","span_id":"s03",
>  "parent_span_id":"s01","agent":"backend-critic","operation":"critique",
>  "subtask":1,"iteration":1,"verdict":"REQUEST_CHANGES",
>  "blockers":1,"warnings":2,"input_tokens":980,"output_tokens":310,"duration_ms":9100}
> ```
> Full format: MULTI_AGENT_SPEC.md §4.5–4.6.

---

Critic returns a structured response:

````markdown
## Critique Report

**VERDICT:** APPROVE | REQUEST_CHANGES | REJECT

> **APPROVE** — no BLOCKER findings; WARNING/SUGGESTION are allowed.
> **APPROVE** is also allowed if all remaining WARNING are explicitly marked as ACKNOWLEDGED
>   in `## Previous Attempts` (executor knowingly defers the fix in the PR thread).
>   Without explicit ACKNOWLEDGED — REQUEST_CHANGES.
> **REQUEST_CHANGES** — there is a BLOCKER; or there is a WARNING without explicit ACKNOWLEDGED: fixable in the next iteration.
> **REJECT** — fundamental constitutional violation (ADR violated without new ADR; work performed outside the agent’s responsibility boundary; executor reinterpreted the task without coordination). Not fixable via patch — requires orchestrator rephrasing.

**Example of correct ACKNOWLEDGED** (in `## Previous Attempts` or PR thread):

```markdown
ACKNOWLEDGED: WARNING | performance | services/bulk.go:120 | N+1 query | Deferred to task #42 (bulk-optimization)
ACKNOWLEDGED: WARNING | style       | models/host.go:34   | Missing godoc | Add next sprint — does not block release
```

> Without an `ACKNOWLEDGED` line, critic must return REQUEST_CHANGES even on repeated review.

### Findings

| Severity | Category | Location | Issue | Recommendation |
|---|---|---|---|---|
| BLOCKER | security | handlers/host.go:45 | Input not validated | Add validation middleware |
| WARNING | performance | services/bulk.go:120 | N+1 query | Collect IDs; do one bulk query |
| SUGGESTION | conventions | models/host.go:33 | Missing godoc | Add a comment |
````

### 3.4 Backend Critic rubric

> Applies to any server-side language and framework.
> Project file extends it with stack-specific triggers (Go, Java, Python, etc.).

```
BLOCKER triggers:
- [ ] Unvalidated/unsanitized input from an external source (HTTP, queue, file, env)
- [ ] Error is propagated without context — caller cannot determine the cause
- [ ] Error is silently ignored (e.g., `_ = err`, `except: pass`, empty `if err != nil {}`) — failure becomes invisible
- [ ] Manual edits to auto-generated code
- [ ] Hard-coded configuration: URLs, ports, credentials, environment-specific values
- [ ] Concurrent block / background task without panic/exception handling
- [ ] Data race on shared mutable state
- [ ] New module/package without tests
- [ ] New public API endpoint without a contract test
- [ ] Test without assertions — always green regardless of behavior
- [ ] Mutation score < 50%
- [ ] Resource leak: unclosed connections, file descriptors, runaway background tasks
- [ ] Test skipped (skip/ignore) without an issue link
- [ ] New dependency (import) added without explicit justification in commit/PR (violates constitutional principle 6)
- [ ] Code comment is not in English (constitutional rule 7)

WARNING triggers:
- [ ] Function/method is significantly too large without an explicit reason
- [ ] Mutation score 50–70%
- [ ] Integration test without teardown/state cleanup
- [ ] Hard-coded test data (use factory/fixture)
- [ ] Global mutable state
- [ ] Blocking call in a concurrent/async context
- [ ] Code parses/deserializes external data (files, binary protocols, third-party JSON) without property-based or fuzz tests
- [ ] N+1 query pattern — loading items one-by-one in a loop (no batch/bulk)
- [ ] HTTP client/external service call without explicit timeout (can deadlock threads/goroutines)
- [ ] Request cancellation context is not propagated (context.Context, CancellationToken, AbortSignal)
- [ ] DB transaction is not rolled back on error path (partial writes, locks held; deadlock/inconsistency risk)

SUGGESTION triggers:
- [ ] Missing documentation on public API symbols
- [ ] Unclear one-letter variable names (except simple iterators)
```

### 3.5 DevOps Critic rubric

> Applies to any IaC tool and CI/CD platform.
> Project file extends it with stack-specific triggers (Terraform, Helm, GitHub Actions, Azure Pipelines, etc.).

```
BLOCKER triggers:
- [ ] Secret/credentials/token in source code or build artifact
- [ ] Secret is passed via build argument (remains in image layer history/artifacts)
- [ ] Infrastructure changes are applied without plan/dry-run review in CI
- [ ] No VCS ignore rules for IaC state files
- [ ] Base image/dependency with a Critical severity vulnerability (CVE)
- [ ] Admin/management port open to all addresses (0.0.0.0/0)
- [ ] Config is hard-coded instead of injected via environment variables (12-Factor III)
- [ ] Hostname/IP is hard-coded (12-Factor IV)
- [ ] Service has no health/readiness endpoint
- [ ] Container/pod runs as root (missing USER in Dockerfile or missing runAsNonRoot in orchestration manifest)

WARNING triggers:
- [ ] Image/artifact without pinned version (floating tag)
- [ ] IaC resource without metadata labels (cost attribution, owner, environment)
- [ ] CI pipeline step without a timeout
- [ ] Service has no health check definition in orchestration manifest
- [ ] Container/pod without CPU/memory limits (OOM/noisy-neighbor risk)
- [ ] Production image without multi-stage build (dev tools shipped to prod image; larger attack surface)
- [ ] No automated vulnerability scanning step in CI (without it, “Critical CVE” BLOCKER cannot trigger)

12-Factor App compliance (additional checks):
- [ ] BLOCKER: logs are written to a file, not stdout/stderr (Factor XI)
- [ ] WARNING: no graceful shutdown on SIGTERM (Factor IX)
```

### 3.6 Frontend Critic rubric

> Applies to any UI framework.
> Project file extends it with stack-specific triggers (React, Vue, Angular, etc.).

```
BLOCKER triggers:
- [ ] API key/token in client code (visible to the user)
- [ ] Type safety is disabled/bypassed without documented justification
- [ ] Component renders without handling loading and error states
- [ ] New component without a unit test
- [ ] Critical user flow without an E2E test
- [ ] Test skipped (skip/xskip/xit) without an issue link
- [ ] Comments/UI strings in components are not in English (constitutional rule 7)
- [ ] XSS via unsafe HTML rendering: dangerouslySetInnerHTML, innerHTML, v-html, or equivalent with unsanitized content

WARNING triggers:
- [ ] Component is significantly too large without an explicit reason (god component)
- [ ] Side effects with incomplete/incorrect dependencies (stale closure risk)
- [ ] HTTP requests directly in the component, bypassing a service/API layer
- [ ] No handling of 4xx/5xx responses
- [ ] Interactive element without a test identifier (data-testid or equivalent)
- [ ] API hook/store action lacks tests for loading/error/success
- [ ] Token/sensitive data is stored in localStorage/sessionStorage (XSS exposure)
- [ ] Subscription/event listener is not unsubscribed on unmount (memory leak; state updates on unmounted component)
- [ ] New critical user flow implemented without an updated manual test plan (§1.4)

SUGGESTION triggers:
- [ ] Missing accessibility attributes on interactive elements
- [ ] Duplicated styling logic not extracted into a shared component/token
```

### 3.7 QA Critic rubric

> QA critic checks test scripts and scenario coverage quality — not production code.
> Project file extends it with concrete tooling (Playwright, k6, pytest, etc.).

```
BLOCKER triggers:
- [ ] Smoke test does not cover all health/readiness endpoints of the deployed system
- [ ] E2E test contains only protocol-level assertions and does not validate a real user flow
- [ ] Load test does not verify agreed SLA (RPS, latency percentile, error rate)
- [ ] A failing test is marked skip/xfail without an issue link
- [ ] Test environment URLs/credentials are hard-coded (violates 12-Factor III)
- [ ] Test depends on execution order (no scenario isolation)
- [ ] E2E does not reproduce the real user flow from `.feature`
- [ ] Benchmark test (Phase 3) has no baseline and no pass criterion (target)

WARNING triggers:
- [ ] No assertions on error rate (only latency or RPS)
- [ ] Load test duration is too short for stabilization
- [ ] Test data is not cleaned up after a run (dirty state)
- [ ] E2E test produces no artifact on failure (screenshot/log/video)
- [ ] Flaky test without a tracking issue
- [ ] External-service mock is used without contract validation (Pact/WireMock/OpenAPI) — mock drifts from real API

SUGGESTION triggers:
- [ ] Test file lacks logical grouping of scenarios
- [ ] Missing description of what the test checks and why it is product-critical
```

### 3.8 Architect Critic rubric

```
BLOCKER triggers:
- [ ] Bounded context violation: module/service directly accesses data from another context
- [ ] Decision contradicts an accepted ADR without a new ADR or explicit SUPERSEDES
- [ ] New public API published without a machine-readable contract spec
- [ ] Circular dependency between modules/services
- [ ] Event/message schema changed without versioning
- [ ] Breaking change in public API without versioning: major version not bumped and/or missing migration guide + CHANGELOG entry
- [ ] DB schema change breaks backward compatibility without a staged rollout plan (e.g., NOT NULL column without DEFAULT; renaming/removing a column in rolling deployment)

WARNING triggers:
- [ ] C4 diagram not updated after a structural change
- [ ] `.feature` spec not updated after observable behavior change
- [ ] New service/module without explicit bounded context mapping
- [ ] New external dependency without resilience strategy documentation (timeout/retry/fallback/circuit breaker) in ADR or architecture doc

SUGGESTION triggers:
- [ ] Missing rationale for the chosen pattern (why this approach?)
- [ ] Missing link to the relevant ADR in code/PR description
```

### 3.9 Security Critic rubric

> Security critic checks OWASP Top 10, STRIDE, and SLSA.
> OWASP LLM Top 10 applies only if the project contains AI/LLM components.
> Project file extends this with stack-specific checks (web headers, cloud IAM, network policies, etc.).

```
BLOCKER triggers:
- [ ] OWASP A01 Broken Access Control — operation runs without authorization checks
- [ ] OWASP A02 Cryptographic Failures — sensitive data stored/transmitted without encryption
- [ ] OWASP A03 Injection — user input reaches an interpreted context without sanitization
- [ ] OWASP A04 Insecure Design — the vulnerability is in the design (missing auth/rate limiting for a protected resource; or business logic allows abuse by design)
- [ ] OWASP A05 Security Misconfiguration — debug mode/verbose traces/internal data exposed in production; default credentials not changed
- [ ] OWASP A06 Vulnerable and Outdated Components — dependency/base image has a Critical CVE
- [ ] OWASP A07 Identification & Authentication Failures — weak/missing auth mechanisms
- [ ] OWASP A08 Software and Data Integrity Failures — artifacts are deployed without integrity/signature checks; pipeline allows unverified dependencies
- [ ] OWASP A10 SSRF — service accepts a user-supplied URL/address and makes outbound calls without allowlist
- [ ] OWASP LLM01 Prompt Injection — untrusted external content is used as instructions (markdown/file/API/webhook payload reaches system prompt/tools without sanitization)
- [ ] OWASP LLM02 Insecure Output Handling — AI output is rendered/executed as HTML/markdown/code without sanitization/validation
- [ ] OWASP LLM06 Supply Chain — AI-generated package/dependency is not verified (typosquatting; package did not exist prior)
- [ ] OWASP LLM09 Misinformation — AI component generates factual artifacts (SQL/API contracts/config) without verification; output used as source of truth without review/validation
- [ ] Secret/API key/password in source/config/build artifacts
- [ ] Missing authentication on a protected endpoint
- [ ] Inter-service communication without transport encryption

WARNING triggers:
- [ ] Missing rate limiting on public/auth endpoints
- [ ] Logs contain PII/sensitive data
- [ ] Dependency without pinned version (floating tag) — supply chain risk
- [ ] Inter-service/cross-origin requests allowed without explicit allowlist
- [ ] Production image without SBOM (CycloneDX/SPDX) in regulated environments
- [ ] Build without SLSA provenance ≥ SLSA L1 in regulated environments
- [ ] OWASP A09 Security Logging & Monitoring Failures — security events not logged or not filterable
- [ ] STRIDE: new endpoint/service added without a documented threat model in ADR (at least Spoofing/Tampering/Repudiation/Information Disclosure/DoS/EoP)

SUGGESTION triggers:
- [ ] Missing comment/annotation explaining why this auth pattern was chosen
- [ ] Unencrypted protocol used even in dev config
```

### 3.10 Documentation Critic rubric

```
BLOCKER triggers:
- [ ] README does not explain how to run the project locally from scratch (Quick Start)
- [ ] API Reference does not match the real schema (spec is outdated)
- [ ] `.feature` spec not updated after observable behavior changes
- [ ] Missing documentation for all required environment variables and allowed values
- [ ] Documentation (README, API Reference, `.feature`, ADR) is not in English (constitutional rule 7)

WARNING triggers:
- [ ] Tutorial section lacks a working end-to-end example with real output
- [ ] Missing at least two How-to guides for key user scenarios
- [ ] Technical term used without a definition in the glossary
- [ ] Code samples in docs do not run or produce different results
- [ ] CHANGELOG.md does not follow Keep a Changelog format when there is a release commit
- [ ] AGENTS.md not updated after convention/architecture changes (agents read it automatically; stale file causes drift)
- [ ] Manual test plan (§1.4) for a new/changed user flow is missing or outdated
- [ ] New module/package without a Component README (§0.7)

SUGGESTION triggers:
- [ ] Missing cross-links between related documentation sections
- [ ] Outdated screenshots or command outputs
- [ ] Diataxis structure is violated (Tutorial mixed with Reference)
```

---

### 3.11 Definition of Ready / Definition of Done

**Definition of Ready (DoR)** — what a task must contain before starting an executor:

```
- [ ] Task is specific (not “improve”, but “endpoint < 50ms”)
- [ ] Impacted files/modules are listed
- [ ] No ADR conflicts
- [ ] Acceptance criteria are defined
- [ ] Dependencies between subtasks are explicit
```

**Definition of Done (DoD)** — what must be true at APPROVE:

```
For code (backend):
- [ ] Tests are written and passing
- [ ] Formatting applied
- [ ] API spec updated if API changed
- [ ] No new BLOCKER or WARNING

For code (frontend):
- [ ] Lint clean
- [ ] Build succeeds
- [ ] No new BLOCKER or WARNING
- [ ] Manual test plan created/updated if a critical user flow was added/changed (§1.4)

For IaC:
- [ ] validate passes
- [ ] No secrets outside secret storage
- [ ] fmt applied
- [ ] CHANGELOG.md updated if a release commit exists (Added/Changed/Fixed/Security)
- [ ] No new BLOCKER or WARNING

For documentation (documentation-writer):
- [ ] README created/updated per §0.7 (Root or Component, depending on scope)
- [ ] API Reference matches real schema (OpenAPI / GraphQL schema)
- [ ] `.feature` updated if observable behavior changed
- [ ] Manual test plan created/updated for all impacted user flows (§1.4)
- [ ] CHANGELOG.md updated if a release commit exists
- [ ] AGENTS.md updated if conventions or repo structure changed
- [ ] No new BLOCKER or WARNING

For any change:
- [ ] Commit follows Conventional Commits
- [ ] Pre-commit hooks passed: fmt, lint, validate (before commit)
- [ ] TASK_CONTEXT.md updated with APPROVED status
- [ ] CHANGELOG.md updated if a release commit exists
- [ ] Trace entry `operation: "complete"` added to .agents/traces/<trace_id>.jsonl

PR merge gates (Gate 1–3; see §0.6):
- [ ] CI: all tests green; build succeeds
- [ ] Critic agent performed review and left comments
- [ ] All BLOCKER threads are RESOLVED
- [ ] All other threads are RESOLVED | ACKNOWLEDGED | DEFERRED (SUGGESTION only)
- [ ] At least 1 human reviewer → APPROVE
```

### 3.11.1 When to create an ADR

```
ADR is mandatory when:
- Choosing a technology/library with long-term architecture impact
- Any decision that contradicts or changes an existing ADR (must mark SUPERSEDES)
- Breaking change in public API or DB schema
- ESCALATED option A: executor position is accepted against critic — exception must be documented
- New dependency on an external service with a documented resilience strategy (timeout/retry/fallback)

ADR is optional but recommended when:
- Non-trivial pattern choice (why this approach?)
- Conscious deviation from a convention for a specific trade-off

Author: architect or orchestrator.
Format: §3.12.
```

### 3.12 ADR file format

Path: `.github/decisions/ADR-NNN-title.md`

```markdown
# ADR-NNN: Decision title

**Date:** YYYY-MM-DD
**Status:** PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED
**Author:** [agent or human]

## Context
[What happened, what problem exists, why a decision is needed]

## Considered alternatives
| Option | Pros | Cons | Why rejected |
|---|---|---|---|
| Option A | ... | ... | ... |
| Option B | ... | ... | Selected |

## Decision
[What exactly was decided — bullet points]

## Consequences
[What changes in the project: files, processes, constraints]

## What NOT to do
[Explicit prohibitions implied by the decision]
```

---

## 4. Observability AI Workflow

Goal: see what agents do, how much each iteration costs, and where the workflow gets stuck.

### 4.1 Standard: OpenTelemetry GenAI Semantic Conventions (CNCF, v1.40.0, 2025)

Each LLM invocation is a span with attributes:

```
gen_ai.system                 = "openai" | "anthropic" | "google"
gen_ai.request.model          = "gpt-4o" | "claude-sonnet-4-6"
gen_ai.operation.name         = "chat"
gen_ai.usage.input_tokens     = 1234
gen_ai.usage.output_tokens    = 456
gen_ai.response.finish_reason = "stop" | "length" | "tool_calls"
```

Current extensions (v1.40.0):

| Extension | URL | What it adds |
|---|---|---|
| **Agent Spans** | `semconv/gen-ai/gen-ai-agent-spans/` | Attributes for orchestrator frameworks: `gen_ai.agent.name`, `gen_ai.agent.id`, nested agent→tool spans |
| **MCP Semantic Conventions** | `semconv/gen-ai/mcp/` | Attributes for MCP calls: tool, server, result |
| **GenAI Events** | `semconv/gen-ai/gen-ai-events/` | Events (not spans): prompt, completion, tool_call |

To enable the latest attributes, set:
`OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental`

Nested calls form a tree:

```
[orchestrator]         ← root span of the task
   ├── [backend-dev]    iteration 1
   │     └── tool: run_in_terminal
   ├── [backend-critic] iteration 1 → REQUEST_CHANGES
   └── [backend-dev]    iteration 2 → APPROVE
```

### 4.2 AI Workflow metrics

| Metric | Formula | Signal |
|---|---|---|
| **iteration_count** | iterations per subtask | Always 3 → critic is too strict |
| **needs_human_rate** | NEEDS_HUMAN / total subtasks | > 20% → rubric/tasks issue |
| **approve_on_first** | APPROVE at iter=1 / total | < 30% → executor too weak or tasks too hard |
| **token_cost_per_task** | sum(input+output tokens) | Cost estimate by task type |
| **tool_failure_rate** | failed / total tool calls | Which tools are unstable |
| **severity_distribution** | % of BLOCKER/WARNING/SUGGESTION | Rubric calibration |

### 4.3 DORA metrics (DevOps process)

| Metric | Elite performance |
|---|---|
| **Lead Time for Changes** | < 1 hour |
| **Deployment Frequency** | multiple times per day |
| **MTTR** | < 1 hour |
| **Change Failure Rate** | < 5% |

Source: https://dora.dev (Google).

### 4.4 DORA AI Capabilities Model (2025)

[DORA State of DevOps 2025](https://dora.dev/research/) identifies 7 practices that amplify the impact of AI tools on team outcomes:

| Practice | Implementation in this spec |
|---|---|
| **Strong version control practices** | Feature branches, GitFlow, ADRs committed → §0.5 |
| **Working in small batches** | Orchestrator decomposes: ≤1 day per subtask; hotfix branches → §1.3 fast-tracks |
| **AI-accessible internal data** | AGENTS.md, llms.txt, SKILL.md, domain/ — machine-readable context → §0.1 |
| **User-centric focus** | `.feature` scenarios describe real user flows; Phase 0 fixes the spec → §1.3 |
| **Clear + communicated AI stance** | This spec is an explicit, documented AI stance |
| **Quality internal platform** | MCP servers, CI gates (Gate 1–3), observability pipeline → §0.6, §4 |
| **Healthy data ecosystems** | JSONL traces, AI metrics, golden evals — feedback loop → §4, §5 |

Projects with these practices show higher delivery speed, code quality, developer productivity, and product performance when using AI.

### 4.5 Trace log structure

```
.agents/
├── session/     ← TASK_CONTEXT.md (temporary)
└── traces/      ← JSONL session logs
   ├── YYYYMMDD-task-slug.jsonl
      └── ...
```

Single-record format examples:

```jsonl
{"ts":"2026-02-23T14:32:00Z","trace_id":"abc123","span_id":"s01","parent_span_id":null,
 "agent":"orchestrator","operation":"plan","task":"add bulk endpoint",
 "input_tokens":412,"output_tokens":89,"duration_ms":3200}

{"ts":"2026-02-23T14:32:05Z","trace_id":"abc123","span_id":"s02","parent_span_id":"s01",
 "agent":"backend-dev","operation":"execute","iteration":1,
 "input_tokens":1840,"output_tokens":620,"duration_ms":18400}

{"ts":"2026-02-23T14:33:10Z","trace_id":"abc123","span_id":"s03","parent_span_id":"s01",
 "agent":"backend-critic","operation":"critique","iteration":1,
 "verdict":"REQUEST_CHANGES","blockers":1,"warnings":2,
 "input_tokens":980,"output_tokens":310,"duration_ms":9100}
```

### 4.6 Trace writing protocol (who writes what and when)

There is no automatic instrumentation — agents write traces manually using normal file tools.

#### 4.6.1 Rules for agents

**Orchestrator** (when creating `TASK_CONTEXT.md`):
1. Assigns `trace_id` (format: `YYYYMMDD-<task-slug>`, e.g., `20260223-bulk-endpoint`)
2. Creates `.agents/traces/<trace_id>.jsonl`
3. Writes the root span (`operation: "plan"`)

**Each executor and critic** (after completing its operation):
1. Appends one JSONL line to the same file
2. Sets `parent_span_id` to the orchestrator’s `span_id`
3. Critics add `verdict`, `blockers`, `warnings`

#### 4.6.2 When to write

| Event | Who writes | `operation` |
|---|---|---|
| Orchestrator created the task plan | orchestrator | `"plan"` |
| Executor completed an iteration | executor (backend-dev, frontend-dev, ...) | `"execute"` |
| Critic produced a verdict | critic (backend-critic, ...) | `"critique"` |
| Orchestrator reached NEEDS_HUMAN | orchestrator | `"escalate"` |
| Orchestrator closed the task | orchestrator | `"complete"` |

#### 4.6.3 Example: complete trace for one task

```jsonl
{"ts":"2026-02-23T14:32:00Z","trace_id":"20260223-bulk-endpoint","span_id":"s01","parent_span_id":null,"agent":"orchestrator","operation":"plan","task":"add-bulk-endpoint","input_tokens":412,"output_tokens":89,"duration_ms":3200}
{"ts":"2026-02-23T14:32:05Z","trace_id":"20260223-bulk-endpoint","span_id":"s02","parent_span_id":"s01","agent":"backend-dev","operation":"execute","iteration":1,"input_tokens":1840,"output_tokens":620,"duration_ms":18400}
{"ts":"2026-02-23T14:33:10Z","trace_id":"20260223-bulk-endpoint","span_id":"s03","parent_span_id":"s01","agent":"backend-critic","operation":"critique","iteration":1,"verdict":"REQUEST_CHANGES","blockers":1,"warnings":2,"input_tokens":980,"output_tokens":310,"duration_ms":9100}
{"ts":"2026-02-23T14:33:15Z","trace_id":"20260223-bulk-endpoint","span_id":"s04","parent_span_id":"s01","agent":"backend-dev","operation":"execute","iteration":2,"input_tokens":2100,"output_tokens":540,"duration_ms":16200}
{"ts":"2026-02-23T14:34:05Z","trace_id":"20260223-bulk-endpoint","span_id":"s05","parent_span_id":"s01","agent":"backend-critic","operation":"critique","iteration":2,"verdict":"APPROVE","blockers":0,"warnings":1,"input_tokens":900,"output_tokens":180,"duration_ms":8400}
{"ts":"2026-02-23T14:34:10Z","trace_id":"20260223-bulk-endpoint","span_id":"s06","parent_span_id":"s01","agent":"orchestrator","operation":"complete","task":"add-bulk-endpoint","total_iterations":2,"input_tokens":6232,"output_tokens":1739,"duration_ms":127600}
```

#### 4.6.4 Analysis with jq (no extra instrumentation)

```powershell
# How many iterations did each task take?
Get-Content .agents\traces\*.jsonl | jq -s '[.[] | select(.operation=="complete")] | .[] | {task, iters: .total_iterations}'

# Where did critics reject most often?
Get-Content .agents\traces\*.jsonl | jq 'select(.operation=="critique" and .verdict=="REQUEST_CHANGES") | .agent'

# Total tokens by agent
Get-Content .agents\traces\*.jsonl | jq -s 'group_by(.agent) | .[] | {agent: .[0].agent, tokens: (map(.input_tokens + .output_tokens) | add)}'

# Tasks where escalation to a human was required
Get-Content .agents\traces\*.jsonl | jq 'select(.operation=="escalate") | .task'
```

### 4.7 Visualization tools

Run on demand — no always-on server required.

| Tool | Run/install | When you need it |
|---|---|---|
| **jq** | `winget install jqlang.jq` (Windows) / `brew install jq` (macOS) | Always — fast JSONL queries |
| **Phoenix (Arize)** | `pip install arize-phoenix && python -m phoenix.server.main` | UI for 10+ sessions |
| **Jaeger all-in-one** | `docker run --rm -p 16686:16686 jaegertracing/all-in-one` | Visualize the span tree |
| **W&B Weave** | `pip install weave` | Tracing + response quality scoring |
| **promptfoo** | `npx promptfoo eval` | Prompt regressions between versions |

Recommended start: JSONL + jq only → add Phoenix after collecting 10+ traces.

---

## 5. Agent prompt versioning policy

Agent prompts are code. They must be versioned, reviewed, and tested like code.

### 5.1 Agent changelog

All changes to `.agent.md` files must be documented in `.github/AGENTS_CHANGELOG.md`:

```markdown
# AGENTS_CHANGELOG

| Date | Agent | Type | Description | Author |
|---|---|---|---|---|
| 2026-02-23 | backend-critic | behavior | Add BLOCKER for missing race detector | architect |
| 2026-02-10 | orchestrator | model | gpt-4o → claude-sonnet-4.6 | human |
```

Change types:

| Type | When to use |
|---|---|
| `behavior` | System prompt/rubric/rule changed — agent behavior changes |
| `model` | Agent model changed |
| `tools` | A tool was added/removed (read_file, run_in_terminal, etc.) |
| `fix` | Typos/clarifications without behavior change |

### 5.2 Golden tests after a Critic change

After any change to a critic’s system prompt or rubric, you must run golden tests.

```
.agents/evals/
├── backend-critic-golden.jsonl      ← {input, expected_verdict, expected_severity}
├── frontend-critic-golden.jsonl
├── devops-critic-golden.jsonl
└── ...

Minimum set: 3 golden tests per agent:
   1. APPROVE scenario          — correct output with no BLOCKERs
   2. REQUEST_CHANGES scenario  — output with one clear BLOCKER
   3. REJECT scenario           — critical constitutional violation

Run: npx promptfoo eval
```

Example lines for `backend-critic-golden.jsonl`:

```jsonl
{"id":"bc-001","input":{"task":"Add POST /hosts endpoint","result_file":"handlers/host.go","result_summary":"Handler added, input validated, unit test written, godoc present"},"expected_verdict":"APPROVE","expected_severity":"none","description":"APPROVE: correct implementation — no BLOCKERs"}
{"id":"bc-002","input":{"task":"Add POST /hosts endpoint","result_file":"handlers/host.go","result_summary":"Handler added but no input validation on body fields"},"expected_verdict":"REQUEST_CHANGES","expected_severity":"BLOCKER","description":"BLOCKER: unvalidated external input (OWASP A03 / Backend Critic rule)"}
{"id":"bc-003","input":{"task":"Add POST /hosts endpoint","result_file":"handlers/host.go","result_summary":"Handler writes directly to devops-managed IaC config — outside backend zone"},"expected_verdict":"REJECT","expected_severity":"BLOCKER","description":"REJECT: executor wrote files outside its responsibility zone (Constitution principle 2)"}
```

Orchestrator golden tests (`orchestrator-golden.jsonl`) validate fast-track selection and decomposition correctness:

```jsonl
{"id":"orch-001","input":{"task":"Fix typo in README.md"},"expected_fast_track":"docs-only","expected_agents":[],"description":"Docs-only: no executors needed"}
{"id":"orch-002","input":{"task":"Update feature spec for login flow"},"expected_fast_track":"docs+feature","expected_agents":["architect-critic"],"description":"Docs+feature: architect-critic required (spec changed)"}
{"id":"orch-003","input":{"task":"Add POST /users endpoint with JWT auth"},"expected_fast_track":"feature","expected_agents":["architect","backend-dev","security-critic"],"description":"Feature: full pipeline; security-critic required for new auth endpoint"}
```

`result_summary` is a short description of what the executor produced; promptfoo uses it as `{{result_summary}}` in the prompt template.

Minimal `promptfooconfig.yaml` (starting point; adapt to project stack):

```yaml
# .agents/evals/promptfooconfig.yaml
prompts:
  - file://../../backend-critic.agent.md   # critic system prompt (in <project>-AgentConfig root)

providers:
  - id: openai:gpt-4o
    config:
      temperature: 0

tests:
  - file://backend-critic-golden.jsonl

defaultTest:
  vars:
    task: "{{task}}"
    result_summary: "{{result_summary}}"
  assert:
    - type: javascript
      value: output.includes(vars.expected_verdict)
```

Create one config per critic: change the `.agent.md` path and the `*-golden.jsonl` file.
> Full format — promptfoo.dev documentation: [promptfoo.dev](https://promptfoo.dev/docs/configuration/guide).

### 5.3 Agent change procedure

```
1. Create a branch: feature/<task-id>-update-<agent-name>-prompt
2. Edit the .agent.md
3. Run golden tests: npx promptfoo eval
4. Record the change in AGENTS_CHANGELOG.md
5. Open PR → review like normal code
6. After merge: verify the first 2–3 real tasks with this agent
```

---

## 6. Adoption roadmap

Universal roadmap for any new project. Project file extends it with stack-specific tasks.

### 6.pre Before you start: capture project parameters

Before running the roadmap, answer the questions below. Answers go into PROJECT.md and are used by the Implementation Agent (§6.agent) while creating files.

Project:
- Project name and short description (what it does, target users)
- Components (repos): how many repos and what types (backend, frontend, infra, etc.)
- Current baseline (existing project / greenfield / legacy+rescue)

Implementation agent must record the current spec version in PROJECT.md §pre:
`MULTI_AGENT_SPEC version: vX.Y.Z`.

Tech stack:
- Languages and frameworks (backend / frontend / mobile)
- Database and ORM/query library
- IaC tool (Terraform / Helm / Pulumi / other)
- CI/CD platform (GitHub Actions / Azure Pipelines / GitLab CI)
- Source control (GitHub / Azure DevOps / GitLab)

AI and models:
- Available AI providers (Azure OpenAI / Anthropic API / GitHub Copilot / other)
- Budget constraints for LLM calls
- Which agent roles are needed (all base / subset / additional) (see PROJECT.md §2.1)

Testing:
- Existing tests (unit / integration / E2E) and frameworks
- Expected thresholds (unit % / mutation %)
- Property-based / fuzz tool (go-fuzz / hypothesis / fast-check / other)

Performance and reliability:
- Target SLAs: RPS, p99 latency, allowed error rate
   (used by Phase 2.5 load tests and QA Critic checks — without these, load tests cannot define pass criteria)

Security and secrets:
- Secret storage (Vault / Key Vault / AWS Secrets Manager / .env + gitignore / other)
- SBOM or SLSA provenance requirements (regulated environment)

Observability:
- Where OTEL spans go (Jaeger endpoint / Phoenix URL / none yet — JSONL only)
- Existing tracing backend in the project

Team:
- Who interacts with AI agents (devs / PM / one person)
- Existing ADRs/architecture docs to consider
- Existing `.feature` specifications

---

### 6.agent Implementation Agent prompt

Use this prompt as the system instruction for the agent that will implement this spec in a project.

```
You — Implementation Agent. Your task is to set up the multi-agent development
system for a specific project, following MULTI_AGENT_SPEC.md and the answers
unlocked in PROJECT.md §pre.

Rules:
- Work through Roadmap phases §6.0–6.8 sequentially.
- Before each phase: read the corresponding spec section.
- Create files using the templates in the spec (exact section referenced in each phase).
- At each phase: check off items in the checklist. Do not proceed to the next
   phase until all checkboxes are done or explicitly deferred with a reason.
- Ask NEEDS_HUMAN if a parameter requires a team decision you cannot infer
   from PROJECT.md answers.
- Language: create all file content in English; communicate with the user in Russian.
- After each phase: summarise what was created and list any deferred items.

Context files to read first (in this order):
   1. MULTI_AGENT_SPEC.md (full specification)
   2. PROJECT.md (project parameters — must already exist with §pre filled in)

Start: say which phase you are beginning and ask for confirmation.
```

---

### 6.agent.2 Spec upgrade agent prompt

Use this when MULTI_AGENT_SPEC.md was updated and you need to sync an already configured project.

Prerequisite: PROJECT.md records the spec version used to set up the project (header field `Spec: MULTI_AGENT_SPEC vX.Y.Z`; see §0.8.1).

```
You — Spec Upgrade Agent. MULTI_AGENT_SPEC.md has been updated.
Your task is to bring the project's agent configuration up to date with the new version.

Input:
   - MULTI_AGENT_SPEC.md new version (current file)
   - PROJECT.md (header field: Spec: MULTI_AGENT_SPEC vX.Y.Z — the version the project was set up with)

Step 1 — Identify version delta.
   Read the new spec version from MULTI_AGENT_SPEC.md header.
   Read the project's current spec version from PROJECT.md.
   State: "Updating from vOLD to vNEW".
   If versions are equal — report "No update needed" and stop.

Step 2 — Audit each major section. Compare new spec with project files:
   §0.3  AGENTS.md global + component — new required fields?
   §0.8  PROJECT.md template — new required sections?
   §0.9  copilot-instructions.md — new required sections?
   §1.2  Model tiers — models removed or reclassified? Check PROJECT.md §2.2 for affected agents.
   §1.3  Pipeline — new phases, gates or protocols?
   §3.x  Critic rubrics — new BLOCKER/WARNING triggers? Update .agent.md critic prompts.
   §5    Golden tests — new required test cases?
   §6    Roadmap — new phases or checklist items?

Step 3 — Classify each delta:
   BREAKING — project cannot function correctly without this update
      (e.g. verdict type renamed, gate logic changed, new mandatory TASK_CONTEXT field)
   ADDITIVE — project works without it but quality improves
      (e.g. new WARNING trigger, new recommended tool)

Step 4 — Apply changes (BREAKING first, then ADDITIVE):
   - Update .agent.md files that reference changed rubrics or pipeline logic
   - Update PROJECT.md sections that gained new required fields (merge — do NOT overwrite
      project-specific values: §pre answers, custom rubrics, model choices)
   - Update copilot-instructions.md if §0.9 changed
   - Leave explicitly project-customised sections untouched unless BREAKING

Step 5 — After any .agent.md change: run golden tests (§5.3 procedure).
   npx promptfoo eval
   If tests pass → record in AGENTS_CHANGELOG.md:
      type: spec-upgrade | description: Sync to MULTI_AGENT_SPEC vNEW

Step 6 — Update PROJECT.md header:
   Spec: MULTI_AGENT_SPEC vNEW

Rules:
   - NEEDS_HUMAN if a BREAKING change requires a team decision
      (e.g. model removed from an available tier, new mandatory gate requiring CI reconfiguration)
   - Additive changes that require significant effort may be deferred:
      record as TODO in PROJECT.md §6 Roadmap with spec version reference
   - Language: all file content in English; communicate with the user in Russian
   - After completing: summarise what was changed, what was deferred, what requires human decision
```

---

### 6.0 Phase 0 — AgentConfig repo

> **Legacy / rescue:** if repos or CI already exist, before Phase 0:
> - Audit existing AGENTS.md, CI configs, ADRs — do not overwrite; merge.
> - Record current metrics (coverage, DORA) in PROJECT.md §pre as a baseline.
> - Mark `baseline: legacy+rescue` in PROJECT.md §pre — implementation agent will use merge mode.

Checklist:

```
- [ ] Create <project>-AgentConfig repo (or use an existing one)
- [ ] Create .vscode/<project>.code-workspace (all project repos)
- [ ] Create .gitignore (.agents/session/)
- [ ] Open the workspace and confirm all repos are visible as folders
- [ ] Create README.md describing:
      why this repo exists, how to run agents, links to MULTI_AGENT_SPEC.md
      and PROJECT.md, and an Observability AI Workflow (§4) section:
        – where traces are stored (.agents/traces/)
        – JSONL format (§4.5)
        – visualization options (§4.7: arize-phoenix / jaeger)
        – key metrics (§4.2, §4.3 DORA)
```

### 6.1 Phase 1 — Context

```
- [ ] <project>-AgentConfig/AGENTS.md — global (template §0.3)
- [ ] AGENTS.md in each component repo
- [ ] llms.txt in each component repo (template §0.4)
- [ ] .github/copilot-instructions.md — system instructions
- [ ] .github/pull_request_template.md (template §0.6)
- [ ] Configure branch protection for `main` and `develop` in all repos (§0.6.2)
      Required status checks: Gate 1 CI jobs; Minimum 1 reviewer; No direct push
```

### 6.2 Phase 2 — Agent skills

```
- [ ] SKILL.md for each component: backend, frontend, devops
- [ ] references/ with technology conventions and examples
- [ ] In backend SKILL.md: a "Property-Based / Fuzz Testing" section — run commands
      for the chosen tool from PROJECT.md §pre (go-fuzz / govulncheck / hypothesis / fast-check / other)
      Without this, the first parser/deserializer will immediately trigger a Backend Critic WARNING (§3.4)
- [ ] Verify: the agent loads SKILL.md at the beginning of each task?
```

### 6.3 Phase 3 — Agents

```
- [ ] <project>-orchestrator.agent.md
- [ ] Each (executor + critic) pair: architect, backend, frontend, qa, devops, security, documentation
- [ ] Verify models using the power/cost matrix (PROJECT.md §2)
- [ ] .pre-commit-config.yaml in each component repo
      (fmt, lint, validate — commands from SKILL.md §Build & Test Commands)
      Without this, DoD "Pre-commit hooks passed" (§3.11) cannot be satisfied
- [ ] Run: pre-commit install — in each component repo after creating .pre-commit-config.yaml
      (without it, hooks are not registered in git and will never run)
```

**Minimal `.pre-commit-config.yaml` (Go/TypeScript — adapt to your stack using SKILL.md):**

```yaml
# .pre-commit-config.yaml  (put in the root of each component repo)
# Install: pip install pre-commit && pre-commit install
repos:
  # ── universal ─────────────────────────────────────────────────────────────
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: detect-private-key        # ← DevOps Critic BLOCKER: secrets in code
      - id: check-added-large-files

  # ── Go (remove if not Go) ─────────────────────────────────────────────────
  - repo: https://github.com/dnephin/pre-commit-golang
    rev: v0.5.1
    hooks:
      - id: go-fmt
      - id: go-vet
      - id: golangci-lint            # requires golangci-lint in PATH

  # ── TypeScript / Node (remove if not TS) ─────────────────────────────────
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v9.0.0
    hooks:
      - id: eslint
        additional_dependencies: ['eslint@9', 'typescript-eslint']
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0
    hooks:
      - id: prettier
```

> Hook list must be derived from commands `## Build & Test Commands` in the component’s SKILL.md.
> Minimum for any language: formatter + linter + secret scanning (`detect-private-key`).
> Hook registry: [pre-commit.com/hooks](https://pre-commit.com/hooks.html).

- [ ] Run the first real task through the orchestrator

### 6.4 Phase 4 — MCP servers

```
- [ ] .vscode/mcp.json
- [ ] SCM MCP (GitHub / Azure DevOps / GitLab)
- [ ] Container runtime MCP (docker)
- [ ] IaC tool MCP (terraform / ansible / etc.)
- [ ] Validate: agents use MCP tools during tasks
```

**Minimal `.vscode/mcp.json`:**

```json
{
  "servers": {
    "github": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${env:GITHUB_TOKEN}"
      }
    },
    "docker": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-docker"]
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem",
               "${workspaceFolder}"]
    }
  }
}
```

> MCP server registry: [modelcontextprotocol.io/servers](https://modelcontextprotocol.io/servers).
> Pass secrets only via `${env:VAR}` — do not hard-code in the file (DevOps Critic BLOCKER).
> Project-specific server list goes into PROJECT.md §5.

### 6.5 Phase 5 — ADR and memory

```
- [ ] First 5 ADRs for key architectural decisions
- [ ] .agents/session/ directory + in .gitignore
- [ ] domain/ directory: glossary.md, bounded-contexts.md, domain-events.md
- [ ] domain/specs/*.feature for core entities (minimum 3)
- [ ] Test workflow: orchestrator → executor → critic → APPROVE on a real task
```

### 6.6 Phase 6 — Observability

```
- [ ] .agents/traces/ directory (committed!)
- [ ] Orchestrator writes a JSONL trace for each session (validate §4 format)
- [ ] After 10+ sessions: use arize-phoenix or jaeger for visualization
```

### 6.7 Phase 7 — Evals

```
- [ ] .agents/evals/ directory
- [ ] 3 golden tests per critic in JSONL (approve / request_changes / reject)
- [ ] After any .agent.md change → run evals: npx promptfoo eval
- [ ] Maintain AGENTS_CHANGELOG.md after each prompt change
```

### 6.8 Phase 8 — Iteration

```
- [ ] Calibrate rubrics based on real sessions
- [ ] Expand SKILL.md as new conventions appear
- [ ] If needs_human_rate > 20% → simplify tasks or rubrics
- [ ] If approve_on_first < 30% → upgrade executor model or refine SKILL.md
- [ ] Quarterly: review AGENTS_CHANGELOG.md and remove obsolete rules
```

---

### 6.9 End-to-end example: full cycle for a minimal feature

> Task: "Add field `description` to Host entity in the backend."

**Step 0 — Orchestrator reads ADRs and chooses fast-track**

```
1. Reads .github/decisions/ — no conflicts
2. Type: feature/* → full pipeline
3. Creates .agents/traces/20260223-add-host-desc.jsonl
4. Writes TASK_CONTEXT.md decomposition:
   #1 architect: .feature + ADR (if schema change)
   #2 backend-dev: model + migration + tests
```

**Step 1 — architect writes Gherkin scenario**

```gherkin
# domain/specs/host.feature
Scenario: Host has description
  Given a host exists with id "host-1"
  When I GET /hosts/host-1
  Then the response body contains field "description"
  And "description" is a string or null
```

architect-critic: `APPROVE` — scenario is unambiguous and does not violate ADRs.

**Step 2 — backend-dev implements (iteration 1)**

```
- models/host.go: add Description *string
- migration: ALTER TABLE hosts ADD COLUMN description TEXT
- test: TestGetHost_Description
```

backend-critic verdict (iter 1): `REQUEST_CHANGES`

```
BLOCKER: handlers/host.go:78 — Description is not included in GET /hosts/:id response
WARNING:  models/host.go:34 — missing godoc for the field
```

**Step 3 — backend-dev implements (iteration 2)**

```
- handlers/host.go: add Description to JSON response
- models/host.go: add godoc
```

backend-critic verdict (iter 2): `APPROVE` — BLOCKERs closed.

**Step 4 — CI Gate 1 (auto) → Gate 2 (critic) → Gate 3 (human) → merge**

```
Gate 1: tests green, lint pass
Gate 2: backend-critic reviewed; no open BLOCKERs
Gate 3: PM verifies description appears in API response — APPROVED
Merge → main + tag v1.4.7
```

**Session trace** (format §4.5: separate spans for executor and critic, verdict — only in critique spans):

```jsonl
{"ts":"2026-02-23T14:32:00Z","trace_id":"20260223-add-host-desc","span_id":"s01","parent_span_id":null,"agent":"orchestrator","operation":"plan","task":"add-host-description","fast_track":"feature","input_tokens":320,"output_tokens":75,"duration_ms":2800}
{"ts":"2026-02-23T14:32:05Z","trace_id":"20260223-add-host-desc","span_id":"s02","parent_span_id":"s01","agent":"architect","operation":"execute","subtask":1,"iteration":1,"input_tokens":1100,"output_tokens":280,"duration_ms":9200}
{"ts":"2026-02-23T14:32:20Z","trace_id":"20260223-add-host-desc","span_id":"s03","parent_span_id":"s01","agent":"architect-critic","operation":"critique","subtask":1,"iteration":1,"verdict":"APPROVE","blockers":0,"warnings":0,"input_tokens":700,"output_tokens":90,"duration_ms":5100}
{"ts":"2026-02-23T14:32:28Z","trace_id":"20260223-add-host-desc","span_id":"s04","parent_span_id":"s01","agent":"backend-dev","operation":"execute","subtask":2,"iteration":1,"input_tokens":1840,"output_tokens":620,"duration_ms":18400}
{"ts":"2026-02-23T14:33:10Z","trace_id":"20260223-add-host-desc","span_id":"s05","parent_span_id":"s01","agent":"backend-critic","operation":"critique","subtask":2,"iteration":1,"verdict":"REQUEST_CHANGES","blockers":1,"warnings":1,"input_tokens":980,"output_tokens":310,"duration_ms":9100}
{"ts":"2026-02-23T14:33:15Z","trace_id":"20260223-add-host-desc","span_id":"s06","parent_span_id":"s01","agent":"backend-dev","operation":"execute","subtask":2,"iteration":2,"input_tokens":2100,"output_tokens":540,"duration_ms":16200}
{"ts":"2026-02-23T14:34:05Z","trace_id":"20260223-add-host-desc","span_id":"s07","parent_span_id":"s01","agent":"backend-critic","operation":"critique","subtask":2,"iteration":2,"verdict":"APPROVE","blockers":0,"warnings":1,"input_tokens":900,"output_tokens":180,"duration_ms":8400}
{"ts":"2026-02-23T14:34:10Z","trace_id":"20260223-add-host-desc","span_id":"s08","parent_span_id":"s01","agent":"orchestrator","operation":"complete","task":"add-host-description","total_iterations":2,"input_tokens":7940,"output_tokens":2095,"duration_ms":127600}
```

---

## G. Glossary

| Term | Definition |
|---|---|
| **APPROVE** | Critic verdict: no BLOCKERs; WARNING allowed |
| **REQUEST_CHANGES** | Critic verdict: there is a BLOCKER; executor fixes and repeats |
| **REJECT** | Critic verdict: fundamental constitutional violation; not patch-fixable |
| **NEEDS_HUMAN** | Reached max_iterations=3 or human input is required |
| **BLOCKER** | Severity that blocks moving to the next phase |
| **WARNING** | Severity that can still allow APPROVE with explicit ACKNOWLEDGED |
| **SUGGESTION** | Severity that does not block; optional |
| **ACKNOWLEDGED** | A warning is consciously deferred in the PR thread; unblocks APPROVE |
| **DEFERRED** | Fix is postponed to a future sprint |
| **ESCALATED** | Blocker escalated to a higher-level human without waiting for resolution |
| **TASK_CONTEXT** | File `.agents/session/TASK_CONTEXT.md`; short-term session memory |
| **Fast-Track** | Shortened pipeline for hotfix / docs-only / infra |
| **Critique Report** | Critic’s structured response (verdict + findings) |
| **Previous Attempts** | TASK_CONTEXT section with REQUEST_CHANGES history for Reflexion |
| **DoR** | Definition of Ready: criteria before starting the work |
| **DoD** | Definition of Done: completion criteria |
| **executor** | Agent that produces work: code, tests, documentation |
| **critic** | Agent that reviews executor output against the rubric |
| **orchestrator** | Agent that decomposes tasks, assigns roles, and controls TASK_CONTEXT |
| **Tier (T1/T2/T3)** | Model level: T1=reasoning-heavy, T2=strong general, T3=efficient |
| **golden tests** | Fixed tests {input, expected_verdict} to detect prompt regressions |
| **trace_id** | Unique session ID `YYYYMMDD-task-slug`; the key in JSONL traces |
