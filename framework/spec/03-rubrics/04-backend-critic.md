# 3.4 Backend Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

> Applies to any server-side language and framework.
> Project file extends it with stack-specific triggers (Go, Java, Python, etc.).

```text
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
