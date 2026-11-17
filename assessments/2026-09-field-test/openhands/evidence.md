# OpenHands (Agent Canvas + software-agent-sdk) evidence

Read at github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. The Automation Service keeps automations, runs and a key-value store in PostgreSQL (automation repository, migrations/versions).
- **schema_changes**: true. Alembic migrations in the Automation Service (migrations/versions, 29 files).
- **multi_tenant**: true. Re-checked under the v0.7 definition: the Automation Service holds automations, runs, drafts and uploads per organisation and checks the caller's organisation and user on every route (automation repository: migrations/versions/023_org_scoped_git_sync.py; openhands/automation/auth.py; draft_router.py:99-140 _assert_org_automation_exists, _assert_draft_creator), so separate organisations with their own members share one deployment.
- **hosted_service**: true. The Automation Service and Agent Server run as long-lived services for OpenHands Cloud.
- **machine_actions**: true. The Agent Server and Automation Service APIs create and run automations with per-user API keys (automation repository: openhands/automation/auth.py).
- **agent_mutations**: true. Changed to true for v0.7 (tightened definition: the product's own AI writes to its definitions). The Agent Canvas offers "Create an automation" by launching a chat in which the agent sets up the automation: "the agent handles the schedule and setup" (OpenHands src/components/features/automations/create-instructions.tsx:58-61; src/i18n/translation.json, AUTOMATIONS$CREATE_INSTRUCTIONS_GUIDANCE), through the Automation Service API with the user's key (automation repository: openhands/automation/router.py:198-282) and the openhands-automation agent skill (docs/kv-store-design.md:887). The skill itself lives outside the three assessed repositories.
- **evolution_auto_apply**: false. Re-checked for v0.7: automations the agent creates are made at a person's request in that conversation; no learning loop or background lane changes OpenHands' definitions on its own.
- **definition_change_path**: true. Automations, skills and settings are definitions.
- **code_release_path**: false. Re-checked under the v0.7 definition: no assessed code has OpenHands' AI write and activate plugins, tools or scripts that run as part of OpenHands. Custom automations can carry an uploaded code tarball (automation repository: router.py validate_tarball_path), but whether the agent skill authors them is outside the assessed repositories. Automations otherwise act on users' repositories.
- **ai_features**: true. The product runs LLM agents (openhands-sdk).
- **ai_data_access**: true. Agents read repositories and workspace files in their sandbox.
- **ai_actions**: true. Agents edit code, run commands and open pull requests; automations run them unattended.

## Kinds of change

- **Scheduled and event-driven automations** (`automations`, main, made by users and organisation admins): reach **1 Self-serve**, confidence medium. Created from templates or the setup UI, where drafts are validated and materialised disabled until a test run (OpenHands src/routes/automation-setup-route.tsx, automation-templates.tsx; automation repository: draft_router.py), or by the agent in chat (create-instructions.tsx:58-61). Changed, disabled and deleted through the API and UI (router.py PATCH and DELETE /{automation_id}, lines 325 and 481). Undo is disabling or deleting; edits keep no earlier version unless git sync is set up (src/routes/automation-git-sync.tsx). Reach 1, not 2: the agent drafts automations, but DEL-04 is 1 under the self rule, so the criteria do not support reach 2. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **Skills, plugins and tool servers the agent uses** (`skills-plugins`, main, made by users): reach **1 Self-serve**, confidence medium. Plugins are installed, enabled, disabled and uninstalled, and MCP servers added, updated and deleted in the canvas (src/routes/skills-plugins.tsx:20-100; src/hooks/mutation/use-install-plugin.ts, use-set-plugin-enabled.ts, use-uninstall-plugin.ts, use-add-mcp-server.ts, use-delete-mcp-server.ts). Undo is the reverse toggle or removal. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **Which models it uses and how the agent behaves** (`models-settings`, main, made by users): reach **1 Self-serve**, confidence low. LLM, agent, agent-profile, condenser and verification settings are chosen in the canvas settings pages (src/routes/llm-settings.tsx, agent-settings.tsx, agent-profiles-settings.tsx, condenser-settings.tsx; src/hooks/mutation/use-save-settings.ts). Undo is selecting the previous value; settings keep no history (GOV-05 2). Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **Which agent actions need a person's approval** (`action-approval`, not main, made by users): reach **1 Self-serve**, confidence medium. Confirmation policies (never, always, confirm risky) are selectable settings (software-agent-sdk openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43). Undo is selecting the previous policy. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **Interface extensions and themes** (`canvas-extensions`, not main, made by users and organisation admins): reach **0 Engineers only**, confidence low. Canvas extensions that contribute pages, panels and themes are specified and only partly shipped (specs/canvas-extensions.md); core layout is code. Reach 0 until extensions ship with an install and remove path.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md and .agents/skills in all three repositories; an OpenHands agent plugin runs in CI only for issue duplicate checking (OpenHands .github/workflows/issue-duplicate-checker.yml:67 and software-agent-sdk issue-duplicate-checker.yml:66, OpenHands/extensions pinned by SHA); software-agent-sdk requires review threads to be resolved (review-thread-gate.yml).
- **Proven, Request → Release**: not evidenced. Searched: All three repositories at the pinned commits: no operating records of requests becoming changes to OpenHands' own definitions in a real deployment (automation run history lives in each deployment's database).
- **Proven, Issue → Fix**: not evidenced. Searched: All three repositories: no incident or fix records from the product's own loop; unhealthy-automation disabling is shown in tests (tests/test_unhealthy_automations.py), not operating records.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: All three repositories: no records of capabilities proposed or launched to a cohort and kept or killed.

