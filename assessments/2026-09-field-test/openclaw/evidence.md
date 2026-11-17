# OpenClaw evidence

Read at github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Skills, memory, workshop state (SQLite) and configuration on disk.
- **schema_changes**: true. The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration.
- **multi_tenant**: false. Re-checked under the v0.7 definition: one gateway is one trust domain; session ownership and roles are "collaboration guardrails inside the boundary, not isolation between adversaries", and mutually untrusted people or organisations are told to run one gateway per tenant (docs/start/teams.md, "One trust boundary"). Agent workspaces belong to the same operator, so they are not self-administering groups.
- **hosted_service**: false. A personal gateway daemon, not a multi-user service.
- **machine_actions**: true. Agent tools and the gateway API change skills, configuration and channels.
- **agent_mutations**: true. The experience review writes skills after runs (src/skills/workshop/experience-review.ts:122-275); the weekly collection review edits the skill collection (src/cron/skill-collection-review-monitor.ts); dreaming promotes memory into MEMORY.md (docs/concepts/dreaming.md, on by default); the system agent proposes configuration and plugin changes (src/agents/tools/system-agent-tool.ts).
- **evolution_auto_apply**: true. autonomous.mode auto and approvalPolicy auto are the defaults (src/skills/workshop/config.ts:15-20).
- **definition_change_path**: true. Skills, memory and configuration are its definitions.
- **code_release_path**: true. Changed to true for v0.7 (tightened definition: plugins or scripts the product's own AI writes and activates). The system agent activates task-authored plugin code packed with `openclaw plugins pack`: plugin_activate_artifact retains and reviews the exact archive and, on approval, installs its trusted backend code (src/system-agent/plugin-artifact.ts, src/system-agent/assistant-prompts.ts:159-160, src/agents/tools/system-agent-tool.ts). The September reading (skills only) predates this definition; the second rater counted the same path.
- **ai_features**: true. The product is an LLM agent.
- **ai_data_access**: true. Reads memory, sessions and workspace files (src/memory, src/context-engine).
- **ai_actions**: true. Runs commands, sends channel messages and changes skills (src/agents, src/skills).

## Kinds of change

- **What the assistant knows how to do (skills)** (`skills`, main, made by the person running the assistant): reach **2 Drafted**, confidence high. The product drafts skills: /learn stages a pending proposal for the person to apply (src/skills/workshop/learn-prompt.ts:23-34), and the experience review writes skills from observed runs (experience-review.ts). People also apply, reject or quarantine proposals (src/cli/skills-cli.ts:877-1135). Undo: skill collections are backed up and restored or rolled back by revision hash (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts). Reach 2, not 3: DEL-04 is 2, and nothing checks and stages a skill change end to end for approval by default.
- **What the assistant remembers and how it presents itself** (`memory-persona`, main, made by the person running the assistant): reach **0 Engineers only**, confidence medium. Memory and persona files (MEMORY.md, SOUL.md, AGENTS.md in the workspace) change in chat and through dreaming, which is on by default (docs/concepts/dreaming.md). No supported undo: the workspace is only `git init`-ed at creation and never committed (src/agents/workspace.ts:682-708); dreaming keeps MEMORY.md preimages in plugin state but offers no restore command; `memory forget` deletes by source session, it does not revert (docs/cli/memory.md). Reach 0 because the path has no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **Which models, providers and chat channels it uses** (`models-channels`, main, made by the person running the assistant): reach **2 Drafted**, confidence medium. Models and providers are selected, and channels connected and disconnected, through onboarding, the Control UI and the validated `openclaw config set|unset` (src/cli/config-cli.ts:330-479). The system agent drafts each such change as a pending proposal that the person approves before it applies, then checks it with the config validator (src/system-agent/assistant-prompts.ts:159-161, src/agents/tools/system-agent-tool.ts). Undo: re-selecting the previous model or disconnecting the channel through the same path; wider configuration edits keep no operator-visible earlier version (five rotating backups serve only automatic recovery, src/config/backup-rotation.ts). Reach 2 rests on DEL-04 2. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **What the assistant may do and who may instruct it** (`tool-permissions`, not main, made by the person running the assistant): reach **1 Self-serve**, confidence medium. Exec allowlist entries are added and removed with `openclaw approvals` and exec policy commands (src/cli/exec-approvals-cli.ts, exec-policy-cli.ts), and senders are paired and revoked with `openclaw pairing` (src/pairing). Undo is removing the entry or revoking the pairing; there is no history of earlier policy versions (GOV-05 inventory: configuration 2). Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **Scheduled and recurring tasks** (`scheduled-jobs`, not main, made by the person running the assistant): reach **1 Self-serve**, confidence low. Jobs are created, edited, paused and removed through `openclaw automations add|edit|remove` and the agent's cron tool (docs/cli/cron.md, src/agents/tools/cron-tool.ts), with no deploy. Undo is by disabling or removing the job; edits keep no earlier version (src/cron/config-revision.ts is a concurrency token only), so an edit is undone only by editing it back.
- **Add-ons for new channels, tools and providers** (`plugins`, not main, made by the person running the assistant): reach **2 Drafted**, confidence medium. People install curated plugins from ClawHub, bundled or official sources and remove them with uninstall (docs/plugins/manage-plugins.md). The agent can write a plugin, pack it with `openclaw plugins pack`, and the system agent proposes activating that exact archive for the person to approve (src/system-agent/plugin-artifact.ts, src/agents/tools/system-agent-tool.ts). Undo is plugin_uninstall. Reach 2 rests on DEL-04 2.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md (145 lines), .agents/skills (maintainer skills such as openclaw-pr-maintainer, autoreview, clawsweeper), .claude/settings.json, and Codex agent steps in CI (.github/workflows/docs-agent.yml:281, dated-todo-sweep.yml:55, maturity-scorecard.yml:596, release-validation-skill-runner.yml:91, openai/codex-action pinned by SHA).
- **Proven, Request → Release**: not evidenced. Searched: Repository at the pinned commit: no operating records of /learn or Workshop proposals being applied in a real deployment (proposal ledgers live in each installation's state database, not in the repository); release notes describe product changes, not the loop.
- **Proven, Issue → Fix**: not evidenced. Searched: Repository at the pinned commit: no experience-review or proposal ledgers, audit exports or incident records from a real installation; QA and maturity evidence (qa/, docs/maturity) are test runs, not operating records.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: Repository at the pinned commit: no records of new capabilities being proposed and launched to a cohort.

Confidence for criteria this migration did not change was assigned at migration to v0.7 from the recorded evidence (high where it names the code path and its tests or exact lines, medium where it names files but not every path, low where it rests on an absence claim or general description); criteria re-read for v0.7 carry the confidence of that re-reading.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **ARC-02 Safe schema and data migrations**: **2** (grade A, confidence medium). The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration; no down steps.

### Scale

- **ARC-03 Horizontal scale of services**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service.
- **ARC-04 Reliable asynchronous work**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **not applicable**. Scope fact multi_tenant is false: A personal assistant per installation; shared gateways carry several people but are not isolated tenants (VISION.md). If counted: 2.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service. If counted: 2.
- **ARC-07 Service objectives defined and monitored**: **not applicable**. Scope fact hosted_service is false: A personal gateway daemon, not a multi-user service.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence medium). Agents can declare model fallbacks (src/agents/agent-scope-config.ts); plugins run in-process, so a 3 is not defensible under the inventory rule.
  - AI-qualified reading: **3** (grade A, confidence medium), facets: implemented, tested. Model fallback attempts and configured provider fallback, tested.
- **ARC-09 Backup, restore and recovery**: **2** (grade A, confidence high), facets: implemented, tested. Corrected for v0.7 from 3 to 2 (second-rating adjudication; both second raters agreed). Backup covers state, configuration, credentials, workspaces, agents and managed skills (src/commands/backup-shared.ts:76), with verification and a restore test that round-trips into a fresh target with a matching inventory (src/commands/backup-restore.test.ts:176), so data, definitions, files and secrets reach 3. Scheduled work reaches 2: cron jobs live in the state database the backup restores, and `openclaw cron list` shows each job's next run, agent and owner (src/cli/cron-cli/shared.ts:493-505); before a run, a job whose owning agent no longer resolves is skipped (src/cron/service.unresolved-owner.test.ts), and a scheduled tool cap is honoured only when its persisted owner session and account match the job's stored owner (src/cron/scheduled-tool-policy.ts:240-258, scheduled-tool-policy.test.ts:44). Those checks compare the job record with itself; nothing re-checks that the creator's current pairing, role or credentials still allow the job, and restore only warns operators to "review pending approvals before resuming the Gateway" (src/commands/backup-restore.ts:22), with no hold on restored jobs. Under the inventory rule the score is the lowest surface, 2.
  - Inventory: data 3, definitions 3, files 3, secrets 3, schedules 2

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **2** (grade A, confidence medium). The /learn command turns a request into requirements and sources and stages a pending skill proposal for review, revising existing Workshop skills before creating new ones (src/skills/workshop/learn-prompt.ts). No acceptance criteria or risk class.
  - Higher reading 3: A pending, reviewed draft that accounts for existing skills approaches level 3.
  - AI-qualified reading: **2** (grade A, confidence medium). /learn turns a request into a pending skill proposal (src/skills/workshop/learn-prompt.ts).
    - Higher reading 3: Close to a specification.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A, confidence medium). Gateway, Control UI and macOS, iOS and Android companion apps are separate deployables with their own release workflows (apps/, .github/workflows/android-release.yml, ios-release-e2e.yml).
