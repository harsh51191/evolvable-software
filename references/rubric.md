# MSR Rubric: criterion definitions and anchored levels

This file is the single source of truth for the Malleability and Self-Evolution Readiness framework. `scripts/score.py` reads the criterion ids and dimension membership from the `###` headings below. Edit here, nowhere else.

Every criterion has: a definition, why it matters, evidence to look for, and one anchored description per level 0 to 4. Score the level whose description the evidence supports in full. If the evidence sits between two levels, take the lower one.

## General maturity ladder

| Level | Meaning |
|---|---|
| 0 | Absent. |
| 1 | Code-only. Engineers change code and ship a release. |
| 2 | Mechanism. A runtime mechanism exists, reachable by engineers or professional services through files, git, config or API. Not exposed to admins. |
| 3 | Productised. Admins or tenants do it through UI or a supported self-serve path, validated, previewable, with no deploy. |
| 4 | Generative and policy-gated. Machine-readable data the platform interprets, producible and consumable by an AI, with a policy gate that decides whether a human is needed, and rollback. |

For the E dimension the ladder reads: 0 no audit, 1 manual audit, 2 automated scan on demand, 3 scan wired as a gate on every change, 4 continuous scan plus automatic fix proposals through the change path.

## Evidence grades

**A** code-verified in the repository at a named tip. **B** verified from first-party documentation, audits or configuration in hand. **C** inferred from product knowledge or secondary material; a C-graded score is capped at 2.

## Evidence status

- **assessed** means the criterion was evaluated and can be assigned an anchored score. Use score 0 when primary evidence establishes absence.
- **not_evidenced** means the criterion appears applicable but the inspected sources could not establish presence or absence. It scores 0 in the evidence-limited index and is reported as uncertainty.
- **not_applicable** means the criterion is outside the product's intended archetype. It is excluded from the denominator and requires a specific rationale.

Read `archetypes.md` before applying `not_applicable`. Missing functionality is not non-applicability.

## Scoring rules

1. Score what ships today, not the roadmap.
2. Every assessed criterion cites evidence, including the inspected surface for an assessed 0.
3. A capability that exists for one entity family only scores at most 2 (`single_entity: true` in the scores file).
4. A capability that has caused a production incident loses one point (`incident: true`).
5. Criteria are integers. Dimension means are reported to one decimal. Indexes are means of dimension means after approved non-applicable criteria are excluded.
6. Compliance and security are scored on whether they are structural and continuously verified. The latest audit result is an input, never a score.
7. Name the branch or tip the evidence was read from. A claim is branch-scoped until proven otherwise.

---

# Pillar 1: Define

## Dimension A: Entity and schema as data

### A1 New entity type without code, DDL or deploy
**Definition.** A new kind of business object, with its own fields, storage, permissions and API presence, can be created and used without writing code, running a schema migration, or deploying.
**Why it matters.** Everything else in the framework generates from the type. If a type needs code, nothing downstream can be data.
**Evidence.** A type registry, enum or table that lists entity kinds and how it is populated. Whether adding a kind requires DDL. Any "custom object" UI or API. Whether a deploy is required.
- **0** Types are hard-coded and adding one is a project.
- **1** Adding a type is code plus migration plus release.
- **2** A runtime type registry or generic store exists but is populated by engineers through config, migration or API.
- **3** Admins define types through UI or a supported API, live, validated, with no deploy.
- **4** Types are machine-readable definitions an AI can author, validated with dry-run, versioned, and applied through a policy gate.

### A2 Field definitions carry type, validation and privacy classification
**Definition.** Fields on any entity are declared with a data type, validation rules and a privacy classification that forms, API, search and erasure all read.
**Why it matters.** Validation and privacy handled per feature is how compliance becomes engineering work; declared once, it becomes inherited.
**Evidence.** Custom field types and their storage. Where validation rules live. Any personal-data or sensitivity tag on fields. Whether the tag is consumed anywhere.
- **0** Fields are database columns only.
- **1** Field additions are code.
- **2** Typed custom fields exist through API for engineers; validation partial; no privacy tag or a tag nothing consumes.
- **3** Admins add typed, validated fields through UI; a privacy tag exists on at least one entity family and is consumed.
- **4** Every field has type, validation and privacy tag in one machine-readable definition consumed by forms, API, search and erasure; AI-authorable.

