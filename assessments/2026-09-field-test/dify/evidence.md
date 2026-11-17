# Dify evidence

Read at github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Apps, datasets and logs in PostgreSQL; vectors in a vector store; files in object storage.
- **schema_changes**: true. Alembic migrations (api/migrations/versions, 219 files).
- **multi_tenant**: true. Workspaces (tenants) with their own members and roles share one deployment, with tenant_id across the data model and per-tenant limits; operators create more with `flask create-tenant` (api/commands/account.py:91-95).
- **hosted_service**: true. API, Celery worker, web, sandbox and plugin daemon run as long-lived services.
- **machine_actions**: true. The console and service APIs change apps, datasets and workflows.
- **agent_mutations**: true. Changed to true under the v0.7 definition, which counts drafts the product stores awaiting approval. In agent build mode the Dify agent writes its own notes, env, files and skills with `dify-agent config ... push` (dify-agent/src/dify_agent/layers/config/layer.py:29-48) into a per-user DEBUG_BUILD draft stored by the server (api/services/agent_config_service.py:913-929); a person applies it (api/controllers/console/agent/roster.py:953). The workflow generator also drafts graphs for the editor (api/services/workflow_generator_service.py:45-98).
- **evolution_auto_apply**: false. AI changes land in a build draft or the editor; applying and publishing are human actions (roster.py:953; workflow publish). No learning loop applies changes.
- **definition_change_path**: true. Apps, workflows, prompts and datasets are definitions.
- **code_release_path**: false. False under the v0.7 definition. The code generator drafts code-node source into the editor (api/controllers/console/app/generator.py:263) and build mode can push skill files to a draft, but a person saves, applies and publishes them, and they are versioned and restored with the workflow or agent definition; the AI does not activate code, and no first-party lane ships Dify's own code.
- **ai_features**: true. LLM apps, agents and workflows are the product (api/core).
- **ai_data_access**: true. Knowledge-base retrieval (api/core/rag).
- **ai_actions**: true. Agent and workflow tools call external services and write data (api/core/tools).

## Kinds of change

- **Apps, workflows and agents** (`apps-workflows`, main, made by app builders in a workspace): reach **2 Drafted**, confidence high. Builders change apps and workflows on the canvas with debug runs, then publish; the workflow generator drafts or refines a whole graph for the builder to apply (api/controllers/console/app/generator.py:482-571, api/services/workflow_generator_service.py:45-98), and in agent build mode the agent writes its own configuration into a per-user build draft that a person applies (api/services/agent_config_service.py:913-929, 968-983; apply at api/controllers/console/agent/roster.py:953). Undo: restore any published workflow version to the draft and publish it (api/services/workflow_service.py:622, api/controllers/console/app/workflow.py:1557) and restore an agent version (roster.py:1302, roster_service.py:1450). Reach 2 rests on DEL-04 2.
- **What the AI is told to do (prompts and instructions)** (`prompts`, main, made by app builders): reach **2 Drafted**, confidence medium. Builders edit prompts in apps, LLM nodes and agents; the prompt and instruction generators draft them on request (api/controllers/console/app/generator.py:230, :327; api/core/llm_generator/llm_generator.py). Undo: prompts in workflows and agents roll back with their published versions (workflow_service.py:622, roster.py:1302). In basic chat and completion apps each save writes a new model configuration row (api/controllers/console/app/model_config.py:68) but there is no path to restore an earlier one, so undo there is by hand.
- **Knowledge the apps answer from** (`knowledge`, main, made by app builders and knowledge owners): reach **1 Self-serve**, confidence medium. Builders upload, sync and re-index documents and set retrieval in the console with no deploy. Undo: documents can be disabled, re-enabled, archived and un-archived (api/controllers/console/datasets/datasets_document.py:731) or deleted; edits to chunks and retrieval settings keep no history.
- **Which AI models and credentials are used** (`model-providers`, not main, made by workspace admins): reach **1 Self-serve**, confidence medium. Admins add provider credentials, validate them and choose default models in the console (api/controllers/console/workspace/model_providers.py:148-313). Undo: several credentials are kept per provider and the admin switches back (credentials/switch at :291); default-model changes are set back by hand.
- **Tools and plugins the apps can use** (`tools-plugins`, not main, made by workspace admins): reach **1 Self-serve**, confidence medium. Admins install plugins from the marketplace, a package or GitHub and upgrade them (api/controllers/console/workspace/plugin.py:810-858, :1010) and add custom API tools. Undo: uninstall (plugin.py:1061); a downgrade path to an earlier plugin version was not found.
- **New node types, screens and platform behaviour** (`platform-features`, not main, made by Dify users, through feature requests): reach **0 Engineers only**, confidence high. Changes to Dify itself (core node types, console screens, runtime behaviour) are code in this monorepo, shipped by release; plugins extend tools, models and triggers but not the core. Engineers only.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md, .agents/skills (backend and frontend code review, testing), .claude/skills and settings; CI workflow translate-i18n-claude.yml runs anthropics/claude-code-action pinned by SHA (v1.0.235) on manual dispatch to translate locale files, told not to create branches, commits or pull requests.
- **Proven, Request → Release**: not evidenced. Searched: Repository at the pinned commit: README, docs/, .github workflows and release configuration. Operating records of real changes going through Dify's Request → Release loop (workflow publish history, app logs) live in running deployments, not in the repository.
- **Proven, Issue → Fix**: not evidenced. Searched: Repository at the pinned commit: README, docs/, .github workflows and release configuration. Operating records of real changes going through Dify's Issue → Fix loop (workflow publish history, app logs) live in running deployments, not in the repository.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: Repository at the pinned commit: README, docs/, .github workflows and release configuration. Operating records of real changes going through Dify's Opportunity → Expansion loop (workflow publish history, app logs) live in running deployments, not in the repository.