- **DEL-03 Module boundaries enforced by tooling**: **3** (grade A, confidence high). Separate TypeScript projects for core, extensions, UI and scripts (tsconfig.core.json, tsconfig.extensions.projects.json) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts).
- **DEL-04 AI implementation lane**: **2** (grade A, confidence medium). By default the autonomous experience review drafts and applies skill proposals (autonomous.mode auto, approvalPolicy auto, src/skills/workshop/config.ts:15-20), under the Workshop's policy, revisions and rollback. Scored at the lower reading under rule 11 because: Changes apply per installation, not across tenants.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A, confidence medium). Experience review drafts and applies skills.
    - Higher reading 3: Autonomous by default.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence high). CI runs on pull requests with CodeQL, dependency audit, E2E and performance checks, but passive draft pull requests are isolated from the main slots (.github/workflows/ci.yml:82-93); no accessibility check.
- **DEL-06 Verification surface**: **3** (grade A, confidence high). Health monitor, status commands with JSON output, and a diagnostics export with sanitised status and health snapshots and the configuration shape (docs/gateway/health.md:13-65).
- **DEL-07 Environment reproducibility**: **2** (grade A, confidence medium). Docker, Fly and Render deployment definitions (fly.toml, render.yaml, deploy/) and CI test boxes (.github/workflows/ci-check-testbox.yml); no per-change ephemeral environment with seeded data.
  - Higher reading 3: CI test boxes are ephemeral per change.
