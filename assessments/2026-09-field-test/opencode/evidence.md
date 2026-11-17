# OpenCode evidence

Read at github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## Scope facts

- **persistent_data**: true. Sessions and messages in a local database (packages/opencode/src/storage).
- **schema_changes**: true. Drizzle migrations for the session database (packages/opencode/migration).
- **multi_tenant**: false. Re-checked under the v0.7 definition: a local tool for one developer; projects and worktrees belong to the same person, so they are not self-administering groups. The console and cloud functions are outside this scope.
- **hosted_service**: false. A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.
- **machine_actions**: true. The local server API and ACP let clients drive sessions and change files (packages/opencode/src/server, acp).
- **agent_mutations**: true. Changed to true for v0.7 (tightened definition: the product's AI writes to its own definitions, including drafts). `opencode agent create` has the model generate an agent definition (identifier, when to use, system prompt) and writes it to .opencode/agents or the global config (packages/opencode/src/agent/agent.ts:368-420, packages/opencode/src/cli/cmd/agent.ts:132-216), and the built-in /init command has the agent create or update AGENTS.md, the instruction file OpenCode loads into every session (packages/opencode/src/command/template/initialize.txt, command/index.ts:47). The September reading missed both.
- **evolution_auto_apply**: false. Re-checked for v0.7: no loop changes OpenCode's definitions on its own. Both AI paths above run only when a person invokes them, and the person chooses the generated agent's permissions and mode before it is written (packages/opencode/src/cli/cmd/agent.ts:140-200).
- **definition_change_path**: true. Agents, commands, themes and configuration files are its definitions.
- **code_release_path**: false. Re-checked under the v0.7 definition: no product path has OpenCode's AI write and activate plugins, tools or scripts for OpenCode itself; plugins and custom tools are loaded from files people place in .opencode or the global config. The team's GitHub agent on this repository is the product's general coding agent, not a first-party evolution system (rule 12; see ai_delivery).
- **ai_features**: true. The product is an LLM coding agent.
- **ai_data_access**: true. Reads the workspace through read, grep, glob and LSP tools.
- **ai_actions**: true. Edits files and runs shell commands (packages/opencode/src/tool).

## Kinds of change

- **Custom agents and commands** (`agents-commands`, main, made by the developer using OpenCode): reach **0 Engineers only**, confidence high. Markdown or JSON files in .opencode or the global config (packages/opencode/src/config/agent.ts, command.ts); `opencode agent create` drafts an agent with the model (cli/cmd/agent.ts). No supported undo: the files are versioned only by the user's own git (GOV-05 1), and the generator writes outside any session, so session revert does not cover it. Reach 0 because the path has no undo; the AI draft would otherwise read as reach 2, which DEL-04 1 would not support.
- **Standing instructions for a project (AGENTS.md)** (`project-instructions`, main, made by the developer using OpenCode): reach **1 Self-serve**, confidence medium. The built-in /init command has the agent create or update AGENTS.md (packages/opencode/src/command/template/initialize.txt), and people edit it in chat. Edits made in a session are snapshotted and the session can be reverted from the TUI or API (packages/opencode/src/session/revert.ts, snapshot/). Reach 1, not 2: the agent drafts the file, but DEL-04 is 1, so the criteria do not support reach 2.
- **Which models and providers it uses** (`models-providers`, main, made by the developer using OpenCode): reach **1 Self-serve**, confidence medium. Providers are added and removed with `opencode auth login` and `opencode providers logout` (packages/opencode/src/cli/cmd/providers.ts:492-501), and the model is chosen in the model picker, which keeps recent choices (packages/opencode/src/provider/provider.ts:2035). Undo is selecting the previous model or logging out. Defaults set by editing opencode.json have no product history. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
- **What the agent may do without asking** (`permissions`, not main, made by the developer using OpenCode): reach **0 Engineers only**, confidence high. Allow, ask and deny rules exist only in configuration files people edit by hand (packages/opencode/src/permission/index.ts:33-80); no in-product path or history. Reach 0.
- **Plugins, MCP servers and skills** (`plugins-mcp`, not main, made by the developer using OpenCode): reach **0 Engineers only**, confidence medium. Configured as entries and files in opencode.json and .opencode that people edit by hand (packages/plugin, mcp/, skill/discovery.ts); no in-product path or history. Reach 0.

## AI delivery and proof

- **AI delivery**: Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit. AGENTS.md and a .opencode folder (agents, commands, skills, plugins) for working on this repository; OpenCode's own agent runs in CI on issues and pull requests (.github/workflows/opencode.yml:29 pinned by SHA, review.yml:35 and triage.yml:41 install the latest release with curl).
- **Proven, Request → Release**: not evidenced. Searched: Repository at the pinned commit: no product records of requests becoming changes to OpenCode's own definitions; the loop is built at L0.
- **Proven, Issue → Fix**: not evidenced. Searched: Repository at the pinned commit: no incident or fix records from the product's own loop; built at L0.
- **Proven, Opportunity → Expansion**: not evidenced. Searched: Repository at the pinned commit: no records of capabilities proposed or launched by the product; built at L0.

Confidence for criteria this migration did not change was assigned at migration to v0.7 from the recorded evidence (high where it names the code path and its tests or exact lines, medium where it names files but not every path, low where it rests on an absence claim or general description); criteria re-read for v0.7 carry the confidence of that re-reading.

## Elastic (ARC)

### Data

- **ARC-01 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 1.
- **ARC-02 Safe schema and data migrations**: **1** (grade A, confidence medium). Drizzle migrations for the session database (packages/opencode/migration); no down steps.
  - Higher reading 2: Generated migrations with a migration table.

### Scale

- **ARC-03 Horizontal scale of services**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.
- **ARC-04 Reliable asynchronous work**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.
- **ARC-05 Tenant isolation and noisy-neighbour controls**: **not applicable**. Scope fact multi_tenant is false: A local single-user tool. If counted: 2.

### Capacity

- **ARC-06 Ceilings measured, not discovered in incidents**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope. If counted: 2.
- **ARC-07 Service objectives defined and monitored**: **not applicable**. Scope fact hosted_service is false: A local CLI and TUI with an optional local server; the console and cloud functions are separate products outside this scope.

### Resilience

- **ARC-08 Failure isolation and graceful degradation**: **2** (grade A, confidence medium). Provider calls are retried with back-off (packages/opencode/src/session/retry.ts); MCP servers and LSPs run as separate processes.
  - AI-qualified reading: **2** (grade A, confidence medium). Provider calls retried with back-off (packages/opencode/src/session/retry.ts).
- **ARC-09 Backup, restore and recovery**: **1** (grade A, confidence medium). Sessions can be exported and imported one at a time (packages/opencode/src/cli/cmd/export.ts, import.ts); configuration lives in files.

## Velocity (DEL)

### Intake

- **DEL-01 Request intake into a structured change specification**: **0** (grade A, confidence low). No request or feature-request object for changing the product was found; requests live outside it.
  - AI-qualified reading: **0** (grade A, confidence low). AI works on users' code, not on OpenCode's own changes.

### Build

- **DEL-02 Layers deploy independently**: **3** (grade A, confidence medium). Client and server architecture: server, TUI, desktop, web, console and cloud functions deploy separately (packages/server, packages/desktop, packages/function, .github/workflows/deploy.yml, containers.yml).
- **DEL-03 Module boundaries enforced by tooling**: **2** (grade A, confidence medium). Monorepo packages with explicit protocol and schema packages as contracts (packages/protocol, packages/schema); no architectural lint.
  - Higher reading 3: Explicit API contracts between modules.
- **DEL-04 AI implementation lane**: **1** (grade A, confidence medium). The team runs OpenCode's general GitHub agent on this repository for reviews and triage (.github/workflows/review.yml, triage.yml, opencode.yml). Under rubric rule 12 that is a team's use of a coding agent, not a first-party evolution system for OpenCode.
  - Higher reading 2: If the GitHub agent is read as part of the product's own evolution system, it is an AI lane for narrow tasks.
  - AI-qualified reading: **1** (grade A, confidence medium). The team's GitHub agent is not a first-party evolution system (rule 12).
    - Higher reading 2: Narrow AI lane.

### Verify

- **DEL-05 Every change class has an automated pre-land check**: **2** (grade A, confidence high). Tests and typecheck run on pull requests (.github/workflows/test.yml:7, typecheck.yml:6); no accessibility or security checks.
- **DEL-06 Verification surface**: **2** (grade A, confidence medium). Server health handler and machine-readable agent, command, provider and model handlers (packages/server/src/handlers/health.ts and others); no build or version endpoint verified.
  - Higher reading 3: The configuration handlers amount to a snapshot.
- **DEL-07 Environment reproducibility**: **2** (grade A, confidence medium). Nix flake and container definitions reproduce environments (nix/, .github/workflows/nix-eval.yml, containers.yml); no per-change ephemeral environment.
- **DEL-08 Machine verifiability**: **2** (grade A, confidence medium). Tests with recorded HTTP interactions for determinism (packages/http-recorder) and Storybook; no changed-path map or adoption instrumentation.
  - Higher reading 3: Recorded interactions make journeys deterministic.

### Release

- **DEL-09 Staged exposure**: **1** (grade A, confidence low). Releases go to all users; no staged exposure.
- **DEL-10 Kill switch**: **1** (grade A, confidence low). Features are switched in configuration files.
- **DEL-11 Release rollback**: **not applicable**. Scope fact code_release_path is false: The GitHub agent the team runs on this repository is the product's general coding agent, not a first-party evolution system for OpenCode (rubric rule 12).

## Open (MAL)

### Data model

- **MAL-01 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **MAL-02 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.
- **MAL-03 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 1.

### APIs

- **MAL-04 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-05 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **MAL-06 Machine-readable contract with introspection and dry-run**: **3** (grade A, confidence medium). The HTTP API is generated from a typed specification into a TypeScript SDK (packages/httpapi-codegen, packages/sdk/js, .github/workflows/generate.yml); no dry-run.

### Interface

- **MAL-07 Layout is data, tenant-overridable, validated, previewable**: **1** (grade A, confidence low). TUI, desktop and web layouts are code; keybinds are configuration.
- **MAL-08 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **MAL-09 Theme tokens and text are data with tenant overrides**: **2** (grade A, confidence medium). Themes are JSON files users can add and select in configuration (packages/opencode/src/config/config.ts); documentation is localised through a sync workflow (.github/workflows/docs-locale-sync.yml).

### Behaviour

- **MAL-10 Rules engine with declarative conditions and actions**: **2** (grade A, confidence medium). Custom commands and agents are markdown or JSON definitions (packages/opencode/src/config/command.ts, agent.ts); there is no condition and action engine.
- **MAL-11 Event model with webhooks or subscriptions and retry**: **2** (grade A, confidence medium). An internal event bus streams events to SDK clients over the server (packages/opencode/src/bus, packages/server/src/handlers/event.ts); no outbound webhooks with retry.
- **MAL-12 Sandboxed server-side hooks**: **2** (grade A, confidence medium). Plugins register hooks such as tool.definition, permission.ask, shell.env and command.execute.before (packages/plugin/src/index.ts) and run in-process without a sandbox.

### Extensions

- **MAL-13 Plugin lane breadth**: **3** (grade A, confidence medium). Plugins with hooks (packages/plugin), custom agents, commands, modes, themes, MCP servers, formatters, LSP servers and skills, both declarative and code.
- **MAL-14 Runtime isolation and dependency control**: **1** (grade A, confidence low). Plugins and local MCP servers run with full trust; permission rules limit agent tools, not plugin code.
  - Higher reading 2: Permission rules act as an allowlist on agent-written commands.
- **MAL-15 Developer loop**: **2** (grade A, confidence low). Plugins load from project directories on start and the SDK and server support local iteration; no validators or staged preview.
  - Higher reading 3: The developer loop is live against the real project.

### Integrations

- **MAL-16 Canonical data model with a mapping layer**: **3** (grade A, confidence medium). Providers map onto one model interface through a models catalogue snapshot (packages/opencode/src/provider, .github/workflows/models-snapshot.yml).
- **MAL-17 Connector definition or SDK**: **3** (grade A, confidence medium). Providers, MCP servers and LSP servers are configured by users with auth flows (packages/opencode/src/auth, mcp, lsp).
- **MAL-18 Stable versioned contracts**: **2** (grade A, confidence low). Versioned SDK and protocol packages; no deprecation windows.

### Agent interface

- **MAL-19 Machine-readable capability surface for agents**: **2** (grade A, confidence medium). Typed HTTP API, SDK and ACP support (packages/opencode/src/acp); OpenCode does not expose itself as an MCP server.
  - AI-qualified reading: **2** (grade A, confidence medium). HTTP API, SDK and ACP; no MCP server for agents.
- **MAL-20 Conversational operability for users and natural-language authoring for operators**: **2** (grade A, confidence medium). Users complete coding tasks conversationally with tool actions; agent definitions can be generated from a natural-language description (packages/opencode/src/agent/generate.txt). Scored at the lower reading under rule 11 because: Natural-language authoring covers agents only.
  - Higher reading 3: The September v0.3 pass scored 3 on the evidence above.
  - AI-qualified reading: **2** (grade A, confidence medium). Model-backed coding conversation; agents generated from descriptions.
    - Higher reading 3: Broad coverage.

## Learn (LRN)

### Sense

- **LRN-01 Telemetry accessible to the platform in near real time**: **2** (grade A, confidence medium). Sessions are stored locally and a stats package aggregates usage (packages/stats); no per-feature instrumentation consumed by the product.
  - Higher reading 3: The event bus is near-real-time to every client.
- **LRN-02 Structured learning signals**: **0** (grade A, confidence low). No feedback, rating or evaluation signals in the product.
- **LRN-03 User-issue detection**: **1** (grade A, confidence low). Logs for engineers.
- **LRN-04 Cross-source mining inside the product**: **1** (grade A, confidence low). Usage analysis happens outside the product.

### Diagnose and propose

- **LRN-05 Automated diagnosis**: **1** (grade A, confidence low). Engineers read logs.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.
- **LRN-06 Ranked, evidence-backed proposals for change**: **0** (grade A, confidence low). No proposals for changing OpenCode itself.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.

### Learn from experience

- **LRN-07 The product turns its own operating experience into candidate changes**: **1** (grade A, confidence medium). People write agents, commands and AGENTS.md by hand; nothing learns from sessions.
  - AI-qualified reading: **0** (grade A, confidence medium). No AI involvement in this behaviour.
- **LRN-08 Learned changes are validated before they take effect**: **1** (grade A, confidence high). Re-checked for v0.7 under the tightened boundary. The product's AI makes two kinds of change to its own definitions, both on request: a generated agent is constrained to a schema of three fields, written only as a new file (it refuses to overwrite an existing one) and given permissions the person selects (packages/opencode/src/agent/agent.ts:58-62, 405-415; cli/cmd/agent.ts:140-212); /init edits AGENTS.md with no check, and the person sees the diff and can revert the session (packages/opencode/src/session/revert.ts). No scan, lint or evaluation runs on either.
  - Higher reading 2: The schema on generated agents is an automated structural check on an AI-made change.
  - AI-qualified reading: **1** (grade A, confidence high). Generated agents are schema-constrained and never overwrite; /init's AGENTS.md edits get only the person's review (packages/opencode/src/agent/agent.ts:58-62; command/template/initialize.txt).
    - Higher reading 2: Schema-constrained generation.

### Measure

- **LRN-09 Post-change impact is measured against a declared baseline**: **0** (grade A, confidence low). No binding of changes to baselines or metrics.
- **LRN-10 The improvement loop improves itself**: **0** (grade A, confidence medium). Nothing governs change to OpenCode's own definitions beyond the generator's schema and the permission rules, which are code defaults plus user configuration (packages/opencode/src/agent/agent.ts:119-136, permission/evaluate.ts). There are no evaluation sets in the repository (AIR-05 1) and no record of failures against checks; the team's tests and CI workflows change only when engineers edit them.

## Vet (GOV)

### Compliance and security

- **GOV-01 Accessibility inherited from a component kit and continuously verified**: **1** (grade A, confidence medium). Storybook exists for UI components (packages/storybook); no automated accessibility scanning found.
- **GOV-02 Audit generic over entities, definition changes and approvals**: **1** (grade A, confidence low). Sessions and messages are stored locally; there is no audit store for configuration or permission decisions.
- **GOV-03 Privacy classification, export, erasure and retention generic over entities**: **2** (grade A, confidence medium). Local-first storage, session export and removal of shared sessions (packages/opencode/src/share); not driven by tags.
- **GOV-04 Security as infrastructure**: **2** (grade A, confidence high). Permission rules with allow, ask and deny actions by tool and pattern (packages/opencode/src/permission/index.ts:33-80, evaluate.ts) and managed enterprise configuration (config/managed.ts); no security scanning in CI.

### Change control

- **GOV-05 Definitions and layouts versioned with rollback**: **1** (grade A, confidence medium). Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions.
  - Higher reading 2: If the agent's work product counts as a customisation surface.
- **GOV-06 Proposal, review, apply as a first-class object with preview**: **1** (grade A, confidence low). No proposal object for changes to OpenCode's own definitions; its code changes go through pull requests.
- **GOV-07 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A, confidence medium). Permission rules decide per tool and pattern which agent actions run automatically and which ask a human (packages/opencode/src/permission/index.ts:33-80); the policy covers actions, not definition changes.
  - Higher reading 3: Read as a change-control policy, the allow, ask and deny rules are a policy object per change class.
