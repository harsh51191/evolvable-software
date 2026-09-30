# Hermes Agent: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the hermes-agent repository (agent loop, tools, skills, curator, approvals, gateway, MCP and ACP servers, desktop and web, CI) plus the first-party hermes-agent-self-evolution repository (DSPy and GEPA skill optimisation). Nous Portal and hosted services are out of scope.

## Reading

**Strongest:** Learning (2.5), the highest in the sample. Background review is on by default and turns conversations into skill and memory changes (P1 3). Every skill has usage signals and curator triage (J2 3). Every change is ledgered with rollback (F1 3). **Gaps by default:** skill and memory approval gates are off (F3 2), and learned skills get security and lint checks but no baseline evaluation (P2 2). **With opt-ins** (write approval on, the GEPA optimiser run), Hermes is the only system in the sample that passes every closed-loop stage.

## Limits

Repository evidence only. The self-evolution repository's last commit is 2026-06-17, and only phase 1 (skills) is implemented; phases 2 and 3 were not scored. No live runs were performed, so the effects of background review and the curator are read from code and documentation. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17). Archetype **agent-runtime**.

Coverage: 42 assessed, 0 not evidenced, 7 not applicable. Grades: 42 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.4 | mechanism | 2.4–2.5 | 2.4 | 2.4 | 2.0 |
| governance | 2.3 | mechanism | 2.3–2.5 | 2.5 | 2.3 | 2.3 |
| learning | 2.5 | productised | 2.5–2.9 | 2.7 | 2.5 | 2.5 |
| factory | 2.0 | mechanism | 2.0–2.3 | 2.0 | 2.0 | 2.0 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.2 | 2.2 |
| Governance | 2.3 | 2.5 |
| Learning | 2.5 | 2.7 |
| Factory | 2.0 | 2.0 |
| Agent Interface | 2.7 | 2.7 |
| Extension Surface | 2.7 | 2.7 |
| Operational Scalability | 1.5 | 1.5 |

## Closed loop

