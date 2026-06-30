# Agent Army

Runtime orchestrator and control plane. Receives tasks and dispatches to released specialist agents.

## Role

- **Army runs and controls.** It does not create, stage, or modify agents.
- **Factory creates.** Agent definitions live in `agent-factory`; Army reads released agents from the registry.
- **Specialist agents** receive tasks dispatched by Army.
- **Coding workers** such as Codex or Claude Code perform bounded implementation work only when routed by the appropriate controlling agent.

## Documentation entry point

Use `docs/INDEX.md` first.

Canonical setup, run, test, and environment commands live only in `docs/COMMANDS.md`. Do not duplicate standard command blocks in README, architecture docs, or handoff text.

## Where things live

| Concern | Repo |
|---------|------|
| Orchestrator, routing, Telegram gateway | `agent-army` |
| Agent design, staging, approval workflow | `agent-factory` |
| Technical-lead control of coding work | `ai-tech-lead-agent` |
| Implementation work | Codex / Claude Code / other bounded coding workers |

## Rules

- Secrets live in `.env` and must never be committed.
- Tests must never write to permanent data; fixtures must isolate all stores.
- Agent registry is read from `agent-factory/config/agents/`; Army never writes there.
- New agent integrations go in `src/agent_army/` as adapter or dispatch code only.
- No hardcoded fallbacks or compatibility shims without explicit approval.
- Documentation impact must be checked before work is called done.

## Backlog

The live backlog is linked from `docs/INDEX.md`.

## Finish report

- Files changed
- Behaviour changed
- Validation evidence, referencing `docs/COMMANDS.md` if a standard command was used
- Documentation impact checked
- Remaining risk or follow-up
