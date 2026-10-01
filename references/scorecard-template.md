# <Software> EVOLVE assessment

Assessment date. Evaluator. Declared archetype. Scope. Repositories and immutable tips. First-party documents used.

## Scope facts

| Fact | Value | Evidence |
|---|---|---|
| persistent_data | | |
| schema_changes | | |
| multi_tenant | | |
| hosted_service | | |
| agent_mutations | | |
| automatic_apply | | |
| code_release_path | | |

## Software Autonomy Level

Headline: **SAL n (name)** · Request → Release Ln · Issue → Fix Ln · Opportunity → Expansion Ln.

| Loop | Stages | Spine | Architecture | Governance | Level | With opt-in settings |
|---|---:|---:|---:|---:|---:|---:|
| Request → Release | | | | | | |
| Issue → Fix | | | | | | |
| Opportunity → Expansion | | | | | | |

Also report the headline with every alternate reading. A loop's level is the lowest of its four parts.

## Critical controls

| Control | Needs | Observed | Status |
|---|---|---|---|
| Definition rollback | | | |
| Release rollback | | | |
| Safe migrations | | | |
| Tested backup and restore | | | |
| Tenant isolation | | | |
| Security as infrastructure | | | |
| Bounded self-change | | | |

## What blocks the next level

For each loop, list every unmet condition for the next level, with the observed value.

## EVOLVE profile

| Capability | Default | Range with alternate readings | With opt-in settings | Assessed only |
|---|---:|---|---:|---:|
| Elastic (ARC) | | | | |
| Velocity (DEL) | | | | |
| Open (MAL) | | | | |
| Learn (LRN) | | | | |
| Vet (GOV) | | | | |
| Expand (EXP) | | | | |

## Evidence coverage

| Status | Count |
|---|---:|
| Assessed | |
| Not evidenced | |
| Not applicable | |

Explain every non-applicable decision, every scope fact that switched a criterion off, and the search scope behind every material uncertainty.

## Scorecard

Paste the tables printed by `scripts/score.py <assessment.json>`.

## Reading

Lead with the headline level and the part that holds it there. Then:

- Say what the product does by default and what its opt-in settings change.
- For learning, intake, implementation and expansion criteria, say whose software improves: the product itself, or software the product works on for its users. Record the second here; it is not scored.
- State the strongest evidenced capabilities, material zeros, uncertainties, non-applicable decisions, and every cap or deduction.
- Say whether the evidence establishes code presence, tested behaviour, operation in production, adoption or measured impact. Do not collapse these states.

## Prescription

When requested, paste the output of `scripts/score.py <assessment.json> --prescribe`. Start with what blocks the next level, then map planned work to the generated slices without scoring roadmap promises. Label projected scores as ceilings and re-estimate all relative sizes.

## Limits

State:

- branches read and evidence grades;
- sources not available;
- live-instance checks not performed;
- hosted-edition uncertainty;
- any claim that requires maintainer correction or operational validation.