Confidence for criteria this migration did not change was assigned at migration to v0.7 from the recorded evidence (high where it names the code path and its tests or exact lines, medium where it names files but not every path, low where it rests on an absence claim or general description); criteria re-read for v0.7 carry the confidence of that re-reading.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 0.
- **ARC-02 Safe schema and data migrations**: **2** (grade A, confidence medium), facets: implemented, tested. Alembic migrations with downgrade steps, and a test of the migration history (automation repository: migrations/versions, tests/test_migration_history.py); no enforced online strategy.
  - Higher reading 3: Migration history is tested in CI.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A, confidence medium). The Automation Service is a stateless FastAPI app over PostgreSQL and object storage; the canvas ships a Helm chart (helm/agent-canvas).
- **ARC-04 Reliable asynchronous work**: **2** (grade A, confidence medium), facets: implemented, tested. A scheduler and watchdog drive runs with timeouts and terminal states (automation repository: openhands/automation/scheduler.py, watchdog.py); git sync backs off after failures (migrations/versions/029_add_git_sync_failure_backoff.py).
  - Higher reading 3: Watchdog recovery and back-off approach level 3.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A, confidence medium). Single user by default, with a Helm chart for team deployments (helm/agent-canvas).

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **0** (grade A, confidence low). No performance suite or documented limits (searched for benchmark, load test and perf).
- **ARC-07 Service objectives defined and monitored**: **1** (grade A, confidence medium). Telemetry for runs and the key-value store (openhands/automation/telemetry.py, kv_metrics.py); no objectives.
  - Higher reading 2: Run metrics are exported.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence medium). Each run executes in its own sandbox with timeouts and cleanup (openhands/automation/watchdog.py); repeatedly failing automations are disabled (migrations/versions/020_add_automation_disabled_reason.py).
  - AI-qualified reading: **3** (grade A, confidence high), facets: implemented, tested. Fallback strategy on provider errors, tested (tests/sdk/llm/test_llm_fallback.py).
- **ARC-09 Backup, restore and recovery**: **0** (grade A, confidence low). No backup command or documented backup for the Automation Service database or storage.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A, confidence low). No request or feature-request object for changing the product was found; requests live outside it.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A, confidence medium). The canvas deploys separately from the Agent Server and Automation Server behind an API contract, as an npm library, desktop app, container and Helm chart (docs/architecture.md, electron/, docker/, helm/).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A, confidence low). Library entrypoints and lint configuration; no architectural boundary tests.
- **DEL-04 AI implementation lane**: **1** (grade A, confidence low). Automations run coding agents on users' repositories (automation repository README); nothing implements changes to OpenHands' own definitions. Recorded under the self rule.
  - Higher reading 2: Automations configured in OpenHands are operator-configured behaviour run by an AI lane.
  - AI-qualified reading: **1** (grade A, confidence low). Automations change users' repositories, not OpenHands itself.
    - Higher reading 2: Operator-configured automations.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence medium). Lint, unit tests and builds on Ubuntu and Windows plus mocked-LLM Playwright E2E on pull requests (.github/workflows/ci.yml:4-66, mock-llm-e2e.yml); mutation testing (stryker.config.mjs); no accessibility or security checks.
  - Higher reading 3: Coverage is broad, including mutation testing.
