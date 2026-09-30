# Directus evidence

Read at github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **3** (grade A). Admins create collections in the Data Model UI and the API creates real tables with no migration or deploy (api/src/services/collections.ts); the AI assistant can also author collections through zod-validated tools behind an approval gate (api/src/ai/tools/collections/index.ts:20-66, api/src/ai/tools/registry.ts:198-214). No dry-run, so not 4.
  - Alternate reading 4: AI authoring through a gate already exists; only dry-run and versioned definitions are missing.
- **A2 Field definitions carry type and validation**: **3** (grade A). Typed fields with validation rules, conditions, required, unique and is_indexed are created in the UI and read by forms and the generated APIs (api/services/fields.ts:62, 1008-1012). v0.3 moved the privacy tag to E3.
  - Alternate reading 2: Validation rules are partial for some field types.
- **A3 Relationships and lifecycle states declarable**: **3** (grade A). M2O, O2M, M2M and M2A relations are declared in the UI with database-level referential actions; lifecycle states are not a feature, and v0.3 accepts either at level 3.
  - Alternate reading 2: If lifecycle states are considered central for this product.
## B API surface generation

- **B1 API per entity is generic or generated**: **4** (grade A). Generic REST (/items/:collection) and a GraphQL schema generated at runtime from the data model per role (api/src/services/graphql/index.ts:23-89): typed, with field selection, deep filters and permission and field validation from the definition.
  - Alternate reading 3: If 'typed projections' requires per-type client types rather than runtime GraphQL types.
- **B2 API reshapes at runtime from definitions**: **3** (grade A). Schema changes invalidate the cached schema so REST and GraphQL reflect them live. No per-consumer schema versions or dry-run.
- **B3 Machine-readable contract with introspection and dry-run**: **3** (grade A). /server/specs/oas and /server/specs/graphql are generated from the live schema (api/src/controllers/server.ts:21-37); typed SDK (sdk/); structured error codes (packages/errors). No mutation dry-run, so not 4.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **3** (grade A). Collection layouts (table, cards, calendar, kanban, map), form widths, groups and interface options are stored as presets and field meta and edited in the Data Studio per role (app/src/layouts); Insights dashboards; visual editing of connected frontends (packages/visual-editing). One project per instance, so per-tenant reads as per project.
  - Alternate reading 2: No schema validation of layout props and no preview of layout changes before they apply.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **3** (grade A). Every collection renders generic list layouts, item detail and create forms from field meta and interfaces (app/src/layouts, app/src/interfaces); admins configure presets.
- **C3 Theme tokens and text are data with tenant overrides**: **3** (grade A). Admin appearance settings with light and dark theme overrides and custom CSS (api/src/database/seeds/13-settings.yaml, packages/themes), custom translation strings, and 93 locale files maintained through Crowdin (crowdin.yml).
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A). Flows compose triggers (event, schedule, webhook, manual, another flow) and operations (condition, exec, item CRUD, request, notification, mail, transform, trigger) across any collection in the admin UI (api/src/operations, api/src/flows.ts). No test or simulation mode.
  - Alternate reading 3: Everything in level 3 except a test mode.
- **D2 Event model with webhooks or subscriptions and retry**: **2** (grade A). Action and filter events fire for every collection including user-defined ones (api/src/emitter.ts); outbound webhooks are Flow request operations with flow logs. No retry or replay in api/src/flows.ts.
  - Alternate reading 3: Admin subscriptions with delivery logs exist; only retry is missing.
- **D3 Sandboxed server-side hooks**: **3** (grade A). The exec operation and sandboxed API extensions run in isolated-vm with memory and time limits (FLOWS_RUN_SCRIPT_MAX_MEMORY 32, FLOWS_RUN_SCRIPT_TIMEOUT 10000, packages/env/src/constants/defaults.ts:213-214) and requested scopes including a request URL allowlist (packages/extensions/src/shared/schemas/options.ts:14-27); triggered by events and requests.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). Component library and theme tokens exist (packages/themes, app/src/components); no automated accessibility scanning in CI or tests.
  - Alternate reading 2: Kit and tokens are present; the anchors bundle kit and scans.