### A3 Relationships and lifecycle states declarable
**Definition.** Relationships between entities and lifecycle states with transitions are declared in the definition, not coded per feature.
**Why it matters.** Most product behaviour is a relationship or a state change. If those are code, so is the product.
**Evidence.** Generic association or relation tables. Workflow or state tables. Per-feature state enums in code. Any admin UI for states.
- **0** None.
- **1** Coded per feature.
- **2** A generic relation or state mechanism exists for engineers, not exposed.
- **3** Admins declare relations and states with transitions through UI.
- **4** Referential integrity and transition guards are enforced by the platform from the definition; AI-authorable.

## Dimension B: API surface generation

### B1 API per entity is generic or generated
**Definition.** An entity's read and write API exists without an engineer writing a resolver or controller for that entity.
**Why it matters.** Hand-written API per entity is the largest fixed cost of a new type and the largest source of contract drift.
**Evidence.** Count of hand-written resolvers, registries or controllers. Any generic entity endpoint. Whether codegen starts from a hand-written schema or from definitions.
- **0** No API.
- **1** Hand-written per entity.
- **2** A generic surface exists for one entity family, or codegen runs from a hand-written schema.
- **3** API for defined entities is generic or generated from definitions with no per-entity code.
- **4** Generated API includes typed projections, filters and validation from the definition and updates at runtime.

### B2 API reshapes at runtime from definitions
**Definition.** A definition change changes the API surface without a build or deploy.
**Why it matters.** This is what makes "no code release" literal rather than aspirational.
**Evidence.** How and when the schema is assembled. Cache invalidation triggers. Whether any resource change reshapes the schema live.
- **0** Schema is compiled into the artifact.
- **1** Any change needs a deploy.
- **2** Runtime schema assembly with invalidation exists, but only from engineer-managed resources.
- **3** Publishing a definition reshapes the API live for that tenant.
- **4** Reshaping is versioned per consumer with deprecation windows and dry-run.

### B3 Machine-readable contract with introspection and dry-run
**Definition.** Callers can discover the API, generate typed clients, and validate or dry-run a mutation before executing it.
**Why it matters.** An AI or agent can only act safely on a contract it can read and test.
**Evidence.** Introspection or OpenAPI coverage. Client codegen. Structured validation errors. Any dry-run or preview mode. Published schema artifacts per build.
- **0** Documentation only.
- **1** Hand-written docs.
- **2** Partial machine-readable contract: introspection or partial OpenAPI.
- **3** Full introspection, typed client generation, structured server validation errors.
- **4** Dry-run mode for mutations, contract tests, versioned schema artifacts published per build.

## Dimension C: Rendering follows the definition

### C1 Layout is data, tenant-overridable, validated, previewable
**Definition.** Page structure, which components, where, with what props, is stored as validated data, overridable per tenant, previewable before publish.
**Why it matters.** Layout as data is where natural-language UI authoring becomes tractable, because the target is a constrained format.
**Evidence.** Layout files or tables and their schema. A page designer. Per-tenant override storage. Preview mechanism. Whether component props are schema-validated.
- **0** Layout is coded.
- **1** Templates in code.
- **2** Layout files as data, engineer-edited, no tenant override.
- **3** Admin layout editor with per-tenant overrides, schema validation, preview.
- **4** Layout and component props target a machine-validated schema; AI-authorable; versioned with rollback.

### C2 Generic list, detail and intake widgets from definition plus view spec
**Definition.** List, detail and create or edit views render from the entity definition and a view spec, so a new type gets UI without new components.
**Why it matters.** Without generic widgets, every new type still needs a front-end feature.
**Evidence.** Whether forms render from a spec. Whether custom fields render generically. Any list or card component parameterised by type. A view spec format.
- **0** None.
- **1** Every view hand-built.
- **2** Partial generic rendering exists, such as forms from a spec or generic field display, but not list, detail and intake together.
- **3** Generic list, detail and intake widgets exist and admins configure view specs.
- **4** View specs are machine-readable and AI-authorable with inherited accessibility and theme.

