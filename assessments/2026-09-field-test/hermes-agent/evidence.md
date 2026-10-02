# Hermes Agent evidence

Read at github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Sessions in SQLite, plus skills, memory and configuration under HERMES_HOME.
- **schema_changes**: true. The state database is versioned and migrated on start (hermes_state_schema.py, SCHEMA_VERSION).
- **multi_tenant**: false. One user per installation; profiles are separate homes, not tenants.
- **hosted_service**: false. A local single-user agent; the gateway relays messaging platforms for the same user.
- **machine_actions**: true. The agent's tools change its own skills, memory and configuration, and the MCP and ACP servers expose it to other clients (mcp_serve.py, acp_adapter).
- **agent_mutations**: true. The background review writes skills and memory (agent/background_review.py).
- **evolution_auto_apply**: true. background_review is on by default and skill and memory write approvals default to off (hermes_cli/config_defaults.py:814, 1320).
- **definition_change_path**: true. Skills, memory, prompts and configuration are its definitions.
- **code_release_path**: true. The first-party GEPA optimiser proposes improved skills as pull requests to this repository, shipped in releases (hermes-agent-self-evolution).
- **ai_features**: true. The product is an LLM agent.
- **ai_data_access**: true. Reads the user's files, sessions, memory and skills (session search, memory providers).
- **ai_actions**: true. Runs commands, edits files and sends messages on the user's behalf (tools/).

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **ARC-02 Safe schema and data migrations**: **2** (grade A), facets: implemented, tested. The state database migrates forward on start (hermes_state_schema.py) and hermes update takes a pre-update snapshot it restores when an update fails (hermes_cli/update_cmd.py:109-110), with migration tests (tests/hermes_state).
  - Higher reading 3: Snapshot restore is a tested rollback path.

### Scale

- **ARC-03 Horizontal scale of services**: **not applicable**. Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user.
- **ARC-04 Reliable asynchronous work**: **not applicable**. Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **not applicable**. Scope fact multi_tenant is false: One user per installation; profiles are separate homes, not tenants. If counted: 2.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **not applicable**. Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user. If counted: 1.
- **ARC-07 Service objectives defined and monitored**: **not applicable**. Scope fact hosted_service is false: A local single-user agent; the gateway relays messaging platforms for the same user.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A). Fallback providers and credential pools take over when a primary model fails (agent/agent_init.py, tests/agent/test_restore_primary_pool_reselect.py); tool and MCP failures are contained to the turn. Plugins and gateway platforms have no breakers, so a 3 is not defensible under the inventory rule.
  - AI-qualified reading: **3** (grade A), facets: implemented, tested. Fallback providers and credential pools contain provider failure, with tests.
- **ARC-09 Backup, restore and recovery**: **3** (grade A), facets: implemented, tested. hermes backup and import cover the home directory: the sessions database (snapshotted with sqlite3.backup), skills, memory, configuration and secrets such as .env, auth.json and the vault (hermes_cli/backup.py:117-161), with pre-update backups and round-trip tests (tests/hermes_cli/test_backup*.py). No recovery objectives are stated (level 4). Scheduled work: cron/jobs.json is in every backup and jobs lost during an update are restored automatically (hermes_cli/backup.py:1059, 1600-1665); hermes cron list shows each job's next run (hermes_cli/cron.py:125); jobs run under their own profile (cron/jobs.py:64-68); a pre-run check, on by default, blocks and alerts on jobs whose provider key, delivery target or skills no longer resolve (cron/scheduler_preflight.py:80-90, 387), with tests (tests/cron/test_preflight_credential_verdict_names_home.py).
  - Inventory: data 3, definitions 3, files 3, secrets 3, schedules 3

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **1** (grade A). Requests are chat turns; the agent can create a skill when asked, without a specification step.
  - Higher reading 2: Skill creation on request records name and description.
  - AI-qualified reading: **1** (grade A). Requests arrive as chat turns.
    - Higher reading 2: Skill creation records name and description.

### Build

- **DEL-02 Layers deploy independently**: **2** (grade A). Python agent, gateway, desktop, web and sandbox images are separate artifacts built from one repository (Dockerfile, .github/workflows/sandbox-image.yml, desktop-bundled-release.yml).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A). Import guards in CI (.github/workflows/lazy-deps-guard.yml, case-collision-check.yml); no architectural boundary lint.
- **DEL-04 AI implementation lane**: **2** (grade A). The background review is an autonomous authoring lane that applies skill and memory changes every turn (agent/background_review.py); GEPA improvements reach every user through upstream pull requests. Scored at the lower reading under rule 11 because: The cross-user path depends on an offline companion tool.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A). Background review is a model lane that applies skill and memory changes.
    - Higher reading 3: Autonomous by default.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A). Python, JavaScript and Rust tests, lint, Nix, OSV, supply-chain, desktop E2E and install E2E run in CI with no draft filter (.github/workflows/tests.yml, js-tests.yml, rust-tests.yml, e2e-desktop.yml); no accessibility check.
  - Higher reading 3: Every change class except accessibility is checked.
