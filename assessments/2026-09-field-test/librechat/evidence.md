# LibreChat evidence

Read at github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **A2 Field definitions carry type and validation**: **1** (grade A). No user-definable fields; schemas are code (packages/data-schemas/src/schema).
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **B3 Machine-readable contract with introspection and dry-run**: **1** (grade A). No published contract for LibreChat's own API; a shared typed client (packages/data-provider) serves the bundled frontend only. Agents are reachable through an OpenAI-compatible API.
  - Alternate reading 2: The OpenAI-compatible agents API is a machine-readable contract.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Interface settings from librechat.yaml can be overridden per user, group or role in the database (packages/data-schemas/src/types/config.ts:6-14); model specs and presets are data. No layout editor or preview.
  - Alternate reading 3: Principal-scoped overrides are tenant-overridable presentation data.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions (fixed per-archetype rule). If counted: 1.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). Theme registry (packages/client/src/theme) and 86 locale files synced through Locize (.github/workflows/locize-i18n-sync.yml); custom welcome and footer text in configuration; no admin theme editor.
  - Alternate reading 3: Per-principal configuration overrides include interface text.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A). Agents can be started by schedules and webhook triggers (api/server/services/Schedules, packages/api/src/agents/triggers); there is no general rules engine.
- **D2 Event model with webhooks or subscriptions and retry**: **2** (grade A). Inbound agent trigger deliveries record succeeded, retry and dead outcomes with stable identities (packages/data-schemas/src/types/triggerDelivery.ts:23-79); LibreChat does not publish its own entity events to subscribers.
- **D3 Sandboxed server-side hooks**: **2** (grade A). Admins and users attach MCP servers and OpenAPI actions that run custom server-side logic when agents call them; stdio MCP servers run as unsandboxed local processes; outbound connections have SSRF tests (packages/api/src/mcp/__tests__/MCPConnectionSSRF.test.ts).
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **2** (grade A). An axe linter workflow runs when triggered manually (.github/workflows/a11y.yml:8-28), Lighthouse audits exist (.github/workflows/lighthouse.yml, e2e/lighthouse), and the ESLint configuration includes accessibility rules.
  - Alternate reading 3: If Lighthouse or lint accessibility checks run on every pull request.
- **E2 Audit generic over entities, definition changes and approvals**: **2** (grade A). Admin audit route and audit-log schema (api/server/routes/admin/audit.js, packages/data-schemas/src/types/auditLog.ts); coverage of configuration and definition changes was not verified.
  - Alternate reading 3: Admin UI and a generic store exist.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Users export conversations and delete their accounts, and an admin deletion script removes user data (config/delete-user.js); not driven by field tags.
- **E4 Security as infrastructure**: **2** (grade A). ACL-based permissions for agents, prompts and MCP servers (packages/data-schemas/src/types/accessRole.ts, aclEntry.ts) and system grants; no security scanning in CI.
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product.
  - Alternate reading 3: Agents and prompts are the main customisation surfaces.
- **F2 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Prompt groups stage versions and promote one to production; agents are edited and saved directly; no review step.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A). Every definition change is a direct human action; the approval lifecycle (packages/api/src/stream/ApprovalLifecycle.ts) gates agent tool calls, not changes.
- **F4 Upgrade safety**: **2** (grade A). librechat.yaml carries a schema version checked at load, and UPGRADING.md documents migrations; compatibility is mostly manual.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **2** (grade A). MeiliSearch index for conversations and messages (search/) and MongoDB indexes; no definition-driven mapping.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Tenant isolation plugin with a coverage specification (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts), per-user token balances and rate limits; no noisy-neighbour detection.
  - Alternate reading 3: Data isolation is verified by tests; per-tenant limits are partial.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). Performance scan and benchmark suites (e2e/perf/scan.ts, e2e/benchmarks) and Lighthouse audits; no documented per-surface limits.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **2** (grade A). API and client ship together in one image; RAG API, search and a Langfuse fan-out service are separate containers with Helm charts (helm/).
