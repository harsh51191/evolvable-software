# LibreChat evidence

Read at github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Conversations, agents, prompts and users in MongoDB.
- **schema_changes**: true. Data migration scripts change stored documents and indexes (config/migrate-*.js).
- **multi_tenant**: false. Re-read at the v0.7 migration under the tightened definition. A default installation is one group of users under one administrator; groups (packages/data-schemas/src/methods/userGroup.ts) share agents and prompts but do not administer themselves. Tenant isolation ships (packages/data-schemas/src/models/plugins/tenantIsolation.ts) but users carry no tenant by default and the plugin passes unscoped queries through unless TENANT_ISOLATION_STRICT is set (tenantIsolation.ts:96-104; .env.example:165-167, 758-761); tenancy needs tenant identities supplied by a deployment's identity provider or proxy. The v0.6 reading (true) counted the plugin's presence.
- **hosted_service**: true. Node API serving many users, with optional Redis (api/cache).
- **machine_actions**: true. The API changes agents, prompts and conversations for authenticated clients, and MCP tools act on users' behalf.
- **agent_mutations**: true. Re-read at the v0.7 migration under the tightened definition. Agents write skills: with the skills capability on by default (packages/data-provider/src/config.ts:830-841) and users allowed to create skills by default (packages/data-provider/src/roles.ts:208-213, 269-274), an agent with skills enabled creates SKILL.md files and edits skill files the user can edit (api/server/services/Endpoints/agents/skillDeps.js:113-147; packages/api/src/agents/handlers.ts:3845-3905, 4591-4594). The opt-in memory agent also writes user memories (librechat.example.yaml:1351-1360). The v0.6 reading (false) looked only at memory.
- **evolution_auto_apply**: true. Re-read at the v0.7 migration under the tightened definition. A skill an agent writes is saved to the live skill at once (packages/api/src/skills/save.ts:36-41); tool-call approval is off by default (librechat.example.yaml:767-768), so no person reviews the change before it takes effect.
- **definition_change_path**: true. librechat.yaml, agents and prompts are definitions.
- **code_release_path**: false. No first-party evolution system ships code changes.
- **ai_features**: true. Chat with many model providers and agents (packages/api/src/endpoints, agents).
- **ai_data_access**: true. File search over uploaded files (api/app/clients/tools/util/fileSearch.js).
- **ai_actions**: true. Agents call tools and MCP servers that act on external systems (packages/api/src/mcp).

## Kinds of change

- **Which AI models and providers are offered, and app-wide settings** (`models-config`, main, made by administrators): reach **1 Self-serve**, confidence medium. Base settings live in librechat.yaml and .env, edited on the server and read at start. Live overrides per role, group or user are set through the admin configuration API (api/server/routes/admin/config.js:38-46), validated and merged per request (packages/api/src/app/service.ts:396-518), and undone by deleting the override, which restores the base setting. The API's client is the first-party admin panel image (deploy-compose.yml), so under the v0.7 self-serve rule this kind is self-serve with undo.
- **Agents: their instructions, tools and files** (`agents`, main, made by users and administrators): reach **1 Self-serve**, confidence high. Built in the agent builder with no deploy; each save keeps a version (packages/data-schemas/src/schema/agent.ts:125) and an agent can be reverted to an earlier version (api/server/routes/agents/v1.js:154-168). No AI drafts agent changes (DEL-04 is 0).
- **Tools and connected services (MCP servers)** (`tools-mcp`, main, made by administrators and users): reach **0 Engineers only**, confidence medium. Servers in librechat.yaml need a server edit and restart; servers added in the UI (api/server/routes/mcp.js:1261-1287) can be removed but keep no history of earlier settings or credentials, so a change cannot be undone through the product. A path without undo is reach 0.
- **Saved prompts** (`prompts`, not main, made by users): reach **1 Self-serve**, confidence medium. Prompt groups keep versions and a chosen production version that can be switched back (packages/data-schemas/src/schema/promptGroup.ts:25).
- **Who may use agents, prompts, skills and memories** (`feature-access`, not main, made by administrators): reach **1 Self-serve**, confidence medium. Role permissions are toggled in the admin settings dialogs (client/src/components/ui/AdminSettingsDialog.tsx; api/server/routes/roles.js:160-172) with no deploy, and toggled back to undo.
- **Skills that agents use** (`skills`, not main, made by users): reach **0 Engineers only**, confidence medium. Written in the skill editor or by an agent (packages/api/src/agents/handlers.ts:3845-3905) and saved over the current file (packages/api/src/skills/save.ts:36-47); the skill keeps a version counter but no earlier content (packages/data-schemas/src/schema/skill.ts:176-180), so an edit cannot be undone. Agent writes apply directly rather than as drafts, and DEL-04 is 0, so this is not reach 2.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md and CONTEXT.md (agent instructions), Claude Code skills (.claude/skills: codebase-design, improve-codebase-architecture), a .codex directory, and CI comments that record fixes made from Codex review findings (.github/workflows/backend-review.yml:37, 176-214).
- **Proven, Request → Release**: not evidenced. Searched: The repository at the pinned commit: agent and prompt version fields, audit-log schema (packages/data-schemas/src/types/auditLog.ts), UPGRADING.md and release workflows for LibreChat's own engineer-made releases. No operating records of real changes made through the product's request loop in a deployment.
- **Proven, Issue → Fix**: not evidenced. Searched: The same sources plus message feedback (packages/data-schemas/src/schema/message.ts:103) and admin insights (packages/api/src/insights); no operating records of issues fixed through the product's loop.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: The same sources; no records of capabilities launched to a group and kept or killed.

