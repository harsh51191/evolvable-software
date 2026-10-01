# OpenClaw evidence

Read at github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Skills, memory, workshop state (SQLite) and configuration on disk.
- **schema_changes**: true. The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration.
- **multi_tenant**: false. A personal assistant per installation; shared gateways carry several people but are not isolated tenants (VISION.md).
- **hosted_service**: false. A personal gateway daemon, not a multi-user service.
- **machine_actions**: true. Agent tools and the gateway API change skills, configuration and channels.
- **agent_mutations**: true. The experience review drafts and applies skill proposals (src/skills/workshop/experience-review.ts).
- **evolution_auto_apply**: true. autonomous.mode auto and approvalPolicy auto are the defaults (src/skills/workshop/config.ts:15-20).
- **definition_change_path**: true. Skills, memory and configuration are its definitions.
- **code_release_path**: false. The self-improvement path changes skills, not OpenClaw code.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **ARC-02 Safe schema and data migrations**: **2** (grade A). The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration; no down steps.

### Scale

- **ARC-03 Horizontal scale of services**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service.
- **ARC-04 Reliable asynchronous work**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **not applicable**. Scope fact multi_tenant is false: A personal assistant per installation; shared gateways carry several people but are not isolated tenants (VISION.md). If counted: 2.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service. If counted: 2.
- **ARC-07 Service objectives defined and monitored**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A). Agents can declare model fallbacks (src/agents/agent-scope-config.ts); plugins run in-process, so a 3 is not defensible under the inventory rule.
- **ARC-09 Backup, restore and recovery**: **3** (grade A), facets: implemented, tested. Backup covers state, configuration, credentials, workspaces, agents and managed skills (src/commands/backup-shared.ts:76), with verification, scheduling and a restore test that round-trips into a fresh target with a matching inventory (src/commands/backup-restore.test.ts:176). Private captures are excluded by design. No recovery objectives are stated (level 4).
  - Inventory: data 3, definitions 3, files 3, secrets 3

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **2** (grade A). The /learn command turns a request into requirements and sources and stages a pending skill proposal for review, revising existing Workshop skills before creating new ones (src/skills/workshop/learn-prompt.ts). No acceptance criteria or risk class.
  - Higher reading 3: A pending, reviewed draft that accounts for existing skills approaches level 3.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A). Gateway, Control UI and macOS, iOS and Android companion apps are separate deployables with their own release workflows (apps/, .github/workflows/android-release.yml, ios-release-e2e.yml).
- **DEL-03 Module boundaries enforced by tooling**: **3** (grade A). Separate TypeScript projects for core, extensions, UI and scripts (tsconfig.core.json, tsconfig.extensions.projects.json) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts).
- **DEL-04 AI implementation lane**: **2** (grade A). By default the autonomous experience review drafts and applies skill proposals (autonomous.mode auto, approvalPolicy auto, src/skills/workshop/config.ts:15-20), under the Workshop's policy, revisions and rollback. Scored at the lower reading under rule 11 because: Changes apply per installation, not across tenants.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A). CI runs on pull requests with CodeQL, dependency audit, E2E and performance checks, but passive draft pull requests are isolated from the main slots (.github/workflows/ci.yml:82-93); no accessibility check.
- **DEL-06 Verification surface**: **3** (grade A). Health monitor, status commands with JSON output, and a diagnostics export with sanitised status and health snapshots and the configuration shape (docs/gateway/health.md:13-65).
- **DEL-07 Environment reproducibility**: **2** (grade A). Docker, Fly and Render deployment definitions (fly.toml, render.yaml, deploy/) and CI test boxes (.github/workflows/ci-check-testbox.yml); no per-change ephemeral environment with seeded data.
  - Higher reading 3: CI test boxes are ephemeral per change.
- **DEL-08 Machine verifiability**: **3** (grade A). Live and E2E checks across channels and apps (.github/workflows/openclaw-live-and-e2e-checks-reusable.yml), and a maturity scorecard generated from a taxonomy and QA evidence covering 280 capability areas (docs/maturity/scorecard.md, taxonomy.yaml, qa/).

### Release