Confidence for criteria whose score did not change in the v0.7 migration was assigned at migration from the recorded evidence; confidence for new and changed readings (kinds of change, LRN-10 and every re-read criterion) comes from re-reading the source at the pinned commit.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **2** (grade A, confidence medium). Knowledge bases get vector and keyword indexes configured per dataset (api/core/rag); application lists use SQL with Redis caching.
- **ARC-02 Safe schema and data migrations**: **2** (grade A, confidence medium). Alembic migrations with downgrade steps (api/migrations/versions, 219 of 219); no enforced online strategy.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A, confidence medium). Stateless Flask API and Celery workers over PostgreSQL and Redis, documented through Docker Compose; no scale-out tests or manifests in the repository.
- **ARC-04 Reliable asynchronous work**: **2** (grade A, confidence high). Celery queues with retries on many tasks (api/extensions/ext_celery.py, api/tasks/delete_conversation_task.py:104); no dead-lettering or idempotency rule.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A, confidence medium), facets: implemented. Multi-tenant workspaces with per-app and per-tenant rate limits (api/libs/helper.py) and plan quotas; no noisy-neighbour detection.
  - Higher reading 3: Per-tenant limits are present throughout.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **0** (grade A, confidence medium). No load or performance suite and no documented limits found (searched for k6, locust, benchmark and load test).
  - Higher reading 1: Vector-database test suites exercise one surface.
- **ARC-07 Service objectives defined and monitored**: **1** (grade A, confidence medium). Optional OpenTelemetry and Sentry; no metrics or objectives for core paths.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence high). Model load balancing with cooldown across credentials (api/core/model_manager.py:68-130); plugins run in a separate daemon and code in a sandbox service. Connectors and internal services have no breakers, so a 3 is not defensible under the inventory rule.
  - AI-qualified reading: **2** (grade A, confidence medium), facets: implemented. Load balancing with cooldown across credentials (api/core/model_manager.py).
    - Higher reading 3: Cooldown acts as a breaker.
