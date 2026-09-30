# n8n: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the n8n monorepo including source-available enterprise modules (*.ee), Instance AI, chat hub, MCP, task runners and CI. n8n Cloud operations and the external template gallery are out of scope.

## Reading

**Strongest:** Governance (2.8), the best in the sample. Workflow reviews block publishing until approved, a shared policy engine audits decisions, admins set type-availability policies, and a breaking-changes module keeps workflows working across upgrades (F2 3, F3 3, F4 4). Workflows are machine-readable, versioned and AI-authored rules (D1 4). **Largest gap:** Learning (1.8). Nothing learns from runs without being asked (P1 1), and evaluations are not tied to the publish decision (P2 2), so the measure stage of the closed loop fails.

## Limits

Repository evidence only, master at the tip named above. Enterprise modules (*.ee) are included; they need a licence to run. n8n Cloud operations, the template gallery and community-node certification processes are outside the repository. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master). Archetype **configurable-application-platform**.

Coverage: 49 assessed, 0 not evidenced, 0 not applicable. Grades: 49 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.4 | mechanism | 2.4–2.7 | 2.4 | 2.4 | 2.4 |
| governance | 2.8 | productised | 2.8 | 2.8 | 2.8 | 2.8 |
| learning | 1.8 | mechanism | 1.8–2.5 | 1.8 | 1.8 | 1.8 |
| factory | 2.5 | productised | 2.5–2.7 | 2.5 | 2.5 | 2.5 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.3 | 2.3 |
| Governance | 2.8 | 2.8 |
| Learning | 1.8 | 1.8 |
| Factory | 2.5 | 2.5 |
| Agent Interface | 2.7 | 2.7 |
| Extension Surface | 2.7 | 2.7 |
| Operational Scalability | 2.0 | 2.0 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 2 pass | 2 pass |
| propose | M1, P1 | 2 | 2 pass | 2 pass |
| review | F2 | 2 | 3 pass | 3 pass |
| gate | F3 | 3 | 3 pass | 3 pass |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 2 fail | 2 fail |
| verify | L1 | 2 | 3 pass | 3 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| A Entity and schema as data | 2.0 |
| B API surface generation | 2.3 |
| C Rendering follows the definition | 2.0 |
| D Behaviour as data | 3.0 |
| E Compliance and security as infrastructure | 2.5 |
| F Change control | 3.0 |
| G Performance under genericity | 2.0 |
| H Stack flexibility and verification | 2.3 |
| I Extension ecosystem | 2.7 |
| J Observe | 2.0 |
| K Agent and conversational readiness | 2.7 |
| L Factory surfaces | 2.7 |
| M Advise and act | 2.0 |
| N Integration and connector extensibility | 2.7 |
| O Adjacent-domain expansion | 2.3 |
| P Learn from experience | 1.5 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | assessed | 3 | 2 |  | A | Data tables are created in the UI with typed columns; a DDL service creates real tables without deploy, with their own permissions and public API (packages/cli/src/modules/data-table: data-table-ddl.service.ts, data-table-permissions.ts; packages/cli/src/public-api/v1/handlers/data-tables). |
| A2 Field definitions carry type and validation | assessed | 2 | 3 |  | A | Data-table columns are typed (data-table-column.entity.ts); execution data has redaction policies (packages/cli/src/modules/redaction/redaction-policy.ts) but no field-level privacy classification. |
| A3 Relationships and lifecycle states declarable | assessed | 1 |  |  | A | No declarable relations between data tables and no lifecycle states for user entities; workflow states are product-defined. |
| B1 API per entity is generic or generated | assessed | 2 | 3 |  | A | One generic rows API serves every data table (public-api/v1/handlers/data-tables); the rest of the API is hand-written per resource. |
| B2 API reshapes at runtime from definitions | assessed | 3 |  |  | A | Creating or altering a data table changes the rows API immediately, and each workflow exposed over MCP or webhooks changes the callable surface without a deploy. |
| B3 Machine-readable contract with introspection and dry-run | assessed | 2 | 3 |  | A | Public API v1 with an OpenAPI description and structured validation errors (packages/cli/src/public-api/index.ts, public-api-validation-error.ts); no typed client generation or dry-run. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A | Workflow canvases and Form trigger pages are stored as data and can be tested before activation (packages/nodes-base/nodes/Form); application layout is code. |
| C2 Generic list, detail and intake widgets from definition plus view spec | assessed | 2 |  |  | A | Generic grid for any data table and generic form rendering from field definitions; no configurable list and detail views for other objects. |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A | UI strings externalised in an i18n package with community locales (33 locale files); no tenant theme editor or text overrides. |
| D1 Rules engine with declarative conditions and actions | assessed | 4 | 3 |  | A | Workflows are machine-readable rules (triggers, If, Switch, Filter and 400+ action nodes) composed in the UI across all integrations and data tables; testable with pinned data and by debugging past executions; versioned in workflow history (packages/cli/src/workflows/workflow-history); authored by the AI workflow builder and Instance AI (packages/@n8n/ai-workflow-builder.ee, packages/@n8n/instance-ai). |
| D2 Event model with webhooks or subscriptions and retry | assessed | 3 |  |  | A | Event bus with log-streaming destinations (webhook, syslog, Sentry) configured by admins (packages/cli/src/modules/log-streaming.ee, packages/workflow/src/message-event-bus.ts); webhook triggers; executions are logged and can be retried. |
| D3 Sandboxed server-side hooks | assessed | 2 | 3 |  | A | Code nodes run in separate task-runner processes with memory, payload, concurrency and time limits (packages/@n8n/config/src/configs/runners.config.ts:36-55) and module allowlists (packages/@n8n/task-runner/src/config/js-runner-config.ts:5-8), triggered by events and webhooks. No egress control found. |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 2 | 3 |  | A | Design-system components and axe-core scanning through a Playwright fixture (packages/testing/playwright/fixtures/a11y.ts) used by a few E2E tests. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 3 | 2 |  | A | Audit events for users, workflows and credentials on the event bus, exported through log streaming; policy decisions are audited (packages/cli/src/modules/policy-infrastructure/policy-decision-audit.ts); workflow review activity is recorded (workflow-review-activity.service.ts); execution pruning sets retention. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A | Redaction policies for execution data (packages/cli/src/modules/redaction) and execution pruning; no data-subject export or tag-driven erasure. |
| E4 Security as infrastructure | assessed | 3 |  |  | A | Scope-based permissions (packages/@n8n/permissions), admin type-availability policies enforced at save, publish, start and import (packages/cli/src/modules/type-availability-policies/README.md), community package scanning (packages/@n8n/scan-community-package), and security jobs on pull requests (.github/workflows/ci-pull-requests.yml:499, sec-ci-reusable.yml, security-trivy-scan-callable.yml). |
| F1 Definitions and layouts versioned with rollback | assessed | 2 | 3 |  | A | Workflow history with versions and restore (packages/cli/src/workflows/workflow-history); other surfaces (credentials, variables, data tables, settings) roll back only through source control. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 3 |  |  | A | Workflow review requests with an inbox, decision policy and a publish guard that blocks publishing until approved (packages/cli/src/modules/workflow-reviews.ee, workflow-review-publish-guard.service.ts:11-29); git-backed environments let changes be staged on another instance first (packages/cli/src/modules/source-control.ee). |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 3 |  |  | A | Shared policy infrastructure runs registered @PolicyCheck classes at fixed points with cleared or blocked outcomes and audited decisions (packages/cli/src/modules/policy-infrastructure/README.md); review decision policy (workflow-review-decision-policy.ts). |
| F4 Upgrade safety | assessed | 4 | 3 |  | A | Nodes are versioned so existing workflows keep their typeVersion; a breaking-changes module scans workflows and configuration against the target version with a rule registry and migration services (packages/cli/src/modules/breaking-changes/README.md); node engine compatibility checks (packages/@n8n/node-engine-compatibility). |
| G1 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A | Data tables are real database tables queried with SQL; a workflow index supports search (packages/cli/src/modules/workflow-index); no definition-driven index mapping. |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A | One instance per customer with projects inside it; concurrency limits and queue mode with workers; no per-tenant noisy-neighbour detection. |
| G3 Ceilings measured, not discovered in incidents | assessed | 2 | 3 |  | A | Performance E2E runs on pull requests (ci-pull-requests.yml:492, test-e2e-performance-reusable.yml) and nightly benchmarks (test-benchmark-nightly.yml, packages/@n8n/benchmark); per-surface limits not documented in the repository. |
| H1 Layers deploy independently | assessed | 2 |  |  | A | Main, worker, webhook and task-runner processes ship as separate container images from one monorepo build (12 Dockerfiles). |
| H2 Module boundaries enforced by tooling | assessed | 2 | 3 |  | A | pnpm workspace packages, a module system with explicit registration, and import restrictions in package lint configs (packages/cli/eslint.config.mjs); Playwright architecture enforced by janitor (packages/testing/janitor). |
| H3 Every change class has an automated pre-land check | assessed | 3 |  |  | A | Pull requests run unit, lint, E2E (including axe fixtures), database, smoke, frontend declaration, performance and security jobs with no draft filter (.github/workflows/ci-pull-requests.yml:280-508). |
| I1 Plugin lane breadth | assessed | 3 | 2 |  | A | Declarative and programmatic custom nodes, community packages installed from the UI (packages/cli/src/modules/community-packages), frontend extension SDK (packages/@n8n/extension-sdk), workflow templates and agent tools. |
| I2 Runtime isolation and dependency control | assessed | 2 | 3 |  | A | User code runs in isolated task-runner processes with resource limits; community nodes are scanned and can be restricted by policy but run with full trust in the main process. |
| I3 Developer loop | assessed | 3 |  |  | A | Node CLI with dev server and linting (packages/@n8n/node-cli, eslint-plugin-community-nodes), source-control branches, execution logs and pinned-data testing against a live instance. |
| K1 Machine-readable capability surface for agents | assessed | 3 | 4 |  | A | Instance MCP server with scoped API keys, per-workflow tool availability and MCP evaluations (packages/cli/src/modules/mcp: mcp-scopes.ts, mcp-tool-availability.ts, evaluations). |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A | Instance AI gives a natural-language interface to workflows, executions, credentials and nodes, with plans and approval cards before execution (packages/@n8n/instance-ai/docs/architecture.md, tools.md:18-82); chat hub for members (packages/cli/src/modules/chat-hub); Instance AI evaluations run in CI (.github/workflows/ci-instance-ai-evals.yml). |
| K3 Agent-safe actions | assessed | 2 | 3 |  | A | Scoped API keys and MCP scopes, approval cards for AI actions, policy checks and audit events; no idempotency keys or dry-run for API mutations. |
| N1 Canonical data model with a mapping layer | assessed | 3 | 2 |  | A | All connectors exchange a common item format and are joined by configurable mapping (expressions and field mapping in the UI), so a second system is mapping configuration (packages/workflow). |
| N2 Connector definition or SDK | assessed | 3 | 4 |  | A | Node SDK with credential types for auth, trigger and polling patterns and versioning (packages/@n8n/create-node, packages/@n8n/node-cli); admins install community connectors in the UI. |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | Path-versioned public API (packages/cli/src/public-api/v1) with documented breaking changes (packages/cli/BREAKING-CHANGES.md); no deprecation windows. |
| O1 Kernel concepts are domain-neutral | assessed | 3 | 4 |  | A | Kernel of users and SSO, projects and roles, workflows, credentials, executions, data tables, chat and triggers from any channel; no business-domain nouns in core. |
| O2 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A | New domains are expressible as workflows, credentials and data tables with no kernel change, but no domain shipped this way is evidenced inside the repository. |
| O3 A domain ships as an installable bundle | assessed | 2 | 3 |  | A | Workflows export and import as JSON; source control pushes and pulls workflows, credential stubs, variables and tags between instances. |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A | The insights module collects execution counts, failures and time saved continuously and shows them in the product (packages/cli/src/modules/insights); vendor telemetry with redaction (packages/@n8n/telemetry). |
| J2 Structured learning signals | assessed | 2 | 3 |  | A | Evaluation test runs record metrics per workflow (packages/@n8n/db/src/entities/test-run.ee.ts) and insights record per-workflow outcomes; no triage workflow. |
| J3 Cross-source mining inside the product | assessed | 1 |  |  | A | Insights cover executions only; nothing joins usage, support and delivery data. |
| M1 Ranked, evidence-backed proposals for change | assessed | 2 |  |  | A | The breaking-changes detection report recommends fixes before upgrades (packages/cli/src/modules/breaking-changes/detection-report.ts): evidence-backed recommendations for one area. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 2 | 3 |  | A | AI workflow builder and Instance AI turn requests into workflow changes behind approvals, per instance. |
| M4 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A | Evaluations run workflows over datasets and record metrics per test run (packages/cli/src/evaluation.ee, test-run.ee entity); agent evals rate agents (packages/cli/src/modules/agent-evals). Runs are not bound to a keep, revise or rollback decision. |
| P1 The product turns its own operating experience into candidate changes | assessed | 1 | 2 |  | A | The AI workflow builder and Instance AI change workflows when asked; nothing learns from runs without being asked. |
| P2 Learned changes are validated before they take effect | assessed | 2 | 3 |  | A | Evaluations can compare a workflow version against a dataset before publishing (packages/cli/src/evaluation.ee), but they are run by people and are not tied to the publish decision. |
| L1 Verification surface | assessed | 3 | 2 |  | A | /healthz and /healthz/readiness (packages/cli/src/abstract-server.ts:139), Prometheus metrics (server.ts:172), instance version history (packages/cli/src/modules/instance-version-history) and settings APIs exposing configuration. |
| L2 Environment reproducibility | assessed | 3 |  |  | A | One preview codespace per pull request from the master prebuild (scripts/codespace-preview/preview.mjs), instance seeding scripts (scripts/instance-seeding), nightly benchmark infrastructure created and destroyed (test-benchmark-destroy-nightly.yml). |
| L3 Machine verifiability | assessed | 2 | 3 |  | A | Playwright journeys (packages/testing/playwright/composables/journeys) with nightly coverage; no changed-path to journey map or adoption instrumentation at ship evidenced. |

