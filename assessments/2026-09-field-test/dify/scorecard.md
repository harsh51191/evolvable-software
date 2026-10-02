# Dify: EVOLVE v0.5 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.5.0 in this repository.

Scope: the dify monorepo (api, web, dify-agent runtime, packages, CLI, docker configuration, CI). The separately released dify-sandbox and plugin-daemon services are assessed through their configuration here. Dify Cloud and the plugin marketplace catalogue are out of scope.

## Reading

**SAL 1.** Builders reshape apps and workflows without code (Open 2.2), and the AI generators draft prompts and code (DEL-04 2), but there is no intake (DEL-01 0) and no load suite (ARC-06 0), which caps the architecture foundation at L1. **Issue → Fix:** end users' likes and dislikes are recorded per app (LRN-03 2), but there is no grouping or diagnosis (LRN-05 1). **Next level:** structured requests, failure grouping, and measured capacity.

## Limits

Repository evidence only, main at the tip named above. dify-sandbox and plugin-daemon are separate repositories; their behaviour was taken from configuration here and not read in source. Dify Cloud and enterprise editions are out of scope. Single rater.

---
Framework EVOLVE 0.5.0. Date 2026-09-30. Source github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main). Archetype **configurable-application-platform**.

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, definition_change_path, ai_features, ai_data_access, ai_actions. False: agent_mutations, evolution_auto_apply, code_release_path.

Coverage: 71 assessed, 0 not evidenced, 3 not applicable. Grades: 71 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L1**

Progress toward the next level: Request → Release 2 of 4 conditions for L2; Issue → Fix 2 of 5 conditions for L2; Opportunity → Expansion 2 of 5 conditions for L2.

- With opt-in settings: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L1.
- With every alternate reading: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L1.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L2 | L1 | L2 | **L1** | L1 |
| Issue → Fix | L1 | L2 | L1 | L2 | **L1** | L1 |
| Opportunity → Expansion | L1 | L2 | L1 | L2 | **L1** | L1 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 1 | fail |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | not applicable (agent_mutations and evolution_auto_apply false) | n/a | n/a |

### What blocks the next level

- **Request → Release to L2**: stages Intake needs DEL-01 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0)
- **Issue → Fix to L2**: stages Diagnose needs LRN-05 ≥ 2 (has 1); stages Propose needs LRN-06 ≥ 2 (has 1); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0)

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.5 | 1.5–1.6 | 1.5 | 1.5 | 1.5 |
| Velocity (DEL) | 1.5 | 1.5–1.6 | 1.5 | 1.5 | 1.5 |
| Open (MAL) | 2.2 | 2.2–2.8 | 2.2 | 2.2 | 2.2 |
| Learn (LRN) | 1.1 | 1.1–1.6 | 1.1 | 1.1 | 1.1 |
| Vet (GOV) | 1.8 | 1.8–2.0 | 1.8 | 1.8 | 1.6 |
| Expand (EXP) | 1.7 | 1.7 | 1.7 | 1.7 | 1.7 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L1 (Experimental) · Context 2 · Quality 1 · Governance 2 · Operations 2 · not production-governed**

