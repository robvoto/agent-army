#!/usr/bin/env bash
set -euo pipefail

MODE="${1:-chat}"

case "$MODE" in
  chat)
    uv run agent-army chat "${@:2}"
    ;;
  telegram)
    uv run agent-army telegram "${@:2}"
    ;;
  *)
    echo "Usage: $0 [chat|telegram] [--verbose]"
    exit 1
    ;;
esac