Confidence for criteria whose reading did not change at the v0.7 migration was assigned at migration from the recorded evidence (high where it names the code path and its tests, medium where it names code but not every path, low where the reading is inferred or rests on documentation or absence); criteria re-read at migration were assigned from that re-reading.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **2** (grade A, confidence medium). MeiliSearch index for conversations and messages (search/) and MongoDB indexes; no definition-driven mapping.
- **ARC-02 Safe schema and data migrations**: **1** (grade A, confidence medium). One-off migration scripts with dry-run modes (config/migrate-*.js, package.json:134-139); no down steps.
  - Higher reading 2: Dry runs reduce migration risk.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A, confidence medium). With USE_REDIS, caches and request limits move to Redis for several instances (api/cache/clearPendingReq.js:5-39); Helm charts deploy it (helm/).
- **ARC-04 Reliable asynchronous work**: **3** (grade A, confidence medium), facets: implemented, tested. Mongo-backed trigger delivery queue with leases, retry history, backoff and dead letters across replicas (packages/data-schemas/src/schema/triggerDelivery.ts:11-20,134-144,183,210-228; packages/api/src/agents/triggers/README.md:46-50; triggers/backoff.ts); stable deliveryId idempotency (README:10-12); schedule occurrences claimed once with deterministic delivery keys and concurrency slots (packages/data-schemas/src/schema/scheduleRun.ts:36,138,162-169); tests delivery.integration.spec.ts, backoff.spec.ts, schedules/engine.spec.ts. No per-tenant fairness or back-pressure policy (level 4). [v0.7 correction from the blind second rating, verified at 14f7b28.]
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **not applicable**. Scope fact multi_tenant is false: a default installation is one group under one administrator; tenant isolation is opt-in through deployment-supplied tenant identities. If counted: 2.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **2** (grade A, confidence medium). Performance scan and benchmark suites (e2e/perf/scan.ts, e2e/benchmarks) and Lighthouse audits; no documented per-surface limits.
- **ARC-07 Service objectives defined and monitored**: **1** (grade A, confidence medium). No metrics endpoint or objectives; tracing fans out to Langfuse.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence medium). Provider calls have timeouts and errors are contained per conversation; MCP servers run as separate connections.
  - AI-qualified reading: **2** (grade A, confidence medium). Timeouts on provider calls (packages/api/src/endpoints/openai/config.ts); errors contained per conversation.
- **ARC-09 Backup, restore and recovery**: **1** (grade A, confidence high). No backup or restore command in repo (searched for backup, mongodump across *.md, *.yml, *.js, *.ts, *.sh). UPGRADING.md:40 tells operators to back up MongoDB themselves. Scheduled runs do re-validate owner, policy and credentials before each run (CONTEXT.md:3, packages/api/src/schedules/README.md:1-40, readiness.ts), which would help a restored schedule surface, but nothing restores it. [v0.7 correction from the blind second rating, verified at 14f7b28.]

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A, confidence medium). No request or feature-request object for changing the product was found; requests live outside it.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Build

