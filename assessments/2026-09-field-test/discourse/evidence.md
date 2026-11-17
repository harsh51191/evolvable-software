# Discourse evidence

Read at github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Posts, users and settings in PostgreSQL; uploads on disk or S3.
- **schema_changes**: true. Rails migrations (db/migrate, 1,765 files) change the schema on every upgrade.
- **multi_tenant**: true. Multisite hosting serves several forums from one deployment, each with its own database, admins and members (RailsMultisite; config/multisite.yml.production-sample), with restore specs covering multisite. Groups and private categories inside one site do not count.
- **hosted_service**: true. Puma web processes and Sidekiq workers run as long-lived services.
- **machine_actions**: true. The admin API with scoped API keys changes content and settings (app/models/api_key_scope.rb).
- **agent_mutations**: false. False by default under the v0.7 definition: no AI writes or drafts changes to settings, categories, themes or automations unless discourse-ai (default false, plugins/discourse-ai/config/settings.yml:2-3) or the workflows AI author (beta, default false) is switched on.
- **evolution_auto_apply**: false. Admins apply changes directly; nothing applies definition changes automatically by default.
- **definition_change_path**: true. Site settings, themes, categories and automations are definitions.
- **code_release_path**: false. No first-party evolution system or AI writes and activates code; theme and plugin code is written by people.
- **ai_features**: false by default, true with opt-in settings. discourse-ai ships bundled but discourse_ai_enabled defaults to false (plugins/discourse-ai/config/settings.yml:2-3).
- **ai_data_access**: false by default, true with opt-in settings. Off by default; when enabled, agents search and read topics and RAG documents.
- **ai_actions**: false by default, true with opt-in settings. Off by default; when enabled, agent tools edit posts, change categories and site settings (plugins/discourse-ai/lib/agents/tools).

## Kinds of change

- **How the forum behaves and what it says (settings and wording)** (`site-settings`, main, made by site admins): reach **1 Self-serve**, confidence medium. Admins change typed, validated site settings and override any interface text in the admin UI with no deploy. Undo: every setting change is logged with its previous and new value (app/services/staff_action_logger.rb:280-296), a setting can be reset to its default, and text overrides log old and new text (:513) and can be reverted to the default; there is no one-step revert to an earlier value, so undo is setting the logged value back.
- **Categories and who can see or post in them** (`categories-permissions`, main, made by site admins and moderators): reach **1 Self-serve**, confidence medium. Admins create categories and set group permissions in the UI under the Guardian model. Undo: each changed category attribute, custom field and permission set is logged with previous and new values (app/services/staff_action_logger.rb:741-776), and creation and deletion are logged (:778-815); undo is editing back from the log, not a revert action.
- **Look and layout (themes and components)** (`themes-components`, main, made by site admins and designers): reach **1 Self-serve**, confidence medium. Admins install themes and components, configure typed settings and preview a theme on the live site before activating it (app/controllers/admin/themes_controller.rb:12-16). Undo: switch the default theme back or disable a component (logged, staff_action_logger.rb:464-482); setting changes are logged with previous values (:484-511) and theme edits store the old theme JSON with field values (:440-452); remote themes come from git. There is no revert button for local theme edits.
- **Automatic rules (automations)** (`automations`, not main, made by site admins): reach **1 Self-serve**, confidence low. The bundled automation plugin is switched on by a site setting (plugins/automation/config/settings.yml:2-3, default false) and admins then define scripts and triggers in the UI. Undo: an automation can be disabled (enabled flag, plugins/automation/app/models/discourse_automation/automation.rb:151, :261) or deleted; edits keep no history.
- **New features from plugins** (`plugins`, not main, made by site owners): reach **0 Engineers only**, confidence high. Bundled plugins are switched on by site settings, but adding a plugin means editing the container definition and rebuilding (docs/INSTALL-cloud.md:204-220, 'Install Plugins' link at :340): a deploy run by whoever operates the server. Engineers only.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md, AI-AGENTS.md, CLAUDE.md, .agents/skills, .claude/skills, .cursor and .github/instructions/copilot.instructions.md. No agent workflow in CI (searched .github/workflows for claude, codex, copilot, anthropic and openai).
- **Proven, Request → Release**: not evidenced. Searched: Repository at the pinned commit: release-notes and release workflows, staff action log and backup code, docs/. Operating records of real changes going through a Discourse site's Request → Release loop live in running sites (staff action logs), not in the repository.
- **Proven, Issue → Fix**: not evidenced. Searched: Repository at the pinned commit: release-notes and release workflows, staff action log and backup code, docs/. Operating records of real changes going through a Discourse site's Issue → Fix loop live in running sites (staff action logs), not in the repository.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: Repository at the pinned commit: release-notes and release workflows, staff action log and backup code, docs/. Operating records of real changes going through a Discourse site's Opportunity → Expansion loop live in running sites (staff action logs), not in the repository.

