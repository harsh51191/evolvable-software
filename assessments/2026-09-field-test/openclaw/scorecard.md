# OpenClaw: EVOLVE v0.5 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.5.0 in this repository.

Scope: the openclaw monorepo (gateway, agents, channels, skills and Skill Workshop, plugins and extensions, MCP, Control UI, companion apps, QA and CI). ClawHub (separate repository) and team.openclaw.ai operations are out of scope.

## Reading

**SAL 2**, joint highest. /learn turns a request into a pending skill proposal (DEL-01 2), and the experience review drafts and applies skills from observed runs (LRN-07 3), so both core loops reach L2. Backup and restore are verified and tested across state, configuration, credentials and skills (ARC-09 3). **Blocks L3:** configuration has only rotating backups, not operator rollback (GOV-05 2, inventory); skill changes have no staged exposure (DEL-09 1); the default auto-apply has no declared blast-radius limit (GOV-10 2).

## Limits

Repository evidence only, main at the tip named above. ClawHub (registry and scanning) is a separate repository. No evaluator plugin is bundled, so measurement depends on third-party or user plugins. The experience review was read from code and tests, not run. Single rater.

---
Framework EVOLVE 0.5.0. Date 2026-09-30. Source github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main). Archetype **agent-runtime**.

Scope facts true: persistent_data, schema_changes, machine_actions, agent_mutations, evolution_auto_apply, definition_change_path, ai_features, ai_data_access, ai_actions. False: multi_tenant, hosted_service, code_release_path.

Coverage: 61 assessed, 0 not evidenced, 13 not applicable. Grades: 61 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 2 (Assisted) · Request → Release L2 · Issue → Fix L2 · Opportunity → Expansion L1**

Progress toward the next level: Request → Release 12 of 19 conditions for L3; Issue → Fix 13 of 21 conditions for L3; Opportunity → Expansion 3 of 5 conditions for L2.

- With opt-in settings: SAL 2 (Assisted) · Request → Release L2 · Issue → Fix L2 · Opportunity → Expansion L1.
- With every alternate reading: SAL 2 (Assisted) · Request → Release L2 · Issue → Fix L2 · Opportunity → Expansion L1.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | L2 | L2 | L2 | L2 | **L2** | L2 |
| Issue → Fix | L2 | L2 | L2 | L2 | **L2** | L2 |
| Opportunity → Expansion | L1 | L2 | L2 | L2 | **L1** | L1 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 3 | pass |
| Tenant isolation | ARC-05 ≥ 3 | n/a | n/a |
| Security as infrastructure | GOV-04 ≥ 3 | 3 | pass |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 2 | fail |

### What blocks the next level

- **Request → Release to L3**: spine Build needs product build path ≥ 3 (has DEL-04 2); spine Verify needs DEL-05 ≥ 3 (has 2); spine Stage needs DEL-09 ≥ 2 (has 1); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Intake needs DEL-01 ≥ 3 (has 2); architecture Foundation needs ARC-02 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 2)
- **Issue → Fix to L3**: spine Verify needs DEL-05 ≥ 3 (has 2); spine Stage needs DEL-09 ≥ 2 (has 1); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Detect needs LRN-03 ≥ 3 (has 2); stages Diagnose needs LRN-05 ≥ 3 (has 2); stages Propose needs LRN-06 ≥ 3 (has 2); architecture Foundation needs ARC-02 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 2)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 1); stages Propose needs EXP-05 ≥ 2 (has 1)

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: DEL-01, DEL-04, DEL-05, LRN-03, LRN-05, LRN-06, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 2.3 | 2.3 | 2.3 | 2.3 | 2.0 |
| Velocity (DEL) | 2.2 | 2.2–2.6 | 2.2 | 2.2 | 2.2 |
| Open (MAL) | 2.4 | 2.4–2.9 | 2.4 | 2.4 | 2.0 |
| Learn (LRN) | 2.1 | 2.1–2.8 | 2.1 | 2.1 | 2.1 |
| Vet (GOV) | 2.3 | 2.3–2.6 | 2.4 | 2.3 | 2.3 |
| Expand (EXP) | 1.7 | 1.7–1.8 | 1.7 | 1.7 | 1.7 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 2 · not production-governed**

