# Agent Army

Runtime orchestrator and control plane. Receives tasks, dispatches to specialist agents.

## Role

- **Army runs and controls.** It does not create or configure agents.
- **Factory creates.** Agent definitions live in `agent-factory`; army reads them.
- **Specialist agents** (ai-tech-lead, etc.) receive tasks dispatched by army.

## Where things live

| Concern | Repo |
|---------|------|
| Orchestrator, routing, Telegram gateway | `agent-army` (here) |
| Agent creation, staging, approval workflow | `agent-factory` |
| Specialist coding tasks | `ai-tech-lead` |

## Rules

- Run from WSL at `~/projects/agent-army`
- Secrets live in `.env` — never committed
- Tests must never write to permanent data; conftest fixtures isolate all stores
- Agent registry is read from `agent-factory/config/agents/` — army never writes there
- New agent integrations go in `src/agent_army/` (adapter / dispatch code only)
- No hardcoded fallbacks or compatibility shims without explicit approval

## Backlog

The live backlog is a Google Sheet:
https://docs.google.com/spreadsheets/d/1v1zJjwGTqhOgb06nYChaGjRNZIVXQht5pNBUbh9r7RA/edit

## Finish report

- Files changed
- Behaviour changed
- Validation command/result, or why not run
- Remaining risk or follow-up
