# MSR Remediation Catalogue

For every criterion in `rubric.md`: the move that reaches level 3 (productised), the move that reaches level 4 (generative and policy-gated), prerequisites among criteria, and a size. `scripts/score.py --prescribe` reads this file by the `### <ID>` headings and prints, for each criterion below target, the moves and the prerequisite order. Edit here, nowhere else.

Sizes: **S** a small bounded change, **M** a multi-surface or multi-sprint change, **L** a cross-team or architectural change. These are relative ordering aids, not estimates. Re-estimate every item for the assessed software.

Format per criterion: `To 3:` · `To 4:` · `Requires:` (hard prerequisites: criterion ids that must reach the target first, or none) · optional `Helps:` (soft prerequisites, shown but not used for ordering) · `Size:`.

# Pillar 1: Define

### A1
To 3: Introduce a versioned type-definition store and a generic store for entities of defined types, and let the entity-type registry accept defined types. Ship an operator type designer over the store.
To 4: Expose the definition as a machine-readable schema an AI can author; validate with dry-run; route publish through the proposal path (F2) and policy gate (F3).
Requires: none. This is the root of the dependency graph.
Size: L

### A2
To 3: Expose typed, validated field authoring in the type designer, with forms and API reading the same definition.
To 4: One field definition consumed by forms, API, search, erasure and audit; AI-authorable through a validated path.
Requires: A1
Size: M

### A3
To 3: Add relation and lifecycle-state sections to the type definition, backed by a generic relation table and a state table; expose both in the type designer.
To 4: Platform-enforced referential integrity on write and transition guards from the definition; AI-authorable.
Requires: A1
Size: M

### B1
To 3: Serve a generic API for every defined type from its definition: read, list with filter, sort and paging, create, update, delete and state transitions. No per-type handlers.
To 4: Generated typed projections and filters per type; validation from the definition; runtime updates.
Requires: A1
Size: M

### B2
To 3: Publishing a definition reshapes the API for that tenant with no deploy, by assembling the schema at runtime and invalidating it on change.
To 4: Per-consumer schema versions with deprecation windows and a dry-run endpoint.
Requires: B1
Size: S

### B3
To 3: Publish a versioned schema artifact per build; structured validation errors; typed client generation from the artifact.
To 4: Dry-run mode on every mutation; contract tests in CI against the artifact.
Requires: none
Size: S

### C1
To 3: Store layout as data with an operator designer, a props schema on every component, and preview on tenant data.
To 4: Layout and props authorable from natural language against the schema; versioned with rollback through F1.
Requires: none
Size: S

### C2
To 3: Build the generic widget family: list, card, detail, intake form, filter, chart, each parameterised by type key and a validated view spec. Map definition field types onto form field components.
To 4: View specs AI-authorable; accessibility and theme inherited from the kit and gated (E1).
Requires: A1, A2
Size: M

### C3
To 3: Theme editor, per-tenant text overrides, locale pipeline with AI translation, if any are missing.
To 4: Token and text schema; contrast checks on theme changes; changes through the proposal path.
Requires: none
Size: S

### D1
To 3: Give the operator a rules engine across entities with a test or simulation mode, including conditions and actions for defined entities (created, transitioned, field changed; transition, notify, webhook).
To 4: Rules simulatable against history, versioned, AI-authorable.
Requires: none
Helps: A1 (defined-entity coverage)
Size: M

### D2
To 3: Publish lifecycle events for every entity, including defined ones, to a durable bus; admin webhook subscriptions with retry and delivery logs.
To 4: Event schema generated from definitions; replay; per-tenant streams.
Requires: none
Helps: A1 (defined-entity events)
Size: M

### D3
To 3: Event- and request-triggered hooks; runtime dependency allowlist, timeouts, egress allowlist, resource limits; partner-deployable.
To 4: AI-authored hooks with a test harness, policy-gated, per-hook observability.
Requires: D2, I2
Size: M

# Pillar 2: Trust

### E1
To 3: Wire the accessibility scanners into CI as a blocking gate on every change class; enforce required accessible props in the component kit by lint or type.
To 4: Continuous scanning of deployed pages with automatic fix proposals through the proposal path; conformance report generated with human sign-off where the criterion needs judgment.
Requires: H3
Size: M

### E2
To 3: Record definition changes, configuration changes and approvals in the generic audit store; ship an admin audit UI with filters and retention.
To 4: Structured, exportable, tamper-evident audit events consumed by the advise loop (M1).
Requires: none
Size: S