### C3 Theme tokens and text are data with tenant overrides
**Definition.** Visual tokens and UI text are externalised data with tenant overrides and locale coverage.
**Why it matters.** Brand and language are the most frequent tenant changes; if they are code, tenants queue for releases.
**Evidence.** Token count and how they are served. A theme editor. Text storage, locale count, tenant override UI, translation pipeline.
- **0** Hard-coded.
- **1** CSS and strings in code.
- **2** Tokens and text externalised but engineer-managed.
- **3** Admin theme editor, per-tenant text overrides, locale pipeline.
- **4** Tokens and text carry a machine-readable schema, changes flow through the proposal path, AI translation and theming validated with contrast checks.

## Dimension D: Behaviour as data

### D1 Rules engine with declarative conditions and actions
**Definition.** Conditions and actions defined as data trigger behaviour such as notifications, role changes, webhooks and state transitions.
**Why it matters.** Most feature requests are behaviour. A rules engine turns them into configuration.
**Evidence.** Rule, condition and action classes or tables. Admin UI for rules. Whether rules cover custom or defined entities. Any simulation or test mode.
- **0** None.
- **1** Behaviour coded.
- **2** Engine exists but is engineer or API only, or narrow in scope.
- **3** Admins compose rules through UI across entities with a test mode.
- **4** Rules are machine-readable, simulatable against history, versioned, AI-authorable, and cover defined entities.

### D2 Event model with webhooks or subscriptions and retry
**Definition.** Entity lifecycle events publish to a durable bus and to outbound subscribers with retry and replay.
**Why it matters.** Integration and automation both hang off events; without durability they are best-effort.
**Evidence.** Event bus or listener framework. Webhook manager. Retry queue. Delivery logs. Replay capability.
- **0** None.
- **1** Per-feature listeners in code.
- **2** Event mechanism exists; webhooks limited or without retry.
- **3** Admins subscribe to events with webhooks, retry and delivery logs.
- **4** Event schema generated from definitions including defined entities; replay; per-tenant streams.

### D3 Sandboxed server-side hooks
**Definition.** Custom server-side logic runs at defined hook points without deploying core, isolated by dependency allowlists, timeouts and egress control.
**Why it matters.** The residue rules cannot express needs code; unsandboxed code is how platforms become un-upgradable.
**Evidence.** Custom endpoint or hook framework. Trigger types. Allowlists. Runtime isolation. Egress control. Who can deploy hooks.
- **0** None.
- **1** Core code only.
- **2** Server-side extension exists but is unsandboxed or request-triggered only.
- **3** Sandboxed hooks with allowlists, timeouts and egress control, triggered by events and requests, deployable by partners.
- **4** Hooks are AI-authorable with a test harness, policy-gated, observable per hook.

# Pillar 2: Trust

## Dimension E: Compliance and security as infrastructure

### E1 Accessibility inherited from a component kit and continuously verified
**Definition.** Accessibility comes from a component kit and design tokens and is verified continuously, not engineered per feature.
**Why it matters.** Per-feature accessibility is re-paid on every feature and fails audits.
**Evidence.** Component kit and token usage share. Automated scanners. Whether scans gate changes. Required accessible props enforced by lint. Conformance reporting.
- **0** No audit and no kit.
- **1** Manual audits; per-feature fixes.
- **2** Component kit and tokens; automated scans on demand.
- **3** Scans gate every change; the kit enforces required accessible props.
- **4** Continuous scanning with automatic fix proposals through the change path; conformance report generated with human sign-off where required.

### E2 Audit generic over entities, definition changes and approvals
**Definition.** One audit trail records every entity mutation, definition change and approval, queryable by admins.
**Why it matters.** SOC 2 change control needs evidence per change; a generic trail makes it free.
**Evidence.** Audit table or service and its schema. Coverage across entities. Admin UI. Whether config or definition changes are recorded. Retention.
- **0** None.
- **1** Per-feature logs.
- **2** Generic audit store exists; coverage partial; no admin UI or definitions uncovered.
- **3** Admin UI; covers all entities, configuration and definition changes, and approvals; retention policy.
- **4** Audit events are structured, exportable, tamper-evident, and consumed by the advise loop.

