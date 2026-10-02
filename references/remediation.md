# EVOLVE Remediation Catalogue

For every criterion in `rubric.md`: the move that reaches level 3 (productised), the move that reaches level 4 (generative and policy-gated), prerequisites among criteria, and a size. `scripts/score.py --prescribe` reads this file by the `### <ID>` headings and prints, for each criterion below target, the moves and the prerequisite order. It also lists what blocks the next Software Autonomy Level, which is usually the best place to start. Edit here, nowhere else.

Sizes: **S** a small bounded change, **M** a multi-surface or multi-sprint change, **L** a cross-team or architectural change. These are relative ordering aids, not estimates. Re-estimate every item for the assessed software.

Format per criterion: `To 3:` · `To 4:` · `Requires:` (hard prerequisites: criterion ids that must reach the target first, or none) · optional `Helps:` (soft prerequisites, shown but not used for ordering) · `Size:`.

# ARC: Elastic (architecture)

### ARC-01
To 3: Definition-driven index mappings (index mappings by field type) and a generic filler; all list and filter queries via the index; get-by-id via the store; caching.
To 4: Query plans derived from definitions with cost limits and observability.
Requires: MAL-01, MAL-02
Size: M

### ARC-02
To 3: Run migrations in CI against representative data; enforce expand-and-contract (or an equivalent online strategy) for destructive changes with a migration linter; route runtime definition changes through the same migration mechanism.
To 4: Plan, preview and validate migrations for AI-authored and self-made changes; refuse unsafe ones by policy; reverse automatically.
Requires: none
Helps: DEL-05
Size: M

### ARC-03
To 3: Move sessions, caches, locks and files into shared managed stores; remove in-process singletons or add leader election; document and test scale-out in deployment manifests.
To 4: Autoscale on load signals and verify scale-out behaviour in a performance environment.
Requires: none
Size: M

### ARC-04
To 3: Make queued work idempotent with back-off, dead-lettering and visibility; ensure scheduled jobs run once across instances.
To 4: Per-tenant fairness and priorities in queues, with back-pressure.
Requires: none
Size: M

### ARC-05
To 3: Per-tenant quotas and rate limits; noisy-neighbour detection; isolation verification tests.
To 4: Elastic per-tenant scaling under policy.
Requires: none
Size: M

### ARC-06
To 3: Document limits per surface; performance suite in CI against budgets.
To 4: Continuous performance regression gating.
Requires: none
Size: S

### ARC-07
To 3: Publish latency, availability or throughput objectives for core paths and alert on them.
To 4: Feed error budgets into rollout and rollback decisions.
Requires: LRN-01
Size: S

### ARC-08
To 3: Inventory connectors, plugins, AI providers, tenant workloads and internal services; give each timeouts and circuit breakers or bulkheads, with tested fallbacks.
To 4: Declare degradation modes per capability, exercise them with automated fault injection, and switch them by policy.
Requires: none
Size: M

### ARC-09
To 3: Supported backup and restore for data, definitions, files and secrets, with automated restore tests.
To 4: Stated RPO and RTO, point-in-time or per-tenant restore, and recorded restore drills.
Requires: none
Size: M

# DEL: Velocity (delivery)

### DEL-01
To 3: Capture requests in the product with structure, and turn each into a change specification with acceptance criteria, affected definitions and a risk class for a person to confirm.
To 4: Make the specification machine-readable so it drives the implementation lane and tests; ask clarifying questions on ambiguous requests.
Requires: none
Helps: LRN-02
Size: M

### DEL-02
To 3: Publish cross-layer contracts as artifacts (schema, hashes) so no layer reads another's source tree at build; independent deploy per layer off shared release trains.
To 4: Progressive delivery per layer with automatic rollback.
Requires: MAL-06
Size: M

### DEL-03
To 3: Architectural tests or lints on top of the dependency graph; explicit API contracts between modules.
To 4: Boundaries derived from definitions; violations blocked at PR with explanations.
Requires: none
Size: S

### DEL-04
To 3: An AI lane, shipped as part of the product's first-party evolution system, that implements accepted changes end to end through definitions or a tested code change and submits them as proposals with verification evidence, under policy.
To 4: Cover every change class, let the lane choose the definition or code path, and measure its output after release with rollback.
Requires: GOV-06, DEL-05
Helps: MAL-01, GOV-10, LRN-09
Size: L

