# 3.10 Documentation Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

```text
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
- [ ] Manual test plan ([01-architecture.md §1.4](../01-architecture.md#14-manual-test-plans)) for a new/changed user flow is missing or outdated
- [ ] New module/package without a Component README ([00-infrastructure.md §0.7](../00-infrastructure.md#07-readme-in-code))

SUGGESTION triggers:
- [ ] Missing cross-links between related documentation sections
- [ ] Outdated screenshots or command outputs
- [ ] Diataxis structure is violated (Tutorial mixed with Reference)
```
