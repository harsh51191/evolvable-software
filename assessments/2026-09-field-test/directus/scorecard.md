# Directus: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the directus monorepo (API, Data Studio app, SDK, CLI, extensions SDK and registry, AI assistant and MCP server). Directus Cloud, the hosted marketplace catalogue and templates published in other repositories are out of scope.

## Reading

**Strongest:** Malleability (2.6), with runtime-generated typed GraphQL and REST (B1 4) and real sandboxing for scripts and marketplace extensions (D3 3, I2 3). Its AI assistant authors collections and flows behind a per-tool approval gate. **Largest gap:** Learning (1.1). Nothing learns from use, and there are no structured feedback signals (J2 1, P1 1).

## Limits

Repository evidence only, main branch at the tip named above. No running instance was inspected, so approval and preview behaviour is read from code. Directus Cloud, the hosted marketplace catalogue and published templates are out of scope. The repository is under a source-available licence, so some features may be licence-gated (api/src/license); entitlement checks were not traced per feature. Single rater; 18 alternate readings mark likely disagreements.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main). Archetype **configurable-application-platform**.

Coverage: 49 assessed, 0 not evidenced, 0 not applicable. Grades: 49 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.6 | productised | 2.3–3.0 | 2.6 | 2.6 | 2.6 |
| governance | 1.8 | mechanism | 1.6–2.5 | 1.8 | 1.8 | 1.8 |
| learning | 1.1 | code-only | 0.9–1.2 | 1.1 | 1.1 | 1.1 |
| factory | 2.0 | mechanism | 2.0–2.3 | 2.0 | 2.0 | 2.0 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.8 | 2.8 |
| Governance | 1.8 | 1.8 |
| Learning | 1.1 | 1.1 |
| Factory | 2.0 | 2.0 |
| Agent Interface | 2.7 | 2.7 |
| Extension Surface | 2.0 | 2.0 |
| Operational Scalability | 1.7 | 1.7 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 1 fail | 1 fail |
| propose | M1, P1 | 2 | 1 fail | 1 fail |
| review | F2 | 2 | 2 pass | 2 pass |
| gate | F3 | 3 | 2 fail | 2 fail |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 1 fail | 1 fail |
| verify | L1 | 2 | 3 pass | 3 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| A Entity and schema as data | 3.0 |
| B API surface generation | 3.3 |
| C Rendering follows the definition | 3.0 |
| D Behaviour as data | 2.3 |
| E Compliance and security as infrastructure | 1.5 |
| F Change control | 2.0 |
| G Performance under genericity | 1.7 |
| H Stack flexibility and verification | 1.7 |
| I Extension ecosystem | 2.7 |
| J Observe | 1.7 |
| K Agent and conversational readiness | 2.7 |
| L Factory surfaces | 2.3 |
| M Advise and act | 0.7 |
| N Integration and connector extensibility | 1.3 |
| O Adjacent-domain expansion | 2.3 |
| P Learn from experience | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | assessed | 3 | 4 |  | A | Admins create collections in the Data Model UI and the API creates real tables with no migration or deploy (api/src/services/collections.ts); the AI assistant can also author collections through zod-validated tools behind an approval gate (api/src/ai/tools/collections/index.ts:20-66, api/src/ai/tools/registry.ts:198-214). No dry-run, so not 4. |
| A2 Field definitions carry type and validation | assessed | 3 | 2 |  | A | Typed fields with validation rules, conditions, required, unique and is_indexed are created in the UI and read by forms and the generated APIs (api/services/fields.ts:62, 1008-1012). v0.3 moved the privacy tag to E3. |
| A3 Relationships and lifecycle states declarable | assessed | 3 | 2 |  | A | M2O, O2M, M2M and M2A relations are declared in the UI with database-level referential actions; lifecycle states are not a feature, and v0.3 accepts either at level 3. |
| B1 API per entity is generic or generated | assessed | 4 | 3 |  | A | Generic REST (/items/:collection) and a GraphQL schema generated at runtime from the data model per role (api/src/services/graphql/index.ts:23-89): typed, with field selection, deep filters and permission and field validation from the definition. |
| B2 API reshapes at runtime from definitions | assessed | 3 |  |  | A | Schema changes invalidate the cached schema so REST and GraphQL reflect them live. No per-consumer schema versions or dry-run. |
| B3 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A | /server/specs/oas and /server/specs/graphql are generated from the live schema (api/src/controllers/server.ts:21-37); typed SDK (sdk/); structured error codes (packages/errors). No mutation dry-run, so not 4. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 3 | 2 |  | A | Collection layouts (table, cards, calendar, kanban, map), form widths, groups and interface options are stored as presets and field meta and edited in the Data Studio per role (app/src/layouts); Insights dashboards; visual editing of connected frontends (packages/visual-editing). One project per instance, so per-tenant reads as per project. |
| C2 Generic list, detail and intake widgets from definition plus view spec | assessed | 3 |  |  | A | Every collection renders generic list layouts, item detail and create forms from field meta and interfaces (app/src/layouts, app/src/interfaces); admins configure presets. |
| C3 Theme tokens and text are data with tenant overrides | assessed | 3 |  |  | A | Admin appearance settings with light and dark theme overrides and custom CSS (api/src/database/seeds/13-settings.yaml, packages/themes), custom translation strings, and 93 locale files maintained through Crowdin (crowdin.yml). |
| D1 Rules engine with declarative conditions and actions | assessed | 2 | 3 |  | A | Flows compose triggers (event, schedule, webhook, manual, another flow) and operations (condition, exec, item CRUD, request, notification, mail, transform, trigger) across any collection in the admin UI (api/src/operations, api/src/flows.ts). No test or simulation mode. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 2 | 3 |  | A | Action and filter events fire for every collection including user-defined ones (api/src/emitter.ts); outbound webhooks are Flow request operations with flow logs. No retry or replay in api/src/flows.ts. |
| D3 Sandboxed server-side hooks | assessed | 3 |  |  | A | The exec operation and sandboxed API extensions run in isolated-vm with memory and time limits (FLOWS_RUN_SCRIPT_MAX_MEMORY 32, FLOWS_RUN_SCRIPT_TIMEOUT 10000, packages/env/src/constants/defaults.ts:213-214) and requested scopes including a request URL allowlist (packages/extensions/src/shared/schemas/options.ts:14-27); triggered by events and requests. |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A | Component library and theme tokens exist (packages/themes, app/src/components); no automated accessibility scanning in CI or tests. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A | Activity and revisions record every item mutation including system collections (schema, permissions, settings, flows), with an admin Activity module and retention (ACTIVITY_RETENTION and REVISIONS_RETENTION, packages/env/src/constants/defaults.ts:167-172). There is no approval object, so approvals are not covered. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 1 | 0 |  | A | No data-subject export or erasure features and no privacy tags (searched for gdpr, erasure, anonymisation and personal data); admins can export collections and delete items by hand. |
| E4 Security as infrastructure | assessed | 2 | 3 |  | A | Policies with collection, field and item-level rules apply to every collection including new ones; field validation is generic. CodeQL runs on a schedule, not on pull requests (.github/workflows/codeql-analysis.yml:5), so scanning does not gate change. |
| F1 Definitions and layouts versioned with rollback | assessed | 2 | 3 |  | A | Revisions can be reverted for items and system records (api/src/services/revisions.ts:13-18); data-model changes have no rollback in the UI. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 2 | 3 |  | A | Content Versioning stages item changes for compare and promote (api/src/services/versions.ts:436-521); definitions and configuration move between projects through schema snapshot, diff and apply (api/src/controllers/schema.ts) and CLI sync pull, diff and push (packages/cli/src/commands/sync), which is an engineer flow. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 | 3 |  | A | Mutating AI tool calls require approval unless the user set that tool to always-allow (api/src/ai/tools/registry.ts:198-214, app/src/ai/stores/use-ai.ts:179-185); deletes can be disabled wholesale (allowDeletes). Approvals are not recorded as audit objects. |
| F4 Upgrade safety | assessed | 2 |  |  | A | Extension SDK and types are versioned packages (packages/extensions-sdk, packages/extensions); system migrations run automatically; schema snapshots apply through diff. No automated compatibility check of extensions against a new release was found. |
| G1 Indexed query path, never a scan of a generic store | assessed | 3 |  |  | A | Collections are real tables, so there is no generic store; fields marked is_indexed get database indexes (api/src/services/fields.ts:1008-1012); schema and response caching (CACHE_* settings). |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A | One project per deployment; a pressure limiter is on by default and a rate limiter is available (packages/env/src/constants/defaults.ts:29, 216). |
| G3 Ceilings measured, not discovered in incidents | assessed | 0 |  |  | A | No load or performance suite in the repository and no documented per-surface limits (searched for k6, locust, artillery, benchmark and load test). |
| H1 Layers deploy independently | assessed | 1 | 2 |  | A | API and Data Studio ship as one Node process and one container image (Dockerfile); packages are separate but deployed together. |
| H2 Module boundaries enforced by tooling | assessed | 2 |  |  | A | pnpm workspace packages with declared dependencies (pnpm-workspace.yaml); no architectural lint. |
| H3 Every change class has an automated pre-land check | assessed | 2 |  |  | A | Lint and tests run on pull requests including drafts (.github/workflows/check.yml:3-12), but a Skip Checks label bypasses them (check.yml:30), E2E runs only when labelled (e2e-pr.yml:15) and CodeQL is scheduled. |
| I1 Plugin lane breadth | assessed | 3 | 4 |  | A | Interfaces, displays, layouts, modules, panels, themes, endpoints, hooks, operations and bundles as code extensions (packages/extensions), plus declarative Flows, presets, translations and theme overrides; in-app marketplace backed by packages/extensions-registry. |
| I2 Runtime isolation and dependency control | assessed | 3 |  |  | A | Sandboxed API extensions run in isolated-vm with memory and time limits and a request URL allowlist; marketplace installs default to sandbox trust (MARKETPLACE_TRUST sandbox, packages/env/src/constants/defaults.ts:124). Local non-sandboxed extensions keep full trust. |
| I3 Developer loop | assessed | 2 |  |  | A | Extensions SDK with create, build and dev commands (packages/create-directus-extension, packages/extensions-sdk) and Docker Compose for local development; no preview against a remote project or staged branches. |
| K1 Machine-readable capability surface for agents | assessed | 3 | 4 |  | A | MCP server over the same tool registry (api/src/ai/mcp/server.ts) with OAuth scope and audience checks (server.ts:75-102) and zod-typed tools; the schema tool returns the live data model as a capability map. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 2 |  | A | In-app AI assistant with grounded tools over items, files, schema, relations and flows, running under the user's permissions (api/src/ai/chat, app/src/ai); admins author collections, fields, relations and flows in natural language with an approval card showing the proposed call. LLM tracing to Braintrust or Langfuse (api/src/ai/telemetry); no groundedness evaluation. |
| K3 Agent-safe actions | assessed | 2 | 3 |  | A | The assistant acts with the user's accountability; MCP clients get OAuth-scoped tokens; mutations need approval; rate limiter and activity rows apply. No idempotency keys or dry-run. |
| N1 Canonical data model with a mapping layer | assessed | 1 |  |  | A | No canonical integration model; integrations are Flow request operations or custom extensions. |
| N2 Connector definition or SDK | assessed | 2 | 1 |  | A | The extensions SDK lets engineers build operation extensions that wrap external APIs; no connector definition covering auth, sync and lifecycle. |
| N3 Stable versioned contracts | assessed | 1 | 2 |  | A | No path versioning; breaking changes are announced in release notes; no deprecation windows or idempotent sync. |
| O1 Kernel concepts are domain-neutral | assessed | 3 | 4 |  | A | Kernel is users, roles, policies, permissions, files, collections, flows, comments and notifications, with no domain nouns; system collections accept custom fields. |
| O2 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A | Any domain can be modelled as collections, relations, flows and policies with no kernel change, but no domain shipped this way is evidenced inside the repository. |
| O3 A domain ships as an installable bundle | assessed | 2 | 3 |  | A | Schema snapshot and apply cover collections, fields and relations; CLI sync pulls and pushes roles, policies, permissions, flows, operations, dashboards, panels, presets, translations and settings between projects (packages/cli/src/commands/sync). Not a versioned bundle with install semantics. |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 | 2 |  | A | Activity rows are written per request and are queryable by in-product Insights dashboards; vendor telemetry counters (api/src/telemetry); AI telemetry to Braintrust or Langfuse (api/src/ai/telemetry). |
| J2 Structured learning signals | assessed | 1 |  |  | A | Item comments are free text; no typed feedback or rating objects linked to definitions. |
| J3 Cross-source mining inside the product | assessed | 1 | 2 |  | A | Insights dashboards can query any collection including activity; no joined usage, support and delivery models or mining. |
| M1 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A | No recommendation or proposal features; the assistant acts only on request. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 2 | 1 |  | A | An AI authoring lane turns admin requests into schema, flow and item changes behind approvals, one project at a time (api/src/ai/tools); nothing applies accepted proposals across projects. |
| M4 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A | No binding of changes to baselines or metrics. |
| P1 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A | The AI assistant acts only on request (api/src/ai); nothing learns from use. |
| P2 Learned changes are validated before they take effect | assessed | 1 |  |  | A | AI-authored changes pass a human approval (api/src/ai/tools/registry.ts:198-214); there is no evaluation against a baseline. |
| L1 Verification surface | assessed | 3 |  |  | A | /server/info with version, /server/health, generated specs (api/src/controllers/server.ts:21-80) and /schema/snapshot as a machine-readable configuration snapshot (api/src/controllers/schema.ts). |
| L2 Environment reproducibility | assessed | 2 | 3 |  | A | Versioned container images, a bootstrap command, schema apply and CLI sync recreate a configured instance; E2E tests start instances per database vendor (tests/e2e). No per-change ephemeral environment or feature flags. |
| L3 Machine verifiability | assessed | 2 |  |  | A | E2E API suite across database vendors (tests/e2e), run on pull requests only when labelled; no changed-path map or adoption instrumentation. |

