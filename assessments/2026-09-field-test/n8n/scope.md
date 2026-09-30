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
