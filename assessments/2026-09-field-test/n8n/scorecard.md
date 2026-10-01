# n8n: EVOLVE v0.4 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.4.0 in this repository.

Scope: the n8n monorepo including source-available enterprise modules (*.ee), Instance AI, chat hub, MCP, task runners and CI. n8n Cloud operations and the external template gallery are out of scope.

## Reading

**SAL 2**, joint highest in the sample. The AI workflow builder asks clarifying questions and produces a plan for approval before it builds (DEL-01 2, DEL-04 2), and Insights reports failure rates per workflow (LRN-03 2), so both core loops reach L2. **Blocks L3:** controls, not workflow: migrations have no enforced online strategy (ARC-02 2), entity export has no restore test or recovery objectives (ARC-09 2), definition rollback covers workflows only (GOV-05 2), and AI changes have no declared blast-radius limit (GOV-10 2).

## Limits

Repository evidence only, master at the tip named above. Enterprise modules (*.ee) are included; they need a licence to run. n8n Cloud operations, the template gallery and community-node certification processes are outside the repository. Single rater.

---
Framework EVOLVE 0.4.0. Date 2026-09-30. Source github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master). Archetype **configurable-application-platform**.

Scope facts true: persistent_data, schema_changes, hosted_service, agent_mutations. False: multi_tenant, automatic_apply, code_release_path.

Coverage: 64 assessed, 0 not evidenced, 2 not applicable. Grades: 64 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 2 (Assisted) · Request → Release L2 · Issue → Fix L2 · Opportunity → Expansion L1**

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
| Tested backup and restore | ARC-09 ≥ 3 | 2 | fail |
| Tenant isolation | ARC-05 ≥ 3 | n/a | n/a |
| Security as infrastructure | GOV-04 ≥ 3 | 3 | pass |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 2 | fail |

### What blocks the next level

