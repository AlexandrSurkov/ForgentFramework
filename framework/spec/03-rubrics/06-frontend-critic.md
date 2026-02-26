# 3.6 Frontend Critic rubric

> Split out of [00-multi-agent-development-spec.md](../../00-multi-agent-development-spec.md) to keep the umbrella file small.

> Applies to any UI framework.
> Project file extends it with stack-specific triggers (React, Vue, Angular, etc.).

```text
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
