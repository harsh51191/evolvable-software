# PostHog evidence

Read at github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). Warehouse views and group types are runtime data models, created by analysts through queries. If counted: 2.
- **A2 Field definitions carry type and validation**: **3** (grade A). Event and person property definitions carry a validated property_type and format editable in Data management and read by queries and the UI (products/event_definitions/backend/models/property_definition.py:73-152). v0.3 moved the privacy tag to E3.
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). The endpoints product publishes APIs from saved queries. If counted: 2.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 2.
- **B3 Machine-readable contract with introspection and dry-run**: **3** (grade A). OpenAPI schema generated from the Django API and used to generate typed TypeScript for the frontend and MCP service (services/mcp/src/api/generated.ts); structured validation errors. No mutation dry-run, so not 4.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **3** (grade A). Dashboards store tile layouts as JSON per dashboard with templates (products/dashboards/backend/models); insight definitions are schema-validated queries (posthog/schema.py) edited with live preview by project members.
  - Alternate reading 2: Only dashboards are layout-as-data; product pages are code.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions (fixed per-archetype rule). If counted: 2.
- **C3 Theme tokens and text are data with tenant overrides**: **1** (grade A). No UI localisation (no locale files in the tree); light and dark themes from design-system tokens (packages/quill) that tenants cannot override.
  - Alternate reading 2: Tokens are externalised in a design system, engineer-managed.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **3** (grade A). Actions, cohorts, feature-flag release conditions, insight alerts and CDP functions with filters are defined as data in the UI across all event and person data; functions can be test-invoked before saving (nodejs/src/cdp/cdp-api.ts:280-281).
  - Alternate reading 4: Functions are machine-readable and testable against real events; versioning and AI authoring are not verified.
- **D2 Event model with webhooks or subscriptions and retry**: **3** (grade A). Events feed CDP destinations with per-function logs and metrics and scheduled invocations (nodejs/src/cdp); batch exports to warehouses support backfills, which amounts to replay (products/batch_exports).
  - Alternate reading 4: Replay and per-project streams exist; event schemas are described, not generated, from definitions.
- **D3 Sandboxed server-side hooks**: **2** (grade A). Hog functions run in the HogVM with a memory cap (DEFAULT_MAX_MEMORY 64 MB, common/hogvm) and a closed built-in function set, triggered by events and incoming webhooks, with per-function logs. No outbound egress guard was found in nodejs/src/cdp.
  - Alternate reading 3: If Hog's closed function set counts as an allowlist and egress control exists outside the paths searched.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). Design system with tokens (packages/quill) and Storybook visual tests (.github/workflows/ci-storybook.yml); no automated accessibility scanning (the Playwright audit workflow audits flakes).
  - Alternate reading 2: Kit and tokens exist; the anchors bundle kit and scans.
- **E2 Audit generic over entities, definition changes and approvals**: **3** (grade A). Activity logging on most models with an activity page (posthog/models/activity_logging), retention by entitlement (retention.py:71), and recorded approval decisions on change requests (products/approvals/backend/models.py:112-140).
  - Alternate reading 2: Activity logging covers most, not all, models.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Data deletion requests and async deletion remove a person's data across products (posthog/api/data_deletion_request.py, posthog/models/async_deletion); not driven by field-level privacy tags.
  - Alternate reading 3: Admin-triggered erasure is generic across products; only tag-driven coverage is missing.
- **E4 Security as infrastructure**: **3** (grade A). Resource-level access control and scoped API keys (products/access_control, posthog/scopes.py); semgrep and image scanning in CI on changed paths (.github/workflows/ci-security.yaml:60-174).
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). The activity log records before-and-after changes for flags, insights, dashboards and more; no general revert across customisation surfaces.
  - Alternate reading 3: History and diffs are broad; rollback coverage was not verified per surface.
- **F2 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Change requests carry the intended change, a validation status and a policy snapshot, and are reviewed and then applied (products/approvals/backend/models.py:15-65); scheduled changes for flags (products/approvals/backend/scheduled_changes.py). No staging-data preview.
  - Alternate reading 3: A first-class proposal and review object exists; only preview on staging data is missing.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **3** (grade A). Approval policies per registered action class with conditions evaluated on the change intent, named approvers, bypass roles and recorded Approval decisions (products/approvals/backend/policies.py:37-147, actions/registry.py, models.py:112-140).
- **F4 Upgrade safety**: **2** (grade A). Customer definitions (insights, flags, functions) are data carried forward by Django migrations; no automated compatibility check or versioned extension contract was found.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **3** (grade A). ClickHouse event store with property materialisation driven by query analysis (ee/clickhouse/materialized_columns/analyze.py:89, columns.py:440), HogQL limits per context (posthog/hogql/constants.py:94-111) and cached query results.
  - Alternate reading 4: Query limits and materialisation from usage approach 'plans derived from definitions with cost limits'.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Multi-tenant organisations and projects with quota limiting and per-team throttles; no noisy-neighbour detection evidenced.
  - Alternate reading 3: Per-tenant limits are extensive; detection may exist in operations tooling outside the repository.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). Performance suites exist (services/mcp/vitest.perf.config.mts and service benchmarks); no documented per-surface limits.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **3** (grade A). Independently deployable services with their own images: Django web, Node CDP and ingestion, Rust capture and flag services, and an MCP worker on Cloudflare (25 Dockerfiles; rust/, nodejs/, services/mcp/wrangler.jsonc).
