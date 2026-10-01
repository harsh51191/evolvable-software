# PostHog: EVOLVE v0.4 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.4.0 in this repository.

Scope: the posthog monorepo (Django app, products/, ee/, Node CDP services, Rust services, MCP service, CI). PostHog Cloud operations and separate SDK repositories are out of scope. Many products here run PostHog's evolve loop for customers' software; see the construct note in the reading.

## Reading

**SAL 1.** Request → Release reaches L2: PostHog AI plans before acting and builds insights and dashboards (DEL-01 2, DEL-04 2). Issue → Fix stops at L1 because nothing diagnoses PostHog's own issues (LRN-05 1); its Signals product does this for customers' products and is excluded under the self rule. **Strengths:** migration risk analysis in CI (ARC-02 3), Temporal and Celery work (ARC-04 3), and feature flags on its own code (DEL-09 2). **Blocks L3:** no backup in the repository (ARC-09 1), and definition rollback covers only some surfaces (GOV-05 2).

## Limits

Repository evidence only, master at the tip named above. The repository is very large (about 55,000 files); only the areas cited were read, so some capabilities are likely under-scored (for example versioning and rollback). Cloud operations, dogfooding practice and incident history are invisible here. Egress controls for Hog functions were searched for and not found; they may exist in infrastructure code outside the paths read. Single rater. Under the v0.3 self rule, Signals, Tasks and experiments on customers' products are excluded from scoring.

---
Framework EVOLVE 0.4.0. Date 2026-09-30. Source github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master). Archetype **focused-application**.

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, agent_mutations, definition_change_path. False: evolution_auto_apply, code_release_path.

Coverage: 57 assessed, 0 not evidenced, 9 not applicable. Grades: 57 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 1 (Configurable) · Request → Release L2 · Issue → Fix L1 · Opportunity → Expansion L1**

Progress toward the next level: Request → Release 11 of 20 conditions for L3; Issue → Fix 4 of 5 conditions for L2; Opportunity → Expansion 3 of 5 conditions for L2.

- With opt-in settings: SAL 1 (Configurable) · Request → Release L2 · Issue → Fix L1 · Opportunity → Expansion L1.
- With every alternate reading: SAL 2 (Assisted) · Request → Release L2 · Issue → Fix L2 · Opportunity → Expansion L1.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | L2 | L2 | L2 | L2 | **L2** | L2 |
| Issue → Fix | L1 | L2 | L2 | L2 | **L1** | L1 |
| Opportunity → Expansion | L1 | L2 | L2 | L2 | **L1** | L1 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 3 | pass |
| Tested backup and restore | ARC-09 ≥ 3 | 1 | fail |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 3 | pass |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 1 | fail |

### What blocks the next level