### E3 GDPR export, erasure and retention generic over entities
**Definition.** Data subject export, erasure and retention work for every entity based on privacy tags, not per-feature code.
**Why it matters.** A metadata-driven platform without this fails GDPR the first time a tenant defines a personal field.
**Evidence.** Erasure and export services and which entities they cover. Privacy tags. Retention policies. Admin triggers. Verification reports.
- **0** None.
- **1** Manual or engineer-run scripts.
- **2** Implemented for one entity family only.
- **3** Admin-triggered export and erasure across entities through tags; retention policies.
- **4** Automatic detection of untagged personal data with tagging proposals; verified erasure reports.

### E4 Security as infrastructure
**Definition.** Authorisation derives from definitions, input validation is generic over entities, and vulnerability scanning is continuous and gates change.
**Why it matters.** Security handled per feature drifts, as reverted mitigations show.
**Evidence.** Permission model and how new permissions are declared. Validation framework and whether it is mandatory. SAST, dependency and container scanning in CI. Whether scans block merges. Runtime policy enforcement.
- **0** None.
- **1** Per-feature checks; manual penetration tests.
- **2** Generic permission model and mandatory validation; scans on demand.
- **3** Scanning gates every change; authorisation generated per defined type.
- **4** Continuous scanning with auto-remediation proposals; runtime policy enforcement; incidents feed rules.

## Dimension F: Change control

### F1 Definitions and layouts versioned with rollback
**Definition.** Every definition, layout, text, theme and configuration change is a version that can be diffed and rolled back.
**Why it matters.** Malleability without rollback is risk; rollback is what lets a policy gate apply changes.
**Evidence.** Version storage for each customisation surface. Diff and history UI. Rollback path. Whether all surfaces are covered.
- **0** None.
- **1** Only in code version control, for engineers.
- **2** Versioning for some surfaces, or without a rollback UI.
- **3** Admins see history, diff and roll back across all customisation surfaces.
- **4** Versions are addressable objects linked to proposals and evidence; rollback automatic on failed verification.

### F2 Proposal, review, apply as a first-class object with preview
**Definition.** A change is a proposal carrying diff, rationale, evidence and preview, reviewed, then applied.
**Why it matters.** This is the object an AI produces and a gate consumes; without it, AI output is a chat message.
**Evidence.** Any proposal or change-request object. Stage and publish workflows. Preview on staging data. Who can create proposals.
- **0** None.
- **1** Pull requests for code only.
- **2** Stage and publish or GitOps flow for engineers.
- **3** Admins propose, preview and apply on staging data with review.
- **4** Proposals are typed objects any actor can create; preview on production-shaped data; evidence attached automatically.

### F3 Policy-based apply with recorded approvals and a movable human boundary
**Definition.** A policy decides which proposal classes apply automatically on passing checks and which need a human; approvals are recorded; the boundary moves with measured verifier trust.
**Why it matters.** Human gating everywhere does not scale; no gating anywhere fails audit. Policy is the middle.
**Evidence.** Policy object or configuration. Auto-apply classes. Approval records. Verifier false-pass measurement. Kill switch.
- **0** None.
- **1** Every change needs a human.
- **2** Auto-apply for narrow classes, such as deploy sync, without a policy object.
- **3** Policy object per change class with recorded approvals.
- **4** Policy adapts to verifier false-pass rates; full audit; kill switch.

### F4 Upgrade safety
**Definition.** Tenant customisations and definitions survive a platform release without code migration.
**Why it matters.** Unlimited malleability at the code layer produced un-upgradable estates; this criterion scores that failure before it happens.
**Evidence.** Extension contract versioning. Compatibility checks. Migration tooling. History of customisations breaking on upgrade.
- **0** Customisations break each release.
- **1** Manual migration per tenant.
- **2** Versioned extension contracts; compatibility mostly manual.
- **3** Automated compatibility checks and migration tooling; customisations confined to stable contracts.
- **4** Backward compatibility guaranteed for definitions with automated migration proposals; breaking changes need a policy exception.

## Dimension G: Performance under genericity

