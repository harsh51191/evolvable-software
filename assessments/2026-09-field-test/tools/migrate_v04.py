#!/usr/bin/env python3
"""One-off migration of the v0.3 field-test inputs to EVOLVE v0.4.

What it does, per system, in order:
  1. Renames every criterion to its EVOLVE id (A1 -> MAL-01, M3 -> DEL-04, ...).
  2. Flips every downward alternate (rubric rule 11: score the lower reading and
     record the higher one). The original evidence is kept and the note says so.
  3. Declares the seven scope facts, each with evidence.
  4. Marks criteria switched off by a false scope fact not_applicable, keeping the
     earlier score as if_applicable.
  5. Applies re-scores of existing criteria that the new definitions change.
  6. Adds the 17 new criteria.
  7. Adds evidence facets to depth-capped criteria read at 3 or more, and
     coverage inventories where a rule needs them.

Every changed or added entry carries its evidence. The script refuses to run
twice. Evidence was read at the tips named in each assessment's source.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYSTEMS = ["frappe", "directus", "discourse", "posthog", "n8n", "dify", "librechat",
           "hermes-agent", "openclaw", "opencode", "openhands"]

MAP = {}
def _seq(olds, prefix):
    for i, o in enumerate(olds, 1):
        MAP[o] = f"{prefix}-{i:02d}"
_seq(["A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3", "D1", "D2", "D3",
      "I1", "I2", "I3", "N1", "N2", "N3", "K1", "K2"], "MAL")
_seq(["E1", "E2", "E3", "E4", "F1", "F2", "F3", "F4", "K3"], "GOV")
MAP.update({"G1": "ARC-01", "G2": "ARC-05", "G3": "ARC-06",
            "H1": "DEL-02", "H2": "DEL-03", "M3": "DEL-04", "H3": "DEL-05", "L1": "DEL-06", "L2": "DEL-07", "L3": "DEL-08",
            "J1": "LRN-01", "J2": "LRN-02", "J3": "LRN-04", "M1": "LRN-06", "P1": "LRN-07", "P2": "LRN-08", "M4": "LRN-09",
            "O1": "EXP-01", "O2": "EXP-02", "O3": "EXP-03"})
assert len(MAP) == 49

GATED = {"ARC-01": ["persistent_data"], "ARC-02": ["schema_changes"], "ARC-03": ["hosted_service"],
         "ARC-04": ["hosted_service"], "ARC-05": ["multi_tenant"], "ARC-06": ["hosted_service"],
         "ARC-07": ["hosted_service"], "ARC-09": ["persistent_data"], "DEL-11": ["code_release_path"],
         "GOV-05": ["definition_change_path"], "GOV-09": ["machine_actions"],
         "GOV-10": ["agent_mutations", "evolution_auto_apply"], "GOV-11": ["agent_mutations", "evolution_auto_apply"]}

I, IT, ITO = ((True, False, False), (True, True, False), (True, True, True))


def a(score, evidence, grade="A", **extra):
    return {"status": "assessed", "score": score, "grade": grade, "evidence": evidence, **extra}


def up(score, evidence, note, grade="A", **extra):
    """Assessed with a higher alternate reading."""
    return a(score, evidence, grade, alt_score=score + 1, alt_note=note, **extra)


def f(value, evidence):
    return {"value": value, "evidence": evidence}


# ---------------------------------------------------------------- scope facts

FACTS = {
 "frappe": {
  "persistent_data": f(True, "Every site keeps documents in MariaDB or PostgreSQL and files on disk."),
  "schema_changes": f(True, "Creating or editing a DocType alters its table at runtime (frappe/database/schema.py:479-485), and bench migrate applies patches (frappe/patches.txt)."),
  "multi_tenant": f(True, "One bench serves several sites, each with its own database (multi-site benches)."),
  "hosted_service": f(True, "Gunicorn web workers, RQ workers, a scheduler and a socket.io server run as long-lived services."),
  "machine_actions": f(True, "The REST API and RPC methods change documents and DocTypes with per-user API keys (frappe/api)."),
  "agent_mutations": f(False, "No first-party AI or agent changes Frappe definitions in this repository."),
  "evolution_auto_apply": f(False, "Every definition change is made by a person with the right role; nothing applies changes automatically."),
  "definition_change_path": f(True, "DocTypes, workflows, print formats and settings are definitions."),
  "code_release_path": f(False, "No first-party evolution system ships code changes; releases are made by engineers."),
 },
 "directus": {
  "persistent_data": f(True, "Collections are database tables and files go to configured storage drivers."),
  "schema_changes": f(True, "The data model editor, schema apply and the AI collection and field tools alter tables at runtime (api/src/services/fields.ts, api/src/ai/tools/collections)."),
  "multi_tenant": f(False, "One project per deployment; isolation inside a project is by roles and policies, not tenants."),
  "hosted_service": f(True, "The API is a long-lived Node service with optional Redis-backed synchronisation (api/src/synchronization.ts)."),
  "machine_actions": f(True, "REST and GraphQL APIs and an MCP server change items and schema (api/src/ai/mcp)."),
  "agent_mutations": f(True, "The AI assistant changes collections, fields, flows and items through tools (api/src/ai/tools)."),
  "evolution_auto_apply": f(False, "Mutating AI tool calls require approval unless a user sets a tool to always-allow (api/src/ai/tools/registry.ts:198-214)."),
  "definition_change_path": f(True, "Collections, fields, flows, roles and settings are definitions."),
  "code_release_path": f(False, "The AI lane changes definitions, not Directus code."),
 },
 "discourse": {
  "persistent_data": f(True, "Posts, users and settings in PostgreSQL; uploads on disk or S3."),
  "schema_changes": f(True, "Rails migrations (db/migrate, 1,765 files) change the schema on every upgrade."),
  "multi_tenant": f(True, "Multisite hosting serves several forums from one deployment, each with its own database."),
  "hosted_service": f(True, "Puma web processes and Sidekiq workers run as long-lived services."),
  "machine_actions": f(True, "The admin API with scoped API keys changes content and settings (app/models/api_key_scope.rb)."),
  "agent_mutations": f(False, "By default no AI changes Discourse definitions: discourse-ai and the workflows AI author are off by default."),
  "evolution_auto_apply": f(False, "Admins apply changes directly; nothing applies definition changes automatically by default."),
  "definition_change_path": f(True, "Site settings, themes, categories and automations are definitions."),
  "code_release_path": f(False, "No first-party evolution system ships code changes."),
 },
 "posthog": {
  "persistent_data": f(True, "Events in ClickHouse, configuration in PostgreSQL, recordings in object storage."),
  "schema_changes": f(True, "Django and ClickHouse migrations, plus property materialisation that adds columns at runtime (ee/clickhouse/materialized_columns/columns.py)."),
  "multi_tenant": f(True, "Organisations and projects share one deployment with access control and quotas."),
  "hosted_service": f(True, "Django web, Celery and Temporal workers, Node ingestion and Rust capture services."),
  "machine_actions": f(True, "The API with scoped personal keys and an MCP server change PostHog objects (posthog/scopes.py, services/mcp)."),
  "agent_mutations": f(True, "PostHog AI creates and edits insights, dashboards and other configured objects (ee/hogai)."),
  "evolution_auto_apply": f(False, "PostHog AI changes are made on request in a conversation; weekly property materialisation applies without approval (posthog/tasks/scheduled.py:927), but it is scheduled maintenance, not a change from the evolution loop."),
  "definition_change_path": f(True, "Insights, dashboards, feature flags, actions and approval policies are definitions."),
  "code_release_path": f(False, "Tasks and Stamphog act on customers' repositories (products/stamphog); no first-party lane ships PostHog code changes."),
 },
 "n8n": {
  "persistent_data": f(True, "Workflows, credentials, executions and data tables in the database."),
  "schema_changes": f(True, "TypeORM migrations (packages/@n8n/db/src/migrations) and data tables created at runtime."),
  "multi_tenant": f(False, "One instance per customer; projects separate work inside an instance but are not isolated tenants."),
  "hosted_service": f(True, "Main, worker and webhook processes run as long-lived services, with multi-main and queue mode (packages/cli/src/scaling)."),
  "machine_actions": f(True, "The public API and MCP server change workflows and credentials (packages/cli/src/modules/mcp)."),
  "agent_mutations": f(True, "The AI workflow builder and Instance AI change workflows (packages/cli/src/modules/instance-ai, workflow-builder)."),
  "evolution_auto_apply": f(False, "AI-built changes pass approvals before they apply."),
  "definition_change_path": f(True, "Workflows, credentials, variables and data tables are definitions."),
  "code_release_path": f(False, "The AI lanes change workflows, not n8n code."),
 },
 "dify": {
  "persistent_data": f(True, "Apps, datasets and logs in PostgreSQL; vectors in a vector store; files in object storage."),
  "schema_changes": f(True, "Alembic migrations (api/migrations/versions, 219 files)."),
  "multi_tenant": f(True, "Workspaces (tenants) share a deployment with per-tenant limits."),
  "hosted_service": f(True, "API, Celery worker, web, sandbox and plugin daemon run as long-lived services."),
  "machine_actions": f(True, "The console and service APIs change apps, datasets and workflows."),
  "agent_mutations": f(False, "AI generators draft prompts, code and workflow steps into the editor; a person saves and publishes (api/core/llm_generator)."),
  "evolution_auto_apply": f(False, "Every publish is a manual human action."),
  "definition_change_path": f(True, "Apps, workflows, prompts and datasets are definitions."),
  "code_release_path": f(False, "No first-party evolution system ships code changes."),
 },
 "librechat": {
  "persistent_data": f(True, "Conversations, agents, prompts and users in MongoDB."),
  "schema_changes": f(True, "Data migration scripts change stored documents and indexes (config/migrate-*.js)."),
  "multi_tenant": f(True, "A tenant isolation plugin scopes models by tenant (packages/data-schemas/src/models/plugins/tenantIsolation.coverage.spec.ts)."),
  "hosted_service": f(True, "Node API serving many users, with optional Redis (api/cache)."),
  "machine_actions": f(True, "The API changes agents, prompts and conversations for authenticated clients, and MCP tools act on users' behalf."),
  "agent_mutations": f(False, "By default no AI changes LibreChat definitions; the memory agent is commented out in librechat.example.yaml:1351-1360."),
  "evolution_auto_apply": f(False, "Definition changes are direct human actions by default."),
  "definition_change_path": f(True, "librechat.yaml, agents and prompts are definitions."),
  "code_release_path": f(False, "No first-party evolution system ships code changes."),
 },
 "hermes-agent": {
  "persistent_data": f(True, "Sessions in SQLite, plus skills, memory and configuration under HERMES_HOME."),
  "schema_changes": f(True, "The state database is versioned and migrated on start (hermes_state_schema.py, SCHEMA_VERSION)."),
  "multi_tenant": f(False, "One user per installation; profiles are separate homes, not tenants."),
  "hosted_service": f(False, "A local single-user agent; the gateway relays messaging platforms for the same user."),
  "machine_actions": f(True, "The agent's tools change its own skills, memory and configuration, and the MCP and ACP servers expose it to other clients (mcp_serve.py, acp_adapter)."),
  "agent_mutations": f(True, "The background review writes skills and memory (agent/background_review.py)."),
  "evolution_auto_apply": f(True, "background_review is on by default and skill and memory write approvals default to off (hermes_cli/config_defaults.py:814, 1320)."),
  "definition_change_path": f(True, "Skills, memory, prompts and configuration are its definitions."),
  "code_release_path": f(True, "The first-party GEPA optimiser proposes improved skills as pull requests to this repository, shipped in releases (hermes-agent-self-evolution)."),
 },
 "openclaw": {
  "persistent_data": f(True, "Skills, memory, workshop state (SQLite) and configuration on disk."),
  "schema_changes": f(True, "The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration."),
  "multi_tenant": f(False, "A personal assistant per installation; shared gateways carry several people but are not isolated tenants (VISION.md)."),
  "hosted_service": f(False, "A personal gateway daemon, not a multi-user service."),
  "machine_actions": f(True, "Agent tools and the gateway API change skills, configuration and channels."),
  "agent_mutations": f(True, "The experience review drafts and applies skill proposals (src/skills/workshop/experience-review.ts)."),
  "evolution_auto_apply": f(True, "autonomous.mode auto and approvalPolicy auto are the defaults (src/skills/workshop/config.ts:15-20)."),
  "definition_change_path": f(True, "Skills, memory and configuration are its definitions."),
  "code_release_path": f(False, "The self-improvement path changes skills, not OpenClaw code."),
 },
 "opencode": {
  "persistent_data": f(True, "Sessions and messages in a local database (packages/opencode/src/storage)."),
  "schema_changes": f(True, "Drizzle migrations for the session database (packages/opencode/migration)."),
  "multi_tenant": f(False, "A local single-user tool."),
  "hosted_service": f(False, "A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope."),
  "machine_actions": f(True, "The local server API and ACP let clients drive sessions and change files (packages/opencode/src/server, acp)."),
  "agent_mutations": f(False, "No product feature lets the agent change OpenCode's own agents, commands or configuration."),
  "evolution_auto_apply": f(False, "Nothing changes OpenCode's definitions automatically."),
  "definition_change_path": f(True, "Agents, commands, themes and configuration files are its definitions."),
  "code_release_path": f(False, "The GitHub agent the team runs on this repository is the product's general coding agent, not a first-party evolution system for OpenCode (rubric rule 12)."),
 },
 "openhands": {
  "persistent_data": f(True, "The Automation Service keeps automations, runs and a key-value store in PostgreSQL (automation repository, migrations/versions)."),
  "schema_changes": f(True, "Alembic migrations in the Automation Service (migrations/versions, 29 files)."),
  "multi_tenant": f(True, "The Automation Service serves organisations with org-scoped data (migrations/versions/023_org_scoped_git_sync.py)."),
  "hosted_service": f(True, "The Automation Service and Agent Server run as long-lived services for OpenHands Cloud."),
  "machine_actions": f(True, "The Agent Server and Automation Service APIs create and run automations with per-user API keys (automation repository: openhands/automation/auth.py)."),
  "agent_mutations": f(False, "Agents change users' repositories, not OpenHands' own definitions."),
  "evolution_auto_apply": f(False, "Nothing changes OpenHands' own definitions automatically."),
  "definition_change_path": f(True, "Automations, skills and settings are definitions."),
  "code_release_path": f(False, "Automations act on users' repositories; no first-party lane ships OpenHands code changes."),
 },
}

# ---------------------------------------------------------------- new criteria

NO_INTAKE = "No request or feature-request object for changing the product was found; requests live outside it."
NEW = {
 "frappe": {
  "ARC-02": up(1, "Schema follows DocType definitions through bench migrate and one-way patches (frappe/patches.txt, frappe/migrate.py); CI upgrades a populated site from the previous version (.github/workflows/server-tests.yml:143-230). There are no down steps and no enforced online strategy.", "The CI upgrade test against existing data goes beyond level 1."),
  "ARC-03": a(2, "Sessions and caches live in Redis (frappe/sessions.py:400) and web workers are stateless, but files sit on local disk and the scheduler holds a file lock on one host (frappe/utils/scheduler.py:43-53)."),
  "ARC-04": up(2, "RQ queues with per-queue timeouts, optional retries and deduplication (frappe/utils/background_jobs.py:99-145); failed jobs are kept and visible as RQ Job records (frappe/core/doctype/rq_job). The scheduler lock is per host, and idempotency is left to each job.", "Failed-job registry and visibility are close to level 3.", facets=IT),
  "ARC-07": up(1, "No published objectives. frappe/monitor.py records request and job timings when monitoring is enabled.", "Monitor logs are latency metrics for core paths."),
  "ARC-08": a(2, "The automation engine counts failures per rule against a circuit breaker and isolates each row with a savepoint (frappe/automation_engine/runner.py:516-525, drainer.py:74); integrations accept timeouts (frappe/integrations/utils.py:59). Apps run in-process without isolation."),
  "ARC-09": a(2, "bench backup covers the database, public and private files and site config, with optional encryption (frappe/commands/site.py:899-1030, frappe/utils/backups.py), and restore from full and partial backups is tested end to end (frappe/commands/test_commands.py:280-330). The site config holding the encryption key is backed up but its restore is not tested, so secrets stay at 2.", inventory={"data": 3, "definitions": 3, "files": 3, "secrets": 2}),
  "DEL-01": a(0, NO_INTAKE),
  "DEL-09": a(2, "Apps can be enabled per site (bench enable-app and disable-app, frappe/commands/site.py:1053-1090); there are no feature flags or percentage rollouts."),
  "DEL-10": up(1, "Disabling an app needs a bench command; automation rules are switched off by their circuit breaker or by an admin (frappe/automation_engine/runner.py:516-525).", "Automation rules can be disabled at runtime."),
  "LRN-03": a(2, "Error Log records exceptions with the method, reference document and trace id, queryable in the desk (frappe/core/doctype/error_log/error_log.json)."),
  "LRN-05": a(2, "Error Log groups errors by fingerprint and reports counts over time (frappe/core/doctype/error_log/error_log.py:80-103), with the trace attached."),
  "EXP-04": a(0, "No record of failed searches or unsupported requests was found (frappe/search, frappe/desk)."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(2, "An app (bundle) can be installed and enabled for selected sites (frappe/commands/site.py:559, 1053); there is no success metric or keep-or-kill record."),
 },
 "directus": {
  "ARC-02": a(2, "Every system migration has up and down steps (api/src/database/migrations, 110 files); user collections change through direct DDL from the schema service, with snapshot and apply for moving schemas between instances. No online strategy is enforced."),
  "ARC-03": up(2, "Redis-backed synchronisation, message bus and locks support several API instances (api/src/synchronization.ts, api/src/bus, api/src/lock); scale-out guidance lives in the separate docs site.", "The building blocks for stateless scale-out are all in place.", facets=I),
  "ARC-04": up(1, "Scheduled jobs and flows run inside the API process (api/src/schedules, api/src/flows.ts); there is no job queue with retries.", "Schedules take a lock so they run once across instances."),
  "ARC-07": a(2, "A Prometheus metrics endpoint for database, cache and storage health (api/src/metrics, METRICS_* settings); no stated objectives."),
  "ARC-08": a(2, "Sandboxed extensions run in an isolated VM with limits (api/src/extensions/lib/sandbox); the pressure limiter sheds load (packages/env/src/constants/defaults.ts:29). Other surfaces have no breakers."),
  "ARC-09": a(1, "No backup command. Schema snapshots move definitions between instances, but data and files are left to the database and storage provider."),
  "DEL-01": up(1, "Requests reach the AI assistant as free-text chat (api/src/ai/chat); nothing structures them into a specification.", "The chat keeps the request with the collections it touches."),
  "DEL-09": a(1, "Features are gated by licence entitlements (api/src/license/entitlements), not cohorts or flags."),
  "DEL-10": a(2, "Flows can be switched inactive and AI tools disabled at runtime; other changes cannot be switched off without editing them."),
  "LRN-03": a(2, "Every flow run records each operation step with its resolve or reject status as activity and revisions (api/src/flows.ts:414-454), viewable per flow; admins can read system logs (app/src/modules/settings/routes/system-logs). Failed actions outside flows are not recorded per product area."),
  "LRN-05": a(1, "Engineers read logs; no grouping or attached context."),
  "GOV-10": a(2, "Each AI tool can require approval and deletes can be disabled wholesale (api/src/ai/tools/registry.ts:198-214); there is no per-period or blast-radius limit."),
  "GOV-11": a(1, "AI changes are recorded as revisions by the acting user, but inputs carry no provenance and nothing separates untrusted content from instructions (api/src/ai)."),
  "EXP-04": a(0, "No record of failed searches or unsupported requests was found."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": up(1, "Extensions are installed per project; there is no cohort launch.", "Roles and policies can expose new collections to selected users."),
 },
 "discourse": {
  "ARC-02": a(3, "SafeMigrate blocks destructive migrations, and Migration::ColumnDropper and TableDropper defer drops so schema changes are expand-and-contract (lib/migration/safe_migrate.rb, column_dropper.rb, table_dropper.rb); post-deploy migrations separate destructive steps; migrations run in CI.", facets=IT),
  "ARC-03": up(2, "Stateless Puma processes over PostgreSQL and Redis; scale-out is documented in the separate discourse_docker repository rather than here.", "Large hosted deployments run many web processes over shared stores.", facets=I),
  "ARC-04": up(2, "Sidekiq jobs with retries and a dead set, and MiniScheduler runs scheduled jobs once across processes with a Redis lock (Gemfile:104-105); idempotency is left to each job.", "Retries, dead-lettering, observability and run-once scheduling are all present.", facets=IT),
  "ARC-07": a(1, "No published objectives in this repository; the prometheus exporter is a separate plugin not bundled here."),
  "ARC-08": a(2, "Outbound requests go through FinalDestination with timeouts, and safe mode disables plugins and themes for a session (config/routes.rb:2036). Plugins run in-process."),
  "ARC-09": a(3, "Built-in backup and restore of the database (data, site settings, themes) and uploads to local or S3 stores, with restore specs for both, including multisite (lib/backup_restore, spec/lib/backup_restore/database_restorer_spec.rb, uploads_restorer_spec.rb). Secrets live in the deployment environment, outside the product. No recovery objectives are stated (level 4).", facets=IT, inventory={"data": 3, "definitions": 3, "files": 3, "secrets": "n/a"}),
  "DEL-01": up(1, "Communities collect requests as topics; the bundled topic-voting plugin ranks them (plugins/discourse-topic-voting). They are not linked to the settings or screens involved.", "Voting adds structure to requests."),
  "DEL-09": up(2, "The upcoming-changes framework releases Discourse's own features to opted-in groups first (lib/upcoming_changes); site setting changes are not staged.", "Group-based rollout covers code changes by default."),
  "DEL-10": a(2, "Site settings switch features and plugins off at runtime, and safe mode disables customisations per session (config/routes.rb:2036-2037)."),
  "LRN-03": a(2, "Logster records server and browser errors in an admin UI (Gemfile:220); problem checks raise configuration issues (app/services/problem_check)."),
  "LRN-05": a(2, "Logster groups identical errors and attaches the environment of each occurrence."),
  "GOV-10": {"status": "not_applicable", "rationale": "No self-change path by default: discourse-ai and the workflows AI author are off.", "if_applicable": 2},
  "GOV-11": {"status": "not_applicable", "rationale": "No self-change path by default.", "if_applicable": 1},
  "EXP-04": a(2, "Search logs record terms and whether a result was clicked, with an admin report of searches without results (app/models/search_log.rb)."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(2, "Features and plugins can be enabled for selected groups, for example through upcoming changes and group settings (lib/upcoming_changes); there is no success metric or keep-or-kill record."),
 },
 "posthog": {
  "ARC-02": a(3, "CI runs migrations up to master, a migration risk analysis and safety tests for ClickHouse migrations (.github/workflows/ci-backend.yml:1661-2034, posthog/management/commands/analyze_migration_risk.py, test_ch_migrations_are_safe.py); async migrations carry rollback steps (posthog/async_migrations).", facets=IT),
  "ARC-03": up(2, "Stateless Django, Node and Rust services over shared stores; the hobby deployment is single-node (docker-compose.hobby.yml) and cloud scale-out manifests are outside this repository.", "The services are built to scale out.", facets=I),
  "ARC-04": a(3, "Celery with Redbeat for once-only schedules (pyproject.toml:21-22) and Temporal workflows with retries (posthog/temporal); ingestion routes failures to dead-letter handling (rust/common/types/src/event.rs).", facets=IT),
  "ARC-07": a(2, "Prometheus metrics across services (for example services/llm-gateway/src/llm_gateway/metrics/prometheus.py); no published objectives in the repository."),
  "ARC-08": a(2, "The LLM gateway has a circuit breaker for model providers (services/llm-gateway/src/llm_gateway/circuit_breaker.py) and subscriptions auto-disable after repeated failures (ee/tasks/subscriptions/auto_disable.py); other surfaces lack breakers, so a 3 is not defensible under the inventory rule."),
  "ARC-09": a(1, "No backup command in the repository; self-hosted backup is left to the operator."),
  "DEL-01": a(2, "PostHog AI takes requests in conversations stored with the page and objects in context, and has a plan mode that sets out steps before acting (ee/hogai/chat_agent/prompts/plan.py); plans carry no acceptance criteria or risk class."),
  "DEL-09": up(2, "PostHog ships its own code behind its own feature flags with percentage and cohort rollouts (products/feature_flags); definition changes and materialisations are not staged.", "Flags cover most code changes."),
  "DEL-10": up(2, "Feature flags switch code features off at runtime; there is no kill switch for AI-made or materialised changes.", "Flags act as a runtime kill switch for most features."),
  "LRN-03": a(2, "The app captures its own exceptions into PostHog's error tracking (frontend/src/lib/colors.ts:80, products/error_tracking); friction detection for customers' products (products/signals) is excluded under the self rule."),
  "LRN-05": up(1, "Exceptions are grouped into issues with stack traces by the error tracking product used on itself.", "Grouping with attached context meets level 2."),
  "GOV-10": a(2, "PostHog AI acts through a fixed tool set with resource-level access control, and approval policies cover registered action classes (products/approvals/backend/policies.py); materialisation has no declared blast-radius limit."),
  "GOV-11": up(2, "Third-party text in AI tool output is defanged and fenced as data, not instructions (ee/hogai/utils/untrusted.py); AI changes are attributed in the activity log, but source inputs are not recorded.", "Injection fencing is systematic for session-derived content."),
  "EXP-04": a(1, "No unmet-demand signals about PostHog itself beyond free-text requests."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": up(2, "Early access features let users opt into new products and betas (products/early_access_features); no success metric or keep-or-kill record.", "Stage-based releases approach a cohort launch."),
 },
 "n8n": {
  "ARC-02": a(2, "TypeORM migrations with down steps for PostgreSQL and SQLite and a migration registry with tests (packages/@n8n/db/src/migrations); no enforced online strategy."),
  "ARC-03": a(3, "Multi-main setup with leader election and Redis locks, and queue mode with separate workers (packages/cli/src/scaling/multi-main-setup.ee.ts, leader-election-client.ts, redis-lock.service.ts), covered by tests.", facets=IT),
  "ARC-04": up(2, "Queue mode runs executions on Bull with Redis (packages/cli/src/scaling/scaling.service.ts:100-105); leader election keeps schedules on one main. Failed executions are kept and can be retried by hand.", "Run-once scheduling and visibility are in place.", facets=IT),
  "ARC-07": a(2, "Prometheus metrics endpoint (packages/cli/src/metrics/prometheus); no published objectives."),
  "ARC-08": a(2, "Code nodes run in separate task-runner processes (packages/@n8n/task-runner, task-runner-python); nodes have retry-on-fail and timeouts; community nodes run in-process."),
  "ARC-09": a(2, "export:entities and import:entities move every database entity, optionally with data-table rows (packages/cli/src/commands/export/entities.ts); binary data and the encryption key are separate; no restore test or recovery objectives."),
  "DEL-01": up(2, "The AI workflow builder plans before building: it asks typed clarifying questions and produces a plan with a trigger, steps, suggested nodes and specifications that the user approves (packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts, agents/planner.agent.ts). The plan has no acceptance criteria or risk class.", "A confirmed, structured plan with clarifying questions approaches levels 3 and 4."),
  "DEL-09": a(2, "Workflow versions are published deliberately, and frontend features are gated per instance; there are no cohort rollouts for workflow changes."),
  "DEL-10": a(2, "Workflows can be deactivated at runtime; there is no global kill switch for AI-made changes."),
  "LRN-03": up(2, "Insights report failures and failure rates per workflow (packages/cli/src/modules/insights/insights.service.ts:181-268) and error workflows fire on failures.", "Failure rates per workflow approach friction detection."),
  "LRN-05": up(2, "Failed executions keep the failing node, input and error; the AI assistant can explain a node error on request.", "On-request AI debugging with node context approaches level 3."),
  "GOV-10": a(2, "Admin type-availability policies restrict which node types any change may use, enforced at save and publish (packages/cli/src/modules/type-availability-policies); no per-period or blast-radius limits."),
  "GOV-11": up(2, "Instance AI wraps resolved node parameters and external responses as untrusted data (packages/cli/src/modules/instance-ai/extract-resolved-node-parameters.ts:378-382); changes do not record their source inputs.", "Untrusted data is separated systematically in Instance AI."),
  "EXP-04": a(0, "No record of unmet intents was found."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(1, "New capabilities ship to all users of an instance."),
 },
 "dify": {
  "ARC-02": a(2, "Alembic migrations with downgrade steps (api/migrations/versions, 219 of 219); no enforced online strategy."),
  "ARC-03": a(2, "Stateless Flask API and Celery workers over PostgreSQL and Redis, documented through Docker Compose; no scale-out tests or manifests in the repository."),
  "ARC-04": a(2, "Celery queues with retries on many tasks (api/extensions/ext_celery.py, api/tasks/delete_conversation_task.py:104); no dead-lettering or idempotency rule."),
  "ARC-07": a(1, "Optional OpenTelemetry and Sentry; no metrics or objectives for core paths."),
  "ARC-08": a(2, "Model load balancing with cooldown across credentials (api/core/model_manager.py:68-130); plugins run in a separate daemon and code in a sandbox service. Connectors and internal services have no breakers, so a 3 is not defensible under the inventory rule."),
  "ARC-09": a(1, "No backup command; Docker volume backup is left to operators."),
  "DEL-01": a(0, NO_INTAKE),
  "DEL-09": a(1, "Published app versions go to all users at once."),
  "DEL-10": a(2, "Apps can switch their web app and API off at runtime (api/models/model.py:445-446)."),
  "LRN-03": a(2, "End users like or dislike answers and the feedback is queryable per app (api/models/model.py:1299-1302); workflow runs record node errors."),
  "LRN-05": up(1, "Run traces show node-level errors per run; there is no grouping.", "Per-run traces attach context."),
  "GOV-10": {"status": "not_applicable", "rationale": "No self-change path: AI drafts are saved by a person.", "if_applicable": 1},
  "GOV-11": {"status": "not_applicable", "rationale": "No self-change path.", "if_applicable": 1},
  "EXP-04": a(0, "No record of unmet intents was found."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(2, "Plugins from the marketplace are installed per workspace (api/services/plugin); no success metric or keep-or-kill record."),
 },
 "librechat": {
  "ARC-02": up(1, "One-off migration scripts with dry-run modes (config/migrate-*.js, package.json:134-139); no down steps.", "Dry runs reduce migration risk."),
  "ARC-03": a(2, "With USE_REDIS, caches and request limits move to Redis for several instances (api/cache/clearPendingReq.js:5-39); Helm charts deploy it (helm/)."),
  "ARC-04": a(1, "No job queue; background work runs in the API process."),
  "ARC-07": a(1, "No metrics endpoint or objectives; tracing fans out to Langfuse."),
  "ARC-08": a(2, "Provider calls have timeouts and errors are contained per conversation; MCP servers run as separate connections."),
  "ARC-09": up(0, "No backup command or documented backup in the repository.", "MongoDB tooling is the implied path."),
  "DEL-01": a(0, NO_INTAKE),
  "DEL-09": a(1, "Interface features are switched globally in librechat.yaml."),
  "DEL-10": a(1, "Disabling a feature needs a configuration change and restart."),
  "LRN-03": a(2, "Users rate messages with thumbs and tags, stored on the message (packages/data-schemas/src/schema/message.ts:103)."),
  "LRN-05": a(1, "Engineers read logs."),
  "GOV-10": {"status": "not_applicable", "rationale": "No self-change path by default; the memory agent is opt-in.", "if_applicable": 1},
  "GOV-11": {"status": "not_applicable", "rationale": "No self-change path by default.", "if_applicable": 1},
  "EXP-04": a(0, "No record of unmet intents was found."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(2, "Agents, prompts and MCP servers can be shared with selected users and groups through ACLs (packages/data-schemas/src/types/aclEntry.ts)."),
 },
 "hermes-agent": {
  "ARC-02": up(2, "The state database migrates forward on start (hermes_state_schema.py) and hermes update takes a pre-update snapshot it restores when an update fails (hermes_cli/update_cmd.py:109-110), with migration tests (tests/hermes_state).", "Snapshot restore is a tested rollback path.", facets=IT),
  "ARC-08": a(2, "Fallback providers and credential pools take over when a primary model fails (agent/agent_init.py, tests/agent/test_restore_primary_pool_reselect.py); tool and MCP failures are contained to the turn. Plugins and gateway platforms have no breakers, so a 3 is not defensible under the inventory rule."),
  "ARC-09": a(3, "hermes backup and import cover the home directory: the sessions database (snapshotted with sqlite3.backup), skills, memory, configuration and secrets such as .env, auth.json and the vault (hermes_cli/backup.py:117-161), with pre-update backups and round-trip tests (tests/hermes_cli/test_backup*.py). No recovery objectives are stated (level 4).", facets=IT, inventory={"data": 3, "definitions": 3, "files": 3, "secrets": 3}),
  "DEL-01": up(1, "Requests are chat turns; the agent can create a skill when asked, without a specification step.", "Skill creation on request records name and description."),
  "DEL-09": a(2, "Update channels let an installation take canary builds before stable (hermes_cli/update_channel.py); skill and memory changes are not staged."),
  "DEL-10": a(2, "Background review and individual skills can be switched off in configuration at runtime; curator archives remove skills without a release."),
  "DEL-11": up(2, "hermes update rolls back a pulled tree that fails a syntax check and restores the state snapshot on failure (hermes_cli/update_cmd.py:840-870); there is no one-step rollback to the previous release.", "Failed updates roll back automatically.", facets=IT),
  "LRN-03": a(2, "Background review sees corrections and failures in recent turns, and evals record failures found in use (evals/)."),
  "LRN-05": a(2, "hermes doctor diagnoses setup problems and cron error diagnostics attach context to failing jobs (hermes_cli/main.py:2567)."),
  "GOV-10": a(2, "Protected instruction files always need a person, and skill writes pass scans and an AST audit (tools/skills_guard.py); there is no declared scope or rate limit for background changes."),
  "GOV-11": up(2, "The skill ledger records the actor of every mutation (tools/skill_ledger.py:54-68) and the skills guard scans writes for injection and exfiltration patterns (tools/skills_guard.py:42-140); session content can still drive an automatically applied skill change.", "Provenance and injection scanning are both present."),
  "EXP-04": a(1, "Unserved requests stay in session history; nothing records them as unmet demand."),
  "EXP-05": a(1, "Background review creates skills for tasks it has just done; it does not propose capabilities nobody has used yet."),
  "EXP-06": a(1, "New skills apply to the whole installation at once."),
 },
 "openclaw": {
  "ARC-02": a(2, "The workshop store has a versioned SQLite schema (src/skills/workshop/store-sqlite-schema.ts) and doctor migrates configuration; no down steps."),
  "ARC-08": a(2, "Agents can declare model fallbacks (src/agents/agent-scope-config.ts); plugins run in-process, so a 3 is not defensible under the inventory rule."),
  "ARC-09": a(3, "Backup covers state, configuration, credentials, workspaces, agents and managed skills (src/commands/backup-shared.ts:76), with verification, scheduling and a restore test that round-trips into a fresh target with a matching inventory (src/commands/backup-restore.test.ts:176). Private captures are excluded by design. No recovery objectives are stated (level 4).", facets=IT, inventory={"data": 3, "definitions": 3, "files": 3, "secrets": 3}),
  "DEL-01": up(2, "The /learn command turns a request into requirements and sources and stages a pending skill proposal for review, revising existing Workshop skills before creating new ones (src/skills/workshop/learn-prompt.ts). No acceptance criteria or risk class.", "A pending, reviewed draft that accounts for existing skills approaches level 3."),
  "DEL-09": a(1, "Skill proposals apply to the whole installation; there are no cohorts."),
  "DEL-10": a(2, "Autonomous mode and individual skills can be switched off in configuration at runtime (src/skills/workshop/config.ts)."),
  "LRN-03": a(2, "The experience review observes failed runs and corrections (src/skills/workshop/experience-review.ts)."),
  "LRN-05": a(2, "openclaw doctor diagnoses configuration and runtime problems; experience review attaches the observed runs to proposals."),
  "GOV-10": a(2, "Workshop policy limits proposal size and origins (src/skills/workshop/policy.ts, proposal-origin-validation.ts); there is no per-period or blast-radius limit."),
  "GOV-11": up(2, "Every proposal records its origin agent, session, run and message (src/skills/workshop/proposal-origin-validation.ts) and is scanned before apply (proposal-scan.ts); with approvalPolicy auto, session content alone can drive an applied change.", "Provenance and scanning meet level 3 apart from the default auto-apply."),
  "EXP-04": a(1, "Unserved requests stay in session history."),
  "EXP-05": a(1, "Experience review proposes skills for observed tasks, not capabilities nobody has used yet."),
  "EXP-06": a(1, "New skills apply to the whole installation at once."),
 },
 "opencode": {
  "ARC-02": up(1, "Drizzle migrations for the session database (packages/opencode/migration); no down steps.", "Generated migrations with a migration table."),
  "ARC-08": a(2, "Provider calls are retried with back-off (packages/opencode/src/session/retry.ts); MCP servers and LSPs run as separate processes."),
  "ARC-09": a(1, "Sessions can be exported and imported one at a time (packages/opencode/src/cli/cmd/export.ts, import.ts); configuration lives in files."),
  "DEL-01": a(0, NO_INTAKE),
  "DEL-09": a(1, "Releases go to all users; no staged exposure."),
  "DEL-10": a(1, "Features are switched in configuration files."),
  "LRN-03": a(1, "Logs for engineers."),
  "LRN-05": a(1, "Engineers read logs."),
  "GOV-10": {"status": "not_applicable", "rationale": "No self-change path.", "if_applicable": 1},
  "GOV-11": {"status": "not_applicable", "rationale": "No self-change path.", "if_applicable": 1},
  "EXP-04": a(0, "No record of unmet intents was found."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(1, "Plugins and agents apply to the whole installation."),
 },
 "openhands": {
  "ARC-02": up(2, "Alembic migrations with downgrade steps, and a test of the migration history (automation repository: migrations/versions, tests/test_migration_history.py); no enforced online strategy.", "Migration history is tested in CI.", facets=IT),
  "ARC-03": a(2, "The Automation Service is a stateless FastAPI app over PostgreSQL and object storage; the canvas ships a Helm chart (helm/agent-canvas)."),
  "ARC-04": up(2, "A scheduler and watchdog drive runs with timeouts and terminal states (automation repository: openhands/automation/scheduler.py, watchdog.py); git sync backs off after failures (migrations/versions/029_add_git_sync_failure_backoff.py).", "Watchdog recovery and back-off approach level 3.", facets=IT),
  "ARC-07": up(1, "Telemetry for runs and the key-value store (openhands/automation/telemetry.py, kv_metrics.py); no objectives.", "Run metrics are exported."),
  "ARC-08": a(2, "Each run executes in its own sandbox with timeouts and cleanup (openhands/automation/watchdog.py); repeatedly failing automations are disabled (migrations/versions/020_add_automation_disabled_reason.py)."),
  "ARC-09": a(0, "No backup command or documented backup for the Automation Service database or storage."),
  "DEL-01": a(0, NO_INTAKE),
  "DEL-09": a(2, "Plugin automations can split runs between weighted variants (openhands/automation/presets/plugin/sdk_main.py:349-373)."),
  "DEL-10": a(2, "Automations can be disabled at runtime, and unhealthy ones are disabled automatically (tests/test_unhealthy_automations.py)."),
  "LRN-03": a(2, "Runs record failure kinds and status details, and unhealthy automations are detected (openhands/automation/watchdog.py, migrations/versions/016_add_run_status_detail.py)."),
  "LRN-05": a(2, "Failed runs keep their phase, failure kind and conversation for inspection (docs/run-phase-reporting.md)."),
  "GOV-10": {"status": "not_applicable", "rationale": "No self-change path.", "if_applicable": 1},
  "GOV-11": {"status": "not_applicable", "rationale": "No self-change path.", "if_applicable": 1},
  "EXP-04": a(0, "No record of unmet intents was found."),
  "EXP-05": a(0, "No adjacent-capability proposals."),
  "EXP-06": a(1, "Presets and plugins are available to every organisation."),
 },
}

# ---------------------------------------------------------------- re-scores of existing criteria

RESCORE = {
 "hermes-agent": {
  "GOV-05": a(2, "Skills have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py) and curator archives are restorable, but configuration has only point-in-time copies on some writes (hermes_cli/config_backups.py) and memory files have no history. Under the inventory rule a 3 needs every default surface at 3.", inventory={"skills": 3, "configuration": 2, "memory": 1}),
 },
 "openclaw": {
  "GOV-05": a(2, "Workshop skill collections are backed up and can be restored or rolled back with revision hashes (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); configuration has rotating backups and recovery (src/config/backup-rotation.ts, recovery-policy.ts) but no operator rollback with diffs. Under the inventory rule a 3 needs every default surface at 3.", inventory={"skills": 3, "configuration": 2}),
 },
 "opencode": {
  "DEL-04": up(1, "The team runs OpenCode's general GitHub agent on this repository for reviews and triage (.github/workflows/review.yml, triage.yml, opencode.yml). Under rubric rule 12 that is a team's use of a coding agent, not a first-party evolution system for OpenCode.", "If the GitHub agent is read as part of the product's own evolution system, it is an AI lane for narrow tasks."),
 },
 "openhands": {
  "DEL-04": up(1, "Automations run coding agents on users' repositories (automation repository README); nothing implements changes to OpenHands' own definitions. Recorded under the self rule.", "Automations configured in OpenHands are operator-configured behaviour run by an AI lane."),
  "LRN-09": up(1, "Plugin automations tag each run with its experiment and variant (openhands/automation/presets/plugin/sdk_main.py:514-530), so variants can be compared by hand; nothing records a baseline or decision.", "Variant-tagged runs are telemetry bound to the change."),
 },
}

# Higher readings of 3 that the inventory rule cannot support (partial surface coverage).
DROP_ALT = {
 "directus": {"GOV-05": "Data-model changes have no rollback."},
 "posthog": {"GOV-05": "Revert is not available across customisation surfaces."},
 "n8n": {"GOV-05": "Credentials, variables, data tables and settings roll back only through source control."},
 "dify": {"GOV-05": "Surfaces other than workflows and app DSL are unversioned."},
 "librechat": {"GOV-05": "Configuration is unversioned in the product."},
}

# Facets for existing depth-capped criteria read at 3 or more.
FACETS = {
 "frappe": {"ARC-01": IT, "GOV-04": IT},
 "directus": {"GOV-05": IT, "ARC-01": IT, "GOV-04": IT},
 "discourse": {"ARC-05": IT},
 "posthog": {"GOV-05": IT, "ARC-01": IT, "ARC-05": IT, "GOV-04": IT},
 "n8n": {"GOV-05": IT, "ARC-06": IT, "GOV-04": IT, "LRN-08": IT},
 "dify": {"GOV-05": I, "ARC-05": I},
 "librechat": {"GOV-05": I, "ARC-05": IT},
 "hermes-agent": {"GOV-04": IT, "LRN-08": IT},
 "openclaw": {"GOV-04": IT},
 "opencode": {},
 "openhands": {},
}


# ---------------------------------------------------------------- readings and scope updates

READINGS = {
 "frappe": "**SAL 1.** Operators reshape Frappe without code (Open 2.3), so every loop reaches L1, but nothing in the product drafts or builds a change (DEL-04 0) and requests have no intake (DEL-01 0), so no loop reaches L2. **Architecture:** backup and restore of data and files are tested end to end, but restoring the site secrets is not (ARC-09 2), and migrations are forward-only (ARC-02 1). **Next level:** an AI lane that drafts DocType, workflow or report changes as proposals, and structured request intake.",
 "directus": "**SAL 1.** Every loop reaches L1 through the data-model editor and flow logs, which record each operation's success or failure (LRN-03 2). The AI assistant drafts schema and flow changes behind approvals but is scored at its lower reading (DEL-04 1), and Learn is the weakest capability (0.8). **Architecture:** no load suite (ARC-06 0) and no backup command (ARC-09 1) hold the architecture foundation at L1. **Next level:** structured request intake and a stronger AI lane, plus capacity and backup evidence.",
 "discourse": "**SAL 1.** Admins configure Discourse without code, and it passes two critical controls that most systems fail: SafeMigrate and deferred column drops enforce expand-and-contract (ARC-02 3), and backup and restore of the database and uploads are tested (ARC-09 3). There is no AI lane by default (DEL-04 0), and as a focused application with adjacent-domain criteria excluded, Opportunity → Expansion stays at L0. **Learn:** search logs already record searches without results (EXP-04 2), the raw material for unmet-demand sensing. **Next level:** turn on and productise the workflows AI author, and cluster search misses and topic votes into proposals.",
 "posthog": "**SAL 1.** Request → Release reaches L2: PostHog AI plans before acting and builds insights and dashboards (DEL-01 2, DEL-04 2). Issue → Fix stops at L1 because nothing diagnoses PostHog's own issues (LRN-05 1); its Signals product does this for customers' products and is excluded under the self rule. **Strengths:** migration risk analysis in CI (ARC-02 3), Temporal and Celery work (ARC-04 3), and feature flags on its own code (DEL-09 2). **Blocks L3:** no backup in the repository (ARC-09 1), and definition rollback covers only some surfaces (GOV-05 2).",
 "n8n": "**SAL 2**, joint highest in the sample. The AI workflow builder asks clarifying questions and produces a plan for approval before it builds (DEL-01 2, DEL-04 2), and Insights reports failure rates per workflow (LRN-03 2), so both core loops reach L2. **Blocks L3:** controls, not workflow: migrations have no enforced online strategy (ARC-02 2), entity export has no restore test or recovery objectives (ARC-09 2), definition rollback covers workflows only (GOV-05 2), and AI changes have no declared blast-radius limit (GOV-10 2).",
 "dify": "**SAL 1.** Builders reshape apps and workflows without code (Open 2.2), and the AI generators draft prompts and code (DEL-04 2), but there is no intake (DEL-01 0) and no load suite (ARC-06 0), which caps the architecture foundation at L1. **Issue → Fix:** end users' likes and dislikes are recorded per app (LRN-03 2), but there is no grouping or diagnosis (LRN-05 1). **Next level:** structured requests, failure grouping, and measured capacity.",
 "librechat": "**SAL 0.** Configuration is file-based and partly unversioned (Open 1.7), and there is no AI lane for LibreChat's own definitions (DEL-04 0), so no loop has a build path at L1. Users rate messages with tags (LRN-03 2), which is a useful start. **Next level:** governed, versioned configuration in the product, and backup (ARC-09 0).",
 "hermes-agent": "**SAL 1.** Issue → Fix reaches L2: background review turns corrections and failures into skill and memory changes by default (LRN-07 3), and hermes doctor diagnoses setup problems (LRN-05 2). Request → Release stops at L1 because requests are chat turns with no specification step (DEL-01 1); raising that one criterion would lift the headline. **Controls:** backup and restore cover every surface including secrets and are tested (ARC-09 3), but configuration and memory lack the rollback skills have (GOV-05 2, inventory) and background changes have no declared scope or rate limit (GOV-10 2).",
 "openclaw": "**SAL 2**, joint highest. /learn turns a request into a pending skill proposal (DEL-01 2), and the experience review drafts and applies skills from observed runs (LRN-07 3), so both core loops reach L2. Backup and restore are verified and tested across state, configuration, credentials and skills (ARC-09 3). **Blocks L3:** configuration has only rotating backups, not operator rollback (GOV-05 2, inventory); skill changes have no staged exposure (DEL-09 1); the default auto-apply has no declared blast-radius limit (GOV-10 2).",
 "opencode": "**SAL 0.** OpenCode's own agents, commands and configuration are files versioned only by the user's git (GOV-05 1), so no loop has a rollback path at L1. The team's use of OpenCode's GitHub agent on its own repository is not a first-party evolution system under rule 12 (DEL-04 1). **Next level:** versioned, validated configuration with rollback, and a learning path for agents and commands.",
 "openhands": "**SAL 1.** With the Automation Service now in scope, OpenHands has a hosted, multi-organisation architecture, but no load suite (ARC-06 0) or backup (ARC-09 0), which caps the foundation at L1. Automations run coding agents on users' repositories, which the self rule excludes (DEL-04 1). Runs record failure kinds and unhealthy automations are disabled automatically (LRN-03 2, DEL-10 2). **Next level:** backup and capacity evidence for the Automation Service, and a lane that improves OpenHands' own skills and automations.",
}

SCOPE_UPDATES = {
 "openhands": {
  "source": "github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30)",
  "scope_line": "Scope: the Agent Canvas (OpenHands repository), the software-agent-sdk that runs agents, and the Automation Service (OpenHands/automation) that schedules and dispatches automations. OpenHands Cloud operations are out of scope.",
  "limits": "Repository evidence only. The Automation Service was added for v0.4 after the inter-rater study found it missing; it is beta. No live runs. Single rater.",
 },
}


def facets(t):
    return {"implemented": t[0], "tested": t[1], "operated": t[2]}


def flip(entry):
    """Rule 11: a downward alternate becomes the score, the original score the alternate."""
    s, alt = entry["score"], entry["alt_score"]
    entry["score"], entry["alt_score"] = alt, s
    entry["evidence"] = (entry["evidence"].rstrip() + f" Scored at the lower reading under rule 11 because: "
                         + entry.get("alt_note", "").rstrip())
    entry["alt_note"] = f"The September v0.3 pass scored {s} on the evidence above."
    return entry


def migrate(system):
    path = os.path.join(ROOT, system, "assessment.json")
    with open(path) as handle:
        data = json.load(handle)
    if data.get("framework") == "EVOLVE":
        sys.exit(f"{system}: already migrated")
    scores = {}
    for old, entry in data["scores"].items():
        for key in ("evidence", "alt_note", "rationale", "searched"):
            if key in entry:
                entry[key] = re.sub(r"\b([A-P][1-4])\b", lambda m: MAP.get(m.group(1), m.group(1)), entry[key])
        if entry.get("status") == "assessed" and "alt_score" in entry and entry["alt_score"] < entry["score"]:
            entry = flip(entry)
        scores[MAP[old]] = entry
    facts = FACTS[system]
    for cid, gate in GATED.items():
        if cid in scores and not any(facts[g]["value"] for g in gate):
            old = scores[cid]
            entry = {"status": "not_applicable",
                     "rationale": f"Scope fact {' and '.join(gate)} is false: " + facts[gate[0]]["evidence"]}
            if old.get("status") == "assessed":
                entry["if_applicable"] = old["score"]
            scores[cid] = entry
    for cid, reason in DROP_ALT.get(system, {}).items():
        entry = scores[cid]
        entry.pop("alt_score"); entry.pop("alt_note")
        entry["evidence"] += (" The higher reading of 3 was dropped under the inventory rule (a 3 needs every "
                              "default surface at 3): " + reason)
    for cid, entry in RESCORE.get(system, {}).items():
        scores[cid] = entry
    for cid, entry in NEW[system].items():
        scores[cid] = entry
    for cid in GATED:
        if cid not in scores:
            gate = GATED[cid]
            scores[cid] = {"status": "not_applicable",
                           "rationale": f"Scope fact {' and '.join(gate)} is false: " + facts[gate[0]]["evidence"]}
    for cid, entry in scores.items():
        if isinstance(entry.get("facets"), tuple):
            entry["facets"] = facets(entry["facets"])
    for cid, t in FACETS[system].items():
        scores[cid]["facets"] = facets(t)
    data["reading"] = READINGS[system]
    data.update(SCOPE_UPDATES.get(system, {}))
    data["framework"] = "EVOLVE"
    data["framework_version"] = "0.4.0"
    data["scope_facts"] = facts
    data["scores"] = scores
    with open(path, "w") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


if __name__ == "__main__":
    for system in SYSTEMS:
        migrate(system)
    print("migrated", len(SYSTEMS), "systems")
