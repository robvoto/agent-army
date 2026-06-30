# Agent Army

Main orchestrator, runtime, and control plane for the agent platform.

## Role

Agent Army is the entry point for all user interactions. It:

- Receives tasks from the user (Telegram or CLI)
- Maintains the orchestrator graph and session state
- Routes tasks to released specialist agents via the agent registry
- Owns the runtime knowledge store
- Enforces the task lifecycle (dispatch → result)

**Agent Army runs and controls. It does not create, stage, or modify agents.**

## Related repos

| Repo | Role |
|------|------|
| `agent-army` (this repo) | Orchestrator / runtime / control plane |
| `agent-factory` | Designs, scaffolds, stages, and tests agents; delegates implementation to bounded coding agents |
| `ai-tech-lead-agent` | Technical-lead specialist that plans, reviews, and controls bounded coding-agent work |
| Codex / Claude Code / other coding agents | Implementation workers used through approved bounded task packs |

## Agent registry

Agents are defined and staged in `agent-factory`. Army reads only approved/released agents from the registry.

Initial local registry location:

```
~/projects/agent-factory/config/agents/
```

Override with the `AGENT_FACTORY_ROOT` environment variable.

Army must not discover agents by scanning random project folders or GitHub repositories. Discovery is registry-driven only.

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
- `src/agent_army/registry.py` — Registry reader (reads released agents from agent-factory)
- `src/agent_army/telegram_gateway.py` — Telegram polling bot
- `src/agent_army/cli.py` — CLI entry point
- `src/agent_army/knowledge_store.py` — Runtime knowledge store
- `docs/ARCHITECTURE.md` — Architecture overview

## Backlog

https://docs.google.com/spreadsheets/d/1v1zJjwGTqhOgb06nYChaGjRNZIVXQht5pNBUbh9r7RA/edit
