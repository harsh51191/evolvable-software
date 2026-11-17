# Dify: EVOLVE v0.7 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.7.0 in this repository.

Scope: the dify monorepo (api, web, dify-agent runtime, packages, CLI, docker configuration, CI). The separately released dify-sandbox and plugin-daemon services are assessed through their configuration here. Dify Cloud and the plugin marketplace catalogue are out of scope.

## Reading

**SAL 1.** Builders reshape apps and workflows without code (Open 2.2), and the AI generators draft prompts and code (DEL-04 2), but there is no intake (DEL-01 0) and no load suite (ARC-06 0), which caps the architecture foundation at L1. **Issue → Fix:** end users' likes and dislikes are recorded per app (LRN-03 2), but there is no grouping or diagnosis (LRN-05 1). **Next level:** structured requests, failure grouping, and measured capacity.

## Limits

Repository evidence only, main at the tip named above. dify-sandbox and plugin-daemon are separate repositories; their behaviour was taken from configuration here and not read in source. Dify Cloud and enterprise editions are out of scope. Single rater.

---
Framework EVOLVE 0.7.0. Date 2026-09-30. Source github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main). Archetype **configurable-application-platform**. Basis **shipped** (what ships).

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, agent_mutations, definition_change_path, ai_features, ai_data_access, ai_actions. False: evolution_auto_apply, code_release_path.

Coverage: 74 assessed, 0 not evidenced, 1 not applicable. Grades: 74 A, 0 B, 0 C.

Confidence: 15 high, 56 medium, 3 low across the assessed criteria. No low-confidence criterion holds a next-level blocker or a critical control.

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

3 of 3 main kinds are self-serve (reach 1 or more: the people running the product make it themselves and can undo it).

| Kind | Who | Main | Reach | Evidence |
|---|---|---|---|---|
| Apps, workflows and agents (`apps-workflows`) | app builders in a workspace | yes | 2 Drafted | Builders change apps and workflows on the canvas with debug runs, then publish; the workflow generator drafts or refines a whole graph for the builder to apply (api/controllers/console/app/generator.py:482-571, api/services/workflow_generator_service.py:45-98), and in agent build mode the agent writes its own configuration into a per-user build draft that a person applies (api/services/agent_config_service.py:913-929, 968-983; apply at api/controllers/console/agent/roster.py:953). Undo: restore any published workflow version to the draft and publish it (api/services/workflow_service.py:622, api/controllers/console/app/workflow.py:1557) and restore an agent version (roster.py:1302, roster_service.py:1450). Reach 2 rests on DEL-04 2. Confidence high. |
| What the AI is told to do (prompts and instructions) (`prompts`) | app builders | yes | 2 Drafted | Builders edit prompts in apps, LLM nodes and agents; the prompt and instruction generators draft them on request (api/controllers/console/app/generator.py:230, :327; api/core/llm_generator/llm_generator.py). Undo: prompts in workflows and agents roll back with their published versions (workflow_service.py:622, roster.py:1302). In basic chat and completion apps each save writes a new model configuration row (api/controllers/console/app/model_config.py:68) but there is no path to restore an earlier one, so undo there is by hand. Confidence medium. |
| Knowledge the apps answer from (`knowledge`) | app builders and knowledge owners | yes | 1 Self-serve | Builders upload, sync and re-index documents and set retrieval in the console with no deploy. Undo: documents can be disabled, re-enabled, archived and un-archived (api/controllers/console/datasets/datasets_document.py:731) or deleted; edits to chunks and retrieval settings keep no history. Confidence medium. |
| Which AI models and credentials are used (`model-providers`) | workspace admins | no | 1 Self-serve | Admins add provider credentials, validate them and choose default models in the console (api/controllers/console/workspace/model_providers.py:148-313). Undo: several credentials are kept per provider and the admin switches back (credentials/switch at :291); default-model changes are set back by hand. Confidence medium. |
| Tools and plugins the apps can use (`tools-plugins`) | workspace admins | no | 1 Self-serve | Admins install plugins from the marketplace, a package or GitHub and upgrade them (api/controllers/console/workspace/plugin.py:810-858, :1010) and add custom API tools. Undo: uninstall (plugin.py:1061); a downgrade path to an earlier plugin version was not found. Confidence medium. |
| New node types, screens and platform behaviour (`platform-features`) | Dify users, through feature requests | no | 0 Engineers only | Changes to Dify itself (core node types, console screens, runtime behaviour) are code in this monorepo, shipped by release; plugins extend tools, models and triggers but not the core. Engineers only. Confidence high. |

