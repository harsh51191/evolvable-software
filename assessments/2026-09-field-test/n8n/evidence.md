# n8n evidence

Read at github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Workflows, credentials, executions and data tables in the database.
- **schema_changes**: true. TypeORM migrations (packages/@n8n/db/src/migrations) and data tables created at runtime.
- **multi_tenant**: true. Re-read at the v0.7 migration under the tightened definition. Team projects have their own members and project roles (project admin, editor, viewer; packages/@n8n/permissions/src/roles/all-roles.ts) and members do not see other projects' workflows or credentials (packages/cli/test/integration/access-control/cross-project-access.test.ts:136-379). Team projects need a licence (quota:maxTeamProjects, packages/cli/src/license.ts:483-485); this assessment scores the licensed enterprise modules as shipped, as it does for workflow reviews and the AI builder. The v0.6 reading (false) treated projects as not isolated tenants.
- **hosted_service**: true. Main, worker and webhook processes run as long-lived services, with multi-main and queue mode (packages/cli/src/scaling).
- **machine_actions**: true. The public API and MCP server change workflows and credentials (packages/cli/src/modules/mcp).
- **agent_mutations**: true. The AI workflow builder and Instance AI change workflows (packages/cli/src/modules/instance-ai, workflow-builder), and the agents builder writes agent configuration, skills and custom tools as drafts it can publish when the user asks (packages/cli/src/modules/agents/builder/agents-builder-tools.service.ts:397-405, 697-740).
- **evolution_auto_apply**: false. AI-built changes pass approvals before they apply.
- **definition_change_path**: true. Workflows, credentials, variables and data tables are definitions.
- **code_release_path**: true. Re-read at the v0.7 migration under the tightened definition. The agents builder (agents module, on by default: packages/@n8n/backend-common/src/modules/module-registry.ts:80) writes TypeScript custom tools, compiles and stores them on the agent (packages/cli/src/modules/agents/builder/agents-builder-tools.service.ts:1090-1123, agent-custom-tools.service.ts) and they run in a V8 isolate when the agent runs (runtime/agent-secure-runtime.ts). The workflow builder may also write Code-node scripts (packages/@n8n/ai-workflow-builder.ee/src/prompts/agents/discovery.prompt.ts:271-284). Both are code the product's AI produces that then runs as part of the product.
- **ai_features**: true. AI workflow builder, Instance AI and AI agent nodes (packages/@n8n/ai-workflow-builder.ee, packages/cli/src/modules/instance-ai).
- **ai_data_access**: true. Instance AI reads workflows, executions and node parameters (packages/cli/src/modules/instance-ai).
- **ai_actions**: true. Instance AI and the builder create and change workflows behind approvals.

## Kinds of change