- **GOV-08 Upgrade safety**: **2** (grade A, confidence medium). Configuration migrations and v2 compatibility (packages/opencode/src/config/tui-migrate.ts, v2-compat.ts); versioned protocol and schema packages (packages/protocol, packages/schema).
  - Higher reading 3: Migrations run automatically and contracts are explicit packages.

### AI and self-change safety

- **GOV-09 Agent-safe actions**: **2** (grade A, confidence low). Ask prompts preview tool actions under permission rules, and snapshots allow revert; commands run with the user's ambient authority and there are no idempotency keys.
  - AI-qualified reading: **2** (grade A, confidence low). Permission rules preview actions with ask prompts; commands run with the user's ambient authority.
- **GOV-10 Bounded self-change**: **2** (grade A, confidence high). Applies from v0.7 because agent_mutations is now true. The agent generator is bounded in code: the model returns only an identifier, when-to-use text and a system prompt; the person picks permissions and mode, and an existing agent file is never overwritten (packages/opencode/src/agent/agent.ts:58-62; cli/cmd/agent.ts:140-212). /init and the build agent edit AGENTS.md and project .opencode files under the default permission rules, which allow edits inside the project and ask only outside it (packages/opencode/src/agent/agent.ts:119-136); there is no rate, scope or blast-radius limit on those paths.
  - AI-qualified reading: **2** (grade A, confidence high). Generator output limited to three fields and new files in code; other AI edits to definitions bounded only by the general permission rules (packages/opencode/src/agent/agent.ts, cli/cmd/agent.ts).
