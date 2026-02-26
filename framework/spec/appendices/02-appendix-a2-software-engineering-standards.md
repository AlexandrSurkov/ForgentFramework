# Appendix A2 — Software Engineering Standards

> Part of [Multi-Agent Development Specification](../../00-multi-agent-development-spec.md)
> See also: [Appendix A1 — AI & LLM Standards](01-appendix-a1-ai-and-llm-standards.md)

Classical software engineering standards applied to agent-driven development pipelines.

---

## Table of Contents

- [A2.1 Engineering standards and conventions](#a21-engineering-standards-and-conventions)
- [A2.2 Security standards](#a22-security-standards)
- [A2.3 Documentation standards](#a23-documentation-standards)
- [A2.4 Domain knowledge standards](#a24-domain-knowledge-standards)
- [A2.5 Process, research, and observability standards](#a25-process-research-and-observability-standards)
- [A2.6 Principles derived from SW standards](#a26-principles-derived-from-sw-standards)

---

## A2.1 Engineering standards and conventions

| Standard | Source | Where it is used |
|---|---|---|
| **Conventional Commits** | [conventionalcommits.org](https://www.conventionalcommits.org) | Commit message format: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`. Basis for SemVer auto-releases. Mandatory for agents. |
| **Semantic Versioning** | [semver.org](https://semver.org) | MAJOR.MINOR.PATCH versioning. Agents must account for breaking changes. |
| **GitFlow** | Vincent Driessen, 2010 | main → develop → feature/id → release/X.Y.Z → hotfix/. Agents work only in feature/*. |
| **12-Factor App** | [12factor.net](https://12factor.net) | III: Config via env. XI: Logs to stdout. IX: Fast startup/shutdown. Critical for portability across environments. |
| **Keep a Changelog** | [keepachangelog.com](https://keepachangelog.com) | Added / Changed / Deprecated / Removed / Fixed / Security. |
| **Pre-commit hooks** | [pre-commit.com](https://pre-commit.com) | Mandatory gates before commits: fmt, lint, validate. |
| **OpenAPI 3.x** | [spec.openapis.org](https://spec.openapis.org), OpenAPI Initiative | REST API contract standard. Provides the schema that makes Contract Testing (CDC) concrete and machine-verifiable. |
| **TDD** | Kent Beck, 2002 | Red→Green→Refactor. Executor follows it in Pipeline Phases 1–2. |
| **ATDD** | Ward Cunningham, [Cucumber](https://cucumber.io) | BDD scenarios are acceptance criteria. Executor does not finish until covered. |
| **Quality Gates** | Watts Humphrey, CMMI | Explicit gates between phases: no phase transition without APPROVE. |
| **Shift-Left Testing** | Larry Smith, 2001 | Tests are written before code or in parallel. |
| **Shift-Right / Smoke Testing** | Cindy Sridharan, 2017 | Verification on a real deployed system (Phase 2.5). |
| **Contract Testing (CDC)** | [Pact.io](https://pact.io), 2013 | Consumer defines expected API contract; provider verifies it. |
| **Mutation Testing** | R. Lipton, 1971 | Mutates code logic to ensure tests catch it. score ≥70% WARNING, <50% BLOCKER. |
| **Property-Based / Fuzz Testing** | QuickCheck (Hughes, 1999) | Generative data for validation and parsing. |
| **Load Testing** | [k6.io](https://k6.io), Grafana Labs | Load tests: SLA, RPS, p99 latency. |
| **IEEE 829 / ISO/IEC/IEEE 29119** | IEEE, 2008 (superseded by ISO/IEC/IEEE 29119, 2013–2021) | Test documentation standard: Test Case Specification, Test Procedure Specification. Basis for manual test plan format (§1.4). |
| **Session-Based Test Management (SBTM)** | James Bach, Jonathan Bach, 2000 | Structured exploratory testing: charters, time-boxed sessions, debrief. Used for edge cases in §1.4. |
| **C4 Model** | [c4model.com](https://c4model.com), Simon Brown | 4 architecture levels: System Context, Containers, Components, Code. |

## A2.2 Security standards

| Standard | Source | Where it is used |
|---|---|---|
| **OWASP Top 10** | [owasp.org](https://owasp.org/www-project-top-ten/) | Rubric for security critic. A01–A10. |
| **OWASP ASVS** | [owasp.org/ASVS](https://owasp.org/www-project-application-security-verification-standard/), v4.0 | Application Security Verification Standard: structured L1/L2/L3 checklist for Security Critic. Complements OWASP Top 10 (what to check) with concrete verification requirements (how to verify). |
| **STRIDE** | Microsoft, Shostack | Threat modeling methodology: Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege. |
| **SLSA** | [slsa.dev](https://slsa.dev) (OpenSSF / Linux Foundation, v1.2) | Supply-chain Levels for Software Artifacts: build provenance, isolated build environments. Protects supply chain from compromise and artifact tampering. |
| **SBOM** | SPDX / CycloneDX (CISA, NIST) | Software Bill of Materials — machine-readable manifest of image dependencies. Required in regulated environments (FedRAMP, ISO 27001). |

## A2.3 Documentation standards

| Standard | Source | Where it is used |
|---|---|---|
| **Diataxis** | [diataxis.fr](https://diataxis.fr) | Tutorial (learn), How-to (solve), Reference (lookup), Explanation (understand). |
| **Standard Readme** | [github.com/RichardLitt/standard-readme](https://github.com/RichardLitt/standard-readme) (RichardLitt, 2016) | Required README sections: Background, Install, Usage, API, Contributing, License. Basis for §0.7. |

## A2.4 Domain knowledge standards

| Standard | Source | Where it is used |
|---|---|---|
| **Domain-Driven Design (DDD)** | Eric Evans, 2003 | Ubiquitous Language, Bounded Contexts, Domain Events. Agents use terms from `domain/glossary.md`. |
| **BDD / Gherkin** | [Cucumber](https://cucumber.io/docs/gherkin/) | `Given/When/Then` scenarios are readiness criteria for executors. |

## A2.5 Process, research, and observability standards

| Standard | Source | Where it is used |
|---|---|---|
| **DORA** | [dora.dev](https://dora.dev), Google / DORA Research Program, 2019–2025 | 4 key DevOps metrics (§4); AI Capabilities Model 2025 — 7 practices to amplify AI impact (§4, §3 principle 8). |
| **SPACE Framework** | Forsgren et al., GitHub/Microsoft, 2021 | Satisfaction, Performance, Activity, Communication, Efficiency — developer productivity dimensions. Complements DORA for measuring AI-assisted development impact. |

## A2.6 Principles derived from SW standards

- **Conventional Commits are mandatory for agents** — commit type controls version bumps and changelog generation.
- **Quality gates between phases** — no phase transition without APPROVE; mirrors CMMI Quality Gates.
- **Tests before or in parallel with code** — Shift-Left principle applied to all executor phases.
- **Contracts are machine-verifiable** — OpenAPI + Pact CDC: executor does not close a feature without a passing contract test.
