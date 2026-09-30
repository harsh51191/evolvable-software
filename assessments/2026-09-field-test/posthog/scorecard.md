# PostHog: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the posthog monorepo (Django app, products/, ee/, Node CDP services, Rust services, MCP service, CI). PostHog Cloud operations and separate SDK repositories are out of scope. Many products here run PostHog's evolve loop for customers' software; see the construct note in the reading.

## Reading

**Strongest:** Factory (2.7) and Agent Interface (3.0): independent services, enforced module boundaries, per-PR preview environments, and MCP tools generated from the API schema. Approval policies give real change control (F3 3). **The self rule matters here:** Signals and Tasks run the evolve loop on customers' software, so they are recorded but not scored. PostHog's own learning is narrow: it materialises hot columns from its own query logs without being asked (P1 3), with no baseline evaluation (P2 1).

## Limits

Repository evidence only, master at the tip named above. The repository is very large (about 55,000 files); only the areas cited were read, so some capabilities are likely under-scored (for example versioning and rollback). Cloud operations, dogfooding practice and incident history are invisible here. Egress controls for Hog functions were searched for and not found; they may exist in infrastructure code outside the paths read. Single rater. Under the v0.3 self rule, Signals, Tasks and experiments on customers' products are excluded from scoring.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master). Archetype **focused-application**.

