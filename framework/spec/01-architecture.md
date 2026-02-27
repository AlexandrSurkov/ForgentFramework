# 1. Agent system architecture

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

```text
User
       │
       ▼
[orchestrator]                  ← single entry point for any task
       │                             reads ADR + TASK_CONTEXT before every decision
       ├──► [architect]           ─┐
       ├──► [backend-dev]         ─┤
       ├──► [frontend-dev]        ─┤
       ├──► [qa-engineer]         ─┤  executor → critic → [iteration, max 3]
       ├──► [devops-engineer]     ─┤       ↑___________________________|
       ├──► [security]            ─┤  if iter=3 and VERDICT≠APPROVE → NEEDS_HUMAN
       └──► [documentation-writer]─┘
                     │
                     ▼
                 .agents/session/<trace_id>/TASK_CONTEXT.md   ← memory: plan + previous attempts (per session)
                     │
                     ▼
             .github/decisions/ADR-*.md        ← long-term memory
```

**Why each agent exists:**

| Agent | Pipeline phase | What it does |
|---|---|---|
| `architect` | 0, 4 | BDD specs, ADR, C4 Model, cross-service contracts |
| `backend-dev` | 1, 2, 3 | Code + unit/integration/contract tests next to code (TDD) |
| `frontend-dev` | 1, 2, 3 | UI components + Jest/RTL tests next to components |
| `qa-engineer` | 2.5, 3.5 | Deployed-system tests: smoke, E2E, load. Does not write business logic code. |
| `devops-engineer` | 2.5, 3.5 + CI | IaC, CI/CD, deploy to test envs for Phases 2.5 and 3.5; CI support across all phases |
| `security` | 5 | OWASP/STRIDE, image CVE scanning, threat modeling |
| `documentation-writer` | 0 (Component README), 6 | Phase 0: Component README (§0.7) with `architect`; Phase 6: API reference, How-to (Diataxis), updates to `.feature`, manual test plans |

> Extensibility: the agent set is the spec baseline.
> PROJECT.md §2 may add roles, remove unused roles, or rename them to match domain terminology.
> Changes must be recorded in `AGENTS_CHANGELOG.md`.

**Patterns:**
- Plan-and-Execute — orchestrator builds the full plan before execution
- ReAct — every executor: Reasoning → Acting → Observation
- Reflexion — executor reads critique from previous attempts before the next iteration
- Critic isolation — critic sees only the result, not chain-of-thought; escalate to human if iter=3 without APPROVE

---

## 1.1 Orchestrator agent assignment rules

Orchestrator selects agents using two signals: **change area** (what changes in code/infra) and **task type** (design, implementation, tests, docs).

### 1.1.1 Assignment matrix by area

| Change area | Primary agent | When to add `architect` |
|---|---|---|
| Server code, API, business logic, DB schema | `backend-dev` | New public API or new service |
| UI components, pages, hooks, styles | `frontend-dev` | New user-facing flow without `.feature` |
| Dockerfile, docker-compose, Helm, IaC | `devops-engineer` | — |
| CI/CD pipeline, deploy scripts | `devops-engineer` | — |
| Test scripts: smoke, E2E, load, benchmark | `qa-engineer` | — |
| Security audit, CVE, threat model, auth | `security` | — |
| README, `.feature`, How-to, API Reference | `documentation-writer` | If `.feature` changes |
| New service / cross-service contract / ADR | `architect` | Primary |

### 1.1.2 Mandatory `architect` first

Orchestrator must invoke `architect` **before** any other executor if at least one condition holds:

```text
- The task creates a new service or standalone module
- The task introduces or changes a public cross-service API
- The task crosses more than one bounded context boundary
- There are no `.feature` specifications for the task
- The task contradicts an active ADR or requires a new ADR
```

### 1.1.3 Mandatory `security` involvement

Run in parallel with the primary executor (or as a separate subtask) if:

```text
- AuthN/AuthZ is added or changed
- A new public endpoint is added that accepts external input
- The task processes PII or financial data
- A new external dependency is added with unknown CVE status
- Network/firewall/TLS configuration changes
```

### 1.1.4 Parallel execution

Independent parts of a task (no mutual dependencies) should be given to multiple executors **concurrently**.
Orchestrator marks them in `TASK_CONTEXT.md` (`Depends on: —`).