- **DEL-09 Staged exposure**: **1** (grade A). Skill proposals apply to the whole installation; there are no cohorts.
- **DEL-10 Kill switch**: **2** (grade A). Autonomous mode and individual skills can be switched off in configuration at runtime (src/skills/workshop/config.ts).
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: The self-improvement path changes skills, not OpenClaw code.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A). Typed gateway methods with JSON output modes and MCP JSON output (docs/cli/mcp/json-output.md); no OpenAPI or dry-run for gateway mutations.
  - Higher reading 3: The gateway protocol is typed end to end.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Canvas serves agent-authored documents and widgets (src/canvas); Control UI layout is code.
  - Higher reading 3: Canvas is AI-authored, validated UI as data.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A). 278 locale files; themes are engineer-managed.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A). Cron jobs, hooks, routing bindings and auto-reply configuration are declared as data (docs/gateway/config-hooks.md, config-automation.md, src/routing, src/auto-reply); no general rules engine with a test mode.
  - Higher reading 3: Routing and automation cover many entities through configuration.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A). Inbound webhook hooks trigger agent runs; audit events record runs, messages and tool actions; no outbound subscriptions with retry.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A). Hook scripts run in the gateway process; agent tools for non-main sessions run in sandboxes governed by tool policy and elevated mode (docs/gateway/sandboxing.md, sandbox-vs-tool-policy-vs-elevated.md).
  - Higher reading 3: Sandboxing with tool policy isolates agent-written code.

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A). Plugins and extensions for channels, providers, tools and memory through a plugin SDK, declarative skills, hooks and an MCP registry (docs/cli/mcp/registry.md); ClawHub is the skill and plugin registry.
  - Higher reading 4: A versioned registry exists.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A). Agent tools can run sandboxed under tool policy; plugins and hooks run in the gateway process with full trust.
  - Higher reading 3: AI-written code runs sandboxed.
- **MAL-15 Developer loop**: **3** (grade A). Control UI, doctor, diagnostics export, logs and a QA lab (qa/) let developers validate against a live gateway.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A). Channel plugins map WhatsApp, Telegram, Slack, Discord, Signal and others onto one canonical message model (src/channels); providers map onto one model interface.
- **MAL-17 Connector definition or SDK**: **3** (grade A). The plugin SDK covers channel auth and pairing, inbound and outbound sync and install and configure lifecycle (src/plugin-sdk, custodian-skills/configure-channel).
- **MAL-18 Stable versioned contracts**: **2** (grade A). A compatibility layer and doctor migrations keep older configuration working; no public deprecation windows.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **3** (grade A). MCP channel-bridge server exposing channel tools (src/mcp/channel-server.ts, channel-tools.ts), an MCP registry and a typed gateway protocol.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). Users complete tasks conversationally across messaging channels with tool actions; operators configure OpenClaw in natural language through the system agent, which plans one safe command and waits for approval of the pending proposal (src/system-agent/assistant.ts, approval-intent.ts); skills are authored in chat.
  - Higher reading 4: Most operations have conversational equivalents.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **3** (grade A). Audit events for runs, messages and tool actions are written as they happen and are queryable (src/audit/audit-event-queries.ts); a runtime trajectory store records sessions (src/trajectory/runtime-store.sqlite.test.ts).
- **LRN-02 Structured learning signals**: **2** (grade A). Experience-review observations and evaluation findings are stored on the proposal revision they concern and recorded in the append-only proposal event ledger (src/skills/workshop/experience-review*.ts, docs/tools/skill-workshop/proposals.md). Scored at the lower reading under rule 11 because: Observations come from sessions, not from users.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-03 User-issue detection**: **2** (grade A). The experience review observes failed runs and corrections (src/skills/workshop/experience-review.ts).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A). Trajectories export for offline analysis; no joined usage, support and delivery models.
  - Higher reading 2: The experience review mines session history continuously.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A). openclaw doctor diagnoses configuration and runtime problems; experience review attaches the observed runs to proposals.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A). The experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, experience-review.ts, proposal-generation.ts); proposals are evidence-backed but not ranked by expected impact.
  - Higher reading 3: Proposals carry their originating experience as evidence.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **3** (grade A). With autonomous.mode auto by default, the experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, proposal-generation.ts).
  - Higher reading 4: The curator tracks which skills persist.
