# n8n: scope

| Item | Value |
|---|---|
| Software | n8n, a workflow automation platform with AI agents, Instance AI, chat hub and MCP |
| Repository and tip | `github.com/n8n-io/n8n` @ `c17c48043eb1080e5ae9795ea3a384960f8748f1`, `master`, committed 2026-09-30 |
| Assessment date | 2026-09-30 |
| Declared archetype | `configurable-application-platform` |
| In scope | `packages/` (cli, core, workflow, nodes-base, frontend, @n8n/*) including `*.ee` enterprise modules, `scripts/`, CI configuration |
| Out of scope | n8n Cloud, the n8n.io template gallery, third-party community nodes |

## Archetype decision

Users define rules (workflows), integrations, data tables and forms without code, so `configurable-application-platform`. `developer-platform` was a close alternative. Neither archetype excludes any criterion, so the choice does not change the numbers, which is itself a finding: the archetype label matters only through exclusions.

## Not-applicable decisions

None.

## Licence note

Enterprise modules (`*.ee`: source control, workflow reviews, log streaming, evaluations) are in the repository under n8n's Sustainable Use and Enterprise licences and were assessed as shipped.

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Workflows, credentials, executions and data tables in the database. |
| `schema_changes` | true | TypeORM migrations (packages/@n8n/db/src/migrations) and data tables created at runtime. |
| `multi_tenant` | false | One instance per customer; projects separate work inside an instance but are not isolated tenants. |
| `hosted_service` | true | Main, worker and webhook processes run as long-lived services, with multi-main and queue mode (packages/cli/src/scaling). |
| `machine_actions` | true | The public API and MCP server change workflows and credentials (packages/cli/src/modules/mcp). |
| `agent_mutations` | true | The AI workflow builder and Instance AI change workflows (packages/cli/src/modules/instance-ai, workflow-builder). |
| `evolution_auto_apply` | false | AI-built changes pass approvals before they apply. |
| `definition_change_path` | true | Workflows, credentials, variables and data tables are definitions. |
| `code_release_path` | false | The AI lanes change workflows, not n8n code. |
