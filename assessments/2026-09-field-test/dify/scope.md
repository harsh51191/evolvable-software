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

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Apps, datasets and logs in PostgreSQL; vectors in a vector store; files in object storage. |
| `schema_changes` | true | Alembic migrations (api/migrations/versions, 219 files). |
| `multi_tenant` | true | Workspaces (tenants) share a deployment with per-tenant limits. |
| `hosted_service` | true | API, Celery worker, web, sandbox and plugin daemon run as long-lived services. |
| `agent_mutations` | false | AI generators draft prompts, code and workflow steps into the editor; a person saves and publishes (api/core/llm_generator). |
| `automatic_apply` | false | Every publish is a manual human action. |
| `code_release_path` | false | No first-party evolution system ships code changes. |
