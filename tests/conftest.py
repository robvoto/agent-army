"""Test isolation fixtures for agent-army."""

import pytest


@pytest.fixture(autouse=True)
def _isolate_checkpointer(tmp_path, monkeypatch):
    import agent_army.checkpointer as cp_mod

    monkeypatch.setattr(cp_mod, "CHECKPOINT_DB", tmp_path / "checkpoints.sqlite3")
    monkeypatch.setattr(cp_mod, "_conn", None)
    monkeypatch.setattr(cp_mod, "_checkpointer", None)


@pytest.fixture(autouse=True)
def _isolate_knowledge_store(tmp_path, monkeypatch):
    import agent_army.knowledge_store as ks_mod

    monkeypatch.setattr(ks_mod, "_store", None)
    # Redirect shared store path to tmp so tests never touch the real agent-factory DB
    monkeypatch.setattr(ks_mod, "SHARED_KNOWLEDGE_DB", tmp_path / "knowledge_store.sqlite3")
    monkeypatch.setattr(ks_mod, "LOCAL_KNOWLEDGE_DB", tmp_path / "knowledge_store_local.sqlite3")


@pytest.fixture()
def sample_registry_dir(tmp_path):
    """Create a minimal agent registry directory for testing."""
    registry = tmp_path / "agents"
    (registry / "code-reviewer").mkdir(parents=True)
    (registry / "code-reviewer" / "agent.json").write_text(
        '{"id": "code-reviewer", "name": "Code Reviewer", "purpose": "Reviews code for quality",'
        ' "aliases": ["reviewer"], "tools": ["read_file"], "version": "1.0.0"}'
    )
    (registry / "job-hunter").mkdir()
    (registry / "job-hunter" / "agent.json").write_text(
        '{"id": "job-hunter", "name": "Job Hunter", "purpose": "Finds job listings",'
        ' "aliases": [], "tools": [], "version": "2.0.0"}'
    )
    return registry
