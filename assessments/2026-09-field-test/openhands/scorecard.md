# OpenHands (Agent Canvas + software-agent-sdk): MSR v0.3 scorecard

Evaluator: Claude, single rater. Framework: rubric v0.3.0 in this repository.

Scope: OpenHands/OpenHands (Agent Canvas front end) plus OpenHands/software-agent-sdk (SDK, agent server, tools, workspaces), because v0.3 requires assessing delegated capabilities where they live. OpenHands Cloud is out of scope.

## Reading

**With the SDK in scope:** webhooks with retries (D2 3), automated compatibility checks in CI (F4 3), and risk-classifying confirmation policies that are available but off by default (K3 2, 3 with ConfirmRisky). **Largest gap:** Learning (1.0). Critics refine task output, but nothing learns from sessions (P1 1).

## Limits

Repository evidence only, at the two tips named above. OpenHands Cloud is out of scope. Hook isolation was not verified. Single rater.

---
Framework 0.3.0. Date 2026-09-30. Source github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main). Archetype **agent-runtime**.

Coverage: 42 assessed, 0 not evidenced, 7 not applicable. Grades: 42 A, 0 B, 0 C.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings | Assessed only | If every criterion counted |
|---|---:|---|---|---:|---:|---:|
| malleability | 2.1 | mechanism | 2.1–2.4 | 2.1 | 2.1 | 1.6 |
| governance | 1.6 | mechanism | 1.6 | 1.6 | 1.6 | 1.6 |
| learning | 1.0 | code-only | 1.0 | 1.0 | 1.0 | 1.0 |
| factory | 2.2 | mechanism | 2.2–2.5 | 2.2 | 2.2 | 2.2 |

## Profiles

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | 2.1 | 2.1 |
| Governance | 1.6 | 1.6 |
| Learning | 1.0 | 1.0 |
| Factory | 2.2 | 2.2 |
| Agent Interface | 2.0 | 2.3 |
| Extension Surface | 2.0 | 2.0 |
| Operational Scalability | 1.0 | 1.0 |

## Closed loop

Closed-loop candidate: **no** by default, **no** with opt-in settings. This is a minimum-mechanism signal, not a production-readiness or outcome claim.

| Stage | Criteria | Needs | Default | With opt-in settings |
|---|---|---:|---:|---:|
| observe | J2 | 2 | 1 fail | 1 fail |
| propose | M1, P1 | 2 | 1 fail | 1 fail |
| review | F2 | 2 | 1 fail | 1 fail |
| gate | F3 | 3 | 2 fail | 2 fail |
| apply and roll back | F1 | 2 | 2 pass | 2 pass |
| measure | M4, P2 | 3 | 1 fail | 1 fail |
| verify | L1 | 2 | 2 pass | 2 pass |

## Dimension means

| Dimension | Default |
|---|---:|
| B API surface generation | 2.0 |
| C Rendering follows the definition | 2.0 |
| D Behaviour as data | 2.3 |
| E Compliance and security as infrastructure | 1.3 |
| F Change control | 2.0 |
| G Performance under genericity | 1.0 |
| H Stack flexibility and verification | 2.3 |
| I Extension ecosystem | 1.7 |
| J Observe | 1.3 |
| K Agent and conversational readiness | 2.0 |
| L Factory surfaces | 2.0 |
| M Advise and act | 0.7 |
| N Integration and connector extensibility | 2.3 |
| O Adjacent-domain expansion | 2.0 |
| P Learn from experience | 1.0 |

## Criteria