### DEL-05
To 3: A named, mandatory check per change class (schema build, lint, unit, accessibility, security), run on drafts too; flake quarantine.
To 4: Checks generated from definitions and change class; evidence attached to proposals.
Requires: none. This is the cheapest high-leverage move on most products.
Size: S

### DEL-06
To 3: A machine-readable build and version endpoint, health, and deployed-configuration snapshot.
To 4: Deployment events emitted; verification evidence attached automatically.
Requires: none. Usually the cheapest factory move.
Size: S

### DEL-07
To 3: Ephemeral instance per change from a build id with seeded data, flags off first, destroyed after; tenant configuration behind an API rather than a hand-edited store.
To 4: Minutes to provision with production-shaped anonymised data and cost controls.
Requires: DEL-06, DEL-02
Size: L

### DEL-08
To 3: Deterministic journeys across roles and devices, maintained and running; a changed-path to feature to journey map; per-feature adoption instrumentation at ship.
To 4: Journeys generated from definitions; verification evidence attached to proposals.
Requires: DEL-06, DEL-07, LRN-01
Size: M

### DEL-09
To 3: Let any change class (code, definition or learned change) go to a cohort, tenant or percentage first.
To 4: Progress or halt exposure automatically on health and impact signals, under policy.
Requires: none
Size: M

### DEL-10
To 3: A runtime kill switch, per tenant or global, for every change the evolution system ships; audit its use.
To 4: Trigger it automatically on health or impact signals, under policy.
Requires: none
Helps: DEL-09
Size: S

### DEL-11
To 3: One-step, tested rollback to the previous release, with schema and data kept backward-compatible across one release.
To 4: Roll back automatically when verification, health or impact signals fail after release.
Requires: ARC-02
Size: M

# MAL: Open (malleability)

### MAL-01
To 3: Introduce a versioned type-definition store and a generic store for entities of defined types, and let the entity-type registry accept defined types. Ship an operator type designer over the store.
To 4: Expose the definition as a machine-readable schema an AI can author; validate with dry-run; route publish through the proposal path (GOV-06) and policy gate (GOV-07).
Requires: none. This is the root of the dependency graph.
Size: L

### MAL-02
To 3: Expose typed, validated field authoring in the type designer, with forms and API reading the same definition.
To 4: One field definition consumed by forms, API, search, erasure and audit; AI-authorable through a validated path.
Requires: MAL-01
Size: M

### MAL-03
To 3: Add relation and lifecycle-state sections to the type definition, backed by a generic relation table and a state table; expose both in the type designer.
To 4: Platform-enforced referential integrity on write and transition guards from the definition; AI-authorable.
Requires: MAL-01
Size: M

### MAL-04
To 3: Serve a generic API for every defined type from its definition: read, list with filter, sort and paging, create, update, delete and state transitions. No per-type handlers.
To 4: Generated typed projections and filters per type; validation from the definition; runtime updates.
Requires: MAL-01
Size: M

### MAL-05
To 3: Publishing a definition reshapes the API for that tenant with no deploy, by assembling the schema at runtime and invalidating it on change.
To 4: Per-consumer schema versions with deprecation windows and a dry-run endpoint.
Requires: MAL-04
Size: S

### MAL-06
To 3: Publish a versioned schema artifact per build; structured validation errors; typed client generation from the artifact.
To 4: Dry-run mode on every mutation; contract tests in CI against the artifact.
Requires: none
Size: S

### MAL-07
To 3: Store layout as data with an operator designer, a props schema on every component, and preview on tenant data.
To 4: Layout and props authorable from natural language against the schema; versioned with rollback through GOV-05.
Requires: none
Size: S

### MAL-08
To 3: Build the generic widget family: list, card, detail, intake form, filter, chart, each parameterised by type key and a validated view spec. Map definition field types onto form field components.
To 4: View specs AI-authorable; accessibility and theme inherited from the kit and gated (GOV-01).
Requires: MAL-01, MAL-02
Size: M

### MAL-09
To 3: Theme editor, per-tenant text overrides, locale pipeline with AI translation, if any are missing.
To 4: Token and text schema; contrast checks on theme changes; changes through the proposal path.
Requires: none
Size: S

