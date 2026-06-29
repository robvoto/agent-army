# Agent Army — Architecture

## Responsibility

Agent Army is the **main orchestrator, runtime, and control plane** for the agent platform.

- Receives all user input (Telegram / CLI)
- Maintains session state and conversation history
- Routes tasks to the correct specialist agent
- Owns the army knowledge store
- Reports results back to the user

Agent Army does **not** create, configure, or stage agents. That is `agent-factory`'s job.

## Repo split

```
agent-army       ← this repo
  orchestrator   — LangGraph supervisor graph
  registry       — reads agent specs from agent-factory
  telegram       — user-facing Telegram bot
  cli            — chat and telegram commands
  knowledge_store — army runtime knowledge (army/data/)
  checkpointer   — LangGraph SQLite checkpoint store

agent-factory    ← specialist agent
  factory_brain  — designs and stages agent packages
  telegram       — factory admin bot (staging, approvals)
  storage        — staged_agents, approvals, factory_threads
  agent_spec     — Pydantic validation for agent packages
  agent_catalog  — staged + enabled agent inventory
  creator_workflow — deterministic scaffolding workflow

ai-tech-lead     ← specialist agent
  (separate repo, called by army)
```

## Data flow

```
User (Telegram / CLI)
  │
  ▼
Army Telegram Gateway / CLI
  │
  ▼
ArmyOrchestrator (LangGraph)
  │
  ├── reads registry from agent-factory/config/agents/
  │
  ├── dispatches to specialist agents
  │   ├── ai-tech-lead  (coding tasks)
  │   ├── agent-factory (create/configure agents)
  │   └── future specialists
  │
  └── stores learnings in army/data/knowledge_store.sqlite3
```

## Agent registry contract

Agents are registered in `agent-factory/config/agents/<id>/agent.json`. Army reads:

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | yes | unique identifier |
| `name` | yes | display name |
| `purpose` | yes | used by orchestrator for routing decisions |
| `aliases` | yes | command aliases |
| `tools` | yes | declared tool list |
| `version` | no | defaults to "1.0.0" |

Factory is responsible for writing all fields including `purpose`. Army reads but never writes.

## Persistence

| Store | Path | Owner |
|-------|------|-------|
| Knowledge store | `army/data/knowledge_store.sqlite3` | Army |
| Checkpoints | `army/data/checkpoints.sqlite3` | Army |
| Staged agents | `factory/data/agent_factory.sqlite3` | Factory |
| Factory checkpoints | `factory/data/factory_checkpoints.sqlite3` | Factory |
| Factory knowledge | `factory/data/knowledge_store.sqlite3` | Factory |

## Backlog

Live backlog: https://docs.google.com/spreadsheets/d/1v1zJjwGTqhOgb06nYChaGjRNZIVXQht5pNBUbh9r7RA/edit

Key open items:
- ARMY-001: Real specialist agent dispatch (orchestrator stubs the call)
- ARMY-002: Approval workflow for tasks requiring human sign-off
- ARMY-003: Token / cost tracking in army
- ARMY-004: Connect army and factory knowledge stores
- ARMY-007: Wire agent-factory as callable specialist from army
- ARMY-008: No-fallback / no-hardcode enforcement gate
