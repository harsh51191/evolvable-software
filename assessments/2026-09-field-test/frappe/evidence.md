# Frappe Framework evidence

Read at github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **3** (grade A). Sites outside developer mode can create DocTypes with custom=1 in Desk (check_developer_mode, frappe/core/doctype/doctype/doctype.py:329-340); on_update calls frappe.db.updatedb to create or alter the table automatically (doctype.py:539-546). No deploy. No dry-run or policy gate, so not 4.
- **A2 Field definitions carry type and validation**: **3** (grade A). DocField carries fieldtype, reqd, length, unique, non_negative, min_value, max_value, options-based validation, mandatory_depends_on and a mask flag (frappe/core/doctype/docfield/docfield.json); admins add typed fields through Customize Form and Custom Field. mask is consumed by read paths (frappe/model/meta.py:207, frappe/model/db_query.py:35, frappe/desk/form/load.py:295). Personal-data scope for erasure is declared in code (user_data_fields, frappe/hooks.py:360), not per field, so not 4.
- **A3 Relationships and lifecycle states declarable**: **4** (grade A). Link, Dynamic Link and Table fields declare relations and Workflow DocTypes declare states and transitions in the UI (frappe/workflow/doctype/); the platform enforces transitions (frappe/model/workflow.py:119-246) and link integrity (frappe/model/delete_doc.py:414); both are creatable through the REST API with validation errors, which meets the rubric's definition of AI-authorable.
  - Alternate reading 3: If AI-authorable is read as needing an AI authoring feature.
## B API surface generation

- **B1 API per entity is generic or generated**: **3** (grade A). One generic document API serves every DocType: frappe/api/v2.py read_doc, document_list with fields and filters, create_doc, update_doc, delete_doc, get_meta (lines 84-245), plus frappe/api/v1.py. No per-type controllers.
  - Alternate reading 4: Projections, filters and validation already derive from the definition at runtime; only 'typed' is missing.
- **B2 API reshapes at runtime from definitions**: **3** (grade A). Meta is loaded and cached at runtime (frappe/model/meta.py); a new or changed DocType is served by /api/resource and /api/v2 immediately on save. No per-consumer schema versions or dry-run.
- **B3 Machine-readable contract with introspection and dry-run**: **2** (grade A). Introspection through get_meta (frappe/api/v2.py:245) and getdoctype (frappe/desk/form/load.py); Python type stubs generated from definitions (frappe/types/exporter.py). No OpenAPI, no external typed client generation; errors carry exc_type but no field-level schema.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **3** (grade A). Form layout (tab, section and column breaks) is DocType data, overridable per site through Customize Form and DocType Layout (frappe/core/doctype/doctype_layout); Workspace, Web Page, Web Form and Print Format are admin builders with previews (frappe/desk/doctype/workspace, frappe/website/doctype/web_page, frappe/printing/doctype/print_format). A site is the tenant unit.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **3** (grade A). Every DocType gets generic list, report, kanban, calendar, form and quick-entry views rendered from its definition (frappe/public/js/frappe/list, form, views); admins configure List View Settings (frappe/desk/doctype/list_view_settings) and saved report views. No inherited accessibility guarantee, so not 4.
- **C3 Theme tokens and text are data with tenant overrides**: **3** (grade A). Per-site text overrides through the Translation DocType (frappe/core/doctype/translation); locale pipeline through Crowdin workflows (.github/workflows/crowdin-actions-*.yml); Website Theme DocType edits website styling (frappe/website/doctype/website_theme).
  - Alternate reading 2: The admin theme editor covers the website only; the Desk application UI offers light and dark modes, not tenant tokens.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **3** (grade A). Automation Flow, Action and Run DocTypes (frappe/automation/doctype) on an engine exposing get_automation_capabilities, validate_action_params and run_manually (frappe/automation_engine/api.py); trial runs simulate wait steps (frappe/automation_engine/tests/test_trial_run.py:115-152); Notification preview_meets_condition (frappe/email/doctype/notification/notification.py:98). Covers custom DocTypes.
  - Alternate reading 4: Capabilities are machine-readable and trial runs exist; versioning of flows and AI authoring are not evidenced.
