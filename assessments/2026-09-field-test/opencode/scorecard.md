# OpenCode: EVOLVE v0.6 scorecard

Evaluator: Claude, single rater. Framework: EVOLVE 0.6.0 in this repository.

Scope: the opencode monorepo (agent core, server and HTTP API, SDK and codegen, TUI, desktop, web, plugin SDK, console and enterprise packages, CI). opencode.ai hosted services and models.dev are out of scope.

## Reading

**SAL 0.** OpenCode's own agents, commands and configuration are files versioned only by the user's git (GOV-05 1), so no loop has a rollback path at L1. The team's use of OpenCode's GitHub agent on its own repository is not a first-party evolution system under rule 12 (DEL-04 1). **Next level:** versioned, validated configuration with rollback, and a learning path for agents and commands.

## Limits

Repository evidence only, dev branch at the tip named above. Enterprise and console behaviour was not traced in depth. Single rater.

---
Framework EVOLVE 0.6.0. Date 2026-09-30. Source github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev). Archetype **agent-runtime**.

Scope facts true: persistent_data, schema_changes, machine_actions, definition_change_path, ai_features, ai_data_access, ai_actions. False: multi_tenant, hosted_service, agent_mutations, evolution_auto_apply, code_release_path.

Coverage: 59 assessed, 0 not evidenced, 15 not applicable. Grades: 59 A, 0 B, 0 C.

## Software Autonomy Level

**SAL 0 (Manual) · AI-driven 0 · Request → Release L0 (AI L0) · Issue → Fix L0 (AI L0) · Opportunity → Expansion L0 (AI L0)**

Progress toward the next level: Request → Release 1 of 2 conditions for L1; Issue → Fix 1 of 3 conditions for L1; Opportunity → Expansion 1 of 2 conditions for L1.

- With opt-in settings: SAL 0 (Manual) · AI-driven 0 · Request → Release L0 (AI L0) · Issue → Fix L0 (AI L0) · Opportunity → Expansion L0 (AI L0).
- With every alternate reading: SAL 0 (Manual) · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L0 (AI L0) · Opportunity → Expansion L1 (AI L0).

| Loop | Stages | Spine | Architecture | Governance | Level | AI-driven | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|---:|
| Request → Release | L1 | L0 | L2 | L2 | **L0** | L0 | L0 |
| Issue → Fix | L0 | L0 | L2 | L2 | **L0** | L0 | L0 |
| Opportunity → Expansion | L1 | L0 | L2 | L2 | **L0** | L0 | L0 |

### Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | 1 | fail |
| Release rollback | DEL-11 ≥ 3 | n/a | n/a |
| Safe migrations | ARC-02 ≥ 3 | 1 | fail |
| Tested backup and restore | ARC-09 ≥ 3 | 1 | fail |
| Tenant isolation | ARC-05 ≥ 3 | n/a | n/a |
| Security as infrastructure | GOV-04 ≥ 3 | 2 | fail |
| Bounded self-change | not applicable (agent_mutations and evolution_auto_apply false) | n/a | n/a |

### What blocks the next level

- **Request → Release to L1**: spine Roll back needs rollback ≥ 2 (has GOV-05 1)
- **Issue → Fix to L1**: spine Roll back needs rollback ≥ 2 (has GOV-05 1); stages Detect needs LRN-03 ≥ 2 (has 1)
- **Opportunity → Expansion to L1**: spine Roll back needs rollback ≥ 2 (has GOV-05 1)

### What AI drives

Each loop re-scored with its AI-performable stages read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level.

| Loop | Level | AI-driven | AI stage readings | What AI needs for its next level |
|---|---:|---:|---|---|
| Request → Release | L0 | L0 | DEL-01 0, DEL-04 1 | – |
| Issue → Fix | L0 | L0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 n/a | – |
| Opportunity → Expansion | L0 | L0 | EXP-05 0 | – |

### Sensitivity

- **Robust:** no single criterion falling one level lowers the headline.
- No single criterion rising one level lifts the headline.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---:|---:|---:|
| Elastic (ARC) | 1.3 | 1.3–1.8 | 1.3 | 1.3 | 1.6 |
| Velocity (DEL) | 1.3 | 1.3–1.5 | 1.3 | 1.3 | 1.3 |
| Open (MAL) | 2.2 | 2.2–2.4 | 2.2 | 2.2 | 1.8 |
| Learn (LRN) | 0.6 | 0.6–0.7 | 0.6 | 0.6 | 0.6 |
| Vet (GOV) | 1.7 | 1.7–1.9 | 1.7 | 1.7 | 1.4 |
| Expand (EXP) | 1.1 | 1.1–1.2 | 1.1 | 1.1 | 1.1 |

## Area means

