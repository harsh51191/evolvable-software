# LibreChat evidence

Read at github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Conversations, agents, prompts and users in MongoDB.
- **schema_changes**: true. Data migration scripts change stored documents and indexes (config/migrate-*.js).
- **multi_tenant**: true. A tenant isolation plugin scopes models by tenant (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts).
- **hosted_service**: true. Node API serving many users, with optional Redis (api/cache).
- **machine_actions**: true. The API changes agents, prompts and conversations for authenticated clients, and MCP tools act on users' behalf.
- **agent_mutations**: false. By default no AI changes LibreChat definitions; the memory agent is commented out in librechat.example.yaml:1351-1360.
- **evolution_auto_apply**: false. Definition changes are direct human actions by default.
- **definition_change_path**: true. librechat.yaml, agents and prompts are definitions.
- **code_release_path**: false. No first-party evolution system ships code changes.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **2** (grade A). MeiliSearch index for conversations and messages (search/) and MongoDB indexes; no definition-driven mapping.
- **ARC-02 Safe schema and data migrations**: **1** (grade A). One-off migration scripts with dry-run modes (config/migrate-*.js, package.json:134-139); no down steps.
  - Higher reading 2: Dry runs reduce migration risk.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A). With USE_REDIS, caches and request limits move to Redis for several instances (api/cache/clearPendingReq.js:5-39); Helm charts deploy it (helm/).
- **ARC-04 Reliable asynchronous work**: **1** (grade A). No job queue; background work runs in the API process.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A), facets: implemented, tested. Tenant isolation plugin with a coverage specification (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts), per-user token balances and rate limits; no noisy-neighbour detection.
  - Higher reading 3: Data isolation is verified by tests; per-tenant limits are partial.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **2** (grade A). Performance scan and benchmark suites (e2e/perf/scan.ts, e2e/benchmarks) and Lighthouse audits; no documented per-surface limits.
- **ARC-07 Service objectives defined and monitored**: **1** (grade A). No metrics endpoint or objectives; tracing fans out to Langfuse.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A). Provider calls have timeouts and errors are contained per conversation; MCP servers run as separate connections.
- **ARC-09 Backup, restore and recovery**: **0** (grade A). No backup command or documented backup in the repository.
  - Higher reading 1: MongoDB tooling is the implied path.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A). No request or feature-request object for changing the product was found; requests live outside it.

### Build

- **DEL-02 Layers deploy independently**: **2** (grade A). API and client ship together in one image; RAG API, search and a Langfuse fan-out service are separate containers with Helm charts (helm/).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A). Workspace packages with explicit dependencies and a circular-dependency check (config/circular-deps.mjs).
- **DEL-04 AI implementation lane**: **0** (grade A). No AI authoring lane for LibreChat's own definitions.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A). Backend, frontend, static checks, mocked Playwright journeys and Docker smoke tests run on pull requests (.github/workflows/backend-review.yml, frontend-review.yml, static-checks.yml, playwright-mock.yml); accessibility runs on demand and there is no security scan.
- **DEL-06 Verification surface**: **2** (grade A). /health (api/server/index.js:328) and a startup configuration endpoint for the client; no build or version endpoint.
  - Higher reading 3: The configuration endpoint is a machine-readable snapshot.
- **DEL-07 Environment reproducibility**: **2** (grade A). Docker Compose and Helm charts, staging image builds (.github/workflows/dev-staging-images.yml) and seeded E2E setup (e2e/setup); no per-change ephemeral environment.
- **DEL-08 Machine verifiability**: **2** (grade A). Mocked and property-based Playwright journeys (playwright-mock.yml, playwright-bombadil.yml); code-graph test selection runs in observe-only shadow mode (.github/workflows/codegraph-select.yml:1-13); no adoption instrumentation.
  - Higher reading 3: The changed-path map exists, though not yet enforced.

### Release

- **DEL-09 Staged exposure**: **1** (grade A). Interface features are switched globally in librechat.yaml.
- **DEL-10 Kill switch**: **1** (grade A). Disabling a feature needs a configuration change and restart.
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: No first-party evolution system ships code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-02 Field definitions carry type and validation**: **1** (grade A). No user-definable fields; schemas are code (packages/data-schemas/src/schema).
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **1** (grade A). No published contract for LibreChat's own API; a shared typed client (packages/data-provider) serves the bundled frontend only. Agents are reachable through an OpenAI-compatible API.
  - Higher reading 2: The OpenAI-compatible agents API is a machine-readable contract.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Interface settings from librechat.yaml can be overridden per user, group or role in the database (packages/data-schemas/src/types/config.ts:6-14); model specs and presets are data. No layout editor or preview.
  - Higher reading 3: Principal-scoped overrides are tenant-overridable presentation data.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A). Theme registry (packages/client/src/theme) and 86 locale files synced through Locize (.github/workflows/locize-i18n-sync.yml); custom welcome and footer text in configuration; no admin theme editor.
  - Higher reading 3: Per-principal configuration overrides include interface text.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A). Agents can be started by schedules and webhook triggers (api/server/services/Schedules, packages/api/src/agents/triggers); there is no general rules engine.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A). Inbound agent trigger deliveries record succeeded, retry and dead outcomes with stable identities (packages/data-schemas/src/types/triggerDelivery.ts:23-79); LibreChat does not publish its own entity events to subscribers.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A). Admins and users attach MCP servers and OpenAPI actions that run custom server-side logic when agents call them; stdio MCP servers run as unsandboxed local processes; outbound connections have SSRF tests (packages/api/src/mcp/__tests__/MCPConnectionSSRF.test.ts).

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A). MCP servers, OpenAPI actions, custom endpoints and skills extend agents; no plugin points for UI, layout or theme.
  - Higher reading 3: Declarative (OpenAPI actions, YAML endpoints) and code (MCP) extension both exist.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A). Remote MCP servers use OAuth and SSRF guards; code execution runs in an external sandbox service; stdio MCP servers run with full trust.