- **DEL-08 Machine verifiability**: **3** (grade A, confidence medium). Live and E2E checks across channels and apps (.github/workflows/openclaw-live-and-e2e-checks-reusable.yml), and a maturity scorecard generated from a taxonomy and QA evidence covering 280 capability areas (docs/maturity/scorecard.md, taxonomy.yaml, qa/).

### Release

- **DEL-09 Staged exposure**: **1** (grade A, confidence low). Skill proposals apply to the whole installation; there are no cohorts.
- **DEL-10 Kill switch**: **2** (grade A, confidence medium). Autonomous mode and individual skills can be switched off in configuration at runtime (src/skills/workshop/config.ts).
- **DEL-11 Release rollback**: **2** (grade A, confidence medium), facets: implemented, tested. Applies from v0.7 because code_release_path is now true. Previous releases can be redeployed with `openclaw update --tag <known-good-version> [--dry-run]` (docs/install/updating/rollback-and-recovery.md:13-55), and the updater retains the previous package during activation (src/infra/package-update-activation-*.ts; src/entry.update-failure.process.test.ts, src/commands/backup-verify-manifest.update-recovery.test.ts; .github/workflows/update-migration.yml). But "downgrading the package does not reverse config or database migrations" (rollback-and-recovery.md:15-19), so data compatibility is not ensured, and an AI-activated plugin artifact is undone by plugin_uninstall, not by a versioned rollback to its previous archive (src/system-agent/plugin-artifact.ts). Agrees with the second rater (2, alternate 3).
  - Higher reading 3: `openclaw update --tag <known-good>` is a previewable managed rollback that checks compatibility, and the updater keeps the previous package and recovers when post-install verification fails, with tests; held at 2 because data compatibility across a release is not ensured.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A, confidence medium). Typed gateway methods with JSON output modes and MCP JSON output (docs/cli/mcp/json-output.md); no OpenAPI or dry-run for gateway mutations.
  - Higher reading 3: The gateway protocol is typed end to end.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Canvas serves agent-authored documents and widgets (src/canvas); Control UI layout is code.
  - Higher reading 3: Canvas is AI-authored, validated UI as data.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A, confidence low). 278 locale files; themes are engineer-managed.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A, confidence medium). Cron jobs, hooks, routing bindings and auto-reply configuration are declared as data (docs/gateway/config-hooks.md, config-automation.md, src/routing, src/auto-reply); no general rules engine with a test mode.
  - Higher reading 3: Routing and automation cover many entities through configuration.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A, confidence low). Inbound webhook hooks trigger agent runs; audit events record runs, messages and tool actions; no outbound subscriptions with retry.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence medium). Hook scripts run in the gateway process; agent tools for non-main sessions run in sandboxes governed by tool policy and elevated mode (docs/gateway/sandboxing.md, sandbox-vs-tool-policy-vs-elevated.md).
  - Higher reading 3: Sandboxing with tool policy isolates agent-written code.

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A, confidence medium). Plugins and extensions for channels, providers, tools and memory through a plugin SDK, declarative skills, hooks and an MCP registry (docs/cli/mcp/registry.md); ClawHub is the skill and plugin registry.
  - Higher reading 4: A versioned registry exists.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A, confidence low). Agent tools can run sandboxed under tool policy; plugins and hooks run in the gateway process with full trust.
  - Higher reading 3: AI-written code runs sandboxed.