### G1 Indexed query path, never a scan of a generic store
**Definition.** Lists and filters over generic or defined entities go through an index; get-by-id goes to the store; caching is in place.
**Why it matters.** Generic storage is the classic performance trap of metadata platforms.
**Evidence.** Search index and mappings. Whether custom or defined fields are filterable at scale. Query paths for lists. Caching layers.
- **0** No index; scans.
- **1** Relational queries hand-tuned per feature.
- **2** Search index exists; generic or custom fields not filterable at scale.
- **3** Definitions drive index mappings; lists via index; caching.
- **4** Query plans derived from definitions with cost limits and observability.

### G2 Tenant isolation and noisy-neighbour controls
**Definition.** Tenants cannot degrade or read each other; per-tenant limits exist.
**Why it matters.** Malleable tenants generate unpredictable load.
**Evidence.** Tenancy model. Quotas. Isolation verification. Autoscaling per tenant.
- **0** None.
- **1** Shared without controls.
- **2** Shared with basic quotas, or single-tenant per deployment.
- **3** Per-tenant limits, noisy-neighbour detection, data isolation verified.
- **4** Elastic per-tenant scaling governed by policy.

### G3 Ceilings measured, not discovered in incidents
**Definition.** Scalability limits per surface are measured, documented and regression-tested.
**Why it matters.** Unknown ceilings become customer-found incidents.
**Evidence.** Load or performance suites. Documented limits. Incident history of performance failures.
- **0** Unknown.
- **1** Discovered in incidents.
- **2** Some load tests.
- **3** Documented limits per surface with a performance suite in CI.
- **4** Continuous performance regression gating against budgets.

## Dimension H: Stack flexibility and verification

### H1 Layers deploy independently
**Definition.** Front end, API and core deploy independently, containerised, with no cross-layer build coupling.
**Why it matters.** Coupling forces every change onto the slowest layer's train.
**Evidence.** Deployables and their build dependencies. Containerisation. Release trains. Cross-layer artifacts consumed at build time.
- **0** One artifact.
- **1** Monolith, manual.
- **2** Containerised layers with build coupling.
- **3** Independently deployable services with contracts; no cross-layer build.
- **4** Progressive delivery per layer with automatic rollback.

### H2 Module boundaries enforced by tooling
**Definition.** Architectural boundaries are enforced by the build or by tests, not by convention.
**Why it matters.** Unenforced boundaries erode, and erosion is what makes change expensive.
**Evidence.** Dependency graph enforcement. Architectural tests or lints. Contracts between modules.
- **0** None.
- **1** Convention.
- **2** Build-system enforced dependency graph.
- **3** Architectural tests or lints plus API contracts between modules.
- **4** Boundaries derived from definitions; violations blocked at PR with explanations.

### H3 Every change class has an automated pre-land check
**Definition.** Each kind of change has a deterministic check that runs before it can land, including schema build, lint, tests, accessibility and security, and drafts are included.
**Why it matters.** AI build throughput is only safe if the checks are automatic and unskippable.
**Evidence.** CI configuration. Which change classes have checks. Whether drafts skip CI. Flake handling. Incidents that passed CI.
- **0** None.
- **1** Manual QA.
- **2** CI on PRs with gaps: drafts skip, some classes uncovered.
- **3** Every change class has a deterministic pre-land check and drafts are included.
- **4** Checks generated from definitions and change class; flake quarantine; evidence attached to proposals.

# Pillar 3: Extend

## Dimension I: Extension ecosystem

### I1 Plugin lane breadth
**Definition.** Plugin points exist across UI components, layout, forms, theme, text and server, in both declarative and code forms.
**Why it matters.** Breadth decides how much can be extended without touching core.
**Evidence.** Plugin or SDK documentation. Plugin point types. Declarative versus code options.
- **0** None.
- **1** Fork the code.
- **2** Code plugins only, or narrow points.
- **3** Declarative and code plugin points across UI, layout, forms, theme, text and server, documented.
- **4** Plugin points generated from definitions; registry or marketplace; versioned.

### I2 Runtime isolation and dependency control
**Definition.** Third-party or AI-written code runs isolated, with dependency allowlists, resource limits and egress control.
**Why it matters.** AI-authored code at volume is only safe inside a sandbox.
**Evidence.** Where plugin code executes. Allowlists and when they are enforced. CSP. Iframe or process isolation. Quotas.
- **0** Full trust.
- **1** Full trust with review.
- **2** Build-time allowlists and CSP; same process.
- **3** Runtime isolation, resource limits, egress control.
- **4** Per-plugin identity, quotas, observability, automatic disable on violation.