- **ARC-09 Backup, restore and recovery**: **0** (grade A, confidence high). Corrected from 1 after the second-rating study. No supported backup or restore of the database, uploaded files or vector store, and no repository documentation telling operators to back them up: searched api/commands, docker/README.md, docs/, README.md and every *.md, *.sh and *.yaml for backup. The only backup is of the .env file before an env sync (docker/dify-env-sync.sh:82-97, docker/README.md:72-80); the app migration commands move workflow apps and custom tools between environments, not the product's state. Dify's separate documentation repository was not read.
  - Higher reading 1: The cross-environment app migration exports and imports workflow apps and custom tools (api/commands/data_migration.py:88-147, docs/cross-env-app-migration/README.md) and the env-sync script backs up .env (docker/dify-env-sync.sh:82-97); a rater may count these as level 1.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A, confidence medium). No request or feature-request object for changing the product was found; requests live outside it.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A, confidence medium). API, worker, web, sandbox, plugin daemon, SSRF proxy and agent runtime are separate containers with separate deploy workflows (9 Dockerfiles; .github/workflows/deploy-agent.yml, deploy-knowledge.yml).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A, confidence low). import-linter layer contracts for the backend (api/.importlinter:1-20) plus ESLint configuration for the frontend. Scored at the lower reading under rule 11 because: Whether the import-linter contract runs as a required CI check was not verified.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **DEL-04 AI implementation lane**: **2** (grade A, confidence medium). AI generators for code, prompts, structured output and workflow instructions assist builders one step at a time (api/core/llm_generator).
  - AI-qualified reading: **2** (grade A, confidence medium). AI generators draft prompts, code and workflow steps (api/core/llm_generator).

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence medium). Main CI on pull requests with no draft filter runs API tests, web tests, style, migration and bundle-size checks (.github/workflows/main-ci.yml, db-migration-test.yml, web-bundle-size.yml); accessibility runs only on demand and there is no security scan.
- **DEL-06 Verification surface**: **2** (grade A, confidence high). /console/api/version and /console/api/ping (api/controllers/console/system.py:27-37) and a worker health check (api/celery_healthcheck.py); no configuration snapshot.
- **DEL-07 Environment reproducibility**: **2** (grade A, confidence medium). Docker Compose stack, seeded E2E runs (e2e/scripts/seed-runner.ts) and branch-triggered dev deploys (.github/workflows/deploy-dev.yml); no per-change ephemeral environment.
  - Higher reading 3: E2E runs create seeded, disposable instances per change.
- **DEL-08 Machine verifiability**: **2** (grade A, confidence medium). Web and CLI E2E suites (.github/workflows/web-e2e.yml, cli-e2e.yml); no changed-path map or adoption instrumentation at ship.

### Release

- **DEL-09 Staged exposure**: **1** (grade A, confidence medium). Published app versions go to all users at once.
- **DEL-10 Kill switch**: **2** (grade A, confidence high). Apps can switch their web app and API off at runtime (api/models/model.py:445-446).
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: No first-party evolution system ships code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **1** (grade A, confidence medium). Entity kinds (apps, workflows, datasets, tools) are fixed models (api/models); new kinds need code, migration and release.
  - Higher reading 2: Apps and datasets behave like runtime-defined entities, though of fixed kinds.
- **MAL-02 Field definitions carry type and validation**: **2** (grade A, confidence medium). Knowledge-base documents carry user-defined typed metadata fields (DatasetMetadata, api/models/dataset.py); app input variables are typed with validation. No privacy tag; one entity family.
- **MAL-03 Relationships and lifecycle states declarable**: **1** (grade A, confidence medium). Relations and lifecycle states are coded per feature (draft and published workflows, document indexing states).

### APIs

- **MAL-04 API per entity is generic or generated**: **2** (grade A, confidence medium). Every app gets the same generated service API shaped by its input variables (api/controllers/service_api), plus an OpenAPI surface (api/controllers/openapi, fastopenapi.py); no per-app code. Scored at the lower reading under rule 11 because: Apps are a single entity family, not arbitrary defined types.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **MAL-05 API reshapes at runtime from definitions**: **3** (grade A, confidence medium). Publishing a new workflow version changes the app's API inputs and outputs live (api/services/workflow_service.py version handling).
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A, confidence low). Generated OpenAPI documents (api/controllers/openapi, API_SCHEMA_GUIDE.md), typed SDKs (sdks/) and structured errors. No dry-run. Scored at the lower reading under rule 11 because: Coverage of the whole API by the generated spec was not verified.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Workflow canvases and each app's web-app settings (branding, opening statement, suggested questions) are data edited by builders; there is no page layout editor.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **2** (grade A, confidence medium). Chat, completion and workflow web apps render intake forms generically from each app's typed input variables; list and detail views are hand-built.
  - Higher reading 3: Intake is fully generic and logs and annotations views are generic across apps.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A, confidence medium). Design-system themes (packages/dify-ui/src/themes) and 1,401 locale files, with AI translation in CI (.github/workflows/translate-i18n-claude.yml); no tenant theme editor or text overrides.
  - Higher reading 3: The locale pipeline includes AI translation.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **3** (grade A, confidence medium). Workflows and chatflows compose triggers (schedule, webhook, plugin triggers in api/core/trigger), conditions, iteration, code, HTTP, tool and LLM nodes in the UI; debug preview and single-step runs; draft and published versions.
  - Higher reading 4: Versioned, testable and partly AI-assisted (generate_workflow_instruction_suggestions), but not simulatable against history.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A, confidence medium). Inbound webhook and plugin triggers with per-node retry settings and run logs; Dify does not publish its own entity lifecycle events to subscribers.