```text
Example: "Add filtering by status"
   Condition: API contract is fixed in `.feature`
   ├── backend-dev (Phase 1): endpoint + unit tests
   └── frontend-dev (Phase 1): filter UI component + unit tests
```

> Parallelism cap: no more than 4 executor agents concurrently for one task.
> Beyond that, orchestrator loses reliable control over `TASK_CONTEXT.md` and traces.
> If you have more than 4 independent parts — group them into prioritized batches.

### 1.1.5 Orchestrator anti-patterns

```text
✗ Assign backend-dev without `.feature` → run architect first
✗ Assign frontend-dev if API contract is not fixed yet
✗ Combine executor and critic in the same agent for the same task
✗ Run independent parts sequentially instead of in parallel
✗ Skip architect when changing a cross-service contract
```

---

## 1.2 Model selection policy

> Concrete model names are defined in the project file: availability depends on platform and budget.
> This spec defines task types and required characteristics; PROJECT.md maps them to specific models.

### 1.2.1 Task types and required characteristics

| Task type | Required characteristics | Preferred | Alternative |
|---|---|---|---|
| Orchestration / Planning | Deep reasoning, task decomposition, ADR + TASK_CONTEXT work. Strong instruction following. | Gemini 2.5 Pro · Claude Opus 4.6 | GPT-5.1 · Claude Opus 4.5 |
| Architecture / ADR | Contradiction analysis, domain modeling, threat modeling. Multi-step reasoning about consequences. | Gemini 2.5 Pro · Claude Opus 4.6 | GPT-5.1 · Claude Opus 4.5 |
| Code generation (executor) | Producing code, tool use, writing tests. High instruction-following precision. | Claude Sonnet 4.6 · GPT-5.3-Codex | GPT-4.1 · GPT-4o · Gemini 3 Pro · GPT-5.1-Codex |
| IaC / DevOps | Terraform/Helm/CI generation. Syntax accuracy is critical: IaC mistakes become production incidents. | Claude Sonnet 4.6 · GPT-5.2-Codex | GPT-4.1 · Gemini 3 Pro |
| Critique (critic agents) | Strict checklist adherence, structured output, catching violations in code. | Never below the executor tier in the same task | — |
| Security review | Broad OWASP/CVE knowledge, STRIDE/SLSA reasoning. | Claude Sonnet 4.6 · Gemini 2.5 Pro | GPT-5.1 |
| Documentation | README, How-to, test plans. Moderate complexity. | Claude Haiku 4.5 | GPT-5 mini · GPT-4o · GPT-4.1 · Gemini 3 Flash |

### 1.2.2 Critic/executor parity rule

```text
A critic must NEVER be weaker than the executor it reviews.
A weaker critic model systematically misses executor mistakes — sycophancy effect.
```

### 1.2.3 Model tier hierarchy

> Used to apply the parity rule: choose a critic from tier ≥ executor tier.
>
> 0x multiplier (GPT-4.1 · GPT-4o · GPT-5 mini · Raptor mini): included in GitHub Copilot subscription with no additional token billing. When quality is equal, prefer 0x.

| Tier | Models | Characteristics |
|---|---|---|
| T1 — Frontier | Gemini 2.5 Pro (1x) · GPT-5.1 (1x) · GPT-5.1-Codex-Max (1x) · Claude Opus 4.6 (3x) · Claude Opus 4.5 (3x) | Deep reasoning, complex planning, threat modeling |
| T2 — Balanced | Claude Sonnet 4.6 (1x) · Claude Sonnet 4.5 (1x) · Claude Sonnet 4 (1x) · GPT-5.3-Codex (1x) · GPT-5.2-Codex (1x) · GPT-5.1-Codex (1x) · GPT-5.2 (1x) · GPT-4.1 (0x) · GPT-4o (0x) · Gemini 3 Pro (1x) · Gemini 3.1 Pro (1x) · Grok Code Fast 1 (0.25x) | High-accuracy code gen / tool use at moderate cost |
| T2+ — Balanced (fast) | Claude Opus 4.6 fast mode (30x) | T1-like reasoning quality but ~30x cost; use only with hard time budget and short tasks |
| T3 — Efficient | Claude Haiku 4.5 (0.33x) · GPT-5 mini (0x) · Gemini 3 Flash (0.33x) · GPT-5.1-Codex-Mini (0.33x) · Raptor mini (0x) | Fast/economic; unambiguous tasks with clear I/O |