Coverage: 41 assessed, 0 not evidenced, 8 not applicable. Grades: 41 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.6 | productised | 2.6–2.8 | 2.6 | 2.6 | 2.2 |
| governance | 2.3 | mechanism | 2.3–2.6 | 2.3 | 2.3 | 2.3 |
| learning | 2.0 | mechanism | 2.0–2.7 | 2.0 | 2.0 | 2.0 |
| factory | 2.7 | productised | 2.7–2.8 | 2.7 | 2.7 | 2.7 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.7 | 2.7 |
| Governance | 2.3 | 2.3 |
| Learning | 2.0 | 2.0 |
| Factory | 2.7 | 2.7 |
| Agent Interface | 3.0 | 3.0 |
| Extension Surface | 2.3 | 2.3 |
| Operational Scalability | 2.3 | 2.3 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 1 fail | 1 fail |
| propose | M1, P1 | 2 | 3 pass | 3 pass |
| review | F2 | 2 | 2 pass | 2 pass |
| gate | F3 | 3 | 3 pass | 3 pass |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 2 fail | 2 fail |
| verify | L1 | 2 | 2 pass | 2 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| A Entity and schema as data | 3.0 |
| B API surface generation | 3.0 |
| C Rendering follows the definition | 2.0 |
| D Behaviour as data | 2.7 |
| E Compliance and security as infrastructure | 2.3 |
| F Change control | 2.3 |
| G Performance under genericity | 2.3 |
| H Stack flexibility and verification | 2.7 |
| I Extension ecosystem | 2.3 |
| J Observe | 2.0 |
| K Agent and conversational readiness | 3.0 |
| L Factory surfaces | 2.7 |
| M Advise and act | 2.0 |
| N Integration and connector extensibility | 2.3 |
| P Learn from experience | 2.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). Warehouse views and group types are runtime data models, created by analysts through queries. |
| A2 Field definitions carry type and validation | assessed | 3 |  |  | A | Event and person property definitions carry a validated property_type and format editable in Data management and read by queries and the UI (products/event_definitions/backend/models/property_definition.py:73-152). v0.3 moved the privacy tag to E3. |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). The endpoints product publishes APIs from saved queries. |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A | OpenAPI schema generated from the Django API and used to generate typed TypeScript for the frontend and MCP service (services/mcp/src/api/generated.ts); structured validation errors. No mutation dry-run, so not 4. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 3 | 2 |  | A | Dashboards store tile layouts as JSON per dashboard with templates (products/dashboards/backend/models); insight definitions are schema-validated queries (posthog/schema.py) edited with live preview by project members. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Focused application: generic widgets from entity definitions (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 1 | 2 |  | A | No UI localisation (no locale files in the tree); light and dark themes from design-system tokens (packages/quill) that tenants cannot override. |
| D1 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A | Actions, cohorts, feature-flag release conditions, insight alerts and CDP functions with filters are defined as data in the UI across all event and person data; functions can be test-invoked before saving (nodejs/src/cdp/cdp-api.ts:280-281). |
| D2 Event model with webhooks or subscriptions and retry | assessed | 3 | 4 |  | A | Events feed CDP destinations with per-function logs and metrics and scheduled invocations (nodejs/src/cdp); batch exports to warehouses support backfills, which amounts to replay (products/batch_exports). |
| D3 Sandboxed server-side hooks | assessed | 2 | 3 |  | A | Hog functions run in the HogVM with a memory cap (DEFAULT_MAX_MEMORY 64 MB, common/hogvm) and a closed built-in function set, triggered by events and incoming webhooks, with per-function logs. No outbound egress guard was found in nodejs/src/cdp. |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A | Design system with tokens (packages/quill) and Storybook visual tests (.github/workflows/ci-storybook.yml); no automated accessibility scanning (the Playwright audit workflow audits flakes). |
| E2 Audit generic over entities, definition changes and approvals | assessed | 3 | 2 |  | A | Activity logging on most models with an activity page (posthog/models/activity_logging), retention by entitlement (retention.py:71), and recorded approval decisions on change requests (products/approvals/backend/models.py:112-140). |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 | 3 |  | A | Data deletion requests and async deletion remove a person's data across products (posthog/api/data_deletion_request.py, posthog/models/async_deletion); not driven by field-level privacy tags. |
| E4 Security as infrastructure | assessed | 3 |  |  | A | Resource-level access control and scoped API keys (products/access_control, posthog/scopes.py); semgrep and image scanning in CI on changed paths (.github/workflows/ci-security.yaml:60-174). |
| F1 Definitions and layouts versioned with rollback | assessed | 2 | 3 |  | A | The activity log records before-and-after changes for flags, insights, dashboards and more; no general revert across customisation surfaces. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 2 | 3 |  | A | Change requests carry the intended change, a validation status and a policy snapshot, and are reviewed and then applied (products/approvals/backend/models.py:15-65); scheduled changes for flags (products/approvals/backend/scheduled_changes.py). No staging-data preview. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 3 |  |  | A | Approval policies per registered action class with conditions evaluated on the change intent, named approvers, bypass roles and recorded Approval decisions (products/approvals/backend/policies.py:37-147, actions/registry.py, models.py:112-140). |
| F4 Upgrade safety | assessed | 2 |  |  | A | Customer definitions (insights, flags, functions) are data carried forward by Django migrations; no automated compatibility check or versioned extension contract was found. |
| G1 Indexed query path, never a scan of a generic store | assessed | 3 | 4 |  | A | ClickHouse event store with property materialisation driven by query analysis (ee/clickhouse/materialized_columns/analyze.py:89, columns.py:440), HogQL limits per context (posthog/hogql/constants.py:94-111) and cached query results. |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | Multi-tenant organisations and projects with quota limiting and per-team throttles; no noisy-neighbour detection evidenced. |
| G3 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A | Performance suites exist (services/mcp/vitest.perf.config.mts and service benchmarks); no documented per-surface limits. |
| H1 Layers deploy independently | assessed | 3 |  |  | A | Independently deployable services with their own images: Django web, Node CDP and ingestion, Rust capture and flag services, and an MCP worker on Cloudflare (25 Dockerfiles; rust/, nodejs/, services/mcp/wrangler.jsonc). |
| H2 Module boundaries enforced by tooling | assessed | 3 |  |  | A | tach enforces module boundaries and interfaces in CI (tach.toml, .github/workflows/ci-backend.yml) with isolation baselines for product modules (products/isolation_baseline.txt). |
| H3 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A | Backend, frontend, Rust, Playwright, Storybook, migration and semgrep checks run on pull requests with impacted-target selection from the import map (.github/scripts/tach_map.py); no accessibility check. |
| I1 Plugin lane breadth | assessed | 2 | 3 |  | A | Hog function templates for sources, transformations and destinations, site apps, dashboard templates and per-product MCP tool definitions; no plugin points for PostHog's own UI, theme or text. |
| I2 Runtime isolation and dependency control | assessed | 2 | 3 |  | A | User code runs in the HogVM with memory limits and a closed function set; egress control was not evidenced. |
| I3 Developer loop | assessed | 3 |  |  | A | Functions are test-invoked with logs and metrics before saving (nodejs/src/cdp/cdp-api.ts:280); per-PR Hogbox preview environments for PostHog's own developers (.github/workflows/hogbox-preview-env.yml). |
| K1 Machine-readable capability surface for agents | assessed | 4 | 3 |  | A | MCP service typed from the generated OpenAPI schema (services/mcp/src/api/generated.ts) with tools declared per product in YAML (57 products/*/mcp/tools.yaml), scoped keys and OAuth, and MCP evals (services/mcp/evals). |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A | PostHog AI answers members with taxonomy-grounded tools and creates insights, dashboards and other objects (ee/hogai, products/posthog_ai); offline and CI evaluation harnesses (ee/hogai/eval). |
| K3 Agent-safe actions | assessed | 2 | 3 |  | A | Scoped personal API keys and OAuth (posthog/scopes.py), approval policies on mutating actions, activity log and throttles; client idempotency identifiers on some writes only (posthog/api/data_deletion_request.py:147); no dry-run. |
| N1 Canonical data model with a mapping layer | assessed | 3 | 2 |  | A | Revenue analytics maps Stripe and event-based sources onto one canonical set of revenue views (products/revenue_analytics/backend/views/sources); warehouse sources share one import framework (products/warehouse_sources). |
| N2 Connector definition or SDK | assessed | 3 |  |  | A | Warehouse source definitions and CDP destination templates follow shared interfaces covering auth, sync schedules, incremental sync and delivery; admins install and configure them in the UI. |
| N3 Stable versioned contracts | assessed | 1 | 2 |  | A | API paths are unversioned; incremental warehouse sync merges by primary key; no public deprecation windows. |
| O1 Kernel concepts are domain-neutral | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| O2 A new domain is expressible without kernel change | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). More than 60 product modules extend the events and persons kernel. |
| O3 A domain ships as an installable bundle | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 | 4 |  | A | Events stream into ClickHouse within seconds and feed product features; PostHog instruments its own product with the same SDKs. |
| J2 Structured learning signals | assessed | 1 | 2 |  | A | Under the self rule, surveys and Signals concern customers' products and are not counted; no typed signals about PostHog's own configured definitions were found (searched products/signals, products/surveys, ee/hogai). |
| J3 Cross-source mining inside the product | assessed | 2 | 3 |  | A | Under the self rule, Signals (which mines customers' products) is not counted; PostHog analyses its own query logs to decide what to materialise (ee/clickhouse/materialized_columns/analyze.py:89). |
| M1 Ranked, evidence-backed proposals for change | assessed | 2 | 3 |  | A | Query analysis recommends and applies materialised columns (ee/clickhouse/materialized_columns/analyze.py); Signals proposals target customers' repositories and are excluded under the self rule. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 2 | 3 |  | A | PostHog AI creates insights, dashboards and other configured objects on request (ee/hogai); Tasks agents that open pull requests in customers' repositories are excluded under the self rule. |
| M4 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A | Report metrics re-run stored queries over trailing windows to track a report's impact (products/signals/backend/report_metrics.py); experiments compare variants against control. Neither binds the applied change's version to a keep, revise or rollback decision. |
| P1 The product turns its own operating experience into candidate changes | assessed | 3 | 2 |  | A | A weekly scheduled task analyses the last week of queries and materialises hot properties without being asked (posthog/tasks/scheduled.py:927, ee/settings.py:68-73, ee/clickhouse/materialized_columns/analyze.py:89). Narrow: storage layout only. |
| P2 Learned changes are validated before they take effect | assessed | 1 | 2 |  | A | No evaluation of materialisation changes against a baseline was found. |
| L1 Verification surface | assessed | 2 | 3 |  | A | _health, livez and _readyz endpoints (posthog/urls.py:125-133); no machine-readable deployed-configuration snapshot evidenced. |
| L2 Environment reproducibility | assessed | 3 |  |  | A | Optional per-pull-request Hogbox environments restore a migrated, demo-seeded database, apply the PR's migrations, hibernate to save cost and are cleaned up (.github/workflows/hogbox-preview-env.yml, hogbox-preview-cleanup.yml). |
| L3 Machine verifiability | assessed | 3 | 2 |  | A | Playwright journeys, Storybook visual tests and impacted-target selection that maps changed files to affected tests through tach's import map (.github/scripts/tach_map.py); features are instrumented with PostHog's own events. |