- **Automations: workflows and their steps** (`workflows`, main, made by workflow builders and instance admins): reach **2 Drafted**, confidence medium. Built and changed in the editor with no deploy; undo through workflow history restore and publishing an earlier version (packages/cli/src/workflows/workflow-history/workflow-history.controller.ts:22-91), with 24 hours of history kept without a licence and the current and published versions always kept (packages/@n8n/constants/src/index.ts:80, workflow-history-manager.ts:35-43). The AI workflow builder plans and drafts the workflow and a person publishes it (licensed feat:aiBuilder, packages/cli/src/controllers/ai.controller.ts:83; packages/@n8n/ai-workflow-builder.ee). Not 3: the draft carries no verification evidence and no policy (DEL-04 is 2).
- **AI agents: their instructions, tools, skills and knowledge** (`agents`, not main, made by project members who build agents): reach **2 Drafted**, confidence medium. Agents module is on by default (packages/@n8n/backend-common/src/modules/module-registry.ts:80); agents are edited as drafts, published, and reverted to any earlier version (packages/cli/src/modules/agents/agent-publish.service.ts:124-176, 358-450). The agents builder drafts configuration and custom tools, tests the draft in preview chat, and publishes only when the user asks (builder/agents-builder-tools.service.ts:397-405, 567-569, 697-740). Not 3 for the same reason as workflows. Not main: a new surface beside workflows; its share of change requests is not evidenced.
- **Connections to other services (credentials)** (`credentials`, main, made by workflow builders and instance admins): reach **0 Engineers only**, confidence medium. Created and edited in the UI with no deploy (packages/cli/src/credentials/credentials.controller.ts:217, 264), but there is no history of earlier values and deletion is permanent (credentials.controller.ts:479); source control carries credential stubs without secrets. A path without undo is reach 0.
- **Add, update or remove community integrations** (`community-nodes`, not main, made by instance owner): reach **1 Self-serve**, confidence medium. Installed, updated and uninstalled from the UI (packages/cli/src/modules/community-packages/community-packages.controller.ts:11-34), on by default (community-packages.config.ts:12-29). An integration with no published package needs an engineer to write a node (packages/@n8n/node-cli).
- **Instance settings and shared variables** (`settings-variables`, not main, made by instance admins): reach **0 Engineers only**, confidence medium. Most instance settings are environment variables read at start (about 500 @Env settings in packages/@n8n/config/src/configs), so a change needs a restart or redeploy; variables are licensed (packages/cli/src/environments.ee/variables/variables.controller.ee.ts:30) and have no history; both roll back only through git source control.
- **Data tables used by workflows** (`data-tables`, not main, made by workflow builders): reach **0 Engineers only**, confidence medium. Tables, columns and rows are created, changed and deleted in the UI (packages/cli/src/modules/data-table/data-table.controller.ts:104-412) with no history or restore. A path without undo is reach 0.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md and CLAUDE.md at the root and in packages (cli, frontend, nodes-base), a Claude Code plugin (.claude/plugins/n8n), shared agent skills (.agents/skills), AI review rules (cubic.yaml, .agents/review-rules), an opencode harness pinned at harness-v0.3.0 from n8n-io/cat-bot (agent-harness.lock.json, scripts/agent-harness.mjs:17-31), and PRs from the n8n-cat-bot agent (.github/workflows/ci-owners-assign-reviewers.yml:31-37).
- **Proven, Request → Release**: not evidenced. Searched: The repository at the pinned commit: CHANGELOG.md (n8n's own releases, made by engineers), packages/cli/src/workflows/workflow-history, packages/cli/src/modules/insights, workflow-reviews.ee and instance-version-history. No operating records of real changes made through the product's request loop in a deployment are in the repository.
- **Proven, Issue → Fix**: not evidenced. Searched: The same sources plus packages/cli/src/modules/breaking-changes and execution error records; no operating records of issues fixed through the product's loop in a deployment.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: The same sources; no records of capabilities launched and kept or killed through the product.

Confidence for criteria whose reading did not change at the v0.7 migration was assigned at migration from the recorded evidence (high where it names the code path and its tests, medium where it names code but not every path, low where the reading is inferred or rests on documentation or absence); criteria re-read at migration were assigned from that re-reading.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **2** (grade A, confidence medium). Data tables are real database tables queried with SQL; a workflow index supports search (packages/cli/src/modules/workflow-index); no definition-driven index mapping.
- **ARC-02 Safe schema and data migrations**: **2** (grade A, confidence high). TypeORM migrations with down steps for PostgreSQL and SQLite and a migration registry with tests (packages/@n8n/db/src/migrations); no enforced online strategy.

### Scale

- **ARC-03 Horizontal scale of services**: **3** (grade A, confidence high), facets: implemented, tested. Multi-main setup with leader election and Redis locks, and queue mode with separate workers (packages/cli/src/scaling/multi-main-setup.ee.ts, leader-election-client.ts, redis-lock.service.ts), covered by tests.
- **ARC-04 Reliable asynchronous work**: **2** (grade A, confidence high), facets: implemented, tested. Queue mode runs executions on Bull with Redis (packages/cli/src/scaling/scaling.service.ts:100-105); leader election keeps schedules on one main. Failed executions are kept and can be retried by hand.
  - Higher reading 3: Run-once scheduling and visibility are in place.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A, confidence medium). Applies since multi_tenant was re-read as true. Projects share one instance and database; isolation is by project-scoped roles with cross-project access tests (packages/@n8n/permissions/src/roles/all-roles.ts, packages/cli/test/integration/access-control/cross-project-access.test.ts:136-379); licensed worker pools can route a project's executions to its own queue (packages/cli/src/scaling/pool-config.service.ee.ts:14-40, packages/cli/src/controllers/project-pool-settings.controller.ee.ts). No per-project quotas or noisy-neighbour detection, so not 3.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **2** (grade A, confidence high), facets: implemented, tested. Performance E2E runs on pull requests (ci-pull-requests.yml:492, test-e2e-performance-reusable.yml) and nightly benchmarks (test-benchmark-nightly.yml, packages/@n8n/benchmark); per-surface limits not documented in the repository.
  - Higher reading 3: A performance suite gates pull requests; only documented limits are missing.
