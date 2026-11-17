# PostHog evidence

Read at github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Events in ClickHouse, configuration in PostgreSQL, recordings in object storage.
- **schema_changes**: true. Django and ClickHouse migrations, plus property materialisation that adds columns at runtime (ee/clickhouse/materialized_columns/columns.py).
- **multi_tenant**: true. Organisations and projects with their own members, roles and access control share one deployment, with quotas (products/access_control); these are separately administered groups, not one person's workspaces.
- **hosted_service**: true. Django web, Celery and Temporal workers, Node ingestion and Rust capture services.
- **machine_actions**: true. The API with scoped personal keys and an MCP server change PostHog objects (posthog/scopes.py, services/mcp).
- **agent_mutations**: true. PostHog AI creates and edits insights, dashboards, feature flags, experiments and surveys (ee/hogai/tools, products/*/backend/max_tools.py).
- **evolution_auto_apply**: false. PostHog AI changes are made on request in a conversation; weekly property materialisation applies without approval (posthog/tasks/scheduled.py:927), but it is scheduled maintenance, not a change from the evolution loop.
- **definition_change_path**: true. Insights, dashboards, feature flags, actions and approval policies are definitions.
- **code_release_path**: false. False under the v0.7 definition. PostHog AI drafts Hog transformation code into the editor (products/cdp/backend/max_tools.py:51), but a person saves and enables it and it is versioned and restored with the function definition (products/cdp/backend/api/hog_function.py:1677); the AI does not activate code. Tasks and Stamphog act on repositories (products/stamphog); no first-party lane ships PostHog's own code changes.
- **ai_features**: true. PostHog AI (ee/hogai) and the LLM gateway (services/llm-gateway).
- **ai_data_access**: true. PostHog AI queries the team's events, insights and taxonomy (ee/hogai/context).
- **ai_actions**: true. PostHog AI creates and edits insights, dashboards and other objects (ee/hogai/tools).

## Kinds of change

- **Charts, reports and dashboards** (`dashboards-insights`, main, made by product and growth teams in a project): reach **2 Drafted**, confidence medium. Members build insights and dashboards in the UI with live preview; PostHog AI drafts them on request (ee/hogai/tools/create_insight.py; ee/hogai/tools/upsert_dashboard/tool.py:116, with a confirmation preview for updates that remove insights at :125-139) and the member keeps or edits the result. Undo: a deleted dashboard and its tiles are restored through undo-delete (products/dashboards/backend/api/dashboard.py:2424, :2747; posthog/api/file_system/deletion.py), and edits are recorded in the activity log with before and after values; there is no one-step revert to an earlier version of a dashboard or insight, so undoing an edit means editing it back from the logged values. Reach 2 rests on DEL-04 2.
- **Who sees which feature (feature flags)** (`feature-flags`, main, made by engineers and product managers in a project): reach **2 Drafted**, confidence medium. Flags are created and edited in the UI and API with validated release conditions; PostHog AI creates flags on request through the same validated facade (products/feature_flags/backend/max_tools.py:211, create_flag with validation errors returned at :340-350). Undo: switch the flag off, restore a deleted or archived flag, and read any earlier version reconstructed from history (products/feature_flags/backend/version_history.py; versions endpoint api/feature_flag.py:4780); restoring an earlier version is done by editing it back, not by a revert button. Approval policies can require a reviewer for flag changes (products/approvals/backend/policies.py).
- **A/B tests and experiments** (`experiments`, not main, made by product teams): reach **2 Drafted**, confidence medium. Experiments are set up and launched in the UI; PostHog AI creates them in draft for a person to configure and launch (products/experiments/backend/max_tools.py:97, :158). Undo: reset an experiment to draft or archive it (products/experiments/backend/experiment_service.py:1963, :2996).
- **Where data is sent and how it is transformed** (`data-pipelines`, not main, made by data and engineering teams): reach **2 Drafted**, confidence high. Destinations, transformations and sources are configured from templates in the UI and test-invoked before saving (nodejs/src/cdp/cdp-api.ts:280); PostHog AI drafts transformation code, filters and inputs into the editor for a person to save (products/cdp/backend/max_tools.py:51, :153, :236). Undo: every live change is a numbered revision that can be restored (products/cdp/backend/api/hog_function.py:1395-1414, revisions restore at :1677-1708).
- **Surveys shown to users** (`surveys`, not main, made by product and research teams): reach **2 Drafted**, confidence medium. Surveys are built and launched in the UI; PostHog AI drafts a survey and launches it only with explicit confirmation (products/surveys/backend/max_tools.py:291-305, is_dangerous_operation at :298). Undo: stop a survey by ending it or archive it (end_date and archived fields, products/surveys/backend/api/survey.py:939-940); edits have no version history.
- **New kinds of analysis and changes to PostHog's own screens** (`product-features`, not main, made by PostHog's users, through feature requests): reach **0 Engineers only**, confidence high. New analysis types, product screens and behaviour are PostHog code in this monorepo, changed by pull request and release; no first-party lane builds PostHog's own code from users' requests (code_release_path false; Tasks and Stamphog act on repositories, not on a running PostHog). Engineers only.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md, CLAUDE.md, AI_POLICY.md, .agents/skills, .claude (agents, commands, hooks, skills), .codex, .cursorrules; agent workflows in CI: pr-autoresolve-conflicts.yml runs openai/codex-action pinned by SHA to resolve merge conflicts (manual dispatch only), review-hog.yml triggers an AI review service on labelled PRs, and stamphog[bot] posts AI approvals on this repository's PRs (products/stamphog/README.md).
- **Proven, Request → Release**: not evidenced. Searched: Repository at the pinned commit: CHANGELOG.md (points to the public changelog of engineering releases), activity-log and change-request models, .github workflows. No operating records of real changes going through PostHog's own Request → Release loop in a deployment are in the repository.
- **Proven, Issue → Fix**: not evidenced. Searched: Repository at the pinned commit: CHANGELOG.md (points to the public changelog of engineering releases), activity-log and change-request models, .github workflows. No operating records of real changes going through PostHog's own Issue → Fix loop in a deployment are in the repository.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: Repository at the pinned commit: CHANGELOG.md (points to the public changelog of engineering releases), activity-log and change-request models, .github workflows. No operating records of real changes going through PostHog's own Opportunity → Expansion loop in a deployment are in the repository.

Confidence for criteria whose score did not change in the v0.7 migration was assigned at migration from the recorded evidence; confidence for new and changed readings (kinds of change, LRN-10 and every re-read criterion) comes from re-reading the source at the pinned commit.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **3** (grade A, confidence medium), facets: implemented, tested. ClickHouse event store with property materialisation driven by query analysis (ee/clickhouse/materialized_columns/analyze.py:89, columns.py:440), HogQL limits per context (posthog/hogql/constants.py:94-111) and cached query results.
  - Higher reading 4: Query limits and materialisation from usage approach 'plans derived from definitions with cost limits'.
- **ARC-02 Safe schema and data migrations**: **3** (grade A, confidence high), facets: implemented, tested. CI runs migrations up to master, a migration risk analysis and safety tests for ClickHouse migrations (.github/workflows/ci-backend.yml:1661-2034, posthog/management/commands/analyze_migration_risk.py, test_ch_migrations_are_safe.py); async migrations carry rollback steps (posthog/async_migrations).

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A, confidence medium), facets: implemented. Stateless Django, Node and Rust services over shared stores; the hobby deployment is single-node (docker-compose.hobby.yml) and cloud scale-out manifests are outside this repository.
  - Higher reading 3: The services are built to scale out.
- **ARC-04 Reliable asynchronous work**: **3** (grade A, confidence high), facets: implemented, tested. Celery with Redbeat for once-only schedules (pyproject.toml:21-22) and Temporal workflows with retries (posthog/temporal); ingestion routes failures to dead-letter handling (rust/common/types/src/event.rs).
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A, confidence medium), facets: implemented, tested. Multi-tenant organisations and projects with quota limiting and per-team throttles; no noisy-neighbour detection evidenced.
  - Higher reading 3: Per-tenant limits are extensive; detection may exist in operations tooling outside the repository.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **2** (grade A, confidence medium). Performance suites exist (services/mcp/vitest.perf.config.mts and service benchmarks); no documented per-surface limits.
- **ARC-07 Service objectives defined and monitored**: **2** (grade A, confidence medium). Prometheus metrics across services (for example services/llm-gateway/src/llm_gateway/metrics/prometheus.py); no published objectives in the repository.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence medium). The LLM gateway has a circuit breaker for model providers (services/llm-gateway/src/llm_gateway/circuit_breaker.py) and subscriptions auto-disable after repeated failures (ee/tasks/subscriptions/auto_disable.py); other surfaces lack breakers, so a 3 is not defensible under the inventory rule.
  - AI-qualified reading: **3** (grade A, confidence high), facets: implemented, tested. LLM gateway circuit breaker and fallback, tested (services/llm-gateway, tests/test_circuit_breaker.py).
- **ARC-09 Backup, restore and recovery**: **1** (grade A, confidence high). No backup command or restore path in the product. The hobby upgrade script tells operators to back up the whole installation, containers and volumes, before upgrading (bin/upgrade-hobby:44-45), and takes a pg_dumpall only during its PostgreSQL version upgrade (bin/upgrade-hobby:239-242); routine backup and restore of ClickHouse, PostgreSQL and object storage are left to the operator. Evidence corrected at the v0.7 migration; score unchanged.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **2** (grade A, confidence medium). PostHog AI takes requests in conversations stored with the page and objects in context, and has a plan mode that sets out steps before acting (ee/hogai/chat_agent/prompts/plan.py); plans carry no acceptance criteria or risk class.
  - AI-qualified reading: **2** (grade A, confidence medium). Plan mode before acting (ee/hogai/chat_agent/prompts/plan.py).

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A, confidence medium). Independently deployable services with their own images: Django web, Node CDP and ingestion, Rust capture and flag services, and an MCP worker on Cloudflare (25 Dockerfiles; rust/, nodejs/, services/mcp/wrangler.jsonc).
- **DEL-03 Module boundaries enforced by tooling**: **3** (grade A, confidence medium). tach enforces module boundaries and interfaces in CI (tach.toml, .github/workflows/ci-backend.yml) with isolation baselines for product modules (products/isolation_baseline.txt).
- **DEL-04 AI implementation lane**: **2** (grade A, confidence medium). PostHog AI creates insights, dashboards and other configured objects on request (ee/hogai); Tasks agents that open pull requests in customers' repositories are excluded under the self rule.
  - Higher reading 3: If the Tasks lane counts.
  - AI-qualified reading: **2** (grade A, confidence medium). PostHog AI builds insights and dashboards on request.
    - Higher reading 3: Broad object coverage.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence medium). Backend, frontend, Rust, Playwright, Storybook, migration and semgrep checks run on pull requests with impacted-target selection from the import map (.github/scripts/tach_map.py); no accessibility check.
  - Higher reading 3: Every class except accessibility is covered.
- **DEL-06 Verification surface**: **2** (grade A, confidence medium). _health, livez and _readyz endpoints (posthog/urls.py:125-133); no machine-readable deployed-configuration snapshot evidenced.
  - Higher reading 3: Instance status APIs may expose configuration.
- **DEL-07 Environment reproducibility**: **3** (grade A, confidence medium). Optional per-pull-request Hogbox environments restore a migrated, demo-seeded database, apply the PR's migrations, hibernate to save cost and are cleaned up (.github/workflows/hogbox-preview-env.yml, hogbox-preview-cleanup.yml).
- **DEL-08 Machine verifiability**: **2** (grade A, confidence low). Playwright journeys, Storybook visual tests and impacted-target selection that maps changed files to affected tests through tach's import map (.github/scripts/tach_map.py); features are instrumented with PostHog's own events. Scored at the lower reading under rule 11 because: Coverage across roles and devices was not verified.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### Release

- **DEL-09 Staged exposure**: **2** (grade A, confidence medium). PostHog ships its own code behind its own feature flags with percentage and cohort rollouts (products/feature_flags); definition changes and materialisations are not staged.
  - Higher reading 3: Flags cover most code changes.
- **DEL-10 Kill switch**: **2** (grade A, confidence medium). Feature flags switch code features off at runtime; there is no kill switch for AI-made or materialised changes.
  - Higher reading 3: Flags act as a runtime kill switch for most features.
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: Tasks and Stamphog act on customers' repositories (products/stamphog); no first-party lane ships PostHog code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). Warehouse views and group types are runtime data models, created by analysts through queries. If counted: 2.
- **MAL-02 Field definitions carry type and validation**: **3** (grade A, confidence high). Event and person property definitions carry a validated property_type and format editable in Data management and read by queries and the UI (products/event_definitions/backend/models/property_definition.py:73-152). v0.3 moved the privacy tag to GOV-03.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). The endpoints product publishes APIs from saved queries. If counted: 2.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 2.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **3** (grade A, confidence medium). OpenAPI schema generated from the Django API and used to generate typed TypeScript for the frontend and MCP service (services/mcp/src/api/generated.ts); structured validation errors. No mutation dry-run, so not 4.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Dashboards store tile layouts as JSON per dashboard with templates (products/dashboards/backend/models); insight definitions are schema-validated queries (posthog/schema.py) edited with live preview by project members. Scored at the lower reading under rule 11 because: Only dashboards are layout-as-data; product pages are code.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions (fixed per-archetype rule). If counted: 2.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **1** (grade A, confidence medium). No UI localisation (no locale files in the tree); light and dark themes from design-system tokens (packages/quill) that tenants cannot override.
  - Higher reading 2: Tokens are externalised in a design system, engineer-managed.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **3** (grade A, confidence medium). Actions, cohorts, feature-flag release conditions, insight alerts and CDP functions with filters are defined as data in the UI across all event and person data; functions can be test-invoked before saving (nodejs/src/cdp/cdp-api.ts:280-281).
  - Higher reading 4: Functions are machine-readable and testable against real events; versioning and AI authoring are not verified.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **3** (grade A, confidence medium). Events feed CDP destinations with per-function logs and metrics and scheduled invocations (nodejs/src/cdp); batch exports to warehouses support backfills, which amounts to replay (products/batch_exports).
  - Higher reading 4: Replay and per-project streams exist; event schemas are described, not generated, from definitions.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence medium). Hog functions run in the HogVM with a memory cap (DEFAULT_MAX_MEMORY 64 MB, common/hogvm) and a closed built-in function set, triggered by events and incoming webhooks, with per-function logs. No outbound egress guard was found in nodejs/src/cdp.
  - Higher reading 3: If Hog's closed function set counts as an allowlist and egress control exists outside the paths searched.

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A, confidence medium). Hog function templates for sources, transformations and destinations, site apps, dashboard templates and per-product MCP tool definitions; no plugin points for PostHog's own UI, theme or text.
  - Higher reading 3: Declarative and code extension exists for server and layout surfaces.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A, confidence medium). User code runs in the HogVM with memory limits and a closed function set; egress control was not evidenced.
  - Higher reading 3: Same egress question as MAL-12.
- **MAL-15 Developer loop**: **3** (grade A, confidence high). Functions are test-invoked with logs and metrics before saving (nodejs/src/cdp/cdp-api.ts:280); per-PR Hogbox preview environments for PostHog's own developers (.github/workflows/hogbox-preview-env.yml).

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **2** (grade A, confidence medium). Revenue analytics maps Stripe and event-based sources onto one canonical set of revenue views (products/revenue_analytics/backend/views/sources); warehouse sources share one import framework (products/warehouse_sources). Scored at the lower reading under rule 11 because: The canonical model covers one domain (revenue).
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **MAL-17 Connector definition or SDK**: **3** (grade A, confidence medium). Warehouse source definitions and CDP destination templates follow shared interfaces covering auth, sync schedules, incremental sync and delivery; admins install and configure them in the UI.
- **MAL-18 Stable versioned contracts**: **1** (grade A, confidence medium). API paths are unversioned; incremental warehouse sync merges by primary key; no public deprecation windows.
  - Higher reading 2: The API is documented and sync is idempotent.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **3** (grade A, confidence medium). MCP service typed from the generated OpenAPI schema (services/mcp/src/api/generated.ts) with tools declared per product in YAML (57 products/*/mcp/tools.yaml), scoped keys and OAuth, and MCP evals (services/mcp/evals). Scored at the lower reading under rule 11 because: If generation from API definitions does not count as generation from entity definitions.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.
  - AI-qualified reading: **3** (grade A, confidence medium). MCP service with typed tools per product and scoped keys (services/mcp).
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **3** (grade A, confidence medium). PostHog AI answers members with taxonomy-grounded tools and creates insights, dashboards and other objects (ee/hogai, products/posthog_ai); offline and CI evaluation harnesses (ee/hogai/eval).
  - Higher reading 4: An evaluation harness exists; not every UI action has a conversational equivalent.
  - AI-qualified reading: **3** (grade A, confidence medium). A grounded assistant that answers and creates objects (ee/hogai).

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **3** (grade A, confidence medium). Events stream into ClickHouse within seconds and feed product features; PostHog instruments its own product with the same SDKs.
  - Higher reading 4: Autocapture adds instrumentation automatically; whether that counts for PostHog's own evolution is the construct question.
