# Frappe Framework evidence

Read at github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Every site keeps documents in MariaDB or PostgreSQL and files on disk.
- **schema_changes**: true. Creating or editing a DocType alters its table at runtime (frappe/database/schema.py:479-485), and bench migrate applies patches (frappe/patches.txt).
- **multi_tenant**: true. One bench serves several sites, each with its own database (multi-site benches).
- **hosted_service**: true. Gunicorn web workers, RQ workers, a scheduler and a socket.io server run as long-lived services.
- **machine_actions**: true. The REST API and RPC methods change documents and DocTypes with per-user API keys (frappe/api).
- **agent_mutations**: false. No first-party AI or agent changes Frappe definitions in this repository.
- **evolution_auto_apply**: false. Every definition change is made by a person with the right role; nothing applies changes automatically.
- **definition_change_path**: true. DocTypes, workflows, print formats and settings are definitions.
- **code_release_path**: false. No first-party evolution system ships code changes; releases are made by engineers.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **3** (grade A), facets: implemented, tested. Each DocType has its own table, so there is no generic store; DocField.search_index creates database indexes from the definition; lists run through indexed SQL (frappe/model/db_query.py) with Redis meta and document caches; global search table (frappe/utils/global_search.py).
- **ARC-02 Safe schema and data migrations**: **1** (grade A). Schema follows DocType definitions through bench migrate and one-way patches (frappe/patches.txt, frappe/migrate.py); CI upgrades a populated site from the previous version (.github/workflows/server-tests.yml:143-230). There are no down steps and no enforced online strategy.
  - Higher reading 2: The CI upgrade test against existing data goes beyond level 1.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A). Sessions and caches live in Redis (frappe/sessions.py:400) and web workers are stateless, but files sit on local disk and the scheduler holds a file lock on one host (frappe/utils/scheduler.py:43-53).
- **ARC-04 Reliable asynchronous work**: **2** (grade A), facets: implemented, tested. RQ queues with per-queue timeouts, optional retries and deduplication (frappe/utils/background_jobs.py:99-145); failed jobs are kept and visible as RQ Job records (frappe/core/doctype/rq_job). The scheduler lock is per host, and idempotency is left to each job.
  - Higher reading 3: Failed-job registry and visibility are close to level 3.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Multi-site benches give each site its own database; per-site request rate limiting (frappe/rate_limiter.py:16-18). No noisy-neighbour detection or isolation verification in the repository.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **2** (grade A). frappe/tests/test_perf.py and frappe/tests/microbenchmarks exist; no documented per-surface limits or CI budgets.
- **ARC-07 Service objectives defined and monitored**: **1** (grade A). No published objectives. frappe/monitor.py records request and job timings when monitoring is enabled.
  - Higher reading 2: Monitor logs are latency metrics for core paths.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A). The automation engine counts failures per rule against a circuit breaker and isolates each row with a savepoint (frappe/automation_engine/runner.py:516-525, drainer.py:74); integrations accept timeouts (frappe/integrations/utils.py:59). Apps run in-process without isolation.
- **ARC-09 Backup, restore and recovery**: **2** (grade A). bench backup covers the database, public and private files and site config, with optional encryption (frappe/commands/site.py:899-1030, frappe/utils/backups.py), and restore from full and partial backups is tested end to end (frappe/commands/test_commands.py:280-330). The site config holding the encryption key is backed up but its restore is not tested, so secrets stay at 2.
  - Inventory: data 3, definitions 3, files 3, secrets 2

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A). No request or feature-request object for changing the product was found; requests live outside it.

### Build

- **DEL-02 Layers deploy independently**: **1** (grade A). One Python and JavaScript codebase deployed as a bench (web, workers, scheduler and realtime share the artifact); container images live in a separate repository.
- **DEL-03 Module boundaries enforced by tooling**: **1** (grade A). Module boundaries are convention; no architectural lint or dependency-graph enforcement found.
- **DEL-04 AI implementation lane**: **0** (grade A). No AI authoring lane in the repository.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A). Server tests, Cypress UI tests, linters with semgrep and a bundle-size check run on every pull request with no draft skip (.github/workflows/server-tests.yml, ui-tests.yml, linters.yml, default-js-bundle-size.yml). No accessibility check.
  - Higher reading 3: Every code change class except accessibility has a pre-land check and drafts are included.
- **DEL-06 Verification surface**: **2** (grade A). frappe.ping (frappe/__init__.py:1478) and get_versions (frappe/utils/change_log.py:105); System Health Report DocType; no deployed-configuration snapshot endpoint.
- **DEL-07 Environment reproducibility**: **2** (grade A). bench new-site and CI create fresh sites with test records per run (.github/workflows/server-tests.yml); no per-change ephemeral environment and no feature flags.
  - Higher reading 3: CI already builds a seeded, disposable site per change.