- **GOV-11 Learning-input integrity**: **1** (grade A, confidence medium). Applies from v0.7 because agent_mutations is now true. /init reads repository files, including untrusted ones such as a cloned README, and writes AGENTS.md without provenance, fencing or injection scanning (packages/opencode/src/command/template/initialize.txt); the generated agent records no source. Inputs reach definitions only when a person runs one of these commands, never by themselves.
  - AI-qualified reading: **1** (grade A, confidence medium). No provenance or injection scanning on content that /init turns into AGENTS.md; nothing triggers a change without a person.

## Expand (EXP)

### Expressible

- **EXP-01 Kernel concepts are domain-neutral**: **3** (grade A, confidence low). Kernel of sessions (conversation), agents, tools, permissions, projects and providers, served through TUI, desktop, web, ACP, Slack and GitHub clients (channels).
- **EXP-02 A new domain is expressible without kernel change**: **2** (grade A, confidence low). New uses are expressible as agents, commands, MCP servers and skills without kernel change; no domain bundles ship in the repository.
  - Higher reading 3: Skill discovery installs remote skill bundles.
- **EXP-03 A domain ships as an installable bundle**: **2** (grade A, confidence high). Agents and commands are shareable files; skills are fetched with a recorded version (packages/opencode/src/skill/discovery.ts:105).

