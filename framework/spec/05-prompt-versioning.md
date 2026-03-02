# 5. Agent prompt versioning policy

> Split out of [00-multi-agent-development-spec.md](../00-multi-agent-development-spec.md) to keep the umbrella file small.

Agent prompts are code. They must be versioned, reviewed, and tested like code.

## 5.1 Agent changelog

All changes to `.agent.md` files must be documented in `.github/AGENTS_CHANGELOG.md`:

```markdown
# AGENTS_CHANGELOG

| Date | Agent | Type | Description | Author |
|---|---|---|---|---|
| 2026-02-23 | backend-critic | behavior | Add BLOCKER for missing race detector | architect |
| 2026-02-10 | orchestrator | model | gpt-4o → claude-sonnet-4.6 | human |
```

Change types:

| Type | When to use |
|---|---|
| `behavior` | System prompt/rubric/rule changed — agent behavior changes |
| `model` | Agent model changed |
| `tools` | A tool was added/removed (`readFile`, `runTerminal`, etc.; canonical tool IDs: see ./04-observability.md#48-canonical-capability-to-tool-mapping-tool-ids) |
| `fix` | Typos/clarifications without behavior change |

## 5.2 Golden tests after a Critic change

Golden tests are optional-by-choice.
They typically require direct access to an LLM provider API (promptfoo needs a provider endpoint/key), which may not be available in all environments (e.g., GitHub Copilot alone does not provide a promptfoo-compatible API).
If your project maintains critic golden tests, run them after any change to a critic’s system prompt or rubric.

```text
.agents/evals/
├── backend-critic-golden.jsonl      ← {input, expected_verdict, expected_severity}
├── frontend-critic-golden.jsonl
├── devops-critic-golden.jsonl
└── ...

Recommended minimum (if you adopt golden tests): 3 golden tests per agent:
  1. APPROVE scenario          — correct output with no BLOCKERs and no WARNINGs
   2. REQUEST_CHANGES scenario  — output with one clear BLOCKER
   3. REJECT scenario           — critical constitutional violation

```

Run:

```bash
npx promptfoo eval
```

If you split evals into multiple configs (one per agent), run them together:

```bash
promptfoo eval -c .agents/evals/*-promptfooconfig.yaml
```

Example lines for `backend-critic-golden.jsonl`:

```json
{"id":"bc-001","input":{"task":"Add POST /hosts endpoint","result_file":"handlers/host.go","result_summary":"Handler added, input validated, unit test written, godoc present"},"expected_verdict":"APPROVE","expected_severity":"none","description":"APPROVE: correct implementation — no BLOCKERs and no WARNINGs"}
{"id":"bc-002","input":{"task":"Add POST /hosts endpoint","result_file":"handlers/host.go","result_summary":"Handler added but no input validation on body fields"},"expected_verdict":"REQUEST_CHANGES","expected_severity":"BLOCKER","description":"BLOCKER: unvalidated external input (OWASP A03 / Backend Critic rule)"}
{"id":"bc-003","input":{"task":"Add POST /hosts endpoint","result_file":"handlers/host.go","result_summary":"Handler writes directly to devops-managed IaC config — outside backend zone"},"expected_verdict":"REJECT","expected_severity":"BLOCKER","description":"REJECT: executor wrote files outside its responsibility zone (Constitution principle 2)"}
```

Orchestrator golden tests (`orchestrator-golden.jsonl`) validate fast-track selection and decomposition correctness:

```json
{"id":"orch-001","input":{"task":"Fix typo in README.md"},"expected_fast_track":"docs-only","expected_agents":["documentation-writer","documentation-critic"],"description":"Docs-only: Phase 6 documentation update + documentation-critic review"}
{"id":"orch-002","input":{"task":"Update feature spec for login flow"},"expected_fast_track":"docs+feature","expected_agents":["architect","architect-critic","documentation-writer","documentation-critic"],"description":"Docs+feature: Phase 0 architect review of .feature + Phase 6 documentation update"}
{"id":"orch-003","input":{"task":"Add POST /users endpoint with JWT auth"},"expected_fast_track":"feature","expected_agents":["architect","backend-dev","security-critic"],"description":"Feature: full pipeline; security-critic required for new auth endpoint"}
```

`result_summary` is a short description of what the executor produced; promptfoo uses it as `{{result_summary}}` in the prompt template.

Minimal per-agent `*-promptfooconfig.yaml` (starting point; adapt to project stack):

```yaml
# .agents/evals/<agent>-promptfooconfig.yaml
prompts:
   - file://../../.github/agents/<project>-backend-critic.agent.md   # critic system prompt

providers:
  - id: openai:gpt-4o
    config:
      temperature: 0

tests:
  - file://backend-critic-golden.jsonl

defaultTest:
  vars:
    task: "{{task}}"
    result_summary: "{{result_summary}}"
  assert:
    - type: javascript
      value: output.includes(vars.expected_verdict)
```

Create one config per critic: change the `.agent.md` path and the `*-golden.jsonl` file.
> Full format — promptfoo.dev documentation: [promptfoo.dev](https://promptfoo.dev/docs/configuration/guide).

## 5.3 Agent change procedure

```text
1. Create a branch: feature/<task-id>-update-<agent-name>-prompt
2. Edit the .agent.md
3. Run golden tests (if configured): npx promptfoo eval
4. Record the change in .github/AGENTS_CHANGELOG.md
5. Open PR → review like normal code
6. After merge: verify the first 2–3 real tasks with this agent
```
