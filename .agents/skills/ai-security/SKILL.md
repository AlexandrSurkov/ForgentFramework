---
name: ai-security
description: "AI security and governance checklists: OWASP LLM Top 10, OWASP Agentic AI Top 10, MITRE ATLAS tactics, NIST AI RMF, least-privilege tool access, EU AI Act risk tiers. Load when reviewing agent architecture for injection risk, tool access policy, trust boundaries, supply chain, or compliance."
---

# SKILL: AI Security & Governance

> Load this skill when the task concerns AI-specific security review, tool access policy,
> trust boundary design, supply chain risk, prompt injection surface, or regulatory compliance.

## When to Load This Skill

- Security review of a new agent or tool integration
- Reviewing tool lists in `.agent.md` or `mcp.json` for least-privilege
- Assessing trust boundaries between agents (orchestrator ↔ executor ↔ external tool)
- Any mention of prompt injection, model extraction, or supply chain risk
- Governance / compliance question (ISO 42001, EU AI Act, NIST AI RMF)

---

## OWASP LLM Top 10 — Priority Three (A1.3)

| ID | Risk | In this pipeline |
|---|---|---|
| **LLM01** | **Prompt Injection** — malicious content in tool output or user input overrides system instructions | Any agent that reads external content (files, issues, URLs) is exposed. Critic must flag if executor reads unvalidated external input. |
| **LLM06** | **Supply Chain** — compromised model, dependency, or third-party agent | Verify model source stays GitHub Copilot managed; every new MCP server = new supply chain surface. |
| **LLM09** | **Misinformation** — agent confidently produces wrong output | Critic isolation and golden tests (A1.5) are the primary mitigations. |

**Quick triage questions for any new agent:**
- Does it read content from outside the repo (URLs, APIs, user uploads)? → LLM01 surface present
- Does it call external MCP servers or third-party tools? → LLM06 review needed
- Does it produce outputs consumed by other agents without validation? → LLM09 chain risk

---

## OWASP Agentic AI Top 10 (2025 — A1.3)

These complement LLM Top 10 — LLM Top 10 covers _model_ vulnerabilities; Agentic Top 10 covers _agent system_ risks.

| Risk | Description | Mitigation in this pipeline |
|---|---|---|
| **Excessive Agency** | Agent has more tools/permissions than its task requires | Least-privilege tool list in `.agent.md`; see checklist below |
| **Trust Boundary Violation** | Agent trusts output from another agent without validation | Critic receives only final result, not raw executor output; orchestrator validates before routing |
| **Human-in-the-Loop Bypass** | Irreversible action taken without human confirmation | `NEEDS_HUMAN` escalation path; no destructive tools in agent tool lists |
| **Insecure Inter-Agent Trust** | Agents authenticate each other implicitly | VS Code Copilot agents don't share sessions; orchestrator is the only caller |
| **Cascading Hallucination** | Hallucination in one agent propagates through the pipeline | Critic reviews each result before the next subtask starts |

---

## Least-Privilege Tool Access Checklist (OWASP Agentic AI, A1.6)

For every agent in `.github/agents/*.agent.md`:

- [ ] Does the agent need to **create files**? If not → remove `createFiles`
- [ ] Does the agent need to **edit existing files**? If not → remove `editFiles`
- [ ] Does the agent need to **run terminal commands**? If not → remove `runTerminal`
- [ ] Does the agent need **web search**? If not → remove `webSearch`
- [ ] Is the tool list the minimal set for the agent's stated role?
- [ ] Any MCP server in `mcp.json` — is it used by this agent? If not, not declared in its scope.

**Roles → expected tool sets:**

| Agent | Expected tools |
|---|---|
| orchestrator | `readFile`, `editFiles` (for traces) |
| spec-editor | `readFile`, `editFiles`, `createFiles`, `fileSearch`, `textSearch` |
| docs-critic | `readFile`, `fileSearch`, `textSearch` (read-only) |
| process-critic | `readFile`, `fileSearch`, `textSearch` (read-only) |
| agent-architect | `readFile`, `editFiles`, `createFiles`, `fileSearch`, `textSearch` |

---

## MITRE ATLAS Key Tactics (A1.3)

| Tactic | Description | Pipeline relevance |
|---|---|---|
| **AML.T0051 — Prompt Injection** | Adversarial input in data manipulates model output | Any agent that reads file content written by parties outside the pipeline |
| **AML.T0040 — Model Extraction** | Repeated queries to reconstruct model weights or behavior | Low risk for VS Code Copilot agents; relevant if agents are exposed via API |
| **AML.T0043 — Craft Adversarial Data** | Poisoning training or fine-tune data | Relevant if golden tests (`.agents/evals/`) could be manipulated |
| **AML.T0048 — Backdoor ML Model** | Trojan in model responds to trigger input | Risk at supply chain layer (LLM06 overlap); mitigated by GitHub Copilot managed infrastructure |

---

## NIST AI RMF — 4-Function Checklist (A1.3)

| Function | Key questions for this pipeline |
|---|---|
| **GOVERN** | Are roles defined? (AGENTS.md) Are ADRs recorded? Is AGENTS_CHANGELOG maintained? |
| **MAP** | Are risks documented per agent? Is the trust boundary diagram current? |
| **MEASURE** | Are golden tests passing? Is the critic rubric calibrated? |
| **MANAGE** | Is `NEEDS_HUMAN` escalation path functional? Are irreversible actions gated? |

---

## AI Governance Quick Reference (A1.4)

| Standard | When relevant | Action |
|---|---|---|
| **Constitutional AI** | Designing critique rubrics | Use BLOCKER/WARNING/SUGGESTION severity (→ see agent-patterns SKILL) |
| **ISO/IEC 42001** | Enterprise/regulated deployment | AI Management System baseline; relevant for audit readiness |
| **EU AI Act** | EU-market deployment | Classify pipeline risk tier: Limited (chatbot) or High (decisions about persons) |
| **Model Cards** | Deploying or fine-tuning a model | Document capabilities, limitations, intended use |
| **Spec-Driven Development (SDD)** | Adding a new agent feature | Phase 0: spec approved before Phase 1: implementation |

---

## References

- [framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md — A1.3, A1.4](../../../framework/spec/appendices/01-appendix-a1-ai-and-llm-standards.md)
- OWASP: https://owasp.org/www-project-top-10-for-large-language-model-applications/
- OWASP Agentic AI: https://owasp.org/www-project-top-10-for-agentic-ai-applications/
- MITRE ATLAS: https://atlas.mitre.org
- NIST AI RMF: https://airc.nist.gov
