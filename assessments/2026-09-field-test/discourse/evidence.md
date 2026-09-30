# Discourse evidence

Read at github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Focused application: archetypes.md says universal entity criteria may be inappropriate, and Discourse is a discussion product, not a business-object platform. Applied by the fixed per-archetype rule in ../_method.md. If counted: 1.
- **A2 Field definitions carry type and validation**: **3** (grade A). Admins define typed user fields (text, confirm, dropdown, multiselect) with required, editable and visibility flags (app/models/user_field.rb); only the user entity family has them, so the single-entity cap applies.
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Focused application: universal entity criterion (fixed per-archetype rule). If counted: 1.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Focused application: generic per-entity API is a universal entity criterion (fixed per-archetype rule). If counted: 1.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Focused application: runtime API reshaping presupposes defined entities (fixed per-archetype rule). If counted: 1.
- **B3 Machine-readable contract with introspection and dry-run**: **2** (grade A). OpenAPI documentation generated from request specs (lib/tasks/api_docs.rake); MCP tools declare output schemas (lib/discourse_mcp/output_schema.rb). No typed client generation or dry-run.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Themes and components are installed and configured by admins with typed, schema-validated settings and settings migrations (app/models/theme_setting.rb, theme_settings_migration.rb) and can be previewed on the live site before activation (app/controllers/admin/themes_controller.rb:12-16); page layout itself is theme code, not data.
  - Alternate reading 3: Admins do override and preview presentation per site; only the 'layout as data' clause fails.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Focused application: generic widgets from entity definitions presuppose defined entities (fixed per-archetype rule). If counted: 1.
- **C3 Theme tokens and text are data with tenant overrides**: **3** (grade A). Admin colour-scheme editor (app/models/color_scheme.rb), per-site overrides for every UI string (app/models/translation_override.rb, theme_translation_override.rb), and a translation pipeline covering thousands of locale files (translator.yml).
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A), **3** with opt-in settings. By default: the automation plugin and watched words with a test mode (plugins/automation, app/models/watched_word.rb). The workflows plugin with versions, validators and test sessions is an off-by-default beta (plugins/discourse-workflows/config/settings.yml:4-11).
- **D2 Event model with webhooks or subscriptions and retry**: **3** (grade A). Admin webhooks with typed event subscriptions, delivery logs (app/models/web_hook_event.rb), automatic retries (MAX_RETRY_COUNT 4, app/jobs/regular/emit_web_hook_event.rb:8) and redelivery (app/models/redelivering_webhook_event.rb).
  - Alternate reading 4: Replay exists; event schemas are not generated from definitions.
- **D3 Sandboxed server-side hooks**: **2** (grade A), **3** with opt-in settings. By default, sandboxed code runs only as discourse-ai tool scripts with timeouts (plugins/discourse-ai/lib/agents/tool_runner.rb:44-58), and discourse-ai is off by default; the beta workflows Code node adds a sandbox with a resource budget (js_sandbox.rb, sandbox_budget.rb).
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). An accessibility service and dialog components exist (frontend/discourse/tests/helpers/qunit-helpers.js:102 imports discourse/services/a11y); no automated accessibility scanning in CI.
  - Alternate reading 2: Kit-level accessibility utilities exist; the anchors bundle kit and scans.
- **E2 Audit generic over entities, definition changes and approvals**: **2** (grade A). Staff action logs record admin actions including site-setting changes with old and new values (app/services/staff_action_logger.rb) with an admin UI; post revisions and reviewable history; an MCP audit log with retention (config/site_settings.yml:4535). Ordinary entity mutations are not all audited.
  - Alternate reading 3: Configuration changes, approvals in the review queue and admin UI are covered; only entity-wide coverage fails.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). User archive export (app/jobs/regular/export_user_archive.rb), anonymisation and deletion (app/services/user_anonymizer.rb, user_destroyer.rb) and purge settings; coded for the user family, not driven by field tags.
  - Alternate reading 3: Admin-triggered export and erasure exist across the user's content; only tag-driven coverage is missing.
- **E4 Security as infrastructure**: **2** (grade A). Central Guardian permission model with group and category permissions and scoped API keys (app/models/api_key_scope.rb); Dependabot configured (.github/dependabot.yml); no SAST in CI.
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Site-setting history in staff logs, revertible post revisions, versioned published workflows (workflow_snapshot.rb) and git-backed remote themes; no admin rollback for settings or themes.
- **F2 Proposal, review, apply as a first-class object with preview**: **1** (grade A), **2** with opt-in settings. By default, admins change settings and themes directly. With the beta workflows plugin on, an AI author writes risk-rated draft proposals that are validated and applied by an admin (plugins/discourse-workflows/lib/discourse_workflows/ai_workflow_author.rb:39-67).
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **1** (grade A). Admins apply changes directly; the upcoming-changes framework controls rollout of Discourse's own features by status and group (lib/upcoming_changes, plugins/discourse-workflows/config/settings.yml:4-11).
  - Alternate reading 2: Upcoming changes is a narrow policy for feature rollout.
