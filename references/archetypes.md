# Archetypes, Applicability And Interpretation

The MSR framework describes a broad class of software. It should not force every product into one universal rank. Choose one archetype, apply only its listed exclusions, and read the rubric through the interpretation notes below.

## Archetypes and their exclusions

The scorer enforces this table (it is the `archetype_exclusions` entry in the `msr-model` block of `rubric.md`). Excluding any other criterion is a validation error. Every exclusion needs a rationale, and should record `if_applicable`, the score it would have received, so reports can show what the exclusion changed.

| Archetype | Use for | May exclude |
|---|---|---|
| `configurable-application-platform` | Products whose operators define or reshape business objects, views, rules, integrations and domain packs | Nothing |
| `focused-application` | Products with a deliberately narrow domain or workflow | A1, A3, B1, B2, C2 (universal entity) and O1, O2, O3 (adjacent-domain expansion) |
| `agent-runtime` | Runtimes for tools, memory, skills, planning, execution and agent governance | A1, A2, A3, B1, B2, C2, G1 (generic business objects and CRUD) |
| `developer-platform` | Frameworks, SDKs and infrastructure changed mainly by developers | C1, C2, C3, E1, only when the product has no end-user interface |
| `other` | Anything else | Any criterion, with a rationale naming the product's purpose |

Missing functionality is never a reason to exclude. A low score is often the most useful result.

## Reading the rubric for agent runtimes

| Rubric term | Read it as |
|---|---|
| Definitions, customisation surfaces | Skills, memory, prompts and persona files, tool and permission policies, cron jobs, configuration |
| Operator, admin | The person or team running the agent |
| Tenant | A profile, workspace or installation |
| Proposal (F2) | A staged skill, memory or configuration change awaiting approval, or a pull request with evaluation evidence |
| Policy (F3) | Settings that decide per change class whether a self-modification applies automatically, needs approval, or is blocked |
| Learning signals (J2) | Per-skill usage and patch counts, corrections, ratings, evaluation outcomes |
| Learn from experience (P1, P2) | Background review, reflection or experience review that writes skills or memory, and any evaluation of those changes |

## Reading the rubric for developer platforms

A reviewed, validated declarative configuration path (for example configuration in version control that the product validates and previews) is a supported path and can reach level 3. Hand-edited files that nothing validates stay at level 2.

## Where self-modification usually lives

Search these before scoring F, J, M or P for any product that claims to learn or self-improve:

- skills, prompts, memory or rules directories written at runtime;
- background, reflection, experience or review jobs that run after tasks or on idle;
- curators, pruning, archival and restore commands;
- approval gates, staged or pending changes, ledgers, backups and rollback;
- evaluation hooks, datasets and baseline comparisons;
- first-party companion repositories (optimisers, evaluation harnesses, agent servers) named in the README or docs.

Record where you searched. In large repositories, list the directories read.

## Profile reading

Read the seven profiles before the four indexes:

- **Change Surface:** schema, APIs, UI, behaviour and domain definitions.
- **Governance:** security, audit, versioning, approval, rollback and upgrade safety.
- **Learning:** observation, structured signals, proposals, learning from experience and impact measurement.
- **Factory:** modularity, environments, verification and machine-readable release evidence.
- **Agent Interface:** discoverable capabilities, identity, scopes, preview and safe action semantics.
- **Extension Surface:** plugins and connectors.
- **Operational Scalability:** genericity, tenancy, limits and measured ceilings.

Cross-product comparison is defensible only when scope, archetype, evidence grades, exclusions and default-versus-available readings are comparable, and when the reported ranges are shown.