- **DEL-06 Verification surface**: **2** (grade A, confidence medium). Backend server_info with runtime services (docs/architecture.md) and container health in the entrypoint (docker/entrypoint.sh).
- **DEL-07 Environment reproducibility**: **2** (grade A, confidence medium). Docker, Helm and desktop builds; mocked-LLM Docker E2E stands up an environment per run (.github/workflows/mock-llm-docker-e2e.yml).
- **DEL-08 Machine verifiability**: **2** (grade A, confidence medium). Playwright journeys with mocked and live configurations and a testing matrix (docs/TESTING_MATRIX.md); no changed-path map or adoption instrumentation.
  - Higher reading 3: The testing matrix maps surfaces to journeys.

### Release

- **DEL-09 Staged exposure**: **2** (grade A, confidence high). Plugin automations can split runs between weighted variants (openhands/automation/presets/plugin/sdk_main.py:349-373).
- **DEL-10 Kill switch**: **2** (grade A, confidence high). Automations can be disabled at runtime, and unhealthy ones are disabled automatically (tests/test_unhealthy_automations.py).
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: Automations act on users' repositories; no first-party lane ships OpenHands code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A, confidence medium). Typed client for the Agent Server API (src/api/open-hands.types.ts); the contract itself belongs to the Agent Server.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Canvas extensions are specified to contribute routed pages, panels, renderers, slots and themes as installable packages (specs/canvas-extensions.md), partly shipped behind capability detection; core layout is code.
  - Higher reading 3: Once shipped, extensions are validated, installable layout data.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A, confidence medium). Colour themes are palette definitions covering interface, code and terminal (src/themes/README.md); eight locale files.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A, confidence high). Automations with cron and event triggers, templates and git sync are defined in the UI (src/types/automation.ts:3-13, src/routes/automation-*.tsx); they run on a separate automation server.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **3** (grade A, confidence high). The agent server posts events to configured webhooks with buffering and retries (openhands-agent-server/openhands/agent_server/config.py:73-104).
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence medium). Hooks run at defined points (openhands-sdk/openhands/sdk/hooks); agent actions run in Docker, Apptainer, cloud or remote workspaces (openhands-workspace/openhands/workspace), but hook isolation and egress control were not verified.
  - Higher reading 3: If hooks execute inside the sandboxed workspace.

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A, confidence medium). Skills, plugins and MCP servers are configured through the canvas (src/routes/skills-plugins.tsx, mcp-settings.tsx); canvas extensions for UI are partly shipped.
  - Higher reading 3: Once extensions ship, UI, layout and theme are all plugin points.
- **MAL-14 Runtime isolation and dependency control**: **1** (grade A, confidence low). No isolation model for canvas extensions is evidenced; agent code isolation is delegated to backends.
- **MAL-15 Developer loop**: **2** (grade A, confidence medium). Mocked-LLM development server and seed scripts (scripts/seed-automation-ux-data.mjs, docs/DEVELOPMENT.md).

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A, confidence medium). OpenHands, Claude Code, Codex, Gemini and other ACP agents map onto one agent protocol, so adding an agent is configuration (docs/ACP_AGENTS.md).
- **MAL-17 Connector definition or SDK**: **2** (grade A, confidence low). Backends (local, Docker, VM, cloud) and ACP agents are configurable; no connector SDK with lifecycle.
  - Higher reading 3: ACP is a standard connector definition.
- **MAL-18 Stable versioned contracts**: **2** (grade A, confidence low). Relies on the versioned Agent Server API and ACP; no deprecation windows in the canvas.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A, confidence medium). The canvas consumes MCP and exposes a UI tool that lets agents drive the canvas (tools/canvas_ui_tool.py); no MCP server for the canvas itself.
  - AI-qualified reading: **2** (grade A, confidence medium). A UI tool lets agents drive the canvas; no MCP server for it.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A, confidence low). Users run agent conversations with actions through the canvas; there is no natural-language authoring of canvas definitions.
  - AI-qualified reading: **2** (grade A, confidence low). Model-backed agent conversations through the canvas.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A, confidence medium). Consent-gated product analytics to PostHog (src/services/telemetry.ts); not available to product features.
