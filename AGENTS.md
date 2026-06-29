# Agent Army

Runtime orchestrator. Routes tasks to specialized agents.

## Rules
- Run from WSL at ~/projects/agent-army
- Secrets live in .env — never committed
- Tests must never write to permanent data; conftest fixtures isolate all stores
- Agents are enabled in agent-factory; army dispatches to them
- New agent integrations go in src/agent_army/agents/
