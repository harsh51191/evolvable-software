# OpenHands (Agent Canvas + software-agent-sdk): EVOLVE v0.7 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.7.0 in this repository.

Scope: the Agent Canvas (OpenHands repository), the software-agent-sdk that runs agents, and the Automation Service (OpenHands/automation) that schedules and dispatches automations. OpenHands Cloud operations are out of scope.

## Reading

**SAL 1.** With the Automation Service now in scope, OpenHands has a hosted, multi-organisation architecture, but no load suite (ARC-06 0) or backup (ARC-09 0), which caps the foundation at L1. Automations run coding agents on users' repositories, which the self rule excludes (DEL-04 1). Runs record failure kinds and unhealthy automations are disabled automatically (LRN-03 2, DEL-10 2). **Next level:** backup and capacity evidence for the Automation Service, and a lane that improves OpenHands' own skills and automations.

## Limits

Repository evidence only. The Automation Service was added for v0.4 after the inter-rater study found it missing; it is beta. No live runs. Single rater.

---
Framework EVOLVE 0.7.0. Date 2026-09-30. Source github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30). Archetype **agent-runtime**. Basis **shipped** (what ships).

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, agent_mutations, definition_change_path, ai_features, ai_data_access, ai_actions. False: evolution_auto_apply, code_release_path.

Coverage: 67 assessed, 0 not evidenced, 8 not applicable. Grades: 67 A, 0 B, 0 C.

Confidence: 11 high, 32 medium, 24 low across the assessed criteria. Check these first (low confidence, and they hold a blocker or a critical control): ARC-06 (Request → Release to L2, Issue → Fix to L2, Opportunity → Expansion to L2); ARC-09 (Request → Release to L2, Issue → Fix to L2, Opportunity → Expansion to L2, Tested backup and restore control); DEL-01 (Request → Release to L2); DEL-04 (Request → Release to L2, Issue → Fix to L2); LRN-06 (Issue → Fix to L2); LRN-08 (Bounded self-change control); GOV-10 (Bounded self-change control); EXP-04 (Opportunity → Expansion to L2); EXP-05 (Opportunity → Expansion to L2).

## Software Autonomy Level

**Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)**

Progress toward the next level: Request → Release 1 of 4 conditions for L2; Issue → Fix 2 of 5 conditions for L2; Opportunity → Expansion 2 of 5 conditions for L2.

- With opt-in settings: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0).
- With every alternate reading: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0).

| Loop | Stages | Spine | Architecture | Governance | Level | AI-driven | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L1 | L1 | L2 | **L1** | L0 | L1 |
| Issue → Fix | L1 | L1 | L1 | L2 | **L1** | L0 | L1 |
| Opportunity → Expansion | L1 | L2 | L1 | L2 | **L1** | L0 | L1 |

**Recursion: 0 Fixed (LRN-10 at 0).** How far the loop improves its own checks, evaluation sets, policies and prompts from measured results.

**AI delivery.** Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

### Kinds of change

3 of 3 main kinds are self-serve (reach 1 or more: the people running the product make it themselves and can undo it).