- **MAL-12 Sandboxed server-side hooks**: **3** (grade A, confidence high). Code nodes run in the separate dify-sandbox service with a worker timeout (SANDBOX_WORKER_TIMEOUT 15) and all network traffic forced through the SSRF proxy (SANDBOX_HTTP_PROXY, docker/.env.example:193-201, api/core/helper/ssrf_proxy.py); triggered by workflow events and requests.

### Extensions

- **MAL-13 Plugin lane breadth**: **2** (grade A, confidence medium). Plugins extend models, tools, agent strategies, endpoints, data sources and triggers; workflow templates and DSL are declarative; there are no plugin points for UI, theme or text.
  - Higher reading 3: Breadth across server surfaces is large.
- **MAL-14 Runtime isolation and dependency control**: **3** (grade A, confidence high). Plugins run in the separate plugin daemon, signatures are verified by default (FORCE_VERIFYING_SIGNATURE true) and outbound traffic goes through the SSRF proxy (docker/.env.example:222-236).
- **MAL-15 Developer loop**: **2** (grade A, confidence medium). Plugin developers connect a local plugin to a running Dify instance for remote debugging through the daemon's install port (EXPOSE_PLUGIN_DAEMON_PORT, docker/.env.example:222), with logs; builders debug workflows step by step. Scored at the lower reading under rule 11 because: Remote debugging configuration was read from settings, not exercised.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A, confidence medium). One model-provider interface maps many LLM vendors onto a canonical model API (api/core/model_manager.py, provider_manager.py); data-source plugins map external content into canonical documents and chunks.
- **MAL-17 Connector definition or SDK**: **3** (grade A, confidence medium). Plugin SDK covers credential schemas and OAuth, triggers with subscriptions, data-source sync and install and upgrade lifecycle; admins install from the marketplace; signatures verify publishers.
  - Higher reading 4: Signature verification is a form of certification.
- **MAL-18 Stable versioned contracts**: **2** (grade A, confidence medium). Service API is path-versioned (/v1) and documented; no deprecation windows or conflict handling.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A, confidence medium). Each app can be exposed as an MCP server with its input schema as the tool definition and a per-app server credential (api/controllers/mcp/mcp.py); Dify also consumes MCP tools. Scored at the lower reading under rule 11 because: No capability map for the platform as a whole.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A, confidence medium). Apps exposed as MCP servers with a per-app credential (api/controllers/mcp/mcp.py).
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A, confidence medium). End users complete tasks conversationally in Dify apps grounded on knowledge bases with tool actions; builders get natural-language generators for prompts, code, structured output and workflow instructions (api/core/llm_generator/llm_generator.py:432-813). Scored at the lower reading under rule 11 because: Admin natural-language authoring covers parts of a workflow, not whole definitions.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A, confidence medium). Grounded end-user apps and builder generators.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **3** (grade A, confidence medium). Per-app statistics and workflow run logs update as runs happen (api/controllers/console/app/statistic.py, workflow_statistic.py); tracing to external LLM-ops tools (api/core/ops).
- **LRN-02 Structured learning signals**: **2** (grade A, confidence low). Message feedback (rating, content, source) is linked to messages and conversations (api/models/model.py:296-335) and triaged through logs and annotations; the link to the app configuration version was not verified.
  - Higher reading 3: Messages record the app configuration they ran with.
- **LRN-03 User-issue detection**: **2** (grade A, confidence high). End users like or dislike answers and the feedback is queryable per app (api/models/model.py:1299-1302); workflow runs record node errors.
- **LRN-04 Cross-source mining inside the product**: **1** (grade A, confidence medium). App statistics combine usage and satisfaction for one app; no joined usage, support and delivery models.
  - Higher reading 2: Satisfaction joins feedback and usage for each app.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **1** (grade A, confidence medium). Run traces show node-level errors per run; there is no grouping.
  - Higher reading 2: Per-run traces attach context.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.
