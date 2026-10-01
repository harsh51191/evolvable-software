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

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Conversations, agents, prompts and users in MongoDB. |
| `schema_changes` | true | Data migration scripts change stored documents and indexes (config/migrate-*.js). |
| `multi_tenant` | true | A tenant isolation plugin scopes models by tenant (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts). |
| `hosted_service` | true | Node API serving many users, with optional Redis (api/cache). |
| `machine_actions` | true | The API changes agents, prompts and conversations for authenticated clients, and MCP tools act on users' behalf. |
| `agent_mutations` | false | By default no AI changes LibreChat definitions; the memory agent is commented out in librechat.example.yaml:1351-1360. |
| `evolution_auto_apply` | false | Definition changes are direct human actions by default. |
| `definition_change_path` | true | librechat.yaml, agents and prompts are definitions. |
| `code_release_path` | false | No first-party evolution system ships code changes. |