| Area | Default |
|---|---:|
| ARC Data | 1.0 |
| ARC Resilience | 1.5 |
| DEL Intake | 0.0 |
| DEL Build | 2.0 |
| DEL Verify | 2.0 |
| DEL Release | 1.0 |
| MAL APIs | 3.0 |
| MAL Interface | 1.5 |
| MAL Behaviour | 2.0 |
| MAL Extensions | 2.0 |
| MAL Integrations | 2.7 |
| MAL Agent interface | 2.0 |
| LRN Sense | 1.0 |
| LRN Diagnose and propose | 0.5 |
| LRN Learn from experience | 1.0 |
| LRN Measure | 0.0 |
| GOV Compliance and security | 1.5 |
| GOV Change control | 1.5 |
| GOV AI and self-change safety | 2.0 |
| EXP Expressible | 2.3 |
| EXP Discover | 0.0 |
| EXP Launch | 1.0 |

## AI Readiness

How safely can the product run AI in production? Separate from SAL, which it never changes.

**AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 1 · not production-governed**

- With opt-in settings: AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 1 · not production-governed.
- With every alternate reading: AI Readiness L1 (Experimental) · Context 3 · Quality 1 · Governance 2 · Operations 1 · not production-governed.

| Dimension | Level | Contributors |
|---|---:|---|
| Context | 3 | AIR-03 3, AIR-04 3 |
| Quality | 1 | AIR-05 1, AIR-06 1 |
| Governance | 2 | AIR-07 3, GOV-09 (AI) 2 |
| Operations | 1 | AIR-01 2, AIR-02 2, AIR-08 0, ARC-08 (AI) 2 |

| AI gate | Needs | Observed | Status |
|---|---|---|---|
| Permission-preserving access | AIR-04 ≥ 3 | 3 | pass |
| Regression evaluation before release | AIR-06 ≥ 3 | 1 | fail |
| Traceability of consequential AI actions | AIR-07 ≥ 3 | 3 | pass |

### AI Capability Footprint

What the product's AI does. Descriptive levels per area, with no headline: it never changes AI Readiness or SAL.

