# Directus: EVOLVE v0.5 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.5.1 in this repository.

Scope: the directus monorepo (API, Data Studio app, SDK, CLI, extensions SDK and registry, AI assistant and MCP server). Directus Cloud, the hosted marketplace catalogue and templates published in other repositories are out of scope.

## Reading

**SAL 1.** Every loop reaches L1 through the data-model editor and flow logs, which record each operation's success or failure (LRN-03 2). The AI assistant drafts schema and flow changes behind approvals but is scored at its lower reading (DEL-04 1), and Learn is the weakest capability (0.8). **Architecture:** no load suite (ARC-06 0) and no backup command (ARC-09 1) hold the architecture foundation at L1. **Next level:** structured request intake and a stronger AI lane, plus capacity and backup evidence.

## Limits

Repository evidence only, main branch at the tip named above. No running instance was inspected, so approval and preview behaviour is read from code. Directus Cloud, the hosted marketplace catalogue and published templates are out of scope. The repository is under a source-available licence, so some features may be licence-gated (api/src/license); entitlement checks were not traced per feature. Single rater; 18 alternate readings mark likely disagreements.

---
Framework EVOLVE 0.5.1. Date 2026-09-30. Source github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main). Archetype **configurable-application-platform**.

Scope facts true: persistent_data, schema_changes, hosted_service, machine_actions, agent_mutations, definition_change_path, ai_features, ai_data_access, ai_actions. False: multi_tenant, evolution_auto_apply, code_release_path.

Coverage: 72 assessed, 0 not evidenced, 2 not applicable. Grades: 72 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L1**

Progress toward the next level: Request → Release 1 of 4 conditions for L2; Issue → Fix 1 of 5 conditions for L2; Opportunity → Expansion 2 of 5 conditions for L2.

- With opt-in settings: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L1.
- With every alternate reading: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L1.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L1 | L1 | L2 | **L1** | L1 |
| Issue → Fix | L1 | L1 | L1 | L2 | **L1** | L1 |
| Opportunity → Expansion | L1 | L2 | L1 | L2 | **L1** | L1 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 1 | fail |
| Tenant isolation | ARC-05 ≥ 3 | n/a | n/a |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 1 | fail |

### What blocks the next level

- **Request → Release to L2**: spine Build needs product build path ≥ 2 (has DEL-04 1); stages Intake needs DEL-01 ≥ 2 (has 1); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0)
- **Issue → Fix to L2**: spine Build needs product build path ≥ 2 (has DEL-04 1, LRN-07 1); stages Diagnose needs LRN-05 ≥ 2 (has 1); stages Propose needs LRN-06 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0)

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.6 | 1.6–1.8 | 1.6 | 1.6 | 1.7 |
| Velocity (DEL) | 1.5 | 1.5–2.0 | 1.5 | 1.5 | 1.5 |
| Open (MAL) | 2.4 | 2.4–3.0 | 2.4 | 2.4 | 2.4 |
| Learn (LRN) | 0.8 | 0.8–0.9 | 0.8 | 0.8 | 0.8 |
| Vet (GOV) | 1.6 | 1.6–2.3 | 1.6 | 1.6 | 1.6 |
| Expand (EXP) | 1.1 | 1.1–1.8 | 1.1 | 1.1 | 1.1 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L0 (Foundational gap) · Context 3 · Quality 0 · Governance 1 · Operations 1 · not production-governed**

