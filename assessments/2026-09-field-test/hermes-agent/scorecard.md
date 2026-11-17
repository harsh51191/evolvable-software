# Hermes Agent: EVOLVE v0.7 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.7.0 in this repository.

Scope: the hermes-agent repository (agent loop, tools, skills, curator, approvals, gateway, MCP and ACP servers, desktop and web, CI) plus the first-party hermes-agent-self-evolution repository (DSPy and GEPA skill optimisation). Nous Portal and hosted services are out of scope.

## Reading

**SAL 1.** Issue → Fix reaches L2: background review turns corrections and failures into skill and memory changes by default (LRN-07 3), and hermes doctor diagnoses setup problems (LRN-05 2). Request → Release stops at L1 because requests are chat turns with no specification step (DEL-01 1); raising that one criterion would lift the headline. **Controls:** backup and restore cover every surface including secrets and are tested (ARC-09 3), but configuration and memory lack the rollback skills have (GOV-05 2, inventory) and background changes have no declared scope or rate limit (GOV-10 2).

## Limits

Repository evidence only. The self-evolution repository's last commit is 2026-06-17, and only phase 1 (skills) is implemented; phases 2 and 3 were not scored. No live runs were performed, so the effects of background review and the curator are read from code and documentation. Single rater.

---
Framework EVOLVE 0.7.0. Date 2026-09-30. Source github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17). Archetype **agent-runtime**. Basis **shipped** (what ships).

Scope facts true: persistent_data, schema_changes, machine_actions, agent_mutations, evolution_auto_apply, definition_change_path, code_release_path, ai_features, ai_data_access, ai_actions. False: multi_tenant, hosted_service.

Coverage: 63 assessed, 0 not evidenced, 12 not applicable. Grades: 63 A, 0 B, 0 C.

Confidence: 11 high, 31 medium, 21 low across the assessed criteria. Check these first (low confidence, and they hold a blocker or a critical control): DEL-01 (Request → Release to L2); LRN-03 (Issue → Fix to L3); EXP-04 (Opportunity → Expansion to L2); EXP-05 (Opportunity → Expansion to L2).

## Software Autonomy Level

**Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0)**

Progress toward the next level: Request → Release 3 of 4 conditions for L2; Issue → Fix 12 of 22 conditions for L3; Opportunity → Expansion 3 of 5 conditions for L2.

- With opt-in settings: Built to SAL 1 (Configurable) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0).
- With every alternate reading: Built to SAL 2 (Assisted) · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0).

| Loop | Stages | Spine | Architecture | Governance | Level | AI-driven | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L2 | L2 | L2 | **L1** | L0 | L1 |
| Issue → Fix | L2 | L2 | L2 | L2 | **L2** | L0 | L2 |
| Opportunity → Expansion | L1 | L2 | L2 | L2 | **L1** | L0 | L1 |

**Recursion: 1 By hand (LRN-10 at 1).** How far the loop improves its own checks, evaluation sets, policies and prompts from measured results.

**AI delivery.** Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

### Kinds of change

2 of 3 main kinds are self-serve (reach 1 or more: the people running the product make it themselves and can undo it).

