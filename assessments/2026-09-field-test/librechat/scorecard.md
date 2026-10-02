# LibreChat: EVOLVE v0.5 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.5.0 in this repository.

Scope: the LibreChat monorepo (api, client, packages/api, data-provider, data-schemas, e2e, helm, CI). The hosted code interpreter service, RAG API image and third-party MCP servers are out of scope.

## Reading

**SAL 0.** Configuration is file-based and partly unversioned (Open 1.7), and there is no AI lane for LibreChat's own definitions (DEL-04 0), so no loop has a build path at L1. Users rate messages with tags (LRN-03 2), which is a useful start. **Next level:** governed, versioned configuration in the product, and backup (ARC-09 0).

## Limits

Repository evidence only, main at the tip named above. The hosted code interpreter, RAG API and third-party MCP servers are out of scope. Whether the accessibility and Lighthouse checks run on every pull request depends on path filters and inputs that were read, not exercised. Single rater.

---
Framework EVOLVE 0.5.0. Date 2026-09-30. Source github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main). Archetype **focused-application**.

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, definition_change_path, ai_features, ai_data_access, ai_actions. False: agent_mutations, evolution_auto_apply, code_release_path.

Coverage: 63 assessed, 0 not evidenced, 11 not applicable. Grades: 63 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 0 (Manual) · Request → Release L0 · Issue → Fix L0 · Opportunity → Expansion L0**

Progress toward the next level: Request → Release 1 of 2 conditions for L1; Issue → Fix 2 of 3 conditions for L1; Opportunity → Expansion 1 of 2 conditions for L1.

- With opt-in settings: SAL 0 (Manual) · Request → Release L0 · Issue → Fix L0 · Opportunity → Expansion L0.
- With every alternate reading: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L0.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L0 | L1 | L2 | **L0** | L0 |
| Issue → Fix | L1 | L0 | L1 | L2 | **L0** | L0 |
| Opportunity → Expansion | L1 | L0 | L1 | L2 | **L0** | L0 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 1 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 0 | fail |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | not applicable (agent_mutations and evolution_auto_apply false) | n/a | n/a |

### What blocks the next level

- **Request → Release to L1**: spine Build needs people build path ≥ 2 or product build path ≥ 2 (has MAL 1.7; DEL-04 0)
- **Issue → Fix to L1**: spine Build needs people build path ≥ 2 or product build path ≥ 2 (has MAL 1.7; DEL-04 0, LRN-07 1)
- **Opportunity → Expansion to L1**: spine Build needs people build path ≥ 2 or product build path ≥ 2 (has EXP-02 n/a; DEL-04 0, EXP-03 n/a)

### Sensitivity

- **Robust:** no single criterion falling one level lowers the headline.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.4 | 1.4–1.8 | 1.4 | 1.4 | 1.4 |
| Velocity (DEL) | 1.1 | 1.1–1.2 | 1.1 | 1.1 | 1.1 |
| Open (MAL) | 1.7 | 1.7–2.2 | 1.7 | 1.7 | 1.7 |
| Learn (LRN) | 0.8 | 0.8–0.9 | 1.1 | 0.8 | 0.8 |
| Vet (GOV) | 1.9 | 1.9–2.4 | 1.9 | 1.9 | 1.7 |
| Expand (EXP) | 1.0 | 1.0 | 1.0 | 1.0 | 1.2 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L0 (Foundational gap) · Context 2 · Quality 0 · Governance 2 · Operations 2 · not production-governed**