- **DEL-06 Verification surface**: **2** (grade A). Version reporting and state health checks (hermes_state_health.py) and a configuration display; no machine-readable deployed-configuration endpoint.
- **DEL-07 Environment reproducibility**: **2** (grade A). Nix flake and lock files reproduce the environment (flake.nix, uv.lock); install E2E jobs build fresh environments per run.
  - Higher reading 3: Reproducible environments are built per change in CI.
- **DEL-08 Machine verifiability**: **2** (grade A). Behaviour probes (evals/), desktop and install E2E suites; no changed-path map or adoption instrumentation at ship.

### Release

- **DEL-09 Staged exposure**: **2** (grade A). Update channels let an installation take canary builds before stable (hermes_cli/update_channel.py); skill and memory changes are not staged.
- **DEL-10 Kill switch**: **2** (grade A). Background review and individual skills can be switched off in configuration at runtime; curator archives remove skills without a release.
- **DEL-11 Release rollback**: **2** (grade A), facets: implemented, tested. hermes update rolls back a pulled tree that fails a syntax check and restores the state snapshot on failure (hermes_cli/update_cmd.py:840-870); there is no one-step rollback to the previous release.
  - Higher reading 3: Failed updates roll back automatically.

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **2** (grade A). Typed tool schemas (model_tools.py, toolsets.py) served over MCP (mcp_serve.py) and the Agent Client Protocol (acp_adapter); no OpenAPI description of the serve API and no dry-run.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **1** (grade A). CLI, TUI, desktop and web layouts are code; persona text (SOUL.md) is data but is not layout.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A). UI strings externalised in locales/ and translated READMEs; themes are engineer-managed.

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A). Cron jobs are defined in natural language or the CLI and run agent tasks on schedules (cron/); plugin hooks add behaviour; there is no general condition and action engine.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A). Gateway adapters receive platform and webhook events; the MCP server lets clients poll live events (mcp_serve.py); no retry or replay for outbound subscribers.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A). Plugins register hooks that run in-process without a sandbox (plugins/); the agent's own commands can run in Docker, SSH or remote sandbox backends with guards (tools/terminal_tool_backends.py, terminal_tool_guards.py).

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A). Declarative skills (SKILL.md), Python plugins with hooks, MCP servers, providers and a plugin catalogue with hundreds of entries (plugin-catalog/, skills/, optional-skills/, optional-mcps/).
  - Higher reading 4: A versioned registry and hub exist.
- **MAL-14 Runtime isolation and dependency control**: **2** (grade A). Hub skills are scanned and installed only after confirmation (tools/skills_hub_install.py, skills_guard.py); plugins run with full trust; commands can be sent to sandbox backends.
  - Higher reading 3: Scanned skills plus sandboxed command backends isolate most third-party and AI-written code.
- **MAL-15 Developer loop**: **3** (grade A). Skill linter (tools/skill_linter.py), curator dry-run (hermes curator run --dry-run), logs (hermes_logging.py) and local iteration against the user's own profile.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A). One provider layer maps many model vendors onto a canonical chat interface (providers/, agent/*_adapter.py), and one gateway maps Telegram, Discord, Slack, WhatsApp and other platforms onto a canonical conversation model (gateway/).
- **MAL-17 Connector definition or SDK**: **3** (grade A). Plugin catalogue entries, provider adapters, platform adapters and MCP servers cover auth, messaging and lifecycle; skill hub sources include official, GitHub, ClawHub and skills.sh (tools/skills_hub_*.py).
- **MAL-18 Stable versioned contracts**: **2** (grade A). Standard protocols (MCP, ACP, OpenAI-compatible APIs) and versioned configuration; no deprecation windows.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A). MCP server exposing conversation, messaging, event and approval tools (mcp_serve.py) and an ACP adapter for editors (acp_adapter/); typed tool registry (model_tools.py). Scored at the lower reading under rule 11 because: The MCP surface covers messaging, not the full capability set.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A). MCP server and ACP adapter (mcp_serve.py, acp_adapter).
    - Higher reading 3: Typed tool registry.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). Users complete tasks conversationally across CLI, desktop and messaging platforms with tool actions; users author skills, memory and cron jobs in natural language, with staged approvals as preview when enabled; evaluation probes (evals/) and GEPA evaluation datasets.
  - Higher reading 4: Almost every capability is reachable conversationally.
  - AI-qualified reading: **3** (grade A). Model-backed conversation across platforms; skills and memory authored in natural language.
    - Higher reading 4: Broad coverage.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **3** (grade A). The session database with full-text search is available to the agent in real time (hermes_state_fts.py, hermes_state_search.py); every skill gets view, use and patch counts automatically (tools/skill_usage.py).
  - Higher reading 4: Per-definition instrumentation is added automatically for every skill.
