# Archetypes, Applicability And Interpretation

EVOLVE describes a broad class of software. It should not force every product into one universal rank. Choose one archetype, declare the scope facts, apply only the exclusions they allow, and read the rubric through the interpretation notes below.

## Two ways a criterion stops applying

1. **Scope facts.** Some criteria only apply when a fact about the product is true (`applies_when` in the `evolve-model` block of `rubric.md`). When the fact is false, the criterion must be `not_applicable`, for any archetype:

   | Criterion | Applies when |
   |---|---|
   | ARC-01 query path, ARC-09 backup | `persistent_data` |
   | ARC-02 migrations | `schema_changes` |
   | ARC-03 scale, ARC-04 async work, ARC-06 capacity, ARC-07 objectives | `hosted_service` |
   | ARC-05 tenant isolation | `multi_tenant` |
   | DEL-11 release rollback | `code_release_path` |
   | GOV-10 bounded self-change, GOV-11 learning-input integrity | `agent_mutations` or `automatic_apply` |

2. **Archetype exclusions.** The scorer enforces this table. Excluding any other criterion is a validation error. Every exclusion needs a rationale, and should record `if_applicable`, the score it would have received, so reports can show what the exclusion changed.

| Archetype | Use for | May exclude |
|---|---|---|
| `configurable-application-platform` | Products whose operators define or reshape business objects, views, rules, integrations and domain packs | Nothing |
| `focused-application` | Products with a deliberately narrow domain or workflow | MAL-01, MAL-03, MAL-04, MAL-05, MAL-08 (universal entity) and EXP-01, EXP-02, EXP-03 (expressing adjacent domains) |
| `agent-runtime` | Runtimes for tools, memory, skills, planning, execution and agent governance | MAL-01 to MAL-05, MAL-08, ARC-01 (generic business objects and CRUD) |
| `developer-platform` | Frameworks, SDKs and infrastructure changed mainly by developers | MAL-07, MAL-08, MAL-09, GOV-01, only when the product has no end-user interface |
| `other` | Anything else | Any criterion, with a rationale naming the product's purpose |

Missing functionality is never a reason to exclude. A low score is often the most useful result.

A focused application may exclude EXP-01 to EXP-03, but never EXP-04 to EXP-06: even a narrow product should notice unmet demand. With EXP-02 excluded, its Opportunity → Expansion loop reaches L1 only through the implementation lane (DEL-04).

## Reading the rubric for agent runtimes

| Rubric term | Read it as |
|---|---|
| Definitions, customisation surfaces | Skills, memory, prompts and persona files, tool and permission policies, cron jobs, configuration |
| Operator, admin | The person or team running the agent |
| Tenant | A profile, workspace or installation |
| Request intake (DEL-01) | A command or flow that turns a request into a reviewable skill or configuration draft |
| Proposal (GOV-06) | A staged skill, memory or configuration change awaiting approval, or a pull request with evaluation evidence |
| Policy (GOV-07) | Settings that decide per change class whether a self-modification applies automatically, needs approval or is blocked |
| Bounds (GOV-10) | Protected files, allow and deny lists, size, rate and scope limits on what the agent may change in itself |
| Learning signals (LRN-02) | Per-skill usage and patch counts, corrections, ratings, evaluation outcomes |
| Learn from experience (LRN-07, LRN-08) | Background review, reflection or experience review that writes skills or memory, and any evaluation of those changes |

## Reading the rubric for developer platforms

A reviewed, validated declarative configuration path (for example configuration in version control that the product validates and previews) is a supported path and can reach level 3. Hand-edited files that nothing validates stay at level 2.

## Where self-modification usually lives

Search these before scoring the Learn and Vet criteria for any product that claims to learn or self-improve:

- skills, prompts, memory or rules directories written at runtime;
- background, reflection, experience or review jobs that run after tasks or on idle;
- curators, pruning, archival and restore commands;
- approval gates, staged or pending changes, ledgers, backups and rollback;
- allow and deny lists, protected files, rate limits and provenance records on changes;
- evaluation hooks, datasets and baseline comparisons;
- first-party companion repositories (optimisers, evaluation harnesses, agent servers, automation services) named in the README or docs.

Record where you searched. In large repositories, list the directories read.

## Reading a result

Read the loop levels first, then the parts that hold each loop at its level, then the critical controls, then the profile:

- **Stages** are what the loop itself needs: intake for requests; detection, diagnosis and proposals for fixes; sensing, proposals and launch for expansion.
- **Spine** is the shared release path: build, verify, stage, release, observe, roll back.
- **Architecture** is the foundation: every applicable ARC criterion must reach the level's threshold.
- **Governance** is the ceiling: compliance, review, policy and bounds on self-change.

Cross-product comparison is defensible only when scope, archetype, scope facts, evidence depth, exclusions and default-versus-available readings are comparable, and when the reported ranges are shown.