| Kind | Who | Main | Reach | Evidence |
|---|---|---|---|---|
| What the agent knows how to do (skills) (`skills`) | the person running the agent | yes | 2 Drafted | The background review drafts and writes skills after turns, on by default (agent/background_review.py; hermes_cli/config_defaults.py:814); with skills.write_approval on, writes are staged for /skills approve (tools/write_approval.py:73-189). People install hub skills after a scan (tools/skills_hub_install.py). Undo: every mutation is ledgered and `hermes curator rollback` reverts one entry, failing closed (tools/skill_ledger.py:569, hermes_cli/curator.py:509). Reach 2 rests on DEL-04 2; nothing builds, checks and stages a skill change end to end for approval by default. Confidence high. |
| What the agent remembers and how it presents itself (`memory-persona`) | the person running the agent | yes | 0 Engineers only | The memory tool and the background review write MEMORY.md and USER.md, with scans and delete gates (tools/memory_tool.py); SOUL.md and other protected instruction files need a person (cli-config.yaml.example:573-576). No supported undo: memory files keep no history (GOV-05 inventory: memory 1). Reach 0 because the path has no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence medium. |
| Which models and providers it uses, and its settings (`models-settings`) | the person running the agent | yes | 1 Self-serve | Models and providers are selected with `hermes model` and settings changed with `hermes config` and the setup flows (hermes_cli/config_migrations.py for upgrades). Undo is selecting the previous model or value again; some writes keep point-in-time copies used only for automatic recovery (hermes_cli/config_backups.py:45-90), and there is no command to list or restore an earlier version, so larger edits have no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence medium. |
| Scheduled and recurring tasks (`scheduled-jobs`) | the person running the agent | no | 1 Self-serve | Jobs are created, paused and removed in natural language through the cronjob_manage tool, with prompt scanning (tools/cronjob_tools.py, cronjob_prompt_scan.py), or with `hermes cron` (hermes_cli/cron.py). Undo is pausing or removing the job; edits keep no earlier version. Confidence low. |
| Which tools it may use and what needs approval (`tools-approvals`) | the person running the agent | no | 1 Self-serve | Toolsets and MCP tools are enabled and disabled with `hermes tools` (hermes_cli/tools_config.py:35, tools_disable_enable_command), and approval behaviour is configuration (tools/approval_smart.py). Toggles are undone by toggling back; approval settings keep no earlier version (GOV-05 inventory: configuration 2). Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none. Confidence medium. |
| Add-ons for new platforms, providers and tools (`plugins`) | the person running the agent | no | 1 Self-serve | `hermes plugins install` from the catalogue and `hermes plugins remove\|uninstall` (hermes_cli/plugins_cmd.py:982-984, plugins_cmd_install.py, plugins_cmd_remove.py), with a plugin ledger (plugins_ledger.py). Undo is removal. Confidence medium. |

### Proven

**Proven: not evidenced.** What operating records show real changes doing, beside what the product is built to do. From a repository alone, proven is usually not evidenced.

| Loop | Built | Proven | Operating records, or what was searched |
|---|---:|---|---|
| Request → Release | L1 | not evidenced | Searched: Both repositories at the pinned commits: no operating records of requested skills or configuration changes going through the loop in a real installation (skill ledgers live in each user's HERMES_HOME). |
| Issue → Fix | L2 | not evidenced | Searched: Both repositories: no background-review or skill-ledger records from a real installation; the self-evolution reports/phase1_validation_report.pdf is a validation study, not operating records of the product's own loop. |
| Opportunity → Expansion | L1 | not evidenced | Searched: Both repositories: no records of new capabilities proposed and launched. |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 2 | fail |
| Release rollback | DEL-11 ≥ 3 | 2 | fail |
| Safe migrations | ARC-02 ≥ 3 | 2 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 3 | pass |
| Tenant isolation | ARC-05 ≥ 3 | n/a | n/a |
| Security as infrastructure | GOV-04 ≥ 3 | 3 | pass |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | 2; 2 | fail |

### What blocks the next level

- **Request → Release to L2**: stages Intake needs DEL-01 ≥ 2 (has 1)
- **Issue → Fix to L3**: spine Build needs product build path ≥ 3 (has DEL-04 2, LRN-07 3 with LRN-08 2 serving a main kind at reach 2); spine Verify needs DEL-05 ≥ 3 (has 2); spine Verify needs DEL-06 ≥ 3 (has 2); spine Roll back needs GOV-05 ≥ 3 (has 2); spine Roll back needs DEL-11 ≥ 3 (has 2); stages Detect needs LRN-03 ≥ 3 (has 2); stages Diagnose needs LRN-05 ≥ 3 (has 2); stages Propose needs LRN-06 ≥ 3 (has 2); architecture Foundation needs ARC-02 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 2)
- **Opportunity → Expansion to L2**: stages Sense needs EXP-04 ≥ 2 (has 1); stages Propose needs EXP-05 ≥ 2 (has 1)

### What AI drives

