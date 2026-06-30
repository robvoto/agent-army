# Agent Army

Main orchestrator, runtime, and control plane for the agent platform.

## Role

Agent Army is the entry point for user interactions. It:

- Receives tasks from the user through Telegram or CLI
- Maintains the orchestrator graph and session state
- Routes tasks to released specialist agents via the agent registry
- Owns the runtime knowledge store
- Enforces the task lifecycle from dispatch to result

**Agent Army runs and controls. It does not create, stage, or modify agents.**

## Related repos

| Repo | Role |
|------|------|
| `agent-army` (this repo) | Orchestrator / runtime / control plane |
| `agent-factory` | Designs, scaffolds, stages, and tests agents; delegates implementation to bounded coding agents |
| `ai-tech-lead-agent` | Technical-lead specialist that plans, reviews, and controls bounded coding-agent work |
| Codex / Claude Code / other coding agents | Implementation workers used through approved bounded task packs |

## Documentation

Use `docs/INDEX.md` as the documentation entry point.

Canonical commands live in `docs/COMMANDS.md`. Do not duplicate command blocks in this README.

## Backlog

The live backlog is linked from `docs/INDEX.md`.