### E3
To 3: Add a privacy classification to every field definition (none, personal, sensitive); drive operator-triggered export and erasure over every entity from it; retention policies per type; a verification report.
To 4: Automatic detection of untagged personal data with tagging proposals.
Requires: none
Helps: A2
Size: M

### E4
To 3: SAST, dependency and container scanning as blocking gates; authorisation verbs generated per defined type (view, create, edit, delete, manage) with role defaults; generic input validation from the definition.
To 4: Auto-remediation proposals for scan findings; runtime policy enforcement; incident findings become rules.
Requires: H3
Helps: A1 (generated authorisation)
Size: M

### F1
To 3: Version every customisation surface (definitions, layouts, text, theme, config) with history, diff and rollback in the admin UI.
To 4: Versions as addressable objects linked to proposals and evidence; automatic rollback on failed verification.
Requires: none
Size: M

### F2
To 3: A Proposal object: target kind, diff, rationale, evidence, preview reference, status, approver, applied version, rollback reference. Preview on a staging tenant using temporary overrides. Admin review queue.
To 4: Any actor including AI can create proposals; evidence attached automatically from checks.
Requires: F1
Size: M

### F3
To 3: A policy configuration per change class stating which classes auto-apply on passing checks and which need a named approver; approvals recorded in audit (E2).
To 4: Policy adapts to measured verifier false-pass rates; kill switch; spend and rate budgets.
Requires: F2, E2, H3
Size: M

### F4
To 3: Versioned extension contracts; automated compatibility checks in CI for plugins and definitions against the next release; migration tooling.
To 4: Backward compatibility guaranteed for definitions with automated migration proposals; breaking changes require a policy exception.
Requires: none
Helps: I1 (plugin contracts), A1 (definition contracts)
Size: M

### G1
To 3: Definition-driven index mappings (index mappings by field type) and a generic filler; all list and filter queries via the index; get-by-id via the store; caching.
To 4: Query plans derived from definitions with cost limits and observability.
Requires: A1, A2
Size: M

### G2
To 3: Per-tenant quotas and rate limits; noisy-neighbour detection; isolation verification tests.
To 4: Elastic per-tenant scaling under policy.
Requires: none
Size: M

### G3
To 3: Document limits per surface; performance suite in CI against budgets.
To 4: Continuous performance regression gating.
Requires: none
Size: S

### H1
To 3: Publish cross-layer contracts as artifacts (schema, hashes) so no layer reads another's source tree at build; independent deploy per layer off shared release trains.
To 4: Progressive delivery per layer with automatic rollback.
Requires: B3
Size: M

### H2
To 3: Architectural tests or lints on top of the dependency graph; explicit API contracts between modules.
To 4: Boundaries derived from definitions; violations blocked at PR with explanations.
Requires: none
Size: S

### H3
To 3: A named, mandatory check per change class (schema build, lint, unit, accessibility, security), run on drafts too; flake quarantine.
To 4: Checks generated from definitions and change class; evidence attached to proposals.
Requires: none. This is the cheapest high-leverage move on most products.
Size: S

# Pillar 3: Extend

### I1
To 3: Declarative plugin points (layout, forms, theme, text) alongside code plugin points (components, endpoints), documented.
To 4: Plugin points generated from definitions; registry or marketplace; versioned.
Requires: none
Size: M

### I2
To 3: Runtime isolation for plugin code (process or iframe boundary), runtime dependency enforcement, resource limits, egress control.
To 4: Per-plugin identity, quotas, observability, automatic disable on violation.
Requires: none
Size: M

### I3
To 3: Preview against a real tenant, staged branches, log access, validators.
To 4: Ephemeral preview environments per change with a test harness.
Requires: none
Helps: L2 (ephemeral previews for the level 4 move)
Size: S

### K1
To 3: A typed tool surface (MCP or equivalent) with scoped authentication; a capability map listing what the product can do.
To 4: Tools generated from definitions, including defined entities; capability map machine-readable and regenerated on publish.
Requires: B3
Helps: A1 (generated tools)
Size: M

### K2
To 3: A grounded conversational surface for end users with actions; natural-language authoring for operators over definitions, layouts and text, with preview.
To 4: Every UI action has a conversational equivalent from the same definitions; groundedness measured by an evaluation harness.
Requires: K1, C1, F2
Size: M