Each loop re-scored with its AI-performable stages read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level.

| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |
|---|---:|---:|---|---|
| Request → Release | L1 | L0 | DEL-01 1, DEL-04 2 | DEL-01 ≥ 2 (has 1) |
| Issue → Fix | L2 | L0 | LRN-05 1, LRN-06 2, LRN-07 3, LRN-08 2 | LRN-05 ≥ 2 (has 1) |
| Opportunity → Expansion | L1 | L0 | EXP-05 1 | EXP-05 ≥ 2 (has 1) |

### Sensitivity

- **Fragile:** the headline drops if any of these falls one level: DEL-04, DEL-11, LRN-03, GOV-05.
- **One step away:** raising any of these one level lifts the headline: DEL-01.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 2.3 | 2.3–2.8 | 2.3 | 2.3 | 1.8 |
| Velocity (DEL) | 1.8 | 1.8–2.3 | 1.8 | 1.8 | 1.8 |
| Open (MAL) | 2.2 | 2.2–2.5 | 2.2 | 2.2 | 1.9 |
| Learn (LRN) | 2.1 | 2.1–2.6 | 2.2 | 2.1 | 2.1 |
| Vet (GOV) | 2.1 | 2.1–2.4 | 2.3 | 2.1 | 2.1 |
| Expand (EXP) | 1.7 | 1.7–1.9 | 1.7 | 1.7 | 1.7 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 2.0 |
| ARC Resilience | 2.5 |
| DEL Intake | 1.0 |
| DEL Build | 2.0 |
| DEL Verify | 2.0 |
| DEL Release | 2.0 |
| MAL APIs | 2.0 |
| MAL Interface | 1.5 |
| MAL Behaviour | 2.0 |
| MAL Extensions | 2.7 |
| MAL Integrations | 2.7 |
| MAL Agent interface | 2.5 |
| LRN Sense | 2.3 |
| LRN Diagnose and propose | 2.0 |
| LRN Learn from experience | 2.5 |
| LRN Measure | 1.5 |
| GOV Compliance and security | 2.0 |
| GOV Change control | 2.3 |
| GOV AI and self-change safety | 2.0 |
| EXP Expressible | 3.0 |
| EXP Discover | 1.0 |
| EXP Launch | 1.0 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 2 · not production-governed**