Confidence for criteria whose score did not change in the v0.7 migration was assigned at migration from the recorded evidence; confidence for new and changed readings (kinds of change, LRN-10 and every re-read criterion) comes from re-reading the source at the pinned commit.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **2** (grade A, confidence medium). PostgreSQL full-text search (lib/search.rb) and hand-tuned list queries; custom fields are not filterable at scale.
- **ARC-02 Safe schema and data migrations**: **3** (grade A, confidence high), facets: implemented, tested. SafeMigrate blocks destructive migrations, and Migration::ColumnDropper and TableDropper defer drops so schema changes are expand-and-contract (lib/migration/safe_migrate.rb, column_dropper.rb, table_dropper.rb); post-deploy migrations separate destructive steps; migrations run in CI.

### Scale

- **ARC-03 Horizontal scale of services**: **2** (grade A, confidence medium), facets: implemented. Stateless Puma processes over PostgreSQL and Redis; scale-out is documented in the separate discourse_docker repository rather than here.
  - Higher reading 3: Large hosted deployments run many web processes over shared stores.
- **ARC-04 Reliable asynchronous work**: **2** (grade A, confidence medium), facets: implemented, tested. Sidekiq jobs with retries and a dead set, and MiniScheduler runs scheduled jobs once across processes with a Redis lock (Gemfile:104-105); idempotency is left to each job.
  - Higher reading 3: Retries, dead-lettering, observability and run-once scheduling are all present.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **2** (grade A, confidence medium), facets: implemented, tested. Multisite hosting with a database per site and pervasive rate limiters; no noisy-neighbour detection or isolation verification in the repository.
  - Higher reading 3: Per-site data isolation and per-user limits are strong; only detection is missing.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **2** (grade A, confidence medium). Benchmark script (script/bench.rb); no documented per-surface limits or CI budgets.
- **ARC-07 Service objectives defined and monitored**: **1** (grade A, confidence medium). No published objectives in this repository; the prometheus exporter is a separate plugin not bundled here.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence high). Outbound requests go through FinalDestination with timeouts, and safe mode disables plugins and themes for a session (config/routes.rb:2036). Plugins run in-process.
  - AI-qualified reading: **0** (grade A, confidence medium), **2** with opt-in settings. Off by default.
- **ARC-09 Backup, restore and recovery**: **2** (grade A, confidence high), facets: implemented, tested. Built-in backup and restore of the database (data, site settings, themes) and uploads to local or S3 stores, with restore specs for both, including multisite (lib/backup_restore, spec/lib/backup_restore/database_restorer_spec.rb, uploads_restorer_spec.rb). Secrets live in the deployment environment, outside the product. No recovery objectives are stated (level 4). Scheduled work: restore pauses Sidekiq, clears its queues and limits email to staff (lib/backup_restore/restorer.rb:55-59, 132-135), and topic timers re-check the scheduling user's current permissions when they run (app/jobs/regular/close_topic.rb:14, publish_topic_to_category.rb:7-13). No view lists upcoming timers and the user each runs as, so scheduled work stays at 2 and the criterion reads 2.
  - Inventory: data 3, definitions 3, files 3, secrets n/a, schedules 2

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **1** (grade A, confidence medium). Communities collect requests as topics; the bundled topic-voting plugin ranks them (plugins/discourse-topic-voting). They are not linked to the settings or screens involved.
  - Higher reading 2: Voting adds structure to requests.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Build