### I3 Developer loop
**Definition.** Extension developers can preview against a real tenant, use staged branches, read logs, and validate before publishing.
**Why it matters.** A slow loop pushes developers to hack core instead.
**Evidence.** Preview tooling. Staging branches. Log access. Validators. Local development support.
- **0** None.
- **1** Build and deploy to test.
- **2** Local development possible; documentation.
- **3** Preview against a real tenant, staged branches, logs, validators.
- **4** Ephemeral preview environments per change with a test harness and AI assistance.

## Dimension K: Agent and conversational readiness

### K1 Machine-readable capability surface over MCP
**Definition.** The product exposes typed tools generated from its definitions over MCP, introspectable, with a current capability map.
**Why it matters.** Agents act on tools, not on documentation.
**Evidence.** MCP server. Tool definitions and their source. Capability map. Auth scoping on tools.
- **0** None.
- **1** Hand-written API documentation.
- **2** Introspectable API; no tool surface.
- **3** MCP server exposing typed tools with scoped auth; capability map exists.
- **4** Tools generated from definitions including defined entities; capability map machine-readable and current.

### K2 Conversational operability for members and natural-language authoring for admins
**Definition.** Members complete tasks through a grounded conversational surface, and admins author definitions, layouts and text through natural language on the same surfaces the UI uses.
**Why it matters.** Conversation is the interface the vision assumes for both members and operators.
**Evidence.** Chat or assistant surfaces. Grounding sources. Actions available conversationally. Admin natural-language authoring. Evaluation harness.
- **0** None.
- **1** FAQ or keyword bot.
- **2** Grounded conversational surface for one persona, or admin natural language for one surface.
- **3** Members complete tasks conversationally with grounding and actions; admins author through natural language with preview.
- **4** Conversation and UI share definitions; every UI action has a conversational equivalent; an evaluation harness measures groundedness.

### K3 Agent-safe actions
**Definition.** Every mutation is scoped to a real identity rather than ambient authority, idempotent, previewable, audited and rate-limited.
**Why it matters.** An agent with ambient authority is an incident waiting for a prompt injection.
**Evidence.** Identity model for API callers. Token scoping. Idempotency keys. Dry-run. Rate limits. Audit rows. Kill switch.
- **0** Ambient authority.
- **1** Shared API keys.
- **2** Per-actor tokens and audit; no dry-run.
- **3** Scoped agent identity, idempotent mutations, preview or dry-run, rate limits, audit rows.
- **4** Policy-gated actions with kill switch, spend and rate budgets, per-action risk classification.

## Dimension N: Integration and connector extensibility

### N1 Canonical data model with a mapping layer
**Definition.** External systems integrate through a canonical model and a configurable mapping layer, so the second connector is field mapping, not core code.
**Why it matters.** This is the Salesforce-then-ServiceNow test: the second integration should cost a fraction of the first.
**Evidence.** Canonical entity model. Mapping configuration or UI. How existing integrations were built. Count of bespoke modules.
- **0** None.
- **1** Bespoke integration per system.
- **2** Canonical model for one domain; mapping partly code.
- **3** Configurable mapping layer, so a second connector is mapping.
- **4** Mapping machine-readable, AI-proposed from the target schema, validated with sample sync.

### N2 Connector definition or SDK
**Definition.** A connector definition or SDK covers authentication, sync, webhooks and lifecycle, so connectors are added without touching the kernel.
**Why it matters.** Without an SDK, every connector is a core project.
**Evidence.** Connector SDK or shared engine pattern. Lifecycle management. Who builds connectors. Admin install and configuration.
- **0** None.
- **1** Core code.
- **2** SDK exists for engineers; lifecycle manual.
- **3** Connector definition or SDK covers auth, sync, webhooks, lifecycle; partners build; admins install and configure.
- **4** Connectors generated or assisted from the target API spec; certified; observable.

