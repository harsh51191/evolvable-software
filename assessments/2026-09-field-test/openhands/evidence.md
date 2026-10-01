# OpenHands (Agent Canvas + software-agent-sdk) evidence

Read at github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. The Automation Service keeps automations, runs and a key-value store in PostgreSQL (automation repository, migrations/versions).
- **schema_changes**: true. Alembic migrations in the Automation Service (migrations/versions, 29 files).
- **multi_tenant**: true. The Automation Service serves organisations with org-scoped data (migrations/versions/023_org_scoped_git_sync.py).
- **hosted_service**: true. The Automation Service and Agent Server run as long-lived services for OpenHands Cloud.
- **machine_actions**: true. The Agent Server and Automation Service APIs create and run automations with per-user API keys (automation repository: openhands/automation/auth.py).
- **agent_mutations**: false. Agents change users' repositories, not OpenHands' own definitions.
- **evolution_auto_apply**: false. Nothing changes OpenHands' own definitions automatically.
- **definition_change_path**: true. Automations, skills and settings are definitions.
- **code_release_path**: false. Automations act on users' repositories; no first-party lane ships OpenHands code changes.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 0.
- **ARC-02 Safe schema and data migrations**: **2** (grade A), facets: implemented, tested. Alembic migrations with downgrade steps, and a test of the migration history (automation repository: migrations/versions, tests/test_migration_history.py); no enforced online strategy.
  - Higher reading 3: Migration history is tested in CI.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A). The Automation Service is a stateless FastAPI app over PostgreSQL and object storage; the canvas ships a Helm chart (helm/agent-canvas).
- **ARC-04 Reliable asynchronous work**: **2** (grade A), facets: implemented, tested. A scheduler and watchdog drive runs with timeouts and terminal states (automation repository: openhands/automation/scheduler.py, watchdog.py); git sync backs off after failures (migrations/versions/029_add_git_sync_failure_backoff.py).
  - Higher reading 3: Watchdog recovery and back-off approach level 3.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Single user by default, with a Helm chart for team deployments (helm/agent-canvas).

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **0** (grade A). No performance suite or documented limits (searched for benchmark, load test and perf).
- **ARC-07 Service objectives defined and monitored**: **1** (grade A). Telemetry for runs and the key-value store (openhands/automation/telemetry.py, kv_metrics.py); no objectives.
  - Higher reading 2: Run metrics are exported.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A). Each run executes in its own sandbox with timeouts and cleanup (openhands/automation/watchdog.py); repeatedly failing automations are disabled (migrations/versions/020_add_automation_disabled_reason.py).
- **ARC-09 Backup, restore and recovery**: **0** (grade A). No backup command or documented backup for the Automation Service database or storage.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A). No request or feature-request object for changing the product was found; requests live outside it.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A). The canvas deploys separately from the Agent Server and Automation Server behind an API contract, as an npm library, desktop app, container and Helm chart (docs/architecture.md, electron/, docker/, helm/).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A). Library entrypoints and lint configuration; no architectural boundary tests.
- **DEL-04 AI implementation lane**: **1** (grade A). Automations run coding agents on users' repositories (automation repository README); nothing implements changes to OpenHands' own definitions. Recorded under the self rule.
  - Higher reading 2: Automations configured in OpenHands are operator-configured behaviour run by an AI lane.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A). Lint, unit tests and builds on Ubuntu and Windows plus mocked-LLM Playwright E2E on pull requests (.github/workflows/ci.yml:4-66, mock-llm-e2e.yml); mutation testing (stryker.config.mjs); no accessibility or security checks.
  - Higher reading 3: Coverage is broad, including mutation testing.
- **DEL-06 Verification surface**: **2** (grade A). Backend server_info with runtime services (docs/architecture.md) and container health in the entrypoint (docker/entrypoint.sh).
- **DEL-07 Environment reproducibility**: **2** (grade A). Docker, Helm and desktop builds; mocked-LLM Docker E2E stands up an environment per run (.github/workflows/mock-llm-docker-e2e.yml).
- **DEL-08 Machine verifiability**: **2** (grade A). Playwright journeys with mocked and live configurations and a testing matrix (docs/TESTING_MATRIX.md); no changed-path map or adoption instrumentation.
  - Higher reading 3: The testing matrix maps surfaces to journeys.

### Release

- **DEL-09 Staged exposure**: **2** (grade A). Plugin automations can split runs between weighted variants (openhands/automation/presets/plugin/sdk_main.py:349-373).
- **DEL-10 Kill switch**: **2** (grade A). Automations can be disabled at runtime, and unhealthy ones are disabled automatically (tests/test_unhealthy_automations.py).
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: Automations act on users' repositories; no first-party lane ships OpenHands code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A). Typed client for the Agent Server API (src/api/open-hands.types.ts); the contract itself belongs to the Agent Server.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Canvas extensions are specified to contribute routed pages, panels, renderers, slots and themes as installable packages (specs/canvas-extensions.md), partly shipped behind capability detection; core layout is code.
  - Higher reading 3: Once shipped, extensions are validated, installable layout data.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A). Colour themes are palette definitions covering interface, code and terminal (src/themes/README.md); eight locale files.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A). Automations with cron and event triggers, templates and git sync are defined in the UI (src/types/automation.ts:3-13, src/routes/automation-*.tsx); they run on a separate automation server.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **3** (grade A). The agent server posts events to configured webhooks with buffering and retries (openhands-agent-server/openhands/agent_server/config.py:73-104).
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A). Hooks run at defined points (openhands-sdk/openhands/sdk/hooks); agent actions run in Docker, Apptainer, cloud or remote workspaces (openhands-workspace/openhands/workspace), but hook isolation and egress control were not verified.
  - Higher reading 3: If hooks execute inside the sandboxed workspace.

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A). Skills, plugins and MCP servers are configured through the canvas (src/routes/skills-plugins.tsx, mcp-settings.tsx); canvas extensions for UI are partly shipped.
  - Higher reading 3: Once extensions ship, UI, layout and theme are all plugin points.