- **ARC-07 Service objectives defined and monitored**: **2** (grade A, confidence medium). Prometheus metrics endpoint (packages/cli/src/metrics/prometheus); no published objectives.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence medium). Code nodes run in separate task-runner processes (packages/@n8n/task-runner, task-runner-python); nodes have retry-on-fail and timeouts; community nodes run in-process.
  - AI-qualified reading: **2** (grade A, confidence medium), facets: implemented. Retry-on-fail, timeouts and fallback models on agent nodes.
    - Higher reading 3: Fallback models contain provider failure.
- **ARC-09 Backup, restore and recovery**: **2** (grade A, confidence medium). export:entities and import:entities move every database entity, optionally with data-table rows (packages/cli/src/commands/export/entities.ts); binary data and the encryption key are separate; no restore test or recovery objectives.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **2** (grade A, confidence medium). The AI workflow builder plans before building: it asks typed clarifying questions and produces a plan with a trigger, steps, suggested nodes and specifications that the user approves (packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts, agents/planner.agent.ts). The plan has no acceptance criteria or risk class.
  - Higher reading 3: A confirmed, structured plan with clarifying questions approaches levels 3 and 4.
  - AI-qualified reading: **2** (grade A, confidence medium). The planner asks clarifying questions and drafts a plan (ai-workflow-builder.ee/src/types/planning.ts).
    - Higher reading 3: Close to a specification.

### Build

- **DEL-02 Layers deploy independently**: **2** (grade A, confidence medium). Main, worker, webhook and task-runner processes ship as separate container images from one monorepo build (12 Dockerfiles).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A, confidence medium). pnpm workspace packages, a module system with explicit registration, and import restrictions in package lint configs (packages/cli/eslint.config.mjs); Playwright architecture enforced by janitor (packages/testing/janitor).
  - Higher reading 3: Lint-enforced boundaries plus API types between packages.
- **DEL-04 AI implementation lane**: **2** (grade A, confidence medium). AI workflow builder and Instance AI turn requests into workflow changes behind approvals, per instance.
  - Higher reading 3: The lane is broad and governed, not narrow and engineer-run.
  - AI-qualified reading: **2** (grade A, confidence medium). The builder and Instance AI change workflows behind approvals.
    - Higher reading 3: Wide coverage.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **3** (grade A, confidence medium). Pull requests run unit, lint, E2E (including axe fixtures), database, smoke, frontend declaration, performance and security jobs with no draft filter (.github/workflows/ci-pull-requests.yml:280-508).