### Proven

**Proven: not evidenced.** What operating records show real changes doing, beside what the product is built to do. From a repository alone, proven is usually not evidenced.

| Loop | Built | Proven | Operating records, or what was searched |
|---|---:|---|---|
| Request → Release | L1 | not evidenced | Searched: Repository at the pinned commit: README, docs/, .github workflows and release configuration. Operating records of real changes going through Dify's Request → Release loop (workflow publish history, app logs) live in running deployments, not in the repository. |
| Issue → Fix | L1 | not evidenced | Searched: Repository at the pinned commit: README, docs/, .github workflows and release configuration. Operating records of real changes going through Dify's Issue → Fix loop (workflow publish history, app logs) live in running deployments, not in the repository. |
| Opportunity → Expansion | L1 | not evidenced | Searched: Repository at the pinned commit: README, docs/, .github workflows and release configuration. Operating records of real changes going through Dify's Opportunity → Expansion loop (workflow publish history, app logs) live in running deployments, not in the repository. |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 0 | fail |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 2 | fail |

### What blocks the next level

- **Request → Release to L2**: stages Intake needs DEL-01 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- **Issue → Fix to L2**: stages Diagnose needs LRN-05 ≥ 2 (has 1); stages Propose needs LRN-06 ≥ 2 (has 1); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)

### What AI drives

Each loop re-scored with its AI-performable stages read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level.

| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |
|---|---:|---:|---|---|
| Request → Release | L1 | L0 | DEL-01 0, DEL-04 2 | DEL-01 ≥ 2 (has 0) |
| Issue → Fix | L1 | L0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 2 | LRN-05 ≥ 2 (has 0); LRN-06 ≥ 2 (has 0) |
| Opportunity → Expansion | L1 | L0 | EXP-05 0 | EXP-05 ≥ 2 (has 0) |

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.4 | 1.4–1.6 | 1.4 | 1.4 | 1.4 |
| Velocity (DEL) | 1.5 | 1.5–1.6 | 1.5 | 1.5 | 1.5 |
| Open (MAL) | 2.2 | 2.2–2.8 | 2.2 | 2.2 | 2.2 |
| Learn (LRN) | 1.3 | 1.3–1.6 | 1.3 | 1.3 | 1.3 |
| Vet (GOV) | 1.7 | 1.7–1.9 | 1.7 | 1.7 | 1.7 |
| Expand (EXP) | 1.7 | 1.7 | 1.7 | 1.7 | 1.7 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Scale | 2.0 |
| ARC Capacity | 0.5 |
| ARC Resilience | 1.0 |
| DEL Intake | 0.0 |
| DEL Build | 2.3 |
| DEL Verify | 2.0 |
| DEL Release | 1.5 |
| MAL Data model | 1.3 |
| MAL APIs | 2.3 |
| MAL Interface | 2.0 |
| MAL Behaviour | 2.7 |
| MAL Extensions | 2.3 |
| MAL Integrations | 2.7 |
| MAL Agent interface | 2.0 |
| LRN Sense | 2.0 |
| LRN Diagnose and propose | 1.0 |
| LRN Learn from experience | 2.0 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 1.8 |
| GOV Change control | 1.8 |
| GOV AI and self-change safety | 1.7 |
| EXP Expressible | 3.0 |
| EXP Discover | 0.0 |
| EXP Launch | 2.0 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L1 (Experimental) · Context 2 · Quality 1 · Governance 1 · Operations 2 · not production-governed**