| Kind | Who | Main | Reach | Evidence |
|---|---|---|---|---|
| Scheduled and event-driven automations (`automations`) | users and organisation admins | yes | 1 Self-serve | Created from templates or the setup UI, where drafts are validated and materialised disabled until a test run (OpenHands src/routes/automation-setup-route.tsx, automation-templates.tsx; automation repository: draft_router.py), or by the agent in chat (create-instructions.tsx:58-61). Changed, disabled and deleted through the API and UI (router.py PATCH and DELETE /{automation_id}, lines 325 and 481). Undo is disabling or deleting; edits keep no earlier version unless git sync is set up (src/routes/automation-git-sync.tsx). Reach 1, not 2: the agent drafts automations, but DEL-04 is 1 under the self rule, so the criteria do not support reach 2. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence medium. |
| Skills, plugins and tool servers the agent uses (`skills-plugins`) | users | yes | 1 Self-serve | Plugins are installed, enabled, disabled and uninstalled, and MCP servers added, updated and deleted in the canvas (src/routes/skills-plugins.tsx:20-100; src/hooks/mutation/use-install-plugin.ts, use-set-plugin-enabled.ts, use-uninstall-plugin.ts, use-add-mcp-server.ts, use-delete-mcp-server.ts). Undo is the reverse toggle or removal. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence medium. |
| Which models it uses and how the agent behaves (`models-settings`) | users | yes | 1 Self-serve | LLM, agent, agent-profile, condenser and verification settings are chosen in the canvas settings pages (src/routes/llm-settings.tsx, agent-settings.tsx, agent-profiles-settings.tsx, condenser-settings.tsx; src/hooks/mutation/use-save-settings.ts). Undo is selecting the previous value; settings keep no history (GOV-05 2). Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence low. |
| Which agent actions need a person's approval (`action-approval`) | users | no | 1 Self-serve | Confirmation policies (never, always, confirm risky) are selectable settings (software-agent-sdk openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43). Undo is selecting the previous policy. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence medium. |
| Interface extensions and themes (`canvas-extensions`) | users and organisation admins | no | 0 Engineers only | Canvas extensions that contribute pages, panels and themes are specified and only partly shipped (specs/canvas-extensions.md); core layout is code. Reach 0 until extensions ship with an install and remove path. Confidence low. |

### Proven

**Proven: not evidenced.** What operating records show real changes doing, beside what the product is built to do. From a repository alone, proven is usually not evidenced.

| Loop | Built | Proven | Operating records, or what was searched |
|---|---:|---|---|
| Request → Release | L1 | not evidenced | Searched: All three repositories at the pinned commits: no operating records of requests becoming changes to OpenHands' own definitions in a real deployment (automation run history lives in each deployment's database). |
| Issue → Fix | L1 | not evidenced | Searched: All three repositories: no incident or fix records from the product's own loop; unhealthy-automation disabling is shown in tests (tests/test_unhealthy_automations.py), not operating records. |
| Opportunity → Expansion | L1 | not evidenced | Searched: All three repositories: no records of capabilities proposed or launched to a cohort and kept or killed. |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 0 | fail |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 1 | fail |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 1; 1 | fail |

### What blocks the next level

- **Request → Release to L2**: spine Build needs product build path ≥ 2 (has DEL-04 1); stages Intake needs DEL-01 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- **Issue → Fix to L2**: spine Build needs product build path ≥ 2 (has DEL-04 1, LRN-07 1); stages Propose needs LRN-06 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)

### What AI drives

Each loop re-scored with its AI-performable stages read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level.

| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |
|---|---:|---:|---|---|
| Request → Release | L1 | L0 | DEL-01 0, DEL-04 1 | product build path ≥ 2 (has DEL-04 1); DEL-01 ≥ 2 (has 0) |
| Issue → Fix | L1 | L0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 1 | product build path ≥ 2 (has DEL-04 1, LRN-07 0); LRN-05 ≥ 2 (has 0); LRN-06 ≥ 2 (has 0) |
| Opportunity → Expansion | L1 | L0 | EXP-05 0 | EXP-05 ≥ 2 (has 0) |

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.4 | 1.4–1.8 | 1.4 | 1.4 | 1.1 |
| Velocity (DEL) | 1.5 | 1.5–1.7 | 1.5 | 1.5 | 1.5 |
| Open (MAL) | 2.1 | 2.1–2.3 | 2.1 | 2.1 | 1.6 |
| Learn (LRN) | 1.0 | 1.0–1.3 | 1.0 | 1.0 | 1.0 |
| Vet (GOV) | 1.4 | 1.4–1.6 | 1.6 | 1.4 | 1.4 |
| Expand (EXP) | 1.0 | 1.0–1.1 | 1.0 | 1.0 | 1.0 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Scale | 2.0 |
| ARC Capacity | 0.5 |
| ARC Resilience | 1.0 |
| DEL Intake | 0.0 |
| DEL Build | 2.0 |
| DEL Verify | 2.0 |
| DEL Release | 2.0 |
| MAL APIs | 2.0 |
| MAL Interface | 2.0 |
| MAL Behaviour | 2.3 |
| MAL Extensions | 1.7 |
| MAL Integrations | 2.3 |
| MAL Agent interface | 2.0 |
| LRN Sense | 1.5 |
| LRN Diagnose and propose | 1.0 |
| LRN Learn from experience | 1.0 |
| LRN Measure | 0.5 |
| GOV Compliance and security | 1.0 |
| GOV Change control | 2.0 |
| GOV AI and self-change safety | 1.3 |
| EXP Expressible | 2.0 |
| EXP Discover | 0.0 |
| EXP Launch | 1.0 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L1 (Experimental) · Context 3 · Quality 2 · Governance 1 · Operations 2 · not production-governed**

