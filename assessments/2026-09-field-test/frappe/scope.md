# Frappe Framework: scope

| Item | Value |
|---|---|
| Software | Frappe Framework, a full-stack, metadata-driven low-code framework (Python, MariaDB/Postgres, Vue) |
| Repository and tip | `github.com/frappe/frappe` @ `82b0384810030c8d347780538821a3b006375d28`, `develop`, committed 2026-09-30 |
| Assessment date | 2026-09-30 |
| Declared archetype | `configurable-application-platform` |
| In scope | Framework core, Desk UI, website module, automation engine, integrations module, CI configuration |
| Out of scope | Apps built on Frappe (ERPNext, HRMS, CRM, Helpdesk), Frappe Cloud, `frappe_docker` |

## Archetype decision

Frappe lets administrators create entity types, fields, workflows, layouts and automations on a live site without code, which matches `configurable-application-platform`. `developer-platform` was considered, because Frappe is a framework and most customers extend it with code apps. It was rejected because the no-code path is first-class: custom DocTypes are allowed outside developer mode.

## Not-applicable decisions

None. Every criterion was judged applicable to a configurable platform. M2 (process-change proposals) was kept applicable and scored 0 rather than excluded, following the framework's rule that missing capability is not non-applicability.

## Conventions applied

See `../README.md`. The site is treated as the tenant unit (multi-site benches give each site its own database).

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Every site keeps documents in MariaDB or PostgreSQL and files on disk. |
| `schema_changes` | true | Creating or editing a DocType alters its table at runtime (frappe/database/schema.py:479-485), and bench migrate applies patches (frappe/patches.txt). |
| `multi_tenant` | true | One bench serves several sites, each with its own database (multi-site benches). |
| `hosted_service` | true | Gunicorn web workers, RQ workers, a scheduler and a socket.io server run as long-lived services. |
| `agent_mutations` | false | No first-party AI or agent changes Frappe definitions in this repository. |
| `automatic_apply` | false | Every definition change is made by a person with the right role; nothing applies changes automatically. |
| `code_release_path` | false | No first-party evolution system ships code changes; releases are made by engineers. |
