# Evidence plan: what to look for, per capability

First settle scope: list every first-party repository that implements the product's core behaviour, and check the architecture docs for capabilities delegated elsewhere. Then declare the seven scope facts with evidence (`rubric.md`), because they decide which criteria apply.

Dispatch one read-only explorer per capability (six in parallel), or one per area for a deep pass. Give each explorer the repository path, the branch or tip, the criteria text from `rubric.md` for its capability, and these instructions:

- Report facts only, with file paths and short excerpts. No recommendations.
- Label every claim MEASURED (read in code at the named tip), DOCUMENTED (first-party doc or config) or NOT FOUND. Never infer silently.
- Say who can change each capability (engineer, professional services, admin, tenant) and whether a deploy is needed.
- Name the branch. A claim like "X does not exist" is branch-scoped.
- Distinguish an assessed absence from insufficient evidence. Record the inspected surface for either one.
- Recommend `not_applicable` only for exclusions listed for the declared archetype in `archetypes.md`, or where a false scope fact switches the criterion off; never because implementation is missing.
- Report the default setting of every capability. If it is off by default, say what turns it on.
- Say whether automated tests in scope exercise each capability (the tested facet), and whether there is any record of it working in production (the operated facet).
- For learning, intake, implementation and expansion criteria, say whose software the capability improves: the product itself (including what operators configure in it) or someone else's. Say whether any tooling involved is a supported first-party evolution system or a team's own CI and bots (rubric rule 12).

## Elastic: architecture (ARC)
- Data: query paths for lists and filters, index mappings, caching; migration framework, down steps, online or expand-and-contract tooling, migration tests in CI, how runtime definition changes reach storage.
- Scale: where sessions, caches, locks and files live; singletons and leader election; deployment manifests and replica counts; queue framework, retries, back-off, dead-lettering, idempotency, once-only scheduling; tenancy model, quotas, isolation tests.
- Capacity: load and performance suites, documented limits, CI budgets; metrics exported for core paths, published objectives, alert rules, error budgets.
- Resilience: for each connector, plugin lane, AI provider, tenant workload and internal service, its timeouts, retries, circuit breakers, bulkheads, fallbacks and fault-injection tests; backup and restore commands for data, definitions, files and secrets; restore tests; stated RPO and RTO; drill records.

## Velocity: delivery (DEL)
- Intake: request, feedback or feature-request objects; AI planners that ask clarifying questions; specifications with acceptance criteria, impact and risk class; who confirms them.
- Build: deployables and build coupling; dependency-graph enforcement and architectural tests; the AI implementation lane, what it can change (definitions or code), how its output arrives (proposal, pull request, direct apply) and with what verification evidence.
- Verify: CI coverage per change class; whether drafts skip CI; version and health endpoints; configuration snapshots; per-change environments and seed data; end-to-end journeys, path maps and adoption instrumentation.
- Release: feature flags, cohorts, per-tenant enablement, percentage rollouts and which change classes they cover; runtime kill switches; release rollback commands, data compatibility across releases, rollback tests, automatic triggers.

## Open: malleability (MAL)
- Data model: entity type registry, type enums, custom object tables, DDL or migration per type; field definitions and validation registries; relations and lifecycle states.
- APIs: hand-written controllers versus generated APIs; how the schema is assembled and when; introspection, OpenAPI, client codegen; dry-run or preview modes.
- Interface: layout or page files and their schema; designers; per-tenant overrides; preview; generic widgets; theme tokens, text storage and locales.
- Behaviour: rule, condition and action classes; event bus, webhooks, retry and replay; sandboxed hooks, allowlists, isolation and egress control.
- Extensions and integrations: plugin points, isolation, developer loop; canonical model and mapping; connector SDK and lifecycle; API versioning, deprecation, idempotent sync, conflict handling.
- Agent interface: MCP server or typed tool surface, its source and auth scoping; chat or assistant surfaces, grounding and natural-language authoring.

## Learn: learning (LRN)
- Sense: event pipeline and latency; feedback, ratings, corrections and per-definition usage; user-facing error capture tied to product areas; friction signals; joined stores and mining jobs.
- Diagnose and propose: failure grouping, attached context, reproduction and root-cause features; recommendation and proposal objects, ranking and evidence.
- Learn from experience: the self-modification checklist in `archetypes.md`; defaults; evaluation of learned changes against a baseline.
- Measure: baselines, target metrics, observation windows and keep, revise or rollback decisions bound to the applied change.

## Vet: governance (GOV)
- Compliance and security: accessibility kit and scanners, whether scans gate CI; audit coverage of definition changes and approvals; privacy classification, export, erasure, retention; permission model, validation, SAST, dependency and container scanning, and whether they block merges.
- Change control: version storage and rollback for each customisation surface (record the inventory); proposal objects, staging and preview; policy objects per change class, approvals, kill switch; extension contract versioning and upgrade compatibility checks.
- AI and self-change safety: agent identities, token scoping, idempotency, dry-run, rate limits; declared scopes, allow and deny lists, protected files and blast-radius limits for self-change; provenance on learned and AI-built changes; separation of untrusted input from instructions; injection scanning.

## Expand: expansion (EXP)
- Expressible: core entity names and where domain behaviour lives; any adjacent domain shipped as configuration; export and import of assets; templates and versioned bundles.
- Discover: failed-search and zero-result logs, unsupported requests to an assistant, feature-request objects, workaround signals (custom fields, exports, external tools); clustering into themes; adjacent-capability proposals with evidence and sizing.
- Launch: per-tenant or per-cohort enablement of new capabilities or bundles; early-access programmes; success metrics, review dates, removal paths and recorded keep-or-kill decisions.

## After the reports

Re-read every score of 3 or higher, and every critical-control criterion, against one primary source yourself before publishing. Explorer summaries are evidence pointers, not evidence.

Wherever the next level up is also defensible, record it as `alt_score`. For comparative work, run a second independent pass on at least the Learn, Vet and Expand criteria and report any criterion where the two passes differ.
