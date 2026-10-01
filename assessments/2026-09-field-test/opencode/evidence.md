# OpenCode evidence

Read at github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Sessions and messages in a local database (packages/opencode/src/storage).
- **schema_changes**: true. Drizzle migrations for the session database (packages/opencode/migration).
- **multi_tenant**: false. A local single-user tool.
- **hosted_service**: false. A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.
- **agent_mutations**: false. No product feature lets the agent change OpenCode's own agents, commands or configuration.
- **automatic_apply**: false. Nothing changes OpenCode's definitions automatically.
- **code_release_path**: false. The GitHub agent the team runs on this repository is the product's general coding agent, not a first-party evolution system for OpenCode (rubric rule 12).

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **ARC-02 Safe schema and data migrations**: **1** (grade A). Drizzle migrations for the session database (packages/opencode/migration); no down steps.
  - Higher reading 2: Generated migrations with a migration table.

### Scale

- **ARC-03 Horizontal scale of services**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.
- **ARC-04 Reliable asynchronous work**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **not applicable**. Scope fact multi_tenant is false: A local single-user tool. If counted: 2.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. If counted: 2.
- **ARC-07 Service objectives defined and monitored**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A). Provider calls are retried with back-off (packages/opencode/src/session/retry.ts); MCP servers and LSPs run as separate processes.
- **ARC-09 Backup, restore and recovery**: **1** (grade A). Sessions can be exported and imported one at a time (packages/opencode/src/cli/cmd/export.ts, import.ts); configuration lives in files.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A). No request or feature-request object for changing the product was found; requests live outside it.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A). Client and server architecture: server, TUI, desktop, web, console and cloud functions deploy separately (packages/server, packages/desktop, packages/function, .github/workflows/deploy.yml, containers.yml).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A). Monorepo packages with explicit protocol and schema packages as contracts (packages/protocol, packages/schema); no architectural lint.
  - Higher reading 3: Explicit API contracts between modules.
- **DEL-04 AI implementation lane**: **1** (grade A). The team runs OpenCode's general GitHub agent on this repository for reviews and triage (.github/workflows/review.yml, triage.yml, opencode.yml). Under rubric rule 12 that is a team's use of a coding agent, not a first-party evolution system for OpenCode.
  - Higher reading 2: If the GitHub agent is read as part of the product's own evolution system, it is an AI lane for narrow tasks.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A). Tests and typecheck run on pull requests (.github/workflows/test.yml:7, typecheck.yml:6); no accessibility or security checks.
- **DEL-06 Verification surface**: **2** (grade A). Server health handler and machine-readable agent, command, provider and model handlers (packages/server/src/handlers/health.ts and others); no build or version endpoint verified.
  - Higher reading 3: The configuration handlers amount to a snapshot.
- **DEL-07 Environment reproducibility**: **2** (grade A). Nix flake and container definitions reproduce environments (nix/, .github/workflows/nix-eval.yml, containers.yml); no per-change ephemeral environment.
- **DEL-08 Machine verifiability**: **2** (grade A). Tests with recorded HTTP interactions for determinism (packages/http-recorder) and Storybook; no changed-path map or adoption instrumentation.
  - Higher reading 3: Recorded interactions make journeys deterministic.

### Release

- **DEL-09 Staged exposure**: **1** (grade A). Releases go to all users; no staged exposure.
- **DEL-10 Kill switch**: **1** (grade A). Features are switched in configuration files.
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: The GitHub agent the team runs on this repository is the product's general coding agent, not a first-party evolution system for OpenCode (rubric rule 12).

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **3** (grade A). The HTTP API is generated from a typed specification into a TypeScript SDK (packages/httpapi-codegen, packages/sdk/js, .github/workflows/generate.yml); no dry-run.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **1** (grade A). TUI, desktop and web layouts are code; keybinds are configuration.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A). Themes are JSON files users can add and select in configuration (packages/opencode/src/config/config.ts); documentation is localised through a sync workflow (.github/workflows/docs-locale-sync.yml).

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A). Custom commands and agents are markdown or JSON definitions (packages/opencode/src/config/command.ts, agent.ts); there is no condition and action engine.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A). An internal event bus streams events to SDK clients over the server (packages/opencode/src/bus, packages/server/src/handlers/event.ts); no outbound webhooks with retry.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A). Plugins register hooks such as tool.definition, permission.ask, shell.env and command.execute.before (packages/plugin/src/index.ts) and run in-process without a sandbox.

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A). Plugins with hooks (packages/plugin), custom agents, commands, modes, themes, MCP servers, formatters, LSP servers and skills, both declarative and code.
- **MAL-14 Runtime isolation and dependency control**: **1** (grade A). Plugins and local MCP servers run with full trust; permission rules limit agent tools, not plugin code.
  - Higher reading 2: Permission rules act as an allowlist on agent-written commands.