| Area | Level | Readings |
|---|---:|---|
| Operate | 2 | MAL-19 2, MAL-20 2 |
| Build | 0 | DEL-01 0, DEL-04 1 |
| Diagnose and improve | 0 | LRN-05 0, LRN-06 0, LRN-07 0, LRN-08 n/a |
| Expand | 0 | EXP-05 0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Facets | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|---|
| ARC-01 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - |  | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| ARC-02 Safe schema and data migrations | assessed | 1 | 2 |  | A |  | Drizzle migrations for the session database (packages/opencode/migration); no down steps. |
| ARC-03 Horizontal scale of services | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. |
| ARC-04 Reliable asynchronous work | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. |
| ARC-05 Tenant isolation and noisy-neighbour controls | not_applicable | excluded |  |  | - |  | Scope fact multi_tenant is false: A local single-user tool. |
| ARC-06 Ceilings measured, not discovered in incidents | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. |
| ARC-07 Service objectives defined and monitored | not_applicable | excluded |  |  | - |  | Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. |
| ARC-08 Failure isolation and graceful degradation | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Provider calls are retried with back-off (packages/opencode/src/session/retry.ts); MCP servers and LSPs run as separate processes. |
| ARC-09 Backup, restore and recovery | assessed | 1 |  |  | A |  | Sessions can be exported and imported one at a time (packages/opencode/src/cli/cmd/export.ts, import.ts); configuration lives in files. |
| DEL-01 Request intake into a structured change specification | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No request or feature-request object for changing the product was found; requests live outside it. |
| DEL-02 Layers deploy independently | assessed | 3 |  |  | A |  | Client and server architecture: server, TUI, desktop, web, console and cloud functions deploy separately (packages/server, packages/desktop, packages/function, .github/workflows/deploy.yml, containers.yml). |
| DEL-03 Module boundaries enforced by tooling | assessed | 2 | 3 |  | A |  | Monorepo packages with explicit protocol and schema packages as contracts (packages/protocol, packages/schema); no architectural lint. |
| DEL-04 AI implementation lane | assessed | 1 | 2 |  | A |  | AI-qualified reading: 1. The team runs OpenCode's general GitHub agent on this repository for reviews and triage (.github/workflows/review.yml, triage.yml, opencode.yml). Under rubric rule 12 that is a team's use of a coding agent, not a first-party evolution system for OpenCode. |
| DEL-05 Every change class has an automated pre-land check | assessed | 2 |  |  | A |  | Tests and typecheck run on pull requests (.github/workflows/test.yml:7, typecheck.yml:6); no accessibility or security checks. |
| DEL-06 Verification surface | assessed | 2 | 3 |  | A |  | Server health handler and machine-readable agent, command, provider and model handlers (packages/server/src/handlers/health.ts and others); no build or version endpoint verified. |
| DEL-07 Environment reproducibility | assessed | 2 |  |  | A |  | Nix flake and container definitions reproduce environments (nix/, .github/workflows/nix-eval.yml, containers.yml); no per-change ephemeral environment. |
| DEL-08 Machine verifiability | assessed | 2 | 3 |  | A |  | Tests with recorded HTTP interactions for determinism (packages/http-recorder) and Storybook; no changed-path map or adoption instrumentation. |
| DEL-09 Staged exposure | assessed | 1 |  |  | A |  | Releases go to all users; no staged exposure. |
| DEL-10 Kill switch | assessed | 1 |  |  | A |  | Features are switched in configuration files. |
| DEL-11 Release rollback | not_applicable | excluded |  |  | - |  | Scope fact code_release_path is false: The GitHub agent the team runs on this repository is the product's general coding agent, not a first-party evolution system for OpenCode (rubric rule 12). |
| MAL-01 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-02 Field definitions carry type and validation | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-03 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - |  | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| MAL-04 API per entity is generic or generated | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-05 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| MAL-06 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A |  | The HTTP API is generated from a typed specification into a TypeScript SDK (packages/httpapi-codegen, packages/sdk/js, .github/workflows/generate.yml); no dry-run. |
| MAL-07 Layout is data, tenant-overridable, validated, previewable | assessed | 1 |  |  | A |  | TUI, desktop and web layouts are code; keybinds are configuration. |
| MAL-08 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - |  | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| MAL-09 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A |  | Themes are JSON files users can add and select in configuration (packages/opencode/src/config/config.ts); documentation is localised through a sync workflow (.github/workflows/docs-locale-sync.yml). |
| MAL-10 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A |  | Custom commands and agents are markdown or JSON definitions (packages/opencode/src/config/command.ts, agent.ts); there is no condition and action engine. |
| MAL-11 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A |  | An internal event bus streams events to SDK clients over the server (packages/opencode/src/bus, packages/server/src/handlers/event.ts); no outbound webhooks with retry. |
| MAL-12 Sandboxed server-side hooks | assessed | 2 |  |  | A |  | Plugins register hooks such as tool.definition, permission.ask, shell.env and command.execute.before (packages/plugin/src/index.ts) and run in-process without a sandbox. |
| MAL-13 Plugin lane breadth | assessed | 3 |  |  | A |  | Plugins with hooks (packages/plugin), custom agents, commands, modes, themes, MCP servers, formatters, LSP servers and skills, both declarative and code. |
| MAL-14 Runtime isolation and dependency control | assessed | 1 | 2 |  | A |  | Plugins and local MCP servers run with full trust; permission rules limit agent tools, not plugin code. |
| MAL-15 Developer loop | assessed | 2 | 3 |  | A |  | Plugins load from project directories on start and the SDK and server support local iteration; no validators or staged preview. |
| MAL-16 Canonical data model with a mapping layer | assessed | 3 |  |  | A |  | Providers map onto one model interface through a models catalogue snapshot (packages/opencode/src/provider, .github/workflows/models-snapshot.yml). |
| MAL-17 Connector definition or SDK | assessed | 3 |  |  | A |  | Providers, MCP servers and LSP servers are configured by users with auth flows (packages/opencode/src/auth, mcp, lsp). |
| MAL-18 Stable versioned contracts | assessed | 2 |  |  | A |  | Versioned SDK and protocol packages; no deprecation windows. |
| MAL-19 Machine-readable capability surface for agents | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Typed HTTP API, SDK and ACP support (packages/opencode/src/acp); OpenCode does not expose itself as an MCP server. |
| MAL-20 Conversational operability for users and natural-language authoring for operators | assessed | 2 | 3 |  | A |  | AI-qualified reading: 2. Users complete coding tasks conversationally with tool actions; agent definitions can be generated from a natural-language description (packages/opencode/src/agent/generate.txt). Scored at the lower reading under rule 11 because: Natural-language authoring covers agents only. |
| LRN-01 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A |  | Sessions are stored locally and a stats package aggregates usage (packages/stats); no per-feature instrumentation consumed by the product. |
| LRN-02 Structured learning signals | assessed | 0 |  |  | A |  | No feedback, rating or evaluation signals in the product. |
| LRN-03 User-issue detection | assessed | 1 |  |  | A |  | Logs for engineers. |
| LRN-04 Cross-source mining inside the product | assessed | 1 |  |  | A |  | Usage analysis happens outside the product. |
| LRN-05 Automated diagnosis | assessed | 1 |  |  | A |  | AI-qualified reading: 0. Engineers read logs. |
| LRN-06 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No proposals for changing OpenCode itself. |
| LRN-07 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A |  | AI-qualified reading: 0. People write agents, commands and AGENTS.md by hand; nothing learns from sessions. |
| LRN-08 Learned changes are validated before they take effect | assessed | 1 |  |  | A |  | AI-qualified reading: not applicable. Changes to OpenCode's definitions are reviewed by people only. |
| LRN-09 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A |  | No binding of changes to baselines or metrics. |
| GOV-01 Accessibility inherited from a component kit and continuously verified | assessed | 1 |  |  | A |  | Storybook exists for UI components (packages/storybook); no automated accessibility scanning found. |
| GOV-02 Audit generic over entities, definition changes and approvals | assessed | 1 |  |  | A |  | Sessions and messages are stored locally; there is no audit store for configuration or permission decisions. |
| GOV-03 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A |  | Local-first storage, session export and removal of shared sessions (packages/opencode/src/share); not driven by tags. |
| GOV-04 Security as infrastructure | assessed | 2 |  |  | A |  | Permission rules with allow, ask and deny actions by tool and pattern (packages/opencode/src/permission/index.ts:33-80, evaluate.ts) and managed enterprise configuration (config/managed.ts); no security scanning in CI. |
| GOV-05 Definitions and layouts versioned with rollback | assessed | 1 | 2 |  | A |  | Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions. |
| GOV-06 Proposal, review, apply as a first-class object with preview | assessed | 1 |  |  | A |  | No proposal object for changes to OpenCode's own definitions; its code changes go through pull requests. |
| GOV-07 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 | 3 |  | A |  | Permission rules decide per tool and pattern which agent actions run automatically and which ask a human (packages/opencode/src/permission/index.ts:33-80); the policy covers actions, not definition changes. |
| GOV-08 Upgrade safety | assessed | 2 | 3 |  | A |  | Configuration migrations and v2 compatibility (packages/opencode/src/config/tui-migrate.ts, v2-compat.ts); versioned protocol and schema packages (packages/protocol, packages/schema). |
| GOV-09 Agent-safe actions | assessed | 2 |  |  | A |  | AI-qualified reading: 2. Ask prompts preview tool actions under permission rules, and snapshots allow revert; commands run with the user's ambient authority and there are no idempotency keys. |
| GOV-10 Bounded self-change | not_applicable | excluded |  |  | - |  | AI-qualified reading: not applicable. No self-change path. |
| GOV-11 Learning-input integrity | not_applicable | excluded |  |  | - |  | AI-qualified reading: not applicable. No self-change path. |
| EXP-01 Kernel concepts are domain-neutral | assessed | 3 |  |  | A |  | Kernel of sessions (conversation), agents, tools, permissions, projects and providers, served through TUI, desktop, web, ACP, Slack and GitHub clients (channels). |
| EXP-02 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A |  | New uses are expressible as agents, commands, MCP servers and skills without kernel change; no domain bundles ship in the repository. |
| EXP-03 A domain ships as an installable bundle | assessed | 2 |  |  | A |  | Agents and commands are shareable files; skills are fetched with a recorded version (packages/opencode/src/skill/discovery.ts:105). |
| EXP-04 Unmet-demand sensing | assessed | 0 |  |  | A |  | No record of unmet intents was found. |
| EXP-05 Evidence-backed opportunity proposals | assessed | 0 |  |  | A |  | AI-qualified reading: 0. No adjacent-capability proposals. |
| EXP-06 Cohort launch with keep-or-kill | assessed | 1 |  |  | A |  | Plugins and agents apply to the whole installation. |
| AIR-03 AI-ready data and context access | assessed | 3 |  |  | A |  | Read, grep, glob and LSP tools give live, attributed workspace context, plus AGENTS.md instructions. |
| AIR-04 Permission-preserving retrieval and tool access | assessed | 3 |  |  | A | IT | A local agent acting with the user's permissions; permission rules allow, ask or deny each tool and pattern, enforced in code (packages/opencode/src/permission/evaluate.ts), with tests. |
| AIR-05 Offline AI evaluation | assessed | 1 |  |  | A |  | No evaluation harness in the repository. |
| AIR-06 Regression gating before release | assessed | 1 |  |  | A |  | No evaluation gates in CI. |
| AIR-07 AI action tracing and auditability | assessed | 3 |  |  | A | IT | Sessions store every message, tool call, model and cost, and snapshots record file changes for revert (packages/opencode/src/session, snapshot). |
| AIR-01 Model and provider portability and resilience | assessed | 2 |  |  | A |  | Many providers through models.dev, with model choice per agent in configuration; retries with back-off (packages/opencode/src/session/retry.ts), no declared fallback. |
| AIR-02 AI usage and per-customer cost controls | assessed | 2 |  |  | A |  | Tokens and cost per session are recorded and shown by opencode stats (packages/opencode/src/cli/cmd/stats.ts); no spend limit. |
| AIR-08 Production quality, drift and feedback monitoring | assessed | 0 |  |  | A |  | No feedback or quality monitoring. |

Facets: I implemented, T tested, O operated.