- **DEL-02 Layers deploy independently**: **1** (grade A, confidence medium). Rails and Ember monolith deployed as one application; container tooling lives in a separate repository.
- **DEL-03 Module boundaries enforced by tooling**: **1** (grade A, confidence medium). Plugin API is a contract, but internal module boundaries are convention; no architectural lint.
- **DEL-04 AI implementation lane**: **0** (grade A, confidence medium), **2** with opt-in settings. By default there is no AI authoring lane; the beta workflows AI author is one when enabled.
  - AI-qualified reading: **0** (grade A, confidence medium), **2** with opt-in settings. Off by default.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence medium). Tests, linting and migration tests run on every pull request with no draft filter (.github/workflows/tests.yml:3-26, linting.yml, migration-tests.yml); no accessibility or security scan in CI.
  - Higher reading 3: Every code change class except accessibility and SAST is checked.
- **DEL-06 Verification surface**: **2** (grade A, confidence high). Health endpoint /srv/status (config/routes.rb:135) and version through the about endpoint; no deployed-configuration snapshot.
- **DEL-07 Environment reproducibility**: **2** (grade A, confidence medium). Scripted Docker development environment (bin/docker/boot_dev), test database setup, and upcoming-change flags that ship features off by default; no per-change ephemeral environment in the repository.
  - Higher reading 3: Flags-off-first is present; ephemeral environments may exist in private infrastructure.
- **DEL-08 Machine verifiability**: **2** (grade A, confidence medium). System specs drive browser journeys (spec/system) alongside QUnit tests; no changed-path to journey map or adoption instrumentation at ship.

### Release

- **DEL-09 Staged exposure**: **2** (grade A, confidence medium). The upcoming-changes framework releases Discourse's own features to opted-in groups first (lib/upcoming_changes); site setting changes are not staged.
  - Higher reading 3: Group-based rollout covers code changes by default.
