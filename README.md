# Agent Army

Main orchestrator, runtime, and control plane for the agent platform.

## Role

Agent Army is the entry point for all user interactions. It:

- Receives tasks from the user (Telegram or CLI)
- Maintains the orchestrator graph and session state
- Routes tasks to specialist agents via the agent registry
- Owns the runtime knowledge store
- Enforces the task lifecycle (dispatch → result)

**Agent Army runs and controls. It does not create or configure agents.**

## Related repos

| Repo | Role |
|------|------|
| `agent-army` (this repo) | Orchestrator / runtime / control plane |
| `agent-factory` | Creates, configures, and stages agents only |
| `ai-tech-lead` | Specialist coding agent |

## Agent registry

Agents are defined and staged in `agent-factory`. Army reads the registry from:

```
~/projects/agent-factory/config/agents/
```

Override with the `AGENT_FACTORY_ROOT` environment variable.

## Quick start

```bash
cd ~/projects/agent-army
uv sync
uv run agent-army --help
uv run agent-army chat
uv run agent-army telegram
```

## Tests

```bash
cd ~/projects/agent-army
uv run pytest
```

## Environment

Copy `.env.example` to `.env` and set:

```
OPENAI_API_KEY=...
ARMY_BOT_TOKEN=...          # Telegram bot token
ARMY_ALLOWED_CHAT_IDS=...   # Comma-separated Telegram chat IDs
ARMY_MODEL=gpt-4.1-mini     # Optional model override
```

## Key files

- `src/agent_army/orchestrator.py` — LangGraph orchestrator
- `src/agent_army/registry.py` — Registry reader (reads from agent-factory)
- `src/agent_army/telegram_gateway.py` — Telegram polling bot
- `src/agent_army/cli.py` — CLI entry point
- `src/agent_army/knowledge_store.py` — Runtime knowledge store
- `docs/ARCHITECTURE.md` — Architecture overview

## Backlog

https://docs.google.com/spreadsheets/d/1v1zJjwGTqhOgb06nYChaGjRNZIVXQht5pNBUbh9r7RA/edit
