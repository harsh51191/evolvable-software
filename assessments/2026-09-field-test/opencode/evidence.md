# OpenCode evidence

Read at github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **A2 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B3 Machine-readable contract with introspection and dry-run**: **3** (grade A). The HTTP API is generated from a typed specification into a TypeScript SDK (packages/httpapi-codegen, packages/sdk/js, .github/workflows/generate.yml); no dry-run.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **1** (grade A). TUI, desktop and web layouts are code; keybinds are configuration.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). Themes are JSON files users can add and select in configuration (packages/opencode/src/config/config.ts); documentation is localised through a sync workflow (.github/workflows/docs-locale-sync.yml).
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A). Custom commands and agents are markdown or JSON definitions (packages/opencode/src/config/command.ts, agent.ts); there is no condition and action engine.
- **D2 Event model with webhooks or subscriptions and retry**: **2** (grade A). An internal event bus streams events to SDK clients over the server (packages/opencode/src/bus, packages/server/src/handlers/event.ts); no outbound webhooks with retry.
- **D3 Sandboxed server-side hooks**: **2** (grade A). Plugins register hooks such as tool.definition, permission.ask, shell.env and command.execute.before (packages/plugin/src/index.ts) and run in-process without a sandbox.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). Storybook exists for UI components (packages/storybook); no automated accessibility scanning found.
- **E2 Audit generic over entities, definition changes and approvals**: **1** (grade A). Sessions and messages are stored locally; there is no audit store for configuration or permission decisions.
- **E3 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Local-first storage, session export and removal of shared sessions (packages/opencode/src/share); not driven by tags.
- **E4 Security as infrastructure**: **2** (grade A). Permission rules with allow, ask and deny actions by tool and pattern (packages/opencode/src/permission/index.ts:33-80, evaluate.ts) and managed enterprise configuration (config/managed.ts); no security scanning in CI.
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **1** (grade A). Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions.
  - Alternate reading 2: If the agent's work product counts as a customisation surface.
- **F2 Proposal, review, apply as a first-class object with preview**: **1** (grade A). No proposal object for changes to OpenCode's own definitions; its code changes go through pull requests.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A). Permission rules decide per tool and pattern which agent actions run automatically and which ask a human (packages/opencode/src/permission/index.ts:33-80); the policy covers actions, not definition changes.
  - Alternate reading 3: Read as a change-control policy, the allow, ask and deny rules are a policy object per change class.
- **F4 Upgrade safety**: **2** (grade A). Configuration migrations and v2 compatibility (packages/opencode/src/config/tui-migrate.ts, v2-compat.ts); versioned protocol and schema packages (packages/protocol, packages/schema).
  - Alternate reading 3: Migrations run automatically and contracts are explicit packages.
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Single user per local installation; console and enterprise packages serve teams without evidenced noisy-neighbour controls.
- **G3 Ceilings measured, not discovered in incidents**: **2** (grade A). A performance test suite is documented (perf/test-suite.md); no per-surface limits or CI budgets.
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **3** (grade A). Client and server architecture: server, TUI, desktop, web, console and cloud functions deploy separately (packages/server, packages/desktop, packages/function, .github/workflows/deploy.yml, containers.yml).
- **H2 Module boundaries enforced by tooling**: **2** (grade A). Monorepo packages with explicit protocol and schema packages as contracts (packages/protocol, packages/schema); no architectural lint.
  - Alternate reading 3: Explicit API contracts between modules.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Tests and typecheck run on pull requests (.github/workflows/test.yml:7, typecheck.yml:6); no accessibility or security checks.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **3** (grade A). Plugins with hooks (packages/plugin), custom agents, commands, modes, themes, MCP servers, formatters, LSP servers and skills, both declarative and code.
- **I2 Runtime isolation and dependency control**: **1** (grade A). Plugins and local MCP servers run with full trust; permission rules limit agent tools, not plugin code.
  - Alternate reading 2: Permission rules act as an allowlist on agent-written commands.
- **I3 Developer loop**: **2** (grade A). Plugins load from project directories on start and the SDK and server support local iteration; no validators or staged preview.
  - Alternate reading 3: The developer loop is live against the real project.
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **2** (grade A). Typed HTTP API, SDK and ACP support (packages/opencode/src/acp); OpenCode does not expose itself as an MCP server.
- **K2 Conversational operability for users and natural-language authoring for operators**: **3** (grade A). Users complete coding tasks conversationally with tool actions; agent definitions can be generated from a natural-language description (packages/opencode/src/agent/generate.txt).
  - Alternate reading 2: Natural-language authoring covers agents only.
- **K3 Agent-safe actions**: **2** (grade A). Ask prompts preview tool actions under permission rules, and snapshots allow revert; commands run with the user's ambient authority and there are no idempotency keys.
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). Providers map onto one model interface through a models catalogue snapshot (packages/opencode/src/provider, .github/workflows/models-snapshot.yml).
- **N2 Connector definition or SDK**: **3** (grade A). Providers, MCP servers and LSP servers are configured by users with auth flows (packages/opencode/src/auth, mcp, lsp).
- **N3 Stable versioned contracts**: **2** (grade A). Versioned SDK and protocol packages; no deprecation windows.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of sessions (conversation), agents, tools, permissions, projects and providers, served through TUI, desktop, web, ACP, Slack and GitHub clients (channels).
- **O2 A new domain is expressible without kernel change**: **2** (grade A). New uses are expressible as agents, commands, MCP servers and skills without kernel change; no domain bundles ship in the repository.
  - Alternate reading 3: Skill discovery installs remote skill bundles.
- **O3 A domain ships as an installable bundle**: **2** (grade A). Agents and commands are shareable files; skills are fetched with a recorded version (packages/opencode/src/skill/discovery.ts:105).
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **2** (grade A). Sessions are stored locally and a stats package aggregates usage (packages/stats); no per-feature instrumentation consumed by the product.
  - Alternate reading 3: The event bus is near-real-time to every client.
- **J2 Structured learning signals**: **0** (grade A). No feedback, rating or evaluation signals in the product.
- **J3 Cross-source mining inside the product**: **1** (grade A). Usage analysis happens outside the product.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **0** (grade A). No proposals for changing OpenCode itself.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **2** (grade A). OpenCode reviews and triages its own repository's pull requests and issues through its GitHub action (.github/workflows/review.yml, triage.yml, opencode.yml): an AI lane for narrow tasks, run by engineers.
- **M4 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **1** (grade A). People write agents, commands and AGENTS.md by hand; nothing learns from sessions.
- **P2 Learned changes are validated before they take effect**: **1** (grade A). Changes to OpenCode's definitions are reviewed by people only.
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). Server health handler and machine-readable agent, command, provider and model handlers (packages/server/src/handlers/health.ts and others); no build or version endpoint verified.
  - Alternate reading 3: The configuration handlers amount to a snapshot.
- **L2 Environment reproducibility**: **2** (grade A). Nix flake and container definitions reproduce environments (nix/, .github/workflows/nix-eval.yml, containers.yml); no per-change ephemeral environment.
- **L3 Machine verifiability**: **2** (grade A). Tests with recorded HTTP interactions for determinism (packages/http-recorder) and Storybook; no changed-path map or adoption instrumentation.
  - Alternate reading 3: Recorded interactions make journeys deterministic.
