# Directus: scope

| Item | Value |
|---|---|
| Software | Directus, a data platform and headless CMS that mirrors a SQL database and adds generated APIs, a Data Studio app, automation, an AI assistant and an MCP server |
| Repository and tip | `github.com/directus/directus` @ `2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a`, `main`, committed 2026-09-29 |
| Assessment date | 2026-09-30 |
| Declared archetype | `configurable-application-platform` |
| In scope | `api/`, `app/`, `sdk/`, `packages/` (including CLI sync, extensions SDK, registry and AI), CI configuration, `tests/` |
| Out of scope | Directus Cloud, hosted marketplace catalogue, templates in other repositories |

## Archetype decision

Administrators define collections, fields, relations, permissions, layouts and flows without code, so `configurable-application-platform` fits. No alternative was seriously considered.

## Not-applicable decisions

None. Directus runs one project per instance. The rubric's tenant clauses (B2, C1, C3, G2) were read as "per project", and G2's anchor explicitly places single-tenant deployments at level 2.

## Licence note

The repository carries a source-available licence and a licence and entitlements manager (`api/src/license`). Features were assessed as present in code; entitlement gating was not traced per feature.
