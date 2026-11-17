# Directus: EVOLVE v0.7 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.7.0 in this repository.

Scope: the directus monorepo (API, Data Studio app, SDK, CLI, extensions SDK and registry, AI assistant and MCP server). Directus Cloud, the hosted marketplace catalogue and templates published in other repositories are out of scope.

## Reading

**SAL 1.** Every loop reaches L1 through the data-model editor and flow logs, which record each operation's success or failure (LRN-03 2). The AI assistant drafts schema and flow changes behind approvals but is scored at its lower reading (DEL-04 1), and Learn is the weakest capability (0.8). **Architecture:** no load suite (ARC-06 0) and no backup command (ARC-09 1) hold the architecture foundation at L1. **Next level:** structured request intake and a stronger AI lane, plus capacity and backup evidence.

## Limits

Repository evidence only, main branch at the tip named above. No running instance was inspected, so approval and preview behaviour is read from code. Directus Cloud, the hosted marketplace catalogue and published templates are out of scope. The repository is under a source-available licence, so some features may be licence-gated (api/src/license); entitlement checks were not traced per feature. Single rater; 18 alternate readings mark likely disagreements.

---
Framework EVOLVE 0.7.0. Date 2026-09-30. Source github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main). Archetype **configurable-application-platform**. Basis **shipped** (what ships).

Scope facts true: persistent_data, schema_changes, hosted_service, machine_actions, agent_mutations, definition_change_path, ai_features, ai_data_access, ai_actions. False: multi_tenant, evolution_auto_apply, code_release_path.

Coverage: 73 assessed, 0 not evidenced, 2 not applicable. Grades: 73 A, 0 B, 0 C.

Confidence: 14 high, 59 medium, 0 low across the assessed criteria. No low-confidence criterion holds a next-level blocker or a critical control.

## Software Autonomy Level

**Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)**

Progress toward the next level: Request → Release 2 of 4 conditions for L2; Issue → Fix 2 of 5 conditions for L2; Opportunity → Expansion 2 of 5 conditions for L2.

- With opt-in settings: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0).
- With every alternate reading: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0).

| Loop | Stages | Spine | Architecture | Governance | Level | AI-driven | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L2 | L1 | L2 | **L1** | L0 | L1 |
| Issue → Fix | L1 | L2 | L1 | L2 | **L1** | L0 | L1 |
| Opportunity → Expansion | L1 | L2 | L1 | L2 | **L1** | L0 | L1 |

**Recursion: 0 Fixed (LRN-10 at 0).** How far the loop improves its own checks, evaluation sets, policies and prompts from measured results.

**AI delivery.** Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

### Kinds of change

2 of 3 main kinds are self-serve (reach 1 or more: the people running the product make it themselves and can undo it).