- **LRN-02 Structured learning signals**: **1** (grade A, confidence medium). Under the self rule, surveys and Signals concern customers' products and are not counted; no typed signals about PostHog's own configured definitions were found (searched products/signals, products/surveys, ee/hogai).
  - Higher reading 2: PostHog AI may record typed feedback on its answers.
- **LRN-03 User-issue detection**: **2** (grade A, confidence high). The app captures its own exceptions into PostHog's error tracking (frontend/src/lib/colors.ts:80, products/error_tracking); friction detection for customers' products (products/signals) is excluded under the self rule.
- **LRN-04 Cross-source mining inside the product**: **2** (grade A, confidence medium). Under the self rule, Signals (which mines customers' products) is not counted; PostHog analyses its own query logs to decide what to materialise (ee/clickhouse/materialized_columns/analyze.py:89).
  - Higher reading 3: If Signals run on PostHog's own product counts.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **1** (grade A, confidence medium). Exceptions are grouped into issues with stack traces by the error tracking product used on itself.
  - Higher reading 2: Grouping with attached context meets level 2.
  - AI-qualified reading: **0** (grade A, confidence medium). Diagnosis of PostHog's own issues is not model-backed.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A, confidence medium). Query analysis recommends and applies materialised columns (ee/clickhouse/materialized_columns/analyze.py); Signals proposals target customers' repositories and are excluded under the self rule.
  - Higher reading 3: If Signals proposals count.
  - AI-qualified reading: **0** (grade A, confidence medium). Materialisation recommendations are rule-based.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **2** (grade A, confidence medium). A weekly scheduled task analyses the last week of queries and materialises hot properties without being asked (posthog/tasks/scheduled.py:927, ee/settings.py:68-73, ee/clickhouse/materialized_columns/analyze.py:89). Narrow: storage layout only. Scored at the lower reading under rule 11 because: Narrow to one area.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **0** (grade A, confidence medium). Column materialisation is heuristic tuning.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A, confidence medium). Under the v0.7 boundary this scores checks on changes the product or its AI makes to its own behaviour. PostHog AI's changes go through the same validated paths as people's: flags through the validating facade (products/feature_flags/backend/max_tools.py:340-350), insights through query-schema validation (ee/hogai/tools/upsert_dashboard/tool.py:273), and approval policies where configured. The learned change (weekly property materialisation, posthog/tasks/scheduled.py:927) applies with no check or baseline evaluation. Lower reading across the two, 1.
  - Higher reading 2: AI-made changes alone pass automated schema validation, which is level 2.
  - AI-qualified reading: **2** (grade A, confidence high). AI-made flags, insights and dashboards pass automated schema and serializer validation before they are saved (products/feature_flags/backend/max_tools.py:340-350; ee/hogai/tools/upsert_dashboard/tool.py:273), and destructive dashboard updates need confirmation (:125-139); no baseline evaluation.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **2** (grade A, confidence medium). Report metrics re-run stored queries over trailing windows to track a report's impact (products/signals/backend/report_metrics.py); experiments compare variants against control. Neither binds the applied change's version to a keep, revise or rollback decision.
  - Higher reading 3: Experiments record baseline, metric, window and conclusion for flag-gated changes.
