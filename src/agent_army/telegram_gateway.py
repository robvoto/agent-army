"""Telegram polling bot gateway for the Agent Army."""

from __future__ import annotations

import logging
import os
import time
from typing import Any

import httpx

from .logging_config import safe_preview
from .orchestrator import ArmyOrchestrator

logger = logging.getLogger(__name__)

_POLL_TIMEOUT = 30
_API_BASE = os.getenv("TELEGRAM_API_BASE", "https://api.telegram.org")


def _api(token: str, method: str, **kwargs: Any) -> dict:
    url = f"{_API_BASE}/bot{token}/{method}"
    resp = httpx.post(url, json=kwargs, timeout=60)
    resp.raise_for_status()
    return resp.json()


def _get_updates(token: str, offset: int) -> list[dict]:
    try:
        data = _api(token, "getUpdates", offset=offset, timeout=_POLL_TIMEOUT)
        updates = data.get("result", [])
        if updates:
            logger.debug("Telegram updates received: %d", len(updates))
        return updates
    except Exception as exc:
        logger.warning("Telegram getUpdates failed: %s", exc)
        return []


def _send_message(token: str, chat_id: int, text: str) -> None:
    try:
        chunks = [text[i : i + 4096] for i in range(0, len(text), 4096)]
        logger.debug(
            "Telegram sending reply | chat_id=%s | chars=%d | chunks=%d",
            chat_id,
            len(text),
            len(chunks),
        )
        for chunk in chunks:
            _api(token, "sendMessage", chat_id=chat_id, text=chunk, parse_mode="Markdown")
    except Exception as exc:
        logger.error("Telegram sendMessage failed | chat_id=%s | error=%s", chat_id, exc)


def _allowed_chat_ids() -> set[int]:
    raw = os.getenv("ARMY_ALLOWED_CHAT_IDS", "")
    if not raw.strip():
        logger.warning("ARMY_ALLOWED_CHAT_IDS is empty; all Telegram chats are allowed.")
        return set()
    try:
        allowed = {int(x.strip()) for x in raw.split(",") if x.strip()}
        logger.info("Telegram allowlist loaded | allowed_chats=%d", len(allowed))
        return allowed
    except ValueError:
        logger.warning("Invalid ARMY_ALLOWED_CHAT_IDS value; no allowlist loaded.")
        return set()


class TelegramGateway:
    def __init__(self, token: str, orchestrator: ArmyOrchestrator) -> None:
        self._token = token
        self._orch = orchestrator
        self._allowed = _allowed_chat_ids()

    def _is_allowed(self, chat_id: int) -> bool:
        return not self._allowed or chat_id in self._allowed

    def _handle_message(self, msg: dict) -> None:
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "").strip()

        if not self._is_allowed(chat_id):
            logger.info("Telegram message ignored | chat_id=%s | reason=unauthorised", chat_id)
            return

        if text == "/new":
            logger.info("Telegram command received | chat_id=%s | command=/new", chat_id)
            self._orch.new_session()
            _send_message(self._token, chat_id, "Started a fresh conversation.")
            return

        if text == "/agents":
            logger.info("Telegram command received | chat_id=%s | command=/agents", chat_id)
            specs = self._orch.registry
            if not specs:
                reply = "No agents registered yet."
            else:
                lines = [f"*{s.name}* (`{s.id}`): {s.purpose}" for s in specs]
                reply = "**Registered agents:**\n" + "\n".join(lines)
            _send_message(self._token, chat_id, reply)
            return

        if not text:
            logger.debug("Telegram empty message ignored | chat_id=%s", chat_id)
            return

        if text.startswith("/"):
            logger.info("Telegram command ignored | chat_id=%s | command=%s", chat_id, safe_preview(text))
            return

        logger.info("Telegram user message received | chat_id=%s | chars=%d", chat_id, len(text))
        logger.debug("Telegram message preview: %s", safe_preview(text, max_chars=140))
        try:
            reply = self._orch.invoke(text)
        except Exception as exc:
            logger.exception("Telegram orchestrator error | chat_id=%s", chat_id)
            reply = f"Error: {exc}"

        _send_message(self._token, chat_id, reply)

    def run(self) -> None:
        logger.info("Army Telegram gateway starting | session=%s", self._orch.session_id)
        offset = 0
        while True:
            updates = _get_updates(self._token, offset)
            for update in updates:
                offset = update["update_id"] + 1
                msg = update.get("message") or update.get("edited_message")
                if msg:
                    self._handle_message(msg)
            if not updates:
                time.sleep(1)


def run_telegram(token: str | None = None) -> None:
    from dotenv import load_dotenv

    load_dotenv()
    tok = token or os.getenv("ARMY_BOT_TOKEN")
    if not tok:
        raise RuntimeError("ARMY_BOT_TOKEN is not set.")

    orch = ArmyOrchestrator()
    gateway = TelegramGateway(tok, orch)
    gateway.run()
