# Dify: scope

| Item | Value |
|---|---|
| Software | Dify, an open-source platform for building LLM applications, agents, workflows and RAG pipelines |
| Repository and tip | `github.com/langgenius/dify` @ `ea38e484b81b4104736d2484aaa1d0d7ea99627e`, `main`, committed 2026-09-30 |
| Assessment date | 2026-09-30 |
| Declared archetype | `configurable-application-platform` |
| In scope | `api/`, `web/`, `dify-agent/`, `dify-agent-runtime/`, `packages/`, `cli/`, `docker/` configuration, CI |
| Out of scope | `dify-sandbox` and `dify-plugin-daemon` source (separate repositories; assessed through configuration), Dify Cloud, the marketplace catalogue |

## Archetype decision

Builders define apps, workflows, knowledge pipelines and integrations without code, so `configurable-application-platform`. `developer-platform` was the alternative. Neither excludes criteria, so the numbers do not change.

## Not-applicable decisions

None.