- **Request → Release to L3**: spine Build needs product build path ≥ 3 (has DEL-04 2); spine Verify needs DEL-06 ≥ 3 (has 2); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Intake needs DEL-01 ≥ 3 (has 2); architecture Foundation needs ARC-02 ≥ 3 (has 2); architecture Foundation needs ARC-09 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 2)
- **Issue → Fix to L3**: spine Build needs product build path ≥ 3 (has DEL-04 2, LRN-07 1); spine Verify needs DEL-06 ≥ 3 (has 2); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Detect needs LRN-03 ≥ 3 (has 2); stages Diagnose needs LRN-05 ≥ 3 (has 2); stages Propose needs LRN-06 ≥ 3 (has 2); architecture Foundation needs ARC-02 ≥ 3 (has 2); architecture Foundation needs ARC-09 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 2)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0)

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 2.1 | 2.1–2.4 | 2.1 | 2.1 | 2.1 |
| Velocity (DEL) | 2.1 | 2.1–2.7 | 2.1 | 2.1 | 2.1 |
| Open (MAL) | 2.3 | 2.3–3.0 | 2.3 | 2.3 | 2.3 |
| Learn (LRN) | 1.9 | 1.9–2.6 | 1.9 | 1.9 | 1.9 |
| Vet (GOV) | 2.3 | 2.3–2.9 | 2.3 | 2.3 | 2.3 |
| Expand (EXP) | 1.1 | 1.1–1.4 | 1.1 | 1.1 | 1.1 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Scale | 2.5 |
| ARC Capacity | 2.0 |
| ARC Resilience | 2.0 |
| DEL Intake | 2.0 |
| DEL Build | 2.0 |
| DEL Verify | 2.5 |
| DEL Release | 2.0 |
| MAL Data model | 1.7 |
| MAL APIs | 2.3 |
| MAL Interface | 2.0 |
| MAL Behaviour | 2.7 |
| MAL Extensions | 2.3 |
| MAL Integrations | 2.3 |
| MAL Agent interface | 3.0 |
| LRN Sense | 2.0 |
| LRN Diagnose and propose | 2.0 |
| LRN Learn from experience | 1.5 |
| LRN Measure | 2.0 |
| GOV Compliance and security | 2.3 |
| GOV Change control | 2.8 |
| GOV AI and self-change safety | 2.0 |
| EXP Expressible | 2.3 |
| EXP Discover | 0.0 |
| EXP Launch | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A |  | Data tables are real database tables queried with SQL; a workflow index supports search (packages/cli/src/modules/workflow-index); no definition-driven index mapping. |
| ARC-02 Safe schema and data migrations | assessed | 2 |  |  | A |  | TypeORM migrations with down steps for PostgreSQL and SQLite and a migration registry with tests (packages/@n8n/db/src/migrations); no enforced online strategy. |
| ARC-03 Horizontal scale of services | assessed | 3 |  |  | A | IT | Multi-main setup with leader election and Redis locks, and queue mode with separate workers (packages/cli/src/scaling/multi-main-setup.ee.ts, leader-election-client.ts, redis-lock.service.ts), covered by tests. |
| ARC-04 Reliable asynchronous work | assessed | 2 | 3 |  | A | IT | Queue mode runs executions on Bull with Redis (packages/cli/src/scaling/scaling.service.ts:100-105); leader election keeps schedules on one main. Failed executions are kept and can be retried by hand. |
| ARC-05 Tenant isolation and noisy-neighbour controls | not_applicable | excluded |  |  | - |  | Scope fact multi_tenant is false: One instance per customer; projects separate work inside an instance but are not isolated tenants. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 2 | 3 |  | A | IT | Performance E2E runs on pull requests (ci-pull-requests.yml:492, test-e2e-performance-reusable.yml) and nightly benchmarks (test-benchmark-nightly.yml, packages/@n8n/benchmark); per-surface limits not documented in the repository. |
| ARC-07 Service objectives defined and monitored | assessed | 2 |  |  | A |  | Prometheus metrics endpoint (packages/cli/src/metrics/prometheus); no published objectives. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | Code nodes run in separate task-runner processes (packages/@n8n/task-runner, task-runner-python); nodes have retry-on-fail and timeouts; community nodes run in-process. |
| ARC-09 Backup, restore and recovery | assessed | 2 |  |  | A |  | export:entities and import:entities move every database entity, optionally with data-table rows (packages/cli/src/commands/export/entities.ts); binary data and the encryption key are separate; no restore test or recovery objectives. |
| DEL-01 Request intake into a structured change specification | assessed | 2 | 3 |  | A |  | The AI workflow builder plans before building: it asks typed clarifying questions and produces a plan with a trigger, steps, suggested nodes and specifications that the user approves (packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts, agents/planner.agent.ts). The plan has no acceptance criteria or risk class. |
| DEL-02 Layers deploy independently | assessed | 2 |  |  | A |  | Main, worker, webhook and task-runner processes ship as separate container images from one monorepo build (12 Dockerfiles). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 | 3 |  | A |  | pnpm workspace packages, a module system with explicit registration, and import restrictions in package lint configs (packages/cli/eslint.config.mjs); Playwright architecture enforced by janitor (packages/testing/janitor). |
| DEL-04 AI implementation lane | assessed | 2 | 3 |  | A |  | AI workflow builder and Instance AI turn requests into workflow changes behind approvals, per instance. |
| DEL-05 Every change class has an automated pre-land check | assessed | 3 |  |  | A |  | Pull requests run unit, lint, E2E (including axe fixtures), database, smoke, frontend declaration, performance and security jobs with no draft filter (.github/workflows/ci-pull-requests.yml:280-508). |
| DEL-06 Verification surface | assessed | 2 | 3 |  | A |  | /healthz and /healthz/readiness (packages/cli/src/abstract-server.ts:139), Prometheus metrics (server.ts:172), instance version history (packages/cli/src/modules/instance-version-history) and settings APIs exposing configuration. Scored at the lower reading under rule 11 because: If the settings API is not a deployed-configuration snapshot. |
| DEL-07 Environment reproducibility | assessed | 3 |  |  | A |  | One preview codespace per pull request from the master prebuild (scripts/codespace-preview/preview.mjs), instance seeding scripts (scripts/instance-seeding), nightly benchmark infrastructure created and destroyed (test-benchmark-destroy-nightly.yml). |
| DEL-08 Machine verifiability | assessed | 2 | 3 |  | A |  | Playwright journeys (packages/testing/playwright/composables/journeys) with nightly coverage; no changed-path to journey map or adoption instrumentation at ship evidenced. |
| DEL-09 Staged exposure | assessed | 2 |  |  | A |  | Workflow versions are published deliberately, and frontend features are gated per instance; there are no cohort rollouts for workflow changes. |
| DEL-10 Kill switch | assessed | 2 |  |  | A |  | Workflows can be deactivated at runtime; there is no global kill switch for AI-made changes. |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: The AI lanes change workflows, not n8n code. |
| MAL-01 New entity type without code, DDL or deploy | assessed | 2 | 3 |  | A |  | Data tables are created in the UI with typed columns; a DDL service creates real tables without deploy, with their own permissions and public API (packages/cli/src/modules/data-table: data-table-ddl.service.ts, data-table-permissions.ts; packages/cli/src/public-api/v1/handlers/data-tables). Scored at the lower reading under rule 11 because: Data tables are storage for workflows, not general business-object types with forms and relations. |
| MAL-02 Field definitions carry type and validation | assessed | 2 | 3 |  | A |  | Data-table columns are typed (data-table-column.entity.ts); execution data has redaction policies (packages/cli/src/modules/redaction/redaction-policy.ts) but no field-level privacy classification. |
| MAL-03 Relationships and lifecycle states declarable | assessed | 1 |  |  | A |  | No declarable relations between data tables and no lifecycle states for user entities; workflow states are product-defined. |
| MAL-04 API per entity is generic or generated | assessed | 2 | 3 |  | A |  | One generic rows API serves every data table (public-api/v1/handlers/data-tables); the rest of the API is hand-written per resource. |
| MAL-05 API reshapes at runtime from definitions | assessed | 3 |  |  | A |  | Creating or altering a data table changes the rows API immediately, and each workflow exposed over MCP or webhooks changes the callable surface without a deploy. |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 | 3 |  | A |  | Public API v1 with an OpenAPI description and structured validation errors (packages/cli/src/public-api/index.ts, public-api-validation-error.ts); no typed client generation or dry-run. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A |  | Workflow canvases and Form trigger pages are stored as data and can be tested before activation (packages/nodes-base/nodes/Form); application layout is code. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | assessed | 2 |  |  | A |  | Generic grid for any data table and generic form rendering from field definitions; no configurable list and detail views for other objects. |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A |  | UI strings externalised in an i18n package with community locales (33 locale files); no tenant theme editor or text overrides. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A |  | Workflows are machine-readable rules (triggers, If, Switch, Filter and 400+ action nodes) composed in the UI across all integrations and data tables; testable with pinned data and by debugging past executions; versioned in workflow history (packages/cli/src/workflows/workflow-history); authored by the AI workflow builder and Instance AI (packages/@n8n/ai-workflow-builder.ee, packages/@n8n/instance-ai). Scored at the lower reading under rule 11 because: If replaying a past execution does not count as simulation against history. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 3 |  |  | A |  | Event bus with log-streaming destinations (webhook, syslog, Sentry) configured by admins (packages/cli/src/modules/log-streaming.ee, packages/workflow/src/message-event-bus.ts); webhook triggers; executions are logged and can be retried. |
| MAL-12 Sandboxed server-side hooks | assessed | 2 | 3 |  | A |  | Code nodes run in separate task-runner processes with memory, payload, concurrency and time limits (packages/@n8n/config/src/configs/runners.config.ts:36-55) and module allowlists (packages/@n8n/task-runner/src/config/js-runner-config.ts:5-8), triggered by events and webhooks. No egress control found. |
| MAL-13 Plugin lane breadth | assessed | 2 | 3 |  | A |  | Declarative and programmatic custom nodes, community packages installed from the UI (packages/cli/src/modules/community-packages), frontend extension SDK (packages/@n8n/extension-sdk), workflow templates and agent tools. Scored at the lower reading under rule 11 because: Theme and text are not plugin points. |
| MAL-14 Runtime isolation and dependency control | assessed | 2 | 3 |  | A |  | User code runs in isolated task-runner processes with resource limits; community nodes are scanned and can be restricted by policy but run with full trust in the main process. |
| MAL-15 Developer loop | assessed | 3 |  |  | A |  | Node CLI with dev server and linting (packages/@n8n/node-cli, eslint-plugin-community-nodes), source-control branches, execution logs and pinned-data testing against a live instance. |
| MAL-16 Canonical data model with a mapping layer | assessed | 2 | 3 |  | A |  | All connectors exchange a common item format and are joined by configurable mapping (expressions and field mapping in the UI), so a second system is mapping configuration (packages/workflow). Scored at the lower reading under rule 11 because: No canonical domain model, only a canonical transport format. |
| MAL-17 Connector definition or SDK | assessed | 3 | 4 |  | A |  | Node SDK with credential types for auth, trigger and polling patterns and versioning (packages/@n8n/create-node, packages/@n8n/node-cli); admins install community connectors in the UI. |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A |  | Path-versioned public API (packages/cli/src/public-api/v1) with documented breaking changes (packages/cli/BREAKING-CHANGES.md); no deprecation windows. |
| MAL-19 Machine-readable capability surface for agents | assessed | 3 | 4 |  | A |  | Instance MCP server with scoped API keys, per-workflow tool availability and MCP evaluations (packages/cli/src/modules/mcp: mcp-scopes.ts, mcp-tool-availability.ts, evaluations). |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A |  | Instance AI gives a natural-language interface to workflows, executions, credentials and nodes, with plans and approval cards before execution (packages/@n8n/instance-ai/docs/architecture.md, tools.md:18-82); chat hub for members (packages/cli/src/modules/chat-hub); Instance AI evaluations run in CI (.github/workflows/ci-instance-ai-evals.yml). |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A |  | The insights module collects execution counts, failures and time saved continuously and shows them in the product (packages/cli/src/modules/insights); vendor telemetry with redaction (packages/@n8n/telemetry). |
| LRN-02 Structured learning signals | assessed | 2 | 3 |  | A |  | Evaluation test runs record metrics per workflow (packages/@n8n/db/src/entities/test-run.ee.ts) and insights record per-workflow outcomes; no triage workflow. |
| LRN-03 User-issue detection | assessed | 2 | 3 |  | A |  | Insights report failures and failure rates per workflow (packages/cli/src/modules/insights/insights.service.ts:181-268) and error workflows fire on failures. |
| LRN-04 Cross-source mining inside the product | assessed | 1 |  |  | A |  | Insights cover executions only; nothing joins usage, support and delivery data. |
| LRN-05 Automated diagnosis | assessed | 2 | 3 |  | A |  | Failed executions keep the failing node, input and error; the AI assistant can explain a node error on request. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 2 |  |  | A |  | The breaking-changes detection report recommends fixes before upgrades (packages/cli/src/modules/breaking-changes/detection-report.ts): evidence-backed recommendations for one area. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 1 | 2 |  | A |  | The AI workflow builder and Instance AI change workflows when asked; nothing learns from runs without being asked. |
| LRN-08 Learned changes are validated before they take effect | assessed | 2 | 3 |  | A | IT | Evaluations can compare a workflow version against a dataset before publishing (packages/cli/src/evaluation.ee), but they are run by people and are not tied to the publish decision. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A |  | Evaluations run workflows over datasets and record metrics per test run (packages/cli/src/evaluation.ee, test-run.ee entity); agent evals rate agents (packages/cli/src/modules/agent-evals). Runs are not bound to a keep, revise or rollback decision. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 2 | 3 |  | A |  | Design-system components and axe-core scanning through a Playwright fixture (packages/testing/playwright/fixtures/a11y.ts) used by a few E2E tests. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A |  | Audit events for users, workflows and credentials on the event bus, exported through log streaming; policy decisions are audited (packages/cli/src/modules/policy-infrastructure/policy-decision-audit.ts); workflow review activity is recorded (workflow-review-activity.service.ts); execution pruning sets retention. Scored at the lower reading under rule 11 because: Coverage across every entity and an in-product audit viewer were not verified. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A |  | Redaction policies for execution data (packages/cli/src/modules/redaction) and execution pruning; no data-subject export or tag-driven erasure. |
| GOV-04 Security as infrastructure | assessed | 3 |  |  | A | IT | Scope-based permissions (packages/@n8n/permissions), admin type-availability policies enforced at save, publish, start and import (packages/cli/src/modules/type-availability-policies/README.md), community package scanning (packages/@n8n/scan-community-package), and security jobs on pull requests (.github/workflows/ci-pull-requests.yml:499, sec-ci-reusable.yml, security-trivy-scan-callable.yml). |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 | 3 |  | A | IT | Workflow history with versions and restore (packages/cli/src/workflows/workflow-history); other surfaces (credentials, variables, data tables, settings) roll back only through source control. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 3 |  |  | A |  | Workflow review requests with an inbox, decision policy and a publish guard that blocks publishing until approved (packages/cli/src/modules/workflow-reviews.ee, workflow-review-publish-guard.service.ts:11-29); git-backed environments let changes be staged on another instance first (packages/cli/src/modules/source-control.ee). |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 3 |  |  | A |  | Shared policy infrastructure runs registered @PolicyCheck classes at fixed points with cleared or blocked outcomes and audited decisions (packages/cli/src/modules/policy-infrastructure/README.md); review decision policy (workflow-review-decision-policy.ts). |
| GOV-08 Upgrade safety | assessed | 3 | 4 |  | A |  | Nodes are versioned so existing workflows keep their typeVersion; a breaking-changes module scans workflows and configuration against the target version with a rule registry and migration services (packages/cli/src/modules/breaking-changes/README.md); node engine compatibility checks (packages/@n8n/node-engine-compatibility). Scored at the lower reading under rule 11 because: If migrations are applied rather than proposed, or breaking changes lack a policy exception. |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A |  | Scoped API keys and MCP scopes, approval cards for AI actions, policy checks and audit events; no idempotency keys or dry-run for API mutations. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A |  | Admin type-availability policies restrict which node types any change may use, enforced at save and publish (packages/cli/src/modules/type-availability-policies); no per-period or blast-radius limits. |
| GOV-11 Learning-input integrity | assessed | 2 | 3 |  | A |  | Instance AI wraps resolved node parameters and external responses as untrusted data (packages/cli/src/modules/instance-ai/extract-resolved-node-parameters.ts:378-382); changes do not record their source inputs. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 | 4 |  | A |  | Kernel of users and SSO, projects and roles, workflows, credentials, executions, data tables, chat and triggers from any channel; no business-domain nouns in core. |
| EXP-02 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A |  | New domains are expressible as workflows, credentials and data tables with no kernel change, but no domain shipped this way is evidenced inside the repository. |
| EXP-03 A domain ships as an installable bundle | assessed | 2 | 3 |  | A |  | Workflows export and import as JSON; source control pushes and pulls workflows, credential stubs, variables and tags between instances. |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A |  | No record of unmet intents was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 |  |  | A |  | New capabilities ship to all users of an instance. |

Facets: I implemented, T tested, O operated.