### Discover

- **EXP-04 Unmet-demand sensing**: **0** (grade A, confidence low). No record of unmet intents was found.
- **EXP-05 Evidence-backed opportunity proposals**: **0** (grade A, confidence low). No adjacent-capability proposals.
  - AI-qualified reading: **0** (grade A, confidence low). No AI involvement in this behaviour.

### Launch

- **EXP-06 Cohort launch with keep-or-kill**: **1** (grade A, confidence low). Plugins and agents apply to the whole installation.

## AI Readiness Checks (AIR)

### Context

- **AIR-03 AI-ready data and context access**: **3** (grade A, confidence medium). Read, grep, glob and LSP tools give live, attributed workspace context, plus AGENTS.md instructions.
- **AIR-04 Permission-preserving retrieval and tool access**: **3** (grade A, confidence high), facets: implemented, tested. A local agent acting with the user's permissions; permission rules allow, ask or deny each tool and pattern, enforced in code (packages/opencode/src/permission/evaluate.ts), with tests.

### Quality

- **AIR-05 Offline AI evaluation**: **1** (grade A, confidence low). No evaluation harness in the repository.
- **AIR-06 Regression gating before release**: **1** (grade A, confidence low). No evaluation gates in CI.

### Governance

- **AIR-07 AI action tracing and auditability**: **3** (grade A, confidence high), facets: implemented, tested. Sessions store every message, tool call, model and cost, and snapshots record file changes for revert (packages/opencode/src/session, snapshot).

### Operations

- **AIR-01 Model and provider portability and resilience**: **2** (grade A, confidence medium). Many providers through models.dev, with model choice per agent in configuration; retries with back-off (packages/opencode/src/session/retry.ts), no declared fallback.
- **AIR-02 AI usage and per-customer cost controls**: **2** (grade A, confidence medium). Tokens and cost per session are recorded and shown by opencode stats (packages/opencode/src/cli/cmd/stats.ts); no spend limit.
- **AIR-08 Production quality, drift and feedback monitoring**: **0** (grade A, confidence low). No feedback or quality monitoring.
