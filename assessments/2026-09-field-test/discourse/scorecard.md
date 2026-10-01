# Discourse: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the discourse repository including the plugins bundled in plugins/ (automation, discourse-ai, discourse-workflows, data explorer, chat and others) and the core MCP server. Several of these ship disabled by default as betas. Hosted Discourse and the separate theme CLI and Docker repositories are out of scope.

## Reading

**By default:** a well-governed forum with strong upgrade safety (F4 3), webhooks with retries (D2 3) and a scoped MCP server (K1 3), but Learning is low (1.5). **With opt-in betas:** the workflows plugin and discourse-ai add an AI author that writes only validated, risk-rated drafts, and Learning rises to 1.9. v0.3 now separates these two states instead of blending them.

## Limits

Repository evidence only, main branch at the tip named above. discourse-ai, discourse-workflows and parts of the MCP surface ship disabled by default as betas; they were scored as shipped, and the alternates show the effect of discounting them. Hosted Discourse operations (incidents, ephemeral environments, telemetry pipelines) are invisible here. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main). Archetype **focused-application**.

Coverage: 41 assessed, 0 not evidenced, 8 not applicable. Grades: 41 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.1 | mechanism | 2.1–2.3 | 2.2 | 2.1 | 1.8 |
| governance | 1.8 | mechanism | 1.8–2.3 | 1.9 | 1.8 | 1.8 |
| learning | 1.5 | mechanism | 1.4–1.6 | 1.9 | 1.5 | 1.5 |
| factory | 1.7 | mechanism | 1.7–2.0 | 1.7 | 1.7 | 1.7 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.2 | 2.4 |
| Governance | 1.8 | 1.9 |
| Learning | 1.5 | 1.9 |
| Factory | 1.7 | 1.7 |
| Agent Interface | 2.0 | 2.7 |
| Extension Surface | 1.8 | 1.8 |
| Operational Scalability | 2.0 | 2.0 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 2 pass | 2 pass |
| propose | M1, P1 | 2 | 2 pass | 2 pass |
| review | F2 | 2 | 1 fail | 2 pass |
| gate | F3 | 3 | 1 fail | 1 fail |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 1 fail | 2 fail |
| verify | L1 | 2 | 2 pass | 2 pass |

Caps and deductions applied:

- A2: single-entity caps 3 -> 2

## Dimension means

