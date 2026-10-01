# Discourse: scope

| Item | Value |
|---|---|
| Software | Discourse, an open-source community discussion platform (Ruby on Rails, Ember) |
| Repository and tip | `github.com/discourse/discourse` @ `2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b`, `main`, committed 2026-09-29 |
| Assessment date | 2026-09-30 |
| Declared archetype | `focused-application` |
| In scope | Core application, the bundled plugins in `plugins/` (automation, discourse-ai, discourse-workflows, data explorer, chat and others), the core MCP server, CI configuration |
| Out of scope | Hosted Discourse, the `discourse_docker` and theme CLI repositories, third-party plugins |

## Archetype decision

Discourse is a discussion product with deep configuration, not a platform for defining business objects, so `focused-application`. `configurable-application-platform` was considered and rejected: there is no way to define new entity types. The last index column in `scorecard.md` shows the result if every criterion is counted.

## Not-applicable decisions

The fixed rule for `focused-application` in `references/archetypes.md` (enforced by the scorer) excludes A1, A3, B1, B2 and C2 (universal entity) and O1, O2 and O3 (adjacent-domain expansion), Each exclusion records what it would have scored.

## Beta features

`discourse-workflows` (`enable_discourse_workflows`, default false, "upcoming change" status beta) and `discourse-ai` (`discourse_ai_enabled`, default false) ship in the repository but are off by default. The rubric does not say how to treat shipped-but-disabled capabilities. They were scored as shipped, with alternates showing the effect of excluding them.

## EVOLVE v0.4 scope facts

Declared for the default configuration. They decide which criteria and critical controls apply (`references/archetypes.md`).

| Fact | Value | Evidence |
|---|---|---|
| `persistent_data` | true | Posts, users and settings in PostgreSQL; uploads on disk or S3. |
| `schema_changes` | true | Rails migrations (db/migrate, 1,765 files) change the schema on every upgrade. |
| `multi_tenant` | true | Multisite hosting serves several forums from one deployment, each with its own database. |
| `hosted_service` | true | Puma web processes and Sidekiq workers run as long-lived services. |
| `machine_actions` | true | The admin API with scoped API keys changes content and settings (app/models/api_key_scope.rb). |
| `agent_mutations` | false | By default no AI changes Discourse definitions: discourse-ai and the workflows AI author are off by default. |
| `evolution_auto_apply` | false | Admins apply changes directly; nothing applies definition changes automatically by default. |
| `definition_change_path` | true | Site settings, themes, categories and automations are definitions. |
| `code_release_path` | false | No first-party evolution system ships code changes. |