- **LRN-10 The improvement loop improves itself**: **1** (grade A, confidence medium). The checks that govern change are code: CI tests, serializer and schema validation, and PostHog AI's evaluation suites and prompts (ee/hogai/eval/ci/*.py, ee/hogai/chat_agent/prompts). PostHog's own team curates PostHog AI's offline evaluation datasets by hand from production traces (ee/hogai/eval/README.md, 'continuously review traces and curate your datasets'), which is level 1: improvement by people, outside the shipped product's change path. Approval policies are admin-editable data (products/approvals/backend/models.py:149-181, api.py:179-260) but are not versioned or activity-logged and are not linked to measured results. The PostHog team also measured its AI pull-request reviewer, ReviewHog, against 35 real production incidents mapped to the PRs that caused them (products/review_hog/eval/experiments/2026-09-incident-golden-set/FINAL_REPORT.md, JUDGE_RUBRIC.md): a by-hand experiment by engineers on the checks for PostHog's own code, outside the shipped product's change path and not a first-party evolution system under rule 12. Nothing in the product records a failure or wrong pass against the check that missed it or turns it into a proposed change to that check.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A, confidence medium). Design system with tokens (packages/quill) and Storybook visual tests (.github/workflows/ci-storybook.yml); no automated accessibility scanning (the Playwright audit workflow audits flakes).
  - Higher reading 2: Kit and tokens exist; the anchors bundle kit and scans.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A, confidence medium). Activity logging on most models with an activity page (posthog/models/activity_logging), retention by entitlement (retention.py:71), and recorded approval decisions on change requests (products/approvals/backend/models.py:112-140). Scored at the lower reading under rule 11 because: Activity logging covers most, not all, models.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence medium). Data deletion requests and async deletion remove a person's data across products (posthog/api/data_deletion_request.py, posthog/models/async_deletion); not driven by field-level privacy tags.
  - Higher reading 3: Admin-triggered erasure is generic across products; only tag-driven coverage is missing.