| Kind | Who | Main | Reach | Evidence |
|---|---|---|---|---|
| What data is kept (collections and fields) (`data-model`) | project admins | yes | 0 Engineers only | Admins create and change collections, fields and relations in the Data Model UI with no deploy (api/src/services/collections.ts, fields.ts), and the AI assistant drafts them behind per-call approval (api/src/ai/tools/collections, fields, relations; registry.ts:198-214). But there is no undo: schema changes record no prior state and have no rollback in the UI (GOV-05), deleting or retyping a field drops data, and schema snapshot, diff and apply (api/src/controllers/schema.ts) is an engineer flow between instances. Only an addition can be reversed, by deleting it. A path without undo is reach 0. Confidence medium. |
| Who can see and change what (roles, policies and permissions) (`permissions`) | project admins | yes | 1 Self-serve | Admins edit roles, policies and permissions in Settings with no deploy. Undo: these system collections keep revisions (accountability 'all' by default, packages/system-data/src/collections/collections.yaml:14-68), and the policy and role pages show the revisions sidebar with revert (app/src/modules/settings/routes/policies/item.vue, roles/item.vue; RevisionsService.revert, api/src/services/revisions.ts:13-27). Confidence high. |
| Automations (flows) (`flows`) | project admins | yes | 2 Drafted | Admins build flows from triggers and operations in the UI; the AI assistant drafts flows and operations, including sandboxed exec scripts, as tool calls a person approves before they run (api/src/ai/tools/flows, operations/index.ts, operations/prompt.md:67, :182; registry.ts:198-214). Undo: a flow can be set inactive or deleted, and flows and operations keep revisions (collections.yaml:100-103) that can be reverted through the revert endpoint (api/src/controllers/utils.ts:75); the flows page has no revisions UI. Reach 2 rests on DEL-04 2, re-scored in this migration. Confidence medium. |
| Dashboards and how lists are laid out (`dashboards-layouts`) | project admins and editors | no | 1 Self-serve | Insights dashboards and panels and collection layouts, bookmarks and presets are edited in the Data Studio with no deploy. Undo: dashboards and panels keep revisions (collections.yaml:87-90) revertible through the API only; presets keep no revisions (accountability null, collections.yaml:55) and are reset or deleted by hand. Confidence low. |
| Add-ons from the marketplace (`marketplace-extensions`) | project admins | no | 1 Self-serve | Admins install marketplace extensions in the app, sandboxed by default (MARKETPLACE_TRUST sandbox, packages/env/src/constants/defaults.ts:124), through /extensions/registry/install and reinstall (api/src/controllers/extensions.ts:184-230). Undo: uninstall (/registry/uninstall, extensions.ts:232). Confidence medium. |
| Custom screens, endpoints and hooks (`custom-extensions`) | developers for the project | no | 0 Engineers only | Custom interfaces, modules, endpoints, hooks and operations are code written with the extensions SDK (packages/extensions-sdk) and deployed to the instance's extensions folder; changes to Directus itself are releases of this repository. Engineers only. Confidence high. |

### Proven

**Proven: not evidenced.** What operating records show real changes doing, beside what the product is built to do. From a repository alone, proven is usually not evidenced.

| Loop | Built | Proven | Operating records, or what was searched |
|---|---:|---|---|
| Request → Release | L1 | not evidenced | Searched: Repository at the pinned commit: release workflows, changesets, revisions and activity code. Operating records of real changes going through a Directus project's Request → Release loop (activity and revisions) live in running instances, not in the repository. |
| Issue → Fix | L1 | not evidenced | Searched: Repository at the pinned commit: release workflows, changesets, revisions and activity code. Operating records of real changes going through a Directus project's Issue → Fix loop (activity and revisions) live in running instances, not in the repository. |
| Opportunity → Expansion | L1 | not evidenced | Searched: Repository at the pinned commit: release workflows, changesets, revisions and activity code. Operating records of real changes going through a Directus project's Opportunity → Expansion loop (activity and revisions) live in running instances, not in the repository. |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 0 | fail |
| Tenant isolation | ARC-05 ≥ 3 | n/a | n/a |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 2 | fail |

### What blocks the next level

- **Request → Release to L2**: stages Intake needs DEL-01 ≥ 2 (has 1); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- **Issue → Fix to L2**: stages Diagnose needs LRN-05 ≥ 2 (has 1); stages Propose needs LRN-06 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)

### What AI drives

Each loop re-scored with its AI-performable stages read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level.

| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |
|---|---:|---:|---|---|
| Request → Release | L1 | L0 | DEL-01 1, DEL-04 2 | DEL-01 ≥ 2 (has 1) |
| Issue → Fix | L1 | L0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 2 | LRN-05 ≥ 2 (has 0); LRN-06 ≥ 2 (has 0) |
| Opportunity → Expansion | L1 | L0 | EXP-05 0 | EXP-05 ≥ 2 (has 0) |

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: DEL-04, LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.5 | 1.5–1.8 | 1.5 | 1.5 | 1.5 |
| Velocity (DEL) | 1.6 | 1.6–2.0 | 1.6 | 1.6 | 1.6 |
| Open (MAL) | 2.4 | 2.4–3.0 | 2.4 | 2.4 | 2.4 |
| Learn (LRN) | 0.9 | 0.9–1.0 | 0.9 | 0.9 | 0.9 |
| Vet (GOV) | 1.6 | 1.6–2.3 | 1.6 | 1.6 | 1.6 |
| Expand (EXP) | 1.1 | 1.1–1.8 | 1.1 | 1.1 | 1.1 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.5 |
| ARC Scale | 1.5 |
| ARC Capacity | 1.0 |
| ARC Resilience | 1.0 |
| DEL Intake | 1.0 |
| DEL Build | 1.7 |
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
| LRN Learn from experience | 1.5 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 1.3 |
| GOV Change control | 2.0 |
| GOV AI and self-change safety | 1.7 |
| EXP Expressible | 2.3 |
| EXP Discover | 0.0 |
| EXP Launch | 1.0 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L0 (Foundational gap) · Context 3 · Quality 0 · Governance 1 · Operations 1 · not production-governed**