- **LRN-02 Structured learning signals**: **2** (grade A). Every skill has view, use and patch counts linked to it (tools/skill_usage.py), and the curator triages skills into active, stale and archived (website/docs/user-guide/features/curator.md). Scored at the lower reading under rule 11 because: Usage counts are not versioned per skill revision.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
- **LRN-03 User-issue detection**: **2** (grade A). Background review sees corrections and failures in recent turns, and evals record failures found in use (evals/).
- **LRN-04 Cross-source mining inside the product**: **2** (grade A). Session search over the agent's own history; the self-evolution repo builds evaluation datasets from Hermes, Claude Code and Copilot session histories (README, --eval-source sessiondb). No continuous mining in the product.
  - Higher reading 3: Cross-source session mining exists, offline.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **2** (grade A). hermes doctor diagnoses setup problems and cron error diagnostics attach context to failing jobs (hermes_cli/main.py:2567).
  - AI-qualified reading: **1** (grade A). The agent explains errors when asked; hermes doctor is rule-based.
- **LRN-06 Ranked, evidence-backed proposals for change**: **2** (grade A). After each turn a background fork proposes skill and memory updates grounded in the conversation (agent/background_review.py); GEPA ranks skill variants on a Pareto front with evaluation evidence (self-evolution repo). Covers skills only.
  - Higher reading 3: Ranked, evidence-backed proposals with expected impact exist for the agent's main behaviour surface.
  - AI-qualified reading: **2** (grade A). A background fork proposes skill and memory updates from the conversation.
    - Higher reading 3: GEPA ranks variants.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **3** (grade A). background_review is enabled by default (hermes_cli/config_defaults.py:814): after turns, a forked agent decides whether to save or update skills and memory (agent/background_review.py).
  - Higher reading 4: The curator's consolidation learns which skills stick, but only when enabled.
  - AI-qualified reading: **3** (grade A). Model reflection after turns writes skills and memory by default.
    - Higher reading 4: Learns from GEPA results.
- **LRN-08 Learned changes are validated before they take effect**: **2** (grade A), **3** with opt-in settings, facets: implemented, tested. Skill writes pass security scans, AST audits and a linter (tools/skills_guard.py, skills_ast_audit.py, skill_linter.py). The first-party GEPA optimiser evaluates variants against the baseline skill before proposing, when it is run (hermes-agent-self-evolution README).
  - AI-qualified reading: **2** (grade A), **3** with opt-in settings, facets: implemented, tested. AI-written skills pass scans, AST audits and a linter.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **2** (grade A). The curator keeps, marks stale or archives skills from measured usage over fixed windows (14 and 30 days, website/docs/user-guide/features/curator.md); GEPA compares variants against the baseline skill before proposing. Nothing measures the outcome of an applied skill in use.
  - Higher reading 3: The curator records a metric, window and explicit keep or archive decision per skill.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). No automated accessibility scanning found for the TUI, desktop or web interfaces.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **2** (grade A). Every skill mutation by any actor is appended to a JSONL ledger with content-addressed before and after snapshots (tools/skill_ledger.py); staged approvals are recorded; sessions are stored in SQLite. Configuration and memory changes are not in the ledger.
  - Higher reading 3: Skills are the main definition surface and are fully audited with approvals.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Session export and import (hermes_state_portability.py) and user-editable memory files; data stays on the user's machine; not driven by tags.