- **MAL-15 Developer loop**: **3** (grade A, confidence low). Control UI, doctor, diagnostics export, logs and a QA lab (qa/) let developers validate against a live gateway.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A, confidence medium). Channel plugins map WhatsApp, Telegram, Slack, Discord, Signal and others onto one canonical message model (src/channels); providers map onto one model interface.
- **MAL-17 Connector definition or SDK**: **3** (grade A, confidence medium). The plugin SDK covers channel auth and pairing, inbound and outbound sync and install and configure lifecycle (src/plugin-sdk, custodian-skills/configure-channel).
- **MAL-18 Stable versioned contracts**: **2** (grade A, confidence low). A compatibility layer and doctor migrations keep older configuration working; no public deprecation windows.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **3** (grade A, confidence medium). MCP channel-bridge server exposing channel tools (src/mcp/channel-server.ts, channel-tools.ts), an MCP registry and a typed gateway protocol.
  - AI-qualified reading: **3** (grade A, confidence medium). MCP channel-bridge server and typed gateway protocol (src/mcp).
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **3** (grade A, confidence medium). Users complete tasks conversationally across messaging channels with tool actions; operators configure OpenClaw in natural language through the system agent, which plans one safe command and waits for approval of the pending proposal (src/system-agent/assistant.ts, approval-intent.ts); skills are authored in chat.
  - Higher reading 4: Most operations have conversational equivalents.
  - AI-qualified reading: **3** (grade A, confidence medium). Model-backed conversation across channels; configuration by natural language.
    - Higher reading 4: Broad coverage.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **3** (grade A, confidence high). Audit events for runs, messages and tool actions are written as they happen and are queryable (src/audit/audit-event-queries.ts); a runtime trajectory store records sessions (src/trajectory/runtime-store.sqlite.test.ts).
