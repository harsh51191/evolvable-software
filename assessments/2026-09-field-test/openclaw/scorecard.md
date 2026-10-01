# OpenClaw: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the openclaw monorepo (gateway, agents, channels, skills and Skill Workshop, plugins and extensions, MCP, Control UI, companion apps, QA and CI). ClawHub (separate repository) and team.openclaw.ai operations are out of scope.

## Reading

**Strongest:** a governed self-modification pipeline. The autonomous experience review drafts skill proposals by default (P1 3). Proposals are revisioned, ledgered and reversible (F1 3, F2 3), and observations are stored on the revision they concern (J2 3). Agent-safe actions are strong (K3 3). **Gaps:** proposals auto-apply by default (F3 2), and no evaluator ships, so learned skills are never compared with the baseline (P2 2, M4 2). Even with opt-ins, the measure stage fails.

## Limits

Repository evidence only, main at the tip named above. ClawHub (registry and scanning) is a separate repository. No evaluator plugin is bundled, so measurement depends on third-party or user plugins. The experience review was read from code and tests, not run. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main). Archetype **agent-runtime**.

Coverage: 42 assessed, 0 not evidenced, 7 not applicable. Grades: 42 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.4 | mechanism | 2.4–2.9 | 2.4 | 2.4 | 2.1 |
| governance | 2.4 | mechanism | 2.4–2.8 | 2.5 | 2.4 | 2.4 |
| learning | 2.4 | mechanism | 2.2–2.9 | 2.4 | 2.4 | 2.4 |
| factory | 2.7 | productised | 2.7–2.8 | 2.7 | 2.7 | 2.7 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.3 | 2.3 |
| Governance | 2.4 | 2.5 |
| Learning | 2.4 | 2.4 |
| Factory | 2.7 | 2.7 |
| Agent Interface | 3.0 | 3.0 |
| Extension Surface | 2.7 | 2.7 |
| Operational Scalability | 2.0 | 2.0 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 3 pass | 3 pass |
| propose | M1, P1 | 2 | 3 pass | 3 pass |
| review | F2 | 2 | 3 pass | 3 pass |
| gate | F3 | 3 | 2 fail | 3 pass |
| apply and roll back | F1 | 2 | 3 pass | 3 pass |
| measure | M4, P2 | 3 | 2 fail | 2 fail |
| verify | L1 | 2 | 3 pass | 3 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| B API surface generation | 2.0 |
| C Rendering follows the definition | 2.0 |
| D Behaviour as data | 2.0 |
| E Compliance and security as infrastructure | 2.0 |
| F Change control | 2.8 |
| G Performance under genericity | 2.0 |
| H Stack flexibility and verification | 2.7 |
| I Extension ecosystem | 2.7 |
| J Observe | 2.3 |
| K Agent and conversational readiness | 3.0 |
| L Factory surfaces | 2.7 |
| M Advise and act | 2.3 |
| N Integration and connector extensibility | 2.7 |
| O Adjacent-domain expansion | 3.3 |
| P Learn from experience | 2.5 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A2 Field definitions carry type and validation | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 2 | 3 |  | A | Typed gateway methods with JSON output modes and MCP JSON output (docs/cli/mcp/json-output.md); no OpenAPI or dry-run for gateway mutations. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A | Canvas serves agent-authored documents and widgets (src/canvas); Control UI layout is code. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A | 278 locale files; themes are engineer-managed. |
| D1 Rules engine with declarative conditions and actions | assessed | 2 | 3 |  | A | Cron jobs, hooks, routing bindings and auto-reply configuration are declared as data (docs/gateway/config-hooks.md, config-automation.md, src/routing, src/auto-reply); no general rules engine with a test mode. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A | Inbound webhook hooks trigger agent runs; audit events record runs, messages and tool actions; no outbound subscriptions with retry. |
| D3 Sandboxed server-side hooks | assessed | 2 | 3 |  | A | Hook scripts run in the gateway process; agent tools for non-main sessions run in sandboxes governed by tool policy and elevated mode (docs/gateway/sandboxing.md, sandbox-vs-tool-policy-vs-elevated.md). |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 1 |  |  | A | No automated accessibility scanning found for the Control UI or companion apps. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A | Audit event store records agent runs, messages and tool actions with queries and configuration (src/audit/audit-event-types.ts, docs/gateway/audit.md); the Skill Workshop keeps an append-only proposal event ledger (docs/tools/skill-workshop/proposals.md). Configuration changes are not audit events. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A | Local-first storage, trajectory export and cleanup (src/trajectory/export.ts, cleanup.ts), and redacted diagnostics export (docs/gateway/health.md:56); not driven by tags. |
| E4 Security as infrastructure | assessed | 3 |  |  | A | Exec approvals with allowlists, DM pairing, tool policies, sandboxing and a secrets subsystem (docs/tools/exec-approvals.md, src/pairing, src/secrets); CodeQL, dependency audit and security review workflows (.github/workflows/codeql.yml, dependency-audit.yml, security-review.yml). |
| F1 Definitions and layouts versioned with rollback | assessed | 3 | 4 |  | A | Workshop collections are backed up and can be restored or rolled back (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); proposal revisions carry hashes (revision-hash.ts); state snapshots to git (src/snapshot/git-backup.ts). |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 3 | 4 |  | A | Skill changes are typed proposals (PROPOSAL.md with revision hashes) that the agent or a person creates; evaluations are stored on the exact revision and apply revalidates the evaluated tree (docs/tools/skill-workshop/proposals.md, src/skills/workshop/service-propose.ts, service-evaluation.ts); the system agent turns chat into proposals for configuration commands with approval classification (src/system-agent/approval-intent.ts). |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 |  | 3 | A | Defaults are autonomous.mode auto and approvalPolicy auto (src/skills/workshop/config.ts:15-20), so proposals apply without a person; evaluator block decisions only exist if an evaluator plugin is installed. Setting approvalPolicy to pending gives a per-class approval policy. |
| F4 Upgrade safety | assessed | 3 |  |  | A | Doctor repairs and migrates configuration (docs/gateway/doctor.md), a compatibility layer (src/compat) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts) around a versioned plugin SDK (src/plugin-sdk). |
| G1 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A | Personal installs are single-tenant; shared gateways carry several people with per-person credit (VISION.md); no noisy-neighbour detection. |
| G3 Ceilings measured, not discovered in incidents | assessed | 2 | 3 |  | A | Performance workflow and test-timing refits in CI (.github/workflows/openclaw-performance.yml, ci-test-timings-refit.yml); no documented per-surface limits. |
| H1 Layers deploy independently | assessed | 3 |  |  | A | Gateway, Control UI and macOS, iOS and Android companion apps are separate deployables with their own release workflows (apps/, .github/workflows/android-release.yml, ios-release-e2e.yml). |
| H2 Module boundaries enforced by tooling | assessed | 3 |  |  | A | Separate TypeScript projects for core, extensions, UI and scripts (tsconfig.core.json, tsconfig.extensions.projects.json) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts). |
| H3 Every change class has an automated pre-land check | assessed | 2 |  |  | A | CI runs on pull requests with CodeQL, dependency audit, E2E and performance checks, but passive draft pull requests are isolated from the main slots (.github/workflows/ci.yml:82-93); no accessibility check. |
| I1 Plugin lane breadth | assessed | 3 | 4 |  | A | Plugins and extensions for channels, providers, tools and memory through a plugin SDK, declarative skills, hooks and an MCP registry (docs/cli/mcp/registry.md); ClawHub is the skill and plugin registry. |
| I2 Runtime isolation and dependency control | assessed | 2 | 3 |  | A | Agent tools can run sandboxed under tool policy; plugins and hooks run in the gateway process with full trust. |
| I3 Developer loop | assessed | 3 |  |  | A | Control UI, doctor, diagnostics export, logs and a QA lab (qa/) let developers validate against a live gateway. |
| K1 Machine-readable capability surface for agents | assessed | 3 |  |  | A | MCP channel-bridge server exposing channel tools (src/mcp/channel-server.ts, channel-tools.ts), an MCP registry and a typed gateway protocol. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A | Users complete tasks conversationally across messaging channels with tool actions; operators configure OpenClaw in natural language through the system agent, which plans one safe command and waits for approval of the pending proposal (src/system-agent/assistant.ts, approval-intent.ts); skills are authored in chat. |
| K3 Agent-safe actions | assessed | 3 |  |  | A | Pairing identities for senders, exec approvals previewing commands, tool policies, sandboxing, idempotency keys on gateway methods (94 non-test files under src/gateway) and audit events for tool actions. |
| N1 Canonical data model with a mapping layer | assessed | 3 |  |  | A | Channel plugins map WhatsApp, Telegram, Slack, Discord, Signal and others onto one canonical message model (src/channels); providers map onto one model interface. |
| N2 Connector definition or SDK | assessed | 3 |  |  | A | The plugin SDK covers channel auth and pairing, inbound and outbound sync and install and configure lifecycle (src/plugin-sdk, custodian-skills/configure-channel). |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | A compatibility layer and doctor migrations keep older configuration working; no public deprecation windows. |
| O1 Kernel concepts are domain-neutral | assessed | 3 |  |  | A | Kernel of gateway sessions (conversation), channels (channel), pairing and auth (identity), tool policy (permission), cron, hooks and flows (workflow), and memory and files (content). |
| O2 A new domain is expressible without kernel change | assessed | 4 | 3 |  | A | About 50 domain skills ship as bundles on an unchanged kernel (skills/: notion, obsidian, github, trello, spotify-player and more), and the agent authors new ones. |
| O3 A domain ships as an installable bundle | assessed | 3 |  |  | A | Skills are versioned, installable bundles installed through ClawHub and the CLI (skills/clawhub, src/cli/skills-cli.ts). |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A | Audit events for runs, messages and tool actions are written as they happen and are queryable (src/audit/audit-event-queries.ts); a runtime trajectory store records sessions (src/trajectory/runtime-store.sqlite.test.ts). |
| J2 Structured learning signals | assessed | 3 | 2 |  | A | Experience-review observations and evaluation findings are stored on the proposal revision they concern and recorded in the append-only proposal event ledger (src/skills/workshop/experience-review*.ts, docs/tools/skill-workshop/proposals.md). |
| J3 Cross-source mining inside the product | assessed | 1 | 2 |  | A | Trajectories export for offline analysis; no joined usage, support and delivery models. |
| M1 Ranked, evidence-backed proposals for change | assessed | 2 | 3 |  | A | The experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, experience-review.ts, proposal-generation.ts); proposals are evidence-backed but not ranked by expected impact. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 3 | 2 |  | A | By default the autonomous experience review drafts and applies skill proposals (autonomous.mode auto, approvalPolicy auto, src/skills/workshop/config.ts:15-20), under the Workshop's policy, revisions and rollback. |
| M4 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A | Evaluator hooks compare each candidate with the complete baseline skill and store metrics and a pass, revise or block decision on the exact revision (docs/tools/skill-workshop/proposals.md); no evaluator is bundled (none in extensions/) and nothing observes impact after apply. |
| P1 The product turns its own operating experience into candidate changes | assessed | 3 | 4 |  | A | With autonomous.mode auto by default, the experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, proposal-generation.ts). |
| P2 Learned changes are validated before they take effect | assessed | 2 |  |  | A | Proposals are scanned before apply (src/skills/workshop/proposal-scan.ts), and evaluator hooks can compare against the baseline and block, but no evaluator ships (none in extensions/). |
| L1 Verification surface | assessed | 3 |  |  | A | Health monitor, status commands with JSON output, and a diagnostics export with sanitised status and health snapshots and the configuration shape (docs/gateway/health.md:13-65). |
| L2 Environment reproducibility | assessed | 2 | 3 |  | A | Docker, Fly and Render deployment definitions (fly.toml, render.yaml, deploy/) and CI test boxes (.github/workflows/ci-check-testbox.yml); no per-change ephemeral environment with seeded data. |
| L3 Machine verifiability | assessed | 3 |  |  | A | Live and E2E checks across channels and apps (.github/workflows/openclaw-live-and-e2e-checks-reusable.yml), and a maturity scorecard generated from a taxonomy and QA evidence covering 280 capability areas (docs/maturity/scorecard.md, taxonomy.yaml, qa/). |