- **MAL-15 Developer loop**: **2** (grade A). Plugins load from project directories on start and the SDK and server support local iteration; no validators or staged preview.
  - Higher reading 3: The developer loop is live against the real project.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A). Providers map onto one model interface through a models catalogue snapshot (packages/opencode/src/provider, .github/workflows/models-snapshot.yml).
- **MAL-17 Connector definition or SDK**: **3** (grade A). Providers, MCP servers and LSP servers are configured by users with auth flows (packages/opencode/src/auth, mcp, lsp).
- **MAL-18 Stable versioned contracts**: **2** (grade A). Versioned SDK and protocol packages; no deprecation windows.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A). Typed HTTP API, SDK and ACP support (packages/opencode/src/acp); OpenCode does not expose itself as an MCP server.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A). Users complete coding tasks conversationally with tool actions; agent definitions can be generated from a natural-language description (packages/opencode/src/agent/generate.txt). Scored at the lower reading under rule 11 because: Natural-language authoring covers agents only.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A). Sessions are stored locally and a stats package aggregates usage (packages/stats); no per-feature instrumentation consumed by the product.
  - Higher reading 3: The event bus is near-real-time to every client.
- **LRN-02 Structured learning signals**: **0** (grade A). No feedback, rating or evaluation signals in the product.
- **LRN-03 User-issue detection**: **1** (grade A). Logs for engineers.
- **LRN-04 Cross-source mining inside the product**: **1** (grade A). Usage analysis happens outside the product.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **1** (grade A). Engineers read logs.
- **LRN-06 Ranked, evidence-backed proposals for change**: **0** (grade A). No proposals for changing OpenCode itself.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A). People write agents, commands and AGENTS.md by hand; nothing learns from sessions.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A). Changes to OpenCode's definitions are reviewed by people only.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A). Storybook exists for UI components (packages/storybook); no automated accessibility scanning found.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **1** (grade A). Sessions and messages are stored locally; there is no audit store for configuration or permission decisions.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A). Local-first storage, session export and removal of shared sessions (packages/opencode/src/share); not driven by tags.
- **GOV-04 Security as infrastructure**: **2** (grade A). Permission rules with allow, ask and deny actions by tool and pattern (packages/opencode/src/permission/index.ts:33-80, evaluate.ts) and managed enterprise configuration (config/managed.ts); no security scanning in CI.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **1** (grade A). Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions.
  - Higher reading 2: If the agent's work product counts as a customisation surface.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **1** (grade A). No proposal object for changes to OpenCode's own definitions; its code changes go through pull requests.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A). Permission rules decide per tool and pattern which agent actions run automatically and which ask a human (packages/opencode/src/permission/index.ts:33-80); the policy covers actions, not definition changes.
  - Higher reading 3: Read as a change-control policy, the allow, ask and deny rules are a policy object per change class.
- **GOV-08 Upgrade safety**: **2** (grade A). Configuration migrations and v2 compatibility (packages/opencode/src/config/tui-migrate.ts, v2-compat.ts); versioned protocol and schema packages (packages/protocol, packages/schema).
  - Higher reading 3: Migrations run automatically and contracts are explicit packages.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A). Ask prompts preview tool actions under permission rules, and snapshots allow revert; commands run with the user's ambient authority and there are no idempotency keys.
- **GOV-10 Bounded self-change**: **not applicable**. No self-change path. If counted: 1.
- **GOV-11 Learning-input integrity**: **not applicable**. No self-change path. If counted: 1.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A). Kernel of sessions (conversation), agents, tools, permissions, projects and providers, served through TUI, desktop, web, ACP, Slack and GitHub clients (channels).
- **EXP-02 A new domain is expressible without kernel change**: **2** (grade A). New uses are expressible as agents, commands, MCP servers and skills without kernel change; no domain bundles ship in the repository.
  - Higher reading 3: Skill discovery installs remote skill bundles.
- **EXP-03 A domain ships as an installable bundle**: **2** (grade A). Agents and commands are shareable files; skills are fetched with a recorded version (packages/opencode/src/skill/discovery.ts:105).

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A). No adjacent-capability proposals.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A). Plugins and agents apply to the whole installation.