- **LRN-06 Ranked, evidence-backed proposals for change**: **1** (grade A, confidence medium). Dashboards only; suggestions exist for conversation questions, not for software change.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **2** (grade A, confidence medium). Admins turn logged answers into annotations that the app reuses for similar questions (api/services/annotation_service.py); nothing proposes changes without being asked.
  - AI-qualified reading: **0** (grade A, confidence medium). Annotations are curated by people.
- **LRN-08 Learned changes are validated before they take effect**: **2** (grade A, confidence medium). Re-scored 1 to 2 under the v0.7 boundary, which scores the checks on changes the product's AI makes to its own definitions. Agent build-mode config pushes are schema-validated (AgentSoulConfig.model_validate, api/services/agent_config_service.py:946-955) and checked by the composer validator, which rejects plaintext secrets, invalid shell and env configuration and missing assets (api/services/agent/composer_validator.py:230-395), before a person applies them (roster.py:953); AI-drafted workflow graphs pass the same graph validation as hand edits when saved and published. No evaluation against a baseline. Dify has no learning-from-experience loop.
  - AI-qualified reading: **2** (grade A, confidence medium). Automated schema and validator checks on AI-made agent configuration (composer_validator.py, agent_config_service.py:946-955); no baseline evaluation.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A, confidence medium). Before-and-after comparison is possible by hand from statistics and traces; nothing binds a published version to a baseline and decision. Scored at the lower reading under rule 11 because: If manual comparison does not count as a mechanism.
  - Higher reading 1: The September v0.3 pass scored 1 on the evidence above.
- **LRN-10 The improvement loop improves itself**: **0** (grade A, confidence medium). The checks that govern change are code: graph and DSL validation (api/services/dsl_version.py, app_dsl_service.py), the agent composer validator (api/services/agent/composer_validator.py:52-395) and the build-draft write rules (api/services/agent_config_service.py:968-983). The generators' prompts are code (api/core/llm_generator). There are no evaluation sets for changes and no change policy object (GOV-07 1); nothing records a failure against the check that missed it. Searched api/services, api/core/llm_generator, dify-agent/src.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **2** (grade A, confidence high). Design system (packages/dify-ui) with accessibility lint rules (lint.config.ts) and an axe-based accessibility E2E workflow that runs on demand for a chosen page and WCAG level (.github/workflows/accessibility-e2e.yml:4-21).
- **GOV-02 Audit generic over entities, definition changes and approvals**: **1** (grade A, confidence medium). Per-feature logs only: authentication audit entities (api/services/entities/auth_audit_entities.py), app and workflow run logs; no generic audit store.
  - Higher reading 2: Run logs are generic across apps.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence medium). Account deletion service and scheduled message cleanup with retention settings (api/services/account_deletion_service.py, api/schedule/clean_messages.py); no data-subject export.
- **GOV-04 Security as infrastructure**: **2** (grade A, confidence high). RBAC resource and agent-access services (api/services/rbac_resource_service.py), SSRF proxy and plugin signature enforcement (FORCE_VERIFYING_SIGNATURE, docker/.env.example:236); no security scanning in CI.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence medium), facets: implemented. Workflows keep numbered published versions (workflow_version_number_service); apps export versioned DSL; other surfaces are unversioned. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Surfaces other than workflows and app DSL are unversioned.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **2** (grade A, confidence medium). Draft and publish with debug preview for apps and workflows; no review step or proposal object.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A, confidence medium). Every publish is a manual human action; the agent runtime's ask-human layer (dify-agent/src/dify_agent/layers/ask_human/layer.py) gates agent actions, not changes.
- **GOV-08 Upgrade safety**: **2** (grade A, confidence medium). Imported DSL is checked against the current DSL version and flagged when older or newer (api/services/dsl_version.py, app_dsl_service.py); plugins declare manifests and versions against a stable plugin SDK contract. Scored at the lower reading under rule 11 because: If version warnings on import do not count as automated compatibility checks.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence medium). App-scoped API keys, OAuth and device-flow login (api/libs/oauth_bearer.py, api/services/oauth_device_flow.py), rate limits and per-call logs; no idempotency keys or dry-run.
  - AI-qualified reading: **1** (grade A, confidence medium). Agent tools run with credentials configured by the builder, shared across end users.
