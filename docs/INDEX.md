# Agent Army Documentation Index

Use this file as the documentation entry point.

## Core documents

| Document | Purpose |
|---|---|
| `../README.md` | Front door only: role, repo boundaries, and links. No command blocks. |
| `ARCHITECTURE.md` | System responsibility, repo split, data flow, registry contract, persistence ownership. |
| `COMMANDS.md` | Canonical setup, run, test, and environment commands. |

## Backlog

Live backlog:

https://docs.google.com/spreadsheets/d/1v1zJjwGTqhOgb06nYChaGjRNZIVXQht5pNBUbh9r7RA/edit

## Documentation health rules

- README is a front door, not a runbook.
- Standard command blocks live only in `docs/COMMANDS.md`.
- Other docs may link to `docs/COMMANDS.md`, but must not repeat the same commands.
- Architecture docs must not carry stale backlog item lists.
- When architecture, ownership, setup, runtime, commands, registry, lifecycle, or agent boundaries change, check documentation impact before calling the work done.
- If a documentation impact check finds unresolved work, add a backlog item instead of leaving it in chat.