### MAL-10
To 3: Give the operator a rules engine across entities with a test or simulation mode, including conditions and actions for defined entities (created, transitioned, field changed; transition, notify, webhook).
To 4: Rules simulatable against history, versioned, AI-authorable.
Requires: none
Helps: MAL-01 (defined-entity coverage)
Size: M

### MAL-11
To 3: Publish lifecycle events for every entity, including defined ones, to a durable bus; admin webhook subscriptions with retry and delivery logs.
To 4: Event schema generated from definitions; replay; per-tenant streams.
Requires: none
Helps: MAL-01 (defined-entity events)
Size: M

### MAL-12
To 3: Event- and request-triggered hooks; runtime dependency allowlist, timeouts, egress allowlist, resource limits; partner-deployable.
To 4: AI-authored hooks with a test harness, policy-gated, per-hook observability.
Requires: MAL-11, MAL-14
Size: M

### MAL-13
To 3: Declarative plugin points (layout, forms, theme, text) alongside code plugin points (components, endpoints), documented.
To 4: Plugin points generated from definitions; registry or marketplace; versioned.
Requires: none
Size: M

### MAL-14
To 3: Runtime isolation for plugin code (process or iframe boundary), runtime dependency enforcement, resource limits, egress control.
To 4: Per-plugin identity, quotas, observability, automatic disable on violation.
Requires: none
Size: M

### MAL-15
To 3: Preview against a real tenant, staged branches, log access, validators.
To 4: Ephemeral preview environments per change with a test harness.
Requires: none
Helps: DEL-07 (ephemeral previews for the level 4 move)
Size: S

### MAL-16
To 3: A canonical integration model per domain (person, case, message, organisation) and a configurable mapping layer, so a second connector is mapping configuration.
To 4: Mapping proposed by AI from the target system's schema and validated with a sample sync.
Requires: none
Helps: MAL-01
Size: M

### MAL-17
To 3: A connector definition or SDK covering authentication, sync, webhooks and lifecycle; admin install and configure; partner-buildable.
To 4: Connectors generated or assisted from the target API specification; certification; observability.
Requires: MAL-16, MAL-11
Size: M

### MAL-18
To 3: Versioned contracts with deprecation windows; idempotent sync; conflict handling.
To 4: Contract tests both directions; compatibility by policy; replay.
Requires: MAL-06
Size: S

### MAL-19
To 3: A typed tool surface (MCP or equivalent) with scoped authentication; a capability map listing what the product can do.
To 4: Tools generated from definitions, including defined entities; capability map machine-readable and regenerated on publish.
Requires: MAL-06
Helps: MAL-01 (generated tools)
Size: M

### MAL-20
To 3: A grounded conversational surface for end users with actions; natural-language authoring for operators over definitions, layouts and text, with preview.
To 4: Every UI action has a conversational equivalent from the same definitions; groundedness measured by an evaluation harness.
Requires: MAL-19, MAL-07, GOV-06
Size: M

# LRN: Learn (learning)

### LRN-01
To 3: Expose the event pipeline to platform features within minutes; instrument every feature at ship as a definition-of-done item.
To 4: Streaming with per-entity and per-definition instrumentation added automatically.
Requires: none
Size: M

### LRN-02
To 3: Record feedback, ratings, corrections, evaluation outcomes and per-definition usage as typed signals linked to the definition and version they concern, with a triage workflow.
To 4: Auto-classification and linking to proposals.
Requires: none
Size: S

### LRN-03
To 3: Detect friction patterns (repeated failures, abandoned flows, retries, corrections, negative feedback, support requests) and raise them as issues attributed to a capability, with affected users and frequency.
To 4: Prioritise detected issues by impact and feed them into diagnosis and the change path automatically.
Requires: LRN-01
Helps: LRN-02
Size: M

### LRN-04
To 3: Join the product's own usage, feedback, errors and change history into queryable models inside the product.
To 4: Continuous mining producing candidate findings with provenance.
Requires: LRN-01, LRN-02
Size: M

### LRN-05
To 3: For each detected issue, produce a reproducible case and likely cause linked to the responsible definition, change or code area.
To 4: Validate diagnoses by reproducing the failure and checking the proposed fix against it.
Requires: LRN-03
Helps: LRN-04
Size: L