- **E2 Audit generic over entities, definition changes and approvals**: **2** (grade A). Activity and revisions record every item mutation including system collections (schema, permissions, settings, flows), with an admin Activity module and retention (ACTIVITY_RETENTION and REVISIONS_RETENTION, packages/env/src/constants/defaults.ts:167-172). There is no approval object, so approvals are not covered.
  - Alternate reading 3: All other level-3 clauses are met.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **1** (grade A). No data-subject export or erasure features and no privacy tags (searched for gdpr, erasure, anonymisation and personal data); admins can export collections and delete items by hand.
  - Alternate reading 0: If manual export and deletion do not count as a mechanism.
- **E4 Security as infrastructure**: **2** (grade A). Policies with collection, field and item-level rules apply to every collection including new ones; field validation is generic. CodeQL runs on a schedule, not on pull requests (.github/workflows/codeql-analysis.yml:5), so scanning does not gate change.
  - Alternate reading 3: Authorisation is generated per defined type; only the gating clause fails.
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Revisions can be reverted for items and system records (api/src/services/revisions.ts:13-18); data-model changes have no rollback in the UI.
  - Alternate reading 3: Revert works on system collections too, so most customisation surfaces are covered through the API.
- **F2 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Content Versioning stages item changes for compare and promote (api/src/services/versions.ts:436-521); definitions and configuration move between projects through schema snapshot, diff and apply (api/src/controllers/schema.ts) and CLI sync pull, diff and push (packages/cli/src/commands/sync), which is an engineer flow.
  - Alternate reading 3: Versions with compare-and-promote already form a proposal, review and apply flow, but for content only.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A). Mutating AI tool calls require approval unless the user set that tool to always-allow (api/src/ai/tools/registry.ts:198-214, app/src/ai/stores/use-ai.ts:179-185); deletes can be disabled wholesale (allowDeletes). Approvals are not recorded as audit objects.
  - Alternate reading 3: Per-tool approval modes are a policy per change class; only recorded approvals are missing.
- **F4 Upgrade safety**: **2** (grade A). Extension SDK and types are versioned packages (packages/extensions-sdk, packages/extensions); system migrations run automatically; schema snapshots apply through diff. No automated compatibility check of extensions against a new release was found.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **3** (grade A). Collections are real tables, so there is no generic store; fields marked is_indexed get database indexes (api/src/services/fields.ts:1008-1012); schema and response caching (CACHE_* settings).
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). One project per deployment; a pressure limiter is on by default and a rate limiter is available (packages/env/src/constants/defaults.ts:29, 216).
- **G3 Ceilings measured, not discovered in incidents**: **0** (grade A). No load or performance suite in the repository and no documented per-surface limits (searched for k6, locust, artillery, benchmark and load test).
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **1** (grade A). API and Data Studio ship as one Node process and one container image (Dockerfile); packages are separate but deployed together.
  - Alternate reading 2: The anchors do not separate 'one artifact' (0) from 'monolith, manual' (1) from a containerised monolith.
- **H2 Module boundaries enforced by tooling**: **2** (grade A). pnpm workspace packages with declared dependencies (pnpm-workspace.yaml); no architectural lint.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Lint and tests run on pull requests including drafts (.github/workflows/check.yml:3-12), but a Skip Checks label bypasses them (check.yml:30), E2E runs only when labelled (e2e-pr.yml:15) and CodeQL is scheduled.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Interfaces, displays, layouts, modules, panels, themes, endpoints, hooks, operations and bundles as code extensions (packages/extensions), plus declarative Flows, presets, translations and theme overrides; in-app marketplace backed by packages/extensions-registry.
  - Alternate reading 4: A registry and marketplace exist; plugin points are not generated from definitions.
- **I2 Runtime isolation and dependency control**: **3** (grade A). Sandboxed API extensions run in isolated-vm with memory and time limits and a request URL allowlist; marketplace installs default to sandbox trust (MARKETPLACE_TRUST sandbox, packages/env/src/constants/defaults.ts:124). Local non-sandboxed extensions keep full trust.
- **I3 Developer loop**: **2** (grade A). Extensions SDK with create, build and dev commands (packages/create-directus-extension, packages/extensions-sdk) and Docker Compose for local development; no preview against a remote project or staged branches.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **3** (grade A). MCP server over the same tool registry (api/src/ai/mcp/server.ts) with OAuth scope and audience checks (server.ts:75-102) and zod-typed tools; the schema tool returns the live data model as a capability map.
  - Alternate reading 4: Items and schema tools cover user-defined collections at runtime; tools are generic rather than generated per collection.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). In-app AI assistant with grounded tools over items, files, schema, relations and flows, running under the user's permissions (api/src/ai/chat, app/src/ai); admins author collections, fields, relations and flows in natural language with an approval card showing the proposed call. LLM tracing to Braintrust or Langfuse (api/src/ai/telemetry); no groundedness evaluation.
  - Alternate reading 2: If an approval card is not a preview of the resulting change.