- **DEL-06 Verification surface**: **2** (grade A, confidence medium). /healthz and /healthz/readiness (packages/cli/src/abstract-server.ts:139), Prometheus metrics (server.ts:172), instance version history (packages/cli/src/modules/instance-version-history) and settings APIs exposing configuration. Scored at the lower reading under rule 11 because: If the settings API is not a deployed-configuration snapshot.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **DEL-07 Environment reproducibility**: **3** (grade A, confidence medium). One preview codespace per pull request from the master prebuild (scripts/codespace-preview/preview.mjs), instance seeding scripts (scripts/instance-seeding), nightly benchmark infrastructure created and destroyed (test-benchmark-destroy-nightly.yml).
- **DEL-08 Machine verifiability**: **2** (grade A, confidence medium). Playwright journeys (packages/testing/playwright/composables/journeys) with nightly coverage; no changed-path to journey map or adoption instrumentation at ship evidenced.
  - Higher reading 3: Telemetry instruments features; janitor enforces test architecture.

### Release

- **DEL-09 Staged exposure**: **2** (grade A, confidence low). Workflow versions are published deliberately, and frontend features are gated per instance; there are no cohort rollouts for workflow changes.
- **DEL-10 Kill switch**: **2** (grade A, confidence low). Workflows can be deactivated at runtime; there is no global kill switch for AI-made changes.
- **DEL-11 Release rollback**: **2** (grade A, confidence medium), facets: implemented, tested. Applies since code_release_path was re-read as true. Code the product's AI writes rolls back with the definition that carries it. An agent version snapshots its tools and skills, and an earlier version can be reverted to or published again (packages/cli/src/modules/agents/agent-publish.service.ts:124-176, 404-450; agent-publish.controller.ts:84-144), covered by agent-publish.service.test.ts. Code-node scripts roll back with workflow history, which keeps only 24 hours of earlier versions without a licence (packages/@n8n/constants/src/index.ts:80, packages/cli/src/workflows/workflow-history/workflow-history-helper.ts:11-27), so a previous release is not always available.
  - Higher reading 3: Activating an earlier agent version, tools included, is one tested step, and tool code changes no stored schema.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **2** (grade A, confidence medium). Data tables are created in the UI with typed columns; a DDL service creates real tables without deploy, with their own permissions and public API (packages/cli/src/modules/data-table: data-table-ddl.service.ts, data-table-permissions.ts; packages/cli/src/public-api/v1/handlers/data-tables). Scored at the lower reading under rule 11 because: Data tables are storage for workflows, not general business-object types with forms and relations.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **MAL-02 Field definitions carry type and validation**: **2** (grade A, confidence medium). Data-table columns are typed (data-table-column.entity.ts); execution data has redaction policies (packages/cli/src/modules/redaction/redaction-policy.ts) but no field-level privacy classification.
  - Higher reading 3: Redaction policies are a consumed privacy control, though not a field tag.
- **MAL-03 Relationships and lifecycle states declarable**: **1** (grade A, confidence low). No declarable relations between data tables and no lifecycle states for user entities; workflow states are product-defined.

### APIs

- **MAL-04 API per entity is generic or generated**: **2** (grade A, confidence medium). One generic rows API serves every data table (public-api/v1/handlers/data-tables); the rest of the API is hand-written per resource.
  - Higher reading 3: Every defined entity type (data table) gets API presence without per-entity code.