- With opt-in settings: AI Readiness L0 (Foundational gap) · Context 3 · Quality 0 · Governance 1 · Operations 1 · not production-governed.
- With every alternate reading: AI Readiness L0 (Foundational gap) · Context 3 · Quality 0 · Governance 1 · Operations 1 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 3 | AIR-03 3, AIR-04 3 |
| Quality | 0 | AIR-05 0, AIR-06 0 |
| Governance | 1 | AIR-07 2, GOV-09 (AI) 2, GOV-10 (AI) 2, GOV-11 (AI) 1, LRN-08 (AI) 1 |
| Operations | 1 | AIR-01 2, AIR-02 1, AIR-08 0, ARC-08 (AI) 1 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 3 | pass |
| Regression evaluation before release | AIR-06 ≥ 3 | 0 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 2 | fail |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 2 | MAL-19 3, MAL-20 2 |
| Build | 1 | DEL-01 1, DEL-04 1 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 1 |
| Expand | 0 | EXP-05 0 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.5 |
| ARC Scale | 1.5 |
| ARC Capacity | 1.0 |
| ARC Resilience | 1.5 |
| DEL Intake | 1.0 |
| DEL Build | 1.3 |
| DEL Verify | 2.3 |
| DEL Release | 1.5 |
| MAL Data model | 2.3 |
| MAL APIs | 3.0 |
| MAL Interface | 2.7 |
| MAL Behaviour | 2.3 |
| MAL Extensions | 2.7 |
| MAL Integrations | 1.0 |
| MAL Agent interface | 2.5 |
| LRN Sense | 1.5 |
| LRN Diagnose and propose | 0.5 |
| LRN Learn from experience | 1.0 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 1.3 |
| GOV Change control | 2.0 |
| GOV AI and self-change safety | 1.7 |
| EXP Expressible | 2.3 |
| EXP Discover | 0.0 |
| EXP Launch | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 3 |  |  | A | IT | Collections are real tables, so there is no generic store; fields marked is_indexed get database indexes (api/src/services/fields.ts:1008-1012); schema and response caching (CACHE_* settings). |
| ARC-02 Safe schema and data migrations | assessed | 2 |  |  | A |  | Every system migration has up and down steps (api/src/database/migrations, 110 files); user collections change through direct DDL from the schema service, with snapshot and apply for moving schemas between instances. No online strategy is enforced. |
| ARC-03 Horizontal scale of services | assessed | 2 | 3 |  | A | I | Redis-backed synchronisation, message bus and locks support several API instances (api/src/synchronization.ts, api/src/bus, api/src/lock); scale-out guidance lives in the separate docs site. |
| ARC-04 Reliable asynchronous work | assessed | 1 | 2 |  | A |  | Scheduled jobs and flows run inside the API process (api/src/schedules, api/src/flows.ts); there is no job queue with retries. |
| ARC-05 Tenant isolation and noisy-neighbour controls | not_applicable | excluded |  |  | - |  | Scope fact multi_tenant is false: One project per deployment; isolation inside a project is by roles and policies, not tenants. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 0 |  |  | A |  | No load or performance suite in the repository and no documented per-surface limits (searched for k6, locust, artillery, benchmark and load test). |
| ARC-07 Service objectives defined and monitored | assessed | 2 |  |  | A |  | A Prometheus metrics endpoint for database, cache and storage health (api/src/metrics, METRICS_* settings); no stated objectives. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | AI-qualified reading: 1. Sandboxed extensions run in an isolated VM with limits (api/src/extensions/lib/sandbox); the pressure limiter sheds load (packages/env/src/constants/defaults.ts:29). Other surfaces have no breakers. |
| ARC-09 Backup, restore and recovery | assessed | 1 |  |  | A |  | No backup command. Schema snapshots move definitions between instances, but data and files are left to the database and storage provider. |
| DEL-01 Request intake into a structured change specification | assessed | 1 | 2 |  | A |  | AI-qualified reading: 1. Requests reach the AI assistant as free-text chat (api/src/ai/chat); nothing structures them into a specification. |
| DEL-02 Layers deploy independently | assessed | 1 | 2 |  | A |  | API and Data Studio ship as one Node process and one container image (Dockerfile); packages are separate but deployed together. |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 |  |  | A |  | pnpm workspace packages with declared dependencies (pnpm-workspace.yaml); no architectural lint. |
| DEL-04 AI implementation lane | assessed | 1 | 2 |  | A |  | AI-qualified reading: 1. An AI authoring lane turns admin requests into schema, flow and item changes behind approvals, one project at a time (api/src/ai/tools); nothing applies accepted proposals across projects. Scored at the lower reading under rule 11 because: If the lane is judged manual per tenant because a human drives every change. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A |  | Lint and tests run on pull requests including drafts (.github/workflows/check.yml:3-12), but a Skip Checks label bypasses them (check.yml:30), E2E runs only when labelled (e2e-pr.yml:15) and CodeQL is scheduled. |
| DEL-06 Verification surface | assessed | 3 |  |  | A |  | /server/info with version, /server/health, generated specs (api/src/controllers/server.ts:21-80) and /schema/snapshot as a machine-readable configuration snapshot (api/src/controllers/schema.ts). |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A |  | Versioned container images, a bootstrap command, schema apply and CLI sync recreate a configured instance; E2E tests start instances per database vendor (tests/e2e). No per-change ephemeral environment or feature flags. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A |  | E2E API suite across database vendors (tests/e2e), run on pull requests only when labelled; no changed-path map or adoption instrumentation. |
| DEL-09 Staged exposure | assessed | 1 |  |  | A |  | Features are gated by licence entitlements (api/src/license/entitlements), not cohorts or flags. |
| DEL-10 Kill switch | assessed | 2 |  |  | A |  | Flows can be switched inactive and AI tools disabled at runtime; other changes cannot be switched off without editing them. |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: The AI lane changes definitions, not Directus code. |
| MAL-01 New entity type without code, DDL or deploy | assessed | 3 | 4 |  | A |  | Admins create collections in the Data Model UI and the API creates real tables with no migration or deploy (api/src/services/collections.ts); the AI assistant can also author collections through zod-validated tools behind an approval gate (api/src/ai/tools/collections/index.ts:20-66, api/src/ai/tools/registry.ts:198-214). No dry-run, so not 4. |
| MAL-02 Field definitions carry type and validation | assessed | 2 | 3 |  | A |  | Typed fields with validation rules, conditions, required, unique and is_indexed are created in the UI and read by forms and the generated APIs (api/services/fields.ts:62, 1008-1012). v0.3 moved the privacy tag to GOV-03. Scored at the lower reading under rule 11 because: Validation rules are partial for some field types. |
| MAL-03 Relationships and lifecycle states declarable | assessed | 2 | 3 |  | A |  | M2O, O2M, M2M and M2A relations are declared in the UI with database-level referential actions; lifecycle states are not a feature, and v0.3 accepts either at level 3. Scored at the lower reading under rule 11 because: If lifecycle states are considered central for this product. |
| MAL-04 API per entity is generic or generated | assessed | 3 | 4 |  | A |  | Generic REST (/items/:collection) and a GraphQL schema generated at runtime from the data model per role (api/src/services/graphql/index.ts:23-89): typed, with field selection, deep filters and permission and field validation from the definition. Scored at the lower reading under rule 11 because: If 'typed projections' requires per-type client types rather than runtime GraphQL types. |
| MAL-05 API reshapes at runtime from definitions | assessed | 3 |  |  | A |  | Schema changes invalidate the cached schema so REST and GraphQL reflect them live. No per-consumer schema versions or dry-run. |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A |  | /server/specs/oas and /server/specs/graphql are generated from the live schema (api/src/controllers/server.ts:21-37); typed SDK (sdk/); structured error codes (packages/errors). No mutation dry-run, so not 4. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A |  | Collection layouts (table, cards, calendar, kanban, map), form widths, groups and interface options are stored as presets and field meta and edited in the Data Studio per role (app/src/layouts); Insights dashboards; visual editing of connected frontends (packages/visual-editing). One project per instance, so per-tenant reads as per project. Scored at the lower reading under rule 11 because: No schema validation of layout props and no preview of layout changes before they apply. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | assessed | 3 |  |  | A |  | Every collection renders generic list layouts, item detail and create forms from field meta and interfaces (app/src/layouts, app/src/interfaces); admins configure presets. |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 3 |  |  | A |  | Admin appearance settings with light and dark theme overrides and custom CSS (api/src/database/seeds/13-settings.yaml, packages/themes), custom translation strings, and 93 locale files maintained through Crowdin (crowdin.yml). |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 | 3 |  | A |  | Flows compose triggers (event, schedule, webhook, manual, another flow) and operations (condition, exec, item CRUD, request, notification, mail, transform, trigger) across any collection in the admin UI (api/src/operations, api/src/flows.ts). No test or simulation mode. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 | 3 |  | A |  | Action and filter events fire for every collection including user-defined ones (api/src/emitter.ts); outbound webhooks are Flow request operations with flow logs. No retry or replay in api/src/flows.ts. |
| MAL-12 Sandboxed server-side hooks | assessed | 3 |  |  | A |  | The exec operation and sandboxed API extensions run in isolated-vm with memory and time limits (FLOWS_RUN_SCRIPT_MAX_MEMORY 32, FLOWS_RUN_SCRIPT_TIMEOUT 10000, packages/env/src/constants/defaults.ts:213-214) and requested scopes including a request URL allowlist (packages/extensions/src/shared/schemas/options.ts:14-27); triggered by events and requests. |
| MAL-13 Plugin lane breadth | assessed | 3 | 4 |  | A |  | Interfaces, displays, layouts, modules, panels, themes, endpoints, hooks, operations and bundles as code extensions (packages/extensions), plus declarative Flows, presets, translations and theme overrides; in-app marketplace backed by packages/extensions-registry. |
| MAL-14 Runtime isolation and dependency control | assessed | 3 |  |  | A |  | Sandboxed API extensions run in isolated-vm with memory and time limits and a request URL allowlist; marketplace installs default to sandbox trust (MARKETPLACE_TRUST sandbox, packages/env/src/constants/defaults.ts:124). Local non-sandboxed extensions keep full trust. |
| MAL-15 Developer loop | assessed | 2 |  |  | A |  | Extensions SDK with create, build and dev commands (packages/create-directus-extension, packages/extensions-sdk) and Docker Compose for local development; no preview against a remote project or staged branches. |
| MAL-16 Canonical data model with a mapping layer | assessed | 1 |  |  | A |  | No canonical integration model; integrations are Flow request operations or custom extensions. |
| MAL-17 Connector definition or SDK | assessed | 1 | 2 |  | A |  | The extensions SDK lets engineers build operation extensions that wrap external APIs; no connector definition covering auth, sync and lifecycle. Scored at the lower reading under rule 11 because: If a general extension SDK does not count as a connector SDK. |
| MAL-18 Stable versioned contracts | assessed | 1 | 2 |  | A |  | No path versioning; breaking changes are announced in release notes; no deprecation windows or idempotent sync. |
| MAL-19 Machine-readable capability surface for agents | assessed | 3 | 4 |  | A |  | AI-qualified reading: 3. MCP server over the same tool registry (api/src/ai/mcp/server.ts) with OAuth scope and audience checks (server.ts:75-102) and zod-typed tools; the schema tool returns the live data model as a capability map. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. In-app AI assistant with grounded tools over items, files, schema, relations and flows, running under the user's permissions (api/src/ai/chat, app/src/ai); admins author collections, fields, relations and flows in natural language with an approval card showing the proposed call. LLM tracing to Braintrust or Langfuse (api/src/ai/telemetry); no groundedness evaluation. Scored at the lower reading under rule 11 because: If an approval card is not a preview of the resulting change. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A |  | Activity rows are written per request and are queryable by in-product Insights dashboards; vendor telemetry counters (api/src/telemetry); AI telemetry to Braintrust or Langfuse (api/src/ai/telemetry). Scored at the lower reading under rule 11 because: Activity is an audit stream, not per-feature usage instrumentation. |
| LRN-02 Structured learning signals | assessed | 1 |  |  | A |  | Item comments are free text; no typed feedback or rating objects linked to definitions. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A |  | Every flow run records each operation step with its resolve or reject status as activity and revisions (api/src/flows.ts:414-454), viewable per flow; admins can read system logs (app/src/modules/settings/routes/system-logs). Failed actions outside flows are not recorded per product area. |
| LRN-04 Cross-source mining inside the product | assessed | 1 | 2 |  | A |  | Insights dashboards can query any collection including activity; no joined usage, support and delivery models or mining. |
| LRN-05 Automated diagnosis | assessed | 1 |  |  | A |  | AI-qualified reading: 0. Engineers read logs; no grouping or attached context. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No recommendation or proposal features; the assistant acts only on request. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A |  | AI-qualified reading: 0. The AI assistant acts only on request (api/src/ai); nothing learns from use. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 |  |  | A |  | AI-qualified reading: 1. AI-authored changes pass a human approval (api/src/ai/tools/registry.ts:198-214); there is no evaluation against a baseline. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A |  | No binding of changes to baselines or metrics. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A |  | Component library and theme tokens exist (packages/themes, app/src/components); no automated accessibility scanning in CI or tests. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A |  | Activity and revisions record every item mutation including system collections (schema, permissions, settings, flows), with an admin Activity module and retention (ACTIVITY_RETENTION and REVISIONS_RETENTION, packages/env/src/constants/defaults.ts:167-172). There is no approval object, so approvals are not covered. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 0 | 1 |  | A |  | No data-subject export or erasure features and no privacy tags (searched for gdpr, erasure, anonymisation and personal data); admins can export collections and delete items by hand. Scored at the lower reading under rule 11 because: If manual export and deletion do not count as a mechanism. |
| GOV-04 Security as infrastructure | assessed | 2 | 3 |  | A | IT | Policies with collection, field and item-level rules apply to every collection including new ones; field validation is generic. CodeQL runs on a schedule, not on pull requests (.github/workflows/codeql-analysis.yml:5), so scanning does not gate change. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A | IT | Revisions can be reverted for items and system records (api/src/services/revisions.ts:13-18); data-model changes have no rollback in the UI. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Data-model changes have no rollback. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 | 3 |  | A |  | Content Versioning stages item changes for compare and promote (api/src/services/versions.ts:436-521); definitions and configuration move between projects through schema snapshot, diff and apply (api/src/controllers/schema.ts) and CLI sync pull, diff and push (packages/cli/src/commands/sync), which is an engineer flow. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 | 3 |  | A |  | Mutating AI tool calls require approval unless the user set that tool to always-allow (api/src/ai/tools/registry.ts:198-214, app/src/ai/stores/use-ai.ts:179-185); deletes can be disabled wholesale (allowDeletes). Approvals are not recorded as audit objects. |
| GOV-08 Upgrade safety | assessed | 2 |  |  | A |  | Extension SDK and types are versioned packages (packages/extensions-sdk, packages/extensions); system migrations run automatically; schema snapshots apply through diff. No automated compatibility check of extensions against a new release was found. |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. The assistant acts with the user's accountability; MCP clients get OAuth-scoped tokens; mutations need approval; rate limiter and activity rows apply. No idempotency keys or dry-run. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Each AI tool can require approval and deletes can be disabled wholesale (api/src/ai/tools/registry.ts:198-214); there is no per-period or blast-radius limit. |
| GOV-11 Learning-input integrity | assessed | 1 |  |  | A |  | AI-qualified reading: 1. AI changes are recorded as revisions by the acting user, but inputs carry no provenance and nothing separates untrusted content from instructions (api/src/ai). |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 | 4 |  | A |  | Kernel is users, roles, policies, permissions, files, collections, flows, comments and notifications, with no domain nouns; system collections accept custom fields. |
| EXP-02 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A |  | Any domain can be modelled as collections, relations, flows and policies with no kernel change, but no domain shipped this way is evidenced inside the repository. |
| EXP-03 A domain ships as an installable bundle | assessed | 2 | 3 |  | A |  | Schema snapshot and apply cover collections, fields and relations; CLI sync pulls and pushes roles, policies, permissions, flows, operations, dashboards, panels, presets, translations and settings between projects (packages/cli/src/commands/sync). Not a versioned bundle with install semantics. |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A |  | No record of failed searches or unsupported requests was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 | 2 |  | A |  | Extensions are installed per project; there is no cohort launch. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A |  | Schema-aware tools read live collections, fields, relations, items and files (api/src/ai/tools/schema, items, files); results come from the source records. |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 3 |  |  | A | IT | Tool calls run through services with the requesting user's accountability, so Directus permissions apply (api/src/ai/tools/items, tests pass accountability through: items/index.test.ts). |
| AIR-05 Offline AI evaluation | assessed | 0 |  |  | A |  | No evaluation harness for the assistant (searched api/src/ai for eval). |
| AIR-06 Regression gating before release | assessed | 0 |  |  | A |  | No evaluation in CI; AI changes ship unevaluated (.github/workflows). |
| AIR-07 AI action tracing and auditability | assessed | 2 |  |  | A |  | Opt-in Langfuse and Braintrust telemetry records model calls with user, role, provider and model (api/src/ai/telemetry); revisions record data changes by the user, without the model or prompt. |
| AIR-01 Model and provider portability and resilience | assessed | 2 |  |  | A |  | OpenAI, Anthropic, Google and OpenAI-compatible providers configured by admins, model chosen in the chat (api/src/ai/providers/registry.ts); no fallback or declared resilience strategy. |
| AIR-02 AI usage and per-customer cost controls | assessed | 1 |  |  | A |  | Usage is streamed to the client per request (api/src/ai/chat/controllers/chat.post.ts:71-72); not recorded per user, and no budgets. |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 0 |  |  | A |  | No feedback or quality monitoring for the assistant. |

Facets: I implemented, T tested, O operated.