- **DEL-10 Kill switch**: **2** (grade A, confidence high). Site settings switch features and plugins off at runtime, and safe mode disables customisations per session (config/routes.rb:2036-2037).
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: No first-party evolution system ships code changes.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Focused application: archetypes.md says universal entity criteria may be inappropriate, and Discourse is a discussion product, not a business-object platform. Applied by the fixed per-archetype rule in ../_method.md. If counted: 1.
- **MAL-02 Field definitions carry type and validation**: **3** (grade A, confidence medium). Admins define typed user fields (text, confirm, dropdown, multiselect) with required, editable and visibility flags (app/models/user_field.rb); only the user entity family has them, so the single-entity cap applies.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Focused application: generic per-entity API is a universal entity criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Focused application: runtime API reshaping presupposes defined entities (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A, confidence medium). OpenAPI documentation generated from request specs (lib/tasks/api_docs.rake); MCP tools declare output schemas (lib/discourse_mcp/output_schema.rb). No typed client generation or dry-run.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A, confidence medium). Themes and components are installed and configured by admins with typed, schema-validated settings and settings migrations (app/models/theme_setting.rb, theme_settings_migration.rb) and can be previewed on the live site before activation (app/controllers/admin/themes_controller.rb:12-16); page layout itself is theme code, not data.
  - Higher reading 3: Admins do override and preview presentation per site; only the 'layout as data' clause fails.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions presuppose defined entities (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **3** (grade A, confidence medium). Admin colour-scheme editor (app/models/color_scheme.rb), per-site overrides for every UI string (app/models/translation_override.rb, theme_translation_override.rb), and a translation pipeline covering thousands of locale files (translator.yml).

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A, confidence high), **3** with opt-in settings. By default: the automation plugin and watched words with a test mode (plugins/automation, app/models/watched_word.rb). The workflows plugin with versions, validators and test sessions is an off-by-default beta (plugins/discourse-workflows/config/settings.yml:4-11).
- **MAL-11 Event model with webhooks or subscriptions and retry**: **3** (grade A, confidence medium). Admin webhooks with typed event subscriptions, delivery logs (app/models/web_hook_event.rb), automatic retries (MAX_RETRY_COUNT 4, app/jobs/regular/emit_web_hook_event.rb:8) and redelivery (app/models/redelivering_webhook_event.rb).
  - Higher reading 4: Replay exists; event schemas are not generated from definitions.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence high), **3** with opt-in settings. By default, sandboxed code runs only as discourse-ai tool scripts with timeouts (plugins/discourse-ai/lib/agents/tool_runner.rb:44-58), and discourse-ai is off by default; the beta workflows Code node adds a sandbox with a resource budget (js_sandbox.rb, sandbox_budget.rb).

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A, confidence medium). Ruby and JavaScript plugins through a versioned plugin API, theme components with typed settings, site settings, text overrides, watched words, automations, SQL badges, user fields and custom sidebar sections.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A, confidence medium). Themes run under a Content Security Policy; AI tool scripts and beta workflow code nodes are sandboxed; plugins run in-process with full trust.
- **MAL-15 Developer loop**: **2** (grade A, confidence medium). Theme preview on the live site, the /logs viewer for admins and a Docker development environment (bin/docker/boot_dev); the theme CLI that syncs to a live site is in another repository.
  - Higher reading 3: Preview against the real site and logs are already available to theme developers.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **1** (grade A, confidence medium). Integrations are bespoke plugins (discourse-zendesk-plugin, discourse-github, import scripts); no canonical integration model.
- **MAL-17 Connector definition or SDK**: **2** (grade A, confidence medium). Chat integration has a provider framework (plugins/discourse-chat-integration/lib/discourse_chat_integration/provider) and beta workflows have typed credential definitions (credential_types); no general connector SDK with lifecycle.
- **MAL-18 Stable versioned contracts**: **1** (grade A, confidence medium). No path versioning; plugin-API deprecations are structured, but the HTTP API has no deprecation windows.
  - Higher reading 2: The API is documented through generated OpenAPI docs.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **3** (grade A, confidence high). Core MCP server with typed tools and output schemas (lib/discourse_mcp, tools for topics, posts, search, users, themes, site settings and moderation), per-primitive required scopes and annotations (primitive.rb:14-78), OAuth and group scopes and a catalog; plugins register further tools.
  - AI-qualified reading: **3** (grade A, confidence medium). Core MCP server with typed tools and scopes (lib/discourse_mcp).
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **1** (grade A, confidence medium), **3** with opt-in settings. By default only the tutorial narrative bot is conversational (plugins/discourse-narrative-bot). With discourse-ai on (default false), AI agents answer members with retrieval and tools, and admins author workflows in natural language.
  - AI-qualified reading: **0** (grade A, confidence medium), **3** with opt-in settings. Off by default.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A, confidence medium). User actions, visits, post timings and search logs are recorded as they happen and feed product features such as top topics and admin reports. Scored at the lower reading under rule 11 because: Engagement tables, not a per-feature event stream.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-02 Structured learning signals**: **2** (grade A, confidence medium). Typed flags feed a review queue with triage (app/models/reviewable.rb); they concern content, not the product's definitions and versions.