- **DEL-02 Layers deploy independently**: **2** (grade A, confidence medium). API and client ship together in one image; RAG API, search and a Langfuse fan-out service are separate containers with Helm charts (helm/).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A, confidence medium). Workspace packages with explicit dependencies and a circular-dependency check (config/circular-deps.mjs).
- **DEL-04 AI implementation lane**: **2** (grade A, confidence medium). The product's agent authors skills (definitions) on a user's request: writeSkillMd validates frontmatter and name, applies content filters, checks create/edit permission, uses expectedVersion concurrency (packages/api/src/agents/handlers.ts:3805-3960; validation packages/data-schemas/src/methods/skill.ts:116-526). Narrow (skills only), on request, applied directly rather than proposed with evidence; a person edits further. [v0.7 correction from the blind second rating, verified at 14f7b28.]
  - AI-qualified reading: **2** (grade A, confidence medium). Same lane; inherently AI: model writes skills on request, narrow scope, no proposal or verification evidence (handlers.ts:3805-3960).

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence medium). Backend, frontend, static checks, mocked Playwright journeys and Docker smoke tests run on pull requests (.github/workflows/backend-review.yml, frontend-review.yml, static-checks.yml, playwright-mock.yml); accessibility runs on demand and there is no security scan.
- **DEL-06 Verification surface**: **2** (grade A, confidence medium). /health (api/server/index.js:328) and a startup configuration endpoint for the client; no build or version endpoint.
  - Higher reading 3: The configuration endpoint is a machine-readable snapshot.
- **DEL-07 Environment reproducibility**: **2** (grade A, confidence medium). Docker Compose and Helm charts, staging image builds (.github/workflows/dev-staging-images.yml) and seeded E2E setup (e2e/setup); no per-change ephemeral environment.
- **DEL-08 Machine verifiability**: **2** (grade A, confidence medium). Mocked and property-based Playwright journeys (playwright-mock.yml, playwright-bombadil.yml); code-graph test selection runs in observe-only shadow mode (.github/workflows/codegraph-select.yml:1-13); no adoption instrumentation.
  - Higher reading 3: The changed-path map exists, though not yet enforced.

### Release

- **DEL-09 Staged exposure**: **1** (grade A, confidence medium). Interface features are switched globally in librechat.yaml.
- **DEL-10 Kill switch**: **1** (grade A, confidence low). Disabling a feature needs a configuration change and restart.
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: No first-party evolution system ships code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-02 Field definitions carry type and validation**: **1** (grade A, confidence medium). No user-definable fields; schemas are code (packages/data-schemas/src/schema).
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A, confidence high). A generated OpenAPI 3.1 contract covers the agents and skills management API (packages/api/src/openapi/: agents.ts, skills.ts, document.ts, generate.ts; committed as packages/api/openapi/agents.openapi.json, 8 paths) and CI fails when the committed contract drifts from the code (.github/workflows/backend-review.yml:311-315, generate.ts --check); docs are served when openapi.enabled is set (packages/api/src/openapi/router.ts:56-71). The rest of LibreChat's API has no published contract; a shared typed client (packages/data-provider) serves the bundled frontend only. Corrected from 1 to 2 at the v0.7 migration.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Interface settings from librechat.yaml can be overridden per user, group or role in the database (packages/data-schemas/src/types/config.ts:6-14); model specs and presets are data. No layout editor or preview.
  - Higher reading 3: Principal-scoped overrides are tenant-overridable presentation data.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A, confidence medium). Theme registry (packages/client/src/theme) and 86 locale files synced through Locize (.github/workflows/locize-i18n-sync.yml); custom welcome and footer text in configuration; no admin theme editor.
  - Higher reading 3: Per-principal configuration overrides include interface text.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A, confidence medium). Agents can be started by schedules and webhook triggers (api/server/services/Schedules, packages/api/src/agents/triggers); there is no general rules engine.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A, confidence medium). Inbound agent trigger deliveries record succeeded, retry and dead outcomes with stable identities (packages/data-schemas/src/types/triggerDelivery.ts:23-79); LibreChat does not publish its own entity events to subscribers.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence high). Admins and users attach MCP servers and OpenAPI actions that run custom server-side logic when agents call them; stdio MCP servers run as unsandboxed local processes; outbound connections have SSRF tests (packages/api/src/mcp/__tests__/MCPConnectionSSRF.test.ts).

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A, confidence low). MCP servers, OpenAPI actions, custom endpoints and skills extend agents; no plugin points for UI, layout or theme.
  - Higher reading 3: Declarative (OpenAPI actions, YAML endpoints) and code (MCP) extension both exist.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A, confidence low). Remote MCP servers use OAuth and SSRF guards; code execution runs in an external sandbox service; stdio MCP servers run with full trust.