```text
Application rule:
   Executor T1 → Critic T1
   Executor T2 → Critic T2 or T1
   Executor T3 → Critic T3, T2, or T1 (minimum T3)
```

### 1.2.4 When a reasoning-heavy model is required

```text
Required (T1 — Gemini 2.5 Pro / GPT-5.1 / GPT-5.1-Codex-Max / Claude Opus 4.6 / Claude Opus 4.5):
   - Task decomposition with implicit dependencies
   - Creating/reviewing a new ADR: alternatives, trade-offs, consequences
   - Resolving NEEDS_HUMAN: identify the root disagreement between executor and critic
   - Threat modeling (STRIDE): systematic attack-vector analysis
   - Circular dependency or bounded context analysis

Not required (T2 is enough: Claude Sonnet 4.6 / GPT-5.3-Codex / GPT-4.1 / Gemini 3 Pro):
   - Typical endpoints, CRUD, simple tests
   - Familiar tasks with clear `.feature` and established ADR
   - README, How-to, test plans
   - Critic review for straightforward checklists
```

### 1.2.5 Using an efficient model instead of an expensive one

```text
Use an efficient model if ALL conditions hold:
   - Task is unambiguous: inputs/outputs are clearly defined
   - No multiple interdependent decisions
   - Agent is not decomposing the task (orchestrator already produced a clear plan)
   - Large output (code/docs) with moderate context

Prefer 0x models (no extra billing): GPT-4o, GPT-4.1, GPT-5 mini, Raptor mini.
When quality is equal — choose 0x over 0.33x or paid models.

> GPT-4o and GPT-4.1 are T2 (Balanced) in capability and 0x in cost.
> For the conditions above, their quality is sufficient for doc and unambiguous tasks.
> Critic tier must still be ≥ executor tier (parity rule §1.2.2).
```

### 1.2.6 Fallback when a model is unavailable

If the preferred model is unavailable (rate limit, quota, outage):

```text
1. Use the Alternative from the same row in §1.2.1
2. If Alternative is also unavailable — choose another model from the same tier (§1.2.3)
3. If tier is downgraded — record in TASK_CONTEXT.md:
    “Replacement used: <model> instead of <preferred> because: <reason>”
4. Never downgrade critic tier below executor tier (parity rule §1.2.2)
```

---

## 1.3 Development Pipeline — from spec to production

> Based on: ATDD (Cunningham), TDD (Kent Beck, 2002), Quality Gates (CMMI),
> Shift-Left Testing (L. Smith, 2001).
> Each phase is a Quality Gate: without critic APPROVE, you cannot move forward.

### 1.3.1 Three levels of work

| Level | Prepared by | Example input | Output |
|---|---|---|---|
| Specs (requirements) | User + architect | feature described in words | `.feature` + `glossary.md` |
| Feature | User formulates | `feature/<id>-desc` | `TASK_CONTEXT.md` |
| Subtask | Orchestrator during decomposition | a row from TASK_CONTEXT Decomposition | commit + one trace line |

Task statement template:

```markdown
## Task
What to do: [1–3 sentences]

## Scenarios (from .feature or inline)
- Scenario: ...

## Area
[ ] Backend / Frontend / DevOps / IaC

## Exceptions / constraints
if any: ...
```

> Multi-sprint rule: if a task takes > 5 days, orchestrator must split it into multiple sprint-sized tasks before running the pipeline.
> Each sprint becomes a separate `TASK_CONTEXT.md`. Indicators the task is too big: decomposition yields > 10 subtasks or total estimate > 5 days.
> Action: NEEDS_HUMAN — “Task is too large for one TASK_CONTEXT; propose a sprint breakdown.”

---

### 1.3.2 Who writes which tests and when

> Tests are written **before or alongside code** (TDD/ATDD) — not after.
> Each test type belongs to a specific agent and phase.