- With opt-in settings: AI Readiness L0 (Foundational gap) · Context 2 · Quality 0 · Governance 2 · Operations 2 · not production-governed.
- With every alternate reading: AI Readiness L0 (Foundational gap) · Context 2 · Quality 0 · Governance 2 · Operations 2 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 2 | AIR-03 2, AIR-04 2 |
| Quality | 0 | AIR-05 0, AIR-06 1 |
| Governance | 2 | AIR-07 2, GOV-09 (AI) 2 |
| Operations | 2 | AIR-01 2, AIR-02 2, AIR-08 2, ARC-08 (AI) 2 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 2 | fail |
| Regression evaluation before release | AIR-06 ≥ 3 | 1 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 2 | fail |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 1 | MAL-19 1, MAL-20 2 |
| Build | 0 | DEL-01 0, DEL-04 0 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 n/a |
| Expand | 0 | EXP-05 0 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 1.5 |
| ARC Scale | 1.7 |
| ARC Capacity | 1.5 |
| ARC Resilience | 1.0 |
| DEL Intake | 0.0 |
| DEL Build | 1.3 |
| DEL Verify | 2.0 |
| DEL Release | 1.0 |
| MAL Data model | 1.0 |
| MAL APIs | 1.0 |
| MAL Interface | 2.0 |
| MAL Behaviour | 2.0 |
| MAL Extensions | 2.0 |
| MAL Integrations | 2.7 |
| MAL Agent interface | 1.5 |
| LRN Sense | 1.8 |
| LRN Diagnose and propose | 0.5 |
| LRN Learn from experience | 1.0 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 2.0 |
| GOV Change control | 1.8 |
| GOV AI and self-change safety | 2.0 |
| EXP Discover | 0.0 |
| EXP Launch | 2.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A |  | MeiliSearch index for conversations and messages (search/) and MongoDB indexes; no definition-driven mapping. |
| ARC-02 Safe schema and data migrations | assessed | 1 | 2 |  | A |  | One-off migration scripts with dry-run modes (config/migrate-*.js, package.json:134-139); no down steps. |
| ARC-03 Horizontal scale of services | assessed | 2 |  |  | A |  | With USE_REDIS, caches and request limits move to Redis for several instances (api/cache/clearPendingReq.js:5-39); Helm charts deploy it (helm/). |
| ARC-04 Reliable asynchronous work | assessed | 1 |  |  | A |  | No job queue; background work runs in the API process. |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | IT | Tenant isolation plugin with a coverage specification (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts), per-user token balances and rate limits; no noisy-neighbour detection. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A |  | Performance scan and benchmark suites (e2e/perf/scan.ts, e2e/benchmarks) and Lighthouse audits; no documented per-surface limits. |
| ARC-07 Service objectives defined and monitored | assessed | 1 |  |  | A |  | No metrics endpoint or objectives; tracing fans out to Langfuse. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Provider calls have timeouts and errors are contained per conversation; MCP servers run as separate connections. |
| ARC-09 Backup, restore and recovery | assessed | 0 | 1 |  | A |  | No backup command or documented backup in the repository. |
| DEL-01 Request intake into a structured change specification | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No request or feature-request object for changing the product was found; requests live outside it. |
| DEL-02 Layers deploy independently | assessed | 2 |  |  | A |  | API and client ship together in one image; RAG API, search and a Langfuse fan-out service are separate containers with Helm charts (helm/). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 |  |  | A |  | Workspace packages with explicit dependencies and a circular-dependency check (config/circular-deps.mjs). |
| DEL-04 AI implementation lane | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No AI authoring lane for LibreChat's own definitions. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A |  | Backend, frontend, static checks, mocked Playwright journeys and Docker smoke tests run on pull requests (.github/workflows/backend-review.yml, frontend-review.yml, static-checks.yml, playwright-mock.yml); accessibility runs on demand and there is no security scan. |
| DEL-06 Verification surface | assessed | 2 | 3 |  | A |  | /health (api/server/index.js:328) and a startup configuration endpoint for the client; no build or version endpoint. |
| DEL-07 Environment reproducibility | assessed | 2 |  |  | A |  | Docker Compose and Helm charts, staging image builds (.github/workflows/dev-staging-images.yml) and seeded E2E setup (e2e/setup); no per-change ephemeral environment. |
| DEL-08 Machine verifiability | assessed | 2 | 3 |  | A |  | Mocked and property-based Playwright journeys (playwright-mock.yml, playwright-bombadil.yml); code-graph test selection runs in observe-only shadow mode (.github/workflows/codegraph-select.yml:1-13); no adoption instrumentation. |
| DEL-09 Staged exposure | assessed | 1 |  |  | A |  | Interface features are switched globally in librechat.yaml. |
| DEL-10 Kill switch | assessed | 1 |  |  | A |  | Disabling a feature needs a configuration change and restart. |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: No first-party evolution system ships code changes. |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-02 Field definitions carry type and validation | assessed | 1 |  |  | A |  | No user-definable fields; schemas are code (packages/data-schemas/src/schema). |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 1 | 2 |  | A |  | No published contract for LibreChat's own API; a shared typed client (packages/data-provider) serves the bundled frontend only. Agents are reachable through an OpenAI-compatible API. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A |  | Interface settings from librechat.yaml can be overridden per user, group or role in the database (packages/data-schemas/src/types/config.ts:6-14); model specs and presets are data. No layout editor or preview. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Focused application: generic widgets from entity definitions (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 | 3 |  | A |  | Theme registry (packages/client/src/theme) and 86 locale files synced through Locize (.github/workflows/locize-i18n-sync.yml); custom welcome and footer text in configuration; no admin theme editor. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A |  | Agents can be started by schedules and webhook triggers (api/server/services/Schedules, packages/api/src/agents/triggers); there is no general rules engine. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A |  | Inbound agent trigger deliveries record succeeded, retry and dead outcomes with stable identities (packages/data-schemas/src/types/triggerDelivery.ts:23-79); LibreChat does not publish its own entity events to subscribers. |
| MAL-12 Sandboxed server-side hooks | assessed | 2 |  |  | A |  | Admins and users attach MCP servers and OpenAPI actions that run custom server-side logic when agents call them; stdio MCP servers run as unsandboxed local processes; outbound connections have SSRF tests (packages/api/src/mcp/__tests__/MCPConnectionSSRF.test.ts). |
| MAL-13 Plugin lane breadth | assessed | 2 | 3 |  | A |  | MCP servers, OpenAPI actions, custom endpoints and skills extend agents; no plugin points for UI, layout or theme. |
| MAL-14 Runtime isolation and dependency control | assessed | 2 |  |  | A |  | Remote MCP servers use OAuth and SSRF guards; code execution runs in an external sandbox service; stdio MCP servers run with full trust. |
| MAL-15 Developer loop | assessed | 2 |  |  | A |  | Local development documentation and a bring-your-own-model E2E harness (e2e/byom). |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A |  | Custom endpoints map any OpenAI-compatible provider onto the canonical chat interface through YAML configuration alone (librechat.example.yaml:575). |
| MAL-17 Connector definition or SDK | assessed | 3 |  |  | A |  | MCP is the connector standard, with OAuth flows, reconnect management and admin or user installation (api/server/services/initializeMCPs.js, initializeOAuthReconnectManager.js). |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A |  | The agents API follows the OpenAI Chat Completions and Responses contracts; LibreChat's own API is unversioned. |
| MAL-19 Machine-readable capability surface for agents | assessed | 1 | 2 |  | A |  | AI-qualified reading: 1. LibreChat consumes MCP but does not expose itself as an MCP server (api/server/routes/mcp.js manages client connections); agents are reachable through an OpenAI-compatible API. Scored at the lower reading under rule 11 because: If an OpenAI-compatible chat API is not an introspectable capability surface. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. Members complete tasks conversationally with retrieval, web search, code and tool actions; there is no natural-language authoring of LibreChat's own definitions. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A |  | Token transactions are recorded per request and enforce balances live; OpenTelemetry and Langfuse tracing (otel/). Scored at the lower reading under rule 11 because: Usage accounting rather than behaviour telemetry. |
| LRN-02 Structured learning signals | assessed | 2 |  |  | A |  | Message feedback with rating, tag and text is stored on messages (packages/data-schemas/src/schema/message.ts:103); no triage workflow. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A |  | Users rate messages with thumbs and tags, stored on the message (packages/data-schemas/src/schema/message.ts:103). |
| LRN-04 Cross-source mining inside the product | assessed | 1 |  |  | A |  | No joined usage, support and delivery models. |
| LRN-05 Automated diagnosis | assessed | 1 |  |  | A |  | AI-qualified reading: 0. Engineers read logs. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No recommendation or proposal features. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 1 |  | 3 | A |  | AI-qualified reading: 0. By default nothing learns from use. With the memory block enabled (commented out in librechat.example.yaml:1351-1360), a memory agent stores user facts from recent chat automatically. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 |  |  | A |  | AI-qualified reading: not applicable. No checks on learned memories beyond configured key and token limits (librechat.example.yaml:1354-1358). |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A |  | No binding of changes to baselines or metrics. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 2 | 3 |  | A |  | An axe linter workflow runs when triggered manually (.github/workflows/a11y.yml:8-28), Lighthouse audits exist (.github/workflows/lighthouse.yml, e2e/lighthouse), and the ESLint configuration includes accessibility rules. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A |  | Admin audit route and audit-log schema (api/server/routes/admin/audit.js, packages/data-schemas/src/types/auditLog.ts); coverage of configuration and definition changes was not verified. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A |  | Users export conversations and delete their accounts, and an admin deletion script removes user data (config/delete-user.js); not driven by field tags. |
| GOV-04 Security as infrastructure | assessed | 2 |  |  | A |  | ACL-based permissions for agents, prompts and MCP servers (packages/data-schemas/src/types/accessRole.ts, aclEntry.ts) and system grants; no security scanning in CI. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A | I | Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Configuration is unversioned in the product. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 |  |  | A |  | Prompt groups stage versions and promote one to production; agents are edited and saved directly; no review step. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 |  |  | A |  | Every definition change is a direct human action; the approval lifecycle (packages/api/src/stream/ApprovalLifecycle.ts) gates agent tool calls, not changes. |
| GOV-08 Upgrade safety | assessed | 2 |  |  | A |  | librechat.yaml carries a schema version checked at load, and UPGRADING.md documents migrations; compatibility is mostly manual. |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. Agent API keys with expiry (packages/data-schemas/src/types/agentApiKey.ts), on-behalf-of token exchange for MCP (api/server/services/OboTokenService.js), tool-call approvals before execution, rate limits, audit logs and idempotent trigger deliveries. Scored at the lower reading under rule 11 because: Idempotency covers trigger deliveries, not API mutations. |
| GOV-10 Bounded self-change | not_applicable | excluded |  |  | - |  | AI-qualified reading: not applicable. No self-change path by default; the memory agent is opt-in. |
| GOV-11 Learning-input integrity | not_applicable | excluded |  |  | - |  | AI-qualified reading: not applicable. No self-change path by default. |
| EXP-01 Kernel concepts are domain-neutral | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| EXP-02 A new domain is expressible without kernel change | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| EXP-03 A domain ships as an installable bundle | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A |  | No record of unmet intents was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 2 |  |  | A |  | Agents, prompts and MCP servers can be shared with selected users and groups through ACLs (packages/data-schemas/src/types/aclEntry.ts). |
| AIR-03 AI-ready data and context access | assessed | 2 |  |  | A |  | File search over uploaded files through the RAG API (api/app/clients/tools/util/fileSearch.js); other product data is not indexed. |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 2 | 3 |  | A | IT | Retrieval covers files attached to the conversation or agent; agents shared through ACLs carry their builder's files to other users. |
| AIR-05 Offline AI evaluation | assessed | 0 |  |  | A |  | No evaluation harness. |
| AIR-06 Regression gating before release | assessed | 1 |  |  | A |  | Configuration changes are tested manually in chat. |
| AIR-07 AI action tracing and auditability | assessed | 2 |  |  | A |  | Messages store model, tokens and tool calls; Langfuse fan-out tracing is optional (packages/api/src/langfuse, traces/handlers.ts). |
| AIR-01 Model and provider portability and resilience | assessed | 2 |  |  | A |  | Admins configure many providers and model specs (librechat.yaml, packages/api/src/endpoints); no declared resilience strategy. |
| AIR-02 AI usage and per-customer cost controls | assessed | 2 |  | 3 | A |  | Token transactions recorded per user; balances that limit spending are opt-in (librechat.example.yaml:363-378). |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 2 |  |  | A |  | Users rate messages with tags, and admin insights summarise usage (packages/data-schemas/src/schema/message.ts:103, packages/api/src/insights); no drift alerts. |

Facets: I implemented, T tested, O operated.