- With opt-in settings: AI Readiness L1 (Experimental) · Context 3 · Quality 2 · Governance 1 · Operations 2 · not production-governed.
- With every alternate reading: AI Readiness L1 (Experimental) · Context 3 · Quality 2 · Governance 1 · Operations 2 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 3 | AIR-03 3, AIR-04 3 |
| Quality | 2 | AIR-05 3, AIR-06 2 |
| Governance | 1 | AIR-07 3, GOV-09 (AI) 2, GOV-10 (AI) 1, GOV-11 (AI) 1, LRN-08 (AI) 1 |
| Operations | 2 | AIR-01 3, AIR-02 2, AIR-08 1, ARC-08 (AI) 3 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 3 | pass |
| Regression evaluation before release | AIR-06 ≥ 3 | 2 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 3 | pass |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 2 | MAL-19 2, MAL-20 2 |
| Build | 0 | DEL-01 0, DEL-04 1 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 1 |
| Expand | 0 | EXP-05 0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - |  | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| ARC-02 Safe schema and data migrations | assessed | 2 | 3 |  | A, medium | IT | Alembic migrations with downgrade steps, and a test of the migration history (automation repository: migrations/versions, tests/test_migration_history.py); no enforced online strategy. |
| ARC-03 Horizontal scale of services | assessed | 2 |  |  | A, medium |  | The Automation Service is a stateless FastAPI app over PostgreSQL and object storage; the canvas ships a Helm chart (helm/agent-canvas). |
| ARC-04 Reliable asynchronous work | assessed | 2 | 3 |  | A, medium | IT | A scheduler and watchdog drive runs with timeouts and terminal states (automation repository: openhands/automation/scheduler.py, watchdog.py); git sync backs off after failures (migrations/versions/029_add_git_sync_failure_backoff.py). |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A, medium |  | Single user by default, with a Helm chart for team deployments (helm/agent-canvas). |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 0 |  |  | A, low |  | No performance suite or documented limits (searched for benchmark, load test and perf). |
| ARC-07 Service objectives defined and monitored | assessed | 1 | 2 |  | A, medium |  | Telemetry for runs and the key-value store (openhands/automation/telemetry.py, kv_metrics.py); no objectives. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 3. Each run executes in its own sandbox with timeouts and cleanup (openhands/automation/watchdog.py); repeatedly failing automations are disabled (migrations/versions/020_add_automation_disabled_reason.py). |
| ARC-09 Backup, restore and recovery | assessed | 0 |  |  | A, low |  | No backup command or documented backup for the Automation Service database or storage. |
| DEL-01 Request intake into a structured change specification | assessed | 0 |  |  | A, low |  | AI-qualified reading: 0. No request or feature-request object for changing the product was found; requests live outside it. |
| DEL-02 Layers deploy independently | assessed | 3 |  |  | A, medium |  | The canvas deploys separately from the Agent Server and Automation Server behind an API contract, as an npm library, desktop app, container and Helm chart (docs/architecture.md, electron/, docker/, helm/). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 |  |  | A, low |  | Library entrypoints and lint configuration; no architectural boundary tests. |
| DEL-04 AI implementation lane | assessed | 1 | 2 |  | A, low |  | AI-qualified reading: 1. Automations run coding agents on users' repositories (automation repository README); nothing implements changes to OpenHands' own definitions. Recorded under the self rule. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A, medium |  | Lint, unit tests and builds on Ubuntu and Windows plus mocked-LLM Playwright E2E on pull requests (.github/workflows/ci.yml:4-66, mock-llm-e2e.yml); mutation testing (stryker.config.mjs); no accessibility or security checks. |
| DEL-06 Verification surface | assessed | 2 |  |  | A, medium |  | Backend server_info with runtime services (docs/architecture.md) and container health in the entrypoint (docker/entrypoint.sh). |
| DEL-07 Environment reproducibility | assessed | 2 |  |  | A, medium |  | Docker, Helm and desktop builds; mocked-LLM Docker E2E stands up an environment per run (.github/workflows/mock-llm-docker-e2e.yml). |
| DEL-08 Machine verifiability | assessed | 2 | 3 |  | A, medium |  | Playwright journeys with mocked and live configurations and a testing matrix (docs/TESTING_MATRIX.md); no changed-path map or adoption instrumentation. |
| DEL-09 Staged exposure | assessed | 2 |  |  | A, high |  | Plugin automations can split runs between weighted variants (openhands/automation/presets/plugin/sdk_main.py:349-373). |
| DEL-10 Kill switch | assessed | 2 |  |  | A, high |  | Automations can be disabled at runtime, and unhealthy ones are disabled automatically (tests/test_unhealthy_automations.py). |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: Automations act on users' repositories; no first-party lane ships OpenHands code changes. |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-02 Field definitions carry type and validation | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A, medium |  | Typed client for the Agent Server API (src/api/open-hands.types.ts); the contract itself belongs to the Agent Server. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A, medium |  | Canvas extensions are specified to contribute routed pages, panels, renderers, slots and themes as installable packages (specs/canvas-extensions.md), partly shipped behind capability detection; core layout is code. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A, medium |  | Colour themes are palette definitions covering interface, code and terminal (src/themes/README.md); eight locale files. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A, high |  | Automations with cron and event triggers, templates and git sync are defined in the UI (src/types/automation.ts:3-13, src/routes/automation-*.tsx); they run on a separate automation server. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 3 |  |  | A, high |  | The agent server posts events to configured webhooks with buffering and retries (openhands-agent-server/openhands/agent_server/config.py:73-104). |
| MAL-12 Sandboxed server-side hooks | assessed | 2 | 3 |  | A, medium |  | Hooks run at defined points (openhands-sdk/openhands/sdk/hooks); agent actions run in Docker, Apptainer, cloud or remote workspaces (openhands-workspace/openhands/workspace), but hook isolation and egress control were not verified. |
| MAL-13 Plugin lane breadth | assessed | 2 | 3 |  | A, medium |  | Skills, plugins and MCP servers are configured through the canvas (src/routes/skills-plugins.tsx, mcp-settings.tsx); canvas extensions for UI are partly shipped. |
| MAL-14 Runtime isolation and dependency control | assessed | 1 |  |  | A, low |  | No isolation model for canvas extensions is evidenced; agent code isolation is delegated to backends. |
| MAL-15 Developer loop | assessed | 2 |  |  | A, medium |  | Mocked-LLM development server and seed scripts (scripts/seed-automation-ux-data.mjs, docs/DEVELOPMENT.md). |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A, medium |  | OpenHands, Claude Code, Codex, Gemini and other ACP agents map onto one agent protocol, so adding an agent is configuration (docs/ACP_AGENTS.md). |
| MAL-17 Connector definition or SDK | assessed | 2 | 3 |  | A, low |  | Backends (local, Docker, VM, cloud) and ACP agents are configurable; no connector SDK with lifecycle. |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A, low |  | Relies on the versioned Agent Server API and ACP; no deprecation windows in the canvas. |
| MAL-19 Machine-readable capability surface for agents | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 2. The canvas consumes MCP and exposes a UI tool that lets agents drive the canvas (tools/canvas_ui_tool.py); no MCP server for the canvas itself. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 |  |  | A, low |  | AI-qualified reading: 2. Users run agent conversations with actions through the canvas; there is no natural-language authoring of canvas definitions. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 |  |  | A, medium |  | Consent-gated product analytics to PostHog (src/services/telemetry.ts); not available to product features. |
| LRN-02 Structured learning signals | assessed | 1 |  |  | A, low |  | No typed feedback or learning signals in the canvas or the SDK. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A, medium |  | Runs record failure kinds and status details, and unhealthy automations are detected (openhands/automation/watchdog.py, migrations/versions/016_add_run_status_detail.py). |
| LRN-04 Cross-source mining inside the product | assessed | 1 |  |  | A, low |  | No joined mining in the canvas. |
| LRN-05 Automated diagnosis | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 0. Failed runs keep their phase, failure kind and conversation for inspection (docs/run-phase-reporting.md). |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A, low |  | AI-qualified reading: 0. No proposals for changing the canvas. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A, medium |  | AI-qualified reading: 0. No learning from sessions was found in the SDK (searched openhands-sdk/openhands/sdk/skills, context, agent). |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 | 2 |  | A, low |  | AI-qualified reading: 1. Re-scored for v0.7 under the tightened boundary; score unchanged, reason changed. The AI-made change to OpenHands' own definitions is an automation the agent creates in chat. The Automation API validates the request schema, tarball path and agent profile (automation repository: openhands/automation/router.py:198-282; capabilities_router.py:251-300), but nothing scans or evaluates the automation's prompt or code against a baseline before it is enabled; the person who asked sees the result in the conversation. Critics score task output, not changes to the agent (software-agent-sdk openhands-sdk/openhands/sdk/critic). |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 1 | 2 |  | A, medium |  | Plugin automations tag each run with its experiment and variant (openhands/automation/presets/plugin/sdk_main.py:514-530), so variants can be compared by hand; nothing records a baseline or decision. |
| LRN-10 The improvement loop improves itself | assessed | 0 |  |  | A, medium |  | The checks that govern change are code maintained by engineers: confirmation policies and security analysers (software-agent-sdk openhands-sdk/openhands/sdk/security), critics (sdk/critic), the Automation API's validation and the unhealthy-automation rule (automation repository: tests/test_unhealthy_automations.py). Evaluation suites (SWE-bench runs, tests/integration; .github/workflows/run-eval.yml) are run and extended by the team on labelled pull requests; no failure is recorded against a check and nothing turns failures into new checks inside the product. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A, low |  | Component library with accessibility lint rules (eslint.config.js); no automated accessibility scans. Scored at the lower reading under rule 11 because: If lint rules without scans count as no automation. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 1 |  |  | A, medium |  | No audit store in the canvas; durable audit is documented only through an external DefenseClaw integration (docs/DefenseClaw.md). |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 1 | 2 |  | A, medium |  | Telemetry is consent-gated with opt-out (src/services/telemetry.ts:9-29); there is no data export or erasure feature in the canvas. |
| GOV-04 Security as infrastructure | assessed | 1 |  |  | A, medium |  | No security scanning in CI; runtime security is delegated to the Agent Server or external guardrails (docs/DefenseClaw.md). |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A, medium |  | Automation definitions sync to git (src/routes/automation-git-sync.tsx); other settings are unversioned. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 1 |  |  | A, low |  | No proposal object for changes. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 |  |  | A, high |  | Confirmation policies (never, always, confirm risky) decide which agent actions need a person (openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43); they govern actions, not changes to the agent itself. |
| GOV-08 Upgrade safety | assessed | 3 |  |  | A, medium |  | CI checks REST API breakage, persisted-settings compatibility and deprecations on every change (software-agent-sdk .github/workflows/agent-server-rest-api-breakage.yml, persisted-settings-compat.yml, deprecation-check.yml). |
| GOV-09 Agent-safe actions | assessed | 2 |  | 3 | A, high |  | AI-qualified reading: 2. The default confirmation policy is NeverConfirm (openhands-sdk/openhands/sdk/conversation/state.py:123); with ConfirmRisky, LLM security analyzers classify each action's risk and risky ones pause for a person (security/llm_analyzer.py, toolshield_llm_analyzer.py, ensemble.py). |
| GOV-10 Bounded self-change | assessed | 1 |  |  | A, low |  | AI-qualified reading: 1. Applies from v0.7 because agent_mutations is now true. The agent creates automations with the user's own API key, scoped to that user's organisation (automation repository: openhands/automation/auth.py), and repeatedly failing automations are disabled (migrations/versions/020_add_automation_disabled_reason.py); what the agent may create, how many and how often is limited only by the skill's instructions. The default confirmation policy is NeverConfirm (software-agent-sdk openhands-sdk/openhands/sdk/conversation/state.py:123). No allow or deny list for self-change was found. |
| GOV-11 Learning-input integrity | assessed | 1 |  |  | A, low |  | AI-qualified reading: 1. Applies from v0.7 because agent_mutations is now true. Automations record the creating user and organisation (automation repository: models and draft_router.py:131 _assert_draft_creator), but not which conversation content led the agent to create them; repository and web content in the conversation is not fenced or scanned before it shapes an automation. Nothing creates an automation without a person's request. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 2 | 3 |  | A, low |  | Kernel of conversations, backends, automations, profiles and skills with no business-domain nouns; channels exist only as automation outputs. |
| EXP-02 A new domain is expressible without kernel change | assessed | 2 |  |  | A, medium |  | Automation templates cover new tasks without kernel change (src/routes/automation-templates.tsx). |
| EXP-03 A domain ships as an installable bundle | assessed | 2 |  |  | A, low |  | Automation templates and git sync; installable canvas extensions are partly shipped. |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A, low |  | No record of unmet intents was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A, low |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 |  |  | A, low |  | Presets and plugins are available to every organisation. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A, low |  | Agents work in a sandboxed workspace with repository files, skills and microagents loaded automatically. |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 3 |  |  | A, high | IT | Each conversation runs in its own sandbox with the user's provider tokens; automations use per-user API keys (automation repository: openhands/automation/auth.py), with tests. |
| AIR-05 Offline AI evaluation | assessed | 3 |  |  | A, high |  | Behaviour and integration test suites for agents (tests/integration) and SWE-bench evaluation runs (.github/workflows/run-eval.yml). |
| AIR-06 Regression gating before release | assessed | 2 |  |  | A, high |  | Integration tests and evaluations run on labelled pull requests and releases (.github/workflows/integration-runner.yml, run-eval.yml); not blocking by default. |
| AIR-07 AI action tracing and auditability | assessed | 3 |  |  | A, high | IT | The event stream persists every action, observation and tool call per conversation, with LLM call metadata (openhands-sdk/openhands/sdk/conversation). |
| AIR-01 Model and provider portability and resilience | assessed | 3 |  |  | A, high |  | LLM fallback strategy on connection, rate-limit and server errors, plus routers (openhands-sdk/openhands/sdk/llm/fallback_strategy.py, router), with tests (tests/sdk/llm/test_llm_fallback.py). |
| AIR-02 AI usage and per-customer cost controls | assessed | 2 | 3 |  | A, medium |  | Conversation cost and budget-exceeded handling (fallback_strategy.py), and run cost recorded per automation (automation repository: migrations/versions/013_add_run_cost.py); no per-user budgets. |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 1 |  |  | A, low |  | Critics score task output during a run; no production quality monitoring. |

Grade cell: evidence grade, then confidence where recorded. Facets: I implemented, T tested, O operated. Operated supports a Proven reading and never changes a score.
