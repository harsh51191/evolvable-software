# Discourse: EVOLVE v0.4 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.4.0 in this repository.

Scope: the discourse repository including the plugins bundled in plugins/ (automation, discourse-ai, discourse-workflows, data explorer, chat and others) and the core MCP server. Several of these ship disabled by default as betas. Hosted Discourse and the separate theme CLI and Docker repositories are out of scope.

## Reading

**SAL 1.** Admins configure Discourse without code, and it passes two critical controls that most systems fail: SafeMigrate and deferred column drops enforce expand-and-contract (ARC-02 3), and backup and restore of the database and uploads are tested (ARC-09 3). There is no AI lane by default (DEL-04 0), and as a focused application with adjacent-domain criteria excluded, Opportunity → Expansion stays at L0. **Learn:** search logs already record searches without results (EXP-04 2), the raw material for unmet-demand sensing. **Next level:** turn on and productise the workflows AI author, and cluster search misses and topic votes into proposals.

## Limits

Repository evidence only, main branch at the tip named above. discourse-ai, discourse-workflows and parts of the MCP surface ship disabled by default as betas; they were scored as shipped, and the alternates show the effect of discounting them. Hosted Discourse operations (incidents, ephemeral environments, telemetry pipelines) are invisible here. Single rater.

---
Framework EVOLVE 0.4.0. Date 2026-09-30. Source github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main). Archetype **focused-application**.

Scope facts true: persistent_data, schema_changes, multi_tenant, hosted_service, machine_actions, definition_change_path. False: agent_mutations, evolution_auto_apply, code_release_path.

Coverage: 55 assessed, 0 not evidenced, 11 not applicable. Grades: 55 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L0**

Progress toward the next level: Request → Release 2 of 4 conditions for L2; Issue → Fix 4 of 5 conditions for L2; Opportunity → Expansion 1 of 2 conditions for L1.

- With opt-in settings: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L2 · Opportunity → Expansion L1.
- With every alternate reading: SAL 1 (Configurable) · Request → Release L1 · Issue → Fix L1 · Opportunity → Expansion L0.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L1 | L2 | L2 | **L1** | L1 |
| Issue → Fix | L2 | L1 | L2 | L2 | **L1** | L2 |
| Opportunity → Expansion | L1 | L0 | L2 | L2 | **L0** | L1 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 3 | pass |
| Tested backup and restore | ARC-09 ≥ 3 | 3 | pass |
| Tenant isolation | ARC-05 ≥ 3 | 2 | fail |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | not applicable (agent_mutations and evolution_auto_apply false) | n/a | n/a |

### What blocks the next level

- **Request → Release to L2**: spine Build needs product build path ≥ 2 (has DEL-04 0); stages Intake needs DEL-01 ≥ 2 (has 1)
- **Issue → Fix to L2**: spine Build needs product build path ≥ 2 (has DEL-04 0, LRN-07 2 with LRN-08 1)
- **Opportunity → Expansion to L1**: spine Build needs people build path ≥ 2 or product build path ≥ 2 (has EXP-02 n/a; DEL-04 0, EXP-03 n/a)

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: MAL-02, MAL-06, LRN-03, GOV-05.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 2.1 | 2.1–2.3 | 2.1 | 2.1 | 2.1 |
| Velocity (DEL) | 1.4 | 1.4–1.9 | 1.6 | 1.4 | 1.4 |
| Open (MAL) | 2.1 | 2.1–2.3 | 2.3 | 2.1 | 1.8 |
| Learn (LRN) | 1.4 | 1.4–1.5 | 1.5 | 1.4 | 1.4 |
| Vet (GOV) | 1.8 | 1.8–2.5 | 1.9 | 1.8 | 1.7 |
| Expand (EXP) | 1.5 | 1.5 | 1.5 | 1.5 | 1.7 |

Caps and deductions applied:

