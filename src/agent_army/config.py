"""Paths and constants for the Agent Army."""

from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"

# Agent Factory — registry and shared knowledge live here.
# Override with AGENT_FACTORY_ROOT env var if agent-factory lives elsewhere.
AGENT_FACTORY_ROOT = Path(
    os.environ.get("AGENT_FACTORY_ROOT", Path.home() / "projects" / "agent-factory")
)
AGENT_REGISTRY_DIR = AGENT_FACTORY_ROOT / "config" / "agents"
SHARED_KNOWLEDGE_DB = AGENT_FACTORY_ROOT / "data" / "knowledge_store.sqlite3"

# Army-local persistence
CHECKPOINT_DB = DATA_DIR / "checkpoints.sqlite3"
LOCAL_KNOWLEDGE_DB = DATA_DIR / "knowledge_store.sqlite3"

DEFAULT_MODEL = "gpt-4.1-mini"
TELEGRAM_API_BASE = "https://api.telegram.org"


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