- **MAL-05 API reshapes at runtime from definitions**: **3** (grade A, confidence medium). Creating or altering a data table changes the rows API immediately, and each workflow exposed over MCP or webhooks changes the callable surface without a deploy.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A, confidence medium). Public API v1 with an OpenAPI description and structured validation errors (packages/cli/src/public-api/index.ts, public-api-validation-error.ts); no typed client generation or dry-run.
  - Higher reading 3: Shared API types package (packages/@n8n/api-types) serves typed clients internally.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Workflow canvases and Form trigger pages are stored as data and can be tested before activation (packages/nodes-base/nodes/Form); application layout is code.
  - Higher reading 3: Forms are admin-authored, validated and previewable layouts.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **2** (grade A, confidence low). Generic grid for any data table and generic form rendering from field definitions; no configurable list and detail views for other objects.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A, confidence low). UI strings externalised in an i18n package with community locales (33 locale files); no tenant theme editor or text overrides.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **3** (grade A, confidence medium). Workflows are machine-readable rules (triggers, If, Switch, Filter and 400+ action nodes) composed in the UI across all integrations and data tables; testable with pinned data and by debugging past executions; versioned in workflow history (packages/cli/src/workflows/workflow-history); authored by the AI workflow builder and Instance AI (packages/@n8n/ai-workflow-builder.ee, packages/@n8n/instance-ai). Scored at the lower reading under rule 11 because: If replaying a past execution does not count as simulation against history.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **3** (grade A, confidence medium). Event bus with log-streaming destinations (webhook, syslog, Sentry) configured by admins (packages/cli/src/modules/log-streaming.ee, packages/workflow/src/message-event-bus.ts); webhook triggers; executions are logged and can be retried.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence medium). Code nodes run in separate task-runner processes with memory, payload, concurrency and time limits (packages/@n8n/config/src/configs/runners.config.ts:36-55) and module allowlists (packages/@n8n/task-runner/src/config/js-runner-config.ts:5-8), triggered by events and webhooks. No egress control found.
  - Higher reading 3: Every clause except egress control is met.

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A, confidence medium). Declarative and programmatic custom nodes, community packages installed from the UI (packages/cli/src/modules/community-packages), frontend extension SDK (packages/@n8n/extension-sdk), workflow templates and agent tools. Scored at the lower reading under rule 11 because: Theme and text are not plugin points.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A, confidence low). User code runs in isolated task-runner processes with resource limits; community nodes are scanned and can be restricted by policy but run with full trust in the main process.
  - Higher reading 3: Code-node isolation meets every clause except egress.
- **MAL-15 Developer loop**: **3** (grade A, confidence medium). Node CLI with dev server and linting (packages/@n8n/node-cli, eslint-plugin-community-nodes), source-control branches, execution logs and pinned-data testing against a live instance.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **2** (grade A, confidence medium). All connectors exchange a common item format and are joined by configurable mapping (expressions and field mapping in the UI), so a second system is mapping configuration (packages/workflow). Scored at the lower reading under rule 11 because: No canonical domain model, only a canonical transport format.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **MAL-17 Connector definition or SDK**: **3** (grade A, confidence medium). Node SDK with credential types for auth, trigger and polling patterns and versioning (packages/@n8n/create-node, packages/@n8n/node-cli); admins install community connectors in the UI.
  - Higher reading 4: Verified community nodes amount to certification.
- **MAL-18 Stable versioned contracts**: **2** (grade A, confidence medium). Path-versioned public API (packages/cli/src/public-api/v1) with documented breaking changes (packages/cli/BREAKING-CHANGES.md); no deprecation windows.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **3** (grade A, confidence medium). Instance MCP server with scoped API keys, per-workflow tool availability and MCP evaluations (packages/cli/src/modules/mcp: mcp-scopes.ts, mcp-tool-availability.ts, evaluations).
  - Higher reading 4: Each exposed workflow becomes a tool whose schema comes from its trigger definition.
  - AI-qualified reading: **3** (grade A, confidence medium). Instance MCP server with scoped keys (packages/cli/src/modules/mcp).
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **3** (grade A, confidence medium). Instance AI gives a natural-language interface to workflows, executions, credentials and nodes, with plans and approval cards before execution (packages/@n8n/instance-ai/docs/architecture.md, tools.md:18-82); chat hub for members (packages/cli/src/modules/chat-hub); Instance AI evaluations run in CI (.github/workflows/ci-instance-ai-evals.yml).
  - Higher reading 4: Instance AI aims to make workflows reachable without the UI and is evaluated in CI.
  - AI-qualified reading: **3** (grade A, confidence medium). Instance AI grounded in workflows and executions, with plans and approvals.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **3** (grade A, confidence medium). The insights module collects execution counts, failures and time saved continuously and shows them in the product (packages/cli/src/modules/insights); vendor telemetry with redaction (packages/@n8n/telemetry).