- **GOV-04 Security as infrastructure**: **3** (grade A, confidence high), facets: implemented, tested. Resource-level access control and scoped API keys (products/access_control, posthog/scopes.py); semgrep and image scanning in CI on changed paths (.github/workflows/ci-security.yaml:60-174).

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence high), facets: implemented, tested. The activity log records before-and-after changes for flags, insights, dashboards and more; no general revert across customisation surfaces. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Revert is not available across customisation surfaces.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **2** (grade A, confidence medium). Change requests carry the intended change, a validation status and a policy snapshot, and are reviewed and then applied (products/approvals/backend/models.py:15-65); scheduled changes for flags (products/approvals/backend/scheduled_changes.py). No staging-data preview.
  - Higher reading 3: A first-class proposal and review object exists; only preview on staging data is missing.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **3** (grade A, confidence high). Approval policies per registered action class with conditions evaluated on the change intent, named approvers, bypass roles and recorded Approval decisions (products/approvals/backend/policies.py:37-147, actions/registry.py, models.py:112-140).
- **GOV-08 Upgrade safety**: **2** (grade A, confidence medium). Customer definitions (insights, flags, functions) are data carried forward by Django migrations; no automated compatibility check or versioned extension contract was found.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence medium). Scoped personal API keys and OAuth (posthog/scopes.py), approval policies on mutating actions, activity log and throttles; client idempotency identifiers on some writes only (posthog/api/data_deletion_request.py:147); no dry-run.
  - Higher reading 3: Scoped identity, policy gates, limits and audit are present.
  - AI-qualified reading: **2** (grade A, confidence medium). AI acts within the user's team with access control and approval policies; idempotency only on some writes.
    - Higher reading 3: Approval policies may meet level 3.
