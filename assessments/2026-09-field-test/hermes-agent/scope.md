# Hermes Agent: scope

| Item | Value |
|---|---|
| Software | Hermes Agent by Nous Research: "the self-improving AI agent … with a built-in learning loop" |
| Repositories and tips | `github.com/NousResearch/hermes-agent` @ `bddd22be7c2e5f7630c3d90507e6e7280ff092e3` (main, 2026-09-30); `github.com/NousResearch/hermes-agent-self-evolution` @ `0a929e3aa20e15cf04dc7c28492a7d41a5139125` (main, 2026-06-17) |
| Assessment date | 2026-09-30 |
| Declared archetype | `agent-runtime` |
| In scope | Agent loop, tools, skills and curator, memory, approvals, gateway, MCP and ACP servers, desktop and web, plugins and catalogue, CI; the first-party self-evolution repository |
| Out of scope | Nous Portal and hosted services, third-party skills and plugins |

## Archetype decision

A runtime for tools, memory, skills, planning and execution, so `agent-runtime`.

## Not-applicable decisions

The fixed `agent-runtime` rule excludes A1, A2, A3, B1, B2, C2 and G1, each with its would-be score recorded.

## How v0.3 settles the choices that split raters under v0.2

1. **Skills count as definitions.** `references/archetypes.md` now lists skills, memory, prompts, tool policies and configuration as an agent's customisation surfaces.
2. **Defaults are scored; opt-ins are reported separately.** `skills.write_approval` and `memory.write_approval` default to false, so F2, F3 and P2 carry a lower `score` and a higher `available_score`.
3. **First-party companions are in scope.** `hermes-agent-self-evolution` targets this agent and is assessed with it (rubric scoring rule 3).