| Dimension | Default |
|---|---:|
| A Entity and schema as data | 2.0 |
| B API surface generation | 2.0 |
| C Rendering follows the definition | 2.5 |
| D Behaviour as data | 2.3 |
| E Compliance and security as infrastructure | 1.8 |
| F Change control | 1.8 |
| G Performance under genericity | 2.0 |
| H Stack flexibility and verification | 1.3 |
| I Extension ecosystem | 2.3 |
| J Observe | 2.3 |
| K Agent and conversational readiness | 2.0 |
| L Factory surfaces | 2.0 |
| M Advise and act | 0.7 |
| N Integration and connector extensibility | 1.3 |
| P Learn from experience | 1.5 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Focused application: archetypes.md says universal entity criteria may be inappropriate, and Discourse is a discussion product, not a business-object platform. Applied by the fixed per-archetype rule in ../_method.md. |
| A2 Field definitions carry type and validation | assessed | 2 |  |  | A | Admins define typed user fields (text, confirm, dropdown, multiselect) with required, editable and visibility flags (app/models/user_field.rb); only the user entity family has them, so the single-entity cap applies. |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Focused application: universal entity criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Focused application: generic per-entity API is a universal entity criterion (fixed per-archetype rule). |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Focused application: runtime API reshaping presupposes defined entities (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A | OpenAPI documentation generated from request specs (lib/tasks/api_docs.rake); MCP tools declare output schemas (lib/discourse_mcp/output_schema.rb). No typed client generation or dry-run. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A | Themes and components are installed and configured by admins with typed, schema-validated settings and settings migrations (app/models/theme_setting.rb, theme_settings_migration.rb) and can be previewed on the live site before activation (app/controllers/admin/themes_controller.rb:12-16); page layout itself is theme code, not data. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Focused application: generic widgets from entity definitions presuppose defined entities (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 3 |  |  | A | Admin colour-scheme editor (app/models/color_scheme.rb), per-site overrides for every UI string (app/models/translation_override.rb, theme_translation_override.rb), and a translation pipeline covering thousands of locale files (translator.yml). |
| D1 Rules engine with declarative conditions and actions | assessed | 2 |  | 3 | A | By default: the automation plugin and watched words with a test mode (plugins/automation, app/models/watched_word.rb). The workflows plugin with versions, validators and test sessions is an off-by-default beta (plugins/discourse-workflows/config/settings.yml:4-11). |
| D2 Event model with webhooks or subscriptions and retry | assessed | 3 | 4 |  | A | Admin webhooks with typed event subscriptions, delivery logs (app/models/web_hook_event.rb), automatic retries (MAX_RETRY_COUNT 4, app/jobs/regular/emit_web_hook_event.rb:8) and redelivery (app/models/redelivering_webhook_event.rb). |
| D3 Sandboxed server-side hooks | assessed | 2 |  | 3 | A | By default, sandboxed code runs only as discourse-ai tool scripts with timeouts (plugins/discourse-ai/lib/agents/tool_runner.rb:44-58), and discourse-ai is off by default; the beta workflows Code node adds a sandbox with a resource budget (js_sandbox.rb, sandbox_budget.rb). |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 1 | 2 |  | A | An accessibility service and dialog components exist (frontend/discourse/tests/helpers/qunit-helpers.js:102 imports discourse/services/a11y); no automated accessibility scanning in CI. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A | Staff action logs record admin actions including site-setting changes with old and new values (app/services/staff_action_logger.rb) with an admin UI; post revisions and reviewable history; an MCP audit log with retention (config/site_settings.yml:4535). Ordinary entity mutations are not all audited. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 | 3 |  | A | User archive export (app/jobs/regular/export_user_archive.rb), anonymisation and deletion (app/services/user_anonymizer.rb, user_destroyer.rb) and purge settings; coded for the user family, not driven by field tags. |
| E4 Security as infrastructure | assessed | 2 |  |  | A | Central Guardian permission model with group and category permissions and scoped API keys (app/models/api_key_scope.rb); Dependabot configured (.github/dependabot.yml); no SAST in CI. |
| F1 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A | Site-setting history in staff logs, revertible post revisions, versioned published workflows (workflow_snapshot.rb) and git-backed remote themes; no admin rollback for settings or themes. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 1 |  | 2 | A | By default, admins change settings and themes directly. With the beta workflows plugin on, an AI author writes risk-rated draft proposals that are validated and applied by an admin (plugins/discourse-workflows/lib/discourse_workflows/ai_workflow_author.rb:39-67). |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 1 | 2 |  | A | Admins apply changes directly; the upcoming-changes framework controls rollout of Discourse's own features by status and group (lib/upcoming_changes, plugins/discourse-workflows/config/settings.yml:4-11). |
| F4 Upgrade safety | assessed | 3 |  |  | A | Plugins and themes pin compatible commits per core version (lib/version_compatibility.rb, lib/tasks/compatibility.rake); a structured deprecation API with since and drop_from (lib/discourse.rb:1185-1189); theme settings migrations (app/models/theme_settings_migration.rb). |
| G1 Indexed query path, never a scan of a generic store | assessed | 2 |  |  | A | PostgreSQL full-text search (lib/search.rb) and hand-tuned list queries; custom fields are not filterable at scale. |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 | 3 |  | A | Multisite hosting with a database per site and pervasive rate limiters; no noisy-neighbour detection or isolation verification in the repository. |
| G3 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A | Benchmark script (script/bench.rb); no documented per-surface limits or CI budgets. |
| H1 Layers deploy independently | assessed | 1 |  |  | A | Rails and Ember monolith deployed as one application; container tooling lives in a separate repository. |
| H2 Module boundaries enforced by tooling | assessed | 1 |  |  | A | Plugin API is a contract, but internal module boundaries are convention; no architectural lint. |
| H3 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A | Tests, linting and migration tests run on every pull request with no draft filter (.github/workflows/tests.yml:3-26, linting.yml, migration-tests.yml); no accessibility or security scan in CI. |
| I1 Plugin lane breadth | assessed | 3 |  |  | A | Ruby and JavaScript plugins through a versioned plugin API, theme components with typed settings, site settings, text overrides, watched words, automations, SQL badges, user fields and custom sidebar sections. |
| I2 Runtime isolation and dependency control | assessed | 2 |  |  | A | Themes run under a Content Security Policy; AI tool scripts and beta workflow code nodes are sandboxed; plugins run in-process with full trust. |
| I3 Developer loop | assessed | 2 | 3 |  | A | Theme preview on the live site, the /logs viewer for admins and a Docker development environment (bin/docker/boot_dev); the theme CLI that syncs to a live site is in another repository. |
| K1 Machine-readable capability surface for agents | assessed | 3 |  |  | A | Core MCP server with typed tools and output schemas (lib/discourse_mcp, tools for topics, posts, search, users, themes, site settings and moderation), per-primitive required scopes and annotations (primitive.rb:14-78), OAuth and group scopes and a catalog; plugins register further tools. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 1 |  | 3 | A | By default only the tutorial narrative bot is conversational (plugins/discourse-narrative-bot). With discourse-ai on (default false), AI agents answer members with retrieval and tools, and admins author workflows in natural language. |
| K3 Agent-safe actions | assessed | 2 | 3 |  | A | Granular API key scopes, user API key scopes and MCP OAuth scopes (app/models/api_key_scope.rb, user_api_key_scope.rb, mcp_oauth_authorization_scope.rb); MCP audit log; rate limiters. Idempotency is only an annotation hint; no dry-run. |
| N1 Canonical data model with a mapping layer | assessed | 1 |  |  | A | Integrations are bespoke plugins (discourse-zendesk-plugin, discourse-github, import scripts); no canonical integration model. |
| N2 Connector definition or SDK | assessed | 2 |  |  | A | Chat integration has a provider framework (plugins/discourse-chat-integration/lib/discourse_chat_integration/provider) and beta workflows have typed credential definitions (credential_types); no general connector SDK with lifecycle. |
| N3 Stable versioned contracts | assessed | 1 | 2 |  | A | No path versioning; plugin-API deprecations are structured, but the HTTP API has no deprecation windows. |
| O1 Kernel concepts are domain-neutral | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). Note that Discourse's kernel of users, groups, posts, topics, permissions and chat channels matches the rubric's level-3 kernel almost word for word. |
| O2 A new domain is expressible without kernel change | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). Chat, events, assignment, subscriptions and voting ship as code plugins on an unchanged core. |
| O3 A domain ships as an installable bundle | not_applicable | excluded |  |  | - | Focused application: adjacent-domain criterion (fixed per-archetype rule). |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 | 2 |  | A | User actions, visits, post timings and search logs are recorded as they happen and feed product features such as top topics and admin reports. |
| J2 Structured learning signals | assessed | 2 |  |  | A | Typed flags feed a review queue with triage (app/models/reviewable.rb); they concern content, not the product's definitions and versions. |
| J3 Cross-source mining inside the product | assessed | 2 | 3 |  | A | Data Explorer runs saved SQL over the whole site database including usage, moderation and support data (plugins/discourse-data-explorer); no continuous mining. |
| M1 Ranked, evidence-backed proposals for change | assessed | 2 |  |  | A | Problem checks raise admin notices recommending configuration fixes (app/services/problem_check): recommendations for one area. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 0 |  | 2 | A | By default there is no AI authoring lane; the beta workflows AI author is one when enabled. |
| M4 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A | No binding of changes to baselines or metrics. |
| P1 The product turns its own operating experience into candidate changes | assessed | 2 |  |  | A | Problem checks run on a schedule and raise configuration recommendations (app/services/problem_check); they are rules, not learning from experience. |
| P2 Learned changes are validated before they take effect | assessed | 1 |  | 2 | A | By default, changes are reviewed by people. With the workflows beta, AI proposals are validated with workflow_validate_patch before an admin applies them. |
| L1 Verification surface | assessed | 2 |  |  | A | Health endpoint /srv/status (config/routes.rb:135) and version through the about endpoint; no deployed-configuration snapshot. |
| L2 Environment reproducibility | assessed | 2 | 3 |  | A | Scripted Docker development environment (bin/docker/boot_dev), test database setup, and upcoming-change flags that ship features off by default; no per-change ephemeral environment in the repository. |
| L3 Machine verifiability | assessed | 2 |  |  | A | System specs drive browser journeys (spec/system) alongside QUnit tests; no changed-path to journey map or adoption instrumentation at ship. |

