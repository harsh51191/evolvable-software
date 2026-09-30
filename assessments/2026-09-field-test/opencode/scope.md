# OpenCode: scope

| Item | Value |
|---|---|
| Software | OpenCode, an open-source coding agent with TUI, desktop, web, server API and SDK |
| Repository and tip | `github.com/anomalyco/opencode` @ `2fa3363c924c5c3e367b84a87ae478296a0ed59b`, `dev` (default branch), committed 2026-09-29 |
| Assessment date | 2026-09-30 |
| Declared archetype | `agent-runtime` |
| In scope | `packages/` (opencode core, server, sdk, httpapi-codegen, plugin, tui, desktop, web, console, enterprise), `perf/`, `nix/`, CI |
| Out of scope | opencode.ai hosted services, models.dev |

## Archetype decision

A runtime for tools, permissions, agents and sessions, so `agent-runtime`.

## Not-applicable decisions

The fixed `agent-runtime` rule excludes A1, A2, A3, B1, B2, C2 and G1, each with its would-be score recorded.