- **H2 Module boundaries enforced by tooling**: **2** (grade A). Workspace packages with explicit dependencies and a circular-dependency check (config/circular-deps.mjs).
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Backend, frontend, static checks, mocked Playwright journeys and Docker smoke tests run on pull requests (.github/workflows/backend-review.yml, frontend-review.yml, static-checks.yml, playwright-mock.yml); accessibility runs on demand and there is no security scan.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **2** (grade A). MCP servers, OpenAPI actions, custom endpoints and skills extend agents; no plugin points for UI, layout or theme.
  - Alternate reading 3: Declarative (OpenAPI actions, YAML endpoints) and code (MCP) extension both exist.
- **I2 Runtime isolation and dependency control**: **2** (grade A). Remote MCP servers use OAuth and SSRF guards; code execution runs in an external sandbox service; stdio MCP servers run with full trust.
- **I3 Developer loop**: **2** (grade A). Local development documentation and a bring-your-own-model E2E harness (e2e/byom).
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **2** (grade A). LibreChat consumes MCP but does not expose itself as an MCP server (api/server/routes/mcp.js manages client connections); agents are reachable through an OpenAI-compatible API.
  - Alternate reading 1: If an OpenAI-compatible chat API is not an introspectable capability surface.
- **K2 Conversational operability for users and natural-language authoring for operators**: **2** (grade A). Members complete tasks conversationally with retrieval, web search, code and tool actions; there is no natural-language authoring of LibreChat's own definitions.
  - Alternate reading 3: The member half of level 3 is fully met.
- **K3 Agent-safe actions**: **3** (grade A). Agent API keys with expiry (packages/data-schemas/src/types/agentApiKey.ts), on-behalf-of token exchange for MCP (api/server/services/OboTokenService.js), tool-call approvals before execution, rate limits, audit logs and idempotent trigger deliveries.
  - Alternate reading 2: Idempotency covers trigger deliveries, not API mutations.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). Custom endpoints map any OpenAI-compatible provider onto the canonical chat interface through YAML configuration alone (librechat.example.yaml:575).
- **N2 Connector definition or SDK**: **3** (grade A). MCP is the connector standard, with OAuth flows, reconnect management and admin or user installation (api/server/services/initializeMCPs.js, initializeOAuthReconnectManager.js).
- **N3 Stable versioned contracts**: **2** (grade A). The agents API follows the OpenAI Chat Completions and Responses contracts; LibreChat's own API is unversioned.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **O2 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **O3 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 1.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). Token transactions are recorded per request and enforce balances live; OpenTelemetry and Langfuse tracing (otel/).
  - Alternate reading 2: Usage accounting rather than behaviour telemetry.
- **J2 Structured learning signals**: **2** (grade A). Message feedback with rating, tag and text is stored on messages (packages/data-schemas/src/schema/message.ts:103); no triage workflow.
- **J3 Cross-source mining inside the product**: **1** (grade A). No joined usage, support and delivery models.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **0** (grade A). No recommendation or proposal features.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **0** (grade A). No AI authoring lane for LibreChat's own definitions.
- **M4 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **1** (grade A), **3** with opt-in settings. By default nothing learns from use. With the memory block enabled (commented out in librechat.example.yaml:1351-1360), a memory agent stores user facts from recent chat automatically.
- **P2 Learned changes are validated before they take effect**: **1** (grade A). No checks on learned memories beyond configured key and token limits (librechat.example.yaml:1354-1358).
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). /health (api/server/index.js:328) and a startup configuration endpoint for the client; no build or version endpoint.
  - Alternate reading 3: The configuration endpoint is a machine-readable snapshot.
- **L2 Environment reproducibility**: **2** (grade A). Docker Compose and Helm charts, staging image builds (.github/workflows/dev-staging-images.yml) and seeded E2E setup (e2e/setup); no per-change ephemeral environment.
- **L3 Machine verifiability**: **2** (grade A). Mocked and property-based Playwright journeys (playwright-mock.yml, playwright-bombadil.yml); code-graph test selection runs in observe-only shadow mode (.github/workflows/codegraph-select.yml:1-13); no adoption instrumentation.
  - Alternate reading 3: The changed-path map exists, though not yet enforced.