- **D2 Event model with webhooks or subscriptions and retry**: **3** (grade A). Admin-configured Webhook per DocType event with conditions, headers and data mapping (frappe/integrations/doctype/webhook), delivery log (webhook_request_log) and scheduled retries with max_retries (retry_failed_webhooks, test_webhook.py:339-354); durable automation trigger queue with retention (frappe/automation_engine/drainer.py:291, settings.py:18). No replay.
- **D3 Sandboxed server-side hooks**: **3** (grade A). Server Script runs under RestrictedPython with allowlisted globals (frappe/utils/safe_exec.py:15-17, 95), triggered by DocType events, API calls, scheduler and permission queries, authored by System Managers when server_script_enabled is set (safe_exec.py:48); outbound requests limited to globally routable http(s) hosts with timeouts (safe_exec.py:372-400, 486). Execution time is bounded only by the worker. No per-hook test harness, so not 4.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). A UI kit with tokens exists (ui/, frappe/public/scss) but no automated accessibility scanning was found in CI or tests (no axe, pa11y, jsx-a11y or vuejs-accessibility in the tree).
  - Alternate reading 2: The kit-and-tokens half of level 2 is present; the anchors bundle kit and scans, so kit-without-scans fits neither level.
- **E2 Audit generic over entities, definition changes and approvals**: **2** (grade A). Version records field-level changes for DocTypes with track_changes (frappe/core/doctype/doctype/doctype.py:181); Audit Trail compares versions (frappe/core/doctype/audit_trail); Activity, Access, API Request and Permission logs exist; retention through Log Settings (frappe/core/doctype/log_settings/log_settings.py:80-86). Coverage is opt-in per DocType; not tamper-evident.
  - Alternate reading 3: Admin UI, retention and config and permission logs exist; only the 'all entities' clause fails because tracking is opt-in.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Personal Data Download and Deletion Requests cover every DocType declared in user_data_fields hooks (frappe/hooks.py:360, frappe/website/doctype/personal_data_deletion_request). The declaration is app code, not a field-level tag; retention exists for logs only.
  - Alternate reading 3: Erasure is generic across entities; the only gap is that coverage comes from a code hook instead of a tag in the definition.
- **E4 Security as infrastructure**: **3** (grade A). Role permissions are part of every DocType definition (DocPerm, Custom DocPerm, user permissions, permlevels, mask); field validation is generic; semgrep runs on every pull request (.github/workflows/linters.yml:67-72) and Dependabot is configured (.github/dependabot.yml). Whether the check blocks merge is a branch-protection setting not visible in the repository.
  - Alternate reading 2: If 'gates every change' needs visible proof that the scan blocks merges.
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Document changes are versioned with diffs (Version, Audit Trail); deleted documents can be restored (frappe/core/doctype/deleted_document/deleted_document.py:43). No revert-to-version for definitions, layouts or configuration.
- **F2 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Customisations move between sites as exported fixtures or Package Releases (frappe/core/doctype/package_release/package_release.py:79-96), an engineer-run stage-and-publish flow. No proposal object with preview.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A). Every definition change is made directly by a person holding the right role; no policy object and no auto-apply classes.
- **F4 Upgrade safety**: **2** (grade A). Customisations live in separate layers (Custom Field, Property Setter, Client Script, Server Script) that survive bench migrate while standard DocTypes resync; frappe/patches.txt carries migrations. No automated compatibility check of customisations against the next release.
  - Alternate reading 3: Customisations are confined to stable layers and migration tooling exists; only automated compatibility checks are missing.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **3** (grade A). Each DocType has its own table, so there is no generic store; DocField.search_index creates database indexes from the definition; lists run through indexed SQL (frappe/model/db_query.py) with Redis meta and document caches; global search table (frappe/utils/global_search.py).
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Multi-site benches give each site its own database; per-site request rate limiting (frappe/rate_limiter.py:16-18). No noisy-neighbour detection or isolation verification in the repository.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). frappe/tests/test_perf.py and frappe/tests/microbenchmarks exist; no documented per-surface limits or CI budgets.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **1** (grade A). One Python and JavaScript codebase deployed as a bench (web, workers, scheduler and realtime share the artifact); container images live in a separate repository.
- **H2 Module boundaries enforced by tooling**: **1** (grade A). Module boundaries are convention; no architectural lint or dependency-graph enforcement found.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Server tests, Cypress UI tests, linters with semgrep and a bundle-size check run on every pull request with no draft skip (.github/workflows/server-tests.yml, ui-tests.yml, linters.yml, default-js-bundle-size.yml). No accessibility check.
  - Alternate reading 3: Every code change class except accessibility has a pre-land check and drafts are included.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Code apps through hooks (hooks.md, frappe/hooks.py) plus declarative layers: Custom Field, Property Setter, Client Script, Server Script, Custom HTML Block, Web Template, Print Format, Workspace, Translation.
- **I2 Runtime isolation and dependency control**: **2** (grade A). Server Scripts run in-process under RestrictedPython allowlists with request egress control (frappe/utils/safe_exec.py); installed apps and client scripts run with full trust.
  - Alternate reading 1: If the criterion is read for third-party apps, which run with full trust.
