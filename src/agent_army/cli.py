"""CLI entry point for the Agent Army."""

from __future__ import annotations

import argparse
import os
import sys

from .logging_config import configure_logging


def _run_chat(model: str) -> None:
    from .orchestrator import ArmyOrchestrator

    orch = ArmyOrchestrator(model=model)
    registry = orch.registry

    if registry:
        print(f"Agent Army ready — {len(registry)} agent(s) registered.")
        for spec in registry:
            print(f"  • {spec.name} ({spec.id}): {spec.purpose}")
    else:
        print("Agent Army ready — no agents registered yet.")

    print("Commands: /new (reset session), /agents (list agents), /quit or Ctrl-C to exit.\n")

    while True:
        try:
            text = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break

        if not text:
            continue

        if text == "/quit":
            print("Bye.")
            break

        if text == "/new":
            orch.new_session()
            print("New session started.")
            continue

        if text == "/agents":
            if not orch.registry:
                print("No agents registered yet.")
            else:
                for spec in orch.registry:
                    print(f"  {spec.name} ({spec.id}): {spec.purpose}")
            continue

        try:
            reply = orch.invoke(text)
            print(f"\nArmy: {reply}\n")
        except Exception as exc:
            print(f"Error: {exc}", file=sys.stderr)


def _run_telegram() -> None:
    from .telegram_gateway import run_telegram

    run_telegram()


def main() -> None:
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(prog="agent-army", description="Agent Army orchestrator")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable Agent Army debug logging")

    sub = parser.add_subparsers(dest="command")

    chat_parser = sub.add_parser("chat", help="Interactive CLI chat (default)")
    chat_parser.add_argument("--model", default=os.getenv("ARMY_MODEL", "gpt-4.1-mini"))

    sub.add_parser("telegram", help="Run the Telegram bot gateway")

    args = parser.parse_args()
    configure_logging(args.verbose)

    command = args.command or "chat"

    if command == "chat":
        model = getattr(args, "model", os.getenv("ARMY_MODEL", "gpt-4.1-mini"))
        _run_chat(model)
    elif command == "telegram":
        _run_telegram()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