- With opt-in settings: AI Readiness L1 (Experimental) · Context 2 · Quality 1 · Governance 2 · Operations 2 · not production-governed.
- With every alternate reading: AI Readiness L1 (Experimental) · Context 2 · Quality 1 · Governance 2 · Operations 2 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 2 | AIR-03 3, AIR-04 2 |
| Quality | 1 | AIR-05 1, AIR-06 1 |
| Governance | 2 | AIR-07 3, GOV-09 (AI) 1 |
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
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 n/a |
| Expand | 0 | EXP-05 0 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Scale | 2.0 |
| ARC Capacity | 0.5 |
| ARC Resilience | 1.5 |
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
| LRN Learn from experience | 1.5 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 1.8 |
| GOV Change control | 1.8 |
| GOV AI and self-change safety | 2.0 |
| EXP Expressible | 3.0 |
| EXP Discover | 0.0 |
| EXP Launch | 2.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A |  | Knowledge bases get vector and keyword indexes configured per dataset (api/core/rag); application lists use SQL with Redis caching. |
| ARC-02 Safe schema and data migrations | assessed | 2 |  |  | A |  | Alembic migrations with downgrade steps (api/migrations/versions, 219 of 219); no enforced online strategy. |
| ARC-03 Horizontal scale of services | assessed | 2 |  |  | A |  | Stateless Flask API and Celery workers over PostgreSQL and Redis, documented through Docker Compose; no scale-out tests or manifests in the repository. |
| ARC-04 Reliable asynchronous work | assessed | 2 |  |  | A |  | Celery queues with retries on many tasks (api/extensions/ext_celery.py, api/tasks/delete_conversation_task.py:104); no dead-lettering or idempotency rule. |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | I | Multi-tenant workspaces with per-app and per-tenant rate limits (api/libs/helper.py) and plan quotas; no noisy-neighbour detection. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 0 | 1 |  | A |  | No load or performance suite and no documented limits found (searched for k6, locust, benchmark and load test). |
| ARC-07 Service objectives defined and monitored | assessed | 1 |  |  | A |  | Optional OpenTelemetry and Sentry; no metrics or objectives for core paths. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Model load balancing with cooldown across credentials (api/core/model_manager.py:68-130); plugins run in a separate daemon and code in a sandbox service. Connectors and internal services have no breakers, so a 3 is not defensible under the inventory rule. |
| ARC-09 Backup, restore and recovery | assessed | 1 |  |  | A |  | No backup command; Docker volume backup is left to operators. |
| DEL-01 Request intake into a structured change specification | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No request or feature-request object for changing the product was found; requests live outside it. |
| DEL-02 Layers deploy independently | assessed | 3 |  |  | A |  | API, worker, web, sandbox, plugin daemon, SSRF proxy and agent runtime are separate containers with separate deploy workflows (9 Dockerfiles; .github/workflows/deploy-agent.yml, deploy-knowledge.yml). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 | 3 |  | A |  | import-linter layer contracts for the backend (api/.importlinter:1-20) plus ESLint configuration for the frontend. Scored at the lower reading under rule 11 because: Whether the import-linter contract runs as a required CI check was not verified. |
| DEL-04 AI implementation lane | assessed | 2 |  |  | A |  | AI-qualified reading: 2. AI generators for code, prompts, structured output and workflow instructions assist builders one step at a time (api/core/llm_generator). |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A |  | Main CI on pull requests with no draft filter runs API tests, web tests, style, migration and bundle-size checks (.github/workflows/main-ci.yml, db-migration-test.yml, web-bundle-size.yml); accessibility runs only on demand and there is no security scan. |
| DEL-06 Verification surface | assessed | 2 |  |  | A |  | /console/api/version and /console/api/ping (api/controllers/console/system.py:27-37) and a worker health check (api/celery_healthcheck.py); no configuration snapshot. |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A |  | Docker Compose stack, seeded E2E runs (e2e/scripts/seed-runner.ts) and branch-triggered dev deploys (.github/workflows/deploy-dev.yml); no per-change ephemeral environment. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A |  | Web and CLI E2E suites (.github/workflows/web-e2e.yml, cli-e2e.yml); no changed-path map or adoption instrumentation at ship. |
| DEL-09 Staged exposure | assessed | 1 |  |  | A |  | Published app versions go to all users at once. |
| DEL-10 Kill switch | assessed | 2 |  |  | A |  | Apps can switch their web app and API off at runtime (api/models/model.py:445-446). |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: No first-party evolution system ships code changes. |
| MAL-01 New entity type without code, DDL or deploy | assessed | 1 | 2 |  | A |  | Entity kinds (apps, workflows, datasets, tools) are fixed models (api/models); new kinds need code, migration and release. |
| MAL-02 Field definitions carry type and validation | assessed | 2 |  |  | A |  | Knowledge-base documents carry user-defined typed metadata fields (DatasetMetadata, api/models/dataset.py); app input variables are typed with validation. No privacy tag; one entity family. |
| MAL-03 Relationships and lifecycle states declarable | assessed | 1 |  |  | A |  | Relations and lifecycle states are coded per feature (draft and published workflows, document indexing states). |
| MAL-04 API per entity is generic or generated | assessed | 2 | 3 |  | A |  | Every app gets the same generated service API shaped by its input variables (api/controllers/service_api), plus an OpenAPI surface (api/controllers/openapi, fastopenapi.py); no per-app code. Scored at the lower reading under rule 11 because: Apps are a single entity family, not arbitrary defined types. |
| MAL-05 API reshapes at runtime from definitions | assessed | 3 |  |  | A |  | Publishing a new workflow version changes the app's API inputs and outputs live (api/services/workflow_service.py version handling). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 | 3 |  | A |  | Generated OpenAPI documents (api/controllers/openapi, API_SCHEMA_GUIDE.md), typed SDKs (sdks/) and structured errors. No dry-run. Scored at the lower reading under rule 11 because: Coverage of the whole API by the generated spec was not verified. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 |  |  | A |  | Workflow canvases and each app's web-app settings (branding, opening statement, suggested questions) are data edited by builders; there is no page layout editor. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | assessed | 2 | 3 |  | A |  | Chat, completion and workflow web apps render intake forms generically from each app's typed input variables; list and detail views are hand-built. |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 | 3 |  | A |  | Design-system themes (packages/dify-ui/src/themes) and 1,401 locale files, with AI translation in CI (.github/workflows/translate-i18n-claude.yml); no tenant theme editor or text overrides. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A |  | Workflows and chatflows compose triggers (schedule, webhook, plugin triggers in api/core/trigger), conditions, iteration, code, HTTP, tool and LLM nodes in the UI; debug preview and single-step runs; draft and published versions. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A |  | Inbound webhook and plugin triggers with per-node retry settings and run logs; Dify does not publish its own entity lifecycle events to subscribers. |
| MAL-12 Sandboxed server-side hooks | assessed | 3 |  |  | A |  | Code nodes run in the separate dify-sandbox service with a worker timeout (SANDBOX_WORKER_TIMEOUT 15) and all network traffic forced through the SSRF proxy (SANDBOX_HTTP_PROXY, docker/.env.example:193-201, api/core/helper/ssrf_proxy.py); triggered by workflow events and requests. |
| MAL-13 Plugin lane breadth | assessed | 2 | 3 |  | A |  | Plugins extend models, tools, agent strategies, endpoints, data sources and triggers; workflow templates and DSL are declarative; there are no plugin points for UI, theme or text. |
| MAL-14 Runtime isolation and dependency control | assessed | 3 |  |  | A |  | Plugins run in the separate plugin daemon, signatures are verified by default (FORCE_VERIFYING_SIGNATURE true) and outbound traffic goes through the SSRF proxy (docker/.env.example:222-236). |
| MAL-15 Developer loop | assessed | 2 | 3 |  | A |  | Plugin developers connect a local plugin to a running Dify instance for remote debugging through the daemon's install port (EXPOSE_PLUGIN_DAEMON_PORT, docker/.env.example:222), with logs; builders debug workflows step by step. Scored at the lower reading under rule 11 because: Remote debugging configuration was read from settings, not exercised. |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A |  | One model-provider interface maps many LLM vendors onto a canonical model API (api/core/model_manager.py, provider_manager.py); data-source plugins map external content into canonical documents and chunks. |
| MAL-17 Connector definition or SDK | assessed | 3 | 4 |  | A |  | Plugin SDK covers credential schemas and OAuth, triggers with subscriptions, data-source sync and install and upgrade lifecycle; admins install from the marketplace; signatures verify publishers. |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A |  | Service API is path-versioned (/v1) and documented; no deprecation windows or conflict handling. |
| MAL-19 Machine-readable capability surface for agents | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. Each app can be exposed as an MCP server with its input schema as the tool definition and a per-app server credential (api/controllers/mcp/mcp.py); Dify also consumes MCP tools. Scored at the lower reading under rule 11 because: No capability map for the platform as a whole. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. End users complete tasks conversationally in Dify apps grounded on knowledge bases with tool actions; builders get natural-language generators for prompts, code, structured output and workflow instructions (api/core/llm_generator/llm_generator.py:432-813). Scored at the lower reading under rule 11 because: Admin natural-language authoring covers parts of a workflow, not whole definitions. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A |  | Per-app statistics and workflow run logs update as runs happen (api/controllers/console/app/statistic.py, workflow_statistic.py); tracing to external LLM-ops tools (api/core/ops). |
| LRN-02 Structured learning signals | assessed | 2 | 3 |  | A |  | Message feedback (rating, content, source) is linked to messages and conversations (api/models/model.py:296-335) and triaged through logs and annotations; the link to the app configuration version was not verified. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A |  | End users like or dislike answers and the feedback is queryable per app (api/models/model.py:1299-1302); workflow runs record node errors. |
| LRN-04 Cross-source mining inside the product | assessed | 1 | 2 |  | A |  | App statistics combine usage and satisfaction for one app; no joined usage, support and delivery models. |
| LRN-05 Automated diagnosis | assessed | 1 | 2 |  | A |  | AI-qualified reading: 0. Run traces show node-level errors per run; there is no grouping. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 1 |  |  | A |  | AI-qualified reading: 0. Dashboards only; suggestions exist for conversation questions, not for software change. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 2 |  |  | A |  | AI-qualified reading: 0. Admins turn logged answers into annotations that the app reuses for similar questions (api/services/annotation_service.py); nothing proposes changes without being asked. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 |  |  | A |  | AI-qualified reading: not applicable. Annotations and app changes are applied by people without evaluation against a baseline. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 | 1 |  | A |  | Before-and-after comparison is possible by hand from statistics and traces; nothing binds a published version to a baseline and decision. Scored at the lower reading under rule 11 because: If manual comparison does not count as a mechanism. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 2 |  |  | A |  | Design system (packages/dify-ui) with accessibility lint rules (lint.config.ts) and an axe-based accessibility E2E workflow that runs on demand for a chosen page and WCAG level (.github/workflows/accessibility-e2e.yml:4-21). |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 1 | 2 |  | A |  | Per-feature logs only: authentication audit entities (api/services/entities/auth_audit_entities.py), app and workflow run logs; no generic audit store. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A |  | Account deletion service and scheduled message cleanup with retention settings (api/services/account_deletion_service.py, api/schedule/clean_messages.py); no data-subject export. |
| GOV-04 Security as infrastructure | assessed | 2 |  |  | A |  | RBAC resource and agent-access services (api/services/rbac_resource_service.py), SSRF proxy and plugin signature enforcement (FORCE_VERIFYING_SIGNATURE, docker/.env.example:236); no security scanning in CI. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A | I | Workflows keep numbered published versions (workflow_version_number_service); apps export versioned DSL; other surfaces are unversioned. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Surfaces other than workflows and app DSL are unversioned. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 |  |  | A |  | Draft and publish with debug preview for apps and workflows; no review step or proposal object. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 |  |  | A |  | Every publish is a manual human action; the agent runtime's ask-human layer (dify-agent/src/dify_agent/layers/ask_human/layer.py) gates agent actions, not changes. |
| GOV-08 Upgrade safety | assessed | 2 | 3 |  | A |  | Imported DSL is checked against the current DSL version and flagged when older or newer (api/services/dsl_version.py, app_dsl_service.py); plugins declare manifests and versions against a stable plugin SDK contract. Scored at the lower reading under rule 11 because: If version warnings on import do not count as automated compatibility checks. |
| GOV-09 Agent-safe actions | assessed | 2 |  |  | A |  | AI-qualified reading: 1. App-scoped API keys, OAuth and device-flow login (api/libs/oauth_bearer.py, api/services/oauth_device_flow.py), rate limits and per-call logs; no idempotency keys or dry-run. |
| GOV-10 Bounded self-change | not_applicable | excluded |  |  | - |  | AI-qualified reading: not applicable. No self-change path: AI drafts are saved by a person. |
| GOV-11 Learning-input integrity | not_applicable | excluded |  |  | - |  | AI-qualified reading: not applicable. No self-change path. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 |  |  | A |  | Kernel of tenants, accounts, apps, workflows, datasets, conversations and messages, tools and plugins, served over web, API, MCP and IM channels; no business-domain nouns. |
| EXP-02 A new domain is expressible without kernel change | assessed | 3 |  |  | A |  | Recommended apps and knowledge-pipeline templates ship domain solutions as app definitions, knowledge and tools on an unchanged kernel (api/constants/recommended_apps.json, pipeline_templates.json). |
| EXP-03 A domain ships as an installable bundle | assessed | 3 |  |  | A |  | App DSL export and import is a versioned bundle of app configuration, workflow graph, model settings and tool references (api/services/app_dsl_service.py, dsl_version.py), plus snippet DSL (snippet_dsl_service.py). |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A |  | No record of unmet intents was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 2 |  |  | A |  | Plugins from the marketplace are installed per workspace (api/services/plugin); no success metric or keep-or-kill record. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A |  | Knowledge bases with indexing, retrieval and citations (api/core/rag). |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 2 |  |  | A |  | Dataset permissions control which builders can attach knowledge (api/services/knowledge_retrieval_inner_service.py), but published apps retrieve with the app's datasets, not each end user's permissions. |
| AIR-05 Offline AI evaluation | assessed | 1 |  |  | A |  | Builders test prompts manually in debug and preview; no evaluation harness. |
| AIR-06 Regression gating before release | assessed | 1 |  |  | A |  | Publishing follows manual testing; nothing blocks a regression. |
| AIR-07 AI action tracing and auditability | assessed | 3 |  |  | A | IT | Every message and workflow run is logged with inputs, outputs, model, tokens and node and tool executions, viewable by builders, with optional Langfuse, LangSmith and other tracing (api/core/ops/ops_trace_manager.py). |
| AIR-01 Model and provider portability and resilience | assessed | 3 |  |  | A |  | Builders choose models per app from many providers; load balancing with cooldown fails over across credentials, with tests (api/core/model_manager.py:68-130, tests/unit_tests/services/test_model_load_balancing_service.py). |
| AIR-02 AI usage and per-customer cost controls | assessed | 3 |  |  | A |  | Token usage and cost recorded per message, credit usage and billing quota reservation per tenant (api/core/credit_usage.py, api/services/billing_service.py:77-89). |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 2 |  |  | A |  | End-user likes and dislikes and app statistics (satisfaction, tokens) per app (api/models/model.py:1299-1302); no drift alerts. |

Facets: I implemented, T tested, O operated.
