# Dify: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the dify monorepo (api, web, dify-agent runtime, packages, CLI, docker configuration, CI). The separately released dify-sandbox and plugin-daemon services are assessed through their configuration here. Dify Cloud and the plugin marketplace catalogue are out of scope.

## Reading

**Strongest:** isolation and bundles. Code runs in a separate sandbox behind a forced SSRF proxy, plugins run in a daemon with signature checks, and apps export as versioned DSL (D3 3, I2 3, O3 3). **Learning (1.6):** admins turn logged answers into annotations the app reuses (P1 2), but nothing evaluates changes against a baseline (P2 1), and publishing has no policy gate (F3 1).

## Limits

Repository evidence only, main at the tip named above. dify-sandbox and plugin-daemon are separate repositories; their behaviour was taken from configuration here and not read in source. Dify Cloud and enterprise editions are out of scope. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main). Archetype **configurable-application-platform**.

Coverage: 49 assessed, 0 not evidenced, 0 not applicable. Grades: 49 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.5 | mechanism | 2.3–2.8 | 2.5 | 2.5 | 2.5 |
| governance | 1.9 | mechanism | 1.8–2.1 | 1.9 | 1.9 | 1.9 |
| learning | 1.6 | mechanism | 1.5–1.8 | 1.6 | 1.6 | 1.6 |
| factory | 2.3 | mechanism | 2.2–2.5 | 2.3 | 2.3 | 2.3 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.4 | 2.4 |
| Governance | 1.9 | 1.9 |
| Learning | 1.6 | 1.6 |
| Factory | 2.3 | 2.3 |
| Agent Interface | 2.7 | 2.7 |
| Extension Surface | 2.7 | 2.7 |
| Operational Scalability | 1.3 | 1.3 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 2 pass | 2 pass |
| propose | M1, P1 | 2 | 2 pass | 2 pass |
| review | F2 | 2 | 2 pass | 2 pass |
| gate | F3 | 3 | 1 fail | 1 fail |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 1 fail | 1 fail |
| verify | L1 | 2 | 2 pass | 2 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| A Entity and schema as data | 1.3 |
| B API surface generation | 3.0 |
| C Rendering follows the definition | 2.0 |
| D Behaviour as data | 2.7 |
| E Compliance and security as infrastructure | 1.8 |
| F Change control | 2.0 |
| G Performance under genericity | 1.3 |
| H Stack flexibility and verification | 2.7 |
| I Extension ecosystem | 2.7 |
| J Observe | 2.0 |
| K Agent and conversational readiness | 2.7 |
| L Factory surfaces | 2.0 |
| M Advise and act | 1.3 |
| N Integration and connector extensibility | 2.7 |
| O Adjacent-domain expansion | 3.0 |
| P Learn from experience | 1.5 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | assessed | 1 | 2 |  | A | Entity kinds (apps, workflows, datasets, tools) are fixed models (api/models); new kinds need code, migration and release. |
| A2 Field definitions carry type and validation | assessed | 2 |  |  | A | Knowledge-base documents carry user-defined typed metadata fields (DatasetMetadata, api/models/dataset.py); app input variables are typed with validation. No privacy tag; one entity family. |
| A3 Relationships and lifecycle states declarable | assessed | 1 |  |  | A | Relations and lifecycle states are coded per feature (draft and published workflows, document indexing states). |
| B1 API per entity is generic or generated | assessed | 3 | 2 |  | A | Every app gets the same generated service API shaped by its input variables (api/controllers/service_api), plus an OpenAPI surface (api/controllers/openapi, fastopenapi.py); no per-app code. |
| B2 API reshapes at runtime from definitions | assessed | 3 |  |  | A | Publishing a new workflow version changes the app's API inputs and outputs live (api/services/workflow_service.py version handling). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 3 | 2 |  | A | Generated OpenAPI documents (api/controllers/openapi, API_SCHEMA_GUIDE.md), typed SDKs (sdks/) and structured errors. No dry-run. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 2 |  |  | A | Workflow canvases and each app's web-app settings (branding, opening statement, suggested questions) are data edited by builders; there is no page layout editor. |
| C2 Generic list, detail and intake widgets from definition plus view spec | assessed | 2 | 3 |  | A | Chat, completion and workflow web apps render intake forms generically from each app's typed input variables; list and detail views are hand-built. |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 | 3 |  | A | Design-system themes (packages/dify-ui/src/themes) and 1,401 locale files, with AI translation in CI (.github/workflows/translate-i18n-claude.yml); no tenant theme editor or text overrides. |
| D1 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A | Workflows and chatflows compose triggers (schedule, webhook, plugin triggers in api/core/trigger), conditions, iteration, code, HTTP, tool and LLM nodes in the UI; debug preview and single-step runs; draft and published versions. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A | Inbound webhook and plugin triggers with per-node retry settings and run logs; Dify does not publish its own entity lifecycle events to subscribers. |
| D3 Sandboxed server-side hooks | assessed | 3 |  |  | A | Code nodes run in the separate dify-sandbox service with a worker timeout (SANDBOX_WORKER_TIMEOUT 15) and all network traffic forced through the SSRF proxy (SANDBOX_HTTP_PROXY, docker/.env.example:193-201, api/core/helper/ssrf_proxy.py); triggered by workflow events and requests. |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 2 |  |  | A | Design system (packages/dify-ui) with accessibility lint rules (lint.config.ts) and an axe-based accessibility E2E workflow that runs on demand for a chosen page and WCAG level (.github/workflows/accessibility-e2e.yml:4-21). |
| E2 Audit generic over entities, definition changes and approvals | assessed | 1 | 2 |  | A | Per-feature logs only: authentication audit entities (api/services/entities/auth_audit_entities.py), app and workflow run logs; no generic audit store. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A | Account deletion service and scheduled message cleanup with retention settings (api/services/account_deletion_service.py, api/schedule/clean_messages.py); no data-subject export. |
| E4 Security as infrastructure | assessed | 2 |  |  | A | RBAC resource and agent-access services (api/services/rbac_resource_service.py), SSRF proxy and plugin signature enforcement (FORCE_VERIFYING_SIGNATURE, docker/.env.example:236); no security scanning in CI. |
| F1 Definitions and layouts versioned with rollback | assessed | 2 | 3 |  | A | Workflows keep numbered published versions (workflow_version_number_service); apps export versioned DSL; other surfaces are unversioned. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 2 |  |  | A | Draft and publish with debug preview for apps and workflows; no review step or proposal object. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 |  |  | A | Every publish is a manual human action; the agent runtime's ask-human layer (dify-agent/src/dify_agent/layers/ask_human/layer.py) gates agent actions, not changes. |
| F4 Upgrade safety | assessed | 3 | 2 |  | A | Imported DSL is checked against the current DSL version and flagged when older or newer (api/services/dsl_version.py, app_dsl_service.py); plugins declare manifests and versions against a stable plugin SDK contract. |
| G1 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A | Knowledge bases get vector and keyword indexes configured per dataset (api/core/rag); application lists use SQL with Redis caching. |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | Multi-tenant workspaces with per-app and per-tenant rate limits (api/libs/helper.py) and plan quotas; no noisy-neighbour detection. |
| G3 Ceilings measured, not discovered in incidents | assessed | 0 | 1 |  | A | No load or performance suite and no documented limits found (searched for k6, locust, benchmark and load test). |
| H1 Layers deploy independently | assessed | 3 |  |  | A | API, worker, web, sandbox, plugin daemon, SSRF proxy and agent runtime are separate containers with separate deploy workflows (9 Dockerfiles; .github/workflows/deploy-agent.yml, deploy-knowledge.yml). |
| H2 Module boundaries enforced by tooling | assessed | 3 | 2 |  | A | import-linter layer contracts for the backend (api/.importlinter:1-20) plus ESLint configuration for the frontend. |
| H3 Every change class has an automated pre-land check | assessed | 2 |  |  | A | Main CI on pull requests with no draft filter runs API tests, web tests, style, migration and bundle-size checks (.github/workflows/main-ci.yml, db-migration-test.yml, web-bundle-size.yml); accessibility runs only on demand and there is no security scan. |
| I1 Plugin lane breadth | assessed | 2 | 3 |  | A | Plugins extend models, tools, agent strategies, endpoints, data sources and triggers; workflow templates and DSL are declarative; there are no plugin points for UI, theme or text. |
| I2 Runtime isolation and dependency control | assessed | 3 |  |  | A | Plugins run in the separate plugin daemon, signatures are verified by default (FORCE_VERIFYING_SIGNATURE true) and outbound traffic goes through the SSRF proxy (docker/.env.example:222-236). |
| I3 Developer loop | assessed | 3 | 2 |  | A | Plugin developers connect a local plugin to a running Dify instance for remote debugging through the daemon's install port (EXPOSE_PLUGIN_DAEMON_PORT, docker/.env.example:222), with logs; builders debug workflows step by step. |
| K1 Machine-readable capability surface for agents | assessed | 3 | 2 |  | A | Each app can be exposed as an MCP server with its input schema as the tool definition and a per-app server credential (api/controllers/mcp/mcp.py); Dify also consumes MCP tools. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 2 |  | A | End users complete tasks conversationally in Dify apps grounded on knowledge bases with tool actions; builders get natural-language generators for prompts, code, structured output and workflow instructions (api/core/llm_generator/llm_generator.py:432-813). |
| K3 Agent-safe actions | assessed | 2 |  |  | A | App-scoped API keys, OAuth and device-flow login (api/libs/oauth_bearer.py, api/services/oauth_device_flow.py), rate limits and per-call logs; no idempotency keys or dry-run. |
| N1 Canonical data model with a mapping layer | assessed | 3 |  |  | A | One model-provider interface maps many LLM vendors onto a canonical model API (api/core/model_manager.py, provider_manager.py); data-source plugins map external content into canonical documents and chunks. |
| N2 Connector definition or SDK | assessed | 3 | 4 |  | A | Plugin SDK covers credential schemas and OAuth, triggers with subscriptions, data-source sync and install and upgrade lifecycle; admins install from the marketplace; signatures verify publishers. |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | Service API is path-versioned (/v1) and documented; no deprecation windows or conflict handling. |
| O1 Kernel concepts are domain-neutral | assessed | 3 |  |  | A | Kernel of tenants, accounts, apps, workflows, datasets, conversations and messages, tools and plugins, served over web, API, MCP and IM channels; no business-domain nouns. |
| O2 A new domain is expressible without kernel change | assessed | 3 |  |  | A | Recommended apps and knowledge-pipeline templates ship domain solutions as app definitions, knowledge and tools on an unchanged kernel (api/constants/recommended_apps.json, pipeline_templates.json). |
| O3 A domain ships as an installable bundle | assessed | 3 |  |  | A | App DSL export and import is a versioned bundle of app configuration, workflow graph, model settings and tool references (api/services/app_dsl_service.py, dsl_version.py), plus snippet DSL (snippet_dsl_service.py). |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 |  |  | A | Per-app statistics and workflow run logs update as runs happen (api/controllers/console/app/statistic.py, workflow_statistic.py); tracing to external LLM-ops tools (api/core/ops). |
| J2 Structured learning signals | assessed | 2 | 3 |  | A | Message feedback (rating, content, source) is linked to messages and conversations (api/models/model.py:296-335) and triaged through logs and annotations; the link to the app configuration version was not verified. |
| J3 Cross-source mining inside the product | assessed | 1 | 2 |  | A | App statistics combine usage and satisfaction for one app; no joined usage, support and delivery models. |
| M1 Ranked, evidence-backed proposals for change | assessed | 1 |  |  | A | Dashboards only; suggestions exist for conversation questions, not for software change. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 2 |  |  | A | AI generators for code, prompts, structured output and workflow instructions assist builders one step at a time (api/core/llm_generator). |
| M4 Post-change impact is measured against a declared baseline | assessed | 1 | 0 |  | A | Before-and-after comparison is possible by hand from statistics and traces; nothing binds a published version to a baseline and decision. |
| P1 The product turns its own operating experience into candidate changes | assessed | 2 |  |  | A | Admins turn logged answers into annotations that the app reuses for similar questions (api/services/annotation_service.py); nothing proposes changes without being asked. |
| P2 Learned changes are validated before they take effect | assessed | 1 |  |  | A | Annotations and app changes are applied by people without evaluation against a baseline. |
| L1 Verification surface | assessed | 2 |  |  | A | /console/api/version and /console/api/ping (api/controllers/console/system.py:27-37) and a worker health check (api/celery_healthcheck.py); no configuration snapshot. |
| L2 Environment reproducibility | assessed | 2 | 3 |  | A | Docker Compose stack, seeded E2E runs (e2e/scripts/seed-runner.ts) and branch-triggered dev deploys (.github/workflows/deploy-dev.yml); no per-change ephemeral environment. |
| L3 Machine verifiability | assessed | 2 |  |  | A | Web and CLI E2E suites (.github/workflows/web-e2e.yml, cli-e2e.yml); no changed-path map or adoption instrumentation at ship. |