- **DEL-08 Machine verifiability**: **2** (grade A). Cypress journeys (cypress/integration) and server tests; no changed-path to journey map or adoption instrumentation at ship.

### Release

- **DEL-09 Staged exposure**: **2** (grade A). Apps can be enabled per site (bench enable-app and disable-app, frappe/commands/site.py:1053-1090); there are no feature flags or percentage rollouts.
- **DEL-10 Kill switch**: **1** (grade A). Disabling an app needs a bench command; automation rules are switched off by their circuit breaker or by an admin (frappe/automation_engine/runner.py:516-525).
  - Higher reading 2: Automation rules can be disabled at runtime.
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: No first-party evolution system ships code changes; releases are made by engineers.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **3** (grade A). Sites outside developer mode can create DocTypes with custom=1 in Desk (check_developer_mode, frappe/core/doctype/doctype/doctype.py:329-340); on_update calls frappe.db.updatedb to create or alter the table automatically (doctype.py:539-546). No deploy. No dry-run or policy gate, so not 4.
- **MAL-02 Field definitions carry type and validation**: **3** (grade A). DocField carries fieldtype, reqd, length, unique, non_negative, min_value, max_value, options-based validation, mandatory_depends_on and a mask flag (frappe/core/doctype/docfield/docfield.json); admins add typed fields through Customize Form and Custom Field. mask is consumed by read paths (frappe/model/meta.py:207, frappe/model/db_query.py:35, frappe/desk/form/load.py:295). Personal-data scope for erasure is declared in code (user_data_fields, frappe/hooks.py:360), not per field, so not 4.
- **MAL-03 Relationships and lifecycle states declarable**: **3** (grade A). Link, Dynamic Link and Table fields declare relations and Workflow DocTypes declare states and transitions in the UI (frappe/workflow/doctype/); the platform enforces transitions (frappe/model/workflow.py:119-246) and link integrity (frappe/model/delete_doc.py:414); both are creatable through the REST API with validation errors, which meets the rubric's definition of AI-authorable. Scored at the lower reading under rule 11 because: If AI-authorable is read as needing an AI authoring feature.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.

### APIs

- **MAL-04 API per entity is generic or generated**: **3** (grade A). One generic document API serves every DocType: frappe/api/v2.py read_doc, document_list with fields and filters, create_doc, update_doc, delete_doc, get_meta (lines 84-245), plus frappe/api/v1.py. No per-type controllers.
  - Higher reading 4: Projections, filters and validation already derive from the definition at runtime; only 'typed' is missing.
- **MAL-05 API reshapes at runtime from definitions**: **3** (grade A). Meta is loaded and cached at runtime (frappe/model/meta.py); a new or changed DocType is served by /api/resource and /api/v2 immediately on save. No per-consumer schema versions or dry-run.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A). Introspection through get_meta (frappe/api/v2.py:245) and getdoctype (frappe/desk/form/load.py); Python type stubs generated from definitions (frappe/types/exporter.py). No OpenAPI, no external typed client generation; errors carry exc_type but no field-level schema.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **3** (grade A). Form layout (tab, section and column breaks) is DocType data, overridable per site through Customize Form and DocType Layout (frappe/core/doctype/doctype_layout); Workspace, Web Page, Web Form and Print Format are admin builders with previews (frappe/desk/doctype/workspace, frappe/website/doctype/web_page, frappe/printing/doctype/print_format). A site is the tenant unit.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **3** (grade A). Every DocType gets generic list, report, kanban, calendar, form and quick-entry views rendered from its definition (frappe/public/js/frappe/list, form, views); admins configure List View Settings (frappe/desk/doctype/list_view_settings) and saved report views. No inherited accessibility guarantee, so not 4.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A). Per-site text overrides through the Translation DocType (frappe/core/doctype/translation); locale pipeline through Crowdin workflows (.github/workflows/crowdin-actions-*.yml); Website Theme DocType edits website styling (frappe/website/doctype/website_theme). Scored at the lower reading under rule 11 because: The admin theme editor covers the website only; the Desk application UI offers light and dark modes, not tenant tokens.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **3** (grade A). Automation Flow, Action and Run DocTypes (frappe/automation/doctype) on an engine exposing get_automation_capabilities, validate_action_params and run_manually (frappe/automation_engine/api.py); trial runs simulate wait steps (frappe/automation_engine/tests/test_trial_run.py:115-152); Notification preview_meets_condition (frappe/email/doctype/notification/notification.py:98). Covers custom DocTypes.
  - Higher reading 4: Capabilities are machine-readable and trial runs exist; versioning of flows and AI authoring are not evidenced.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **3** (grade A). Admin-configured Webhook per DocType event with conditions, headers and data mapping (frappe/integrations/doctype/webhook), delivery log (webhook_request_log) and scheduled retries with max_retries (retry_failed_webhooks, test_webhook.py:339-354); durable automation trigger queue with retention (frappe/automation_engine/drainer.py:291, settings.py:18). No replay.