### N3 Stable versioned contracts
**Definition.** Inbound and outbound contracts are versioned with deprecation windows, idempotent sync and conflict handling.
**Why it matters.** Unstable contracts make every platform change a partner incident.
**Evidence.** API versioning scheme. Deprecation policy. Idempotency. Conflict resolution. Contract tests.
- **0** None.
- **1** Undocumented changes.
- **2** Documented API; versioning by path; no deprecation policy.
- **3** Versioned contracts, deprecation windows, idempotent sync, conflict handling.
- **4** Contract tests in both directions; compatibility guaranteed by policy; replay.

## Dimension O: Adjacent-domain expansion

### O1 Kernel concepts are domain-neutral
**Definition.** The kernel is identity, content, conversation, permission, workflow and channel, with the domain expressed above it.
**Why it matters.** Domain nouns in the kernel make adjacent domains rewrites.
**Evidence.** Core entity names. Where domain-specific behaviour lives. Presence of a channel concept.
- **0** Single-purpose.
- **1** Domain baked in.
- **2** Some neutral primitives, but domain nouns remain in core.
- **3** Kernel is identity, content, conversation, permission, workflow and channel; domain expressed above.
- **4** Kernel primitives are themselves configurable definitions.

### O2 A new domain is expressible without kernel change
**Definition.** An adjacent domain is built as definitions plus connectors plus rules, with no kernel change.
**Why it matters.** This is the omnichannel or autonomous-agent test.
**Evidence.** Any adjacent domain shipped this way. What a new domain would need in core today.
- **0** Rewrite.
- **1** Major core work.
- **2** Mechanisms exist but a new domain needs core additions.
- **3** New domain as definitions, connectors and rules; proven by at least one adjacent domain shipped this way.
- **4** Multiple domains shipped as bundles with the kernel unchanged.

### O3 A domain ships as an installable bundle
**Definition.** A domain or solution ships as a versioned bundle of definitions, layouts, rules and connectors that can be applied to a tenant.
**Why it matters.** Bundles are how a platform sells opinionated workflows instead of blank canvases.
**Evidence.** Export and import of assets. Templates. Bundle format and versioning.
- **0** None.
- **1** Manual setup.
- **2** Export and import of assets per tenant.
- **3** Installable bundle of definitions, layouts, rules and connectors, versioned.
- **4** Bundles composable, upgradeable, AI-assembled from requirements.

# Pillar 4: Evolve

## Dimension J: Observe

### J1 Telemetry accessible to the platform in near real time
**Definition.** Usage and behaviour telemetry is available to platform features within minutes, not only to analysts nightly.
**Why it matters.** Self-evolution starts with seeing.
**Evidence.** Event pipeline and latency. Consumers inside the product. Per-feature instrumentation.
- **0** None.
- **1** Logs.
- **2** Batch analytics.
- **3** Near-real-time events available to platform features.
- **4** Streaming with per-entity and per-definition instrumentation added automatically.

### J2 Feedback captured as structured objects
**Definition.** Member reports, admin signals and support tickets are structured objects linked to entities, features and versions.
**Why it matters.** Free-text feedback cannot drive proposals.
**Evidence.** Feedback types. Linking to entities. Triage workflow. Closure loop with reporter.
- **0** None.
- **1** Free-text reports.
- **2** Some typed feedback, such as moderation reports.
- **3** Feedback objects linked to entities, features and versions with a triage workflow.
- **4** Feedback auto-classified and linked to proposals; loop closes with the reporter.

### J3 Cross-source mining inside the product
**Definition.** The product joins usage, support and delivery data into queryable models and mines them continuously.
**Why it matters.** Diagnosis needs joined data; analysis done outside the product does not compound.
**Evidence.** Data lake or warehouse and what it joins. Mining jobs. Whether findings surface in the product.
- **0** None.
- **1** Manual analysis outside the product.
- **2** A data lake joins some sources.
- **3** Product joins usage, support and delivery data with queryable models.
- **4** Continuous mining producing candidate findings with provenance.

## Dimension M: Advise and act

