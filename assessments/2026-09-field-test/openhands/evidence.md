# OpenHands (Agent Canvas + software-agent-sdk) evidence

Read at github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) on 2026-09-30. Grade A is code at the tip, B is in-repository documentation.

## A Entity and schema as data

- **A1 New entity type without code, DDL or deploy**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **A2 Field definitions carry type and validation**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
- **A3 Relationships and lifecycle states declarable**: **not applicable**. Agent runtime: generic business-object criterion (fixed per-archetype rule). If counted: 0.
## B API surface generation

- **B1 API per entity is generic or generated**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B2 API reshapes at runtime from definitions**: **not applicable**. Agent runtime: generic CRUD criterion (fixed per-archetype rule). If counted: 1.
- **B3 Machine-readable contract with introspection and dry-run**: **2** (grade A). Typed client for the Agent Server API (src/api/open-hands.types.ts); the contract itself belongs to the Agent Server.
## C Rendering follows the definition

- **C1 Layout is data, tenant-overridable, validated, previewable**: **2** (grade A). Canvas extensions are specified to contribute routed pages, panels, renderers, slots and themes as installable packages (specs/canvas-extensions.md), partly shipped behind capability detection; core layout is code.
  - Alternate reading 3: Once shipped, extensions are validated, installable layout data.
- **C2 Generic list, detail and intake widgets from definition plus view spec**: **not applicable**. Agent runtime: generic CRUD views (fixed per-archetype rule). If counted: 1.
- **C3 Theme tokens and text are data with tenant overrides**: **2** (grade A). Colour themes are palette definitions covering interface, code and terminal (src/themes/README.md); eight locale files.
## D Behaviour as data

- **D1 Rules engine with declarative conditions and actions**: **2** (grade A). Automations with cron and event triggers, templates and git sync are defined in the UI (src/types/automation.ts:3-13, src/routes/automation-*.tsx); they run on a separate automation server.
- **D2 Event model with webhooks or subscriptions and retry**: **3** (grade A). The agent server posts events to configured webhooks with buffering and retries (openhands-agent-server/openhands/agent_server/config.py:73-104).
- **D3 Sandboxed server-side hooks**: **2** (grade A). Hooks run at defined points (openhands-sdk/openhands/sdk/hooks); agent actions run in Docker, Apptainer, cloud or remote workspaces (openhands-workspace/openhands/workspace), but hook isolation and egress control were not verified.
  - Alternate reading 3: If hooks execute inside the sandboxed workspace.
## E Compliance and security as infrastructure

- **E1 Accessibility inherited from a component kit and continuously verified**: **2** (grade A). Component library with accessibility lint rules (eslint.config.js); no automated accessibility scans.
  - Alternate reading 1: If lint rules without scans count as no automation.
- **E2 Audit generic over entities, definition changes and approvals**: **1** (grade A). No audit store in the canvas; durable audit is documented only through an external DefenseClaw integration (docs/DefenseClaw.md).
- **E3 Privacy classification, export, erasure and retention generic over entities**: **1** (grade A). Telemetry is consent-gated with opt-out (src/services/telemetry.ts:9-29); there is no data export or erasure feature in the canvas.
  - Alternate reading 2: Consent management is a privacy control, though not export or erasure.
- **E4 Security as infrastructure**: **1** (grade A). No security scanning in CI; runtime security is delegated to the Agent Server or external guardrails (docs/DefenseClaw.md).
## F Change control

- **F1 Definitions and layouts versioned with rollback**: **2** (grade A). Automation definitions sync to git (src/routes/automation-git-sync.tsx); other settings are unversioned.
- **F2 Proposal, review, apply as a first-class object with preview**: **1** (grade A). No proposal object for changes.
- **F3 Policy-based apply with recorded approvals and a movable human boundary**: **2** (grade A). Confirmation policies (never, always, confirm risky) decide which agent actions need a person (openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43); they govern actions, not changes to the agent itself.
- **F4 Upgrade safety**: **3** (grade A). CI checks REST API breakage, persisted-settings compatibility and deprecations on every change (software-agent-sdk .github/workflows/agent-server-rest-api-breakage.yml, persisted-settings-compat.yml, deprecation-check.yml).
## G Performance under genericity

- **G1 Indexed query path, never a scan of a generic store**: **not applicable**. Agent runtime: generic-store query performance (fixed per-archetype rule). If counted: 0.
- **G2 Tenant isolation and noisy-neighbour controls**: **2** (grade A). Single user by default, with a Helm chart for team deployments (helm/agent-canvas).
- **G3 Ceilings measured, not discovered in incidents**: **0** (grade A). No performance suite or documented limits (searched for benchmark, load test and perf).
## H Stack flexibility and verification