- **LRN-02 Structured learning signals**: **2** (grade A, confidence medium). Experience-review observations and evaluation findings are stored on the proposal revision they concern and recorded in the append-only proposal event ledger (src/skills/workshop/experience-review*.ts, docs/tools/skill-workshop/proposals.md). Scored at the lower reading under rule 11 because: Observations come from sessions, not from users.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-03 User-issue detection**: **2** (grade A, confidence medium). The experience review observes failed runs and corrections (src/skills/workshop/experience-review.ts).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A, confidence low). Trajectories export for offline analysis; no joined usage, support and delivery models.
  - Higher reading 2: The experience review mines session history continuously.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A, confidence low). openclaw doctor diagnoses configuration and runtime problems; experience review attaches the observed runs to proposals.
  - AI-qualified reading: **1** (grade A, confidence low). The agent explains errors when asked; doctor checks are rule-based.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A, confidence medium). The experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, experience-review.ts, proposal-generation.ts); proposals are evidence-backed but not ranked by expected impact.
  - Higher reading 3: Proposals carry their originating experience as evidence.
  - AI-qualified reading: **2** (grade A, confidence medium). Experience review proposes skills from observed runs.
    - Higher reading 3: Ranked when idle.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **3** (grade A, confidence medium). With autonomous.mode auto by default, the experience review scheduler turns observed runs into skill proposals when the system is idle (src/skills/workshop/experience-review-scheduler.ts, proposal-generation.ts).
  - Higher reading 4: The curator tracks which skills persist.
  - AI-qualified reading: **3** (grade A, confidence medium). Model review of runs drafts skills unprompted by default.
    - Higher reading 4: Autonomous mode.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A, confidence high), **2** with opt-in settings. Re-scored for v0.7 under the tightened boundary (changes the product or its AI makes to its own behaviour). By default (autonomous.mode auto, src/skills/workshop/config.ts:16-23) the experience review edits skill files directly with ls, read, write, edit, apply_patch and exec (src/skills/workshop/maintenance-prompt.ts:1-9, experience-review.ts:248-253, "Direct edits have normal file-tool semantics"), with no scan, lint or evaluation before they take effect; the model is only told to verify its own edits. Other AI-made changes are checked: Workshop proposals are scanned when drafted and before apply, and quarantined on failure (src/skills/workshop/proposal-draft.ts, apply-transition.ts:167-169); dreaming promotes memory only past score, recall and query gates, after removing untrusted or system provenance, and rejects rewrites that lose too many prior entries (docs/concepts/dreaming.md, "Consolidation safety"). No evaluator ships, so nothing compares a learned change with a baseline. Scored 1 because the main default learning path has no check; propose mode routes every learned skill change through the scanned proposal path (available 2). The second and third raters scored 0 and 1.
  - Higher reading 2: Workshop proposals (from /learn, the skill_workshop tool and propose mode) are scanned at draft and again before apply and quarantined on failure, and dreaming gates memory promotion by thresholds, a provenance taint gate and rewrite validation; if those paths are read as the learned-change path, 2.
  - AI-qualified reading: **1** (grade A, confidence high), **2** with opt-in settings. Experience-review skill edits apply with no check by default; Workshop proposals are scanned and dreaming promotions gated (src/skills/workshop/experience-review.ts, proposal-scan.ts, docs/concepts/dreaming.md). Propose mode scans every learned skill change.
    - Higher reading 2: Scans on Workshop proposals and dreaming's gates are automated checks on AI-made changes.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **2** (grade A, confidence medium). Evaluator hooks compare each candidate with the complete baseline skill and store metrics and a pass, revise or block decision on the exact revision (docs/tools/skill-workshop/proposals.md); no evaluator is bundled (none in extensions/) and nothing observes impact after apply.
  - Higher reading 3: Baseline, metric and decision are recorded per proposal once an evaluator is installed.