- **LRN-02 Structured learning signals**: **2** (grade A, confidence medium). Evaluation test runs record metrics per workflow (packages/@n8n/db/src/entities/test-run.ee.ts) and insights record per-workflow outcomes; no triage workflow.
  - Higher reading 3: Test runs are linked to the workflow they evaluate.
- **LRN-03 User-issue detection**: **2** (grade A, confidence medium). Insights report failures and failure rates per workflow (packages/cli/src/modules/insights/insights.service.ts:181-268) and error workflows fire on failures.
  - Higher reading 3: Failure rates per workflow approach friction detection.
- **LRN-04 Cross-source mining inside the product**: **1** (grade A, confidence low). Insights cover executions only; nothing joins usage, support and delivery data.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A, confidence low). Failed executions keep the failing node, input and error; the AI assistant can explain a node error on request.
  - Higher reading 3: On-request AI debugging with node context approaches level 3.
  - AI-qualified reading: **2** (grade A, confidence low). The AI assistant explains node errors with context on request.
    - Higher reading 3: Close to level 3.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A, confidence medium). The breaking-changes detection report recommends fixes before upgrades (packages/cli/src/modules/breaking-changes/detection-report.ts): evidence-backed recommendations for one area.
  - AI-qualified reading: **0** (grade A, confidence medium). Breaking-change recommendations are rule-based.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A, confidence medium). The AI workflow builder and Instance AI change workflows when asked; nothing learns from runs without being asked.
  - Higher reading 2: Insights capture experience that the AI can read on request.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.
- **LRN-08 Learned changes are validated before they take effect**: **2** (grade A, confidence medium), facets: implemented, tested. AI-built workflows pass automated graph and JSON validation while the builder works (packages/@n8n/ai-workflow-builder.ee/src/code-builder/handlers/parse-validate-handler.ts:164-196), and type-availability policies check them at save and publish where enabled; evaluations can compare a workflow version against a dataset before publishing (packages/cli/src/evaluation.ee), but they are run by people and are not tied to the publish decision. Re-read at the v0.7 migration under the tightened boundary (AI-built workflows and agents count as learned or AI-made changes); the reading stands at 2.
  - Higher reading 3: If evaluations plus the review publish guard count as a pass or block decision.
  - AI-qualified reading: **2** (grade A, confidence medium). AI-built workflow versions can be evaluated against datasets before publishing, run by people (packages/cli/src/evaluation.ee).

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **2** (grade A, confidence medium). Evaluations run workflows over datasets and record metrics per test run (packages/cli/src/evaluation.ee, test-run.ee entity); agent evals rate agents (packages/cli/src/modules/agent-evals). Runs are not bound to a keep, revise or rollback decision.
  - Higher reading 3: Test runs give a baseline and metric per workflow version.