- **GOV-10 Bounded self-change**: **2** (grade A, confidence medium). PostHog AI acts through a fixed tool set with resource-level access control, and approval policies cover registered action classes (products/approvals/backend/policies.py); materialisation has no declared blast-radius limit.
  - AI-qualified reading: **2** (grade A, confidence medium). A fixed tool set and approval policies; no blast-radius limit.
- **GOV-11 Learning-input integrity**: **2** (grade A, confidence medium). Third-party text in AI tool output is defanged and fenced as data, not instructions (ee/hogai/utils/untrusted.py); AI changes are attributed in the activity log, but source inputs are not recorded.
  - Higher reading 3: Injection fencing is systematic for session-derived content.
  - AI-qualified reading: **2** (grade A, confidence medium). Session-derived content is fenced as data (ee/hogai/utils/untrusted.py).
    - Higher reading 3: Systematic fencing.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **EXP-02 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). More than 60 product modules extend the events and persons kernel. If counted: 2.
- **EXP-03 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.

### Discover

- **EXP-04 Unmet-demand sensing**: **1** (grade A, confidence medium). No unmet-demand signals about PostHog itself beyond free-text requests.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence medium). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **2** (grade A, confidence medium). Early access features let users opt into new products and betas (products/early_access_features); no success metric or keep-or-kill record.
  - Higher reading 3: Stage-based releases approach a cohort launch.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence medium). PostHog AI gets taxonomy, schema and entity context through tools over the team's live data (ee/hogai/context, tools).
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A, confidence high), facets: implemented, tested. PostHog AI acts within the user's team with resource-level access control (products/access_control) and approval policies on mutating actions; covered by tests.