- **I3 Developer loop**: **2** (grade A). bench developer mode, System Console (frappe/desk/doctype/system_console), Recorder and Error Log support local and on-site iteration; no staged branches or preview against a tenant in the repository.
  - Alternate reading 3: System Console and Recorder already give validators and logs against a live site.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **2** (grade A). Introspectable meta (get_meta) and automation capability APIs (frappe/automation_engine/api.py); no MCP server or tool surface in the repository.
- **K2 Conversational operability for users and natural-language authoring for operators**: **0** (grade A). No member-facing assistant or natural-language authoring in the repository (searched for assistant, chat, LLM and copilot features; hits are developer docs only: AGENTS.md, ui/CLAUDE.md).
- **K3 Agent-safe actions**: **2** (grade A). Per-user API key and secret (frappe/core/doctype/user/user.json:600-620), OAuth scopes (frappe/integrations/doctype/oauth_scope), API Request Log, rate limiting (frappe/rate_limiter.py). No idempotency keys or dry-run.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **1** (grade A). Integrations (Google Calendar and Contacts, LDAP, Connected App) are bespoke modules (frappe/integrations/doctype); Data Import value mapping covers imports only.
  - Alternate reading 2: Webhook data mapping and import mapping are configurable mapping layers for narrow flows.
- **N2 Connector definition or SDK**: **2** (grade A). Connected App is an admin-configured generic OAuth2 client and Integration Request logs calls (frappe/integrations/doctype/connected_app, integration_request); no connector SDK covering sync and lifecycle.
- **N3 Stable versioned contracts**: **2** (grade A). Path-versioned APIs (frappe/api/v1.py, frappe/api/v2.py); no deprecation policy, idempotent sync or conflict handling found.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **4** (grade A). Kernel is User, Role, DocPerm, DocType, File, Communication, Workflow, Notification and Email Account; domains live in separate apps (README.md:22-32 names ERPNext); kernel objects are themselves DocTypes customisable through the same definitions (DocType is a DocType).
  - Alternate reading 3: If 'configurable definitions' requires more than kernel objects being customisable DocTypes.
- **O2 A new domain is expressible without kernel change**: **3** (grade B). README.md:22-32 states ERPNext was built on the framework; several domains ship as separate apps on an unchanged kernel. Those apps contain code as well as definitions; a domain can also be built from custom DocTypes, workflows and server scripts alone.
  - Alternate reading 4: Multiple domains already ship as installable bundles with the kernel unchanged, if code-carrying apps count as bundles.
- **O3 A domain ships as an installable bundle**: **3** (grade A). Package, Package Release and Package Import DocTypes export and install versioned bundles of DocTypes, scripts and other customisations (frappe/core/doctype/package, package_release, package_import).
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). Route History, Activity Log and Access Log are written to the site database as events happen and are read by product features (frappe/desk/doctype/route_history); vendor telemetry through pulse and PostHog (frappe/utils/telemetry).
  - Alternate reading 2: Only navigation and access events are near-real-time; there is no general per-feature event stream.
- **J2 Structured learning signals**: **1** (grade A). No typed feedback or rating objects; Error Log links errors to reference documents but not to the definition version.
  - Alternate reading 2: Error Log entries are typed signals linked to documents.
- **J3 Cross-source mining inside the product**: **1** (grade A). DuckDB Sync copies DocType data for analytics (frappe/core/doctype/duckdb_sync) and reports can join DocTypes, but nothing joins usage, support and delivery data or mines them.
  - Alternate reading 2: In-product reporting over the site database is a partial join of sources.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **2** (grade A). The Recorder's query optimiser proposes database indexes from recorded queries (frappe/core/doctype/recorder/db_optimizer.py:242, recorder.py:159): evidence-backed recommendations for one area.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **0** (grade A). No AI authoring lane in the repository.
- **M4 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
  - Alternate reading 1: The Recorder supports ad hoc before-and-after checks.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **2** (grade A). The Recorder proposes database indexes from recorded queries when a person runs it (frappe/core/doctype/recorder/db_optimizer.py:242); nothing proposes changes without being asked.
- **P2 Learned changes are validated before they take effect**: **1** (grade A). Suggested changes are applied by a person; there is no automated evaluation.
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). frappe.ping (frappe/__init__.py:1478) and get_versions (frappe/utils/change_log.py:105); System Health Report DocType; no deployed-configuration snapshot endpoint.
- **L2 Environment reproducibility**: **2** (grade A). bench new-site and CI create fresh sites with test records per run (.github/workflows/server-tests.yml); no per-change ephemeral environment and no feature flags.
  - Alternate reading 3: CI already builds a seeded, disposable site per change.
- **L3 Machine verifiability**: **2** (grade A). Cypress journeys (cypress/integration) and server tests; no changed-path to journey map or adoption instrumentation at ship.
