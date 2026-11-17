# Frappe Framework: EVOLVE v0.7 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.7.0 in this repository.

Scope: the frappe repository only (framework, Desk UI, website module, automation engine). Apps built on it (ERPNext, HRMS, CRM) and Frappe Cloud are out of scope.

## Reading

**SAL 1.** Operators reshape Frappe without code (Open 2.3), so every loop reaches L1, but nothing in the product drafts or builds a change (DEL-04 0) and requests have no intake (DEL-01 0), so no loop reaches L2. **Architecture:** backup and restore of data and files are tested end to end, but restoring the site secrets is not (ARC-09 2), and migrations are forward-only (ARC-02 1). **Next level:** an AI lane that drafts DocType, workflow or report changes as proposals, and structured request intake.

## Limits

Repository evidence only, develop branch at the tip named above. No running site was inspected, so validation and preview behaviour is read from code, not exercised. Frappe Cloud features (marketplace, staging sites, backups) and apps built on the framework are out of scope. Whether CI checks block merges depends on branch protection, which is not visible in the repository. Single rater; the eight alternate readings mark where a second rater could reasonably differ.

---
Framework EVOLVE 0.7.0. Date 2026-09-30. Source github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop). Archetype **configurable-application-platform**. Basis **shipped** (what ships).

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, definition_change_path. False: agent_mutations, evolution_auto_apply, code_release_path, ai_features, ai_data_access, ai_actions.

Coverage: 64 assessed, 0 not evidenced, 11 not applicable. Grades: 63 A, 1 B, 0 C.

Confidence: 6 high, 49 medium, 9 low across the assessed criteria. Check these first (low confidence, and they hold a blocker or a critical control): DEL-01 (Request → Release to L2); EXP-05 (Opportunity → Expansion to L2).

## Software Autonomy Level

**Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)**

Progress toward the next level: Request → Release 2 of 4 conditions for L2; Issue → Fix 4 of 5 conditions for L2; Opportunity → Expansion 3 of 5 conditions for L2.

- With opt-in settings: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0).
- With every alternate reading: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0).

| Loop | Stages | Spine | Architecture | Governance | Level | AI-driven | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L1 | L2 | L2 | **L1** | L0 | L1 |
| Issue → Fix | L2 | L1 | L2 | L2 | **L1** | L0 | L1 |
| Opportunity → Expansion | L1 | L2 | L2 | L2 | **L1** | L0 | L1 |

**Recursion: 1 By hand (LRN-10 at 1).** How far the loop improves its own checks, evaluation sets, policies and prompts from measured results.

**AI delivery.** Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

### Kinds of change

4 of 4 main kinds are self-serve (reach 1 or more: the people running the product make it themselves and can undo it).

| Kind | Who | Main | Reach | Evidence |
|---|---|---|---|---|
| Record types, fields and form layouts (`forms-fields`) | system managers | yes | 1 Self-serve | Custom DocTypes, Custom Fields and Customize Form changes are made in Desk with no deploy (frappe/core/doctype/doctype/doctype.py:329-340, 539-546; frappe/custom/doctype/customize_form). Undo: DocType, Custom Field and Property Setter track changes, so every change keeps a Version with the earlier values (their .json: track_changes 1); Customize Form resets a form's layout or all its customisations (customize_form.py:635-660, 692-712); deleted documents can be restored for 180 days (frappe/core/doctype/deleted_document/deleted_document.py:32-70). No one-step revert to an earlier version (GOV-05 is 2), so undo is by hand from the recorded history. Confidence medium. |
| Approval workflows, notifications and automation rules (`workflows-automation`) | system managers and process owners | yes | 1 Self-serve | Workflow, Notification and Automation Flow are DocTypes edited in Desk with no deploy (frappe/workflow/doctype/workflow, frappe/email/doctype/notification, frappe/automation/doctype/automation_flow); each tracks changes and can be switched off (workflow.json is_active, notification.json and automation_flow.json enabled). No one-step revert to an earlier version (GOV-05 is 2), so undo is by hand from the recorded history. Confidence medium. |
| Who can see and change what (roles and permissions) (`permissions`) | system managers | yes | 1 Self-serve | Role Permission Manager changes Custom DocPerm rules with no deploy; each change is written to Permission Log and a DocType's permissions can be reset to standard (frappe/core/page/permission_manager/permission_manager.py:179-247); User Permission and Role track changes. Confidence medium. |
| Reports and printed documents (`reports-print`) | system managers and report users | yes | 1 Self-serve | Report Builder reports are saved in Desk and Report tracks changes (frappe/core/doctype/report/report.json); the print format builder keeps drafts and named versions that can be loaded back and applied (frappe/printing/doctype/print_format/print_format.py:461-560). Script reports need Server Scripts or app code. Confidence medium. |
| Custom server-side logic, integrations and new apps (`server-logic-apps`) | system managers, with engineers | no | 0 Engineers only | Server Scripts can be enabled only by editing common_site_config.json (frappe/utils/safe_exec.py:86-88), and new apps and bespoke integrations are installed with bench commands (frappe/commands/site.py:559); both need an engineer. Not main: most change requests are met by the self-serve kinds above and by Client Scripts, Automation Flows and Notifications; a rater who reads server-side logic as a large share would mark this main and the people path would drop to 1. Confidence low. |

