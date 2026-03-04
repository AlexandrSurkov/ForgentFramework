# 3.9 Security Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

> Security critic checks OWASP Top 10, STRIDE, and SLSA.
> OWASP LLM Top 10 applies only if the project contains AI/LLM components.
> Project file extends this with stack-specific checks (web headers, cloud IAM, network policies, etc.).

```text
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