- **GOV-10 Bounded self-change**: **2** (grade A, confidence high). Now applicable: agent_mutations is true under the v0.7 definition. The agent's own config writes are enforced server-side: pushes are accepted only on the calling user's DEBUG_BUILD draft of an agent in the same tenant, and published snapshots and the shared draft are not writable from the runtime (api/services/agent_config_service.py:890-955, _require_writable at 968-983, 403 config_not_writable), with tests (api/tests/unit_tests/services/test_agent_config_service.py, api/tests/unit_tests/controllers/inner_api/plugin/test_agent_config.py). The workflow generator path has no enforced scope beyond a person applying the returned graph, and there are no rate or volume limits, so not every self-change path is bounded.
  - AI-qualified reading: **2** (grade A, confidence high). An enforced allow rule for the agent build-mode path (agent_config_service.py:968-983); the workflow generator path is unbounded.
- **GOV-11 Learning-input integrity**: **1** (grade A, confidence medium). Now applicable: agent_mutations is true under the v0.7 definition. Build drafts record the owning account (api/models/agent.py:252-277), but changes do not record the inputs that drove them, and retrieved knowledge, files and tool output reach the agent's prompt with no fencing or injection scanning (searched dify-agent/src, api/services/agent, api/core/llm_generator for untrusted-content handling; only package documents are validated, api/services/agent/roster_package_reader.py:360). A person applies every change.
  - AI-qualified reading: **1** (grade A, confidence low). No provenance of source inputs on AI-made config changes and no fencing of untrusted content; mitigated only by human apply.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A, confidence medium). Kernel of tenants, accounts, apps, workflows, datasets, conversations and messages, tools and plugins, served over web, API, MCP and IM channels; no business-domain nouns.
- **EXP-02 A new domain is expressible without kernel change**: **3** (grade A, confidence medium). Recommended apps and knowledge-pipeline templates ship domain solutions as app definitions, knowledge and tools on an unchanged kernel (api/constants/recommended_apps.json, pipeline_templates.json).
- **EXP-03 A domain ships as an installable bundle**: **3** (grade A, confidence medium). App DSL export and import is a versioned bundle of app configuration, workflow graph, model settings and tool references (api/services/app_dsl_service.py, dsl_version.py), plus snippet DSL (snippet_dsl_service.py).

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A, confidence medium). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence medium). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **2** (grade A, confidence medium). Plugins from the marketplace are installed per workspace (api/services/plugin); no success metric or keep-or-kill record.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence medium). Knowledge bases with indexing, retrieval and citations (api/core/rag).
- **AIR-04 Permission-preserving retrieval and tool access**: **2** (grade A, confidence medium). Dataset permissions control which builders can attach knowledge (api/services/knowledge_retrieval_inner_service.py), but published apps retrieve with the app's datasets, not each end user's permissions.

### Quality

- **AIR-05 Offline AI evaluation**: **1** (grade A, confidence medium). Builders test prompts manually in debug and preview; no evaluation harness.
- **AIR-06 Regression gating before release**: **1** (grade A, confidence medium). Publishing follows manual testing; nothing blocks a regression.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A, confidence high), facets: implemented, tested. Every message and workflow run is logged with inputs, outputs, model, tokens and node and tool executions, viewable by builders, with optional Langfuse, LangSmith and other tracing (api/core/ops/ops_trace_manager.py).

### Operations

- **AIR-01 Model and provider portability and resilience**: **3** (grade A, confidence high). Builders choose models per app from many providers; load balancing with cooldown fails over across credentials, with tests (api/core/model_manager.py:68-130, tests/unit_tests/services/test_model_load_balancing_service.py).
- **AIR-02 AI usage and per-customer cost controls**: **3** (grade A, confidence high). Token usage and cost recorded per message, credit usage and billing quota reservation per tenant (api/core/credit_usage.py, api/services/billing_service.py:77-89).
- **AIR-08 Production quality, drift and feedback monitoring**: **2** (grade A, confidence high). End-user likes and dislikes and app statistics (satisfaction, tokens) per app (api/models/model.py:1299-1302); no drift alerts.
