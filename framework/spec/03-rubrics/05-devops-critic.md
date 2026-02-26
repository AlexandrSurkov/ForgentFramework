# 3.5 DevOps Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

> Applies to any IaC tool and CI/CD platform.
> Project file extends it with stack-specific triggers (Terraform, Helm, GitHub Actions, Azure Pipelines, etc.).

```text
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
