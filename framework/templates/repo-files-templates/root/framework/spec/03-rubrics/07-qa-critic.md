# 3.7 QA Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

> QA critic checks test scripts and scenario coverage quality — not production code.
> Project file extends it with concrete tooling (Playwright, k6, pytest, etc.).

```text
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
