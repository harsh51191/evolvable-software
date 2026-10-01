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

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Sessions and messages in a local database (packages/opencode/src/storage). |
| `schema_changes` | true | Drizzle migrations for the session database (packages/opencode/migration). |
| `multi_tenant` | false | A local single-user tool. |
| `hosted_service` | false | A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. |
| `agent_mutations` | false | No product feature lets the agent change OpenCode's own agents, commands or configuration. |
| `automatic_apply` | false | Nothing changes OpenCode's definitions automatically. |
| `code_release_path` | false | The GitHub agent the team runs on this repository is the product's general coding agent, not a first-party evolution system for OpenCode (rubric rule 12). |
