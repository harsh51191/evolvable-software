# OpenClaw: scope

| Item | Value |
|---|---|
| Software | OpenClaw, a personal and team AI assistant gateway across messaging channels, devices and tools |
| Repository and tip | `github.com/openclaw/openclaw` @ `df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0`, `main`, committed 2026-09-29 |
| Assessment date | 2026-09-30 |
| Declared archetype | `agent-runtime` |
| In scope | `src/` (gateway, agents, channels, skills and Skill Workshop, audit, system agent, snapshot, MCP), `extensions/`, `skills/`, `custodian-skills/`, `apps/`, `ui/`, `qa/`, `docs/`, CI |
| Out of scope | ClawHub (separate repository), team.openclaw.ai operations |

## Archetype decision

A runtime for tools, memory, skills, channels and execution, so `agent-runtime`.

## Not-applicable decisions

The fixed `agent-runtime` rule excludes A1, A2, A3, B1, B2, C2 and G1, each with its would-be score recorded.

## Why this matters for the Governance and Learning indexes

The Skill Workshop (autonomous experience review, typed proposals, evaluator hooks, event ledger, rollback, policy) is the evidence behind F1–F3, J2, M1–M4, P1 and P2. It lives in `src/skills/workshop/` and `docs/tools/skill-workshop/`. Its defaults (`autonomous.mode: auto`, `approvalPolicy: auto`) mean self-modification is on out of the box, so F3 is scored at its default (auto) with the pending policy as `available_score`.

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Skills, memory, workshop state (SQLite) and configuration on disk. |
| `schema_changes` | true | The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration. |
| `multi_tenant` | false | A personal assistant per installation; shared gateways carry several people but are not isolated tenants (VISION.md). |
| `hosted_service` | false | A personal gateway daemon, not a multi-user service. |
| `machine_actions` | true | Agent tools and the gateway API change skills, configuration and channels. |
| `agent_mutations` | true | The experience review drafts and applies skill proposals (src/skills/workshop/experience-review.ts). |
| `evolution_auto_apply` | true | autonomous.mode auto and approvalPolicy auto are the defaults (src/skills/workshop/config.ts:15-20). |
| `definition_change_path` | true | Skills, memory and configuration are its definitions. |
| `code_release_path` | false | The self-improvement path changes skills, not OpenClaw code. |