- **MAL-14 Runtime isolation and dependency control**: **1** (grade A). No isolation model for canvas extensions is evidenced; agent code isolation is delegated to backends.
- **MAL-15 Developer loop**: **2** (grade A). Mocked-LLM development server and seed scripts (scripts/seed-automation-ux-data.mjs, docs/DEVELOPMENT.md).

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A). OpenHands, Claude Code, Codex, Gemini and other ACP agents map onto one agent protocol, so adding an agent is configuration (docs/ACP_AGENTS.md).
- **MAL-17 Connector definition or SDK**: **2** (grade A). Backends (local, Docker, VM, cloud) and ACP agents are configurable; no connector SDK with lifecycle.
  - Higher reading 3: ACP is a standard connector definition.
- **MAL-18 Stable versioned contracts**: **2** (grade A). Relies on the versioned Agent Server API and ACP; no deprecation windows in the canvas.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A). The canvas consumes MCP and exposes a UI tool that lets agents drive the canvas (tools/canvas_ui_tool.py); no MCP server for the canvas itself.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A). Users run agent conversations with actions through the canvas; there is no natural-language authoring of canvas definitions.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A). Consent-gated product analytics to PostHog (src/services/telemetry.ts); not available to product features.
- **LRN-02 Structured learning signals**: **1** (grade A). No typed feedback or learning signals in the canvas or the SDK.
- **LRN-03 User-issue detection**: **2** (grade A). Runs record failure kinds and status details, and unhealthy automations are detected (openhands/automation/watchdog.py, migrations/versions/016_add_run_status_detail.py).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A). No joined mining in the canvas.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A). Failed runs keep their phase, failure kind and conversation for inspection (docs/run-phase-reporting.md).
- **LRN-06 Ranked, evidence-backed proposals for change**: **0** (grade A). No proposals for changing the canvas.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A). No learning from sessions was found in the SDK (searched openhands-sdk/openhands/sdk/skills, context, agent).
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A). Critics evaluate task output for iterative refinement (openhands-sdk/openhands/sdk/critic), not changes to the agent itself.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **1** (grade A). Plugin automations tag each run with its experiment and variant (openhands/automation/presets/plugin/sdk_main.py:514-530), so variants can be compared by hand; nothing records a baseline or decision.
  - Higher reading 2: Variant-tagged runs are telemetry bound to the change.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). Component library with accessibility lint rules (eslint.config.js); no automated accessibility scans. Scored at the lower reading under rule 11 because: If lint rules without scans count as no automation.
  - Higher reading 2: The September v0.3 pass scored 2 on the evidence above.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **1** (grade A). No audit store in the canvas; durable audit is documented only through an external DefenseClaw integration (docs/DefenseClaw.md).
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **1** (grade A). Telemetry is consent-gated with opt-out (src/services/telemetry.ts:9-29); there is no data export or erasure feature in the canvas.
  - Higher reading 2: Consent management is a privacy control, though not export or erasure.
- **GOV-04 Security as infrastructure**: **1** (grade A). No security scanning in CI; runtime security is delegated to the Agent Server or external guardrails (docs/DefenseClaw.md).

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A). Automation definitions sync to git (src/routes/automation-git-sync.tsx); other settings are unversioned.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **1** (grade A). No proposal object for changes.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A). Confirmation policies (never, always, confirm risky) decide which agent actions need a person (openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43); they govern actions, not changes to the agent itself.
- **GOV-08 Upgrade safety**: **3** (grade A). CI checks REST API breakage, persisted-settings compatibility and deprecations on every change (software-agent-sdk .github/workflows/agent-server-rest-api-breakage.yml, persisted-settings-compat.yml, deprecation-check.yml).

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A), **3** with opt-in settings. The default confirmation policy is NeverConfirm (openhands-sdk/openhands/sdk/conversation/state.py:123); with ConfirmRisky, LLM security analyzers classify each action's risk and risky ones pause for a person (security/llm_analyzer.py, toolshield_llm_analyzer.py, ensemble.py).
- **GOV-10 Bounded self-change**: **not applicable**. No self-change path. If counted: 1.
- **GOV-11 Learning-input integrity**: **not applicable**. No self-change path. If counted: 1.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **2** (grade A). Kernel of conversations, backends, automations, profiles and skills with no business-domain nouns; channels exist only as automation outputs.
  - Higher reading 3: Domain-neutral coding-agent console.
- **EXP-02 A new domain is expressible without kernel change**: **2** (grade A). Automation templates cover new tasks without kernel change (src/routes/automation-templates.tsx).
- **EXP-03 A domain ships as an installable bundle**: **2** (grade A). Automation templates and git sync; installable canvas extensions are partly shipped.

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A). No adjacent-capability proposals.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A). Presets and plugins are available to every organisation.
