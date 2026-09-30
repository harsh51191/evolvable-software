# Hermes Agent evidence

Read at github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **A2 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B3 Machine-readable contract with introspection and dry-run**: **2** (grade A). Typed tool schemas (model_tools.py, toolsets.py) served over MCP (mcp_serve.py) and the Agent Client Protocol (acp_adapter); no OpenAPI description of the serve API and no dry-run.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **1** (grade A). CLI, TUI, desktop and web layouts are code; persona text (SOUL.md) is data but is not layout.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). UI strings externalised in locales/ and translated READMEs; themes are engineer-managed.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A). Cron jobs are defined in natural language or the CLI and run agent tasks on schedules (cron/); plugin hooks add behaviour; there is no general condition and action engine.
- **D2 Event model with webhooks or subscriptions and retry**: **2** (grade A). Gateway adapters receive platform and webhook events; the MCP server lets clients poll live events (mcp_serve.py); no retry or replay for outbound subscribers.
- **D3 Sandboxed server-side hooks**: **2** (grade A). Plugins register hooks that run in-process without a sandbox (plugins/); the agent's own commands can run in Docker, SSH or remote sandbox backends with guards (tools/terminal_tool_backends.py, terminal_tool_guards.py).
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). No automated accessibility scanning found for the TUI, desktop or web interfaces.
- **E2 Audit generic over entities, definition changes and approvals**: **2** (grade A). Every skill mutation by any actor is appended to a JSONL ledger with content-addressed before and after snapshots (tools/skill_ledger.py); staged approvals are recorded; sessions are stored in SQLite. Configuration and memory changes are not in the ledger.
  - Alternate reading 3: Skills are the main definition surface and are fully audited with approvals.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Session export and import (hermes_state_portability.py) and user-editable memory files; data stays on the user's machine; not driven by tags.
- **E4 Security as infrastructure**: **3** (grade A). Command scanning with tirith and dangerous-command approvals with an LLM risk classifier and floors (tools/approval_smart.py, approval_floors.py); skill security scans and AST audits before install or write (tools/skills_guard.py, skills_ast_audit.py); OSV and supply-chain scans in CI (.github/workflows/osv-scanner.yml, supply-chain-audit.yml).
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **3** (grade A). Skills, the agent's main customisation surface, have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py); curator archives are recoverable with hermes curator restore; a write blocked by the security scan restores the original automatically (tools/skill_manager_tool.py:353-461).
  - Alternate reading 4: Ledger entries are addressable and rollback is automatic on failed scans; links to evidence are partial.
- **F2 Proposal, review, apply as a first-class object with preview**: **2** (grade A), **3** with opt-in settings. By default, skill and memory writes apply directly and are ledgered. With skills.write_approval or memory.write_approval on, writes are staged with a gist and applied through /skills approve (tools/write_approval.py:73-189); the self-evolution repo proposes evaluated skill variants as pull requests.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A), **3** with opt-in settings. By default only protected instruction files always need a human (cli-config.yaml.example:573-576); skill and memory gates default to off (hermes_cli/config_defaults.py:1320). With them on, each change class has its own gate.
- **F4 Upgrade safety**: **3** (grade A). Numbered configuration migrations run on update (hermes_cli/config_migrations.py:379-397); bundled-skill sync updates shipped skills without overwriting user copies (tools/skills_sync*.py); skills follow the agentskills.io specification.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Single user per installation with isolated profiles (separate homes); no multi-tenant limits.
- **G3 Ceilings measured, not discovered in incidents**: **1** (grade A). evals/ holds regression probes named after failures found in use (for example auxiliary_resource_exhausted.py, cron_error_diagnostics.py): ceilings are discovered in incidents.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **2** (grade A). Python agent, gateway, desktop, web and sandbox images are separate artifacts built from one repository (Dockerfile, .github/workflows/sandbox-image.yml, desktop-bundled-release.yml).
- **H2 Module boundaries enforced by tooling**: **2** (grade A). Import guards in CI (.github/workflows/lazy-deps-guard.yml, case-collision-check.yml); no architectural boundary lint.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Python, JavaScript and Rust tests, lint, Nix, OSV, supply-chain, desktop E2E and install E2E run in CI with no draft filter (.github/workflows/tests.yml, js-tests.yml, rust-tests.yml, e2e-desktop.yml); no accessibility check.
  - Alternate reading 3: Every change class except accessibility is checked.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Declarative skills (SKILL.md), Python plugins with hooks, MCP servers, providers and a plugin catalogue with hundreds of entries (plugin-catalog/, skills/, optional-skills/, optional-mcps/).
  - Alternate reading 4: A versioned registry and hub exist.
- **I2 Runtime isolation and dependency control**: **2** (grade A). Hub skills are scanned and installed only after confirmation (tools/skills_hub_install.py, skills_guard.py); plugins run with full trust; commands can be sent to sandbox backends.
  - Alternate reading 3: Scanned skills plus sandboxed command backends isolate most third-party and AI-written code.