| Test type | Who writes | When written | Who runs / verifies |
|---|---|---|---|
| `.feature` scenarios (Gherkin) | `architect` (or user) | Phase 0 — before implementation | `architect-critic` checks completeness |
| Unit tests (from `.feature`) | `backend-dev` / `frontend-dev` | Phase 1a — before code (Red) | critic checks: all Given/When/Then covered |
| Edge cases + Property-Based/Fuzz | `backend-dev` / `frontend-dev` | Phase 2, Cycle 2 | critic checks: no uncovered edge cases |
| Integration tests | `backend-dev` | Phase 2, Cycle 3 | critic checks: real DB/HTTP, no stub bypass |
| Contract tests (CDC) | `backend-dev` (provider) + `frontend-dev` (consumer) | Phase 2, Cycle 4 | critic checks: pact file is valid |
| E2E tests | `qa-engineer` | Phase 2, Cycles 1–3 — written in parallel; executed in Phase 2.5 | `qa-critic` checks: real user flow |
| Load tests (k6 / locust) | `qa-engineer` | Phase 2, Cycle 3 — after Integration; executed in Phase 2.5 | `qa-critic` checks: SLA RPS/p99/error rate recorded |
| Benchmarks (function perf) | `backend-dev` | Phase 3, Cycle 2 — only when optimizing a specific algorithm/query | critic checks: benchmark improves vs baseline |
| Regression run | `backend-dev` / `frontend-dev` + `qa-engineer` | Phase 3.5 — run existing tests; do not write new ones | critic checks: mutation score did not degrade |

> Rule: if a test type is not written by the time it is needed, that is a BLOCKER for moving to the next phase.
> E2E and Load tests are written ahead of time (Phase 2) and committed; in Phase 2.5 they are only executed.

---

### 1.3.3 Development Pipeline (9 steps: phases 0, 1, 2, 2.5, 3, 3.5, 4, 5, 6)

> Parallel execution: `backend-dev` and `frontend-dev` may work in Phases 1–2 concurrently if their subtasks do not depend on each other.
> Orchestrator explicitly marks independence in `TASK_CONTEXT.md` (`Depends on: —`).
> Critics operate independently per branch; orchestrator waits for APPROVE from both before entering Phase 2.5.
>
> Handing off results when going back a phase:
> every time you go backwards, orchestrator creates a new “fix” subtask and must carry over concrete findings
> from the completed phase’s Critique Report:
>
> ```
> ## Previous Attempts
> Returned from Phase N after [architect-critic / security-critic / qa-critic]:
> - BLOCKER | <category> | <file>:<line> | <issue> | <recommendation>
> - ...
> What we already tried and it did not work: [if this is not the first return]
> ```
>
> Executor starts with specific locations and problems — not “fix something”, but “fix X in file Y:Z”.
> Without `## Previous Attempts`, executor does not know why it is here and will repeat the same mistake (sycophancy / anchoring).

