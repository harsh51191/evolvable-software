# Dify evidence

Read at github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **1** (grade A). Entity kinds (apps, workflows, datasets, tools) are fixed models (api/models); new kinds need code, migration and release.
  - Alternate reading 2: Apps and datasets behave like runtime-defined entities, though of fixed kinds.
- **A2 Field definitions carry type and validation**: **2** (grade A). Knowledge-base documents carry user-defined typed metadata fields (DatasetMetadata, api/models/dataset.py); app input variables are typed with validation. No privacy tag; one entity family.
- **A3 Relationships and lifecycle states declarable**: **1** (grade A). Relations and lifecycle states are coded per feature (draft and published workflows, document indexing states).
## B API surface generation

- **B1 API per entity is generic or generated**: **3** (grade A). Every app gets the same generated service API shaped by its input variables (api/controllers/service_api), plus an OpenAPI surface (api/controllers/openapi, fastopenapi.py); no per-app code.
  - Alternate reading 2: Apps are a single entity family, not arbitrary defined types.
- **B2 API reshapes at runtime from definitions**: **3** (grade A). Publishing a new workflow version changes the app's API inputs and outputs live (api/services/workflow_service.py version handling).
- **B3 Machine-readable contract with introspection and dry-run**: **3** (grade A). Generated OpenAPI documents (api/controllers/openapi, API_SCHEMA_GUIDE.md), typed SDKs (sdks/) and structured errors. No dry-run.
  - Alternate reading 2: Coverage of the whole API by the generated spec was not verified.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Workflow canvases and each app's web-app settings (branding, opening statement, suggested questions) are data edited by builders; there is no page layout editor.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **2** (grade A). Chat, completion and workflow web apps render intake forms generically from each app's typed input variables; list and detail views are hand-built.
  - Alternate reading 3: Intake is fully generic and logs and annotations views are generic across apps.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). Design-system themes (packages/dify-ui/src/themes) and 1,401 locale files, with AI translation in CI (.github/workflows/translate-i18n-claude.yml); no tenant theme editor or text overrides.
  - Alternate reading 3: The locale pipeline includes AI translation.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **3** (grade A). Workflows and chatflows compose triggers (schedule, webhook, plugin triggers in api/core/trigger), conditions, iteration, code, HTTP, tool and LLM nodes in the UI; debug preview and single-step runs; draft and published versions.
  - Alternate reading 4: Versioned, testable and partly AI-assisted (generate_workflow_instruction_suggestions), but not simulatable against history.
- **D2 Event model with webhooks or subscriptions and retry**: **2** (grade A). Inbound webhook and plugin triggers with per-node retry settings and run logs; Dify does not publish its own entity lifecycle events to subscribers.
- **D3 Sandboxed server-side hooks**: **3** (grade A). Code nodes run in the separate dify-sandbox service with a worker timeout (SANDBOX_WORKER_TIMEOUT 15) and all network traffic forced through the SSRF proxy (SANDBOX_HTTP_PROXY, docker/.env.example:193-201, api/core/helper/ssrf_proxy.py); triggered by workflow events and requests.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **2** (grade A). Design system (packages/dify-ui) with accessibility lint rules (lint.config.ts) and an axe-based accessibility E2E workflow that runs on demand for a chosen page and WCAG level (.github/workflows/accessibility-e2e.yml:4-21).
- **E2 Audit generic over entities, definition changes and approvals**: **1** (grade A). Per-feature logs only: authentication audit entities (api/services/entities/auth_audit_entities.py), app and workflow run logs; no generic audit store.
  - Alternate reading 2: Run logs are generic across apps.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Account deletion service and scheduled message cleanup with retention settings (api/services/account_deletion_service.py, api/schedule/clean_messages.py); no data-subject export.
- **E4 Security as infrastructure**: **2** (grade A). RBAC resource and agent-access services (api/services/rbac_resource_service.py), SSRF proxy and plugin signature enforcement (FORCE_VERIFYING_SIGNATURE, docker/.env.example:236); no security scanning in CI.
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Workflows keep numbered published versions (workflow_version_number_service); apps export versioned DSL; other surfaces are unversioned.
  - Alternate reading 3: Apps and workflows are the main customisation surfaces.
- **F2 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Draft and publish with debug preview for apps and workflows; no review step or proposal object.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A). Every publish is a manual human action; the agent runtime's ask-human layer (dify-agent/src/dify_agent/layers/ask_human/layer.py) gates agent actions, not changes.
- **F4 Upgrade safety**: **3** (grade A). Imported DSL is checked against the current DSL version and flagged when older or newer (api/services/dsl_version.py, app_dsl_service.py); plugins declare manifests and versions against a stable plugin SDK contract.
  - Alternate reading 2: If version warnings on import do not count as automated compatibility checks.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **2** (grade A). Knowledge bases get vector and keyword indexes configured per dataset (api/core/rag); application lists use SQL with Redis caching.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Multi-tenant workspaces with per-app and per-tenant rate limits (api/libs/helper.py) and plan quotas; no noisy-neighbour detection.
  - Alternate reading 3: Per-tenant limits are present throughout.
- **G3 Ceilings measured, not discovered in incidents**: **0** (grade A). No load or performance suite and no documented limits found (searched for k6, locust, benchmark and load test).
  - Alternate reading 1: Vector-database test suites exercise one surface.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **3** (grade A). API, worker, web, sandbox, plugin daemon, SSRF proxy and agent runtime are separate containers with separate deploy workflows (9 Dockerfiles; .github/workflows/deploy-agent.yml, deploy-knowledge.yml).
