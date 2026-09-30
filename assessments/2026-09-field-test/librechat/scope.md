# LibreChat: scope

| Item | Value |
|---|---|
| Software | LibreChat, an open-source multi-provider AI chat application with agents, MCP, prompts, memory and sharing |
| Repository and tip | `github.com/danny-avila/LibreChat` @ `14f7b2865692d27364c934ecb9912496371018bb`, `main`, committed 2026-09-29 |
| Assessment date | 2026-09-30 |
| Declared archetype | `focused-application` |
| In scope | `api/`, `client/`, `packages/`, `e2e/`, `helm/`, `config/`, CI configuration |
| Out of scope | Hosted code interpreter, RAG API image, third-party MCP servers |

## Archetype decision

A chat product with configurable providers and agents, not a platform for defining business objects, so `focused-application`.

## Not-applicable decisions

The fixed `focused-application` rule excludes A1, A3, B1, B2, C2, O1, O2 and O3, each with its would-be score recorded.