```text
▼ PHASE 0 — Requirements (source of truth) — SDD: spec before code
┌─────────────────────────────────────────────────────────┐
│  User writes/updates domain/specs/*.feature              │
│  architect reviews: completeness, contradictions         │
│  architect-critic: APPROVE / REQUEST_CHANGES             │
│  max iter: 3 → if .feature not agreed → NEEDS_HUMAN      │
│    (requirements contradictory or incomplete —           │
│     user clarifies before Phase 1)                       │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE → specs are fixed →

▼ PHASE 1 — Development (TDD Red→Green loop)
┌─────────────────────────────────────────────────────────┐
│  1a. Executor writes tests from .feature (sets Red)      │
│  1b. Executor writes code (all tests Green)              │
│  Critic: are all Given/When/Then covered?                │
│  max iter: 3 per subtask                                 │
│  If tests not Green after iter=3 → NEEDS_HUMAN            │
│    (spec is contradictory or task statement needs edits) │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 2 — In-code tests (5 cycles)
┌─────────────────────────────────────────────────────────┐
│  Cycle 1: Unit — all .feature scenarios have coverage    │
│  Cycle 2: Edge cases — empty input, boundaries, 4xx/5xx  │
│           Property-Based/Fuzz — parsers, deserializers,  │
│           and external data formats                      │
│  Cycle 3: Integration — real DB/HTTP                     │
│  Cycle 4: Contract — Consumer-Driven Contract            │
│  Cycle 5: Mutation — score ≥70%                          │
│  If Cycle 1/2/3/4 fails (code issue) → return to Phase 1 │
│    (code-fix subtask, iter+1)                            │
│  Mutation < 50% after iter=3 → BLOCKER → NEEDS_HUMAN     │
│  Mutation 50–70% → WARNING: transition allowed;          │
│    executor adds coverage in the same PR                 │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 2.5 — Deployed-system tests (Shift-Right)
┌─────────────────────────────────────────────────────────┐
│  devops-engineer: deploy to target environments          │
│    (configs — see project file)                          │
│  ↓ deploy APPROVE → qa-engineer takes over               │
│  Smoke: GET /health — all 200?                           │
│  E2E: automated tests against a live stack               │
│  Load: SLA RPS / p99 latency / error rate                │
│  If smoke fails → NEEDS_HUMAN (to devops, not QA)         │
│  If E2E fails (code issue) → return to Phase 1           │
│  If Load misses SLA → return to Phase 3 (performance)    │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 3 — Optimization / Refactor (2 cycles)
┌─────────────────────────────────────────────────────────┐
│  Cycle 1: Refactor (readability, structure)              │
│    → no new tests; existing tests must stay GREEN        │
│  Cycle 2: Optimization (performance)                     │
│    → if optimizing a specific algorithm/query:           │
│      executor writes a benchmark with baseline + target  │
│      (example: BenchmarkBulkInsert — was 500ms, target   │
│       <100ms); without benchmark there is no proof       │
│      of improvement → critic: BLOCKER                    │
│    → if optimization is systemic (Load→Phase 2.5):       │
│      benchmark not required; Phase 2 Load test is the    │
│      metric; rerun in Phase 3.5                          │
│  Cycles 1 and 2: mutation score must not degrade          │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 3.5 — Regression after optimization
┌─────────────────────────────────────────────────────────┐
│  Cycle 1: Unit + Integration — nothing broken?           │
│    backend-dev + frontend-dev run in-code tests          │
│  devops-engineer: redeploy optimized code                │
│  Cycle 2: Smoke on deployed system (again)               │
│    qa-engineer: smoke + critical E2E                     │
│  If tests fail → return to Phase 3 (iter+1)              │
│  Mutation score did not degrade?                         │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 4 — Architecture (1 pass)
┌─────────────────────────────────────────────────────────┐
│  architect + critic: does code comply with ADR?          │
│  bounded contexts respected?                             │
│  C4 model up to date after changes?                      │
│  BLOCKER (ADR violated / bounded context / circular dep  │
│    / public API without contract):                       │
│    → return to Phase 1 (code fix, iter+1)                │
│    → after fix: rerun Phase 4                            │
│  WARNING (C4 not updated / .feature outdated):           │
│    → architect updates docs in Phase 4                   │
│    → rerun Phase 4 (no return to Phase 1)                │
│  iter=3 without APPROVE → NEEDS_HUMAN                    │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 5 — Security (1 pass)
┌─────────────────────────────────────────────────────────┐
│  security + critic: OWASP Top 10, STRIDE                 │
│  Container images have no Critical CVEs?                 │
│  No secrets leaked into code?                            │
│  BLOCKER in code (OWASP injection / auth / secret):      │
│    → return to Phase 1 (code fix, iter+1)                │
│    → after fix: rerun Phase 5                            │
│  BLOCKER in image/infra (Critical CVE):                  │
│    → devops-engineer updates image within Phase 5        │
│    → rerun Phase 5 (no return to Phase 1)                │
│  iter=3 without APPROVE → NEEDS_HUMAN                    │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE →

▼ PHASE 6 — Documentation (1 pass)
┌─────────────────────────────────────────────────────────┐
│  documentation-writer + critic:                          │
│  README, API reference, How-to (Diataxis)                │
│  .feature updated if API changed?                        │
└─────────────────────────────────────────────────────────┘
               ↓ APPROVE → merge feature → develop
```

### 1.3.4 Why these cycle counts

| Phase | Cycles | Rationale |
|---|---|---|
| Development | max 3 iter/subtask | AutoGen rule: after 3 → NEEDS_HUMAN |
| In-code tests | 5 | unit; edge cases; integration; contracts (CDC); mutation score |
| Deployed tests | 1 | smoke+E2E+load: system is alive under load |
| Optimization | 2 | Cycle 1: Refactor; Cycle 2: Performance |
| Regression | 2 | Cycle 1: unit+integration; Cycle 2: smoke again |
| Architecture | 1 | ADR compliance is binary |
| Security | 1 | OWASP/STRIDE is binary: BLOCKER found or not |
| Documentation | 1 | API reference updates are binary |

### 1.3.5 When the user intervenes