- **LRN-03 User-issue detection**: **2** (grade A, confidence high). Logster records server and browser errors in an admin UI (Gemfile:220); problem checks raise configuration issues (app/services/problem_check).
- **LRN-04 Cross-source mining inside the product**: **2** (grade A, confidence medium). Data Explorer runs saved SQL over the whole site database including usage, moderation and support data (plugins/discourse-data-explorer); no continuous mining.
  - Higher reading 3: Usage and support data are already joinable and queryable inside the product.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A, confidence medium). Logster groups identical errors and attaches the environment of each occurrence.
  - AI-qualified reading: **0** (grade A, confidence medium). Logster grouping is rule-based.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A, confidence medium). Problem checks raise admin notices recommending configuration fixes (app/services/problem_check): recommendations for one area.
  - AI-qualified reading: **0** (grade A, confidence medium). Problem checks are rules.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **2** (grade A, confidence medium). Problem checks run on a schedule and raise configuration recommendations (app/services/problem_check); they are rules, not learning from experience.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.
- **LRN-08 Learned changes are validated before they take effect**: **0** (grade A, confidence medium), **2** with opt-in settings. Re-scored 1 to 0 under the v0.7 boundary. By default Discourse produces no learned or AI-made changes: discourse-ai and the workflows AI author are off (plugins/discourse-ai/config/settings.yml:2-3, plugins/discourse-workflows/config/settings.yml:2-14), and problem checks are rule-based notices that admins act on by hand, whose checks are DEL-05. Nothing specific to learned or AI-made changes would apply. With the workflows beta on, AI proposals are validated with workflow_validate_patch before an admin applies them (plugins/discourse-workflows/lib/discourse_workflows/ai_workflow_author.rb:39-67), which is the opt-in 2.
  - AI-qualified reading: **not applicable**. agent_mutations is false.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A, confidence medium). No binding of changes to baselines or metrics.
- **LRN-10 The improvement loop improves itself**: **0** (grade A, confidence medium). The checks that govern change are code: setting type validators, SafeMigrate and the deferred droppers (lib/migration/safe_migrate.rb), and CI (.github/workflows/tests.yml). There is no change policy object (GOV-07 1). With discourse-ai on, its evaluation harness and judge are code with datasets outside the repository (plugins/discourse-ai/evals/lib/eval.rb, judge.rb) and are not run in CI. Model accuracy against moderator decisions (app/models/model_accuracy.rb) measures moderation classifiers, not the checks that govern changes to Discourse. Nothing links a failure to the check that missed it.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A, confidence medium). An accessibility service and dialog components exist (frontend/discourse/tests/helpers/qunit-helpers.js:102 imports discourse/services/a11y); no automated accessibility scanning in CI.
  - Higher reading 2: Kit-level accessibility utilities exist; the anchors bundle kit and scans.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A, confidence medium). Staff action logs record admin actions including site-setting changes with old and new values (app/services/staff_action_logger.rb) with an admin UI; post revisions and reviewable history; an MCP audit log with retention (config/site_settings.yml:4535). Ordinary entity mutations are not all audited.
  - Higher reading 3: Configuration changes, approvals in the review queue and admin UI are covered; only entity-wide coverage fails.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence medium). User archive export (app/jobs/regular/export_user_archive.rb), anonymisation and deletion (app/services/user_anonymizer.rb, user_destroyer.rb) and purge settings; coded for the user family, not driven by field tags.
  - Higher reading 3: Admin-triggered export and erasure exist across the user's content; only tag-driven coverage is missing.
- **GOV-04 Security as infrastructure**: **2** (grade A, confidence medium). Central Guardian permission model with group and category permissions and scoped API keys (app/models/api_key_scope.rb); Dependabot configured (.github/dependabot.yml); no SAST in CI.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A, confidence medium). Site-setting history in staff logs, revertible post revisions, versioned published workflows (workflow_snapshot.rb) and git-backed remote themes; no admin rollback for settings or themes.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **1** (grade A, confidence high), **2** with opt-in settings. By default, admins change settings and themes directly. With the beta workflows plugin on, an AI author writes risk-rated draft proposals that are validated and applied by an admin (plugins/discourse-workflows/lib/discourse_workflows/ai_workflow_author.rb:39-67).
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A, confidence medium). Admins apply changes directly; the upcoming-changes framework controls rollout of Discourse's own features by status and group (lib/upcoming_changes, plugins/discourse-workflows/config/settings.yml:4-11).
  - Higher reading 2: Upcoming changes is a narrow policy for feature rollout.