- **H2 Module boundaries enforced by tooling**: **3** (grade A). tach enforces module boundaries and interfaces in CI (tach.toml, .github/workflows/ci-backend.yml) with isolation baselines for product modules (products/isolation_baseline.txt).
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Backend, frontend, Rust, Playwright, Storybook, migration and semgrep checks run on pull requests with impacted-target selection from the import map (.github/scripts/tach_map.py); no accessibility check.
  - Alternate reading 3: Every class except accessibility is covered.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **2** (grade A). Hog function templates for sources, transformations and destinations, site apps, dashboard templates and per-product MCP tool definitions; no plugin points for PostHog's own UI, theme or text.
  - Alternate reading 3: Declarative and code extension exists for server and layout surfaces.
- **I2 Runtime isolation and dependency control**: **2** (grade A). User code runs in the HogVM with memory limits and a closed function set; egress control was not evidenced.
  - Alternate reading 3: Same egress question as D3.
- **I3 Developer loop**: **3** (grade A). Functions are test-invoked with logs and metrics before saving (nodejs/src/cdp/cdp-api.ts:280); per-PR Hogbox preview environments for PostHog's own developers (.github/workflows/hogbox-preview-env.yml).
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **4** (grade A). MCP service typed from the generated OpenAPI schema (services/mcp/src/api/generated.ts) with tools declared per product in YAML (57 products/*/mcp/tools.yaml), scoped keys and OAuth, and MCP evals (services/mcp/evals).
  - Alternate reading 3: If generation from API definitions does not count as generation from entity definitions.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). PostHog AI answers members with taxonomy-grounded tools and creates insights, dashboards and other objects (ee/hogai, products/posthog_ai); offline and CI evaluation harnesses (ee/hogai/eval).
  - Alternate reading 4: An evaluation harness exists; not every UI action has a conversational equivalent.
- **K3 Agent-safe actions**: **2** (grade A). Scoped personal API keys and OAuth (posthog/scopes.py), approval policies on mutating actions, activity log and throttles; client idempotency identifiers on some writes only (posthog/api/data_deletion_request.py:147); no dry-run.
  - Alternate reading 3: Scoped identity, policy gates, limits and audit are present.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). Revenue analytics maps Stripe and event-based sources onto one canonical set of revenue views (products/revenue_analytics/backend/views/sources); warehouse sources share one import framework (products/warehouse_sources).
  - Alternate reading 2: The canonical model covers one domain (revenue).
- **N2 Connector definition or SDK**: **3** (grade A). Warehouse source definitions and CDP destination templates follow shared interfaces covering auth, sync schedules, incremental sync and delivery; admins install and configure them in the UI.
- **N3 Stable versioned contracts**: **1** (grade A). API paths are unversioned; incremental warehouse sync merges by primary key; no public deprecation windows.
  - Alternate reading 2: The API is documented and sync is idempotent.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **O2 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). More than 60 product modules extend the events and persons kernel. If counted: 2.
- **O3 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). Events stream into ClickHouse within seconds and feed product features; PostHog instruments its own product with the same SDKs.
  - Alternate reading 4: Autocapture adds instrumentation automatically; whether that counts for PostHog's own evolution is the construct question.
- **J2 Structured learning signals**: **1** (grade A). Under the self rule, surveys and Signals concern customers' products and are not counted; no typed signals about PostHog's own configured definitions were found (searched products/signals, products/surveys, ee/hogai).
  - Alternate reading 2: PostHog AI may record typed feedback on its answers.
- **J3 Cross-source mining inside the product**: **2** (grade A). Under the self rule, Signals (which mines customers' products) is not counted; PostHog analyses its own query logs to decide what to materialise (ee/clickhouse/materialized_columns/analyze.py:89).
  - Alternate reading 3: If Signals run on PostHog's own product counts.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **2** (grade A). Query analysis recommends and applies materialised columns (ee/clickhouse/materialized_columns/analyze.py); Signals proposals target customers' repositories and are excluded under the self rule.
  - Alternate reading 3: If Signals proposals count.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **2** (grade A). PostHog AI creates insights, dashboards and other configured objects on request (ee/hogai); Tasks agents that open pull requests in customers' repositories are excluded under the self rule.
  - Alternate reading 3: If the Tasks lane counts.
- **M4 Post-change impact is measured against a declared baseline**: **2** (grade A). Report metrics re-run stored queries over trailing windows to track a report's impact (products/signals/backend/report_metrics.py); experiments compare variants against control. Neither binds the applied change's version to a keep, revise or rollback decision.
  - Alternate reading 3: Experiments record baseline, metric, window and conclusion for flag-gated changes.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **3** (grade A). A weekly scheduled task analyses the last week of queries and materialises hot properties without being asked (posthog/tasks/scheduled.py:927, ee/settings.py:68-73, ee/clickhouse/materialized_columns/analyze.py:89). Narrow: storage layout only.
  - Alternate reading 2: Narrow to one area.
- **P2 Learned changes are validated before they take effect**: **1** (grade A). No evaluation of materialisation changes against a baseline was found.
  - Alternate reading 2: Materialisation may be checked in code not read.
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). _health, livez and _readyz endpoints (posthog/urls.py:125-133); no machine-readable deployed-configuration snapshot evidenced.
  - Alternate reading 3: Instance status APIs may expose configuration.
- **L2 Environment reproducibility**: **3** (grade A). Optional per-pull-request Hogbox environments restore a migrated, demo-seeded database, apply the PR's migrations, hibernate to save cost and are cleaned up (.github/workflows/hogbox-preview-env.yml, hogbox-preview-cleanup.yml).
- **L3 Machine verifiability**: **3** (grade A). Playwright journeys, Storybook visual tests and impacted-target selection that maps changed files to affected tests through tach's import map (.github/scripts/tach_map.py); features are instrumented with PostHog's own events.
  - Alternate reading 2: Coverage across roles and devices was not verified.
