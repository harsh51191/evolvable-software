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