Closed-loop candidate: **no** by default, **yes** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 3 pass | 3 pass |
| propose | M1, P1 | 2 | 3 pass | 3 pass |
| review | F2 | 2 | 2 pass | 3 pass |
| gate | F3 | 3 | 2 fail | 3 pass |
| apply and roll back | F1 | 2 | 3 pass | 3 pass |
| measure | M4, P2 | 3 | 2 fail | 3 pass |
| verify | L1 | 2 | 2 pass | 2 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| B API surface generation | 2.0 |
| C Rendering follows the definition | 1.5 |
| D Behaviour as data | 2.0 |
| E Compliance and security as infrastructure | 2.0 |
| F Change control | 2.5 |
| G Performance under genericity | 1.5 |
| H Stack flexibility and verification | 2.0 |
| I Extension ecosystem | 2.7 |
| J Observe | 2.7 |
| K Agent and conversational readiness | 2.7 |
| L Factory surfaces | 2.0 |
| M Advise and act | 2.3 |
| N Integration and connector extensibility | 2.7 |
| O Adjacent-domain expansion | 3.3 |
| P Learn from experience | 2.5 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A2 Field definitions carry type and validation | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A | Typed tool schemas (model_tools.py, toolsets.py) served over MCP (mcp_serve.py) and the Agent Client Protocol (acp_adapter); no OpenAPI description of the serve API and no dry-run. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 1 |  |  | A | CLI, TUI, desktop and web layouts are code; persona text (SOUL.md) is data but is not layout. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A | UI strings externalised in locales/ and translated READMEs; themes are engineer-managed. |
| D1 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A | Cron jobs are defined in natural language or the CLI and run agent tasks on schedules (cron/); plugin hooks add behaviour; there is no general condition and action engine. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A | Gateway adapters receive platform and webhook events; the MCP server lets clients poll live events (mcp_serve.py); no retry or replay for outbound subscribers. |
| D3 Sandboxed server-side hooks | assessed | 2 |  |  | A | Plugins register hooks that run in-process without a sandbox (plugins/); the agent's own commands can run in Docker, SSH or remote sandbox backends with guards (tools/terminal_tool_backends.py, terminal_tool_guards.py). |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 1 |  |  | A | No automated accessibility scanning found for the TUI, desktop or web interfaces. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 2 | 3 |  | A | Every skill mutation by any actor is appended to a JSONL ledger with content-addressed before and after snapshots (tools/skill_ledger.py); staged approvals are recorded; sessions are stored in SQLite. Configuration and memory changes are not in the ledger. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A | Session export and import (hermes_state_portability.py) and user-editable memory files; data stays on the user's machine; not driven by tags. |
| E4 Security as infrastructure | assessed | 3 |  |  | A | Command scanning with tirith and dangerous-command approvals with an LLM risk classifier and floors (tools/approval_smart.py, approval_floors.py); skill security scans and AST audits before install or write (tools/skills_guard.py, skills_ast_audit.py); OSV and supply-chain scans in CI (.github/workflows/osv-scanner.yml, supply-chain-audit.yml). |
| F1 Definitions and layouts versioned with rollback | assessed | 3 | 4 |  | A | Skills, the agent's main customisation surface, have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py); curator archives are recoverable with hermes curator restore; a write blocked by the security scan restores the original automatically (tools/skill_manager_tool.py:353-461). |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 2 |  | 3 | A | By default, skill and memory writes apply directly and are ledgered. With skills.write_approval or memory.write_approval on, writes are staged with a gist and applied through /skills approve (tools/write_approval.py:73-189); the self-evolution repo proposes evaluated skill variants as pull requests. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 |  | 3 | A | By default only protected instruction files always need a human (cli-config.yaml.example:573-576); skill and memory gates default to off (hermes_cli/config_defaults.py:1320). With them on, each change class has its own gate. |
| F4 Upgrade safety | assessed | 3 |  |  | A | Numbered configuration migrations run on update (hermes_cli/config_migrations.py:379-397); bundled-skill sync updates shipped skills without overwriting user copies (tools/skills_sync*.py); skills follow the agentskills.io specification. |
| G1 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A | Single user per installation with isolated profiles (separate homes); no multi-tenant limits. |
| G3 Ceilings measured, not discovered in incidents | assessed | 1 |  |  | A | evals/ holds regression probes named after failures found in use (for example auxiliary_resource_exhausted.py, cron_error_diagnostics.py): ceilings are discovered in incidents. |
| H1 Layers deploy independently | assessed | 2 |  |  | A | Python agent, gateway, desktop, web and sandbox images are separate artifacts built from one repository (Dockerfile, .github/workflows/sandbox-image.yml, desktop-bundled-release.yml). |
| H2 Module boundaries enforced by tooling | assessed | 2 |  |  | A | Import guards in CI (.github/workflows/lazy-deps-guard.yml, case-collision-check.yml); no architectural boundary lint. |
| H3 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A | Python, JavaScript and Rust tests, lint, Nix, OSV, supply-chain, desktop E2E and install E2E run in CI with no draft filter (.github/workflows/tests.yml, js-tests.yml, rust-tests.yml, e2e-desktop.yml); no accessibility check. |
| I1 Plugin lane breadth | assessed | 3 | 4 |  | A | Declarative skills (SKILL.md), Python plugins with hooks, MCP servers, providers and a plugin catalogue with hundreds of entries (plugin-catalog/, skills/, optional-skills/, optional-mcps/). |
| I2 Runtime isolation and dependency control | assessed | 2 | 3 |  | A | Hub skills are scanned and installed only after confirmation (tools/skills_hub_install.py, skills_guard.py); plugins run with full trust; commands can be sent to sandbox backends. |
| I3 Developer loop | assessed | 3 |  |  | A | Skill linter (tools/skill_linter.py), curator dry-run (hermes curator run --dry-run), logs (hermes_logging.py) and local iteration against the user's own profile. |
| K1 Machine-readable capability surface for agents | assessed | 3 | 2 |  | A | MCP server exposing conversation, messaging, event and approval tools (mcp_serve.py) and an ACP adapter for editors (acp_adapter/); typed tool registry (model_tools.py). |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 4 |  | A | Users complete tasks conversationally across CLI, desktop and messaging platforms with tool actions; users author skills, memory and cron jobs in natural language, with staged approvals as preview when enabled; evaluation probes (evals/) and GEPA evaluation datasets. |
| K3 Agent-safe actions | assessed | 2 | 3 |  | A | Dangerous-command approvals with LLM risk classification and floors, tirith scanning, sandbox backends, subagent auto-deny and session audit; commands otherwise run with the user's ambient authority; no idempotency keys. |
| N1 Canonical data model with a mapping layer | assessed | 3 |  |  | A | One provider layer maps many model vendors onto a canonical chat interface (providers/, agent/*_adapter.py), and one gateway maps Telegram, Discord, Slack, WhatsApp and other platforms onto a canonical conversation model (gateway/). |
| N2 Connector definition or SDK | assessed | 3 |  |  | A | Plugin catalogue entries, provider adapters, platform adapters and MCP servers cover auth, messaging and lifecycle; skill hub sources include official, GitHub, ClawHub and skills.sh (tools/skills_hub_*.py). |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | Standard protocols (MCP, ACP, OpenAI-compatible APIs) and versioned configuration; no deprecation windows. |
| O1 Kernel concepts are domain-neutral | assessed | 3 |  |  | A | Kernel of sessions (conversation), gateway platforms (channel), profiles (identity), approvals (permission), cron and delegation (workflow), and skills and files (content); no domain nouns. |
| O2 A new domain is expressible without kernel change | assessed | 4 | 3 |  | A | Many domains ship as skill bundles on an unchanged kernel (skills/, optional-skills/), and the agent creates new domain skills itself. |
| O3 A domain ships as an installable bundle | assessed | 3 | 4 |  | A | Skills are versionable, installable bundles under the agentskills.io specification, installed from the hub with scanning and synced on update. |
| J1 Telemetry accessible to the platform in near real time | assessed | 3 | 4 |  | A | The session database with full-text search is available to the agent in real time (hermes_state_fts.py, hermes_state_search.py); every skill gets view, use and patch counts automatically (tools/skill_usage.py). |
| J2 Structured learning signals | assessed | 3 | 2 |  | A | Every skill has view, use and patch counts linked to it (tools/skill_usage.py), and the curator triages skills into active, stale and archived (website/docs/user-guide/features/curator.md). |
| J3 Cross-source mining inside the product | assessed | 2 | 3 |  | A | Session search over the agent's own history; the self-evolution repo builds evaluation datasets from Hermes, Claude Code and Copilot session histories (README, --eval-source sessiondb). No continuous mining in the product. |
| M1 Ranked, evidence-backed proposals for change | assessed | 2 | 3 |  | A | After each turn a background fork proposes skill and memory updates grounded in the conversation (agent/background_review.py); GEPA ranks skill variants on a Pareto front with evaluation evidence (self-evolution repo). Covers skills only. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 3 | 2 |  | A | The background review is an autonomous authoring lane that applies skill and memory changes every turn (agent/background_review.py); GEPA improvements reach every user through upstream pull requests. |
| M4 Post-change impact is measured against a declared baseline | assessed | 2 | 3 |  | A | The curator keeps, marks stale or archives skills from measured usage over fixed windows (14 and 30 days, website/docs/user-guide/features/curator.md); GEPA compares variants against the baseline skill before proposing. Nothing measures the outcome of an applied skill in use. |
| P1 The product turns its own operating experience into candidate changes | assessed | 3 | 4 |  | A | background_review is enabled by default (hermes_cli/config_defaults.py:814): after turns, a forked agent decides whether to save or update skills and memory (agent/background_review.py). |
| P2 Learned changes are validated before they take effect | assessed | 2 |  | 3 | A | Skill writes pass security scans, AST audits and a linter (tools/skills_guard.py, skills_ast_audit.py, skill_linter.py). The first-party GEPA optimiser evaluates variants against the baseline skill before proposing, when it is run (hermes-agent-self-evolution README). |
| L1 Verification surface | assessed | 2 |  |  | A | Version reporting and state health checks (hermes_state_health.py) and a configuration display; no machine-readable deployed-configuration endpoint. |
| L2 Environment reproducibility | assessed | 2 | 3 |  | A | Nix flake and lock files reproduce the environment (flake.nix, uv.lock); install E2E jobs build fresh environments per run. |
| L3 Machine verifiability | assessed | 2 |  |  | A | Behaviour probes (evals/), desktop and install E2E suites; no changed-path map or adoption instrumentation at ship. |

