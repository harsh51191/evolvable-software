# Archetypes And Applicability

The MSR framework describes a broad software system. It should not force every product into one universal rank.

## Supported Archetypes

### Configurable application platform

A platform intended to let administrators define or reshape business objects, views, rules, integrations, and domain packs. Most change-surface criteria should be applicable.

### Agent runtime

A runtime focused on tools, memory, skills, planning, execution, and agent governance. Generic business-object and generic CRUD criteria may be outside its intended purpose. Governance, factory, learning, and agent-interface criteria remain central.

### Developer platform

A framework, SDK, infrastructure platform, or extensibility substrate primarily changed by developers. Admin self-service may be intentionally limited, but extension safety, contracts, verification, rollback, and factory surfaces remain applicable.

### Focused application

A product with a deliberately narrow domain or workflow. Universal entity and adjacent-domain expansion criteria may be inappropriate; safe configuration, evidence, operations, and change control can still be assessed.

### Other

Use only with a short description of the product's intended purpose and the applicability decision.

## Status Rules

- `assessed`: the criterion belongs to the product's intended surface. Use score 0 when evidence establishes absence.
- `not_evidenced`: the criterion appears applicable, but the available sources cannot establish presence or absence. It remains a zero for the current evidence-limited index and is counted as uncertainty.
- `not_applicable`: the criterion is outside the product's intended purpose. It is excluded from the relevant denominator and requires a concrete rationale.

Missing functionality is not a reason to use `not_applicable`. A low score is often the most useful assessment result.

## Profile Reading

Read the seven profiles before comparing the three aggregate indexes:

- **Change Surface:** schema, APIs, UI, behaviour, and domain definitions.
- **Governance:** security, audit, versioning, approval, rollback, and upgrade safety.
- **Factory:** modularity, environments, verification, and machine-readable release evidence.
- **Learning Loop:** observation, structured feedback, proposals, application, and impact measurement.
- **Agent Interface:** discoverable capabilities, identity, scopes, preview, and safe action semantics.
- **Extension Surface:** plugins and connectors.
- **Operational Scalability:** genericity, tenancy, limits, and measured ceilings.

Cross-product comparison is defensible only when scope, archetype, evidence grades, applicability decisions, and operational-validation depth are comparable.
