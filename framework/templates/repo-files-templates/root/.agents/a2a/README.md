# A2A Profile (Template)

This file documents the repository’s **Agent-to-Agent (A2A)** interaction contract.

## Agents and roles

- TODO: `<project>-orchestrator` — responsibilities
- TODO: `<project>-backend-dev` — responsibilities
- TODO: `<project>-backend-critic` — responsibilities

## Allowed message types

- `PLAN_REQUEST`
- `PLAN_RESPONSE`
- `IMPLEMENTATION_REQUEST`
- `IMPLEMENTATION_RESPONSE`
- `REVIEW_REQUEST`
- `REVIEW_RESPONSE`

## Trust boundaries

- TODO: what information is safe to pass between agents
- TODO: what must never be passed (secrets, raw logs, etc.)

## Message envelope (example)

```json
{
  "type": "PLAN_REQUEST",
  "id": "TODO",
  "from": "<project>-orchestrator",
  "to": "<project>-backend-dev",
  "ts": "2026-01-01T00:00:00Z",
  "payload": {
    "task": "TODO",
    "acceptance_criteria": ["TODO"],
    "constraints": ["TODO"]
  }
}
```