- **H2 Module boundaries enforced by tooling**: **3** (grade A). import-linter layer contracts for the backend (api/.importlinter:1-20) plus ESLint configuration for the frontend.
  - Alternate reading 2: Whether the import-linter contract runs as a required CI check was not verified.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Main CI on pull requests with no draft filter runs API tests, web tests, style, migration and bundle-size checks (.github/workflows/main-ci.yml, db-migration-test.yml, web-bundle-size.yml); accessibility runs only on demand and there is no security scan.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **2** (grade A). Plugins extend models, tools, agent strategies, endpoints, data sources and triggers; workflow templates and DSL are declarative; there are no plugin points for UI, theme or text.
  - Alternate reading 3: Breadth across server surfaces is large.
- **I2 Runtime isolation and dependency control**: **3** (grade A). Plugins run in the separate plugin daemon, signatures are verified by default (FORCE_VERIFYING_SIGNATURE true) and outbound traffic goes through the SSRF proxy (docker/.env.example:222-236).
- **I3 Developer loop**: **3** (grade A). Plugin developers connect a local plugin to a running Dify instance for remote debugging through the daemon's install port (EXPOSE_PLUGIN_DAEMON_PORT, docker/.env.example:222), with logs; builders debug workflows step by step.
  - Alternate reading 2: Remote debugging configuration was read from settings, not exercised.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **3** (grade A). Each app can be exposed as an MCP server with its input schema as the tool definition and a per-app server credential (api/controllers/mcp/mcp.py); Dify also consumes MCP tools.
  - Alternate reading 2: No capability map for the platform as a whole.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). End users complete tasks conversationally in Dify apps grounded on knowledge bases with tool actions; builders get natural-language generators for prompts, code, structured output and workflow instructions (api/core/llm_generator/llm_generator.py:432-813).
  - Alternate reading 2: Admin natural-language authoring covers parts of a workflow, not whole definitions.
- **K3 Agent-safe actions**: **2** (grade A). App-scoped API keys, OAuth and device-flow login (api/libs/oauth_bearer.py, api/services/oauth_device_flow.py), rate limits and per-call logs; no idempotency keys or dry-run.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). One model-provider interface maps many LLM vendors onto a canonical model API (api/core/model_manager.py, provider_manager.py); data-source plugins map external content into canonical documents and chunks.
- **N2 Connector definition or SDK**: **3** (grade A). Plugin SDK covers credential schemas and OAuth, triggers with subscriptions, data-source sync and install and upgrade lifecycle; admins install from the marketplace; signatures verify publishers.
  - Alternate reading 4: Signature verification is a form of certification.
- **N3 Stable versioned contracts**: **2** (grade A). Service API is path-versioned (/v1) and documented; no deprecation windows or conflict handling.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of tenants, accounts, apps, workflows, datasets, conversations and messages, tools and plugins, served over web, API, MCP and IM channels; no business-domain nouns.
- **O2 A new domain is expressible without kernel change**: **3** (grade A). Recommended apps and knowledge-pipeline templates ship domain solutions as app definitions, knowledge and tools on an unchanged kernel (api/constants/recommended_apps.json, pipeline_templates.json).
- **O3 A domain ships as an installable bundle**: **3** (grade A). App DSL export and import is a versioned bundle of app configuration, workflow graph, model settings and tool references (api/services/app_dsl_service.py, dsl_version.py), plus snippet DSL (snippet_dsl_service.py).
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). Per-app statistics and workflow run logs update as runs happen (api/controllers/console/app/statistic.py, workflow_statistic.py); tracing to external LLM-ops tools (api/core/ops).
- **J2 Structured learning signals**: **2** (grade A). Message feedback (rating, content, source) is linked to messages and conversations (api/models/model.py:296-335) and triaged through logs and annotations; the link to the app configuration version was not verified.
  - Alternate reading 3: Messages record the app configuration they ran with.
- **J3 Cross-source mining inside the product**: **1** (grade A). App statistics combine usage and satisfaction for one app; no joined usage, support and delivery models.
  - Alternate reading 2: Satisfaction joins feedback and usage for each app.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **1** (grade A). Dashboards only; suggestions exist for conversation questions, not for software change.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **2** (grade A). AI generators for code, prompts, structured output and workflow instructions assist builders one step at a time (api/core/llm_generator).
- **M4 Post-change impact is measured against a declared baseline**: **1** (grade A). Before-and-after comparison is possible by hand from statistics and traces; nothing binds a published version to a baseline and decision.
  - Alternate reading 0: If manual comparison does not count as a mechanism.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **2** (grade A). Admins turn logged answers into annotations that the app reuses for similar questions (api/services/annotation_service.py); nothing proposes changes without being asked.
- **P2 Learned changes are validated before they take effect**: **1** (grade A). Annotations and app changes are applied by people without evaluation against a baseline.
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). /console/api/version and /console/api/ping (api/controllers/console/system.py:27-37) and a worker health check (api/celery_healthcheck.py); no configuration snapshot.
- **L2 Environment reproducibility**: **2** (grade A). Docker Compose stack, seeded E2E runs (e2e/scripts/seed-runner.ts) and branch-triggered dev deploys (.github/workflows/deploy-dev.yml); no per-change ephemeral environment.
  - Alternate reading 3: E2E runs create seeded, disposable instances per change.
- **L3 Machine verifiability**: **2** (grade A). Web and CLI E2E suites (.github/workflows/web-e2e.yml, cli-e2e.yml); no changed-path map or adoption instrumentation at ship.
