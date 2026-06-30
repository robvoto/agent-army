# Agent Army Commands

This is the only documentation file that should contain standard Agent Army command blocks.

Other docs may link here, but must not duplicate these commands.

## Setup

```bash
cd ~/projects/agent-army
uv sync
```

## Run

```bash
cd ~/projects/agent-army
uv run agent-army --help
uv run agent-army chat
uv run agent-army telegram
```

## Test

```bash
cd ~/projects/agent-army
uv run pytest
```

## Environment

Copy `.env.example` to `.env` and set:

```text
OPENAI_API_KEY=...
ARMY_BOT_TOKEN=...
ARMY_ALLOWED_CHAT_IDS=...
ARMY_MODEL=gpt-4.1-mini
```

## Documentation rule

If a command changes, update this file only. Then check whether README, `docs/INDEX.md`, `AGENTS.md`, and architecture docs still point here correctly.
