# OpenClaw evidence

Read at github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **A2 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B3 Machine-readable contract with introspection and dry-run**: **2** (grade A). Typed gateway methods with JSON output modes and MCP JSON output (docs/cli/mcp/json-output.md); no OpenAPI or dry-run for gateway mutations.
  - Alternate reading 3: The gateway protocol is typed end to end.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Canvas serves agent-authored documents and widgets (src/canvas); Control UI layout is code.
  - Alternate reading 3: Canvas is AI-authored, validated UI as data.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). 278 locale files; themes are engineer-managed.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A). Cron jobs, hooks, routing bindings and auto-reply configuration are declared as data (docs/gateway/config-hooks.md, config-automation.md, src/routing, src/auto-reply); no general rules engine with a test mode.
  - Alternate reading 3: Routing and automation cover many entities through configuration.
- **D2 Event model with webhooks or subscriptions and retry**: **2** (grade A). Inbound webhook hooks trigger agent runs; audit events record runs, messages and tool actions; no outbound subscriptions with retry.
- **D3 Sandboxed server-side hooks**: **2** (grade A). Hook scripts run in the gateway process; agent tools for non-main sessions run in sandboxes governed by tool policy and elevated mode (docs/gateway/sandboxing.md, sandbox-vs-tool-policy-vs-elevated.md).
  - Alternate reading 3: Sandboxing with tool policy isolates agent-written code.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). No automated accessibility scanning found for the Control UI or companion apps.
- **E2 Audit generic over entities, definition changes and approvals**: **2** (grade A). Audit event store records agent runs, messages and tool actions with queries and configuration (src/audit/audit-event-types.ts, docs/gateway/audit.md); the Skill Workshop keeps an append-only proposal event ledger (docs/tools/skill-workshop/proposals.md). Configuration changes are not audit events.
  - Alternate reading 3: Skill definitions and their approvals are fully audited.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Local-first storage, trajectory export and cleanup (src/trajectory/export.ts, cleanup.ts), and redacted diagnostics export (docs/gateway/health.md:56); not driven by tags.
- **E4 Security as infrastructure**: **3** (grade A). Exec approvals with allowlists, DM pairing, tool policies, sandboxing and a secrets subsystem (docs/tools/exec-approvals.md, src/pairing, src/secrets); CodeQL, dependency audit and security review workflows (.github/workflows/codeql.yml, dependency-audit.yml, security-review.yml).
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **3** (grade A). Workshop collections are backed up and can be restored or rolled back (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); proposal revisions carry hashes (revision-hash.ts); state snapshots to git (src/snapshot/git-backup.ts).
  - Alternate reading 4: Revisions are addressable and link to evaluations.
- **F2 Proposal, review, apply as a first-class object with preview**: **3** (grade A). Skill changes are typed proposals (PROPOSAL.md with revision hashes) that the agent or a person creates; evaluations are stored on the exact revision and apply revalidates the evaluated tree (docs/tools/skill-workshop/proposals.md, src/skills/workshop/service-propose.ts, service-evaluation.ts); the system agent turns chat into proposals for configuration commands with approval classification (src/system-agent/approval-intent.ts).
  - Alternate reading 4: Evidence attaches automatically once an evaluator plugin is installed; none is bundled.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A), **3** with opt-in settings. Defaults are autonomous.mode auto and approvalPolicy auto (src/skills/workshop/config.ts:15-20), so proposals apply without a person; evaluator block decisions only exist if an evaluator plugin is installed. Setting approvalPolicy to pending gives a per-class approval policy.
- **F4 Upgrade safety**: **3** (grade A). Doctor repairs and migrates configuration (docs/gateway/doctor.md), a compatibility layer (src/compat) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts) around a versioned plugin SDK (src/plugin-sdk).
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Personal installs are single-tenant; shared gateways carry several people with per-person credit (VISION.md); no noisy-neighbour detection.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). Performance workflow and test-timing refits in CI (.github/workflows/openclaw-performance.yml, ci-test-timings-refit.yml); no documented per-surface limits.
  - Alternate reading 3: Performance is checked in CI.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **3** (grade A). Gateway, Control UI and macOS, iOS and Android companion apps are separate deployables with their own release workflows (apps/, .github/workflows/android-release.yml, ios-release-e2e.yml).
- **H2 Module boundaries enforced by tooling**: **3** (grade A). Separate TypeScript projects for core, extensions, UI and scripts (tsconfig.core.json, tsconfig.extensions.projects.json) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts).
- **H3 Every change class has an automated pre-land check**: **2** (grade A). CI runs on pull requests with CodeQL, dependency audit, E2E and performance checks, but passive draft pull requests are isolated from the main slots (.github/workflows/ci.yml:82-93); no accessibility check.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Plugins and extensions for channels, providers, tools and memory through a plugin SDK, declarative skills, hooks and an MCP registry (docs/cli/mcp/registry.md); ClawHub is the skill and plugin registry.
  - Alternate reading 4: A versioned registry exists.