- With opt-in settings: AI Readiness L1 (Experimental) · Context 2 · Quality 1 · Governance 1 · Operations 2 · not production-governed.
- With every alternate reading: AI Readiness L1 (Experimental) · Context 2 · Quality 1 · Governance 1 · Operations 2 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 2 | AIR-03 3, AIR-04 2 |
| Quality | 1 | AIR-05 1, AIR-06 1 |
| Governance | 1 | AIR-07 3, GOV-09 (AI) 1, GOV-10 (AI) 2, GOV-11 (AI) 1, LRN-08 (AI) 2 |
| Operations | 2 | AIR-01 3, AIR-02 3, AIR-08 2, ARC-08 (AI) 2 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 2 | fail |
| Regression evaluation before release | AIR-06 ≥ 3 | 1 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 3 | pass |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 2 | MAL-19 2, MAL-20 2 |
| Build | 1 | DEL-01 0, DEL-04 2 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 2 |
| Expand | 0 | EXP-05 0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A, medium |  | Knowledge bases get vector and keyword indexes configured per dataset (api/core/rag); application lists use SQL with Redis caching. |
| ARC-02 Safe schema and data migrations | assessed | 2 |  |  | A, medium |  | Alembic migrations with downgrade steps (api/migrations/versions, 219 of 219); no enforced online strategy. |
| ARC-03 Horizontal scale of services | assessed | 2 |  |  | A, medium |  | Stateless Flask API and Celery workers over PostgreSQL and Redis, documented through Docker Compose; no scale-out tests or manifests in the repository. |
| ARC-04 Reliable asynchronous work | assessed | 2 |  |  | A, high |  | Celery queues with retries on many tasks (api/extensions/ext_celery.py, api/tasks/delete_conversation_task.py:104); no dead-lettering or idempotency rule. |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A, medium | I | Multi-tenant workspaces with per-app and per-tenant rate limits (api/libs/helper.py) and plan quotas; no noisy-neighbour detection. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 0 | 1 |  | A, medium |  | No load or performance suite and no documented limits found (searched for k6, locust, benchmark and load test). |
| ARC-07 Service objectives defined and monitored | assessed | 1 |  |  | A, medium |  | Optional OpenTelemetry and Sentry; no metrics or objectives for core paths. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A, high |  | AI-qualified reading: 2. Model load balancing with cooldown across credentials (api/core/model_manager.py:68-130); plugins run in a separate daemon and code in a sandbox service. Connectors and internal services have no breakers, so a 3 is not defensible under the inventory rule. |
| ARC-09 Backup, restore and recovery | assessed | 0 | 1 |  | A, high |  | Corrected from 1 after the second-rating study. No supported backup or restore of the database, uploaded files or vector store, and no repository documentation telling operators to back them up: searched api/commands, docker/README.md, docs/, README.md and every *.md, *.sh and *.yaml for backup. The only backup is of the .env file before an env sync (docker/dify-env-sync.sh:82-97, docker/README.md:72-80); the app migration commands move workflow apps and custom tools between environments, not the product's state. Dify's separate documentation repository was not read. |
| DEL-01 Request intake into a structured change specification | assessed | 0 |  |  | A, medium |  | AI-qualified reading: 0. No request or feature-request object for changing the product was found; requests live outside it. |
| DEL-02 Layers deploy independently | assessed | 3 |  |  | A, medium |  | API, worker, web, sandbox, plugin daemon, SSRF proxy and agent runtime are separate containers with separate deploy workflows (9 Dockerfiles; .github/workflows/deploy-agent.yml, deploy-knowledge.yml). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 | 3 |  | A, low |  | import-linter layer contracts for the backend (api/.importlinter:1-20) plus ESLint configuration for the frontend. Scored at the lower reading under rule 11 because: Whether the import-linter contract runs as a required CI check was not verified. |
| DEL-04 AI implementation lane | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 2. AI generators for code, prompts, structured output and workflow instructions assist builders one step at a time (api/core/llm_generator). |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A, medium |  | Main CI on pull requests with no draft filter runs API tests, web tests, style, migration and bundle-size checks (.github/workflows/main-ci.yml, db-migration-test.yml, web-bundle-size.yml); accessibility runs only on demand and there is no security scan. |
| DEL-06 Verification surface | assessed | 2 |  |  | A, high |  | /console/api/version and /console/api/ping (api/controllers/console/system.py:27-37) and a worker health check (api/celery_healthcheck.py); no configuration snapshot. |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A, medium |  | Docker Compose stack, seeded E2E runs (e2e/scripts/seed-runner.ts) and branch-triggered dev deploys (.github/workflows/deploy-dev.yml); no per-change ephemeral environment. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A, medium |  | Web and CLI E2E suites (.github/workflows/web-e2e.yml, cli-e2e.yml); no changed-path map or adoption instrumentation at ship. |
| DEL-09 Staged exposure | assessed | 1 |  |  | A, medium |  | Published app versions go to all users at once. |
| DEL-10 Kill switch | assessed | 2 |  |  | A, high |  | Apps can switch their web app and API off at runtime (api/models/model.py:445-446). |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: No first-party evolution system ships code changes. |
| MAL-01 New entity type without code, DDL or deploy | assessed | 1 | 2 |  | A, medium |  | Entity kinds (apps, workflows, datasets, tools) are fixed models (api/models); new kinds need code, migration and release. |
| MAL-02 Field definitions carry type and validation | assessed | 2 |  |  | A, medium |  | Knowledge-base documents carry user-defined typed metadata fields (DatasetMetadata, api/models/dataset.py); app input variables are typed with validation. No privacy tag; one entity family. |
| MAL-03 Relationships and lifecycle states declarable | assessed | 1 |  |  | A, medium |  | Relations and lifecycle states are coded per feature (draft and published workflows, document indexing states). |
| MAL-04 API per entity is generic or generated | assessed | 2 | 3 |  | A, medium |  | Every app gets the same generated service API shaped by its input variables (api/controllers/service_api), plus an OpenAPI surface (api/controllers/openapi, fastopenapi.py); no per-app code. Scored at the lower reading under rule 11 because: Apps are a single entity family, not arbitrary defined types. |
| MAL-05 API reshapes at runtime from definitions | assessed | 3 |  |  | A, medium |  | Publishing a new workflow version changes the app's API inputs and outputs live (api/services/workflow_service.py version handling). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 | 3 |  | A, low |  | Generated OpenAPI documents (api/controllers/openapi, API_SCHEMA_GUIDE.md), typed SDKs (sdks/) and structured errors. No dry-run. Scored at the lower reading under rule 11 because: Coverage of the whole API by the generated spec was not verified. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 |  |  | A, medium |  | Workflow canvases and each app's web-app settings (branding, opening statement, suggested questions) are data edited by builders; there is no page layout editor. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | assessed | 2 | 3 |  | A, medium |  | Chat, completion and workflow web apps render intake forms generically from each app's typed input variables; list and detail views are hand-built. |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 | 3 |  | A, medium |  | Design-system themes (packages/dify-ui/src/themes) and 1,401 locale files, with AI translation in CI (.github/workflows/translate-i18n-claude.yml); no tenant theme editor or text overrides. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A, medium |  | Workflows and chatflows compose triggers (schedule, webhook, plugin triggers in api/core/trigger), conditions, iteration, code, HTTP, tool and LLM nodes in the UI; debug preview and single-step runs; draft and published versions. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A, medium |  | Inbound webhook and plugin triggers with per-node retry settings and run logs; Dify does not publish its own entity lifecycle events to subscribers. |
| MAL-12 Sandboxed server-side hooks | assessed | 3 |  |  | A, high |  | Code nodes run in the separate dify-sandbox service with a worker timeout (SANDBOX_WORKER_TIMEOUT 15) and all network traffic forced through the SSRF proxy (SANDBOX_HTTP_PROXY, docker/.env.example:193-201, api/core/helper/ssrf_proxy.py); triggered by workflow events and requests. |
| MAL-13 Plugin lane breadth | assessed | 2 | 3 |  | A, medium |  | Plugins extend models, tools, agent strategies, endpoints, data sources and triggers; workflow templates and DSL are declarative; there are no plugin points for UI, theme or text. |
| MAL-14 Runtime isolation and dependency control | assessed | 3 |  |  | A, high |  | Plugins run in the separate plugin daemon, signatures are verified by default (FORCE_VERIFYING_SIGNATURE true) and outbound traffic goes through the SSRF proxy (docker/.env.example:222-236). |
| MAL-15 Developer loop | assessed | 2 | 3 |  | A, medium |  | Plugin developers connect a local plugin to a running Dify instance for remote debugging through the daemon's install port (EXPOSE_PLUGIN_DAEMON_PORT, docker/.env.example:222), with logs; builders debug workflows step by step. Scored at the lower reading under rule 11 because: Remote debugging configuration was read from settings, not exercised. |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A, medium |  | One model-provider interface maps many LLM vendors onto a canonical model API (api/core/model_manager.py, provider_manager.py); data-source plugins map external content into canonical documents and chunks. |
| MAL-17 Connector definition or SDK | assessed | 3 | 4 |  | A, medium |  | Plugin SDK covers credential schemas and OAuth, triggers with subscriptions, data-source sync and install and upgrade lifecycle; admins install from the marketplace; signatures verify publishers. |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A, medium |  | Service API is path-versioned (/v1) and documented; no deprecation windows or conflict handling. |
| MAL-19 Machine-readable capability surface for agents | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. Each app can be exposed as an MCP server with its input schema as the tool definition and a per-app server credential (api/controllers/mcp/mcp.py); Dify also consumes MCP tools. Scored at the lower reading under rule 11 because: No capability map for the platform as a whole. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. End users complete tasks conversationally in Dify apps grounded on knowledge bases with tool actions; builders get natural-language generators for prompts, code, structured output and workflow instructions (api/core/llm_generator/llm_generator.py:432-813). Scored at the lower reading under rule 11 because: Admin natural-language authoring covers parts of a workflow, not whole definitions. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A, medium |  | Per-app statistics and workflow run logs update as runs happen (api/controllers/console/app/statistic.py, workflow_statistic.py); tracing to external LLM-ops tools (api/core/ops). |
| LRN-02 Structured learning signals | assessed | 2 | 3 |  | A, low |  | Message feedback (rating, content, source) is linked to messages and conversations (api/models/model.py:296-335) and triaged through logs and annotations; the link to the app configuration version was not verified. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A, high |  | End users like or dislike answers and the feedback is queryable per app (api/models/model.py:1299-1302); workflow runs record node errors. |
| LRN-04 Cross-source mining inside the product | assessed | 1 | 2 |  | A, medium |  | App statistics combine usage and satisfaction for one app; no joined usage, support and delivery models. |
| LRN-05 Automated diagnosis | assessed | 1 | 2 |  | A, medium |  | AI-qualified reading: 0. Run traces show node-level errors per run; there is no grouping. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 1 |  |  | A, medium |  | AI-qualified reading: 0. Dashboards only; suggestions exist for conversation questions, not for software change. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 0. Admins turn logged answers into annotations that the app reuses for similar questions (api/services/annotation_service.py); nothing proposes changes without being asked. |
| LRN-08 Learned changes are validated before they take effect | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 2. Re-scored 1 to 2 under the v0.7 boundary, which scores the checks on changes the product's AI makes to its own definitions. Agent build-mode config pushes are schema-validated (AgentSoulConfig.model_validate, api/services/agent_config_service.py:946-955) and checked by the composer validator, which rejects plaintext secrets, invalid shell and env configuration and missing assets (api/services/agent/composer_validator.py:230-395), before a person applies them (roster.py:953); AI-drafted workflow graphs pass the same graph validation as hand edits when saved and published. No evaluation against a baseline. Dify has no learning-from-experience loop. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 | 1 |  | A, medium |  | Before-and-after comparison is possible by hand from statistics and traces; nothing binds a published version to a baseline and decision. Scored at the lower reading under rule 11 because: If manual comparison does not count as a mechanism. |
| LRN-10 The improvement loop improves itself | assessed | 0 |  |  | A, medium |  | The checks that govern change are code: graph and DSL validation (api/services/dsl_version.py, app_dsl_service.py), the agent composer validator (api/services/agent/composer_validator.py:52-395) and the build-draft write rules (api/services/agent_config_service.py:968-983). The generators' prompts are code (api/core/llm_generator). There are no evaluation sets for changes and no change policy object (GOV-07 1); nothing records a failure against the check that missed it. Searched api/services, api/core/llm_generator, dify-agent/src. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 2 |  |  | A, high |  | Design system (packages/dify-ui) with accessibility lint rules (lint.config.ts) and an axe-based accessibility E2E workflow that runs on demand for a chosen page and WCAG level (.github/workflows/accessibility-e2e.yml:4-21). |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 1 | 2 |  | A, medium |  | Per-feature logs only: authentication audit entities (api/services/entities/auth_audit_entities.py), app and workflow run logs; no generic audit store. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A, medium |  | Account deletion service and scheduled message cleanup with retention settings (api/services/account_deletion_service.py, api/schedule/clean_messages.py); no data-subject export. |
| GOV-04 Security as infrastructure | assessed | 2 |  |  | A, high |  | RBAC resource and agent-access services (api/services/rbac_resource_service.py), SSRF proxy and plugin signature enforcement (FORCE_VERIFYING_SIGNATURE, docker/.env.example:236); no security scanning in CI. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A, medium | I | Workflows keep numbered published versions (workflow_version_number_service); apps export versioned DSL; other surfaces are unversioned. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Surfaces other than workflows and app DSL are unversioned. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 |  |  | A, medium |  | Draft and publish with debug preview for apps and workflows; no review step or proposal object. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 |  |  | A, medium |  | Every publish is a manual human action; the agent runtime's ask-human layer (dify-agent/src/dify_agent/layers/ask_human/layer.py) gates agent actions, not changes. |
| GOV-08 Upgrade safety | assessed | 2 | 3 |  | A, medium |  | Imported DSL is checked against the current DSL version and flagged when older or newer (api/services/dsl_version.py, app_dsl_service.py); plugins declare manifests and versions against a stable plugin SDK contract. Scored at the lower reading under rule 11 because: If version warnings on import do not count as automated compatibility checks. |
| GOV-09 Agent-safe actions | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 1. App-scoped API keys, OAuth and device-flow login (api/libs/oauth_bearer.py, api/services/oauth_device_flow.py), rate limits and per-call logs; no idempotency keys or dry-run. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A, high |  | AI-qualified reading: 2. Now applicable: agent_mutations is true under the v0.7 definition. The agent's own config writes are enforced server-side: pushes are accepted only on the calling user's DEBUG_BUILD draft of an agent in the same tenant, and published snapshots and the shared draft are not writable from the runtime (api/services/agent_config_service.py:890-955, _require_writable at 968-983, 403 config_not_writable), with tests (api/tests/unit_tests/services/test_agent_config_service.py, api/tests/unit_tests/controllers/inner_api/plugin/test_agent_config.py). The workflow generator path has no enforced scope beyond a person applying the returned graph, and there are no rate or volume limits, so not every self-change path is bounded. |
| GOV-11 Learning-input integrity | assessed | 1 |  |  | A, medium |  | AI-qualified reading: 1. Now applicable: agent_mutations is true under the v0.7 definition. Build drafts record the owning account (api/models/agent.py:252-277), but changes do not record the inputs that drove them, and retrieved knowledge, files and tool output reach the agent's prompt with no fencing or injection scanning (searched dify-agent/src, api/services/agent, api/core/llm_generator for untrusted-content handling; only package documents are validated, api/services/agent/roster_package_reader.py:360). A person applies every change. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 |  |  | A, medium |  | Kernel of tenants, accounts, apps, workflows, datasets, conversations and messages, tools and plugins, served over web, API, MCP and IM channels; no business-domain nouns. |
| EXP-02 A new domain is expressible without kernel change | assessed | 3 |  |  | A, medium |  | Recommended apps and knowledge-pipeline templates ship domain solutions as app definitions, knowledge and tools on an unchanged kernel (api/constants/recommended_apps.json, pipeline_templates.json). |
| EXP-03 A domain ships as an installable bundle | assessed | 3 |  |  | A, medium |  | App DSL export and import is a versioned bundle of app configuration, workflow graph, model settings and tool references (api/services/app_dsl_service.py, dsl_version.py), plus snippet DSL (snippet_dsl_service.py). |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A, medium |  | No record of unmet intents was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A, medium |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 2 |  |  | A, medium |  | Plugins from the marketplace are installed per workspace (api/services/plugin); no success metric or keep-or-kill record. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A, medium |  | Knowledge bases with indexing, retrieval and citations (api/core/rag). |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 2 |  |  | A, medium |  | Dataset permissions control which builders can attach knowledge (api/services/knowledge_retrieval_inner_service.py), but published apps retrieve with the app's datasets, not each end user's permissions. |
| AIR-05 Offline AI evaluation | assessed | 1 |  |  | A, medium |  | Builders test prompts manually in debug and preview; no evaluation harness. |
| AIR-06 Regression gating before release | assessed | 1 |  |  | A, medium |  | Publishing follows manual testing; nothing blocks a regression. |
| AIR-07 AI action tracing and auditability | assessed | 3 |  |  | A, high | IT | Every message and workflow run is logged with inputs, outputs, model, tokens and node and tool executions, viewable by builders, with optional Langfuse, LangSmith and other tracing (api/core/ops/ops_trace_manager.py). |
| AIR-01 Model and provider portability and resilience | assessed | 3 |  |  | A, high |  | Builders choose models per app from many providers; load balancing with cooldown fails over across credentials, with tests (api/core/model_manager.py:68-130, tests/unit_tests/services/test_model_load_balancing_service.py). |
| AIR-02 AI usage and per-customer cost controls | assessed | 3 |  |  | A, high |  | Token usage and cost recorded per message, credit usage and billing quota reservation per tenant (api/core/credit_usage.py, api/services/billing_service.py:77-89). |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 2 |  |  | A, high |  | End-user likes and dislikes and app statistics (satisfaction, tokens) per app (api/models/model.py:1299-1302); no drift alerts. |

Grade cell: evidence grade, then confidence where recorded. Facets: I implemented, T tested, O operated. Operated supports a Proven reading and never changes a score.