- **I3 Developer loop**: **3** (grade A). Skill linter (tools/skill_linter.py), curator dry-run (hermes curator run --dry-run), logs (hermes_logging.py) and local iteration against the user's own profile.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **3** (grade A). MCP server exposing conversation, messaging, event and approval tools (mcp_serve.py) and an ACP adapter for editors (acp_adapter/); typed tool registry (model_tools.py).
  - Alternate reading 2: The MCP surface covers messaging, not the full capability set.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). Users complete tasks conversationally across CLI, desktop and messaging platforms with tool actions; users author skills, memory and cron jobs in natural language, with staged approvals as preview when enabled; evaluation probes (evals/) and GEPA evaluation datasets.
  - Alternate reading 4: Almost every capability is reachable conversationally.
- **K3 Agent-safe actions**: **2** (grade A). Dangerous-command approvals with LLM risk classification and floors, tirith scanning, sandbox backends, subagent auto-deny and session audit; commands otherwise run with the user's ambient authority; no idempotency keys.
  - Alternate reading 3: Per-action risk classification and approval previews are level 3 and 4 features.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). One provider layer maps many model vendors onto a canonical chat interface (providers/, agent/*_adapter.py), and one gateway maps Telegram, Discord, Slack, WhatsApp and other platforms onto a canonical conversation model (gateway/).
- **N2 Connector definition or SDK**: **3** (grade A). Plugin catalogue entries, provider adapters, platform adapters and MCP servers cover auth, messaging and lifecycle; skill hub sources include official, GitHub, ClawHub and skills.sh (tools/skills_hub_*.py).
- **N3 Stable versioned contracts**: **2** (grade A). Standard protocols (MCP, ACP, OpenAI-compatible APIs) and versioned configuration; no deprecation windows.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of sessions (conversation), gateway platforms (channel), profiles (identity), approvals (permission), cron and delegation (workflow), and skills and files (content); no domain nouns.
- **O2 A new domain is expressible without kernel change**: **4** (grade A). Many domains ship as skill bundles on an unchanged kernel (skills/, optional-skills/), and the agent creates new domain skills itself.
  - Alternate reading 3: If skills are judged too small to count as domains.
- **O3 A domain ships as an installable bundle**: **3** (grade A). Skills are versionable, installable bundles under the agentskills.io specification, installed from the hub with scanning and synced on update.
  - Alternate reading 4: Bundles are composable (curator umbrella skills), upgradeable and AI-assembled.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **3** (grade A). The session database with full-text search is available to the agent in real time (hermes_state_fts.py, hermes_state_search.py); every skill gets view, use and patch counts automatically (tools/skill_usage.py).
  - Alternate reading 4: Per-definition instrumentation is added automatically for every skill.
- **J2 Structured learning signals**: **3** (grade A). Every skill has view, use and patch counts linked to it (tools/skill_usage.py), and the curator triages skills into active, stale and archived (website/docs/user-guide/features/curator.md).
  - Alternate reading 2: Usage counts are not versioned per skill revision.
- **J3 Cross-source mining inside the product**: **2** (grade A). Session search over the agent's own history; the self-evolution repo builds evaluation datasets from Hermes, Claude Code and Copilot session histories (README, --eval-source sessiondb). No continuous mining in the product.
  - Alternate reading 3: Cross-source session mining exists, offline.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **2** (grade A). After each turn a background fork proposes skill and memory updates grounded in the conversation (agent/background_review.py); GEPA ranks skill variants on a Pareto front with evaluation evidence (self-evolution repo). Covers skills only.
  - Alternate reading 3: Ranked, evidence-backed proposals with expected impact exist for the agent's main behaviour surface.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **3** (grade A). The background review is an autonomous authoring lane that applies skill and memory changes every turn (agent/background_review.py); GEPA improvements reach every user through upstream pull requests.
  - Alternate reading 2: The cross-user path depends on an offline companion tool.
- **M4 Post-change impact is measured against a declared baseline**: **2** (grade A). The curator keeps, marks stale or archives skills from measured usage over fixed windows (14 and 30 days, website/docs/user-guide/features/curator.md); GEPA compares variants against the baseline skill before proposing. Nothing measures the outcome of an applied skill in use.
  - Alternate reading 3: The curator records a metric, window and explicit keep or archive decision per skill.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **3** (grade A). background_review is enabled by default (hermes_cli/config_defaults.py:814): after turns, a forked agent decides whether to save or update skills and memory (agent/background_review.py).
  - Alternate reading 4: The curator's consolidation learns which skills stick, but only when enabled.
- **P2 Learned changes are validated before they take effect**: **2** (grade A), **3** with opt-in settings. Skill writes pass security scans, AST audits and a linter (tools/skills_guard.py, skills_ast_audit.py, skill_linter.py). The first-party GEPA optimiser evaluates variants against the baseline skill before proposing, when it is run (hermes-agent-self-evolution README).
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). Version reporting and state health checks (hermes_state_health.py) and a configuration display; no machine-readable deployed-configuration endpoint.
- **L2 Environment reproducibility**: **2** (grade A). Nix flake and lock files reproduce the environment (flake.nix, uv.lock); install E2E jobs build fresh environments per run.
  - Alternate reading 3: Reproducible environments are built per change in CI.
- **L3 Machine verifiability**: **2** (grade A). Behaviour probes (evals/), desktop and install E2E suites; no changed-path map or adoption instrumentation at ship.