- **I2 Runtime isolation and dependency control**: **2** (grade A). Agent tools can run sandboxed under tool policy; plugins and hooks run in the gateway process with full trust.
  - Alternate reading 3: AI-written code runs sandboxed.
- **I3 Developer loop**: **3** (grade A). Control UI, doctor, diagnostics export, logs and a QA lab (qa/) let developers validate against a live gateway.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **3** (grade A). MCP channel-bridge server exposing channel tools (src/mcp/channel-server.ts, channel-tools.ts), an MCP registry and a typed gateway protocol.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). Users complete tasks conversationally across messaging channels with tool actions; operators configure OpenClaw in natural language through the system agent, which plans one safe command and waits for approval of the pending proposal (src/system-agent/assistant.ts, approval-intent.ts); skills are authored in chat.
  - Alternate reading 4: Most operations have conversational equivalents.
- **K3 Agent-safe actions**: **3** (grade A). Pairing identities for senders, exec approvals previewing commands, tool policies, sandboxing, idempotency keys on gateway methods (94 non-test files under src/gateway) and audit events for tool actions.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). Channel plugins map WhatsApp, Telegram, Slack, Discord, Signal and others onto one canonical message model (src/channels); providers map onto one model interface.
- **N2 Connector definition or SDK**: **3** (grade A). The plugin SDK covers channel auth and pairing, inbound and outbound sync and install and configure lifecycle (src/plugin-sdk, custodian-skills/configure-channel).
- **N3 Stable versioned contracts**: **2** (grade A). A compatibility layer and doctor migrations keep older configuration working; no public deprecation windows.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of gateway sessions (conversation), channels (channel), pairing and auth (identity), tool policy (permission), cron, hooks and flows (workflow), and memory and files (content).
- **O2 A new domain is expressible without kernel change**: **4** (grade A). About 50 domain skills ship as bundles on an unchanged kernel (skills/: notion, obsidian, github, trello, spotify-player and more), and the agent authors new ones.
  - Alternate reading 3: If skills are judged too small to count as domains.
- **O3 A domain ships as an installable bundle**: **3** (grade A). Skills are versioned, installable bundles installed through ClawHub and the CLI (skills/clawhub, src/cli/skills-cli.ts).
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). Audit events for runs, messages and tool actions are written as they happen and are queryable (src/audit/audit-event-queries.ts); a runtime trajectory store records sessions (src/trajectory/runtime-store.sqlite.test.ts).
- **J2 Structured learning signals**: **3** (grade A). Experience-review observations and evaluation findings are stored on the proposal revision they concern and recorded in the append-only proposal event ledger (src/skills/workshop/experience-review*.ts, docs/tools/skill-workshop/proposals.md).
  - Alternate reading 2: Observations come from sessions, not from users.
- **J3 Cross-source mining inside the product**: **1** (grade A). Trajectories export for offline analysis; no joined usage, support and delivery models.
  - Alternate reading 2: The experience review mines session history continuously.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **2** (grade A). The experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, experience-review.ts, proposal-generation.ts); proposals are evidence-backed but not ranked by expected impact.
  - Alternate reading 3: Proposals carry their originating experience as evidence.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **3** (grade A). By default the autonomous experience review drafts and applies skill proposals (autonomous.mode auto, approvalPolicy auto, src/skills/workshop/config.ts:15-20), under the Workshop's policy, revisions and rollback.
  - Alternate reading 2: Changes apply per installation, not across tenants.
- **M4 Post-change impact is measured against a declared baseline**: **2** (grade A). Evaluator hooks compare each candidate with the complete baseline skill and store metrics and a pass, revise or block decision on the exact revision (docs/tools/skill-workshop/proposals.md); no evaluator is bundled (none in extensions/) and nothing observes impact after apply.
  - Alternate reading 3: Baseline, metric and decision are recorded per proposal once an evaluator is installed.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **3** (grade A). With autonomous.mode auto by default, the experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, proposal-generation.ts).
  - Alternate reading 4: The curator tracks which skills persist.
- **P2 Learned changes are validated before they take effect**: **2** (grade A). Proposals are scanned before apply (src/skills/workshop/proposal-scan.ts), and evaluator hooks can compare against the baseline and block, but no evaluator ships (none in extensions/).
## L Factory surfaces

- **L1 Verification surface**: **3** (grade A). Health monitor, status commands with JSON output, and a diagnostics export with sanitised status and health snapshots and the configuration shape (docs/gateway/health.md:13-65).
- **L2 Environment reproducibility**: **2** (grade A). Docker, Fly and Render deployment definitions (fly.toml, render.yaml, deploy/) and CI test boxes (.github/workflows/ci-check-testbox.yml); no per-change ephemeral environment with seeded data.
  - Alternate reading 3: CI test boxes are ephemeral per change.
- **L3 Machine verifiability**: **3** (grade A). Live and E2E checks across channels and apps (.github/workflows/openclaw-live-and-e2e-checks-reusable.yml), and a maturity scorecard generated from a taxonomy and QA evidence covering 280 capability areas (docs/maturity/scorecard.md, taxonomy.yaml, qa/).
