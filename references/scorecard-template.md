# <Software> MSR assessment

Assessment date. Evaluator. Declared archetype. Scope. Repositories and immutable tips. First-party documents used.

## Evidence Coverage

| Status | Count |
|---|---:|
| Assessed | |
| Not evidenced | |
| Not applicable | |

Explain every non-applicable decision and the search scope behind every material uncertainty.

## Indexes

| Index | Default | Band | Range with alternate readings | With opt-in settings |
|---|---:|---|---|---:|
| Malleability | | | | |
| Governance | | | | |
| Learning | | | | |
| Factory | | | | |

Report the range whenever alternate readings exist. Report the opt-in column whenever a shipped but off-by-default setting changes a score.

## Profile

| Profile | Default | With opt-in settings |
|---|---:|---:|
| Change Surface | | |
| Governance | | |
| Learning | | |
| Factory | | |
| Agent Interface | | |
| Extension Surface | | |
| Operational Scalability | | |

## Closed Loop

Closed-loop candidate by default: yes or no. With opt-in settings: yes or no. List every failing stage (observe, propose, review, gate, apply and roll back, measure, verify). This is a minimum-mechanism signal, not a production-readiness or outcome claim.

## Scorecard

Paste the table printed by `scripts/score.py <scores.json>`.

## Reading

Lead with the largest blocker. Say what the product does by default and what its opt-in settings change. For Learning criteria, say whose software improves: the product itself, or software the product works on for its users (recorded here, not scored). Then state the strongest evidenced capabilities, material zeros, uncertainties, non-applicable decisions, and every cap or incident deduction. Explain whether the evidence establishes code presence, operational usability, adoption, or measured impact; do not collapse these states.

## Prescription

When requested, paste the output of `scripts/score.py <scores.json> --prescribe`. Map planned work to the generated slices without scoring roadmap promises. Label projected indexes as ceilings and re-estimate all relative sizes.

## Limits

State branches read, evidence grades, sources not available, live-instance checks not performed, hosted-edition uncertainty, and any claim that requires maintainer correction or operational validation.
