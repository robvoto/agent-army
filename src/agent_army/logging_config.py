"""Logging configuration for Agent Army.

Keep operator logs useful without exposing provider request payloads, headers, cookies,
or full prompts from third-party SDK debug loggers.
"""

from __future__ import annotations

import logging

_FORMAT = "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_NOISY_OR_SENSITIVE_LOGGERS = [
    "openai",
    "openai._base_client",
    "httpx",
    "httpcore",
    "httpcore.connection",
    "httpcore.http11",
    "httpcore.proxy",
    "langchain",
    "langgraph",
]


def configure_logging(verbose: bool = False) -> None:
    """Configure logging with safe defaults.

    Verbose mode enables DEBUG for Agent Army code only. Third-party HTTP/provider
    libraries remain at WARNING to avoid dumping prompts, request bodies, headers,
    cookies, tokens, and other noisy internals.
    """

    root_level = logging.INFO
    army_level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        format=_FORMAT,
        datefmt=_DATE_FORMAT,
        level=root_level,
        force=True,
    )

    logging.getLogger("agent_army").setLevel(army_level)

    for logger_name in _NOISY_OR_SENSITIVE_LOGGERS:
        logging.getLogger(logger_name).setLevel(logging.WARNING)


def safe_preview(value: str, *, max_chars: int = 80) -> str:
    """Return a short single-line preview for human logs.

    This is for operator readability only. It avoids dumping long prompts or full
    user messages into logs.
    """

    clean = " ".join(value.split())
    if len(clean) <= max_chars:
        return clean
    return clean[: max_chars - 3] + "..."