- **LRN-10 The improvement loop improves itself**: **1** (grade A, confidence low). The checks that gate the product's own AI-made changes are code that engineers change: builder graph and JSON validation (packages/@n8n/ai-workflow-builder.ee/src/code-builder/handlers/parse-validate-handler.ts:164-196, validation/programmatic.ts), policy checks registered as code (packages/cli/src/modules/policy-infrastructure/README.md), builder prompts (packages/@n8n/ai-workflow-builder.ee/src/prompts) and the AI evaluation suites in the repository (.github/workflows/ci-instance-ai-evals.yml, packages/@n8n/ai-workflow-builder.ee/evaluations). Operators keep their own evaluation datasets and evaluation workflows in the product (packages/cli/src/evaluation.ee) and agent evaluation datasets as data tables, behind a rollout flag (packages/cli/src/modules/agent-evals/agent-evals-flag-gate.ts); generated cases are drafted from the agent's configuration, not from failures (agent-eval-case-generation.service.ts:55-73). People improve these by hand; no failure or wrong pass is recorded against the check that missed it.
  - Higher reading 2: Evaluation workflows are versioned in workflow history, and opt-in, licensed type-availability policies are admin-edited rules enforced at save and publish (packages/cli/src/modules/type-availability-policies/README.md:17-25); but evaluations do not gate publishing and policy rules are not versioned.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **2** (grade A, confidence medium). Design-system components and axe-core scanning through a Playwright fixture (packages/testing/playwright/fixtures/a11y.ts) used by a few E2E tests.
  - Higher reading 3: The scans run in PR E2E jobs, but cover only a few pages.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A, confidence low). Audit events for users, workflows and credentials on the event bus, exported through log streaming; policy decisions are audited (packages/cli/src/modules/policy-infrastructure/policy-decision-audit.ts); workflow review activity is recorded (workflow-review-activity.service.ts); execution pruning sets retention. Scored at the lower reading under rule 11 because: Coverage across every entity and an in-product audit viewer were not verified.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence medium). Redaction policies for execution data (packages/cli/src/modules/redaction) and execution pruning; no data-subject export or tag-driven erasure.
- **GOV-04 Security as infrastructure**: **2** (grade A, confidence high), facets: implemented, tested. Scope-based permissions (packages/@n8n/permissions), admin type-availability policies enforced at save, publish, start and import (packages/cli/src/modules/type-availability-policies/README.md), and community package scanning (packages/@n8n/scan-community-package). Scanning does not gate every change: the pull-request security job runs only when files under .github/ change (.github/workflows/ci-pull-requests.yml:135, 496-502) and runs Poutine and Zizmor, which scan GitHub Actions workflows (sec-ci-reusable.yml:12-26); the container Trivy scan runs from the image build (docker-build-push.yml:757-790) with exit-code '0' (security-trivy-scan-callable.yml:51), so it reports but never fails. Corrected from 3 to 2 at the v0.7 migration, as the blind second and third ratings found.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence high), facets: implemented, tested. Workflow history with versions and restore (packages/cli/src/workflows/workflow-history); other surfaces (credentials, variables, data tables, settings) roll back only through source control. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Credentials, variables, data tables and settings roll back only through source control.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **3** (grade A, confidence medium). Workflow review requests with an inbox, decision policy and a publish guard that blocks publishing until approved (packages/cli/src/modules/workflow-reviews.ee, workflow-review-publish-guard.service.ts:11-29); git-backed environments let changes be staged on another instance first (packages/cli/src/modules/source-control.ee).
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **3** (grade A, confidence medium). Shared policy infrastructure runs registered @PolicyCheck classes at fixed points with cleared or blocked outcomes and audited decisions (packages/cli/src/modules/policy-infrastructure/README.md); review decision policy (workflow-review-decision-policy.ts).
- **GOV-08 Upgrade safety**: **3** (grade A, confidence medium). Nodes are versioned so existing workflows keep their typeVersion; a breaking-changes module scans workflows and configuration against the target version with a rule registry and migration services (packages/cli/src/modules/breaking-changes/README.md); node engine compatibility checks (packages/@n8n/node-engine-compatibility). Scored at the lower reading under rule 11 because: If migrations are applied rather than proposed, or breaking changes lack a policy exception.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence low). Scoped API keys and MCP scopes, approval cards for AI actions, policy checks and audit events; no idempotency keys or dry-run for API mutations.
  - Higher reading 3: Manual test executions with pinned data act as a dry-run for workflows.
  - AI-qualified reading: **2** (grade A, confidence medium). Scoped keys and approval cards for AI actions; no idempotency or dry-run.
    - Higher reading 3: Approval cards preview actions.