### LRN-06
To 3: Produce ranked, evidence-backed proposals to change the product's own behaviour or configured definitions, with expected impact, across the product.
To 4: Proposals carry definition diffs ready for the gate; post-apply impact measured.
Requires: LRN-04, GOV-06
Size: M

### LRN-07
To 3: A background review that runs after tasks or on idle, reads recent runs, and drafts candidate changes to skills, rules, prompts, memory or configuration without being asked; candidates go through the GOV-06 proposal path.
To 4: Prioritise candidates by expected impact and track which kinds of change pass evaluation and stick.
Requires: LRN-02
Helps: LRN-01
Size: M

### LRN-08
To 3: Evaluate every learned change against the current baseline on representative tasks or recorded data, and return pass, revise or block before apply.
To 4: Run the evaluation automatically with held-out data and feed pass rates into the GOV-07 policy.
Requires: LRN-07, GOV-06
Size: M

### LRN-09
To 3: Bind every applied proposal to a baseline, target metric, observation window and explicit keep, revise or rollback decision.
To 4: Generate instrumentation with the proposal and let policy use measured impact to promote, revise or reverse the change while recording attribution limits.
Requires: LRN-01, GOV-05, GOV-06, DEL-06
Size: M

# GOV: Vet (governance)

### GOV-01
To 3: Wire the accessibility scanners into CI as a blocking gate on every change class; enforce required accessible props in the component kit by lint or type.
To 4: Continuous scanning of deployed pages with automatic fix proposals through the proposal path; conformance report generated with human sign-off where the criterion needs judgment.
Requires: DEL-05
Size: M

### GOV-02
To 3: Record definition changes, configuration changes and approvals in the generic audit store; ship an admin audit UI with filters and retention.
To 4: Structured, exportable, tamper-evident audit events consumed by the advise loop (LRN-06).
Requires: none
Size: S

### GOV-03
To 3: Add a privacy classification to every field definition (none, personal, sensitive); drive operator-triggered export and erasure over every entity from it; retention policies per type; a verification report.
To 4: Automatic detection of untagged personal data with tagging proposals.
Requires: none
Helps: MAL-02
Size: M

### GOV-04
To 3: SAST, dependency and container scanning as blocking gates; authorisation verbs generated per defined type (view, create, edit, delete, manage) with role defaults; generic input validation from the definition.
To 4: Auto-remediation proposals for scan findings; runtime policy enforcement; incident findings become rules.
Requires: DEL-05
Helps: MAL-01 (generated authorisation)
Size: M

### GOV-05
To 3: Version every customisation surface (definitions, layouts, text, theme, config) with history, diff and rollback in the admin UI.
To 4: Versions as addressable objects linked to proposals and evidence; automatic rollback on failed verification.
Requires: none
Size: M

### GOV-06
To 3: A Proposal object: target kind, diff, rationale, evidence, preview reference, status, approver, applied version, rollback reference. Preview on a staging tenant using temporary overrides. Admin review queue.
To 4: Any actor including AI can create proposals; evidence attached automatically from checks.
Requires: GOV-05
Size: M

### GOV-07
To 3: A policy configuration per change class stating which classes auto-apply on passing checks and which need a named approver; approvals recorded in audit (GOV-02).
To 4: Policy adapts to measured verifier false-pass rates; kill switch; spend and rate budgets.
Requires: GOV-06, GOV-02, DEL-05
Size: M

### GOV-08
To 3: Versioned extension contracts; automated compatibility checks in CI for plugins and definitions against the next release; migration tooling.
To 4: Backward compatibility guaranteed for definitions with automated migration proposals; breaking changes require a policy exception.
Requires: none
Helps: MAL-13 (plugin contracts), MAL-01 (definition contracts)
Size: M

### GOV-09
To 3: Scoped agent identities (not shared keys), idempotency keys on mutations, dry-run, rate limits, audit rows per action.
To 4: Policy-gated actions with kill switch, budgets, per-action risk classification.
Requires: GOV-02, MAL-06
Size: M

### GOV-10
To 3: Declare and enforce a scope for every self-change path (surfaces, tenants, changes per period) with a blast-radius limit; block and log out-of-scope changes.
To 4: Make scopes versioned, reviewed policy that tightens automatically after a failed or reverted change.
Requires: none
Helps: GOV-07
Size: M

