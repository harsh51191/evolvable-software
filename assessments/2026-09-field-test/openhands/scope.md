# OpenHands: scope

| Item | Value |
|---|---|
| Software | OpenHands: the Agent Canvas control centre and the OpenHands agent (SDK, agent server, tools, workspaces) |
| Repositories and tips | `github.com/OpenHands/OpenHands` @ `21cc5c6170fe093c0fcd23ffc61949f4933e17b9` (main, 2026-09-29); `github.com/OpenHands/software-agent-sdk` @ `5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a` (main, 2026-09-30); `github.com/OpenHands/automation` @ `ec4c5cc0cb05f3fb01816b36ff6271f6680b6675` (main, 2026-09-30), added for v0.4 |
| Assessment date | 2026-09-30 |
| Declared archetype | `agent-runtime` |
| In scope | Agent Canvas (`src/`, `electron/`, `docker/`, `helm/`, `docs/`, `specs/`, CI), the SDK repository (`openhands-sdk`, `openhands-agent-server`, `openhands-tools`, `openhands-workspace`, CI) and the Automation Service (`openhands/automation`, `migrations`, `tests`) |
| Out of scope | OpenHands Cloud operations |

## Scope decision

`OpenHands/OpenHands` is now a front end whose architecture document delegates execution, sandboxing, confirmation policies and automation runs to the agent server. Under v0.2 those criteria could only be `not_evidenced`. Rubric v0.3 (scoring rule 3) requires assessing delegated capabilities where they live, so the SDK repository is in scope and D2, D3, F3, F4 and K3 are scored from it.

## Not-applicable decisions

The `agent-runtime` exclusions: A1, A2, A3, B1, B2, C2 and G1, each with its would-be score recorded.

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | The Automation Service keeps automations, runs and a key-value store in PostgreSQL (automation repository, migrations/versions). |
| `schema_changes` | true | Alembic migrations in the Automation Service (migrations/versions, 29 files). |
| `multi_tenant` | true | The Automation Service serves organisations with org-scoped data (migrations/versions/023_org_scoped_git_sync.py). |
| `hosted_service` | true | The Automation Service and Agent Server run as long-lived services for OpenHands Cloud. |
| `machine_actions` | true | The Agent Server and Automation Service APIs create and run automations with per-user API keys (automation repository: openhands/automation/auth.py). |
| `agent_mutations` | false | Agents change users' repositories, not OpenHands' own definitions. |
| `evolution_auto_apply` | false | Nothing changes OpenHands' own definitions automatically. |
| `definition_change_path` | true | Automations, skills and settings are definitions. |
| `code_release_path` | false | Automations act on users' repositories; no first-party lane ships OpenHands code changes. |