- **GOV-10 Bounded self-change**: **2** (grade A, confidence medium). Admin type-availability policies restrict which node types any change may use, enforced at save and publish (packages/cli/src/modules/type-availability-policies); no per-period or blast-radius limits.
  - AI-qualified reading: **2** (grade A, confidence medium). Type-availability policies restrict AI-built workflows.
- **GOV-11 Learning-input integrity**: **2** (grade A, confidence medium). Instance AI wraps resolved node parameters and external responses as untrusted data (packages/cli/src/modules/instance-ai/extract-resolved-node-parameters.ts:378-382); changes do not record their source inputs.
  - Higher reading 3: Untrusted data is separated systematically in Instance AI.
  - AI-qualified reading: **2** (grade A, confidence medium). Instance AI wraps external data as untrusted (extract-resolved-node-parameters.ts:378-382).
    - Higher reading 3: Systematic in Instance AI.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A, confidence medium). Kernel of users and SSO, projects and roles, workflows, credentials, executions, data tables, chat and triggers from any channel; no business-domain nouns in core.
  - Higher reading 4: Kernel primitives are not themselves configurable definitions, so 4 is a stretch.
- **EXP-02 A new domain is expressible without kernel change**: **2** (grade A, confidence low). New domains are expressible as workflows, credentials and data tables with no kernel change, but no domain shipped this way is evidenced inside the repository.
  - Higher reading 3: The public template gallery (grade C) proves many domains.
- **EXP-03 A domain ships as an installable bundle**: **2** (grade A, confidence low). Workflows export and import as JSON; source control pushes and pulls workflows, credential stubs, variables and tags between instances.
  - Higher reading 3: A source-control branch is a versioned, installable bundle.

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A, confidence medium). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence medium). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A, confidence low). New capabilities ship to all users of an instance.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence medium). The builder gets node types and workflow context; Instance AI resolves workflows, executions and node parameters live (packages/cli/src/modules/instance-ai/instance-context.service.ts).
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A, confidence high), facets: implemented, tested. Instance AI looks up workflows within the user's scopes (instance-ai.adapter.service.ts) with folder-scope tests (__tests__/instance-ai-folder-scope.test.ts, instance-ai-folder-scoped-listing.integration.test.ts).

### Quality

- **AIR-05 Offline AI evaluation**: **3** (grade A, confidence medium). Evaluation harness with evaluators, datasets and LangSmith runs for the workflow builder and Instance AI (packages/@n8n/ai-workflow-builder.ee/evaluations).
- **AIR-06 Regression gating before release**: **2** (grade A, confidence high), facets: implemented, tested. Instance AI evals run automatically on pull requests touching AI paths (.github/workflows/ci-instance-ai-evals.yml:18-21) and builder evals on minor releases (test-evals-ai-release.yml); no blocking threshold was found.
  - Higher reading 3: Results are posted on every relevant pull request.

### Governance

- **AIR-07 AI action tracing and auditability**: **2** (grade A, confidence high), facets: implemented, tested. Instance AI tracing service (packages/cli/src/modules/instance-ai/tracing) and audit events for approved actions; model and prompt version are not recorded with each change.
  - Higher reading 3: Approval cards and tracing together approach level 3.

### Operations

- **AIR-01 Model and provider portability and resilience**: **3** (grade A, confidence medium). AI agent nodes support a fallback model (packages/@n8n/nodes-langchain/nodes/agents/Agent/agents/utils.ts, ToolsAgent/common.ts), and operators choose models per node.
- **AIR-02 AI usage and per-customer cost controls**: **3** (grade A, confidence medium). Instance AI credits are tracked and enforced per instance with a credit display (packages/cli/src/modules/instance-ai/instance-ai-credit.service.ts, instance-ai-credit-display.ts).
- **AIR-08 Production quality, drift and feedback monitoring**: **2** (grade A, confidence medium). Evaluation metrics per test run and failure rates per workflow are recorded (packages/cli/src/evaluation.ee, modules/insights); no drift alerts.
