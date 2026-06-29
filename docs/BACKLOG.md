# Agent Army — Backlog

Items discovered during the army/factory split (2026-06-29). Add to the Google Sheet backlog.

## Must-have (incomplete implementation)

### ARMY-001: Wire real specialist agent dispatch
**Status:** Stubbed  
**Detail:** `orchestrator.py` creates LangChain tools per agent spec but `_call_agent()` returns a stub string — no actual subprocess/API call happens. Dispatch to `ai-tech-lead` and `agent-factory` specialist agents is not implemented.  
**Depends on:** Agent execution contract, army↔specialist handoff payload spec.

### ARMY-002: Approval workflow
**Status:** Not implemented  
**Detail:** Army has no interrupt-on / human-in-the-loop approval gate. The factory brain has one but army does not. Tasks requiring user approval (risky operations, destructive changes) cannot be held for confirmation.

### ARMY-003: Token and cost tracking in army
**Status:** Not implemented  
**Detail:** Factory tracks LLM costs in `cost_log.py` and `data/llm_usage.json`. Army has no equivalent. All LLM calls via army orchestrator are untracked.

### ARMY-004: Connect army and factory knowledge stores
**Status:** Architecturally deferred  
**Detail:** Army previously shared factory's SQLite knowledge store for the `("shared","docs")` namespace. After the split, they are independent. Docs indexed in factory (`knowledge_ingestion.py`) are not visible to army's orchestrator. Requires a shared store path config or a sync mechanism.  
**Options:** (a) Army owns the shared store, factory writes to it. (b) Configure a shared path env var. (c) Accept independent stores and live without the shared namespace.

### ARMY-005: No-fallback / no-hardcode enforcement
**Status:** Not implemented  
**Detail:** AGENTS.md rule says "no hardcoded fallbacks without explicit approval". There is no automated enforcement gate. Needs a pre-commit check or CI rule.

### ARMY-006: Skill / AGENTS.md compliance enforcement
**Status:** Not implemented  
**Detail:** No automated check that code changes comply with AGENTS.md rules or skill constraints. Should be a lint/test step.

## Should-have

### ARMY-007: Persistent run logs
**Status:** Not implemented  
**Detail:** Army has no task execution log. Should record: task received, agent dispatched, result summary, cost, timestamp.

### ARMY-008: Task execution lifecycle states
**Status:** Not implemented  
**Detail:** No formal state machine for task lifecycle (received → dispatched → in-progress → done/failed). Army just invokes and returns synchronously.

### ARMY-009: Factory agent callable via army orchestrator
**Status:** Architectural — not wired  
**Detail:** Factory brain should be callable by army when the user asks to create/modify agents. Currently they are completely independent — factory is only reachable via its own Telegram bot or CLI.

## Won't-do for now (decided)

### ARMY-010: Move factory/knowledge_store.py to army
**Decision:** Not moving. Factory keeps its own knowledge store for factory-specific namespaces. Army owns its own store. Sharing is a future concern (see ARMY-004).

### ARMY-011: Move factory/telegram_gateway.py to army
**Decision:** Not moving. Factory's Telegram bot handles factory-specific admin commands (/staged, /approve, /reject). It is a factory admin surface, not a user-facing orchestrator surface.