### GOV-11
To 3: Record provenance for every learned or AI-built change; separate untrusted inputs from instructions; scan for injection; never let untrusted input alone trigger an automatically applied change.
To 4: Bulk-revert by source and include adversarial inputs in automated evaluation.
Requires: none
Helps: LRN-08
Size: M

# EXP: Expand (expansion)

### EXP-01
To 3: Extract any missing neutral kernel primitive and move domain nouns above the kernel into definitions.
To 4: Kernel primitives themselves configurable.
Requires: MAL-01
Size: L

### EXP-02
To 3: Ship one adjacent domain as definitions plus connectors plus rules with the kernel unchanged, and prove it.
To 4: Multiple domains shipped as bundles.
Requires: MAL-01, MAL-03, MAL-10, MAL-17, EXP-01
Size: L

### EXP-03
To 3: A versioned bundle format for definitions, layouts, rules and connectors, installable to a tenant.
To 4: Bundles composable, upgradeable, AI-assembled from requirements.
Requires: MAL-01, GOV-05
Size: M

### EXP-04
To 3: Record unmet intents (failed searches, unsupported requests, feature requests, workaround use) and cluster them into themes outside the current domain, with volume, trend and segments.
To 4: Combine demand signals across tenants under privacy controls, refreshed continuously.
Requires: LRN-01
Helps: GOV-03
Size: M

### EXP-05
To 3: Propose adjacent capabilities unprompted, each with evidence, sizing, fit with existing concepts and a success metric, ranked for a decision.
To 4: Attach a buildable specification and a prototype assembled from bundles or the implementation lane.
Requires: EXP-04
Helps: EXP-01
Size: M

### EXP-06
To 3: Launch expansions to a cohort with a declared success metric, review date and clean removal path; record the keep-or-kill decision.
To 4: Measure the cohort against the metric and recommend keep, extend or kill under policy.
Requires: DEL-09
Helps: LRN-09, EXP-03
Size: M

# AIR: AI Readiness Checks

### AIR-01
To 3: Let operators choose models per AI feature through a supported path, and declare and test a resilience strategy for model failure: fallback model or provider, same-provider failover, self-hosted redundancy, or controlled degradation.
To 4: Route models by policy (cost, latency, quality) and evaluate equivalence before switching.
Requires: none
Helps: ARC-08
Size: M

### AIR-02
To 3: Record tokens and cost per request, user and tenant, and enforce per-tenant or per-user budgets or quotas with an admin view.
To 4: Degrade gracefully when budgets run low (cheaper model, queueing) and forecast usage.
Requires: none
Size: M

### AIR-03
To 3: Give AI features a governed context layer (retrieval, tools, schema-aware context) over product data and definitions that stays fresh automatically and attributes sources.
To 4: Generate the context layer from definitions so new entities reach AI without code, and measure retrieval quality.
Requires: AIR-04
Helps: MAL-19
Size: L

### AIR-04
To 3: Run every AI retrieval and tool call with the requesting user's permissions or a scoped agent identity, enforced in code, and add tests that try to obtain restricted data through AI.
To 4: Cover row- and field-level policy and tenant isolation with automated adversarial tests, and audit denials.
Requires: none
Helps: GOV-09
Size: M

### AIR-05
To 3: Maintain an evaluation set with metrics for each AI feature, run reproducibly, with results stored per prompt and model version.
To 4: Grow evaluation sets from production failures and feedback, including adversarial cases.
Requires: none
Size: M

### AIR-06
To 3: Block releases of prompt, model, tool or retrieval changes when evaluation scores regress past declared thresholds.
To 4: Extend gating to learned and self-made AI changes, with canary comparison in production.
Requires: AIR-05
Helps: DEL-05
Size: M

### AIR-07
To 3: Record, for every consequential AI action, what triggered it and for whom, inputs, model and prompt version, tool calls, output and resulting change, queryable by operators and retained.
To 4: Link traces to approvals and reversals; make them replayable and tamper-evident.
Requires: none
Helps: GOV-02
Size: M

### AIR-08
To 3: Monitor feedback, evaluator scores and failure and refusal rates per AI feature and model version, with alerts on drift.
To 4: Let drift trigger re-evaluation, rollback or a model switch under policy.
Requires: AIR-05
Helps: LRN-01
Size: M
