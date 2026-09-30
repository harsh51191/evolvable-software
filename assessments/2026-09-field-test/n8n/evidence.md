# n8n evidence

Read at github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **3** (grade A). Data tables are created in the UI with typed columns; a DDL service creates real tables without deploy, with their own permissions and public API (packages/cli/src/modules/data-table: data-table-ddl.service.ts, data-table-permissions.ts; packages/cli/src/public-api/v1/handlers/data-tables).
  - Alternate reading 2: Data tables are storage for workflows, not general business-object types with forms and relations.
- **A2 Field definitions carry type and validation**: **2** (grade A). Data-table columns are typed (data-table-column.entity.ts); execution data has redaction policies (packages/cli/src/modules/redaction/redaction-policy.ts) but no field-level privacy classification.
  - Alternate reading 3: Redaction policies are a consumed privacy control, though not a field tag.
- **A3 Relationships and lifecycle states declarable**: **1** (grade A). No declarable relations between data tables and no lifecycle states for user entities; workflow states are product-defined.
## B API surface generation

- **B1 API per entity is generic or generated**: **2** (grade A). One generic rows API serves every data table (public-api/v1/handlers/data-tables); the rest of the API is hand-written per resource.
  - Alternate reading 3: Every defined entity type (data table) gets API presence without per-entity code.
- **B2 API reshapes at runtime from definitions**: **3** (grade A). Creating or altering a data table changes the rows API immediately, and each workflow exposed over MCP or webhooks changes the callable surface without a deploy.
- **B3 Machine-readable contract with introspection and dry-run**: **2** (grade A). Public API v1 with an OpenAPI description and structured validation errors (packages/cli/src/public-api/index.ts, public-api-validation-error.ts); no typed client generation or dry-run.
  - Alternate reading 3: Shared API types package (packages/@n8n/api-types) serves typed clients internally.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Workflow canvases and Form trigger pages are stored as data and can be tested before activation (packages/nodes-base/nodes/Form); application layout is code.
  - Alternate reading 3: Forms are admin-authored, validated and previewable layouts.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **2** (grade A). Generic grid for any data table and generic form rendering from field definitions; no configurable list and detail views for other objects.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). UI strings externalised in an i18n package with community locales (33 locale files); no tenant theme editor or text overrides.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **4** (grade A). Workflows are machine-readable rules (triggers, If, Switch, Filter and 400+ action nodes) composed in the UI across all integrations and data tables; testable with pinned data and by debugging past executions; versioned in workflow history (packages/cli/src/workflows/workflow-history); authored by the AI workflow builder and Instance AI (packages/@n8n/ai-workflow-builder.ee, packages/@n8n/instance-ai).
  - Alternate reading 3: If replaying a past execution does not count as simulation against history.
- **D2 Event model with webhooks or subscriptions and retry**: **3** (grade A). Event bus with log-streaming destinations (webhook, syslog, Sentry) configured by admins (packages/cli/src/modules/log-streaming.ee, packages/workflow/src/message-event-bus.ts); webhook triggers; executions are logged and can be retried.
- **D3 Sandboxed server-side hooks**: **2** (grade A). Code nodes run in separate task-runner processes with memory, payload, concurrency and time limits (packages/@n8n/config/src/configs/runners.config.ts:36-55) and module allowlists (packages/@n8n/task-runner/src/config/js-runner-config.ts:5-8), triggered by events and webhooks. No egress control found.
  - Alternate reading 3: Every clause except egress control is met.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **2** (grade A). Design-system components and axe-core scanning through a Playwright fixture (packages/testing/playwright/fixtures/a11y.ts) used by a few E2E tests.
  - Alternate reading 3: The scans run in PR E2E jobs, but cover only a few pages.
- **E2 Audit generic over entities, definition changes and approvals**: **3** (grade A). Audit events for users, workflows and credentials on the event bus, exported through log streaming; policy decisions are audited (packages/cli/src/modules/policy-infrastructure/policy-decision-audit.ts); workflow review activity is recorded (workflow-review-activity.service.ts); execution pruning sets retention.
  - Alternate reading 2: Coverage across every entity and an in-product audit viewer were not verified.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Redaction policies for execution data (packages/cli/src/modules/redaction) and execution pruning; no data-subject export or tag-driven erasure.
