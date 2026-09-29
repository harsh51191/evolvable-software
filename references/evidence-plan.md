# Evidence plan: what to look for, per pillar

Dispatch one read-only explorer per pillar (four in parallel), or one per dimension for a deep pass. Give each explorer the repository path, the branch or tip, the criteria text from `rubric.md` for its dimensions, and these instructions:

- Report facts only, with file paths and short excerpts. No recommendations.
- Label every claim MEASURED (read in code at the named tip), DOCUMENTED (first-party doc or config) or NOT FOUND. Never infer silently.
- Say who can change each capability (engineer, professional services, admin, tenant) and whether a deploy is needed.
- Name the branch. A claim like "X does not exist" is branch-scoped.
- Distinguish an assessed absence from insufficient evidence. Record the inspected surface for either one.
- Recommend `not_applicable` only when the criterion falls outside the declared product archetype, never because implementation is missing.

## Pillar 1: Define (A, B, C, D)
- Entity type registry: grep for type enums, `EntityType`, content type tables, "custom object", DDL or migration per type.
- Field definitions: custom field types, validation registries, PII or sensitivity tags and their consumers.
- Relations and states: association tables, workflow or state tables, per-feature state enums.
- API: count hand-written resolvers, controllers or schema registries; how the schema is assembled and when; introspection, OpenAPI, client codegen; dry-run or preview modes.
- Layout: layout or page files and their schema; page designer; per-tenant override storage; preview.
- Generic rendering: forms from spec; generic field display; any list or detail component parameterised by type.
- Theme and text: token definitions and serving; theme editor; text storage; locale count; tenant override UI; translation pipeline.
- Rules: rule, condition and action classes; admin UI; scope.
- Events: bus, listeners, webhook manager, retry queue, replay.
- Hooks: custom endpoint or hook framework; trigger types; allowlists; isolation; egress control.

## Pillar 2: Trust (E, F, G, H)
- Accessibility: component kit, token usage share, scanners, whether scans gate CI, required accessible props, conformance reports.
- Audit: audit table or service, coverage, admin UI, config and definition changes recorded.
- GDPR: erasure and export services and their entity coverage; privacy tags; retention; admin triggers.
- Security: permission model and how permissions are declared; validation framework; SAST, dependency and container scanning; whether scans block merges; recent security findings and reverted mitigations.
- Versioning: version storage per customisation surface; diff and history UI; rollback.
- Proposals: any proposal or change-request object; stage and publish; preview on staging data.
- Policy: auto-apply classes; approval records; kill switch.
- Upgrade safety: extension contract versioning; compatibility checks; history of customisations breaking on upgrade.
- Performance: index mappings; filterability of generic fields; caching; tenancy model; quotas; load tests; performance incident history.
- Stack: deployables and build coupling; containerisation; release trains; dependency-graph enforcement; architectural tests; CI coverage per change class; whether drafts skip CI; incidents that passed CI.

## Pillar 3: Extend (I, K, N, O)
- Plugins: SDK or plugin docs; plugin point types; declarative versus code; where plugin code executes; allowlists and when enforced; preview tooling, staging branches, logs, validators.
- Agents: MCP server; tool definitions and their source; capability map; chat or assistant surfaces and grounding; admin natural-language authoring; API identity model, token scoping, idempotency, dry-run, rate limits.
- Connectors: canonical model; mapping configuration; how existing integrations were built; connector SDK; lifecycle; API versioning and deprecation; idempotent sync; conflict handling.
- Domains: core entity names; where domain behaviour lives; channel concept; any adjacent domain shipped as configuration; export and import of assets; templates or bundles.

## Pillar 4: Evolve (J, M, L)
- Telemetry: event pipeline and latency; consumers inside the product; per-feature instrumentation.
- Feedback: feedback types; linking to entities; triage; closure loop.
- Mining: data lake or warehouse and what it joins; mining jobs; findings surfaced in product.
- Advise: recommendation features; proposal objects; ranking; process recommendations; AI authoring lane and its scope; cross-tenant application; baseline, observation window and proposal-to-impact linkage.
- Factory: version or build endpoint; health; config snapshot; instance provisioning tooling and time; seed data; configuration source and access; end-to-end suites and their state; path-to-journey mapping; adoption instrumentation coverage.

## After the reports
Re-read every score of 3 or higher against one primary source yourself before publishing. Explorer summaries are evidence pointers, not evidence.