- **Request → Release to L3**: spine Build needs product build path ≥ 3 (has DEL-04 2); spine Verify needs DEL-05 ≥ 3 (has 2); spine Verify needs DEL-06 ≥ 3 (has 2); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Intake needs DEL-01 ≥ 3 (has 2); architecture Foundation needs every applicable ARC ≥ 2 (has ARC-09 1); architecture Foundation needs ARC-09 ≥ 3 (has 1); architecture Foundation needs ARC-05 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 1)
- **Issue → Fix to L2**: stages Diagnose needs LRN-05 ≥ 2 (has 1)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 1); stages Propose needs EXP-05 ≥ 2 (has 0)

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: LRN-03, GOV-05.
- **One step away:** raising any of these one level lifts the headline: LRN-05.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 2.2 | 2.2–2.3 | 2.2 | 2.2 | 2.2 |
| Velocity (DEL) | 2.2 | 2.2–2.8 | 2.2 | 2.2 | 2.2 |
| Open (MAL) | 2.5 | 2.5–3.1 | 2.5 | 2.5 | 2.3 |
| Learn (LRN) | 1.8 | 1.8–2.7 | 1.8 | 1.8 | 1.8 |
| Vet (GOV) | 2.1 | 2.1–2.6 | 2.1 | 2.1 | 2.1 |
| Expand (EXP) | 1.3 | 1.3–1.8 | 1.3 | 1.3 | 1.5 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 3.0 |
| ARC Scale | 2.3 |
| ARC Capacity | 2.0 |
| ARC Resilience | 1.5 |
| DEL Intake | 2.0 |
| DEL Build | 2.7 |
| DEL Verify | 2.3 |
| DEL Release | 2.0 |
| MAL Data model | 3.0 |
| MAL APIs | 3.0 |
| MAL Interface | 1.5 |
| MAL Behaviour | 2.7 |
| MAL Extensions | 2.3 |
| MAL Integrations | 2.0 |
| MAL Agent interface | 3.0 |
| LRN Sense | 2.0 |
| LRN Diagnose and propose | 1.5 |
| LRN Learn from experience | 1.5 |
| LRN Measure | 2.0 |
| GOV Compliance and security | 2.0 |
| GOV Change control | 2.3 |
| GOV AI and self-change safety | 2.0 |
| EXP Discover | 0.5 |
| EXP Launch | 2.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 3 | 4 |  | A | IT | ClickHouse event store with property materialisation driven by query analysis (ee/clickhouse/materialized_columns/analyze.py:89, columns.py:440), HogQL limits per context (posthog/hogql/constants.py:94-111) and cached query results. |
| ARC-02 Safe schema and data migrations | assessed | 3 |  |  | A | IT | CI runs migrations up to master, a migration risk analysis and safety tests for ClickHouse migrations (.github/workflows/ci-backend.yml:1661-2034, posthog/management/commands/analyze_migration_risk.py, test_ch_migrations_are_safe.py); async migrations carry rollback steps (posthog/async_migrations). |
| ARC-03 Horizontal scale of services | assessed | 2 | 3 |  | A | I | Stateless Django, Node and Rust services over shared stores; the hobby deployment is single-node (docker-compose.hobby.yml) and cloud scale-out manifests are outside this repository. |
| ARC-04 Reliable asynchronous work | assessed | 3 |  |  | A | IT | Celery with Redbeat for once-only schedules (pyproject.toml:21-22) and Temporal workflows with retries (posthog/temporal); ingestion routes failures to dead-letter handling (rust/common/types/src/event.rs). |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | IT | Multi-tenant organisations and projects with quota limiting and per-team throttles; no noisy-neighbour detection evidenced. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A |  | Performance suites exist (services/mcp/vitest.perf.config.mts and service benchmarks); no documented per-surface limits. |
| ARC-07 Service objectives defined and monitored | assessed | 2 |  |  | A |  | Prometheus metrics across services (for example services/llm-gateway/src/llm_gateway/metrics/prometheus.py); no published objectives in the repository. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | The LLM gateway has a circuit breaker for model providers (services/llm-gateway/src/llm_gateway/circuit_breaker.py) and subscriptions auto-disable after repeated failures (ee/tasks/subscriptions/auto_disable.py); other surfaces lack breakers, so a 3 is not defensible under the inventory rule. |
| ARC-09 Backup, restore and recovery | assessed | 1 |  |  | A |  | No backup command in the repository; self-hosted backup is left to the operator. |
| DEL-01 Request intake into a structured change specification | assessed | 2 |  |  | A |  | PostHog AI takes requests in conversations stored with the page and objects in context, and has a plan mode that sets out steps before acting (ee/hogai/chat_agent/prompts/plan.py); plans carry no acceptance criteria or risk class. |
| DEL-02 Layers deploy independently | assessed | 3 |  |  | A |  | Independently deployable services with their own images: Django web, Node CDP and ingestion, Rust capture and flag services, and an MCP worker on Cloudflare (25 Dockerfiles; rust/, nodejs/, services/mcp/wrangler.jsonc). |
| DEL-03 Module boundaries enforced by tooling | assessed | 3 |  |  | A |  | tach enforces module boundaries and interfaces in CI (tach.toml, .github/workflows/ci-backend.yml) with isolation baselines for product modules (products/isolation_baseline.txt). |
| DEL-04 AI implementation lane | assessed | 2 | 3 |  | A |  | PostHog AI creates insights, dashboards and other configured objects on request (ee/hogai); Tasks agents that open pull requests in customers' repositories are excluded under the self rule. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A |  | Backend, frontend, Rust, Playwright, Storybook, migration and semgrep checks run on pull requests with impacted-target selection from the import map (.github/scripts/tach_map.py); no accessibility check. |
| DEL-06 Verification surface | assessed | 2 | 3 |  | A |  | _health, livez and _readyz endpoints (posthog/urls.py:125-133); no machine-readable deployed-configuration snapshot evidenced. |
| DEL-07 Environment reproducibility | assessed | 3 |  |  | A |  | Optional per-pull-request Hogbox environments restore a migrated, demo-seeded database, apply the PR's migrations, hibernate to save cost and are cleaned up (.github/workflows/hogbox-preview-env.yml, hogbox-preview-cleanup.yml). |
| DEL-08 Machine verifiability | assessed | 2 | 3 |  | A |  | Playwright journeys, Storybook visual tests and impacted-target selection that maps changed files to affected tests through tach's import map (.github/scripts/tach_map.py); features are instrumented with PostHog's own events. Scored at the lower reading under rule 11 because: Coverage across roles and devices was not verified. |
| DEL-09 Staged exposure | assessed | 2 | 3 |  | A |  | PostHog ships its own code behind its own feature flags with percentage and cohort rollouts (products/feature_flags); definition changes and materialisations are not staged. |
| DEL-10 Kill switch | assessed | 2 | 3 |  | A |  | Feature flags switch code features off at runtime; there is no kill switch for AI-made or materialised changes. |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: Tasks and Stamphog act on customers' repositories (products/stamphog); no first-party lane ships PostHog code changes. |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). Warehouse views and group types are runtime data models, created by analysts through queries. |
| MAL-02 Field definitions carry type and validation | assessed | 3 |  |  | A |  | Event and person property definitions carry a validated property_type and format editable in Data management and read by queries and the UI (products/event_definitions/backend/models/property_definition.py:73-152). v0.3 moved the privacy tag to GOV-03. |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). The endpoints product publishes APIs from saved queries. |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A |  | OpenAPI schema generated from the Django API and used to generate typed TypeScript for the frontend and MCP service (services/mcp/src/api/generated.ts); structured validation errors. No mutation dry-run, so not 4. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A |  | Dashboards store tile layouts as JSON per dashboard with templates (products/dashboards/backend/models); insight definitions are schema-validated queries (posthog/schema.py) edited with live preview by project members. Scored at the lower reading under rule 11 because: Only dashboards are layout-as-data; product pages are code. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Focused application: generic widgets from entity definitions (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 1 | 2 |  | A |  | No UI localisation (no locale files in the tree); light and dark themes from design-system tokens (packages/quill) that tenants cannot override. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A |  | Actions, cohorts, feature-flag release conditions, insight alerts and CDP functions with filters are defined as data in the UI across all event and person data; functions can be test-invoked before saving (nodejs/src/cdp/cdp-api.ts:280-281). |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 3 | 4 |  | A |  | Events feed CDP destinations with per-function logs and metrics and scheduled invocations (nodejs/src/cdp); batch exports to warehouses support backfills, which amounts to replay (products/batch_exports). |
| MAL-12 Sandboxed server-side hooks | assessed | 2 | 3 |  | A |  | Hog functions run in the HogVM with a memory cap (DEFAULT_MAX_MEMORY 64 MB, common/hogvm) and a closed built-in function set, triggered by events and incoming webhooks, with per-function logs. No outbound egress guard was found in nodejs/src/cdp. |
| MAL-13 Plugin lane breadth | assessed | 2 | 3 |  | A |  | Hog function templates for sources, transformations and destinations, site apps, dashboard templates and per-product MCP tool definitions; no plugin points for PostHog's own UI, theme or text. |
| MAL-14 Runtime isolation and dependency control | assessed | 2 | 3 |  | A |  | User code runs in the HogVM with memory limits and a closed function set; egress control was not evidenced. |
| MAL-15 Developer loop | assessed | 3 |  |  | A |  | Functions are test-invoked with logs and metrics before saving (nodejs/src/cdp/cdp-api.ts:280); per-PR Hogbox preview environments for PostHog's own developers (.github/workflows/hogbox-preview-env.yml). |
| MAL-16 Canonical data model with a mapping layer | assessed | 2 | 3 |  | A |  | Revenue analytics maps Stripe and event-based sources onto one canonical set of revenue views (products/revenue_analytics/backend/views/sources); warehouse sources share one import framework (products/warehouse_sources). Scored at the lower reading under rule 11 because: The canonical model covers one domain (revenue). |
| MAL-17 Connector definition or SDK | assessed | 3 |  |  | A |  | Warehouse source definitions and CDP destination templates follow shared interfaces covering auth, sync schedules, incremental sync and delivery; admins install and configure them in the UI. |
| MAL-18 Stable versioned contracts | assessed | 1 | 2 |  | A |  | API paths are unversioned; incremental warehouse sync merges by primary key; no public deprecation windows. |
| MAL-19 Machine-readable capability surface for agents | assessed | 3 | 4 |  | A |  | MCP service typed from the generated OpenAPI schema (services/mcp/src/api/generated.ts) with tools declared per product in YAML (57 products/*/mcp/tools.yaml), scoped keys and OAuth, and MCP evals (services/mcp/evals). Scored at the lower reading under rule 11 because: If generation from API definitions does not count as generation from entity definitions. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A |  | PostHog AI answers members with taxonomy-grounded tools and creates insights, dashboards and other objects (ee/hogai, products/posthog_ai); offline and CI evaluation harnesses (ee/hogai/eval). |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 3 | 4 |  | A |  | Events stream into ClickHouse within seconds and feed product features; PostHog instruments its own product with the same SDKs. |
| LRN-02 Structured learning signals | assessed | 1 | 2 |  | A |  | Under the self rule, surveys and Signals concern customers' products and are not counted; no typed signals about PostHog's own configured definitions were found (searched products/signals, products/surveys, ee/hogai). |
| LRN-03 User-issue detection | assessed | 2 |  |  | A |  | The app captures its own exceptions into PostHog's error tracking (frontend/src/lib/colors.ts:80, products/error_tracking); friction detection for customers' products (products/signals) is excluded under the self rule. |
| LRN-04 Cross-source mining inside the product | assessed | 2 | 3 |  | A |  | Under the self rule, Signals (which mines customers' products) is not counted; PostHog analyses its own query logs to decide what to materialise (ee/clickhouse/materialized_columns/analyze.py:89). |
| LRN-05 Automated diagnosis | assessed | 1 | 2 |  | A |  | Exceptions are grouped into issues with stack traces by the error tracking product used on itself. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 2 | 3 |  | A |  | Query analysis recommends and applies materialised columns (ee/clickhouse/materialized_columns/analyze.py); Signals proposals target customers' repositories and are excluded under the self rule. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 2 | 3 |  | A |  | A weekly scheduled task analyses the last week of queries and materialises hot properties without being asked (posthog/tasks/scheduled.py:927, ee/settings.py:68-73, ee/clickhouse/materialized_columns/analyze.py:89). Narrow: storage layout only. Scored at the lower reading under rule 11 because: Narrow to one area. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 | 2 |  | A |  | No evaluation of materialisation changes against a baseline was found. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A |  | Report metrics re-run stored queries over trailing windows to track a report's impact (products/signals/backend/report_metrics.py); experiments compare variants against control. Neither binds the applied change's version to a keep, revise or rollback decision. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A |  | Design system with tokens (packages/quill) and Storybook visual tests (.github/workflows/ci-storybook.yml); no automated accessibility scanning (the Playwright audit workflow audits flakes). |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A |  | Activity logging on most models with an activity page (posthog/models/activity_logging), retention by entitlement (retention.py:71), and recorded approval decisions on change requests (products/approvals/backend/models.py:112-140). Scored at the lower reading under rule 11 because: Activity logging covers most, not all, models. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 | 3 |  | A |  | Data deletion requests and async deletion remove a person's data across products (posthog/api/data_deletion_request.py, posthog/models/async_deletion); not driven by field-level privacy tags. |
| GOV-04 Security as infrastructure | assessed | 3 |  |  | A | IT | Resource-level access control and scoped API keys (products/access_control, posthog/scopes.py); semgrep and image scanning in CI on changed paths (.github/workflows/ci-security.yaml:60-174). |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A | IT | The activity log records before-and-after changes for flags, insights, dashboards and more; no general revert across customisation surfaces. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Revert is not available across customisation surfaces. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 | 3 |  | A |  | Change requests carry the intended change, a validation status and a policy snapshot, and are reviewed and then applied (products/approvals/backend/models.py:15-65); scheduled changes for flags (products/approvals/backend/scheduled_changes.py). No staging-data preview. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 3 |  |  | A |  | Approval policies per registered action class with conditions evaluated on the change intent, named approvers, bypass roles and recorded Approval decisions (products/approvals/backend/policies.py:37-147, actions/registry.py, models.py:112-140). |
| GOV-08 Upgrade safety | assessed | 2 |  |  | A |  | Customer definitions (insights, flags, functions) are data carried forward by Django migrations; no automated compatibility check or versioned extension contract was found. |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A |  | Scoped personal API keys and OAuth (posthog/scopes.py), approval policies on mutating actions, activity log and throttles; client idempotency identifiers on some writes only (posthog/api/data_deletion_request.py:147); no dry-run. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A |  | PostHog AI acts through a fixed tool set with resource-level access control, and approval policies cover registered action classes (products/approvals/backend/policies.py); materialisation has no declared blast-radius limit. |
| GOV-11 Learning-input integrity | assessed | 2 | 3 |  | A |  | Third-party text in AI tool output is defanged and fenced as data, not instructions (ee/hogai/utils/untrusted.py); AI changes are attributed in the activity log, but source inputs are not recorded. |
| EXP-01 Kernel concepts are domain-neutral | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| EXP-02 A new domain is expressible without kernel change | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). More than 60 product modules extend the events and persons kernel. |
| EXP-03 A domain ships as an installable bundle | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| EXP-04 Unmet-demand sensing | assessed | 1 |  |  | A |  | No unmet-demand signals about PostHog itself beyond free-text requests. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 2 | 3 |  | A |  | Early access features let users opt into new products and betas (products/early_access_features); no success metric or keep-or-kill record. |

Facets: I implemented, T tested, O operated.