| Criterion | Status | Score | Alternate | Opt-in | Grade | Evidence, search scope or rationale |
|---|---|---:|---:|---:|---|---|
| A1 New entity type without code, DDL or deploy | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A2 Field definitions carry type and validation | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| A3 Relationships and lifecycle states declarable | not_applicable | excluded |  |  | - | Agent runtime: generic business-object criterion (fixed per-archetype rule). |
| B1 API per entity is generic or generated | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B2 API reshapes at runtime from definitions | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD criterion (fixed per-archetype rule). |
| B3 Machine-readable contract with introspection and dry-run | assessed | 2 |  |  | A | Typed client for the Agent Server API (src/api/open-hands.types.ts); the contract itself belongs to the Agent Server. |
| C1 Layout is data, tenant-overridable, validated, previewable | assessed | 2 | 3 |  | A | Canvas extensions are specified to contribute routed pages, panels, renderers, slots and themes as installable packages (specs/canvas-extensions.md), partly shipped behind capability detection; core layout is code. |
| C2 Generic list, detail and intake widgets from definition plus view spec | not_applicable | excluded |  |  | - | Agent runtime: generic CRUD views (fixed per-archetype rule). |
| C3 Theme tokens and text are data with tenant overrides | assessed | 2 |  |  | A | Colour themes are palette definitions covering interface, code and terminal (src/themes/README.md); eight locale files. |
| D1 Rules engine with declarative conditions and actions | assessed | 2 |  |  | A | Automations with cron and event triggers, templates and git sync are defined in the UI (src/types/automation.ts:3-13, src/routes/automation-*.tsx); they run on a separate automation server. |
| D2 Event model with webhooks or subscriptions and retry | assessed | 3 |  |  | A | The agent server posts events to configured webhooks with buffering and retries (openhands-agent-server/openhands/agent_server/config.py:73-104). |
| D3 Sandboxed server-side hooks | assessed | 2 | 3 |  | A | Hooks run at defined points (openhands-sdk/openhands/sdk/hooks); agent actions run in Docker, Apptainer, cloud or remote workspaces (openhands-workspace/openhands/workspace), but hook isolation and egress control were not verified. |
| E1 Accessibility inherited from a component kit and continuously verified | assessed | 2 | 1 |  | A | Component library with accessibility lint rules (eslint.config.js); no automated accessibility scans. |
| E2 Audit generic over entities, definition changes and approvals | assessed | 1 |  |  | A | No audit store in the canvas; durable audit is documented only through an external DefenseClaw integration (docs/DefenseClaw.md). |
| E3 Privacy classification, export, erasure and retention generic over entities | assessed | 1 | 2 |  | A | Telemetry is consent-gated with opt-out (src/services/telemetry.ts:9-29); there is no data export or erasure feature in the canvas. |
| E4 Security as infrastructure | assessed | 1 |  |  | A | No security scanning in CI; runtime security is delegated to the Agent Server or external guardrails (docs/DefenseClaw.md). |
| F1 Definitions and layouts versioned with rollback | assessed | 2 |  |  | A | Automation definitions sync to git (src/routes/automation-git-sync.tsx); other settings are unversioned. |
| F2 Proposal, review, apply as a first-class object with preview | assessed | 1 |  |  | A | No proposal object for changes. |
| F3 Policy-based apply with recorded approvals and a movable human boundary | assessed | 2 |  |  | A | Confirmation policies (never, always, confirm risky) decide which agent actions need a person (openhands-sdk/openhands/sdk/security/confirmation_policy.py:27-43); they govern actions, not changes to the agent itself. |
| F4 Upgrade safety | assessed | 3 |  |  | A | CI checks REST API breakage, persisted-settings compatibility and deprecations on every change (software-agent-sdk .github/workflows/agent-server-rest-api-breakage.yml, persisted-settings-compat.yml, deprecation-check.yml). |
| G1 Indexed query path, never a scan of a generic store | not_applicable | excluded |  |  | - | Agent runtime: generic-store query performance (fixed per-archetype rule). |
| G2 Tenant isolation and noisy-neighbour controls | assessed | 2 |  |  | A | Single user by default, with a Helm chart for team deployments (helm/agent-canvas). |
| G3 Ceilings measured, not discovered in incidents | assessed | 0 |  |  | A | No performance suite or documented limits (searched for benchmark, load test and perf). |
| H1 Layers deploy independently | assessed | 3 |  |  | A | The canvas deploys separately from the Agent Server and Automation Server behind an API contract, as an npm library, desktop app, container and Helm chart (docs/architecture.md, electron/, docker/, helm/). |
| H2 Module boundaries enforced by tooling | assessed | 2 |  |  | A | Library entrypoints and lint configuration; no architectural boundary tests. |
| H3 Every change class has an automated pre-land check | assessed | 2 | 3 |  | A | Lint, unit tests and builds on Ubuntu and Windows plus mocked-LLM Playwright E2E on pull requests (.github/workflows/ci.yml:4-66, mock-llm-e2e.yml); mutation testing (stryker.config.mjs); no accessibility or security checks. |
| I1 Plugin lane breadth | assessed | 2 | 3 |  | A | Skills, plugins and MCP servers are configured through the canvas (src/routes/skills-plugins.tsx, mcp-settings.tsx); canvas extensions for UI are partly shipped. |
| I2 Runtime isolation and dependency control | assessed | 1 |  |  | A | No isolation model for canvas extensions is evidenced; agent code isolation is delegated to backends. |
| I3 Developer loop | assessed | 2 |  |  | A | Mocked-LLM development server and seed scripts (scripts/seed-automation-ux-data.mjs, docs/DEVELOPMENT.md). |
| K1 Machine-readable capability surface for agents | assessed | 2 |  |  | A | The canvas consumes MCP and exposes a UI tool that lets agents drive the canvas (tools/canvas_ui_tool.py); no MCP server for the canvas itself. |
| K2 Conversational operability for users and natural-language authoring for operators | assessed | 2 |  |  | A | Users run agent conversations with actions through the canvas; there is no natural-language authoring of canvas definitions. |
| K3 Agent-safe actions | assessed | 2 |  | 3 | A | The default confirmation policy is NeverConfirm (openhands-sdk/openhands/sdk/conversation/state.py:123); with ConfirmRisky, LLM security analyzers classify each action's risk and risky ones pause for a person (security/llm_analyzer.py, toolshield_llm_analyzer.py, ensemble.py). |
| N1 Canonical data model with a mapping layer | assessed | 3 |  |  | A | OpenHands, Claude Code, Codex, Gemini and other ACP agents map onto one agent protocol, so adding an agent is configuration (docs/ACP_AGENTS.md). |
| N2 Connector definition or SDK | assessed | 2 | 3 |  | A | Backends (local, Docker, VM, cloud) and ACP agents are configurable; no connector SDK with lifecycle. |
| N3 Stable versioned contracts | assessed | 2 |  |  | A | Relies on the versioned Agent Server API and ACP; no deprecation windows in the canvas. |
| O1 Kernel concepts are domain-neutral | assessed | 2 | 3 |  | A | Kernel of conversations, backends, automations, profiles and skills with no business-domain nouns; channels exist only as automation outputs. |
| O2 A new domain is expressible without kernel change | assessed | 2 |  |  | A | Automation templates cover new tasks without kernel change (src/routes/automation-templates.tsx). |
| O3 A domain ships as an installable bundle | assessed | 2 |  |  | A | Automation templates and git sync; installable canvas extensions are partly shipped. |
| J1 Telemetry accessible to the platform in near real time | assessed | 2 |  |  | A | Consent-gated product analytics to PostHog (src/services/telemetry.ts); not available to product features. |
| J2 Structured learning signals | assessed | 1 |  |  | A | No typed feedback or learning signals in the canvas or the SDK. |
| J3 Cross-source mining inside the product | assessed | 1 |  |  | A | No joined mining in the canvas. |
| M1 Ranked, evidence-backed proposals for change | assessed | 0 |  |  | A | No proposals for changing the canvas. |
| M3 Accepted proposals are implemented by an AI authoring lane | assessed | 2 |  |  | A | Automations run coding agents on schedules and events for narrow tasks such as decomposing GitHub issues (README). |
| M4 Post-change impact is measured against a declared baseline | assessed | 0 |  |  | A | No binding of changes to baselines or metrics. |
| P1 The product turns its own operating experience into candidate changes | assessed | 1 |  |  | A | No learning from sessions was found in the SDK (searched openhands-sdk/openhands/sdk/skills, context, agent). |
| P2 Learned changes are validated before they take effect | assessed | 1 |  |  | A | Critics evaluate task output for iterative refinement (openhands-sdk/openhands/sdk/critic), not changes to the agent itself. |
| L1 Verification surface | assessed | 2 |  |  | A | Backend server_info with runtime services (docs/architecture.md) and container health in the entrypoint (docker/entrypoint.sh). |
| L2 Environment reproducibility | assessed | 2 |  |  | A | Docker, Helm and desktop builds; mocked-LLM Docker E2E stands up an environment per run (.github/workflows/mock-llm-docker-e2e.yml). |
| L3 Machine verifiability | assessed | 2 | 3 |  | A | Playwright journeys with mocked and live configurations and a testing matrix (docs/TESTING_MATRIX.md); no changed-path map or adoption instrumentation. |