- **LRN-08 Learned changes are validated before they take effect**: **2** (grade A). Proposals are scanned before apply (src/skills/workshop/proposal-scan.ts), and evaluator hooks can compare against the baseline and block, but no evaluator ships (none in extensions/).

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **2** (grade A). Evaluator hooks compare each candidate with the complete baseline skill and store metrics and a pass, revise or block decision on the exact revision (docs/tools/skill-workshop/proposals.md); no evaluator is bundled (none in extensions/) and nothing observes impact after apply.
  - Higher reading 3: Baseline, metric and decision are recorded per proposal once an evaluator is installed.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). No automated accessibility scanning found for the Control UI or companion apps.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A). Audit event store records agent runs, messages and tool actions with queries and configuration (src/audit/audit-event-types.ts, docs/gateway/audit.md); the Skill Workshop keeps an append-only proposal event ledger (docs/tools/skill-workshop/proposals.md). Configuration changes are not audit events.
  - Higher reading 3: Skill definitions and their approvals are fully audited.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Local-first storage, trajectory export and cleanup (src/trajectory/export.ts, cleanup.ts), and redacted diagnostics export (docs/gateway/health.md:56); not driven by tags.
- **GOV-04 Security as infrastructure**: **3** (grade A), facets: implemented, tested. Exec approvals with allowlists, DM pairing, tool policies, sandboxing and a secrets subsystem (docs/tools/exec-approvals.md, src/pairing, src/secrets); CodeQL, dependency audit and security review workflows (.github/workflows/codeql.yml, dependency-audit.yml, security-review.yml).

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A). Workshop skill collections are backed up and can be restored or rolled back with revision hashes (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); configuration has rotating backups and recovery (src/config/backup-rotation.ts, recovery-policy.ts) but no operator rollback with diffs. Under the inventory rule a 3 needs every default surface at 3.
  - Inventory: skills 3, configuration 2
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **3** (grade A). Skill changes are typed proposals (PROPOSAL.md with revision hashes) that the agent or a person creates; evaluations are stored on the exact revision and apply revalidates the evaluated tree (docs/tools/skill-workshop/proposals.md, src/skills/workshop/service-propose.ts, service-evaluation.ts); the system agent turns chat into proposals for configuration commands with approval classification (src/system-agent/approval-intent.ts).
  - Higher reading 4: Evidence attaches automatically once an evaluator plugin is installed; none is bundled.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A), **3** with opt-in settings. Defaults are autonomous.mode auto and approvalPolicy auto (src/skills/workshop/config.ts:15-20), so proposals apply without a person; evaluator block decisions only exist if an evaluator plugin is installed. Setting approvalPolicy to pending gives a per-class approval policy.
- **GOV-08 Upgrade safety**: **3** (grade A). Doctor repairs and migrates configuration (docs/gateway/doctor.md), a compatibility layer (src/compat) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts) around a versioned plugin SDK (src/plugin-sdk).

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **3** (grade A). Pairing identities for senders, exec approvals previewing commands, tool policies, sandboxing, idempotency keys on gateway methods (94 non-test files under src/gateway) and audit events for tool actions.
- **GOV-10 Bounded self-change**: **2** (grade A). Workshop policy limits proposal size and origins (src/skills/workshop/policy.ts, proposal-origin-validation.ts); there is no per-period or blast-radius limit.
- **GOV-11 Learning-input integrity**: **2** (grade A). Every proposal records its origin agent, session, run and message (src/skills/workshop/proposal-origin-validation.ts) and is scanned before apply (proposal-scan.ts); with approvalPolicy auto, session content alone can drive an applied change.
  - Higher reading 3: Provenance and scanning meet level 3 apart from the default auto-apply.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of gateway sessions (conversation), channels (channel), pairing and auth (identity), tool policy (permission), cron, hooks and flows (workflow), and memory and files (content).
- **EXP-02 A new domain is expressible without kernel change**: **3** (grade A). About 50 domain skills ship as bundles on an unchanged kernel (skills/: notion, obsidian, github, trello, spotify-player and more), and the agent authors new ones. Scored at the lower reading under rule 11 because: If skills are judged too small to count as domains.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.
- **EXP-03 A domain ships as an installable bundle**: **3** (grade A). Skills are versioned, installable bundles installed through ClawHub and the CLI (skills/clawhub, src/cli/skills-cli.ts).

### Discover

- **EXP-04 Unmet-demand sensing**: **1** (grade A). Unserved requests stay in session history.
- **EXP-05 Evidence-backed opportunity proposals**: **1** (grade A). Experience review proposes skills for observed tasks, not capabilities nobody has used yet.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A). New skills apply to the whole installation at once.