- **LRN-10 The improvement loop improves itself**: **0** (grade A, confidence medium). The checks that govern self-change are code: the proposal scanner (src/skills/workshop/proposal-scan.ts, src/skills/security/scanner.ts), the Workshop policy (src/skills/workshop/policy.ts), the maintenance and /learn prompts (maintenance-prompt.ts, learn-prompt.ts) and dreaming's gates. Operators can change only a few settings (autonomous.mode, approvalPolicy, maxPending, maxSkillBytes in config.ts; dreaming thresholds) through unversioned configuration, and evaluation exists only as a hook for a plugin, with no evaluation set shipped (docs/tools/skill-workshop/proposals.md, "Plugin evaluation and lifecycle hooks"). Evaluator results are stored on the proposal revision, not against the check; nothing records a wrong pass or turns a failure into a new check. The maturity scorecard (docs/maturity/scorecard.md, .github/workflows/maturity-scorecard.yml) is the team's engineering tooling, not the product's governed path.
  - Higher reading 1: Operators can tune the Workshop policy knobs and install an evaluator plugin with their own evaluation cases, by hand.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A, confidence low). No automated accessibility scanning found for the Control UI or companion apps.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A, confidence medium). Audit event store records agent runs, messages and tool actions with queries and configuration (src/audit/audit-event-types.ts, docs/gateway/audit.md); the Skill Workshop keeps an append-only proposal event ledger (docs/tools/skill-workshop/proposals.md). Configuration changes are not audit events.
  - Higher reading 3: Skill definitions and their approvals are fully audited.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence high). Local-first storage, trajectory export and cleanup (src/trajectory/export.ts, cleanup.ts), and redacted diagnostics export (docs/gateway/health.md:56); not driven by tags.
- **GOV-04 Security as infrastructure**: **3** (grade A, confidence high), facets: implemented, tested. Exec approvals with allowlists, DM pairing, tool policies, sandboxing and a secrets subsystem (docs/tools/exec-approvals.md, src/pairing, src/secrets); CodeQL, dependency audit and security review workflows (.github/workflows/codeql.yml, dependency-audit.yml, security-review.yml).

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence medium). Workshop skill collections are backed up and can be restored or rolled back with revision hashes (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); configuration has rotating backups and recovery (src/config/backup-rotation.ts, recovery-policy.ts) but no operator rollback with diffs. Under the inventory rule a 3 needs every default surface at 3.
  - Inventory: skills 3, configuration 2
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **3** (grade A, confidence medium). Skill changes are typed proposals (PROPOSAL.md with revision hashes) that the agent or a person creates; evaluations are stored on the exact revision and apply revalidates the evaluated tree (docs/tools/skill-workshop/proposals.md, src/skills/workshop/service-propose.ts, service-evaluation.ts); the system agent turns chat into proposals for configuration commands with approval classification (src/system-agent/approval-intent.ts).
  - Higher reading 4: Evidence attaches automatically once an evaluator plugin is installed; none is bundled.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A, confidence high), **3** with opt-in settings. Defaults are autonomous.mode auto and approvalPolicy auto (src/skills/workshop/config.ts:15-20), so proposals apply without a person; evaluator block decisions only exist if an evaluator plugin is installed. Setting approvalPolicy to pending gives a per-class approval policy.
