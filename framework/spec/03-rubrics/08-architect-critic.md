# 3.8 Architect Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

```text
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