### Proven

**Proven: not evidenced.** What operating records show real changes doing, beside what the product is built to do. From a repository alone, proven is usually not evidenced.

| Loop | Built | Proven | Operating records, or what was searched |
|---|---:|---|---|
| Request → Release | L1 | not evidenced | Searched: The repository at the pinned commit: Version, Audit Trail and Permission Log DocTypes (the mechanisms, not records), frappe/change_log and release notes for Frappe's own engineer-made releases. No operating records of real changes made through the product's request loop in a deployment are in the repository. |
| Issue → Fix | L1 | not evidenced | Searched: The same sources plus Error Log and Recorder; no operating records of issues fixed through the product's loop in a deployment. |
| Opportunity → Expansion | L1 | not evidenced | Searched: The same sources plus Package Release; no records of capabilities launched to selected sites and kept or killed. |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 1 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 2 | fail |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | not applicable (agent_mutations and evolution_auto_apply false) | n/a | n/a |

### What blocks the next level

- **Request → Release to L2**: spine Build needs product build path ≥ 2 (has DEL-04 0); stages Intake needs DEL-01 ≥ 2 (has 0)
- **Issue → Fix to L2**: spine Build needs product build path ≥ 2 (has DEL-04 0, LRN-07 2 with LRN-08 1)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0)

### What AI drives

Each loop re-scored with its AI-performable stages read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level.

| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |
|---|---:|---:|---|---|
| Request → Release | L1 | L0 | DEL-01 0, DEL-04 0 | product build path ≥ 2 (has DEL-04 0); DEL-01 ≥ 2 (has 0) |
| Issue → Fix | L1 | L0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 0 | product build path ≥ 2 (has DEL-04 0, LRN-07 0); LRN-05 ≥ 2 (has 0); LRN-06 ≥ 2 (has 0) |
| Opportunity → Expansion | L1 | L0 | EXP-05 0 | EXP-05 ≥ 2 (has 0) |

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.9 | 1.9–2.2 | 1.9 | 1.9 | 1.9 |
| Velocity (DEL) | 1.0 | 1.0–1.3 | 1.0 | 1.0 | 1.0 |
| Open (MAL) | 2.3 | 2.3–2.6 | 2.3 | 2.3 | 2.3 |
| Learn (LRN) | 1.4 | 1.4–1.8 | 1.4 | 1.4 | 1.4 |
| Vet (GOV) | 1.8 | 1.8–2.3 | 1.8 | 1.8 | 1.8 |
| Expand (EXP) | 1.7 | 1.7–1.9 | 1.7 | 1.7 | 1.7 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Scale | 2.0 |
| ARC Capacity | 1.5 |
| ARC Resilience | 2.0 |
| DEL Intake | 0.0 |
| DEL Build | 0.7 |
| DEL Verify | 2.0 |
| DEL Release | 1.5 |
| MAL Data model | 3.0 |
| MAL APIs | 2.7 |
| MAL Interface | 2.7 |
| MAL Behaviour | 3.0 |
| MAL Extensions | 2.0 |
| MAL Integrations | 1.7 |
| MAL Agent interface | 1.0 |
| LRN Sense | 1.5 |
| LRN Diagnose and propose | 2.0 |
| LRN Learn from experience | 1.5 |
| LRN Measure | 0.5 |
| GOV Compliance and security | 1.8 |
| GOV Change control | 1.8 |
| GOV AI and self-change safety | 2.0 |
| EXP Expressible | 3.0 |
| EXP Discover | 0.0 |
| EXP Launch | 2.0 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**no AI features**