- **MAL-15 Developer loop**: **2** (grade A). Local development documentation and a bring-your-own-model E2E harness (e2e/byom).

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A). Custom endpoints map any OpenAI-compatible provider onto the canonical chat interface through YAML configuration alone (librechat.example.yaml:575).
- **MAL-17 Connector definition or SDK**: **3** (grade A). MCP is the connector standard, with OAuth flows, reconnect management and admin or user installation (api/server/services/initializeMCPs.js, initializeOAuthReconnectManager.js).
- **MAL-18 Stable versioned contracts**: **2** (grade A). The agents API follows the OpenAI Chat Completions and Responses contracts; LibreChat's own API is unversioned.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **1** (grade A). LibreChat consumes MCP but does not expose itself as an MCP server (api/server/routes/mcp.js manages client connections); agents are reachable through an OpenAI-compatible API. Scored at the lower reading under rule 11 because: If an OpenAI-compatible chat API is not an introspectable capability surface.
  - Higher reading 2: The September v0.3 pass scored 2 on the evidence above.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A). Members complete tasks conversationally with retrieval, web search, code and tool actions; there is no natural-language authoring of LibreChat's own definitions.
  - Higher reading 3: The member half of level 3 is fully met.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A). Token transactions are recorded per request and enforce balances live; OpenTelemetry and Langfuse tracing (otel/). Scored at the lower reading under rule 11 because: Usage accounting rather than behaviour telemetry.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-02 Structured learning signals**: **2** (grade A). Message feedback with rating, tag and text is stored on messages (packages/data-schemas/src/schema/message.ts:103); no triage workflow.
- **LRN-03 User-issue detection**: **2** (grade A). Users rate messages with thumbs and tags, stored on the message (packages/data-schemas/src/schema/message.ts:103).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A). No joined usage, support and delivery models.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **1** (grade A). Engineers read logs.
- **LRN-06 Ranked, evidence-backed proposals for change**: **0** (grade A). No recommendation or proposal features.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A), **3** with opt-in settings. By default nothing learns from use. With the memory block enabled (commented out in librechat.example.yaml:1351-1360), a memory agent stores user facts from recent chat automatically.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A). No checks on learned memories beyond configured key and token limits (librechat.example.yaml:1354-1358).

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **2** (grade A). An axe linter workflow runs when triggered manually (.github/workflows/a11y.yml:8-28), Lighthouse audits exist (.github/workflows/lighthouse.yml, e2e/lighthouse), and the ESLint configuration includes accessibility rules.
  - Higher reading 3: If Lighthouse or lint accessibility checks run on every pull request.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A). Admin audit route and audit-log schema (api/server/routes/admin/audit.js, packages/data-schemas/src/types/auditLog.ts); coverage of configuration and definition changes was not verified.
  - Higher reading 3: Admin UI and a generic store exist.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Users export conversations and delete their accounts, and an admin deletion script removes user data (config/delete-user.js); not driven by field tags.
- **GOV-04 Security as infrastructure**: **2** (grade A). ACL-based permissions for agents, prompts and MCP servers (packages/data-schemas/src/types/accessRole.ts, aclEntry.ts) and system grants; no security scanning in CI.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A), facets: implemented. Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Configuration is unversioned in the product.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Prompt groups stage versions and promote one to production; agents are edited and saved directly; no review step.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A). Every definition change is a direct human action; the approval lifecycle (packages/api/src/stream/ApprovalLifecycle.ts) gates agent tool calls, not changes.
- **GOV-08 Upgrade safety**: **2** (grade A). librechat.yaml carries a schema version checked at load, and UPGRADING.md documents migrations; compatibility is mostly manual.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A). Agent API keys with expiry (packages/data-schemas/src/types/agentApiKey.ts), on-behalf-of token exchange for MCP (api/server/services/OboTokenService.js), tool-call approvals before execution, rate limits, audit logs and idempotent trigger deliveries. Scored at the lower reading under rule 11 because: Idempotency covers trigger deliveries, not API mutations.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **GOV-10 Bounded self-change**: **not applicable**. No self-change path by default; the memory agent is opt-in. If counted: 1.
- **GOV-11 Learning-input integrity**: **not applicable**. No self-change path by default. If counted: 1.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **EXP-02 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **EXP-03 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 1.

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A). No adjacent-capability proposals.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **2** (grade A). Agents, prompts and MCP servers can be shared with selected users and groups through ACLs (packages/data-schemas/src/types/aclEntry.ts).