- **MAL-12 Sandboxed server-side hooks**: **3** (grade A). Server Script runs under RestrictedPython with allowlisted globals (frappe/utils/safe_exec.py:15-17, 95), triggered by DocType events, API calls, scheduler and permission queries, authored by System Managers when server_script_enabled is set (safe_exec.py:48); outbound requests limited to globally routable http(s) hosts with timeouts (safe_exec.py:372-400, 486). Execution time is bounded only by the worker. No per-hook test harness, so not 4.

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A). Code apps through hooks (hooks.md, frappe/hooks.py) plus declarative layers: Custom Field, Property Setter, Client Script, Server Script, Custom HTML Block, Web Template, Print Format, Workspace, Translation.
- **MAL-14 Runtime isolation and dependency control**: **1** (grade A). Server Scripts run in-process under RestrictedPython allowlists with request egress control (frappe/utils/safe_exec.py); installed apps and client scripts run with full trust. Scored at the lower reading under rule 11 because: If the criterion is read for third-party apps, which run with full trust.
  - Higher reading 2: The September v0.3 pass scored 2 on the evidence above.
- **MAL-15 Developer loop**: **2** (grade A). bench developer mode, System Console (frappe/desk/doctype/system_console), Recorder and Error Log support local and on-site iteration; no staged branches or preview against a tenant in the repository.
  - Higher reading 3: System Console and Recorder already give validators and logs against a live site.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **1** (grade A). Integrations (Google Calendar and Contacts, LDAP, Connected App) are bespoke modules (frappe/integrations/doctype); Data Import value mapping covers imports only.
  - Higher reading 2: Webhook data mapping and import mapping are configurable mapping layers for narrow flows.
- **MAL-17 Connector definition or SDK**: **2** (grade A). Connected App is an admin-configured generic OAuth2 client and Integration Request logs calls (frappe/integrations/doctype/connected_app, integration_request); no connector SDK covering sync and lifecycle.
- **MAL-18 Stable versioned contracts**: **2** (grade A). Path-versioned APIs (frappe/api/v1.py, frappe/api/v2.py); no deprecation policy, idempotent sync or conflict handling found.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A). Introspectable meta (get_meta) and automation capability APIs (frappe/automation_engine/api.py); no MCP server or tool surface in the repository.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **0** (grade A). No member-facing assistant or natural-language authoring in the repository (searched for assistant, chat, LLM and copilot features; hits are developer docs only: AGENTS.md, ui/CLAUDE.md).

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A). Route History, Activity Log and Access Log are written to the site database as events happen and are read by product features (frappe/desk/doctype/route_history); vendor telemetry through pulse and PostHog (frappe/utils/telemetry). Scored at the lower reading under rule 11 because: Only navigation and access events are near-real-time; there is no general per-feature event stream.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-02 Structured learning signals**: **1** (grade A). No typed feedback or rating objects; Error Log links errors to reference documents but not to the definition version.
  - Higher reading 2: Error Log entries are typed signals linked to documents.