- With opt-in settings: AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 2 · not production-governed.
- With every alternate reading: AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 2 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 3 | AIR-03 3, AIR-04 3 |
| Quality | 1 | AIR-05 2, AIR-06 1 |
| Governance | 2 | AIR-07 3, GOV-09 (AI) 2, GOV-10 (AI) 2, GOV-11 (AI) 2, LRN-08 (AI) 2 |
| Operations | 2 | AIR-01 3, AIR-02 2, AIR-08 1, ARC-08 (AI) 3 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 3 | pass |
| Regression evaluation before release | AIR-06 ≥ 3 | 1 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 3 | pass |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 2 | MAL-19 2, MAL-20 3 |
| Build | 1 | DEL-01 1, DEL-04 2 |
| Diagnose and improve | 2 | LRN-05 1, LRN-06 2, LRN-07 3, LRN-08 2 |
| Expand | 1 | EXP-05 1 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - |  | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| ARC-02 Safe schema and data migrations | assessed | 2 | 3 |  | A, medium | IT | The state database migrates forward on start (hermes_state_schema.py) and hermes update takes a pre-update snapshot it restores when an update fails (hermes_cli/update_cmd.py:109-110), with migration tests (tests/hermes_state). |
| ARC-03 Horizontal scale of services | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user. |
| ARC-04 Reliable asynchronous work | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user. |
| ARC-05 Tenant isolation and noisy-neighbour controls | not_applicable | excluded |  |  | - |  | Scope fact multi_tenant is false: One user per installation; profiles are separate homes, not tenants. |
| ARC-06 Ceilings measured, not discovered in incidents | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user. |
| ARC-07 Service objectives defined and monitored | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A, high |  | AI-qualified reading: 3. Fallback providers and credential pools take over when a primary model fails (agent/agent_init.py, tests/agent/test_restore_primary_pool_reselect.py); tool and MCP failures are contained to the turn. Plugins and gateway platforms have no breakers, so a 3 is not defensible under the inventory rule. |
| ARC-09 Backup, restore and recovery | assessed | 3 |  |  | A, high | IT | Inventory: data 3, definitions 3, files 3, secrets 3, schedules 3. hermes backup and import cover the home directory: the sessions database (snapshotted with sqlite3.backup), skills, memory, configuration and secrets such as .env, auth.json and the vault (hermes_cli/backup.py:117-161), with pre-update backups and round-trip tests (tests/hermes_cli/test_backup*.py). No recovery objectives are stated (level 4). Scheduled work: cron/jobs.json is in every backup and jobs lost during an update are restored automatically (hermes_cli/backup.py:1059, 1600-1665); hermes cron list shows each job's next run (hermes_cli/cron.py:125); jobs run under their own profile (cron/jobs.py:64-68); a pre-run check, on by default, blocks and alerts on jobs whose provider key, delivery target or skills no longer resolve (cron/scheduler_preflight.py:80-90, 387), with tests (tests/cron/test_preflight_credential_verdict_names_home.py). |
| DEL-01 Request intake into a structured change specification | assessed | 1 | 2 |  | A, low |  | AI-qualified reading: 1. Requests are chat turns; the agent can create a skill when asked, without a specification step. |
| DEL-02 Layers deploy independently | assessed | 2 |  |  | A, medium |  | Python agent, gateway, desktop, web and sandbox images are separate artifacts built from one repository (Dockerfile, .github/workflows/sandbox-image.yml, desktop-bundled-release.yml). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 |  |  | A, medium |  | Import guards in CI (.github/workflows/lazy-deps-guard.yml, case-collision-check.yml); no architectural boundary lint. |
| DEL-04 AI implementation lane | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. The background review is an autonomous authoring lane that applies skill and memory changes every turn (agent/background_review.py); GEPA improvements reach every user through upstream pull requests. Scored at the lower reading under rule 11 because: The cross-user path depends on an offline companion tool. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A, medium |  | Python, JavaScript and Rust tests, lint, Nix, OSV, supply-chain, desktop E2E and install E2E run in CI with no draft filter (.github/workflows/tests.yml, js-tests.yml, rust-tests.yml, e2e-desktop.yml); no accessibility check. |
| DEL-06 Verification surface | assessed | 2 |  |  | A, medium |  | Version reporting and state health checks (hermes_state_health.py) and a configuration display; no machine-readable deployed-configuration endpoint. |
| DEL-07 Environment reproducibility | assessed | 2 | 3 |  | A, low |  | Nix flake and lock files reproduce the environment (flake.nix, uv.lock); install E2E jobs build fresh environments per run. |
| DEL-08 Machine verifiability | assessed | 2 |  |  | A, low |  | Behaviour probes (evals/), desktop and install E2E suites; no changed-path map or adoption instrumentation at ship. |
| DEL-09 Staged exposure | assessed | 2 |  |  | A, medium |  | Update channels let an installation take canary builds before stable (hermes_cli/update_channel.py); skill and memory changes are not staged. |
| DEL-10 Kill switch | assessed | 2 |  |  | A, low |  | Background review and individual skills can be switched off in configuration at runtime; curator archives remove skills without a release. |
| DEL-11 Release rollback | assessed | 2 | 3 |  | A, medium | IT | Two code paths. Product releases: hermes update rolls back a pulled tree that fails a syntax check and restores the state snapshot on failure (hermes_cli/update_cmd.py:840-870); there is no one-step rollback to the previous release. Code the agent writes into skills: every skill mutation, supporting files included, is ledgered with before and after snapshots and can be rolled back one entry at a time with `hermes curator rollback`, failing closed (tools/skill_ledger.py:569, hermes_cli/curator.py:509). Re-checked for v0.7 after the code_release_path grounds changed; score unchanged. |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-02 Field definitions carry type and validation | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A, medium |  | Typed tool schemas (model_tools.py, toolsets.py) served over MCP (mcp_serve.py) and the Agent Client Protocol (acp_adapter); no OpenAPI description of the serve API and no dry-run. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 1 |  |  | A, medium |  | CLI, TUI, desktop and web layouts are code; persona text (SOUL.md) is data but is not layout. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A, low |  | UI strings externalised in locales/ and translated READMEs; themes are engineer-managed. |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A, low |  | Cron jobs are defined in natural language or the CLI and run agent tasks on schedules (cron/); plugin hooks add behaviour; there is no general condition and action engine. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A, medium |  | Gateway adapters receive platform and webhook events; the MCP server lets clients poll live events (mcp_serve.py); no retry or replay for outbound subscribers. |
| MAL-12 Sandboxed server-side hooks | assessed | 2 |  |  | A, medium |  | Plugins register hooks that run in-process without a sandbox (plugins/); the agent's own commands can run in Docker, SSH or remote sandbox backends with guards (tools/terminal_tool_backends.py, terminal_tool_guards.py). |
| MAL-13 Plugin lane breadth | assessed | 3 | 4 |  | A, medium |  | Declarative skills (SKILL.md), Python plugins with hooks, MCP servers, providers and a plugin catalogue with hundreds of entries (plugin-catalog/, skills/, optional-skills/, optional-mcps/). |
| MAL-14 Runtime isolation and dependency control | assessed | 2 | 3 |  | A, medium |  | Hub skills are scanned and installed only after confirmation (tools/skills_hub_install.py, skills_guard.py); plugins run with full trust; commands can be sent to sandbox backends. |
| MAL-15 Developer loop | assessed | 3 |  |  | A, medium |  | Skill linter (tools/skill_linter.py), curator dry-run (hermes curator run --dry-run), logs (hermes_logging.py) and local iteration against the user's own profile. |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A, medium |  | One provider layer maps many model vendors onto a canonical chat interface (providers/, agent/*_adapter.py), and one gateway maps Telegram, Discord, Slack, WhatsApp and other platforms onto a canonical conversation model (gateway/). |
| MAL-17 Connector definition or SDK | assessed | 3 |  |  | A, medium |  | Plugin catalogue entries, provider adapters, platform adapters and MCP servers cover auth, messaging and lifecycle; skill hub sources include official, GitHub, ClawHub and skills.sh (tools/skills_hub_*.py). |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A, low |  | Standard protocols (MCP, ACP, OpenAI-compatible APIs) and versioned configuration; no deprecation windows. |
| MAL-19 Machine-readable capability surface for agents | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. MCP server exposing conversation, messaging, event and approval tools (mcp_serve.py) and an ACP adapter for editors (acp_adapter/); typed tool registry (model_tools.py). Scored at the lower reading under rule 11 because: The MCP surface covers messaging, not the full capability set. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A, low |  | AI-qualified reading: 3. Users complete tasks conversationally across CLI, desktop and messaging platforms with tool actions; users author skills, memory and cron jobs in natural language, with staged approvals as preview when enabled; evaluation probes (evals/) and GEPA evaluation datasets. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 3 | 4 |  | A, medium |  | The session database with full-text search is available to the agent in real time (hermes_state_fts.py, hermes_state_search.py); every skill gets view, use and patch counts automatically (tools/skill_usage.py). |
| LRN-02 Structured learning signals | assessed | 2 | 3 |  | A, medium |  | Every skill has view, use and patch counts linked to it (tools/skill_usage.py), and the curator triages skills into active, stale and archived (website/docs/user-guide/features/curator.md). Scored at the lower reading under rule 11 because: Usage counts are not versioned per skill revision. |
| LRN-03 User-issue detection | assessed | 2 |  |  | A, low |  | Background review sees corrections and failures in recent turns, and evals record failures found in use (evals/). |
| LRN-04 Cross-source mining inside the product | assessed | 2 | 3 |  | A, low |  | Session search over the agent's own history; the self-evolution repo builds evaluation datasets from Hermes, Claude Code and Copilot session histories (README, --eval-source sessiondb). No continuous mining in the product. |
| LRN-05 Automated diagnosis | assessed | 2 |  |  | A, high |  | AI-qualified reading: 1. hermes doctor diagnoses setup problems and cron error diagnostics attach context to failing jobs (hermes_cli/main.py:2567). |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. After each turn a background fork proposes skill and memory updates grounded in the conversation (agent/background_review.py); GEPA ranks skill variants on a Pareto front with evaluation evidence (self-evolution repo). Covers skills only. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 3 | 4 |  | A, medium |  | AI-qualified reading: 3. background_review is enabled by default (hermes_cli/config_defaults.py:814): after turns, a forked agent decides whether to save or update skills and memory (agent/background_review.py). |
| LRN-08 Learned changes are validated before they take effect | assessed | 2 |  | 3 | A, high | IT | AI-qualified reading: 2. Re-checked for v0.7 under the tightened boundary; unchanged. Skill writes by the agent and the background review pass security scans, AST audits and a linter (tools/skills_guard.py, skills_ast_audit.py, skill_linter.py), and memory writes are scanned and destructive background deletes gated (tools/memory_tool.py:44, 84-205). The first-party optimiser evaluates variants against the baseline skill on a holdout set before proposing, when a person runs it (hermes-agent-self-evolution evolution/skills/evolve_skill.py:185-210). |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A, medium |  | The curator keeps, marks stale or archives skills from measured usage over fixed windows (14 and 30 days, website/docs/user-guide/features/curator.md); GEPA compares variants against the baseline skill before proposing. Nothing measures the outcome of an applied skill in use. |
| LRN-10 The improvement loop improves itself | assessed | 1 |  |  | A, medium |  | The checks that govern change are code: skill scans, AST audit and linter (tools/skills_guard.py, skills_ast_audit.py, skill_linter.py), the memory scan and write gates (tools/memory_tool.py) and the optimiser's fixed constraint gates (hermes-agent-self-evolution evolution/core/constraints.py:24-174). People improve evaluation material by hand outside the product: regression probes in evals/ (69 entries) are written by engineers, and the optimiser builds an evaluation set per run from synthetic cases, mined session history or hand-curated golden sets (evolution/core/dataset_builder.py, external_importers.py) when a person runs it. Nothing records a wrong pass against the check that missed it, evaluation sets are not versioned through the product's change path, and policy changes do not cite results. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 |  |  | A, low |  | No automated accessibility scanning found for the TUI, desktop or web interfaces. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A, medium |  | Every skill mutation by any actor is appended to a JSONL ledger with content-addressed before and after snapshots (tools/skill_ledger.py); staged approvals are recorded; sessions are stored in SQLite. Configuration and memory changes are not in the ledger. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A, medium |  | Session export and import (hermes_state_portability.py) and user-editable memory files; data stays on the user's machine; not driven by tags. |
| GOV-04 Security as infrastructure | assessed | 3 |  |  | A, high | IT | Command scanning with tirith and dangerous-command approvals with an LLM risk classifier and floors (tools/approval_smart.py, approval_floors.py); skill security scans and AST audits before install or write (tools/skills_guard.py, skills_ast_audit.py); OSV and supply-chain scans in CI (.github/workflows/osv-scanner.yml, supply-chain-audit.yml). |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A, medium |  | Inventory: skills 3, configuration 2, memory 1. Skills have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py) and curator archives are restorable, but configuration has only point-in-time copies on some writes (hermes_cli/config_backups.py) and memory files have no history. Under the inventory rule a 3 needs every default surface at 3. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 2 |  | 3 | A, high |  | By default, skill and memory writes apply directly and are ledgered. With skills.write_approval or memory.write_approval on, writes are staged with a gist and applied through /skills approve (tools/write_approval.py:73-189); the self-evolution repo proposes evaluated skill variants as pull requests. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 |  | 3 | A, high |  | By default only protected instruction files always need a human (cli-config.yaml.example:573-576); skill and memory gates default to off (hermes_cli/config_defaults.py:1320). With them on, each change class has its own gate. |
| GOV-08 Upgrade safety | assessed | 3 |  |  | A, high |  | Numbered configuration migrations run on update (hermes_cli/config_migrations.py:379-397); bundled-skill sync updates shipped skills without overwriting user copies (tools/skills_sync*.py); skills follow the agentskills.io specification. |
| GOV-09 Agent-safe actions | assessed | 2 | 3 |  | A, low |  | AI-qualified reading: 2. Dangerous-command approvals with LLM risk classification and floors, tirith scanning, sandbox backends, subagent auto-deny and session audit; commands otherwise run with the user's ambient authority; no idempotency keys. |
| GOV-10 Bounded self-change | assessed | 2 |  |  | A, medium |  | AI-qualified reading: 2. Protected instruction files always need a person, and skill writes pass scans and an AST audit (tools/skills_guard.py); there is no declared scope or rate limit for background changes. |
| GOV-11 Learning-input integrity | assessed | 2 | 3 |  | A, medium |  | AI-qualified reading: 2. The skill ledger records the actor of every mutation (tools/skill_ledger.py:54-68) and the skills guard scans writes for injection and exfiltration patterns (tools/skills_guard.py:42-140); session content can still drive an automatically applied skill change. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 |  |  | A, low |  | Kernel of sessions (conversation), gateway platforms (channel), profiles (identity), approvals (permission), cron and delegation (workflow), and skills and files (content); no domain nouns. |
| EXP-02 A new domain is expressible without kernel change | assessed | 3 | 4 |  | A, low |  | Many domains ship as skill bundles on an unchanged kernel (skills/, optional-skills/), and the agent creates new domain skills itself. Scored at the lower reading under rule 11 because: If skills are judged too small to count as domains. |
| EXP-03 A domain ships as an installable bundle | assessed | 3 | 4 |  | A, low |  | Skills are versionable, installable bundles under the agentskills.io specification, installed from the hub with scanning and synced on update. |
| EXP-04 Unmet-demand sensing | assessed | 1 |  |  | A, low |  | Unserved requests stay in session history; nothing records them as unmet demand. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 1 |  |  | A, low |  | AI-qualified reading: 1. Background review creates skills for tasks it has just done; it does not propose capabilities nobody has used yet. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 |  |  | A, low |  | New skills apply to the whole installation at once. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A, medium |  | Session search over full-text indexes, memory and skills injected into context, with memory provider plugins (hermes_state_fts.py, plugins). |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 3 |  |  | A, high | IT | A single-user agent acting with the user's own permissions; the gateway accepts only paired users, profiles isolate homes, and dangerous commands need approval (tools/approval_smart.py), with security tests (tests/security). |
| AIR-05 Offline AI evaluation | assessed | 2 |  |  | A, low |  | Regression probes named after failures found in use (evals/) and GEPA skill evaluation in the companion repository, run on request. |
| AIR-06 Regression gating before release | assessed | 1 |  |  | A, low |  | Evaluations are not part of CI. |
| AIR-07 AI action tracing and auditability | assessed | 3 |  |  | A, high | IT | Sessions record every message, tool call and model in the state database, with trajectories and trace upload (agent/trajectory.py, trace_upload.py, hermes_state_*.py), queryable through hermes sessions and insights. |
| AIR-01 Model and provider portability and resilience | assessed | 3 |  |  | A, high |  | Fallback providers and credential pools take over when a primary model fails, with tests (agent/agent_init.py, tests/agent/test_restore_primary_pool_reselect.py). |
| AIR-02 AI usage and per-customer cost controls | assessed | 2 | 3 |  | A, medium |  | Usage and pricing per turn and per account are tracked (agent/usage_pricing.py, turn_usage.py, billing_usage.py) and iterations are budgeted (agent/iteration_budget.py); no spend limit per user. |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 1 |  |  | A, low |  | Skill usage counts feed the curator; no quality or feedback monitoring of the agent's answers. |

Grade cell: evidence grade, then confidence where recorded. Facets: I implemented, T tested, O operated. Operated supports a Proven reading and never changes a score.