- With opt-in settings: no AI features.
- With every alternate reading: no AI features.

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 0 | MAL-19 0, MAL-20 0 |
| Build | 0 | DEL-01 0, DEL-04 0 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 0 |
| Expand | 0 | EXP-05 0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 3 |  |  | A, high | IT | Each DocType has its own table, so there is no generic store; DocField.search_index creates database indexes from the definition; lists run through indexed SQL (frappe/model/db_query.py) with Redis meta and document caches; global search table (frappe/utils/global_search.py). |
| ARC-02 Safe schema and data migrations | assessed | 1 | 2 |  | A, high |  | Schema follows DocType definitions through bench migrate and one-way patches (frappe/patches.txt, frappe/migrate.py); CI upgrades a populated site from the previous version (.github/workflows/server-tests.yml:143-230). There are no down steps and no enforced online strategy. |
| ARC-03 Horizontal scale of services | assessed | 2 |  |  | A, medium |  | Sessions and caches live in Redis (frappe/sessions.py:400) and web workers are stateless, but files sit on local disk and the scheduler holds a file lock on one host (frappe/utils/scheduler.py:43-53). |
| ARC-04 Reliable asynchronous work | assessed | 2 | 3 |  | A, high | IT | RQ queues with per-queue timeouts, optional retries and deduplication (frappe/utils/background_jobs.py:99-145); failed jobs are kept and visible as RQ Job records (frappe/core/doctype/rq_job). The scheduler lock is per host, and idempotency is left to each job. |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A, medium |  | Multi-site benches give each site its own database; per-site request rate limiting (frappe/rate_limiter.py:16-18). No noisy-neighbour detection or isolation verification in the repository. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A, medium |  | frappe/tests/test_perf.py and frappe/tests/microbenchmarks exist; no documented per-surface limits or CI budgets. |
| ARC-07 Service objectives defined and monitored | assessed | 1 | 2 |  | A, medium |  | No published objectives. frappe/monitor.py records request and job timings when monitoring is enabled. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A, medium |  | The automation engine counts failures per rule against a circuit breaker and isolates each row with a savepoint (frappe/automation_engine/runner.py:516-525, drainer.py:74); integrations accept timeouts (frappe/integrations/utils.py:59). Apps run in-process without isolation. |
| ARC-09 Backup, restore and recovery | assessed | 2 |  |  | A, high |  | Inventory: data 3, definitions 3, files 3, secrets 2, schedules 2. bench backup covers the database, public and private files and site config, with optional encryption (frappe/commands/site.py:899-1030, frappe/utils/backups.py), and restore from full and partial backups is tested end to end (frappe/commands/test_commands.py:280-330). The site config holding the encryption key is backed up but its restore is not tested, so secrets stay at 2. Scheduled work: scheduled job records and server-script scheduler events restore with the database and resume with the scheduler; no check of each job's identity, permissions or credentials before it runs was found (frappe/utils/scheduler.py), so scheduled work is 2. |
| DEL-01 Request intake into a structured change specification | assessed | 0 |  |  | A, low |  | No request or feature-request object for changing the product was found; requests live outside it. |
| DEL-02 Layers deploy independently | assessed | 1 |  |  | A, low |  | One Python and JavaScript codebase deployed as a bench (web, workers, scheduler and realtime share the artifact); container images live in a separate repository. |
| DEL-03 Module boundaries enforced by tooling | assessed | 1 |  |  | A, low |  | Module boundaries are convention; no architectural lint or dependency-graph enforcement found. |
| DEL-04 AI implementation lane | assessed | 0 |  |  | A, medium |  | No AI authoring lane in the repository. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A, medium |  | Server tests, Cypress UI tests, linters with semgrep and a bundle-size check run on every pull request with no draft skip (.github/workflows/server-tests.yml, ui-tests.yml, linters.yml, default-js-bundle-size.yml). No accessibility check. |
| DEL-06 Verification surface | assessed | 2 |  |  | A, medium |  | frappe.ping (frappe/__init__.py:1478) and get_versions (frappe/utils/change_log.py:105); System Health Report DocType; no deployed-configuration snapshot endpoint. |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A, medium |  | bench new-site and CI create fresh sites with test records per run (.github/workflows/server-tests.yml); no per-change ephemeral environment and no feature flags. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A, medium |  | Cypress journeys (cypress/integration) and server tests; no changed-path to journey map or adoption instrumentation at ship. |
| DEL-09 Staged exposure | assessed | 2 |  |  | A, medium |  | Apps can be enabled per site (bench enable-app and disable-app, frappe/commands/site.py:1053-1090); there are no feature flags or percentage rollouts. |
| DEL-10 Kill switch | assessed | 1 | 2 |  | A, medium |  | Disabling an app needs a bench command; automation rules are switched off by their circuit breaker or by an admin (frappe/automation_engine/runner.py:516-525). |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: No first-party evolution system ships code changes; releases are made by engineers. |
| MAL-01 New entity type without code, DDL or deploy | assessed | 3 |  |  | A, medium |  | Sites outside developer mode can create DocTypes with custom=1 in Desk (check_developer_mode, frappe/core/doctype/doctype/doctype.py:329-340); on_update calls frappe.db.updatedb to create or alter the table automatically (doctype.py:539-546). No deploy. No dry-run or policy gate, so not 4. |
| MAL-02 Field definitions carry type and validation | assessed | 3 |  |  | A, medium |  | DocField carries fieldtype, reqd, length, unique, non_negative, min_value, max_value, options-based validation, mandatory_depends_on and a mask flag (frappe/core/doctype/docfield/docfield.json); admins add typed fields through Customize Form and Custom Field. mask is consumed by read paths (frappe/model/meta.py:207, frappe/model/db_query.py:35, frappe/desk/form/load.py:295). Personal-data scope for erasure is declared in code (user_data_fields, frappe/hooks.py:360), not per field, so not 4. |
| MAL-03 Relationships and lifecycle states declarable | assessed | 3 | 4 |  | A, medium |  | Link, Dynamic Link and Table fields declare relations and Workflow DocTypes declare states and transitions in the UI (frappe/workflow/doctype/); the platform enforces transitions (frappe/model/workflow.py:119-246) and link integrity (frappe/model/delete_doc.py:414); both are creatable through the REST API with validation errors, which meets the rubric's definition of AI-authorable. Scored at the lower reading under rule 11 because: If AI-authorable is read as needing an AI authoring feature. |
| MAL-04 API per entity is generic or generated | assessed | 3 | 4 |  | A, medium |  | One generic document API serves every DocType: frappe/api/v2.py read_doc, document_list with fields and filters, create_doc, update_doc, delete_doc, get_meta (lines 84-245), plus frappe/api/v1.py. No per-type controllers. |
| MAL-05 API reshapes at runtime from definitions | assessed | 3 |  |  | A, medium |  | Meta is loaded and cached at runtime (frappe/model/meta.py); a new or changed DocType is served by /api/resource and /api/v2 immediately on save. No per-consumer schema versions or dry-run. |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A, medium |  | Introspection through get_meta (frappe/api/v2.py:245) and getdoctype (frappe/desk/form/load.py); Python type stubs generated from definitions (frappe/types/exporter.py). No OpenAPI, no external typed client generation; errors carry exc_type but no field-level schema. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 3 |  |  | A, medium |  | Form layout (tab, section and column breaks) is DocType data, overridable per site through Customize Form and DocType Layout (frappe/core/doctype/doctype_layout); Workspace, Web Page, Web Form and Print Format are admin builders with previews (frappe/desk/doctype/workspace, frappe/website/doctype/web_page, frappe/printing/doctype/print_format). A site is the tenant unit. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | assessed | 3 |  |  | A, medium |  | Every DocType gets generic list, report, kanban, calendar, form and quick-entry views rendered from its definition (frappe/public/js/frappe/list, form, views); admins configure List View Settings (frappe/desk/doctype/list_view_settings) and saved report views. No inherited accessibility guarantee, so not 4. |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 | 3 |  | A, medium |  | Per-site text overrides through the Translation DocType (frappe/core/doctype/translation); locale pipeline through Crowdin workflows (.github/workflows/crowdin-actions-*.yml); Website Theme DocType edits website styling (frappe/website/doctype/website_theme). Scored at the lower reading under rule 11 because: The admin theme editor covers the website only; the Desk application UI offers light and dark modes, not tenant tokens. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 3 | 4 |  | A, high |  | Automation Flow, Action and Run DocTypes (frappe/automation/doctype) on an engine exposing get_automation_capabilities, validate_action_params and run_manually (frappe/automation_engine/api.py); trial runs simulate wait steps (frappe/automation_engine/tests/test_trial_run.py:115-152); Notification preview_meets_condition (frappe/email/doctype/notification/notification.py:98). Covers custom DocTypes. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 3 |  |  | A, high |  | Admin-configured Webhook per DocType event with conditions, headers and data mapping (frappe/integrations/doctype/webhook), delivery log (webhook_request_log) and scheduled retries with max_retries (retry_failed_webhooks, test_webhook.py:339-354); durable automation trigger queue with retention (frappe/automation_engine/drainer.py:291, settings.py:18). No replay. |
| MAL-12 Sandboxed server-side hooks | assessed | 3 |  |  | A, medium |  | Server Script runs under RestrictedPython with allowlisted globals (frappe/utils/safe_exec.py:15-17, 95), triggered by DocType events, API calls, scheduler and permission queries, authored by System Managers when server_script_enabled is set (safe_exec.py:48); outbound requests limited to globally routable http(s) hosts with timeouts (safe_exec.py:372-400, 486). Execution time is bounded only by the worker. No per-hook test harness, so not 4. |
| MAL-13 Plugin lane breadth | assessed | 3 |  |  | A, medium |  | Code apps through hooks (hooks.md, frappe/hooks.py) plus declarative layers: Custom Field, Property Setter, Client Script, Server Script, Custom HTML Block, Web Template, Print Format, Workspace, Translation. |
| MAL-14 Runtime isolation and dependency control | assessed | 1 | 2 |  | A, medium |  | Server Scripts run in-process under RestrictedPython allowlists with request egress control (frappe/utils/safe_exec.py); installed apps and client scripts run with full trust. Scored at the lower reading under rule 11 because: If the criterion is read for third-party apps, which run with full trust. |
| MAL-15 Developer loop | assessed | 2 | 3 |  | A, medium |  | bench developer mode, System Console (frappe/desk/doctype/system_console), Recorder and Error Log support local and on-site iteration; no staged branches or preview against a tenant in the repository. |
| MAL-16 Canonical data model with a mapping layer | assessed | 1 | 2 |  | A, medium |  | Integrations (Google Calendar and Contacts, LDAP, Connected App) are bespoke modules (frappe/integrations/doctype); Data Import value mapping covers imports only. |
| MAL-17 Connector definition or SDK | assessed | 2 |  |  | A, medium |  | Connected App is an admin-configured generic OAuth2 client and Integration Request logs calls (frappe/integrations/doctype/connected_app, integration_request); no connector SDK covering sync and lifecycle. |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A, medium |  | Path-versioned APIs (frappe/api/v1.py, frappe/api/v2.py); no deprecation policy, idempotent sync or conflict handling found. |
| MAL-19 Machine-readable capability surface for agents | assessed | 2 |  |  | A, medium |  | Introspectable meta (get_meta) and automation capability APIs (frappe/automation_engine/api.py); no MCP server or tool surface in the repository. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 0 |  |  | A, medium |  | No member-facing assistant or natural-language authoring in the repository (searched for assistant, chat, LLM and copilot features; hits are developer docs only: AGENTS.md, ui/CLAUDE.md). |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A, medium |  | Route History, Activity Log and Access Log are written to the site database as events happen and are read by product features (frappe/desk/doctype/route_history); vendor telemetry through pulse and PostHog (frappe/utils/telemetry). Scored at the lower reading under rule 11 because: Only navigation and access events are near-real-time; there is no general per-feature event stream. |
| LRN-02 Structured learning signals | assessed | 1 | 2 |  | A, low |  | No typed feedback or rating objects; Error Log links errors to reference documents but not to the definition version. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A, medium |  | Error Log records exceptions with the method, reference document and trace id, queryable in the desk (frappe/core/doctype/error_log/error_log.json). |
| LRN-04 Cross-source mining inside the product | assessed | 1 | 2 |  | A, medium |  | DuckDB Sync copies DocType data for analytics (frappe/core/doctype/duckdb_sync) and reports can join DocTypes, but nothing joins usage, support and delivery data or mines them. |
| LRN-05 Automated diagnosis | assessed | 2 |  |  | A, medium |  | Error Log groups errors by fingerprint and reports counts over time (frappe/core/doctype/error_log/error_log.py:80-103), with the trace attached. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 2 |  |  | A, medium |  | The Recorder's query optimiser proposes database indexes from recorded queries (frappe/core/doctype/recorder/db_optimizer.py:242, recorder.py:159): evidence-backed recommendations for one area. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 2 |  |  | A, medium |  | The Recorder proposes database indexes from recorded queries when a person runs it (frappe/core/doctype/recorder/db_optimizer.py:242); nothing proposes changes without being asked. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 |  |  | A, medium |  | The only changes the product proposes to itself are the Recorder's index suggestions (LRN-07); the Administrator applies them (frappe/core/doctype/recorder/recorder.py:139-155) with no automated check or baseline comparison before they take effect; the duration thresholds (recorder.py:163-171) shape the suggestion, not a check on it. Re-read at the v0.7 migration under the tightened boundary: the reading stands at 1, manual review only. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 | 1 |  | A, low |  | No binding of changes to baselines or metrics. |
| LRN-10 The improvement loop improves itself | assessed | 1 | 2 |  | A, low |  | The checks that govern definition changes are code that engineers change: DocType and Customize Form validation (frappe/core/doctype/doctype/doctype.py, frappe/custom/doctype/customize_form/customize_form.py) and the Recorder's fixed suggestion thresholds (frappe/core/doctype/recorder/recorder.py:163-171). The policies on who may change definitions are role permissions that System Managers change by hand in the Role Permission Manager, logged with before and after values in Permission Log and resettable to standard (frappe/core/page/permission_manager/permission_manager.py:179-247). There are no evaluation sets, and nothing records a failure against the check or rule that missed it. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A, medium |  | A UI kit with tokens exists (ui/, frappe/public/scss) but no automated accessibility scanning was found in CI or tests (no axe, pa11y, jsx-a11y or vuejs-accessibility in the tree). |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A, medium |  | Version records field-level changes for DocTypes with track_changes (frappe/core/doctype/doctype/doctype.py:181); Audit Trail compares versions (frappe/core/doctype/audit_trail); Activity, Access, API Request and Permission logs exist; retention through Log Settings (frappe/core/doctype/log_settings/log_settings.py:80-86). Coverage is opt-in per DocType; not tamper-evident. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 | 3 |  | A, medium |  | Personal Data Download and Deletion Requests cover every DocType declared in user_data_fields hooks (frappe/hooks.py:360, frappe/website/doctype/personal_data_deletion_request). The declaration is app code, not a field-level tag; retention exists for logs only. |
| GOV-04 Security as infrastructure | assessed | 2 | 3 |  | A, medium | IT | Role permissions are part of every DocType definition (DocPerm, Custom DocPerm, user permissions, permlevels, mask); field validation is generic; semgrep runs on every pull request (.github/workflows/linters.yml:67-72) and Dependabot is configured (.github/dependabot.yml). Whether the check blocks merge is a branch-protection setting not visible in the repository. Scored at the lower reading under rule 11 because: If 'gates every change' needs visible proof that the scan blocks merges. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A, medium |  | Document changes are versioned with diffs (Version, Audit Trail); deleted documents can be restored (frappe/core/doctype/deleted_document/deleted_document.py:43). No revert-to-version for definitions, layouts or configuration. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 |  |  | A, medium |  | Customisations move between sites as exported fixtures or Package Releases (frappe/core/doctype/package_release/package_release.py:79-96), an engineer-run stage-and-publish flow. No proposal object with preview. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 |  |  | A, low |  | Every definition change is made directly by a person holding the right role; no policy object and no auto-apply classes. |
| GOV-08 Upgrade safety | assessed | 2 | 3 |  | A, medium |  | Customisations live in separate layers (Custom Field, Property Setter, Client Script, Server Script) that survive bench migrate while standard DocTypes resync; frappe/patches.txt carries migrations. No automated compatibility check of customisations against the next release. |
| GOV-09 Agent-safe actions | assessed | 2 |  |  | A, medium |  | Per-user API key and secret (frappe/core/doctype/user/user.json:600-620), OAuth scopes (frappe/integrations/doctype/oauth_scope), API Request Log, rate limiting (frappe/rate_limiter.py). No idempotency keys or dry-run. |
| GOV-10 Bounded self-change | not_applicable | excluded |  |  | - |  | Scope fact agent_mutations and evolution_auto_apply is false: No first-party AI or agent changes Frappe definitions in this repository. |
| GOV-11 Learning-input integrity | not_applicable | excluded |  |  | - |  | Scope fact agent_mutations and evolution_auto_apply is false: No first-party AI or agent changes Frappe definitions in this repository. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 | 4 |  | A, medium |  | Kernel is User, Role, DocPerm, DocType, File, Communication, Workflow, Notification and Email Account; domains live in separate apps (README.md:22-32 names ERPNext); kernel objects are themselves DocTypes customisable through the same definitions (DocType is a DocType). Scored at the lower reading under rule 11 because: If 'configurable definitions' requires more than kernel objects being customisable DocTypes. |
| EXP-02 A new domain is expressible without kernel change | assessed | 3 | 4 |  | B, low |  | README.md:22-32 states ERPNext was built on the framework; several domains ship as separate apps on an unchanged kernel. Those apps contain code as well as definitions; a domain can also be built from custom DocTypes, workflows and server scripts alone. |
| EXP-03 A domain ships as an installable bundle | assessed | 3 |  |  | A, medium |  | Package, Package Release and Package Import DocTypes export and install versioned bundles of DocTypes, scripts and other customisations (frappe/core/doctype/package, package_release, package_import). |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A, medium |  | No record of failed searches or unsupported requests was found (frappe/search, frappe/desk). |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A, low |  | No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 2 |  |  | A, medium |  | An app (bundle) can be installed and enabled for selected sites (frappe/commands/site.py:559, 1053); there is no success metric or keep-or-kill record. |
| AIR-03 AI-ready data and context access | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-04 Permission-preserving retrieval and tool access | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-05 Offline AI evaluation | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-06 Regression gating before release | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-07 AI action tracing and auditability | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-01 Model and provider portability and resilience | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-02 AI usage and per-customer cost controls | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |
| AIR-08 Production quality, drift and feedback monitoring | not_applicable | excluded |  |  | - |  | ai_features is false: No model-backed features in the framework (searched frappe/ for openai, anthropic, llm). |

Grade cell: evidence grade, then confidence where recorded. Facets: I implemented, T tested, O operated. Operated supports a Proven reading and never changes a score.