- **LRN-03 User-issue detection**: **2** (grade A). Error Log records exceptions with the method, reference document and trace id, queryable in the desk (frappe/core/doctype/error_log/error_log.json).
- **LRN-04 Cross-source mining inside the product**: **1** (grade A). DuckDB Sync copies DocType data for analytics (frappe/core/doctype/duckdb_sync) and reports can join DocTypes, but nothing joins usage, support and delivery data or mines them.
  - Higher reading 2: In-product reporting over the site database is a partial join of sources.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A). Error Log groups errors by fingerprint and reports counts over time (frappe/core/doctype/error_log/error_log.py:80-103), with the trace attached.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A). The Recorder's query optimiser proposes database indexes from recorded queries (frappe/core/doctype/recorder/db_optimizer.py:242, recorder.py:159): evidence-backed recommendations for one area.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **2** (grade A). The Recorder proposes database indexes from recorded queries when a person runs it (frappe/core/doctype/recorder/db_optimizer.py:242); nothing proposes changes without being asked.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A). Suggested changes are applied by a person; there is no automated evaluation.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
  - Higher reading 1: The Recorder supports ad hoc before-and-after checks.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). A UI kit with tokens exists (ui/, frappe/public/scss) but no automated accessibility scanning was found in CI or tests (no axe, pa11y, jsx-a11y or vuejs-accessibility in the tree).
  - Higher reading 2: The kit-and-tokens half of level 2 is present; the anchors bundle kit and scans, so kit-without-scans fits neither level.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A). Version records field-level changes for DocTypes with track_changes (frappe/core/doctype/doctype/doctype.py:181); Audit Trail compares versions (frappe/core/doctype/audit_trail); Activity, Access, API Request and Permission logs exist; retention through Log Settings (frappe/core/doctype/log_settings/log_settings.py:80-86). Coverage is opt-in per DocType; not tamper-evident.
  - Higher reading 3: Admin UI, retention and config and permission logs exist; only the 'all entities' clause fails because tracking is opt-in.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Personal Data Download and Deletion Requests cover every DocType declared in user_data_fields hooks (frappe/hooks.py:360, frappe/website/doctype/personal_data_deletion_request). The declaration is app code, not a field-level tag; retention exists for logs only.
  - Higher reading 3: Erasure is generic across entities; the only gap is that coverage comes from a code hook instead of a tag in the definition.
- **GOV-04 Security as infrastructure**: **2** (grade A), facets: implemented, tested. Role permissions are part of every DocType definition (DocPerm, Custom DocPerm, user permissions, permlevels, mask); field validation is generic; semgrep runs on every pull request (.github/workflows/linters.yml:67-72) and Dependabot is configured (.github/dependabot.yml). Whether the check blocks merge is a branch-protection setting not visible in the repository. Scored at the lower reading under rule 11 because: If 'gates every change' needs visible proof that the scan blocks merges.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A). Document changes are versioned with diffs (Version, Audit Trail); deleted documents can be restored (frappe/core/doctype/deleted_document/deleted_document.py:43). No revert-to-version for definitions, layouts or configuration.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **2** (grade A). Customisations move between sites as exported fixtures or Package Releases (frappe/core/doctype/package_release/package_release.py:79-96), an engineer-run stage-and-publish flow. No proposal object with preview.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A). Every definition change is made directly by a person holding the right role; no policy object and no auto-apply classes.
- **GOV-08 Upgrade safety**: **2** (grade A). Customisations live in separate layers (Custom Field, Property Setter, Client Script, Server Script) that survive bench migrate while standard DocTypes resync; frappe/patches.txt carries migrations. No automated compatibility check of customisations against the next release.
  - Higher reading 3: Customisations are confined to stable layers and migration tooling exists; only automated compatibility checks are missing.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A). Per-user API key and secret (frappe/core/doctype/user/user.json:600-620), OAuth scopes (frappe/integrations/doctype/oauth_scope), API Request Log, rate limiting (frappe/rate_limiter.py). No idempotency keys or dry-run.
- **GOV-10 Bounded self-change**: **not applicable**. Scope fact agent_mutations and evolution_auto_apply is false: No first-party AI or agent changes Frappe definitions in this repository.
- **GOV-11 Learning-input integrity**: **not applicable**. Scope fact agent_mutations and evolution_auto_apply is false: No first-party AI or agent changes Frappe definitions in this repository.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A). Kernel is User, Role, DocPerm, DocType, File, Communication, Workflow, Notification and Email Account; domains live in separate apps (README.md:22-32 names ERPNext); kernel objects are themselves DocTypes customisable through the same definitions (DocType is a DocType). Scored at the lower reading under rule 11 because: If 'configurable definitions' requires more than kernel objects being customisable DocTypes.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.
- **EXP-02 A new domain is expressible without kernel change**: **3** (grade B). README.md:22-32 states ERPNext was built on the framework; several domains ship as separate apps on an unchanged kernel. Those apps contain code as well as definitions; a domain can also be built from custom DocTypes, workflows and server scripts alone.
  - Higher reading 4: Multiple domains already ship as installable bundles with the kernel unchanged, if code-carrying apps count as bundles.
- **EXP-03 A domain ships as an installable bundle**: **3** (grade A). Package, Package Release and Package Import DocTypes export and install versioned bundles of DocTypes, scripts and other customisations (frappe/core/doctype/package, package_release, package_import).

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A). No record of failed searches or unsupported requests was found (frappe/search, frappe/desk).
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A). No adjacent-capability proposals.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **2** (grade A). An app (bundle) can be installed and enabled for selected sites (frappe/commands/site.py:559, 1053); there is no success metric or keep-or-kill record.