- **F4 Upgrade safety**: **3** (grade A). Plugins and themes pin compatible commits per core version (lib/version_compatibility.rb, lib/tasks/compatibility.rake); a structured deprecation API with since and drop_from (lib/discourse.rb:1185-1189); theme settings migrations (app/models/theme_settings_migration.rb).
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **2** (grade A). PostgreSQL full-text search (lib/search.rb) and hand-tuned list queries; custom fields are not filterable at scale.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Multisite hosting with a database per site and pervasive rate limiters; no noisy-neighbour detection or isolation verification in the repository.
  - Alternate reading 3: Per-site data isolation and per-user limits are strong; only detection is missing.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). Benchmark script (script/bench.rb); no documented per-surface limits or CI budgets.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **1** (grade A). Rails and Ember monolith deployed as one application; container tooling lives in a separate repository.
- **H2 Module boundaries enforced by tooling**: **1** (grade A). Plugin API is a contract, but internal module boundaries are convention; no architectural lint.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Tests, linting and migration tests run on every pull request with no draft filter (.github/workflows/tests.yml:3-26, linting.yml, migration-tests.yml); no accessibility or security scan in CI.
  - Alternate reading 3: Every code change class except accessibility and SAST is checked.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Ruby and JavaScript plugins through a versioned plugin API, theme components with typed settings, site settings, text overrides, watched words, automations, SQL badges, user fields and custom sidebar sections.
- **I2 Runtime isolation and dependency control**: **2** (grade A). Themes run under a Content Security Policy; AI tool scripts and beta workflow code nodes are sandboxed; plugins run in-process with full trust.
- **I3 Developer loop**: **2** (grade A). Theme preview on the live site, the /logs viewer for admins and a Docker development environment (bin/docker/boot_dev); the theme CLI that syncs to a live site is in another repository.
  - Alternate reading 3: Preview against the real site and logs are already available to theme developers.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **3** (grade A). Core MCP server with typed tools and output schemas (lib/discourse_mcp, tools for topics, posts, search, users, themes, site settings and moderation), per-primitive required scopes and annotations (primitive.rb:14-78), OAuth and group scopes and a catalog; plugins register further tools.
- **K2 Conversational operability for users and natural-language authoring for operators**: **1** (grade A), **3** with opt-in settings. By default only the tutorial narrative bot is conversational (plugins/discourse-narrative-bot). With discourse-ai on (default false), AI agents answer members with retrieval and tools, and admins author workflows in natural language.
- **K3 Agent-safe actions**: **2** (grade A). Granular API key scopes, user API key scopes and MCP OAuth scopes (app/models/api_key_scope.rb, user_api_key_scope.rb, mcp_oauth_authorization_scope.rb); MCP audit log; rate limiters. Idempotency is only an annotation hint; no dry-run.
  - Alternate reading 3: Scoped identity, audit and rate limits are strong; only idempotency keys and dry-run are missing.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **1** (grade A). Integrations are bespoke plugins (discourse-zendesk-plugin, discourse-github, import scripts); no canonical integration model.
- **N2 Connector definition or SDK**: **2** (grade A). Chat integration has a provider framework (plugins/discourse-chat-integration/lib/discourse_chat_integration/provider) and beta workflows have typed credential definitions (credential_types); no general connector SDK with lifecycle.
- **N3 Stable versioned contracts**: **1** (grade A). No path versioning; plugin-API deprecations are structured, but the HTTP API has no deprecation windows.
  - Alternate reading 2: The API is documented through generated OpenAPI docs.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). Note that Discourse's kernel of users, groups, posts, topics, permissions and chat channels matches the rubric's level-3 kernel almost word for word. If counted: 2.
- **O2 A new domain is expressible without kernel change**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). Chat, events, assignment, subscriptions and voting ship as code plugins on an unchanged core. If counted: 2.
- **O3 A domain ships as an installable bundle**: **not applicable**. Focused application: adjacent-domain criterion (fixed per-archetype rule). If counted: 2.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). User actions, visits, post timings and search logs are recorded as they happen and feed product features such as top topics and admin reports.
  - Alternate reading 2: Engagement tables, not a per-feature event stream.
- **J2 Structured learning signals**: **2** (grade A). Typed flags feed a review queue with triage (app/models/reviewable.rb); they concern content, not the product's definitions and versions.
- **J3 Cross-source mining inside the product**: **2** (grade A). Data Explorer runs saved SQL over the whole site database including usage, moderation and support data (plugins/discourse-data-explorer); no continuous mining.
  - Alternate reading 3: Usage and support data are already joinable and queryable inside the product.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **2** (grade A). Problem checks raise admin notices recommending configuration fixes (app/services/problem_check): recommendations for one area.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **0** (grade A), **2** with opt-in settings. By default there is no AI authoring lane; the beta workflows AI author is one when enabled.
- **M4 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **2** (grade A). Problem checks run on a schedule and raise configuration recommendations (app/services/problem_check); they are rules, not learning from experience.
- **P2 Learned changes are validated before they take effect**: **1** (grade A), **2** with opt-in settings. By default, changes are reviewed by people. With the workflows beta, AI proposals are validated with workflow_validate_patch before an admin applies them.
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). Health endpoint /srv/status (config/routes.rb:135) and version through the about endpoint; no deployed-configuration snapshot.
- **L2 Environment reproducibility**: **2** (grade A). Scripted Docker development environment (bin/docker/boot_dev), test database setup, and upcoming-change flags that ship features off by default; no per-change ephemeral environment in the repository.
  - Alternate reading 3: Flags-off-first is present; ephemeral environments may exist in private infrastructure.
- **L3 Machine verifiability**: **2** (grade A). System specs drive browser journeys (spec/system) alongside QUnit tests; no changed-path to journey map or adoption instrumentation at ship.
