"""LangGraph orchestrator — supervisor that routes to enabled agents via tool calls."""

from __future__ import annotations

import logging
import uuid
from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool as lc_tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .checkpointer import get_checkpointer
from .config import DEFAULT_MODEL
from .knowledge_store import get_knowledge_store
from .registry import AgentSpec, load_registry

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = """You are the Agent Army orchestrator. You coordinate a fleet of AI agents
and answer questions about their capabilities and status.

When a user's request is best handled by a specific agent, explain which agent would handle it
and what it would do. You have access to the agent registry and shared knowledge base.

Be concise. If the user asks you to run a task, route it clearly. If no agent exists yet for
the task, say so and suggest how it could be added."""


def _make_agent_tool(spec: AgentSpec) -> Any:
    """Create a LangChain tool for each registered agent."""

    @lc_tool(name=spec.id, description=f"{spec.name}: {spec.purpose}")
    def _call_agent(task: str) -> str:
        """Invoke this agent with a task description."""
        return (
            f"[{spec.name} v{spec.version}] Routing task: {task!r}\n"
            f"Agent '{spec.id}' is registered but not yet wired for live invocation. "
            f"Capabilities: {', '.join(spec.tools) if spec.tools else 'none listed'}."
        )

    return _call_agent


def _build_memory_tools(store: Any) -> list[Any]:
    try:
        from langmem import create_manage_memory_tool, create_search_memory_tool

        return [
            create_manage_memory_tool(
                ("army", "learnings"),
                store=store,
                instructions="Store reusable facts, decisions, and learnings about agents and tasks.",
            ),
            create_search_memory_tool(
                ("shared", "docs"),
                store=store,
                instructions="Search shared documentation and architecture notes.",
            ),
        ]
    except Exception as exc:
        logger.debug("langmem tools not available: %s", exc)
        return []


class ArmyOrchestrator:
    """Stateful orchestrator with per-session thread isolation."""

    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        self._model = model
        self._registry = load_registry()
        self._session_id = str(uuid.uuid4())
        self._graph = self._build_graph()

    def _build_graph(self) -> Any:
        store = get_knowledge_store()
        checkpointer = get_checkpointer()

        agent_tools = [_make_agent_tool(s) for s in self._registry]
        memory_tools = _build_memory_tools(store)
        tools = agent_tools + memory_tools

        llm = ChatOpenAI(model=self._model, temperature=0)

        return create_react_agent(
            model=llm,
            tools=tools,
            prompt=_SYSTEM_PROMPT,
            checkpointer=checkpointer,
            store=store,
        )

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def registry(self) -> list[AgentSpec]:
        return self._registry

    def new_session(self) -> None:
        """Start a fresh conversation while preserving history in SQLite."""
        self._session_id = str(uuid.uuid4())
        logger.info("New army session: %s", self._session_id)

    def invoke(self, message: str) -> str:
        """Send a message and return the assistant's text reply."""
        config = {"configurable": {"thread_id": self._session_id}}
        result = self._graph.invoke(
            {"messages": [HumanMessage(content=message)]},
            config=config,
        )
        messages = result.get("messages", [])
        if messages:
            return messages[-1].content
        return "(no response)"