- **MAL-15 Developer loop**: **2** (grade A, confidence medium). Local development documentation and a bring-your-own-model E2E harness (e2e/byom).

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A, confidence medium). Custom endpoints map any OpenAI-compatible provider onto the canonical chat interface through YAML configuration alone (librechat.example.yaml:575).
- **MAL-17 Connector definition or SDK**: **3** (grade A, confidence medium). MCP is the connector standard, with OAuth flows, reconnect management and admin or user installation (api/server/services/initializeMCPs.js, initializeOAuthReconnectManager.js).
- **MAL-18 Stable versioned contracts**: **2** (grade A, confidence low). The agents API follows the OpenAI Chat Completions and Responses contracts; LibreChat's own API is unversioned.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **1** (grade A, confidence medium). LibreChat consumes MCP but does not expose itself as an MCP server (api/server/routes/mcp.js manages client connections); agents are reachable through an OpenAI-compatible API. Scored at the lower reading under rule 11 because: If an OpenAI-compatible chat API is not an introspectable capability surface.
  - Higher reading 2: The September v0.3 pass scored 2 on the evidence above.
  - AI-qualified reading: **1** (grade A, confidence medium). Consumes MCP; exposes no MCP server for agents.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A, confidence medium). Members complete tasks conversationally with retrieval, web search, code and tool actions; there is no natural-language authoring of LibreChat's own definitions.
  - Higher reading 3: The member half of level 3 is fully met.
  - AI-qualified reading: **2** (grade A, confidence medium). Grounded chat with retrieval and tools for members.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A, confidence medium). Token transactions are recorded per request and enforce balances live; OpenTelemetry and Langfuse tracing (otel/). Scored at the lower reading under rule 11 because: Usage accounting rather than behaviour telemetry.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-02 Structured learning signals**: **2** (grade A, confidence medium). Message feedback with rating, tag and text is stored on messages (packages/data-schemas/src/schema/message.ts:103); no triage workflow.
- **LRN-03 User-issue detection**: **2** (grade A, confidence medium). Users rate messages with thumbs and tags, stored on the message (packages/data-schemas/src/schema/message.ts:103).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A, confidence low). No joined usage, support and delivery models.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **1** (grade A, confidence low). Engineers read logs.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.
- **LRN-06 Ranked, evidence-backed proposals for change**: **0** (grade A, confidence medium). No recommendation or proposal features.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A, confidence medium), **3** with opt-in settings. By default nothing learns from use. With the memory block enabled (commented out in librechat.example.yaml:1351-1360), a memory agent stores user facts from recent chat automatically.
  - AI-qualified reading: **1** (grade A, confidence medium), **3** with opt-in settings. People ask an agent to write or edit skills (packages/api/src/agents/handlers.ts:3845-3905); nothing drafts changes from experience unprompted by default.
- **LRN-08 Learned changes are validated before they take effect**: **2** (grade A, confidence medium). Re-read at the v0.7 migration under the tightened boundary: skills agents write are AI-made changes. Creating a skill runs validation whose warnings are returned to the agent (packages/api/src/agents/handlers.ts:1365-1380, 3903), duplicate names are refused and a skill cannot be renamed through an edit (handlers.ts:1500, 3873-3877), and the opt-in memory agent has key and token limits (librechat.example.yaml:1354-1358). Nothing evaluates a skill against a baseline before it takes effect.
  - AI-qualified reading: **2** (grade A, confidence medium). Automated validation and refusal rules on agent-written skills (packages/api/src/agents/handlers.ts:1365-1380, 3873-3877); no baseline evaluation.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A, confidence low). No binding of changes to baselines or metrics.
- **LRN-10 The improvement loop improves itself**: **1** (grade A, confidence low). The checks that govern change are code that engineers change: configuration validation (packages/data-provider/src/config.ts) and skill validation (packages/api/src/skills/deployment.ts:10-15); the tool-approval policy lives in librechat.yaml (librechat.example.yaml:767-775), edited by whoever runs the server. Admins change role permissions for agents, prompts, skills and memories by hand in the product (api/server/routes/roles.js:160-172) with no history. There are no evaluation sets (AIR-05 is 0) and nothing records a failure against the check that missed it.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **2** (grade A, confidence medium). An axe linter workflow runs when triggered manually (.github/workflows/a11y.yml:8-28), Lighthouse audits exist (.github/workflows/lighthouse.yml, e2e/lighthouse), and the ESLint configuration includes accessibility rules.
  - Higher reading 3: If Lighthouse or lint accessibility checks run on every pull request.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A, confidence medium). Admin audit route and audit-log schema (api/server/routes/admin/audit.js, packages/data-schemas/src/types/auditLog.ts); coverage of configuration and definition changes was not verified.
  - Higher reading 3: Admin UI and a generic store exist.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence medium). Users export conversations and delete their accounts, and an admin deletion script removes user data (config/delete-user.js); not driven by field tags.
