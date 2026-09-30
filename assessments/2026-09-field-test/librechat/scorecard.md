# LibreChat: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the LibreChat monorepo (api, client, packages/api, data-provider, data-schemas, e2e, helm, CI). The hosted code interpreter service, RAG API image and third-party MCP servers are out of scope.

## Reading

**Strongest:** agent-safe actions (K3 3) and connector layers (N1 3, N2 3). **Largest gap:** Learning (1.0): no proposals, no AI authoring of its own configuration, no impact measurement. Enabling the opt-in memory agent raises P1 to 3 and Learning to 1.3.

## Limits

Repository evidence only, main at the tip named above. The hosted code interpreter, RAG API and third-party MCP servers are out of scope. Whether the accessibility and Lighthouse checks run on every pull request depends on path filters and inputs that were read, not exercised. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main). Archetype **focused-application**.

Coverage: 41 assessed, 0 not evidenced, 8 not applicable. Grades: 41 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 1.8 | mechanism | 1.8–2.2 | 1.8 | 1.8 | 1.7 |
| governance | 1.9 | mechanism | 1.9–2.3 | 1.9 | 1.9 | 1.9 |
| learning | 1.0 | code-only | 0.9–1.0 | 1.3 | 1.0 | 1.0 |
| factory | 2.0 | mechanism | 2.0–2.3 | 2.0 | 2.0 | 2.0 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 1.5 | 1.5 |
| Governance | 1.9 | 1.9 |
| Learning | 1.0 | 1.3 |
| Factory | 2.0 | 2.0 |
| Agent Interface | 2.3 | 2.3 |
| Extension Surface | 2.3 | 2.3 |
| Operational Scalability | 2.0 | 2.0 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 2 pass | 2 pass |
| propose | M1, P1 | 2 | 1 fail | 3 pass |
| review | F2 | 2 | 2 pass | 2 pass |
| gate | F3 | 3 | 1 fail | 1 fail |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 1 fail | 1 fail |
| verify | L1 | 2 | 2 pass | 2 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| A Entity and schema as data | 1.0 |
| B API surface generation | 1.0 |
| C Rendering follows the definition | 2.0 |
| D Behaviour as data | 2.0 |
| E Compliance and security as infrastructure | 2.0 |
| F Change control | 1.8 |
| G Performance under genericity | 2.0 |
| H Stack flexibility and verification | 2.0 |
| I Extension ecosystem | 2.0 |
| J Observe | 2.0 |
| K Agent and conversational readiness | 2.3 |
| L Factory surfaces | 2.0 |
| M Advise and act | 0.0 |
| N Integration and connector extensibility | 2.7 |
| P Learn from experience | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| A2 Field definitions carry type and validation | assessed | 1 |  |  | A | No user-definable fields; schemas are code (packages/data-schemas/src/schema). |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 1 | 2 |  | A | No published contract for LibreChat's own API; a shared typed client (packages/data-provider) serves the bundled frontend only. Agents are reachable through an OpenAI-compatible API. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A | Interface settings from librechat.yaml can be overridden per user, group or role in the database (packages/data-schemas/src/types/config.ts:6-14); model specs and presets are data. No layout editor or preview. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Focused application: generic widgets from entity definitions (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 | 3 |  | A | Theme registry (packages/client/src/theme) and 86 locale files synced through Locize (.github/workflows/locize-i18n-sync.yml); custom welcome and footer text in configuration; no admin theme editor. |
| D1 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A | Agents can be started by schedules and webhook triggers (api/server/services/Schedules, packages/api/src/agents/triggers); there is no general rules engine. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A | Inbound agent trigger deliveries record succeeded, retry and dead outcomes with stable identities (packages/data-schemas/src/types/triggerDelivery.ts:23-79); LibreChat does not publish its own entity events to subscribers. |
| D3 Sandboxed server-side hooks | assessed | 2 |  |  | A | Admins and users attach MCP servers and OpenAPI actions that run custom server-side logic when agents call them; stdio MCP servers run as unsandboxed local processes; outbound connections have SSRF tests (packages/api/src/mcp/__tests__/MCPConnectionSSRF.test.ts). |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 2 | 3 |  | A | An axe linter workflow runs when triggered manually (.github/workflows/a11y.yml:8-28), Lighthouse audits exist (.github/workflows/lighthouse.yml, e2e/lighthouse), and the ESLint configuration includes accessibility rules. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A | Admin audit route and audit-log schema (api/server/routes/admin/audit.js, packages/data-schemas/src/types/auditLog.ts); coverage of configuration and definition changes was not verified. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A | Users export conversations and delete their accounts, and an admin deletion script removes user data (config/delete-user.js); not driven by field tags. |
| E4 Security as infrastructure | assessed | 2 |  |  | A | ACL-based permissions for agents, prompts and MCP servers (packages/data-schemas/src/types/accessRole.ts, aclEntry.ts) and system grants; no security scanning in CI. |
| F1 Definitions and layouts versioned with rollback | assessed | 2 | 3 |  | A | Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 2 |  |  | A | Prompt groups stage versions and promote one to production; agents are edited and saved directly; no review step. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 |  |  | A | Every definition change is a direct human action; the approval lifecycle (packages/api/src/stream/ApprovalLifecycle.ts) gates agent tool calls, not changes. |
| F4 Upgrade safety | assessed | 2 |  |  | A | librechat.yaml carries a schema version checked at load, and UPGRADING.md documents migrations; compatibility is mostly manual. |
| G1 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A | MeiliSearch index for conversations and messages (search/) and MongoDB indexes; no definition-driven mapping. |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | Tenant isolation plugin with a coverage specification (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts), per-user token balances and rate limits; no noisy-neighbour detection. |
| G3 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A | Performance scan and benchmark suites (e2e/perf/scan.ts, e2e/benchmarks) and Lighthouse audits; no documented per-surface limits. |
| H1 Layers deploy independently | assessed | 2 |  |  | A | API and client ship together in one image; RAG API, search and a Langfuse fan-out service are separate containers with Helm charts (helm/). |
| H2 Module boundaries enforced by tooling | assessed | 2 |  |  | A | Workspace packages with explicit dependencies and a circular-dependency check (config/circular-deps.mjs). |
| H3 Every change class has an automated pre-land check | assessed | 2 |  |  | A | Backend, frontend, static checks, mocked Playwright journeys and Docker smoke tests run on pull requests (.github/workflows/backend-review.yml, frontend-review.yml, static-checks.yml, playwright-mock.yml); accessibility runs on demand and there is no security scan. |
| I1 Plugin lane breadth | assessed | 2 | 3 |  | A | MCP servers, OpenAPI actions, custom endpoints and skills extend agents; no plugin points for UI, layout or theme. |
| I2 Runtime isolation and dependency control | assessed | 2 |  |  | A | Remote MCP servers use OAuth and SSRF guards; code execution runs in an external sandbox service; stdio MCP servers run with full trust. |
| I3 Developer loop | assessed | 2 |  |  | A | Local development documentation and a bring-your-own-model E2E harness (e2e/byom). |
| K1 Machine-readable capability surface for agents | assessed | 2 | 1 |  | A | LibreChat consumes MCP but does not expose itself as an MCP server (api/server/routes/mcp.js manages client connections); agents are reachable through an OpenAI-compatible API. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A | Members complete tasks conversationally with retrieval, web search, code and tool actions; there is no natural-language authoring of LibreChat's own definitions. |
| K3 Agent-safe actions | assessed | 3 | 2 |  | A | Agent API keys with expiry (packages/data-schemas/src/types/agentApiKey.ts), on-behalf-of token exchange for MCP (api/server/services/OboTokenService.js), tool-call approvals before execution, rate limits, audit logs and idempotent trigger deliveries. |
| N1 Canonical data model with a mapping layer | assessed | 3 |  |  | A | Custom endpoints map any OpenAI-compatible provider onto the canonical chat interface through YAML configuration alone (librechat.example.yaml:575). |
| N2 Connector definition or SDK | assessed | 3 |  |  | A | MCP is the connector standard, with OAuth flows, reconnect management and admin or user installation (api/server/services/initializeMCPs.js, initializeOAuthReconnectManager.js). |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | The agents API follows the OpenAI Chat Completions and Responses contracts; LibreChat's own API is unversioned. |
| O1 Kernel concepts are domain-neutral | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| O2 A new domain is expressible without kernel change | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| O3 A domain ships as an installable bundle | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 | 2 |  | A | Token transactions are recorded per request and enforce balances live; OpenTelemetry and Langfuse tracing (otel/). |
| J2 Structured learning signals | assessed | 2 |  |  | A | Message feedback with rating, tag and text is stored on messages (packages/data-schemas/src/schema/message.ts:103); no triage workflow. |
| J3 Cross-source mining inside the product | assessed | 1 |  |  | A | No joined usage, support and delivery models. |
| M1 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A | No recommendation or proposal features. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 0 |  |  | A | No AI authoring lane for LibreChat's own definitions. |
| M4 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A | No binding of changes to baselines or metrics. |
| P1 The product turns its own operating experience into candidate changes | assessed | 1 |  | 3 | A | By default nothing learns from use. With the memory block enabled (commented out in librechat.example.yaml:1351-1360), a memory agent stores user facts from recent chat automatically. |
| P2 Learned changes are validated before they take effect | assessed | 1 |  |  | A | No checks on learned memories beyond configured key and token limits (librechat.example.yaml:1354-1358). |
| L1 Verification surface | assessed | 2 | 3 |  | A | /health (api/server/index.js:328) and a startup configuration endpoint for the client; no build or version endpoint. |
| L2 Environment reproducibility | assessed | 2 |  |  | A | Docker Compose and Helm charts, staging image builds (.github/workflows/dev-staging-images.yml) and seeded E2E setup (e2e/setup); no per-change ephemeral environment. |
| L3 Machine verifiability | assessed | 2 | 3 |  | A | Mocked and property-based Playwright journeys (playwright-mock.yml, playwright-bombadil.yml); code-graph test selection runs in observe-only shadow mode (.github/workflows/codegraph-select.yml:1-13); no adoption instrumentation. |