- **E4 Security as infrastructure**: **3** (grade A). Scope-based permissions (packages/@n8n/permissions), admin type-availability policies enforced at save, publish, start and import (packages/cli/src/modules/type-availability-policies/README.md), community package scanning (packages/@n8n/scan-community-package), and security jobs on pull requests (.github/workflows/ci-pull-requests.yml:499, sec-ci-reusable.yml, security-trivy-scan-callable.yml).
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Workflow history with versions and restore (packages/cli/src/workflows/workflow-history); other surfaces (credentials, variables, data tables, settings) roll back only through source control.
  - Alternate reading 3: Workflows are the main customisation surface and have full history and restore.
- **F2 Proposal, review, apply as a first-class object with preview**: **3** (grade A). Workflow review requests with an inbox, decision policy and a publish guard that blocks publishing until approved (packages/cli/src/modules/workflow-reviews.ee, workflow-review-publish-guard.service.ts:11-29); git-backed environments let changes be staged on another instance first (packages/cli/src/modules/source-control.ee).
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **3** (grade A). Shared policy infrastructure runs registered @PolicyCheck classes at fixed points with cleared or blocked outcomes and audited decisions (packages/cli/src/modules/policy-infrastructure/README.md); review decision policy (workflow-review-decision-policy.ts).
- **F4 Upgrade safety**: **4** (grade A). Nodes are versioned so existing workflows keep their typeVersion; a breaking-changes module scans workflows and configuration against the target version with a rule registry and migration services (packages/cli/src/modules/breaking-changes/README.md); node engine compatibility checks (packages/@n8n/node-engine-compatibility).
  - Alternate reading 3: If migrations are applied rather than proposed, or breaking changes lack a policy exception.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **2** (grade A). Data tables are real database tables queried with SQL; a workflow index supports search (packages/cli/src/modules/workflow-index); no definition-driven index mapping.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). One instance per customer with projects inside it; concurrency limits and queue mode with workers; no per-tenant noisy-neighbour detection.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). Performance E2E runs on pull requests (ci-pull-requests.yml:492, test-e2e-performance-reusable.yml) and nightly benchmarks (test-benchmark-nightly.yml, packages/@n8n/benchmark); per-surface limits not documented in the repository.
  - Alternate reading 3: A performance suite gates pull requests; only documented limits are missing.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **2** (grade A). Main, worker, webhook and task-runner processes ship as separate container images from one monorepo build (12 Dockerfiles).
- **H2 Module boundaries enforced by tooling**: **2** (grade A). pnpm workspace packages, a module system with explicit registration, and import restrictions in package lint configs (packages/cli/eslint.config.mjs); Playwright architecture enforced by janitor (packages/testing/janitor).
  - Alternate reading 3: Lint-enforced boundaries plus API types between packages.
- **H3 Every change class has an automated pre-land check**: **3** (grade A). Pull requests run unit, lint, E2E (including axe fixtures), database, smoke, frontend declaration, performance and security jobs with no draft filter (.github/workflows/ci-pull-requests.yml:280-508).
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Declarative and programmatic custom nodes, community packages installed from the UI (packages/cli/src/modules/community-packages), frontend extension SDK (packages/@n8n/extension-sdk), workflow templates and agent tools.
  - Alternate reading 2: Theme and text are not plugin points.
- **I2 Runtime isolation and dependency control**: **2** (grade A). User code runs in isolated task-runner processes with resource limits; community nodes are scanned and can be restricted by policy but run with full trust in the main process.
  - Alternate reading 3: Code-node isolation meets every clause except egress.
- **I3 Developer loop**: **3** (grade A). Node CLI with dev server and linting (packages/@n8n/node-cli, eslint-plugin-community-nodes), source-control branches, execution logs and pinned-data testing against a live instance.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **3** (grade A). Instance MCP server with scoped API keys, per-workflow tool availability and MCP evaluations (packages/cli/src/modules/mcp: mcp-scopes.ts, mcp-tool-availability.ts, evaluations).
  - Alternate reading 4: Each exposed workflow becomes a tool whose schema comes from its trigger definition.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). Instance AI gives a natural-language interface to workflows, executions, credentials and nodes, with plans and approval cards before execution (packages/@n8n/instance-ai/docs/architecture.md, tools.md:18-82); chat hub for members (packages/cli/src/modules/chat-hub); Instance AI evaluations run in CI (.github/workflows/ci-instance-ai-evals.yml).
  - Alternate reading 4: Instance AI aims to make workflows reachable without the UI and is evaluated in CI.