- **K3 Agent-safe actions**: **2** (grade A). The assistant acts with the user's accountability; MCP clients get OAuth-scoped tokens; mutations need approval; rate limiter and activity rows apply. No idempotency keys or dry-run.
  - Alternate reading 3: Scoped identity, approval-as-preview, rate limits and audit are present; idempotency is the gap.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **1** (grade A). No canonical integration model; integrations are Flow request operations or custom extensions.
- **N2 Connector definition or SDK**: **2** (grade A). The extensions SDK lets engineers build operation extensions that wrap external APIs; no connector definition covering auth, sync and lifecycle.
  - Alternate reading 1: If a general extension SDK does not count as a connector SDK.
- **N3 Stable versioned contracts**: **1** (grade A). No path versioning; breaking changes are announced in release notes; no deprecation windows or idempotent sync.
  - Alternate reading 2: The API is documented through a generated OpenAPI spec.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **3** (grade A). Kernel is users, roles, policies, permissions, files, collections, flows, comments and notifications, with no domain nouns; system collections accept custom fields.
  - Alternate reading 4: System collections are themselves extensible definitions.
- **O2 A new domain is expressible without kernel change**: **2** (grade A). Any domain can be modelled as collections, relations, flows and policies with no kernel change, but no domain shipped this way is evidenced inside the repository.
  - Alternate reading 3: Domain templates exist in other repositories (grade C knowledge), which would prove the path.
- **O3 A domain ships as an installable bundle**: **2** (grade A). Schema snapshot and apply cover collections, fields and relations; CLI sync pulls and pushes roles, policies, permissions, flows, operations, dashboards, panels, presets, translations and settings between projects (packages/cli/src/commands/sync). Not a versioned bundle with install semantics.
  - Alternate reading 3: A pulled sync directory is a versionable, installable bundle of definitions, layouts and rules.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). Activity rows are written per request and are queryable by in-product Insights dashboards; vendor telemetry counters (api/src/telemetry); AI telemetry to Braintrust or Langfuse (api/src/ai/telemetry).
  - Alternate reading 2: Activity is an audit stream, not per-feature usage instrumentation.
- **J2 Structured learning signals**: **1** (grade A). Item comments are free text; no typed feedback or rating objects linked to definitions.
- **J3 Cross-source mining inside the product**: **1** (grade A). Insights dashboards can query any collection including activity; no joined usage, support and delivery models or mining.
  - Alternate reading 2: In-product dashboards over system collections are a partial join.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **0** (grade A). No recommendation or proposal features; the assistant acts only on request.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **2** (grade A). An AI authoring lane turns admin requests into schema, flow and item changes behind approvals, one project at a time (api/src/ai/tools); nothing applies accepted proposals across projects.
  - Alternate reading 1: If the lane is judged manual per tenant because a human drives every change.
- **M4 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **1** (grade A). The AI assistant acts only on request (api/src/ai); nothing learns from use.
- **P2 Learned changes are validated before they take effect**: **1** (grade A). AI-authored changes pass a human approval (api/src/ai/tools/registry.ts:198-214); there is no evaluation against a baseline.
## L Factory surfaces

- **L1 Verification surface**: **3** (grade A). /server/info with version, /server/health, generated specs (api/src/controllers/server.ts:21-80) and /schema/snapshot as a machine-readable configuration snapshot (api/src/controllers/schema.ts).
- **L2 Environment reproducibility**: **2** (grade A). Versioned container images, a bootstrap command, schema apply and CLI sync recreate a configured instance; E2E tests start instances per database vendor (tests/e2e). No per-change ephemeral environment or feature flags.
  - Alternate reading 3: Instances are reproducible from a build id and snapshot in minutes.
- **L3 Machine verifiability**: **2** (grade A). E2E API suite across database vendors (tests/e2e), run on pull requests only when labelled; no changed-path map or adoption instrumentation.
