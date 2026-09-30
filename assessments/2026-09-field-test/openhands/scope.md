# OpenHands: scope

| Item | Value |
|---|---|
| Software | OpenHands: the Agent Canvas control centre and the OpenHands agent (SDK, agent server, tools, workspaces) |
| Repositories and tips | `github.com/OpenHands/OpenHands` @ `21cc5c6170fe093c0fcd23ffc61949f4933e17b9` (main, 2026-09-29); `github.com/OpenHands/software-agent-sdk` @ `5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a` (main, 2026-09-30) |
| Assessment date | 2026-09-30 |
| Declared archetype | `agent-runtime` |
| In scope | Agent Canvas (`src/`, `electron/`, `docker/`, `helm/`, `docs/`, `specs/`, CI) and the SDK repository (`openhands-sdk`, `openhands-agent-server`, `openhands-tools`, `openhands-workspace`, CI) |
| Out of scope | OpenHands Cloud |

## Scope decision

`OpenHands/OpenHands` is now a front end whose architecture document delegates execution, sandboxing, confirmation policies and automation runs to the agent server. Under v0.2 those criteria could only be `not_evidenced`. Rubric v0.3 (scoring rule 3) requires assessing delegated capabilities where they live, so the SDK repository is in scope and D2, D3, F3, F4 and K3 are scored from it.

## Not-applicable decisions

The `agent-runtime` exclusions: A1, A2, A3, B1, B2, C2 and G1, each with its would-be score recorded.