- With opt-in settings: AI Readiness L0 (Foundational gap) · Context 3 · Quality 0 · Governance 1 · Operations 1 · not production-governed.
- With every alternate reading: AI Readiness L0 (Foundational gap) · Context 3 · Quality 0 · Governance 1 · Operations 1 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 3 | AIR-03 3, AIR-04 3 |
| Quality | 0 | AIR-05 0, AIR-06 0 |
| Governance | 1 | AIR-07 2, GOV-09 (AI) 2, GOV-10 (AI) 2, GOV-11 (AI) 1, LRN-08 (AI) 2 |
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
| Build | 1 | DEL-01 1, DEL-04 2 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 2 |
| Expand | 0 | EXP-05 0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 3 |  |  | A, high | IT | Collections are real tables, so there is no generic store; fields marked is_indexed get database indexes (api/src/services/fields.ts:1008-1012); schema and response caching (CACHE_* settings). |
| ARC-02 Safe schema and data migrations | assessed | 2 |  |  | A, medium |  | Every system migration has up and down steps (api/src/database/migrations, 110 files); user collections change through direct DDL from the schema service, with snapshot and apply for moving schemas between instances. No online strategy is enforced. |
| ARC-03 Horizontal scale of services | assessed | 2 | 3 |  | A, medium | I | Redis-backed synchronisation, message bus and locks support several API instances (api/src/synchronization.ts, api/src/bus, api/src/lock); scale-out guidance lives in the separate docs site. |
| ARC-04 Reliable asynchronous work | assessed | 1 | 2 |  | A, medium |  | Scheduled jobs and flows run inside the API process (api/src/schedules, api/src/flows.ts); there is no job queue with retries. |
| ARC-05 Tenant isolation and noisy-neighbour controls | not_applicable | excluded |  |  | - |  | Scope fact multi_tenant is false: One project per deployment; isolation inside a project is by roles and policies, not tenants. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 0 |  |  | A, medium |  | No load or performance suite in the repository and no documented per-surface limits (searched for k6, locust, artillery, benchmark and load test). |
| ARC-07 Service objectives defined and monitored | assessed | 2 |  |  | A, medium |  | A Prometheus metrics endpoint for database, cache and storage health (api/src/metrics, METRICS_* settings); no stated objectives. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A, high |  | AI-qualified reading: 1. Sandboxed extensions run in an isolated VM with limits (api/src/extensions/lib/sandbox); the pressure limiter sheds load (packages/env/src/constants/defaults.ts:29). Other surfaces have no breakers. |
| ARC-09 Backup, restore and recovery | assessed | 0 | 1 |  | A, medium |  | Corrected from 1 to 0 at the v0.7 migration, applying the anchor as the second rating did for Dify: level 1 needs documentation telling operators to back up, and this repository has none. No backup or restore command or feature for the database, files or settings; searched every file outside node_modules for 'backup' and 'back up' (only icon names in app/src). Schema snapshot and apply move the data model, not data or files. |
| DEL-01 Request intake into a structured change specification | assessed | 1 | 2 |  | A, medium |  | AI-qualified reading: 1. Requests reach the AI assistant as free-text chat (api/src/ai/chat); nothing structures them into a specification. |
| DEL-02 Layers deploy independently | assessed | 1 | 2 |  | A, medium |  | API and Data Studio ship as one Node process and one container image (Dockerfile); packages are separate but deployed together. |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 |  |  | A, medium |  | pnpm workspace packages with declared dependencies (pnpm-workspace.yaml); no architectural lint. |
| DEL-04 AI implementation lane | assessed | 2 |  |  | A, high |  | AI-qualified reading: 2. Re-scored 1 to 2 at the v0.7 migration, after the kinds of change exposed the gap. The AI assistant, on by default (AI_ENABLED true, packages/env/src/constants/defaults.ts:265) once a provider key is set, drafts collections, fields, relations, flows, operations and items as zod-validated tool calls; every mutating call waits for the user's approval unless that user set the tool to always-allow (api/src/ai/tools/registry.ts:198-214, tests in registry.test.ts). That is anchor 2: an AI lane drafts changes on request and a person finishes them. It is not 3: there is no accepted-change specification, verification evidence or policy across change classes. The earlier lower reading treated per-call human approval as a manual lane, which is what anchor 2 describes. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A, high |  | Lint and tests run on pull requests including drafts (.github/workflows/check.yml:3-12), but a Skip Checks label bypasses them (check.yml:30), E2E runs only when labelled (e2e-pr.yml:15) and CodeQL is scheduled. |
| DEL-06 Verification surface | assessed | 3 |  |  | A, high |  | /server/info with version, /server/health, generated specs (api/src/controllers/server.ts:21-80) and /schema/snapshot as a machine-readable configuration snapshot (api/src/controllers/schema.ts). |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A, medium |  | Versioned container images, a bootstrap command, schema apply and CLI sync recreate a configured instance; E2E tests start instances per database vendor (tests/e2e). No per-change ephemeral environment or feature flags. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A, medium |  | E2E API suite across database vendors (tests/e2e), run on pull requests only when labelled; no changed-path map or adoption instrumentation. |
| DEL-09 Staged exposure | assessed | 1 |  |  | A, medium |  | Features are gated by licence entitlements (api/src/license/entitlements), not cohorts or flags. |
| DEL-10 Kill switch | assessed | 2 |  |  | A, medium |  | Flows can be switched inactive and AI tools disabled at runtime; other changes cannot be switched off without editing them. |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: The AI lane changes definitions, not Directus code. |
| MAL-01 New entity type without code, DDL or deploy | assessed | 3 | 4 |  | A, medium |  | Admins create collections in the Data Model UI and the API creates real tables with no migration or deploy (api/src/services/collections.ts); the AI assistant can also author collections through zod-validated tools behind an approval gate (api/src/ai/tools/collections/index.ts:20-66, api/src/ai/tools/registry.ts:198-214). No dry-run, so not 4. |
| MAL-02 Field definitions carry type and validation | assessed | 2 | 3 |  | A, medium |  | Typed fields with validation rules, conditions, required, unique and is_indexed are created in the UI and read by forms and the generated APIs (api/services/fields.ts:62, 1008-1012). v0.3 moved the privacy tag to GOV-03. Scored at the lower reading under rule 11 because: Validation rules are partial for some field types. |
| MAL-03 Relationships and lifecycle states declarable | assessed | 2 | 3 |  | A, medium |  | M2O, O2M, M2M and M2A relations are declared in the UI with database-level referential actions; lifecycle states are not a feature, and v0.3 accepts either at level 3. Scored at the lower reading under rule 11 because: If lifecycle states are considered central for this product. |
| MAL-04 API per entity is generic or generated | assessed | 3 | 4 |  | A, medium |  | Generic REST (/items/:collection) and a GraphQL schema generated at runtime from the data model per role (api/src/services/graphql/index.ts:23-89): typed, with field selection, deep filters and permission and field validation from the definition. Scored at the lower reading under rule 11 because: If 'typed projections' requires per-type client types rather than runtime GraphQL types. |
| MAL-05 API reshapes at runtime from definitions | assessed | 3 |  |  | A, medium |  | Schema changes invalidate the cached schema so REST and GraphQL reflect them live. No per-consumer schema versions or dry-run. |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A, high |  | /server/specs/oas and /server/specs/graphql are generated from the live schema (api/src/controllers/server.ts:21-37); typed SDK (sdk/); structured error codes (packages/errors). No mutation dry-run, so not 4. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A, medium |  | Collection layouts (table, cards, calendar, kanban, map), form widths, groups and interface options are stored as presets and field meta and edited in the Data Studio per role (app/src/layouts); Insights dashboards; visual editing of connected frontends (packages/visual-editing). One project per instance, so per-tenant reads as per project. Scored at the lower reading under rule 11 because: No schema validation of layout props and no preview of layout changes before they apply. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | assessed | 3 |  |  | A, medium |  | Every collection renders generic list layouts, item detail and create forms from field meta and interfaces (app/src/layouts, app/src/interfaces); admins configure presets. |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 3 |  |  | A, medium |  | Admin appearance settings with light and dark theme overrides and custom CSS (api/src/database/seeds/13-settings.yaml, packages/themes), custom translation strings, and 93 locale files maintained through Crowdin (crowdin.yml). |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 | 3 |  | A, medium |  | Flows compose triggers (event, schedule, webhook, manual, another flow) and operations (condition, exec, item CRUD, request, notification, mail, transform, trigger) across any collection in the admin UI (api/src/operations, api/src/flows.ts). No test or simulation mode. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 | 3 |  | A, medium |  | Action and filter events fire for every collection including user-defined ones (api/src/emitter.ts); outbound webhooks are Flow request operations with flow logs. No retry or replay in api/src/flows.ts. |
| MAL-12 Sandboxed server-side hooks | assessed | 3 |  |  | A, high |  | The exec operation and sandboxed API extensions run in isolated-vm with memory and time limits (FLOWS_RUN_SCRIPT_MAX_MEMORY 32, FLOWS_RUN_SCRIPT_TIMEOUT 10000, packages/env/src/constants/defaults.ts:213-214) and requested scopes including a request URL allowlist (packages/extensions/src/shared/schemas/options.ts:14-27); triggered by events and requests. |
| MAL-13 Plugin lane breadth | assessed | 3 | 4 |  | A, medium |  | Interfaces, displays, layouts, modules, panels, themes, endpoints, hooks, operations and bundles as code extensions (packages/extensions), plus declarative Flows, presets, translations and theme overrides; in-app marketplace backed by packages/extensions-registry. |
| MAL-14 Runtime isolation and dependency control | assessed | 3 |  |  | A, high |  | Sandboxed API extensions run in isolated-vm with memory and time limits and a request URL allowlist; marketplace installs default to sandbox trust (MARKETPLACE_TRUST sandbox, packages/env/src/constants/defaults.ts:124). Local non-sandboxed extensions keep full trust. |
| MAL-15 Developer loop | assessed | 2 |  |  | A, medium |  | Extensions SDK with create, build and dev commands (packages/create-directus-extension, packages/extensions-sdk) and Docker Compose for local development; no preview against a remote project or staged branches. |
| MAL-16 Canonical data model with a mapping layer | assessed | 1 |  |  | A, medium |  | No canonical integration model; integrations are Flow request operations or custom extensions. |
| MAL-17 Connector definition or SDK | assessed | 1 | 2 |  | A, medium |  | The extensions SDK lets engineers build operation extensions that wrap external APIs; no connector definition covering auth, sync and lifecycle. Scored at the lower reading under rule 11 because: If a general extension SDK does not count as a connector SDK. |
| MAL-18 Stable versioned contracts | assessed | 1 | 2 |  | A, medium |  | No path versioning; breaking changes are announced in release notes; no deprecation windows or idempotent sync. |
| MAL-19 Machine-readable capability surface for agents | assessed | 3 | 4 |  | A, medium |  | AI-qualified reading: 3. MCP server over the same tool registry (api/src/ai/mcp/server.ts) with OAuth scope and audience checks (server.ts:75-102) and zod-typed tools; the schema tool returns the live data model as a capability map. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. In-app AI assistant with grounded tools over items, files, schema, relations and flows, running under the user's permissions (api/src/ai/chat, app/src/ai); admins author collections, fields, relations and flows in natural language with an approval card showing the proposed call. LLM tracing to Braintrust or Langfuse (api/src/ai/telemetry); no groundedness evaluation. Scored at the lower reading under rule 11 because: If an approval card is not a preview of the resulting change. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A, medium |  | Activity rows are written per request and are queryable by in-product Insights dashboards; vendor telemetry counters (api/src/telemetry); AI telemetry to Braintrust or Langfuse (api/src/ai/telemetry). Scored at the lower reading under rule 11 because: Activity is an audit stream, not per-feature usage instrumentation. |
| LRN-02 Structured learning signals | assessed | 1 |  |  | A, medium |  | Item comments are free text; no typed feedback or rating objects linked to definitions. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A, high |  | Every flow run records each operation step with its resolve or reject status as activity and revisions (api/src/flows.ts:414-454), viewable per flow; admins can read system logs (app/src/modules/settings/routes/system-logs). Failed actions outside flows are not recorded per product area. |
| LRN-04 Cross-source mining inside the product | assessed | 1 | 2 |  | A, medium |  | Insights dashboards can query any collection including activity; no joined usage, support and delivery models or mining. |
| LRN-05 Automated diagnosis | assessed | 1 |  |  | A, medium |  | AI-qualified reading: 0. Engineers read logs; no grouping or attached context. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A, medium |  | AI-qualified reading: 0. No recommendation or proposal features; the assistant acts only on request. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A, medium |  | AI-qualified reading: 0. The AI assistant acts only on request (api/src/ai); nothing learns from use. |
| LRN-08 Learned changes are validated before they take effect | assessed | 2 |  |  | A, high |  | AI-qualified reading: 2. Re-scored 1 to 2 under the v0.7 boundary, which scores the checks on changes the product's AI makes. Every AI tool call is parsed against its zod schema before it can run (registry.ts #parseInput, collections/index.ts:20-66), deletes can be blocked wholesale (registry.ts:202), and the change then passes the same service validation as a person's; a person approves each mutating call. No evaluation against a baseline. Directus has no learning-from-experience loop. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A, medium |  | No binding of changes to baselines or metrics. |
| LRN-10 The improvement loop improves itself | assessed | 0 |  |  | A, medium |  | The checks that govern change are code: zod schemas on every AI tool (api/src/ai/tools/*/index.ts, parsed in registry.ts), service-level validation, and the tool prompts (api/src/ai/tools/*/prompt.md). The only governing settings are the project's MCP allow-deletes setting (api/src/controllers/mcp/index.ts:52) and each user's per-tool approval modes kept in the app (app/src/ai/stores/use-ai.ts:179-185); neither is linked to results. No evaluation sets exist (AIR-05 0) and nothing records a failure against the check that missed it. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A, medium |  | Component library and theme tokens exist (packages/themes, app/src/components); no automated accessibility scanning in CI or tests. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A, medium |  | Activity and revisions record every item mutation including system collections (schema, permissions, settings, flows), with an admin Activity module and retention (ACTIVITY_RETENTION and REVISIONS_RETENTION, packages/env/src/constants/defaults.ts:167-172). There is no approval object, so approvals are not covered. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 0 | 1 |  | A, medium |  | No data-subject export or erasure features and no privacy tags (searched for gdpr, erasure, anonymisation and personal data); admins can export collections and delete items by hand. Scored at the lower reading under rule 11 because: If manual export and deletion do not count as a mechanism. |
| GOV-04 Security as infrastructure | assessed | 2 | 3 |  | A, medium | IT | Policies with collection, field and item-level rules apply to every collection including new ones; field validation is generic. CodeQL runs on a schedule, not on pull requests (.github/workflows/codeql-analysis.yml:5), so scanning does not gate change. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A, high | IT | Revisions can be reverted for items and system records (api/src/services/revisions.ts:13-18); data-model changes have no rollback in the UI. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Data-model changes have no rollback. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 | 3 |  | A, medium |  | Content Versioning stages item changes for compare and promote (api/src/services/versions.ts:436-521); definitions and configuration move between projects through schema snapshot, diff and apply (api/src/controllers/schema.ts) and CLI sync pull, diff and push (packages/cli/src/commands/sync), which is an engineer flow. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 | 3 |  | A, medium |  | Mutating AI tool calls require approval unless the user set that tool to always-allow (api/src/ai/tools/registry.ts:198-214, app/src/ai/stores/use-ai.ts:179-185); deletes can be disabled wholesale (allowDeletes). Approvals are not recorded as audit objects. |
| GOV-08 Upgrade safety | assessed | 2 |  |  | A, medium |  | Extension SDK and types are versioned packages (packages/extensions-sdk, packages/extensions); system migrations run automatically; schema snapshots apply through diff. No automated compatibility check of extensions against a new release was found. |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. The assistant acts with the user's accountability; MCP clients get OAuth-scoped tokens; mutations need approval; rate limiter and activity rows apply. No idempotency keys or dry-run. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A, high |  | AI-qualified reading: 2. Each AI tool can require approval and deletes can be disabled wholesale (api/src/ai/tools/registry.ts:198-214); there is no per-period or blast-radius limit. |
| GOV-11 Learning-input integrity | assessed | 1 |  |  | A, medium |  | AI-qualified reading: 1. AI changes are recorded as revisions by the acting user, but inputs carry no provenance and nothing separates untrusted content from instructions (api/src/ai). |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 | 4 |  | A, medium |  | Kernel is users, roles, policies, permissions, files, collections, flows, comments and notifications, with no domain nouns; system collections accept custom fields. |
| EXP-02 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A, medium |  | Any domain can be modelled as collections, relations, flows and policies with no kernel change, but no domain shipped this way is evidenced inside the repository. |
| EXP-03 A domain ships as an installable bundle | assessed | 2 | 3 |  | A, medium |  | Schema snapshot and apply cover collections, fields and relations; CLI sync pulls and pushes roles, policies, permissions, flows, operations, dashboards, panels, presets, translations and settings between projects (packages/cli/src/commands/sync). Not a versioned bundle with install semantics. |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A, medium |  | No record of failed searches or unsupported requests was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A, medium |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 | 2 |  | A, medium |  | Extensions are installed per project; there is no cohort launch. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A, medium |  | Schema-aware tools read live collections, fields, relations, items and files (api/src/ai/tools/schema, items, files); results come from the source records. |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 3 |  |  | A, high | IT | Tool calls run through services with the requesting user's accountability, so Directus permissions apply (api/src/ai/tools/items, tests pass accountability through: items/index.test.ts). |
| AIR-05 Offline AI evaluation | assessed | 0 |  |  | A, medium |  | No evaluation harness for the assistant (searched api/src/ai for eval). |
| AIR-06 Regression gating before release | assessed | 0 |  |  | A, medium |  | No evaluation in CI; AI changes ship unevaluated (.github/workflows). |
| AIR-07 AI action tracing and auditability | assessed | 2 |  |  | A, medium |  | Opt-in Langfuse and Braintrust telemetry records model calls with user, role, provider and model (api/src/ai/telemetry); revisions record data changes by the user, without the model or prompt. |
| AIR-01 Model and provider portability and resilience | assessed | 2 |  |  | A, medium |  | OpenAI, Anthropic, Google and OpenAI-compatible providers configured by admins, model chosen in the chat (api/src/ai/providers/registry.ts); no fallback or declared resilience strategy. |
| AIR-02 AI usage and per-customer cost controls | assessed | 1 |  |  | A, high |  | Usage is streamed to the client per request (api/src/ai/chat/controllers/chat.post.ts:71-72); not recorded per user, and no budgets. |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 0 |  |  | A, medium |  | No feedback or quality monitoring for the assistant. |

Grade cell: evidence grade, then confidence where recorded. Facets: I implemented, T tested, O operated. Operated supports a Proven reading and never changes a score.
