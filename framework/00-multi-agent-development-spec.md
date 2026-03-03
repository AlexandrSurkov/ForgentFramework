# Multi-Agent Development Specification

> **Version:** 0.25.7 · **Updated:** 2026-03-03

> This is a universal specification: it defines principles, protocols, and critique rubrics **independent of technology**.
> Project-specific application (stack, models, prompts, technology-specific rubric triggers) lives in a separate file at the **AgentConfig repo root** (e.g., `PROJECT.md` next to `framework/`).

> This umbrella file is intentionally small. The full spec is split into modules under `framework/spec/`.


## Framework operations

Install / Upgrade / Remove procedures live in: **[spec/07-framework-operations.md](spec/07-framework-operations.md)**.

For the detailed, phase-by-phase setup workflow and the agent prompts (Implementation Agent / Spec Upgrade Agent), use: **[spec/06-adoption-roadmap.md](spec/06-adoption-roadmap.md)**.

---

## Table of Contents

- [A. Standards and References](spec/appendices/00-appendix-a-standards-and-references.md)
- [0. Agent infrastructure organization](spec/00-infrastructure.md)
- [1. Agent system architecture](spec/01-architecture.md)
- [2. Work Protocol: Sessions and Memory](spec/02-sessions-and-memory.md)
- [3. Critique Rubrics (Constitutional Checklists)](spec/03-rubrics/00-constitutional-principles.md)
- [4. Observability AI workflow](spec/04-observability.md)
- [5. Agent prompt versioning policy](spec/05-prompt-versioning.md)
- [6. Adoption roadmap](spec/06-adoption-roadmap.md)
- [7. Framework operations](spec/07-framework-operations.md)
- [G. Glossary](spec/06-adoption-roadmap.md#g-glossary)

---

## A. Standards and References

> Full content has been extracted for readability.
> See **[00-appendix-a-standards-and-references.md](spec/appendices/00-appendix-a-standards-and-references.md)** for all subsections (A1–A2).

### Quick index

**[A1 — AI & LLM Standards](spec/appendices/01-appendix-a1-ai-and-llm-standards.md)**

| Subsection | Topic |
|---|---|
| [A1.1](spec/appendices/01-appendix-a1-ai-and-llm-standards.md#a11-agent-file-structure-standards) | Agent file-structure standards (AGENTS.md, llms.txt, SKILL.md, .agent.md, MCP, mcp.json, ADR, OTel, A2A, .prompt.md) |
| [A1.2](spec/appendices/01-appendix-a1-ai-and-llm-standards.md#a12-academic-executorcritic-patterns) | Academic Executor/Critic patterns (CoT, ReAct, Reflexion, LLM-as-Judge, ToT, RAG, Multi-Agent Debate, MoA, SoT, SDD) |
| [A1.3](spec/appendices/01-appendix-a1-ai-and-llm-standards.md#a13-ai-security-standards) | AI security standards (OWASP LLM Top 10, OWASP Agentic AI Top 10, MITRE ATLAS, NIST AI RMF) |
| [A1.4](spec/appendices/01-appendix-a1-ai-and-llm-standards.md#a14-ai-governance-and-process-standards) | AI governance and process standards (Constitutional AI, ISO/IEC 42001, EU AI Act, Model Cards, AI BOM) |
| [A1.5](spec/appendices/01-appendix-a1-ai-and-llm-standards.md#a15-ai-evaluation-standards) | AI evaluation standards (promptfoo, HELM, G-Eval, AgentBench) |
| [A1.6](spec/appendices/01-appendix-a1-ai-and-llm-standards.md#a16-principles-derived-from-ai-standards) | Principles derived from AI standards |

**[A2 — Software Engineering Standards](spec/appendices/02-appendix-a2-software-engineering-standards.md)**

| Subsection | Topic |
|---|---|
| [A2.1](spec/appendices/02-appendix-a2-software-engineering-standards.md#a21-engineering-standards-and-conventions) | Engineering standards (Conventional Commits, TDD, ATDD, OpenAPI, C4, GitFlow…) |
| [A2.2](spec/appendices/02-appendix-a2-software-engineering-standards.md#a22-security-standards) | Security standards (OWASP Top 10, OWASP ASVS, STRIDE, SLSA, SBOM) |
| [A2.3](spec/appendices/02-appendix-a2-software-engineering-standards.md#a23-documentation-standards) | Documentation standards (Diataxis, Standard Readme) |
| [A2.4](spec/appendices/02-appendix-a2-software-engineering-standards.md#a24-domain-knowledge-standards) | Domain knowledge standards (DDD, BDD/Gherkin) |
| [A2.5](spec/appendices/02-appendix-a2-software-engineering-standards.md#a25-process-research-and-observability-standards) | Process and observability standards (DORA, SPACE) |
| [A2.6](spec/appendices/02-appendix-a2-software-engineering-standards.md#a26-principles-derived-from-sw-standards) | Principles derived from SW standards |

---

## Spec modules

These are the canonical locations for the full specification content:

- **§0 Infrastructure** → [spec/00-infrastructure.md](spec/00-infrastructure.md)
- **§1 Architecture** → [spec/01-architecture.md](spec/01-architecture.md)
- **§2 Sessions & memory** → [spec/02-sessions-and-memory.md](spec/02-sessions-and-memory.md)
- **§3 Rubrics** → [spec/03-rubrics/00-constitutional-principles.md](spec/03-rubrics/00-constitutional-principles.md)
  - Orchestrator rules → [spec/03-rubrics/01-orchestrator-rules.md](spec/03-rubrics/01-orchestrator-rules.md)
  - Executor rules → [spec/03-rubrics/02-executor-rules.md](spec/03-rubrics/02-executor-rules.md)
  - Critic rules + report format → [spec/03-rubrics/03-critic-rules-and-report-format.md](spec/03-rubrics/03-critic-rules-and-report-format.md)
  - Backend critic → [spec/03-rubrics/04-backend-critic.md](spec/03-rubrics/04-backend-critic.md)
  - DevOps critic → [spec/03-rubrics/05-devops-critic.md](spec/03-rubrics/05-devops-critic.md)
  - Frontend critic → [spec/03-rubrics/06-frontend-critic.md](spec/03-rubrics/06-frontend-critic.md)
  - QA critic → [spec/03-rubrics/07-qa-critic.md](spec/03-rubrics/07-qa-critic.md)
  - Architect critic → [spec/03-rubrics/08-architect-critic.md](spec/03-rubrics/08-architect-critic.md)
  - Security critic → [spec/03-rubrics/09-security-critic.md](spec/03-rubrics/09-security-critic.md)
  - Documentation critic → [spec/03-rubrics/10-documentation-critic.md](spec/03-rubrics/10-documentation-critic.md)
  - DoR/DoD + ADR format → [spec/03-rubrics/11-dor-dod-and-adr-format.md](spec/03-rubrics/11-dor-dod-and-adr-format.md)
- **§4 Observability** → [spec/04-observability.md](spec/04-observability.md)
- **§5 Prompt versioning** → [spec/05-prompt-versioning.md](spec/05-prompt-versioning.md)
- **§6 Roadmap + glossary** → [spec/06-adoption-roadmap.md](spec/06-adoption-roadmap.md)
- **§7 Framework operations** → [spec/07-framework-operations.md](spec/07-framework-operations.md)