- **GOV-08 Upgrade safety**: **3** (grade A, confidence high). Doctor repairs and migrates configuration (docs/gateway/doctor.md), a compatibility layer (src/compat) and a plugin activation boundary test (src/plugin-activation-boundary.test.ts) around a versioned plugin SDK (src/plugin-sdk).

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **3** (grade A, confidence high). Pairing identities for senders, exec approvals previewing commands, tool policies, sandboxing, idempotency keys on gateway methods (94 non-test files under src/gateway) and audit events for tool actions.
  - AI-qualified reading: **3** (grade A, confidence high). Pairing identities, exec approvals with previews, tool policies and idempotency keys for agent actions.
- **GOV-10 Bounded self-change**: **2** (grade A, confidence medium). Workshop policy limits proposal size and origins (src/skills/workshop/policy.ts, proposal-origin-validation.ts); there is no per-period or blast-radius limit.
  - AI-qualified reading: **2** (grade A, confidence medium). Proposal size and origin limits; no blast-radius limit.
- **GOV-11 Learning-input integrity**: **2** (grade A, confidence medium). Every proposal records its origin agent, session, run and message (src/skills/workshop/proposal-origin-validation.ts) and is scanned before apply (proposal-scan.ts); with approvalPolicy auto, session content alone can drive an applied change.
  - Higher reading 3: Provenance and scanning meet level 3 apart from the default auto-apply.
  - AI-qualified reading: **2** (grade A, confidence medium). Origin recorded and proposals scanned; auto-apply by default.
    - Higher reading 3: Both present.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A, confidence low). Kernel of gateway sessions (conversation), channels (channel), pairing and auth (identity), tool policy (permission), cron, hooks and flows (workflow), and memory and files (content).
- **EXP-02 A new domain is expressible without kernel change**: **3** (grade A, confidence low). About 50 domain skills ship as bundles on an unchanged kernel (skills/: notion, obsidian, github, trello, spotify-player and more), and the agent authors new ones. Scored at the lower reading under rule 11 because: If skills are judged too small to count as domains.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.
- **EXP-03 A domain ships as an installable bundle**: **3** (grade A, confidence medium). Skills are versioned, installable bundles installed through ClawHub and the CLI (skills/clawhub, src/cli/skills-cli.ts).

### Discover

- **EXP-04 Unmet-demand sensing**: **1** (grade A, confidence low). Unserved requests stay in session history.
- **EXP-05 Evidence-backed opportunity proposals**: **1** (grade A, confidence low). Experience review proposes skills for observed tasks, not capabilities nobody has used yet.
  - AI-qualified reading: **1** (grade A, confidence low). Proposes skills for observed tasks only.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A, confidence low). New skills apply to the whole installation at once.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence medium). Memory host, context engine and session memory search assemble context automatically (src/memory, src/context-engine).
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A, confidence high), facets: implemented, tested. A personal agent acting with the owner's permissions; DM pairing restricts who can instruct it, tool policies and exec approvals gate actions, with tests (src/pairing, src/agents/bash-tools.exec-approval-followup.test.ts).

### Quality

- **AIR-05 Offline AI evaluation**: **1** (grade A, confidence low). Evaluator hooks exist for skill proposals but no evaluation set ships.
- **AIR-06 Regression gating before release**: **1** (grade A, confidence low). No evaluation gates in CI.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A, confidence high), facets: implemented, tested. An agent event audit store with typed events and queries (src/audit/agent-event-audit.ts, audit-event-store.ts, audit-event-queries.ts) and session transcripts.

### Operations

- **AIR-01 Model and provider portability and resilience**: **3** (grade A, confidence high). Model fallback with candidate generation and configured provider fallback, with tests (src/agents/model-fallback-attempt.ts, configured-provider-fallback.ts, configured-provider-fallback.test.ts).
- **AIR-02 AI usage and per-customer cost controls**: **2** (grade A, confidence medium). Agent run usage is recorded (src/infra/agent-run-usage.ts); no spend limit per user.
- **AIR-08 Production quality, drift and feedback monitoring**: **1** (grade A, confidence low). Diagnostic events only; no quality or feedback monitoring.