- **GOV-04 Security as infrastructure**: **2** (grade A, confidence medium). ACL-based permissions for agents, prompts and MCP servers (packages/data-schemas/src/types/accessRole.ts, aclEntry.ts) and system grants; no security scanning in CI.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence medium), facets: implemented. Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Configuration is unversioned in the product.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **2** (grade A, confidence low). Prompt groups stage versions and promote one to production; agents are edited and saved directly; no review step.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A, confidence medium). Every definition change is a direct human action; the approval lifecycle (packages/api/src/stream/ApprovalLifecycle.ts) gates agent tool calls, not changes.
- **GOV-08 Upgrade safety**: **2** (grade A, confidence medium). librechat.yaml carries a schema version checked at load, and UPGRADING.md documents migrations; compatibility is mostly manual.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence medium). Agent API keys with expiry (packages/data-schemas/src/types/agentApiKey.ts), on-behalf-of token exchange for MCP (api/server/services/OboTokenService.js), tool-call approvals before execution, rate limits, audit logs and idempotent trigger deliveries. Scored at the lower reading under rule 11 because: Idempotency covers trigger deliveries, not API mutations.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A, confidence medium). Agent API keys, on-behalf-of token exchange for MCP and tool-call approvals (api/server/services/OboTokenService.js).
- **GOV-10 Bounded self-change**: **2** (grade A, confidence medium). Applies since agent_mutations was re-read as true. Agent skill writes are checked in code: the user's skill-create permission (handlers.ts:3845-3848), edits only to skills the user can already edit (api/server/services/Endpoints/agents/skillDeps.js:133-147), and refusals of duplicate names and renames (handlers.ts:1500, 3873-3877). No rate, volume or blast-radius limit; a skill shared with others changes for them at once.
  - AI-qualified reading: **2** (grade A, confidence medium). Permission and editable-scope checks in code on agent skill writes (skillDeps.js:133-147); no blast-radius limit.
- **GOV-11 Learning-input integrity**: **1** (grade A, confidence low). Applies since agent_mutations was re-read as true. An agent-written skill records its author (packages/api/src/skills/save.ts:104-127) but not the conversation, files or tool results that led to it; no injection scanning was found on the authoring path, and with tool approval off by default (librechat.example.yaml:767-768) content read in the same run can lead to a skill write.
  - AI-qualified reading: **1** (grade A, confidence low). Author recorded on agent-written skills, not source inputs; no injection scanning found on the authoring path.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **EXP-02 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
- **EXP-03 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 1.

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A, confidence low). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence low). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **2** (grade A, confidence medium). Agents, prompts and MCP servers can be shared with selected users and groups through ACLs (packages/data-schemas/src/types/aclEntry.ts).

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **2** (grade A, confidence medium). File search over uploaded files through the RAG API (api/app/clients/tools/util/fileSearch.js); other product data is not indexed.
- **AIR-04 Permission-preserving retrieval and tool access**: **2** (grade A, confidence medium), facets: implemented, tested. Retrieval covers files attached to the conversation or agent; agents shared through ACLs carry their builder's files to other users.
  - Higher reading 3: Per-user file ownership checks may meet level 3.

### Quality

- **AIR-05 Offline AI evaluation**: **0** (grade A, confidence medium). No evaluation harness.
- **AIR-06 Regression gating before release**: **1** (grade A, confidence low). Configuration changes are tested manually in chat.

### Governance

- **AIR-07 AI action tracing and auditability**: **2** (grade A, confidence medium). Messages store model, tokens and tool calls; Langfuse fan-out tracing is optional (packages/api/src/langfuse, traces/handlers.ts).

### Operations

- **AIR-01 Model and provider portability and resilience**: **2** (grade A, confidence medium). Admins configure many providers and model specs (librechat.yaml, packages/api/src/endpoints); no declared resilience strategy.
- **AIR-02 AI usage and per-customer cost controls**: **2** (grade A, confidence medium), **3** with opt-in settings. Token transactions recorded per user; balances that limit spending are opt-in (librechat.example.yaml:363-378).
- **AIR-08 Production quality, drift and feedback monitoring**: **2** (grade A, confidence medium). Users rate messages with tags, and admin insights summarise usage (packages/data-schemas/src/schema/message.ts:103, packages/api/src/insights); no drift alerts.