### K3
To 3: Scoped agent identities (not shared keys), idempotency keys on mutations, dry-run, rate limits, audit rows per action.
To 4: Policy-gated actions with kill switch, budgets, per-action risk classification.
Requires: E2, B3
Size: M

### N1
To 3: A canonical integration model per domain (person, case, message, organisation) and a configurable mapping layer, so a second connector is mapping configuration.
To 4: Mapping proposed by AI from the target system's schema and validated with a sample sync.
Requires: none
Helps: A1
Size: M

### N2
To 3: A connector definition or SDK covering authentication, sync, webhooks and lifecycle; admin install and configure; partner-buildable.
To 4: Connectors generated or assisted from the target API specification; certification; observability.
Requires: N1, D2
Size: M

### N3
To 3: Versioned contracts with deprecation windows; idempotent sync; conflict handling.
To 4: Contract tests both directions; compatibility by policy; replay.
Requires: B3
Size: S

### O1
To 3: Extract any missing neutral kernel primitive and move domain nouns above the kernel into definitions.
To 4: Kernel primitives themselves configurable.
Requires: A1
Size: L

### O2
To 3: Ship one adjacent domain as definitions plus connectors plus rules with the kernel unchanged, and prove it.
To 4: Multiple domains shipped as bundles.
Requires: A1, A3, D1, N2, O1
Size: L

### O3
To 3: A versioned bundle format for definitions, layouts, rules and connectors, installable to a tenant.
To 4: Bundles composable, upgradeable, AI-assembled from requirements.
Requires: A1, F1
Size: M

# Pillar 4: Evolve

### J1
To 3: Expose the event pipeline to platform features within minutes; instrument every feature at ship as a definition-of-done item.
To 4: Streaming with per-entity and per-definition instrumentation added automatically.
Requires: none
Size: M

### J2
To 3: Record feedback, ratings, corrections, evaluation outcomes and per-definition usage as typed signals linked to the definition and version they concern, with a triage workflow.
To 4: Auto-classification and linking to proposals.
Requires: none
Size: S

### J3
To 3: Join the product's own usage, feedback, errors and change history into queryable models inside the product.
To 4: Continuous mining producing candidate findings with provenance.
Requires: J1, J2
Size: M

### M1
To 3: Produce ranked, evidence-backed proposals to change the product's own behaviour or configured definitions, with expected impact, across the product.
To 4: Proposals carry definition diffs ready for the gate; post-apply impact measured.
Requires: J3, F2
Size: M

### M3
To 3: An AI authoring lane that turns accepted proposals into definition and layout changes and applies them wherever they apply, under policy.
To 4: Closed loop: propose, gate, apply, measure, learn, roll back.
Requires: A1, F2, F3, M1, M4
Size: L

### M4
To 3: Bind every applied proposal to a baseline, target metric, observation window and explicit keep, revise or rollback decision.
To 4: Generate instrumentation with the proposal and let policy use measured impact to promote, revise or reverse the change while recording attribution limits.
Requires: J1, F1, F2, L1
Size: M

### P1
To 3: A background review that runs after tasks or on idle, reads recent runs, and drafts candidate changes to skills, rules, prompts, memory or configuration without being asked; candidates go through the F2 proposal path.
To 4: Prioritise candidates by expected impact and track which kinds of change pass evaluation and stick.
Requires: J2
Helps: J1
Size: M

### P2
To 3: Evaluate every learned change against the current baseline on representative tasks or recorded data, and return pass, revise or block before apply.
To 4: Run the evaluation automatically with held-out data and feed pass rates into the F3 policy.
Requires: P1, F2
Size: M

### L1
To 3: A machine-readable build and version endpoint, health, and deployed-configuration snapshot.
To 4: Deployment events emitted; verification evidence attached automatically.
Requires: none. Usually the cheapest factory move.
Size: S

### L2
To 3: Ephemeral instance per change from a build id with seeded data, flags off first, destroyed after; tenant configuration behind an API rather than a hand-edited store.
To 4: Minutes to provision with production-shaped anonymised data and cost controls.
Requires: L1, H1
Size: L

### L3
To 3: Deterministic journeys across roles and devices, maintained and running; a changed-path to feature to journey map; per-feature adoption instrumentation at ship.
To 4: Journeys generated from definitions; verification evidence attached to proposals.
Requires: L1, L2, J1
Size: M