```text
Position A (normal):
   User states the task for the orchestrator once per sprint.
   Orchestrator runs the Pipeline autonomously.
   User receives the result after Phase 6.

Position B (NEEDS_HUMAN):
   Orchestrator is stuck at iter=3 without APPROVE.
   User receives NEEDS_HUMAN with a description of the disagreement.
   User decides and provides Human Input (see template below).
   Pipeline continues from the stuck point.

Position C (spec correction):
   During work, `.feature` is discovered to be incomplete.
   User updates `.feature`.
   Orchestrator reruns only the affected phases.
```

What happens after Human Input (Position B):

```text
User adds ## Human Input to TASK_CONTEXT.md (template → §2.3):

   ## Human Input — [date]
   ### Decision on the blocker: <concrete instruction>
   ### Permission: [x] Rephrase subtask and restart at iter=0

Orchestrator reads the entry and then:
   1. If “Rephrase” — resets iter to 0 and updates subtask description in TASK_CONTEXT.md.
   2. If “Iteration 4” — continues the same subtask with iter=4, routed to the same executor.
   3. If “WONT_FIX” — closes the subtask; records the reason in ADR or TASK_CONTEXT.md Decisions; pipeline continues without it.

After re-entry, one executor loop runs: executor → critic → (APPROVE | NEEDS_HUMAN again).
If NEEDS_HUMAN occurs a second time on the same subtask — ESCALATED (see §3.3).
```

> The full `## Human Input` template and orchestrator details are in §2.3.

---

### 1.3.6 Test Failure Protocol

> Applies to any test failure in Phases 1, 2, 2.5, 3.5.
> Executor must record in `TASK_CONTEXT.md`: what failed (test, file:line), root cause (hypothesis), what was changed in the current iteration.

#### 1.3.6.1 Tests are failing (RED)

| Phase | Situation | Action | After iter=3 |
|---|---|---|---|
| **Phase 1** | Tests are not Green (code does not compile or assertions fail) | Executor fixes code → critic → repeat | NEEDS_HUMAN: "tests do not match the spec — `.feature` may be contradictory" |
| **Phase 2, Cycles 1–4** | Unit / Edge / Integration / Contract failed | Executor fixes code → return to Phase 1 (subtask: code-fix, iter+1) | NEEDS_HUMAN after 3 attempts in Phase 1 |
| **Phase 2.5** | E2E failed (code issue, not env) | qa traces the failure → orchestrator returns to Phase 1 (code-fix) | NEEDS_HUMAN after iter=3 |
| **Phase 2.5** | Smoke failed (env / deploy issue) | NEEDS_HUMAN immediately to devops-engineer (not to qa) | — |
| **Phase 3.5** | Unit / Integration failed after refactor | Return to Phase 3 (iter+1) | NEEDS_HUMAN after iter=3 |
| **Phase 3.5** | Smoke failed after re-deploy | NEEDS_HUMAN to devops-engineer | — |

#### 1.3.6.2 Insufficient coverage

| Situation | Severity | Action | After iter=3 |
|---|---|---|---|
| Mutation score **< 50%** (Phase 2, Cycle 5) | BLOCKER | Executor adds tests → critic → repeat | NEEDS_HUMAN: "coverage is unreachable without refactoring code or extending the test plan" |
| Mutation score **50–70%** (Phase 2, Cycle 5) | WARNING | Transition to Phase 3 is allowed; executor **must** add coverage in the same PR before merge | If WARNING is not resolved before merge → ACKNOWLEDGED thread in PR |
| Mutation score **degraded** after refactor (Phase 3.5) | BLOCKER | Return to Phase 3 to restore coverage | NEEDS_HUMAN after iter=3 |
| Not all `.feature` scenarios have a Unit test (Phase 2, Cycle 1) | BLOCKER | Executor adds missing tests | NEEDS_HUMAN after iter=3 |

> **Goal of return:** executor must ensure that **all tests pass** (GREEN) before
> the orchestrator initiates transition to the next phase again. Return means not "take a look",
> but "fix until fully passing".
>
> **Recording rule:** see "Passing results on return" in the Pipeline preamble —
> each `## Previous Attempts` line is populated from the findings of the completed phase's `Critique Report`.
> This ensures the Reflexion cycle and prevents repeating the same mistakes.

#### 1.3.6.3 REJECT verdict

