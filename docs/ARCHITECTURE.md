# Agent Army — Architecture

## Responsibility

Agent Army is the **main orchestrator, runtime, and control plane** for the agent platform.

- Receives all user input through Telegram or CLI
- Maintains session state and conversation history
- Routes tasks to released specialist agents
- Owns the Army knowledge store
- Reports results back to the user

Agent Army does **not** create, configure, stage, or modify agents. That is `agent-factory`'s responsibility.

## Repo split

| Repo / component | Responsibility |
|---|---|
| `agent-army` | Runtime orchestrator, registry reader, Telegram gateway, CLI, Army-owned knowledge store, checkpoint store |
| `agent-factory` | Designs, scaffolds, stages, tests, and promotes agents; delegates implementation to bounded coding workers |
| `ai-tech-lead-agent` | Technical-lead specialist that plans, reviews, and controls bounded coding-agent work |
| Codex / Claude Code / other coding workers | Implementation workers called through bounded, approved task packs |

## Data flow

```text
User
  │
  ▼
Army Telegram Gateway / CLI
  │
  ▼
Army Orchestrator
  │
  ├── reads released agents from the registry
  │
  ├── dispatches to specialist agents
  │   ├── ai-tech-lead-agent
  │   ├── agent-factory
  │   └── future released specialists
  │
  └── stores Army-owned runtime knowledge
```

## Agent registry contract

Agents are registered in `agent-factory/config/agents/<id>/agent.json`.

Army reads the registry. Factory writes and promotes registry entries.

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | yes | Unique identifier |
| `name` | yes | Display name |
| `purpose` | yes | Used by orchestrator for routing decisions |
| `aliases` | yes | Command aliases |
| `tools` | yes | Declared tool list |
| `status` | yes | Draft, incubating, candidate, released, or deprecated |
| `version` | no | Defaults to `1.0.0` |
| `backlog_sheet_id` | no | Google Sheets spreadsheet ID for this agent's backlog |

Army may route work only to approved/released agents. It must not discover agents by scanning random project folders or GitHub repositories.

## Backlog routing

When the user asks Army to add a backlog item for a specialist agent, Army:

1. Looks up the agent in the registry by name or alias.
2. Reads `backlog_sheet_id` from the agent spec.
3. Appends the item to that agent's Google Sheet.
4. Reports clearly if the agent has no backlog sheet configured.

The backlog location is declared in the agent's registry entry. Army must not hardcode specialist backlog URLs.

## Persistence ownership

| Store | Owner |
|-------|-------|
| Knowledge store | Army |
| Checkpoints | Army |
| Staged agents | Factory |
| Factory checkpoints | Factory |
| Factory knowledge | Factory |

## Documentation and commands

Use `docs/INDEX.md` as the documentation entry point.

Standard setup, run, test, and environment commands live only in `docs/COMMANDS.md`.