- MAL-02: single-entity caps 3 -> 2

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.5 |
| ARC Scale | 2.0 |
| ARC Capacity | 1.5 |
| ARC Resilience | 2.5 |
| DEL Intake | 1.0 |
| DEL Build | 0.7 |
| DEL Verify | 2.0 |
| DEL Release | 2.0 |
| MAL Data model | 2.0 |
| MAL APIs | 2.0 |
| MAL Interface | 2.5 |
| MAL Behaviour | 2.3 |
| MAL Extensions | 2.3 |
| MAL Integrations | 1.3 |
| MAL Agent interface | 2.0 |
| LRN Sense | 2.0 |
| LRN Diagnose and propose | 2.0 |
| LRN Learn from experience | 1.5 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 1.8 |
| GOV Change control | 1.8 |
| GOV AI and self-change safety | 2.0 |
| EXP Discover | 1.0 |
| EXP Launch | 2.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A |  | PostgreSQL full-text search (lib/search.rb) and hand-tuned list queries; custom fields are not filterable at scale. |
| ARC-02 Safe schema and data migrations | assessed | 3 |  |  | A | IT | SafeMigrate blocks destructive migrations, and Migration::ColumnDropper and TableDropper defer drops so schema changes are expand-and-contract (lib/migration/safe_migrate.rb, column_dropper.rb, table_dropper.rb); post-deploy migrations separate destructive steps; migrations run in CI. |
| ARC-03 Horizontal scale of services | assessed | 2 | 3 |  | A | I | Stateless Puma processes over PostgreSQL and Redis; scale-out is documented in the separate discourse_docker repository rather than here. |
| ARC-04 Reliable asynchronous work | assessed | 2 | 3 |  | A | IT | Sidekiq jobs with retries and a dead set, and MiniScheduler runs scheduled jobs once across processes with a Redis lock (Gemfile:104-105); idempotency is left to each job. |
| ARC-05 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | IT | Multisite hosting with a database per site and pervasive rate limiters; no noisy-neighbour detection or isolation verification in the repository. |
| ARC-06 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A |  | Benchmark script (script/bench.rb); no documented per-surface limits or CI budgets. |
| ARC-07 Service objectives defined and monitored | assessed | 1 |  |  | A |  | No published objectives in this repository; the prometheus exporter is a separate plugin not bundled here. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | Outbound requests go through FinalDestination with timeouts, and safe mode disables plugins and themes for a session (config/routes.rb:2036). Plugins run in-process. |
| ARC-09 Backup, restore and recovery | assessed | 3 |  |  | A | IT | Inventory: data 3, definitions 3, files 3, secrets n/a. Built-in backup and restore of the database (data, site settings, themes) and uploads to local or S3 stores, with restore specs for both, including multisite (lib/backup_restore, spec/lib/backup_restore/database_restorer_spec.rb, uploads_restorer_spec.rb). Secrets live in the deployment environment, outside the product. No recovery objectives are stated (level 4). |
| DEL-01 Request intake into a structured change specification | assessed | 1 | 2 |  | A |  | Communities collect requests as topics; the bundled topic-voting plugin ranks them (plugins/discourse-topic-voting). They are not linked to the settings or screens involved. |
| DEL-02 Layers deploy independently | assessed | 1 |  |  | A |  | Rails and Ember monolith deployed as one application; container tooling lives in a separate repository. |
| DEL-03 Module boundaries enforced by tooling | assessed | 1 |  |  | A |  | Plugin API is a contract, but internal module boundaries are convention; no architectural lint. |
| DEL-04 AI implementation lane | assessed | 0 |  | 2 | A |  | By default there is no AI authoring lane; the beta workflows AI author is one when enabled. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A |  | Tests, linting and migration tests run on every pull request with no draft filter (.github/workflows/tests.yml:3-26, linting.yml, migration-tests.yml); no accessibility or security scan in CI. |
| DEL-06 Verification surface | assessed | 2 |  |  | A |  | Health endpoint /srv/status (config/routes.rb:135) and version through the about endpoint; no deployed-configuration snapshot. |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A |  | Scripted Docker development environment (bin/docker/boot_dev), test database setup, and upcoming-change flags that ship features off by default; no per-change ephemeral environment in the repository. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A |  | System specs drive browser journeys (spec/system) alongside QUnit tests; no changed-path to journey map or adoption instrumentation at ship. |
| DEL-09 Staged exposure | assessed | 2 | 3 |  | A |  | The upcoming-changes framework releases Discourse's own features to opted-in groups first (lib/upcoming_changes); site setting changes are not staged. |
| DEL-10 Kill switch | assessed | 2 |  |  | A |  | Site settings switch features and plugins off at runtime, and safe mode disables customisations per session (config/routes.rb:2036-2037). |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: No first-party evolution system ships code changes. |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Focused application: archetypes.md says universal entity criteria may be inappropriate, and Discourse is a discussion product, not a business-object platform. Applied by the fixed per-archetype rule in ../_method.md. |
| MAL-02 Field definitions carry type and validation | assessed | 2 |  |  | A |  | Admins define typed user fields (text, confirm, dropdown, multiselect) with required, editable and visibility flags (app/models/user_field.rb); only the user entity family has them, so the single-entity cap applies. |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Focused application: universal entity criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Focused application: generic per-entity API is a universal entity criterion (fixed per-archetype rule). |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Focused application: runtime API reshaping presupposes defined entities (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A |  | OpenAPI documentation generated from request specs (lib/tasks/api_docs.rake); MCP tools declare output schemas (lib/discourse_mcp/output_schema.rb). No typed client generation or dry-run. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A |  | Themes and components are installed and configured by admins with typed, schema-validated settings and settings migrations (app/models/theme_setting.rb, theme_settings_migration.rb) and can be previewed on the live site before activation (app/controllers/admin/themes_controller.rb:12-16); page layout itself is theme code, not data. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Focused application: generic widgets from entity definitions presuppose defined entities (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 3 |  |  | A |  | Admin colour-scheme editor (app/models/color_scheme.rb), per-site overrides for every UI string (app/models/translation_override.rb, theme_translation_override.rb), and a translation pipeline covering thousands of locale files (translator.yml). |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 |  | 3 | A |  | By default: the automation plugin and watched words with a test mode (plugins/automation, app/models/watched_word.rb). The workflows plugin with versions, validators and test sessions is an off-by-default beta (plugins/discourse-workflows/config/settings.yml:4-11). |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 3 | 4 |  | A |  | Admin webhooks with typed event subscriptions, delivery logs (app/models/web_hook_event.rb), automatic retries (MAX_RETRY_COUNT 4, app/jobs/regular/emit_web_hook_event.rb:8) and redelivery (app/models/redelivering_webhook_event.rb). |
| MAL-12 Sandboxed server-side hooks | assessed | 2 |  | 3 | A |  | By default, sandboxed code runs only as discourse-ai tool scripts with timeouts (plugins/discourse-ai/lib/agents/tool_runner.rb:44-58), and discourse-ai is off by default; the beta workflows Code node adds a sandbox with a resource budget (js_sandbox.rb, sandbox_budget.rb). |
| MAL-13 Plugin lane breadth | assessed | 3 |  |  | A |  | Ruby and JavaScript plugins through a versioned plugin API, theme components with typed settings, site settings, text overrides, watched words, automations, SQL badges, user fields and custom sidebar sections. |
| MAL-14 Runtime isolation and dependency control | assessed | 2 |  |  | A |  | Themes run under a Content Security Policy; AI tool scripts and beta workflow code nodes are sandboxed; plugins run in-process with full trust. |
| MAL-15 Developer loop | assessed | 2 | 3 |  | A |  | Theme preview on the live site, the /logs viewer for admins and a Docker development environment (bin/docker/boot_dev); the theme CLI that syncs to a live site is in another repository. |
| MAL-16 Canonical data model with a mapping layer | assessed | 1 |  |  | A |  | Integrations are bespoke plugins (discourse-zendesk-plugin, discourse-github, import scripts); no canonical integration model. |
| MAL-17 Connector definition or SDK | assessed | 2 |  |  | A |  | Chat integration has a provider framework (plugins/discourse-chat-integration/lib/discourse_chat_integration/provider) and beta workflows have typed credential definitions (credential_types); no general connector SDK with lifecycle. |
| MAL-18 Stable versioned contracts | assessed | 1 | 2 |  | A |  | No path versioning; plugin-API deprecations are structured, but the HTTP API has no deprecation windows. |
| MAL-19 Machine-readable capability surface for agents | assessed | 3 |  |  | A |  | Core MCP server with typed tools and output schemas (lib/discourse_mcp, tools for topics, posts, search, users, themes, site settings and moderation), per-primitive required scopes and annotations (primitive.rb:14-78), OAuth and group scopes and a catalog; plugins register further tools. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 1 |  | 3 | A |  | By default only the tutorial narrative bot is conversational (plugins/discourse-narrative-bot). With discourse-ai on (default false), AI agents answer members with retrieval and tools, and admins author workflows in natural language. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A |  | User actions, visits, post timings and search logs are recorded as they happen and feed product features such as top topics and admin reports. Scored at the lower reading under rule 11 because: Engagement tables, not a per-feature event stream. |
| LRN-02 Structured learning signals | assessed | 2 |  |  | A |  | Typed flags feed a review queue with triage (app/models/reviewable.rb); they concern content, not the product's definitions and versions. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A |  | Logster records server and browser errors in an admin UI (Gemfile:220); problem checks raise configuration issues (app/services/problem_check). |
| LRN-04 Cross-source mining inside the product | assessed | 2 | 3 |  | A |  | Data Explorer runs saved SQL over the whole site database including usage, moderation and support data (plugins/discourse-data-explorer); no continuous mining. |
| LRN-05 Automated diagnosis | assessed | 2 |  |  | A |  | Logster groups identical errors and attaches the environment of each occurrence. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 2 |  |  | A |  | Problem checks raise admin notices recommending configuration fixes (app/services/problem_check): recommendations for one area. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 2 |  |  | A |  | Problem checks run on a schedule and raise configuration recommendations (app/services/problem_check); they are rules, not learning from experience. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 |  | 2 | A |  | By default, changes are reviewed by people. With the workflows beta, AI proposals are validated with workflow_validate_patch before an admin applies them. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A |  | No binding of changes to baselines or metrics. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A |  | An accessibility service and dialog components exist (frontend/discourse/tests/helpers/qunit-helpers.js:102 imports discourse/services/a11y); no automated accessibility scanning in CI. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A |  | Staff action logs record admin actions including site-setting changes with old and new values (app/services/staff_action_logger.rb) with an admin UI; post revisions and reviewable history; an MCP audit log with retention (config/site_settings.yml:4535). Ordinary entity mutations are not all audited. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 | 3 |  | A |  | User archive export (app/jobs/regular/export_user_archive.rb), anonymisation and deletion (app/services/user_anonymizer.rb, user_destroyer.rb) and purge settings; coded for the user family, not driven by field tags. |
| GOV-04 Security as infrastructure | assessed | 2 |  |  | A |  | Central Guardian permission model with group and category permissions and scoped API keys (app/models/api_key_scope.rb); Dependabot configured (.github/dependabot.yml); no SAST in CI. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A |  | Site-setting history in staff logs, revertible post revisions, versioned published workflows (workflow_snapshot.rb) and git-backed remote themes; no admin rollback for settings or themes. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 1 |  | 2 | A |  | By default, admins change settings and themes directly. With the beta workflows plugin on, an AI author writes risk-rated draft proposals that are validated and applied by an admin (plugins/discourse-workflows/lib/discourse_workflows/ai_workflow_author.rb:39-67). |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 | 2 |  | A |  | Admins apply changes directly; the upcoming-changes framework controls rollout of Discourse's own features by status and group (lib/upcoming_changes, plugins/discourse-workflows/config/settings.yml:4-11). |
| GOV-08 Upgrade safety | assessed | 3 |  |  | A |  | Plugins and themes pin compatible commits per core version (lib/version_compatibility.rb, lib/tasks/compatibility.rake); a structured deprecation API with since and drop_from (lib/discourse.rb:1185-1189); theme settings migrations (app/models/theme_settings_migration.rb). |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A |  | Granular API key scopes, user API key scopes and MCP OAuth scopes (app/models/api_key_scope.rb, user_api_key_scope.rb, mcp_oauth_authorization_scope.rb); MCP audit log; rate limiters. Idempotency is only an annotation hint; no dry-run. |
| GOV-10 Bounded self-change | not_applicable | excluded |  |  | - |  | No self-change path by default: discourse-ai and the workflows AI author are off. |
| GOV-11 Learning-input integrity | not_applicable | excluded |  |  | - |  | No self-change path by default. |
| EXP-01 Kernel concepts are domain-neutral | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). Note that Discourse's kernel of users, groups, posts, topics, permissions and chat channels matches the rubric's level-3 kernel almost word for word. |
| EXP-02 A new domain is expressible without kernel change | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). Chat, events, assignment, subscriptions and voting ship as code plugins on an unchanged core. |
| EXP-03 A domain ships as an installable bundle | not_applicable | excluded |  |  | - |  | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| EXP-04 Unmet-demand sensing | assessed | 2 |  |  | A |  | Search logs record terms and whether a result was clicked, with an admin report of searches without results (app/models/search_log.rb). |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 2 |  |  | A |  | Features and plugins can be enabled for selected groups, for example through upcoming changes and group settings (lib/upcoming_changes); there is no success metric or keep-or-kill record. |

Facets: I implemented, T tested, O operated.

