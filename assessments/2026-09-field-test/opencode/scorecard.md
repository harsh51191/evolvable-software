# OpenCode: MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: the opencode monorepo (agent core, server and HTTP API, SDK and codegen, TUI, desktop, web, plugin SDK, console and enterprise packages, CI). opencode.ai hosted services and models.dev are out of scope.

## Reading

**Strongest:** generated API contracts and SDK (B3 3), a client and server architecture (H1 3), and broad extension (I1 3). **Largest gap:** Learning (0.9). By design, OpenCode improves the user's code, not itself: no learning signals, proposals or measurement. Both raters agreed on this under v0.2, and v0.3 does not change it.

## Limits

Repository evidence only, dev branch at the tip named above. Enterprise and console behaviour was not traced in depth. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev). Archetype **agent-runtime**.

Coverage: 42 assessed, 0 not evidenced, 7 not applicable. Grades: 42 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.3 | mechanism | 2.3–2.4 | 2.3 | 2.3 | 1.8 |
| governance | 1.5 | mechanism | 1.5–1.9 | 1.5 | 1.5 | 1.5 |
| learning | 0.9 | code-only | 0.9–1.0 | 0.9 | 0.9 | 0.9 |
| factory | 2.2 | mechanism | 2.2–2.7 | 2.2 | 2.2 | 2.2 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.2 | 2.2 |
| Governance | 1.5 | 1.5 |
| Learning | 0.9 | 0.9 |
| Factory | 2.2 | 2.2 |
| Agent Interface | 2.3 | 2.3 |
| Extension Surface | 2.3 | 2.3 |
| Operational Scalability | 2.0 | 2.0 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 0 fail | 0 fail |
| propose | M1, P1 | 2 | 1 fail | 1 fail |
| review | F2 | 2 | 1 fail | 1 fail |
| gate | F3 | 3 | 2 fail | 2 fail |
| apply and roll back | F1 | 2 | 1 fail | 1 fail |
| measure | M4, P2 | 3 | 1 fail | 1 fail |
| verify | L1 | 2 | 2 pass | 2 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| B API surface generation | 3.0 |
| C Rendering follows the definition | 1.5 |
| D Behaviour as data | 2.0 |
| E Compliance and security as infrastructure | 1.5 |
| F Change control | 1.5 |
| G Performance under genericity | 2.0 |
| H Stack flexibility and verification | 2.3 |
| I Extension ecosystem | 2.0 |
| J Observe | 1.0 |
| K Agent and conversational readiness | 2.3 |
| L Factory surfaces | 2.0 |
| M Advise and act | 0.7 |
| N Integration and connector extensibility | 2.7 |
| O Adjacent-domain expansion | 2.3 |
| P Learn from experience | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A2 Field definitions carry type and validation | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 3 |  |  | A | The HTTP API is generated from a typed specification into a TypeScript SDK (packages/httpapi-codegen, packages/sdk/js, .github/workflows/generate.yml); no dry-run. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 1 |  |  | A | TUI, desktop and web layouts are code; keybinds are configuration. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A | Themes are JSON files users can add and select in configuration (packages/opencode/src/config/config.ts); documentation is localised through a sync workflow (.github/workflows/docs-locale-sync.yml). |
| D1 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A | Custom commands and agents are markdown or JSON definitions (packages/opencode/src/config/command.ts, agent.ts); there is no condition and action engine. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 2 |  |  | A | An internal event bus streams events to SDK clients over the server (packages/opencode/src/bus, packages/server/src/handlers/event.ts); no outbound webhooks with retry. |
| D3 Sandboxed server-side hooks | assessed | 2 |  |  | A | Plugins register hooks such as tool.definition, permission.ask, shell.env and command.execute.before (packages/plugin/src/index.ts) and run in-process without a sandbox. |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 1 |  |  | A | Storybook exists for UI components (packages/storybook); no automated accessibility scanning found. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 1 |  |  | A | Sessions and messages are stored locally; there is no audit store for configuration or permission decisions. |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 2 |  |  | A | Local-first storage, session export and removal of shared sessions (packages/opencode/src/share); not driven by tags. |
| E4 Security as infrastructure | assessed | 2 |  |  | A | Permission rules with allow, ask and deny actions by tool and pattern (packages/opencode/src/permission/index.ts:33-80, evaluate.ts) and managed enterprise configuration (config/managed.ts); no security scanning in CI. |
| F1 Definitions and layouts versioned with rollback | assessed | 1 | 2 |  | A | Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 1 |  |  | A | No proposal object for changes to OpenCode's own definitions; its code changes go through pull requests. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 | 3 |  | A | Permission rules decide per tool and pattern which agent actions run automatically and which ask a human (packages/opencode/src/permission/index.ts:33-80); the policy covers actions, not definition changes. |
| F4 Upgrade safety | assessed | 2 | 3 |  | A | Configuration migrations and v2 compatibility (packages/opencode/src/config/tui-migrate.ts, v2-compat.ts); versioned protocol and schema packages (packages/protocol, packages/schema). |
| G1 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A | Single user per local installation; console and enterprise packages serve teams without evidenced noisy-neighbour controls. |
| G3 Ceilings measured, not discovered in incidents | assessed | 2 |  |  | A | A performance test suite is documented (perf/test-suite.md); no per-surface limits or CI budgets. |
| H1 Layers deploy independently | assessed | 3 |  |  | A | Client and server architecture: server, TUI, desktop, web, console and cloud functions deploy separately (packages/server, packages/desktop, packages/function, .github/workflows/deploy.yml, containers.yml). |
| H2 Module boundaries enforced by tooling | assessed | 2 | 3 |  | A | Monorepo packages with explicit protocol and schema packages as contracts (packages/protocol, packages/schema); no architectural lint. |
| H3 Every change class has an automated pre-land check | assessed | 2 |  |  | A | Tests and typecheck run on pull requests (.github/workflows/test.yml:7, typecheck.yml:6); no accessibility or security checks. |
| I1 Plugin lane breadth | assessed | 3 |  |  | A | Plugins with hooks (packages/plugin), custom agents, commands, modes, themes, MCP servers, formatters, LSP servers and skills, both declarative and code. |
| I2 Runtime isolation and dependency control | assessed | 1 | 2 |  | A | Plugins and local MCP servers run with full trust; permission rules limit agent tools, not plugin code. |
| I3 Developer loop | assessed | 2 | 3 |  | A | Plugins load from project directories on start and the SDK and server support local iteration; no validators or staged preview. |
| K1 Machine-readable capability surface for agents | assessed | 2 |  |  | A | Typed HTTP API, SDK and ACP support (packages/opencode/src/acp); OpenCode does not expose itself as an MCP server. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 3 | 2 |  | A | Users complete coding tasks conversationally with tool actions; agent definitions can be generated from a natural-language description (packages/opencode/src/agent/generate.txt). |
| K3 Agent-safe actions | assessed | 2 |  |  | A | Ask prompts preview tool actions under permission rules, and snapshots allow revert; commands run with the user's ambient authority and there are no idempotency keys. |
| N1 Canonical data model with a mapping layer | assessed | 3 |  |  | A | Providers map onto one model interface through a models catalogue snapshot (packages/opencode/src/provider, .github/workflows/models-snapshot.yml). |
| N2 Connector definition or SDK | assessed | 3 |  |  | A | Providers, MCP servers and LSP servers are configured by users with auth flows (packages/opencode/src/auth, mcp, lsp). |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | Versioned SDK and protocol packages; no deprecation windows. |
| O1 Kernel concepts are domain-neutral | assessed | 3 |  |  | A | Kernel of sessions (conversation), agents, tools, permissions, projects and providers, served through TUI, desktop, web, ACP, Slack and GitHub clients (channels). |
| O2 A new domain is expressible without kernel change | assessed | 2 | 3 |  | A | New uses are expressible as agents, commands, MCP servers and skills without kernel change; no domain bundles ship in the repository. |
| O3 A domain ships as an installable bundle | assessed | 2 |  |  | A | Agents and commands are shareable files; skills are fetched with a recorded version (packages/opencode/src/skill/discovery.ts:105). |
| J1 Telemetry accessible to the platform in near real time | assessed | 2 | 3 |  | A | Sessions are stored locally and a stats package aggregates usage (packages/stats); no per-feature instrumentation consumed by the product. |
| J2 Structured learning signals | assessed | 0 |  |  | A | No feedback, rating or evaluation signals in the product. |
| J3 Cross-source mining inside the product | assessed | 1 |  |  | A | Usage analysis happens outside the product. |
| M1 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A | No proposals for changing OpenCode itself. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 2 |  |  | A | OpenCode reviews and triages its own repository's pull requests and issues through its GitHub action (.github/workflows/review.yml, triage.yml, opencode.yml): an AI lane for narrow tasks, run by engineers. |
| M4 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A | No binding of changes to baselines or metrics. |
| P1 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A | People write agents, commands and AGENTS.md by hand; nothing learns from sessions. |
| P2 Learned changes are validated before they take effect | assessed | 1 |  |  | A | Changes to OpenCode's definitions are reviewed by people only. |
| L1 Verification surface | assessed | 2 | 3 |  | A | Server health handler and machine-readable agent, command, provider and model handlers (packages/server/src/handlers/health.ts and others); no build or version endpoint verified. |
| L2 Environment reproducibility | assessed | 2 |  |  | A | Nix flake and container definitions reproduce environments (nix/, .github/workflows/nix-eval.yml, containers.yml); no per-change ephemeral environment. |
| L3 Machine verifiability | assessed | 2 | 3 |  | A | Tests with recorded HTTP interactions for determinism (packages/http-recorder) and Storybook; no changed-path map or adoption instrumentation. |