- With opt-in settings: AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 2 · not production-governed.
- With every alternate reading: AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 2 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 3 | AIR-03 3, AIR-04 3 |
| Quality | 1 | AIR-05 1, AIR-06 1 |
| Governance | 2 | AIR-07 3, GOV-09 (AI) 3, GOV-10 (AI) 2, GOV-11 (AI) 2, LRN-08 (AI) 2 |
| Operations | 2 | AIR-01 3, AIR-02 2, AIR-08 1, ARC-08 (AI) 3 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 3 | pass |
| Regression evaluation before release | AIR-06 ≥ 3 | 1 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 3 | pass |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 3 | MAL-19 3, MAL-20 3 |
| Build | 2 | DEL-01 2, DEL-04 2 |
| Diagnose and improve | 2 | LRN-05 1, LRN-06 2, LRN-07 3, LRN-08 2 |
| Expand | 1 | EXP-05 1 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Resilience | 2.5 |
| DEL Intake | 2.0 |
| DEL Build | 2.7 |
| DEL Verify | 2.5 |
| DEL Release | 1.5 |
| MAL APIs | 2.0 |
| MAL Interface | 2.0 |
| MAL Behaviour | 2.0 |
| MAL Extensions | 2.7 |
| MAL Integrations | 2.7 |
| MAL Agent interface | 3.0 |
| LRN Sense | 2.0 |
| LRN Diagnose and propose | 2.0 |
| LRN Learn from experience | 2.5 |
| LRN Measure | 2.0 |
| GOV Compliance and security | 2.0 |
| GOV Change control | 2.5 |
| GOV AI and self-change safety | 2.3 |
| EXP Expressible | 3.0 |
| EXP Discover | 1.0 |
| EXP Launch | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - |  | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| ARC-02 Safe schema and data migrations | assessed | 2 |  |  | A |  | The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration; no down steps. |
| ARC-03 Horizontal scale of services | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service. |
| ARC-04 Reliable asynchronous work | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service. |
| ARC-05 Tenant isolation and noisy-neighbour controls | not_applicable | excluded |  |  | - |  | Scope fact multi_tenant is false: A personal assistant per installation; shared gateways carry several people but are not isolated tenants (VISION.md). |
| ARC-06 Ceilings measured, not discovered in incidents | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service. |
| ARC-07 Service objectives defined and monitored | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | AI-qualified reading: 3. Agents can declare model fallbacks (src/agents/agent-scope-config.ts); plugins run in-process, so a 3 is not defensible under the inventory rule. |
| ARC-09 Backup, restore and recovery | assessed | 3 |  |  | A | IT | Inventory: data 3, definitions 3, files 3, secrets 3. Backup covers state, configuration, credentials, workspaces, agents and managed skills (src/commands/backup-shared.ts:76), with verification, scheduling and a restore test that round-trips into a fresh target with a matching inventory (src/commands/backup-restore.test.ts:176). Private captures are excluded by design. No recovery objectives are stated (level 4). |
| DEL-01 Request intake into a structured change specification | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. The /learn command turns a request into requirements and sources and stages a pending skill proposal for review, revising existing Workshop skills before creating new ones (src/skills/workshop/learn-prompt.ts). No acceptance criteria or risk class. |
| DEL-02 Layers deploy independently | assessed | 3 |  |  | A |  | Gateway, Control UI and macOS, iOS and Android companion apps are separate deployables with their own release workflows (apps/, .github/workflows/android-release.yml, ios-release-e2e.yml). |
| DEL-03 Module boundaries enforced by tooling | assessed | 3 |  |  | A |  | Separate TypeScript projects for core, extensions, UI and scripts (tsconfig.core.json, tsconfig.extensions.projects.json) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts). |
| DEL-04 AI implementation lane | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. By default the autonomous experience review drafts and applies skill proposals (autonomous.mode auto, approvalPolicy auto, src/skills/workshop/config.ts:15-20), under the Workshop's policy, revisions and rollback. Scored at the lower reading under rule 11 because: Changes apply per installation, not across tenants. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A |  | CI runs on pull requests with CodeQL, dependency audit, E2E and performance checks, but passive draft pull requests are isolated from the main slots (.github/workflows/ci.yml:82-93); no accessibility check. |
| DEL-06 Verification surface | assessed | 3 |  |  | A |  | Health monitor, status commands with JSON output, and a diagnostics export with sanitised status and health snapshots and the configuration shape (docs/gateway/health.md:13-65). |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A |  | Docker, Fly and Render deployment definitions (fly.toml, render.yaml, deploy/) and CI test boxes (.github/workflows/ci-check-testbox.yml); no per-change ephemeral environment with seeded data. |
| DEL-08 Machine verifiability | assessed | 3 |  |  | A |  | Live and E2E checks across channels and apps (.github/workflows/openclaw-live-and-e2e-checks-reusable.yml), and a maturity scorecard generated from a taxonomy and QA evidence covering 280 capability areas (docs/maturity/scorecard.md, taxonomy.yaml, qa/). |
| DEL-09 Staged exposure | assessed | 1 |  |  | A |  | Skill proposals apply to the whole installation; there are no cohorts. |
| DEL-10 Kill switch | assessed | 2 |  |  | A |  | Autonomous mode and individual skills can be switched off in configuration at runtime (src/skills/workshop/config.ts). |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: The self-improvement path changes skills, not OpenClaw code. |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-02 Field definitions carry type and validation | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 | 3 |  | A |  | Typed gateway methods with JSON output modes and MCP JSON output (docs/cli/mcp/json-output.md); no OpenAPI or dry-run for gateway mutations. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A |  | Canvas serves agent-authored documents and widgets (src/canvas); Control UI layout is code. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A |  | 278 locale files; themes are engineer-managed. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 | 3 |  | A |  | Cron jobs, hooks, routing bindings and auto-reply configuration are declared as data (docs/gateway/config-hooks.md, config-automation.md, src/routing, src/auto-reply); no general rules engine with a test mode. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A |  | Inbound webhook hooks trigger agent runs; audit events record runs, messages and tool actions; no outbound subscriptions with retry. |
| MAL-12 Sandboxed server-side hooks | assessed | 2 | 3 |  | A |  | Hook scripts run in the gateway process; agent tools for non-main sessions run in sandboxes governed by tool policy and elevated mode (docs/gateway/sandboxing.md, sandbox-vs-tool-policy-vs-elevated.md). |
| MAL-13 Plugin lane breadth | assessed | 3 | 4 |  | A |  | Plugins and extensions for channels, providers, tools and memory through a plugin SDK, declarative skills, hooks and an MCP registry (docs/cli/mcp/registry.md); ClawHub is the skill and plugin registry. |
| MAL-14 Runtime isolation and dependency control | assessed | 2 | 3 |  | A |  | Agent tools can run sandboxed under tool policy; plugins and hooks run in the gateway process with full trust. |
| MAL-15 Developer loop | assessed | 3 |  |  | A |  | Control UI, doctor, diagnostics export, logs and a QA lab (qa/) let developers validate against a live gateway. |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A |  | Channel plugins map WhatsApp, Telegram, Slack, Discord, Signal and others onto one canonical message model (src/channels); providers map onto one model interface. |
| MAL-17 Connector definition or SDK | assessed | 3 |  |  | A |  | The plugin SDK covers channel auth and pairing, inbound and outbound sync and install and configure lifecycle (src/plugin-sdk, custodian-skills/configure-channel). |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A |  | A compatibility layer and doctor migrations keep older configuration working; no public deprecation windows. |
| MAL-19 Machine-readable capability surface for agents | assessed | 3 |  |  | A |  | AI-qualified reading: 3. MCP channel-bridge server exposing channel tools (src/mcp/channel-server.ts, channel-tools.ts), an MCP registry and a typed gateway protocol. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A |  | AI-qualified reading: 3. Users complete tasks conversationally across messaging channels with tool actions; operators configure OpenClaw in natural language through the system agent, which plans one safe command and waits for approval of the pending proposal (src/system-agent/assistant.ts, approval-intent.ts); skills are authored in chat. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A |  | Audit events for runs, messages and tool actions are written as they happen and are queryable (src/audit/audit-event-queries.ts); a runtime trajectory store records sessions (src/trajectory/runtime-store.sqlite.test.ts). |
| LRN-02 Structured learning signals | assessed | 2 | 3 |  | A |  | Experience-review observations and evaluation findings are stored on the proposal revision they concern and recorded in the append-only proposal event ledger (src/skills/workshop/experience-review*.ts, docs/tools/skill-workshop/proposals.md). Scored at the lower reading under rule 11 because: Observations come from sessions, not from users. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A |  | The experience review observes failed runs and corrections (src/skills/workshop/experience-review.ts). |
| LRN-04 Cross-source mining inside the product | assessed | 1 | 2 |  | A |  | Trajectories export for offline analysis; no joined usage, support and delivery models. |
| LRN-05 Automated diagnosis | assessed | 2 |  |  | A |  | AI-qualified reading: 1. openclaw doctor diagnoses configuration and runtime problems; experience review attaches the observed runs to proposals. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. The experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, experience-review.ts, proposal-generation.ts); proposals are evidence-backed but not ranked by expected impact. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 3 | 4 |  | A |  | AI-qualified reading: 3. With autonomous.mode auto by default, the experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, proposal-generation.ts). |
| LRN-08 Learned changes are validated before they take effect | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Proposals are scanned before apply (src/skills/workshop/proposal-scan.ts), and evaluator hooks can compare against the baseline and block, but no evaluator ships (none in extensions/). |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A |  | Evaluator hooks compare each candidate with the complete baseline skill and store metrics and a pass, revise or block decision on the exact revision (docs/tools/skill-workshop/proposals.md); no evaluator is bundled (none in extensions/) and nothing observes impact after apply. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 |  |  | A |  | No automated accessibility scanning found for the Control UI or companion apps. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A |  | Audit event store records agent runs, messages and tool actions with queries and configuration (src/audit/audit-event-types.ts, docs/gateway/audit.md); the Skill Workshop keeps an append-only proposal event ledger (docs/tools/skill-workshop/proposals.md). Configuration changes are not audit events. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A |  | Local-first storage, trajectory export and cleanup (src/trajectory/export.ts, cleanup.ts), and redacted diagnostics export (docs/gateway/health.md:56); not driven by tags. |
| GOV-04 Security as infrastructure | assessed | 3 |  |  | A | IT | Exec approvals with allowlists, DM pairing, tool policies, sandboxing and a secrets subsystem (docs/tools/exec-approvals.md, src/pairing, src/secrets); CodeQL, dependency audit and security review workflows (.github/workflows/codeql.yml, dependency-audit.yml, security-review.yml). |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A |  | Inventory: skills 3, configuration 2. Workshop skill collections are backed up and can be restored or rolled back with revision hashes (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); configuration has rotating backups and recovery (src/config/backup-rotation.ts, recovery-policy.ts) but no operator rollback with diffs. Under the inventory rule a 3 needs every default surface at 3. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 3 | 4 |  | A |  | Skill changes are typed proposals (PROPOSAL.md with revision hashes) that the agent or a person creates; evaluations are stored on the exact revision and apply revalidates the evaluated tree (docs/tools/skill-workshop/proposals.md, src/skills/workshop/service-propose.ts, service-evaluation.ts); the system agent turns chat into proposals for configuration commands with approval classification (src/system-agent/approval-intent.ts). |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 |  | 3 | A |  | Defaults are autonomous.mode auto and approvalPolicy auto (src/skills/workshop/config.ts:15-20), so proposals apply without a person; evaluator block decisions only exist if an evaluator plugin is installed. Setting approvalPolicy to pending gives a per-class approval policy. |
| GOV-08 Upgrade safety | assessed | 3 |  |  | A |  | Doctor repairs and migrates configuration (docs/gateway/doctor.md), a compatibility layer (src/compat) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts) around a versioned plugin SDK (src/plugin-sdk). |
| GOV-09 Agent-safe actions | assessed | 3 |  |  | A |  | AI-qualified reading: 3. Pairing identities for senders, exec approvals previewing commands, tool policies, sandboxing, idempotency keys on gateway methods (94 non-test files under src/gateway) and audit events for tool actions. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Workshop policy limits proposal size and origins (src/skills/workshop/policy.ts, proposal-origin-validation.ts); there is no per-period or blast-radius limit. |
| GOV-11 Learning-input integrity | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. Every proposal records its origin agent, session, run and message (src/skills/workshop/proposal-origin-validation.ts) and is scanned before apply (proposal-scan.ts); with approvalPolicy auto, session content alone can drive an applied change. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 |  |  | A |  | Kernel of gateway sessions (conversation), channels (channel), pairing and auth (identity), tool policy (permission), cron, hooks and flows (workflow), and memory and files (content). |
| EXP-02 A new domain is expressible without kernel change | assessed | 3 | 4 |  | A |  | About 50 domain skills ship as bundles on an unchanged kernel (skills/: notion, obsidian, github, trello, spotify-player and more), and the agent authors new ones. Scored at the lower reading under rule 11 because: If skills are judged too small to count as domains. |
| EXP-03 A domain ships as an installable bundle | assessed | 3 |  |  | A |  | Skills are versioned, installable bundles installed through ClawHub and the CLI (skills/clawhub, src/cli/skills-cli.ts). |
| EXP-04 Unmet-demand sensing | assessed | 1 |  |  | A |  | Unserved requests stay in session history. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 1 |  |  | A |  | AI-qualified reading: 1. Experience review proposes skills for observed tasks, not capabilities nobody has used yet. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 |  |  | A |  | New skills apply to the whole installation at once. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A |  | Memory host, context engine and session memory search assemble context automatically (src/memory, src/context-engine). |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 3 |  |  | A | IT | A personal agent acting with the owner's permissions; DM pairing restricts who can instruct it, tool policies and exec approvals gate actions, with tests (src/pairing, src/agents/bash-tools.exec-approval-followup.test.ts). |
| AIR-05 Offline AI evaluation | assessed | 1 |  |  | A |  | Evaluator hooks exist for skill proposals but no evaluation set ships. |
| AIR-06 Regression gating before release | assessed | 1 |  |  | A |  | No evaluation gates in CI. |
| AIR-07 AI action tracing and auditability | assessed | 3 |  |  | A | IT | An agent event audit store with typed events and queries (src/audit/agent-event-audit.ts, audit-event-store.ts, audit-event-queries.ts) and session transcripts. |
| AIR-01 Model and provider portability and resilience | assessed | 3 |  |  | A |  | Model fallback with candidate generation and configured provider fallback, with tests (src/agents/model-fallback-attempt.ts, configured-provider-fallback.ts, configured-provider-fallback.test.ts). |
| AIR-02 AI usage and per-customer cost controls | assessed | 2 |  |  | A |  | Agent run usage is recorded (src/infra/agent-run-usage.ts); no spend limit per user. |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 1 |  |  | A |  | Diagnostic events only; no quality or feedback monitoring. |

Facets: I implemented, T tested, O operated.