- **LRN-02 Structured learning signals**: **1** (grade A, confidence low). No typed feedback or learning signals in the canvas or the SDK.
- **LRN-03 User-issue detection**: **2** (grade A, confidence medium). Runs record failure kinds and status details, and unhealthy automations are detected (openhands/automation/watchdog.py, migrations/versions/016_add_run_status_detail.py).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A, confidence low). No joined mining in the canvas.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A, confidence medium). Failed runs keep their phase, failure kind and conversation for inspection (docs/run-phase-reporting.md).
  - AI-qualified reading: **0** (grade A, confidence medium). Run failure kinds are rule-based.
- **LRN-06 Ranked, evidence-backed proposals for change**: **0** (grade A, confidence low). No proposals for changing the canvas.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A, confidence medium). No learning from sessions was found in the SDK (searched openhands-sdk/openhands/sdk/skills, context, agent).
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A, confidence low). Re-scored for v0.7 under the tightened boundary; score unchanged, reason changed. The AI-made change to OpenHands' own definitions is an automation the agent creates in chat. The Automation API validates the request schema, tarball path and agent profile (automation repository: openhands/automation/router.py:198-282; capabilities_router.py:251-300), but nothing scans or evaluates the automation's prompt or code against a baseline before it is enabled; the person who asked sees the result in the conversation. Critics score task output, not changes to the agent (software-agent-sdk openhands-sdk/openhands/sdk/critic).
  - Higher reading 2: The Automation API validates every automation the agent creates (schema, trigger, tarball path, agent profile), an automated structural check on an AI-made change.
  - AI-qualified reading: **1** (grade A, confidence low). Agent-created automations pass only the Automation API's input validation (automation repository: router.py:198-282); no scan or evaluation.
    - Higher reading 2: API schema validation on agent-created automations.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **1** (grade A, confidence medium). Plugin automations tag each run with its experiment and variant (openhands/automation/presets/plugin/sdk_main.py:514-530), so variants can be compared by hand; nothing records a baseline or decision.
  - Higher reading 2: Variant-tagged runs are telemetry bound to the change.
- **LRN-10 The improvement loop improves itself**: **0** (grade A, confidence medium). The checks that govern change are code maintained by engineers: confirmation policies and security analysers (software-agent-sdk openhands-sdk/openhands/sdk/security), critics (sdk/critic), the Automation API's validation and the unhealthy-automation rule (automation repository: tests/test_unhealthy_automations.py). Evaluation suites (SWE-bench runs, tests/integration; .github/workflows/run-eval.yml) are run and extended by the team on labelled pull requests; no failure is recorded against a check and nothing turns failures into new checks inside the product.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A, confidence low). Component library with accessibility lint rules (eslint.config.js); no automated accessibility scans. Scored at the lower reading under rule 11 because: If lint rules without scans count as no automation.
  - Higher reading 2: The September v0.3 pass scored 2 on the evidence above.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **1** (grade A, confidence medium). No audit store in the canvas; durable audit is documented only through an external DefenseClaw integration (docs/DefenseClaw.md).
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **1** (grade A, confidence medium). Telemetry is consent-gated with opt-out (src/services/telemetry.ts:9-29); there is no data export or erasure feature in the canvas.
  - Higher reading 2: Consent management is a privacy control, though not export or erasure.