| Situation | Action |
|---|---|
| Critic issued `REJECT` (fundamental constitutional violation) | Orchestrator **immediately** stops iterations; retry is impossible without reconsidering the task |
| — | Records a span `operation: "escalate"` in the JSONL trace (§4.6.2) |
| — | Sets `TASK_CONTEXT.md` status to `NEEDS_HUMAN` with the critic's explanation |
| — | Task is returned to the human: reason for REJECT + what needs to change in the problem statement |

> **Difference from NEEDS_HUMAN due to iter=3:** REJECT does not depend on the number of iterations — it is a qualitative assessment,
> not an exhausted limit. The task is not resumed without explicit human approval.

---

#### 1.3.7 Alignment with Reflexion loop

The Pipeline does not replace the internal executor→critic loop (max 3 iter) — it is built **on top of** it.
Each phase consists of one or more subtasks, each going through a Reflexion cycle.

```text
[Pipeline]
  └─ Phase 1: Development
       └─ subtask: write tests       [executor → critic, max 3]
       └─ subtask: implement handlers [executor → critic, max 3]
  └─ Phase 2: Tests
       └─ subtask: cycle 1 unit      [executor → critic, max 3]
       └─ subtask: cycle 2 edge cases [executor → critic, max 3]
```

---

#### 1.3.8 Shortened Pipeline Paths (Fast-Track)

The full 9-phase pipeline is intended for **feature work** on `feature/*` branches.
For other types of changes — shortened paths:

<a id="fast-track-enum"></a>

**Canonical `fast_track` enum (used in `TASK_CONTEXT.md`)**

The orchestrator MUST set `fast_track` to exactly one of these string values:

| `fast_track` | Meaning (classification rule) |
|---|---|
| `feature` | Default: new behavior or non-trivial change; run the full 9-phase pipeline. |
| `lightweight-feature` | Small, atomic feature change on `feature/*` that meets all “Lightweight feature criterion” conditions below. |
| `hotfix` | Urgent bug fix in `main` with shortened verification. |
| `docs-only` | Documentation-only change that does **not** modify any `.feature` file. |
| `docs+feature` | Documentation-only change that modifies one or more `.feature` files (no code/IaC changes). |
| `infra` | IaC/config-only changes (no product logic changes). |
| `security-patch` | Dependency update due to CVE with no intentional logic change. |
| `agent-prompt-update` | Update to agent prompts / prompt procedures (see §5 procedure). |

| Change type | Branch | Active phases | Skip |
|---|---|---|---|
| **Feature** (default) (`fast_track: feature`) | `feature/*` | 0 → 1 → 2 → 2.5 → 3 → 3.5 → 4 → 5 → 6 | — |
| **Lightweight feature** (atomic change with no architectural impact) (`fast_track: lightweight-feature`) | `feature/*` | 1 → 2 (unit+edge) → 5 | 0, 2.5, 3, 3.5, 4, 6 |
| **Hotfix** (urgent bug in `main`) (`fast_track: hotfix`) | `hotfix/*` | 1 → 2 (unit+regression only) → CI Gate 1 → 5 | 0, 2.5, 3, 3.5, 4, 6 |
| **Docs-only** (`fast_track: docs-only`) | `docs/*` | 6 → CI Gate 1 | 0, 1, 2, 2.5, 3, 3.5, 4, 5 |
| **Docs + `.feature` changed** (`fast_track: docs+feature`) | `docs/*` | 0 → 6 → CI Gate 1 | 1, 2, 2.5, 3, 3.5, 4, 5 |
| **IaC/Config-only** (`fast_track: infra`) | `infra/*` | 1 → 2 (integration) → 2.5 (smoke) → 5 | 0, 3, 3.5, 4, 6 |
| **Security-patch** (dependency update due to CVE, no logic change) (`fast_track: security-patch`) | `hotfix/*` or `infra/*` | 2 (unit+regression) → 5 (CVE-scan) → CI Gate 1 | 0, 2.5, 3, 3.5, 4, 6 |
| **Agent prompt update** (`fast_track: agent-prompt-update`) | `feature/*` | §5 procedure → CI Gate 1 | 0–6 pipeline |

**Hotfix procedure:**

```text
1. branch: hotfix/<id>-<slug> from main
2. Phase 1: executor → quick fix (max 3 iter, no full TDD)
3. Phase 2: unit tests only — existing tests are not broken, regression test for the bug
4. CI Gate 1: all tests green
5. Phase 5: security-critic — no secrets leaked?
6. PR → merge to main + tag vX.Y.(Z+1)
7. Backmerge: main → develop (required)
```