- **H1 Layers deploy independently**: **3** (grade A). The canvas deploys separately from the Agent Server and Automation Server behind an API contract, as an npm library, desktop app, container and Helm chart (docs/architecture.md, electron/, docker/, helm/).
- **H2 Module boundaries enforced by tooling**: **2** (grade A). Library entrypoints and lint configuration; no architectural boundary tests.
- **H3 Every change class has an automated pre-land check**: **2** (grade A). Lint, unit tests and builds on Ubuntu and Windows plus mocked-LLM Playwright E2E on pull requests (.github/workflows/ci.yml:4-66, mock-llm-e2e.yml); mutation testing (stryker.config.mjs); no accessibility or security checks.
  - Alternate reading 3: Coverage is broad, including mutation testing.
## I Extension ecosystem

- **I1 Plugin lane breadth**: **2** (grade A). Skills, plugins and MCP servers are configured through the canvas (src/routes/skills-plugins.tsx, mcp-settings.tsx); canvas extensions for UI are partly shipped.
  - Alternate reading 3: Once extensions ship, UI, layout and theme are all plugin points.
- **I2 Runtime isolation and dependency control**: **1** (grade A). No isolation model for canvas extensions is evidenced; agent code isolation is delegated to backends.
- **I3 Developer loop**: **2** (grade A). Mocked-LLM development server and seed scripts (scripts/seed-automation-ux-data.mjs, docs/DEVELOPMENT.md).
## K Agent and conversational readiness

- **K1 Machine-readable capability surface for agents**: **2** (grade A). The canvas consumes MCP and exposes a UI tool that lets agents drive the canvas (tools/canvas_ui_tool.py); no MCP server for the canvas itself.
- **K2 Conversational operability for users and natural-language authoring for operators**: **2** (grade A). Users run agent conversations with actions through the canvas; there is no natural-language authoring of canvas definitions.
- **K3 Agent-safe actions**: **2** (grade A), **3** with opt-in settings. The default confirmation policy is NeverConfirm (openhands-sdk/openhands/sdk/conversation/state.py:123); with ConfirmRisky, LLM security analyzers classify each action's risk and risky ones pause for a person (security/llm_analyzer.py, toolshield_llm_analyzer.py, ensemble.py).
## N Integration and connector extensibility

- **N1 Canonical data model with a mapping layer**: **3** (grade A). OpenHands, Claude Code, Codex, Gemini and other ACP agents map onto one agent protocol, so adding an agent is configuration (docs/ACP_AGENTS.md).
- **N2 Connector definition or SDK**: **2** (grade A). Backends (local, Docker, VM, cloud) and ACP agents are configurable; no connector SDK with lifecycle.
  - Alternate reading 3: ACP is a standard connector definition.
- **N3 Stable versioned contracts**: **2** (grade A). Relies on the versioned Agent Server API and ACP; no deprecation windows in the canvas.
## O Adjacent-domain expansion

- **O1 Kernel concepts are domain-neutral**: **2** (grade A). Kernel of conversations, backends, automations, profiles and skills with no business-domain nouns; channels exist only as automation outputs.
  - Alternate reading 3: Domain-neutral coding-agent console.
- **O2 A new domain is expressible without kernel change**: **2** (grade A). Automation templates cover new tasks without kernel change (src/routes/automation-templates.tsx).
- **O3 A domain ships as an installable bundle**: **2** (grade A). Automation templates and git sync; installable canvas extensions are partly shipped.
## J Observe

- **J1 Telemetry accessible to the platform in near real time**: **2** (grade A). Consent-gated product analytics to PostHog (src/services/telemetry.ts); not available to product features.
- **J2 Structured learning signals**: **1** (grade A). No typed feedback or learning signals in the canvas or the SDK.
- **J3 Cross-source mining inside the product**: **1** (grade A). No joined mining in the canvas.
## M Advise and act

- **M1 Ranked, evidence-backed proposals for change**: **0** (grade A). No proposals for changing the canvas.
- **M3 Accepted proposals are implemented by an AI authoring lane**: **2** (grade A). Automations run coding agents on schedules and events for narrow tasks such as decomposing GitHub issues (README).
- **M4 Post-change impact is measured against a declared baseline**: **0** (grade A). No binding of changes to baselines or metrics.
## P Learn from experience

- **P1 The product turns its own operating experience into candidate changes**: **1** (grade A). No learning from sessions was found in the SDK (searched openhands-sdk/openhands/sdk/skills, context, agent).
- **P2 Learned changes are validated before they take effect**: **1** (grade A). Critics evaluate task output for iterative refinement (openhands-sdk/openhands/sdk/critic), not changes to the agent itself.
## L Factory surfaces

- **L1 Verification surface**: **2** (grade A). Backend server_info with runtime services (docs/architecture.md) and container health in the entrypoint (docker/entrypoint.sh).
- **L2 Environment reproducibility**: **2** (grade A). Docker, Helm and desktop builds; mocked-LLM Docker E2E stands up an environment per run (.github/workflows/mock-llm-docker-e2e.yml).
- **L3 Machine verifiability**: **2** (grade A). Playwright journeys with mocked and live configurations and a testing matrix (docs/TESTING_MATRIX.md); no changed-path map or adoption instrumentation.
  - Alternate reading 3: The testing matrix maps surfaces to journeys.