- **GOV-08 Upgrade safety**: **3** (grade A, confidence high). Plugins and themes pin compatible commits per core version (lib/version_compatibility.rb, lib/tasks/compatibility.rake); a structured deprecation API with since and drop_from (lib/discourse.rb:1185-1189); theme settings migrations (app/models/theme_settings_migration.rb).

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence medium). Granular API key scopes, user API key scopes and MCP OAuth scopes (app/models/api_key_scope.rb, user_api_key_scope.rb, mcp_oauth_authorization_scope.rb); MCP audit log; rate limiters. Idempotency is only an annotation hint; no dry-run.
  - Higher reading 3: Scoped identity, audit and rate limits are strong; only idempotency keys and dry-run are missing.
  - AI-qualified reading: **0** (grade A, confidence medium), **3** with opt-in settings. Off by default.
- **GOV-10 Bounded self-change**: **not applicable**. No self-change path by default: discourse-ai and the workflows AI author are off. If counted: 2.
  - AI-qualified reading: **not applicable**. GOV-10 is not applicable.
- **GOV-11 Learning-input integrity**: **not applicable**. No self-change path by default. If counted: 1.
  - AI-qualified reading: **not applicable**. GOV-11 is not applicable.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). Note that Discourse's kernel of users, groups, posts, topics, permissions and chat channels matches the rubric's level-3 kernel almost word for word. If counted: 2.
- **EXP-02 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). Chat, events, assignment, subscriptions and voting ship as code plugins on an unchanged core. If counted: 2.
- **EXP-03 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.

### Discover

- **EXP-04 Unmet-demand sensing**: **2** (grade A, confidence medium). Search logs record terms and whether a result was clicked, with an admin report of searches without results (app/models/search_log.rb).
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence medium). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **2** (grade A, confidence medium). Features and plugins can be enabled for selected groups, for example through upcoming changes and group settings (lib/upcoming_changes); there is no success metric or keep-or-kill record.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence medium). Embeddings, semantic search and RAG fragments kept up to date by jobs (app/models/rag_document_fragment.rb, embedding_definition.rb); agents search and read topics with citations.
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A, confidence high), facets: implemented, tested. Agent tools read with an anonymous Guardian unless private reading is allowed, then with the user's Guardian (lib/agents/tools/read.rb:51-62); 34 tools use Guardian checks, with specs.

### Quality

- **AIR-05 Offline AI evaluation**: **2** (grade A, confidence medium). An evaluation harness with an LLM judge (plugins/discourse-ai/evals/lib/eval.rb, judge.rb) run from the command line; datasets live outside this repository.
- **AIR-06 Regression gating before release**: **1** (grade A, confidence medium). Evaluations are not run in CI; prompt and model changes are reviewed manually.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A, confidence high), facets: implemented, tested. Every LLM call is logged with user, topic, model, feature, request and response payloads and tokens (app/models/ai_api_audit_log.rb, migration 20230424055354); tool actions are recorded and can be reviewed (ai_tool_action.rb, reviewable_ai_tool_action.rb).

### Operations

- **AIR-01 Model and provider portability and resilience**: **2** (grade A, confidence medium). Admins configure LLM models per provider and assign them per agent and feature (app/models/llm_model.rb); no fallback when a model fails. Scored as shipped, with discourse-ai enabled.
- **AIR-02 AI usage and per-customer cost controls**: **3** (grade A, confidence medium). Per-group LLM quotas on tokens and usages per period, credit allocations and daily usage (app/models/llm_quota.rb, llm_credit_allocation.rb, llm_credit_daily_usage.rb), with admin screens.
- **AIR-08 Production quality, drift and feedback monitoring**: **2** (grade A, confidence medium). Accuracy of AI triage against moderator decisions and spam logs are recorded per model and feature (app/models/model_accuracy.rb, ai_spam_log.rb); no drift alerts.
