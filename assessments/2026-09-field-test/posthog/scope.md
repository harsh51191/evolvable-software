# PostHog: scope

| Item | Value |
|---|---|
| Software | PostHog, a product-engineering suite: analytics, session replay, feature flags, experiments, surveys, data warehouse, CDP, error tracking, LLM analytics, PostHog AI, Signals |
| Repository and tip | `github.com/PostHog/posthog` @ `645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6`, `master`, committed 2026-09-30 |
| Assessment date | 2026-09-30 |
| Declared archetype | `focused-application` |
| In scope | `posthog/`, `ee/`, `products/`, `nodejs/`, `rust/`, `services/mcp/`, `common/hogvm`, CI configuration |
| Out of scope | PostHog Cloud operations, SDK repositories, the separate charts repository |

## Archetype decision

PostHog is a suite for one domain, product engineering data, and has no way to define business-object types, so `focused-application`. `configurable-application-platform` was considered because of warehouse data modelling and the endpoints product, and rejected. The last index column in `scorecard.md` shows the all-criteria result.

## Not-applicable decisions

The fixed `focused-application` rule excludes A1, A3, B1, B2, C2, O1, O2 and O3, each with its would-be score recorded.

## Construct note

Many PostHog capabilities (Signals, Tasks, experiments, autoresearch) run the observe, propose, apply and measure loop for *customers'* software. They were scored as shipped capability. The rubric does not say whether a product must apply the loop to itself.

## Coverage note

About 55,000 tracked files. Evidence was gathered from the modules cited in `evidence.md`, not from a full read. Absence claims are limited to the paths searched.

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Events in ClickHouse, configuration in PostgreSQL, recordings in object storage. |
| `schema_changes` | true | Django and ClickHouse migrations, plus property materialisation that adds columns at runtime (ee/clickhouse/materialized_columns/columns.py). |
| `multi_tenant` | true | Organisations and projects share one deployment with access control and quotas. |
| `hosted_service` | true | Django web, Celery and Temporal workers, Node ingestion and Rust capture services. |
| `machine_actions` | true | The API with scoped personal keys and an MCP server change PostHog objects (posthog/scopes.py, services/mcp). |
| `agent_mutations` | true | PostHog AI creates and edits insights, dashboards and other configured objects (ee/hogai). |
| `evolution_auto_apply` | false | PostHog AI changes are made on request in a conversation; weekly property materialisation applies without approval (posthog/tasks/scheduled.py:927), but it is scheduled maintenance, not a change from the evolution loop. |
| `definition_change_path` | true | Insights, dashboards, feature flags, actions and approval policies are definitions. |
| `code_release_path` | false | Tasks and Stamphog act on customers' repositories (products/stamphog); no first-party lane ships PostHog code changes. |