- **K3 Agent-safe actions**: **2** (grade A). Scoped API keys and MCP scopes, approval cards for AI actions, policy checks and audit events; no idempotency keys or dry-run for API mutations.
  - Alternate reading 3: Manual test executions with pinned data act as a dry-run for workflows.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). All connectors exchange a common item format and are joined by configurable mapping (expressions and field mapping in the UI), so a second system is mapping configuration (packages/workflow).
  - Alternate reading 2: No canonical domain model, only a canonical transport format.
- **N2 Connector definition or SDK**: **3** (grade A). Node SDK with credential types for auth, trigger and polling patterns and versioning (packages/@n8n/create-node, packages/@n8n/node-cli); admins install community connectors in the UI.
  - Alternate reading 4: Verified community nodes amount to certification.
- **N3 Stable versioned contracts**: **2** (grade A). Path-versioned public API (packages/cli/src/public-api/v1) with documented breaking changes (packages/cli/BREAKING-CHANGES.md); no deprecation windows.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of users and SSO, projects and roles, workflows, credentials, executions, data tables, chat and triggers from any channel; no business-domain nouns in core.
  - Alternate reading 4: Kernel primitives are not themselves configurable definitions, so 4 is a stretch.
- **O2 A new domain is expressible without kernel change**: **2** (grade A). New domains are expressible as workflows, credentials and data tables with no kernel change, but no domain shipped this way is evidenced inside the repository.
  - Alternate reading 3: The public template gallery (grade C) proves many domains.
- **O3 A domain ships as an installable bundle**: **2** (grade A). Workflows export and import as JSON; source control pushes and pulls workflows, credential stubs, variables and tags between instances.
  - Alternate reading 3: A source-control branch is a versioned, installable bundle.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). The insights module collects execution counts, failures and time saved continuously and shows them in the product (packages/cli/src/modules/insights); vendor telemetry with redaction (packages/@n8n/telemetry).
- **J2 Structured learning signals**: **2** (grade A). Evaluation test runs record metrics per workflow (packages/@n8n/db/src/entities/test-run.ee.ts) and insights record per-workflow outcomes; no triage workflow.
  - Alternate reading 3: Test runs are linked to the workflow they evaluate.
- **J3 Cross-source mining inside the product**: **1** (grade A). Insights cover executions only; nothing joins usage, support and delivery data.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **2** (grade A). The breaking-changes detection report recommends fixes before upgrades (packages/cli/src/modules/breaking-changes/detection-report.ts): evidence-backed recommendations for one area.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **2** (grade A). AI workflow builder and Instance AI turn requests into workflow changes behind approvals, per instance.
  - Alternate reading 3: The lane is broad and governed, not narrow and engineer-run.
- **M4 Post-change impact is measured against a declared baseline**: **2** (grade A). Evaluations run workflows over datasets and record metrics per test run (packages/cli/src/evaluation.ee, test-run.ee entity); agent evals rate agents (packages/cli/src/modules/agent-evals). Runs are not bound to a keep, revise or rollback decision.
  - Alternate reading 3: Test runs give a baseline and metric per workflow version.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **1** (grade A). The AI workflow builder and Instance AI change workflows when asked; nothing learns from runs without being asked.
  - Alternate reading 2: Insights capture experience that the AI can read on request.
- **P2 Learned changes are validated before they take effect**: **2** (grade A). Evaluations can compare a workflow version against a dataset before publishing (packages/cli/src/evaluation.ee), but they are run by people and are not tied to the publish decision.
  - Alternate reading 3: If evaluations plus the review publish guard count as a pass or block decision.
## L Factory surfaces

- **L1 Verification surface**: **3** (grade A). /healthz and /healthz/readiness (packages/cli/src/abstract-server.ts:139), Prometheus metrics (server.ts:172), instance version history (packages/cli/src/modules/instance-version-history) and settings APIs exposing configuration.
  - Alternate reading 2: If the settings API is not a deployed-configuration snapshot.
- **L2 Environment reproducibility**: **3** (grade A). One preview codespace per pull request from the master prebuild (scripts/codespace-preview/preview.mjs), instance seeding scripts (scripts/instance-seeding), nightly benchmark infrastructure created and destroyed (test-benchmark-destroy-nightly.yml).
- **L3 Machine verifiability**: **2** (grade A). Playwright journeys (packages/testing/playwright/composables/journeys) with nightly coverage; no changed-path to journey map or adoption instrumentation at ship evidenced.
  - Alternate reading 3: Telemetry instruments features; janitor enforces test architecture.