- **GOV-04 Security as infrastructure**: **3** (grade A), facets: implemented, tested. Command scanning with tirith and dangerous-command approvals with an LLM risk classifier and floors (tools/approval_smart.py, approval_floors.py); skill security scans and AST audits before install or write (tools/skills_guard.py, skills_ast_audit.py); OSV and supply-chain scans in CI (.github/workflows/osv-scanner.yml, supply-chain-audit.yml).

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **2** (grade A). Skills have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py) and curator archives are restorable, but configuration has only point-in-time copies on some writes (hermes_cli/config_backups.py) and memory files have no history. Under the inventory rule a 3 needs every default surface at 3.
  - Inventory: skills 3, configuration 2, memory 1
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **2** (grade A), **3** with opt-in settings. By default, skill and memory writes apply directly and are ledgered. With skills.write_approval or memory.write_approval on, writes are staged with a gist and applied through /skills approve (tools/write_approval.py:73-189); the self-evolution repo proposes evaluated skill variants as pull requests.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A), **3** with opt-in settings. By default only protected instruction files always need a human (cli-config.yaml.example:573-576); skill and memory gates default to off (hermes_cli/config_defaults.py:1320). With them on, each change class has its own gate.
- **GOV-08 Upgrade safety**: **3** (grade A). Numbered configuration migrations run on update (hermes_cli/config_migrations.py:379-397); bundled-skill sync updates shipped skills without overwriting user copies (tools/skills_sync*.py); skills follow the agentskills.io specification.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A). Dangerous-command approvals with LLM risk classification and floors, tirith scanning, sandbox backends, subagent auto-deny and session audit; commands otherwise run with the user's ambient authority; no idempotency keys.
  - Higher reading 3: Per-action risk classification and approval previews are level 3 and 4 features.
  - AI-qualified reading: **2** (grade A). Dangerous commands need approval with LLM risk classification; the agent acts with the user's authority.
    - Higher reading 3: Approval floors.
- **GOV-10 Bounded self-change**: **2** (grade A). Protected instruction files always need a person, and skill writes pass scans and an AST audit (tools/skills_guard.py); there is no declared scope or rate limit for background changes.
  - AI-qualified reading: **2** (grade A). Protected files and write scans; no declared scope or rate limit.
- **GOV-11 Learning-input integrity**: **2** (grade A). The skill ledger records the actor of every mutation (tools/skill_ledger.py:54-68) and the skills guard scans writes for injection and exfiltration patterns (tools/skills_guard.py:42-140); session content can still drive an automatically applied skill change.
  - Higher reading 3: Provenance and injection scanning are both present.
  - AI-qualified reading: **2** (grade A). Ledger actor and injection scans on skill writes.
    - Higher reading 3: Both present.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of sessions (conversation), gateway platforms (channel), profiles (identity), approvals (permission), cron and delegation (workflow), and skills and files (content); no domain nouns.
- **EXP-02 A new domain is expressible without kernel change**: **3** (grade A). Many domains ship as skill bundles on an unchanged kernel (skills/, optional-skills/), and the agent creates new domain skills itself. Scored at the lower reading under rule 11 because: If skills are judged too small to count as domains.
  - Higher reading 4: The September v0.3 pass scored 4 on the evidence above.
- **EXP-03 A domain ships as an installable bundle**: **3** (grade A). Skills are versionable, installable bundles under the agentskills.io specification, installed from the hub with scanning and synced on update.
  - Higher reading 4: Bundles are composable (curator umbrella skills), upgradeable and AI-assembled.

### Discover

- **EXP-04 Unmet-demand sensing**: **1** (grade A). Unserved requests stay in session history; nothing records them as unmet demand.
- **EXP-05 Evidence-backed opportunity proposals**: **1** (grade A). Background review creates skills for tasks it has just done; it does not propose capabilities nobody has used yet.
  - AI-qualified reading: **1** (grade A). Creates skills for tasks it has done; no unprompted proposals.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A). New skills apply to the whole installation at once.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A). Session search over full-text indexes, memory and skills injected into context, with memory provider plugins (hermes_state_fts.py, plugins).
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A), facets: implemented, tested. A single-user agent acting with the user's own permissions; the gateway accepts only paired users, profiles isolate homes, and dangerous commands need approval (tools/approval_smart.py), with security tests (tests/security).

### Quality

- **AIR-05 Offline AI evaluation**: **2** (grade A). Regression probes named after failures found in use (evals/) and GEPA skill evaluation in the companion repository, run on request.
- **AIR-06 Regression gating before release**: **1** (grade A). Evaluations are not part of CI.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A), facets: implemented, tested. Sessions record every message, tool call and model in the state database, with trajectories and trace upload (agent/trajectory.py, trace_upload.py, hermes_state_*.py), queryable through hermes sessions and insights.

### Operations

- **AIR-01 Model and provider portability and resilience**: **3** (grade A). Fallback providers and credential pools take over when a primary model fails, with tests (agent/agent_init.py, tests/agent/test_restore_primary_pool_reselect.py).
- **AIR-02 AI usage and per-customer cost controls**: **2** (grade A). Usage and pricing per turn and per account are tracked (agent/usage_pricing.py, turn_usage.py, billing_usage.py) and iterations are budgeted (agent/iteration_budget.py); no spend limit per user.
  - Higher reading 3: Iteration budgets bound usage per task.
- **AIR-08 Production quality, drift and feedback monitoring**: **1** (grade A). Skill usage counts feed the curator; no quality or feedback monitoring of the agent's answers.