### Quality

- **AIR-05 Offline AI evaluation**: **3** (grade A, confidence medium). Maintained offline and CI evaluation suites per capability with scored metrics (ee/hogai/eval/ci: funnel, retention, insight search, memory, root; eval/offline).
- **AIR-06 Regression gating before release**: **2** (grade A, confidence high). LLM evals run on pull requests labelled evals-ready (.github/workflows/ci-ai.yml:2-20); they are not automatic for every AI change and no blocking threshold was found.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A, confidence high), facets: implemented, tested. AI generations and traces are captured in PostHog's own LLM analytics, and AI changes are attributed in the activity log (ee/hogai/llm.py, ee/hogai/llm_traces_summaries).

### Operations

- **AIR-01 Model and provider portability and resilience**: **3** (grade A, confidence high). The LLM gateway routes across providers with Cloudflare, Modal and Bedrock fallbacks and a circuit breaker (services/llm-gateway/src/llm_gateway/baseten.py:34, circuit_breaker.py), with tests (tests/test_circuit_breaker.py).
- **AIR-02 AI usage and per-customer cost controls**: **3** (grade A, confidence high). Generations are marked billable for AI credits in the usage report and rate-limited (ee/hogai/llm.py:129-167, 282); credits are enforced per organisation through billing.
- **AIR-08 Production quality, drift and feedback monitoring**: **2** (grade A, confidence medium). Generations, traces and user feedback on PostHog AI are recorded and summarised (ee/hogai/llm_traces_summaries, chat_agent/slash_commands/commands/feedback); no drift alerts found.
  - Higher reading 3: LLM analytics dashboards per model may act as continuous monitoring.