**Rollback procedure (when the hotfix will take > 30 minutes):**

```text
1. git revert <last-good-commit> --no-edit
2. Additional PR → fast-merge into main (CI Gate 1, skip Gate 2/3)
3. tag: vX.Y.Z-rollback
4. Backmerge: main → develop
5. Hotfix continues in the hotfix/* branch in parallel
```

> **Rule:** orchestrator checks the change type before starting the pipeline.
> Hotfix criterion: bug is reproducible in `main`, no time for the full cycle.
> Docs-only criterion: only `*.md`, `*.txt`, `*.rst` files changed (no `.feature`), and no code/IaC changes.
> `.feature` classification rule: if the change set would otherwise be `docs-only` but includes one or more `.feature` files, `fast_track` MUST be `docs+feature` (never `docs-only`); otherwise keep `feature` / `lightweight-feature` as applicable.
> **Lightweight feature criterion** (ALL conditions must be met):
>   - Change is isolated within one module / package; no cross-module API changes
>   - No new external dependencies and no database schema migrations
>   - No conflict with ADR and no new ADR required
>   - No public API changes (adding a field to an internal type / method is allowed)
>   - Change does not touch authentication, authorization, or PII
>   If any condition is not met — run the full feature pipeline.
> **Docs + `.feature`: roles in Phase 0** — `architect` reviews the modified `.feature` files; `architect-critic` issues the verdict (APPROVE / REQUEST_CHANGES). This Phase 0 review does not involve code/IaC executors; documentation work still runs in Phase 6.

---

## 1.4 Manual Test Plans

> Based on: [IEEE 829-2008](https://standards.ieee.org/ieee/829/) (Test Case Specification, Test Procedure Specification),
> [Session-Based Test Management](https://www.satisfice.com/sbtm) (James Bach, 2000), ISTQB Foundation.
>
> A manual test plan is a **step-by-step guide** for a human (QA, product owner, developer)
> to verify UI and user scenarios.
> It complements automated tests: covers visual layout, complex UX flows,
> cross-browser behaviour, accessibility — everything that is expensive or impossible to fully automate.

### 1.4.1 Who creates it and when

`frontend-dev` creates a manual test plan when:

```text
- Implementing a new critical user flow (any scenario from .feature)
- Changing the observable behaviour of an existing flow
- Adding a form with validation, a multi-step wizard, a new state (empty, error, loading)
- Adding a new page or navigation route
```

The test plan **must be updated** whenever the observable behaviour changes — just like `.feature`.
Stored at: `docs/test-plans/<feature-name>.md` (canonical path).

### 1.4.2 Format (IEEE 829 Test Procedure Specification + Gherkin scenarios)

```markdown
# Manual Test Plan: <Feature Name>
<!-- Scenario ref: domain/specs/<file>.feature -->

**Target environment:** staging | dev | local
**App version:** X.Y.Z
**Last updated:** YYYY-MM-DD

## Prerequisites
- [ ] Environment deployed: <URL>
- [ ] Account with role: <role / permissions>
- [ ] Test data: <what must exist in the system>
- [ ] Browser / device: <list if cross-browser test>

## TC-001: <Test Case Name>
**Scenario ref:** `<file>.feature : Scenario: <name>`
**Goal:** <what we are verifying — one sentence>

| # | Action | Expected result |
|---|--------|-----------------|
| 1 | Open <URL> | Page loads; heading <X> is visible |
| 2 | Click the "<Label>" button | <Y> opens; URL becomes <Z> |
| 3 | Enter "<value>" in the "<Field>" field | Field accepts input; no validation error appears |
| 4 | Click "Submit" | Form closes; a new entry appears in the table |

**Pass criteria:** <observable sign of success — without the word "works">
**Fail criteria:** <observable sign of failure>
**Edge cases to probe:** <boundary conditions for exploratory testing (SBTM charter)>

## TC-002: ...
```

### 1.4.3 Composition rules

```text
- Each step = one action + one expected result
- Expected result: only what the tester sees (not the internal state of the system)
- Preconditions are specific: not "log in" but "log in as role=admin"
- Each TC is linked to a .feature scenario via Scenario ref
- Pass/Fail criteria do not contain "works" / "does not work" — only observable signs
- Test plan is understandable by the product owner without knowledge of the code
```

---