### M1 Ranked, evidence-backed proposals for software change
**Definition.** From mined data, the product produces ranked proposals for software change with evidence and expected impact.
**Why it matters.** This is the difference between a dashboard and a self-diagnosing system.
**Evidence.** Recommendation features. Proposal objects. Ranking and evidence. Post-apply impact measurement.
- **0** None.
- **1** Dashboards.
- **2** Insights or recommendations for one area.
- **3** Ranked evidence-backed proposals for software change across the product with expected impact.
- **4** Proposals carry definition diffs ready for the gate and post-apply impact measurement.

### M2 Proposals for process change
**Definition.** The product proposes changes to how the customer runs their operation and to how the vendor delivers, with evidence.
**Why it matters.** Consultative value is the part no feature request captures.
**Evidence.** Benchmarks. Operational recommendations. Delivery-process recommendations. Implementation paths.
- **0** None.
- **1** Reports.
- **2** Benchmarks against peers.
- **3** Consultative proposals for customer operations and delivery process with evidence.
- **4** Proposals include an implementation path through rules, definitions or training, with measured outcomes.

### M3 Aligned proposals implement at scale with an AI authoring lane
**Definition.** Accepted proposals implement through the definition and proposal path across tenants, authored by an AI lane.
**Why it matters.** Proposals that need a human to hand-build per tenant do not scale.
**Evidence.** AI authoring lane and its scope. Cross-tenant application. Policy gate. Measurement after apply.
- **0** None.
- **1** Manual per tenant.
- **2** AI lane for narrow tasks, engineer-run.
- **3** Aligned proposals implemented across tenants through definitions and proposals under policy.
- **4** Closed loop: propose, gate, apply, measure, learn, with rollback.

### M4 Post-change impact is measured against a declared baseline
**Definition.** Every material applied change carries a baseline, intended outcome, observation window and decision to keep, revise or roll back.
**Why it matters.** Applying a proposal is not evidence that it improved the product or operation. A learning loop exists only when impact changes the next decision.
**Evidence.** Proposal-to-metric linkage. Baseline capture. Success thresholds. Observation windows. Segment or counterfactual comparison where practical. Recorded keep, revise or rollback decisions.
- **0** No post-change outcome measurement.
- **1** Ad hoc manual before-and-after checks.
- **2** Relevant telemetry exists, but it is not bound to the proposal version, baseline and decision.
- **3** Applied proposals record a baseline, target metric, observation window and explicit keep, revise or rollback decision.
- **4** Instrumentation is created with the proposal; policy uses measured impact to promote, revise or reverse the change, with attribution limits recorded.

## Dimension L: Factory surfaces

### L1 Verification surface
**Definition.** A machine-readable build and version endpoint, health, and a deployed-configuration snapshot.
**Why it matters.** A pipeline cannot verify what it cannot probe.
**Evidence.** Version or build endpoint. Health checks. Config snapshot. Deployment events.
- **0** None.
- **1** Version visible in the UI only.
- **2** Version endpoint or health, without a config snapshot.
- **3** Build and version endpoint, health, deployed-config snapshot, machine-readable.
- **4** Deployment events emitted and verification evidence attached automatically.

### L2 Environment reproducibility
**Definition.** An instance can be created from a build id with seeded data, flags off first, and destroyed after.
**Why it matters.** Environment drift multiplies QA rounds and hides defects.
**Evidence.** Instance provisioning tooling. Time to create. Seed data. Sharing model. Configuration source and access.
- **0** Hand-built.
- **1** Long-lived shared environments.
- **2** Scripted instance build from a build id; hours; shared.
- **3** Ephemeral instance per change from a build id with seeded data, flags off, destroyed after.
- **4** On demand in minutes with production-shaped anonymised data and cost controls.

### L3 Machine verifiability
**Definition.** Deterministic journeys across roles and devices, a changed-path to feature to journey map, and per-feature adoption instrumentation at ship.
**Why it matters.** Without this, acceptance is a human reading a screen.
**Evidence.** End-to-end suites and their state. Path-to-journey mapping. Adoption instrumentation coverage.
- **0** Manual testing.
- **1** Unit tests only.
- **2** End-to-end journeys exist but are partial or dormant; no path map; no adoption instrumentation.
- **3** Deterministic journeys across roles and devices, changed-path to journey map, per-feature adoption instrumentation at ship.
- **4** Journeys generated from definitions; verification evidence attached to proposals automatically.