- **GOV-04 Security as infrastructure**: **1** (grade A, confidence medium). No security scanning in CI; runtime security is delegated to the Agent Server or external guardrails (docs/DefenseClaw.md).

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence medium). Automation definitions sync to git (src/routes/automation-git-sync.tsx); other settings are unversioned.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **1** (grade A, confidence low). No proposal object for changes.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A, confidence high). Confirmation policies (never, always, confirm risky) decide which agent actions need a person (openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43); they govern actions, not changes to the agent itself.
- **GOV-08 Upgrade safety**: **3** (grade A, confidence medium). CI checks REST API breakage, persisted-settings compatibility and deprecations on every change (software-agent-sdk .github/workflows/agent-server-rest-api-breakage.yml, persisted-settings-compat.yml, deprecation-check.yml).

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence high), **3** with opt-in settings. The default confirmation policy is NeverConfirm (openhands-sdk/openhands/sdk/conversation/state.py:123); with ConfirmRisky, LLM security analyzers classify each action's risk and risky ones pause for a person (security/llm_analyzer.py, toolshield_llm_analyzer.py, ensemble.py).
  - AI-qualified reading: **2** (grade A, confidence high), **3** with opt-in settings. Confirmation policy defaults to never; with ConfirmRisky, an LLM security analyser classifies actions (openhands-sdk/openhands/sdk/conversation/state.py:123).
- **GOV-10 Bounded self-change**: **1** (grade A, confidence low). Applies from v0.7 because agent_mutations is now true. The agent creates automations with the user's own API key, scoped to that user's organisation (automation repository: openhands/automation/auth.py), and repeatedly failing automations are disabled (migrations/versions/020_add_automation_disabled_reason.py); what the agent may create, how many and how often is limited only by the skill's instructions. The default confirmation policy is NeverConfirm (software-agent-sdk openhands-sdk/openhands/sdk/conversation/state.py:123). No allow or deny list for self-change was found.
  - AI-qualified reading: **1** (grade A, confidence low). Agent-created automations bounded by the user's key and skill instructions only (automation repository: auth.py).
- **GOV-11 Learning-input integrity**: **1** (grade A, confidence low). Applies from v0.7 because agent_mutations is now true. Automations record the creating user and organisation (automation repository: models and draft_router.py:131 _assert_draft_creator), but not which conversation content led the agent to create them; repository and web content in the conversation is not fenced or scanned before it shapes an automation. Nothing creates an automation without a person's request.
  - AI-qualified reading: **1** (grade A, confidence low). No provenance from conversation inputs to the automations the agent creates; no injection scan.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **2** (grade A, confidence low). Kernel of conversations, backends, automations, profiles and skills with no business-domain nouns; channels exist only as automation outputs.
  - Higher reading 3: Domain-neutral coding-agent console.
- **EXP-02 A new domain is expressible without kernel change**: **2** (grade A, confidence medium). Automation templates cover new tasks without kernel change (src/routes/automation-templates.tsx).
- **EXP-03 A domain ships as an installable bundle**: **2** (grade A, confidence low). Automation templates and git sync; installable canvas extensions are partly shipped.

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A, confidence low). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence low). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A, confidence low). Presets and plugins are available to every organisation.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence low). Agents work in a sandboxed workspace with repository files, skills and microagents loaded automatically.
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A, confidence high), facets: implemented, tested. Each conversation runs in its own sandbox with the user's provider tokens; automations use per-user API keys (automation repository: openhands/automation/auth.py), with tests.

### Quality

- **AIR-05 Offline AI evaluation**: **3** (grade A, confidence high). Behaviour and integration test suites for agents (tests/integration) and SWE-bench evaluation runs (.github/workflows/run-eval.yml).
- **AIR-06 Regression gating before release**: **2** (grade A, confidence high). Integration tests and evaluations run on labelled pull requests and releases (.github/workflows/integration-runner.yml, run-eval.yml); not blocking by default.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A, confidence high), facets: implemented, tested. The event stream persists every action, observation and tool call per conversation, with LLM call metadata (openhands-sdk/openhands/sdk/conversation).

### Operations

- **AIR-01 Model and provider portability and resilience**: **3** (grade A, confidence high). LLM fallback strategy on connection, rate-limit and server errors, plus routers (openhands-sdk/openhands/sdk/llm/fallback_strategy.py, router), with tests (tests/sdk/llm/test_llm_fallback.py).
- **AIR-02 AI usage and per-customer cost controls**: **2** (grade A, confidence medium). Conversation cost and budget-exceeded handling (fallback_strategy.py), and run cost recorded per automation (automation repository: migrations/versions/013_add_run_cost.py); no per-user budgets.
  - Higher reading 3: A per-conversation budget limits spend.
- **AIR-08 Production quality, drift and feedback monitoring**: **1** (grade A, confidence low). Critics score task output during a run; no production quality monitoring.
