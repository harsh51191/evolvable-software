# EVOLVE Rubric: criteria, anchored levels and scoring model

This file is the single source of truth for the EVOLVE framework. `scripts/score.py` reads the criterion ids, capabilities and areas from the headings below, and reads the scoring model (scope facts, applicability, loop conditions, critical controls, depth rules, archetype exclusions and caps) from the `evolve-model` block in this preamble. Change any of them here, nowhere else.

EVOLVE answers one question: **how ready is a software product to evolve itself safely?** It reports a Software Autonomy Level (SAL) for three loops (Request → Release, Issue → Fix, Opportunity → Expansion) and a profile of six capabilities: **E**lastic (architecture, `ARC`), **V**elocity (delivery, `DEL`), **O**pen (malleability, `MAL`), **L**earn (learning, `LRN`), **V**et (governance, `GOV`) and **E**xpand (expansion, `EXP`). `spec/evolve-v0.4-draft.md` explains the design and why each piece exists.

Every criterion has a definition, why it matters, evidence to look for, and one anchored description per level 0 to 4. Levels are cumulative: a level includes the substance of the levels below it. Score the level whose description the evidence supports in full. If the evidence sits between two levels, score the lower one and record the higher one as `alt_score`.

## General maturity ladder

| Level | Meaning |
|---|---|
| 0 | Absent. |
| 1 | Code-only. Engineers change code and ship a release. |
| 2 | Mechanism. A runtime mechanism exists, reachable by engineers through files, git, config or API, without validation or a supported path for the product's operator. |
| 3 | Productised. The product's operator does it through a supported, validated path with no deploy: a UI, a first-party CLI command, a conversational command the product handles, or reviewed declarative configuration the product validates. |
| 4 | Generative and policy-gated. Machine-readable definitions an AI can author through a supported path, validated before they take effect, with a policy that decides whether a human is needed, and rollback. |

The ladder reads most naturally for the Open criteria. Architecture, delivery and compliance criteria give their own anchors; read those as written. For GOV-01 to GOV-04 the ladder reads: 0 no audit, 1 manual audit, 2 automated scan on demand, 3 scan wired as a gate on every change, 4 continuous scan plus automatic fix proposals through the change path.

**Who the operator is.** For a multi-user platform, the in-product administrator. For a developer platform or a single-user agent runtime, the person who runs it. Hand-editing a file the product does not validate stays at level 2. The ladder measures how governed and supported a change path is, not whether it has a graphical UI.

**What "tenant" means.** The unit of isolation: a tenant, workspace, site or project, or the installation itself for single-tenant products.

**What "customisation surface" and "definition" mean.** Anything the operator changes to shape behaviour without a code release: entity and field definitions, layouts, rules, workflows, apps, and for agents their skills, memory, prompts, tool policies and configuration.

**What "AI-authorable" means.** The definition has a documented machine-readable form, and the product exposes a path (tool, API or conversational command) that creates or changes it with structured validation errors. Storing JSON somewhere is not enough.

## Evidence grades

**A** code-verified in the repository at a named tip. **B** verified from first-party documentation, audits or configuration in hand. **C** inferred from product knowledge or secondary material; a C-graded score is capped at 2.

## Evidence status

- **assessed** means the criterion was evaluated and can be assigned an anchored score. Use score 0 when primary evidence establishes absence.
- **not_evidenced** means the criterion appears applicable but the inspected sources could not establish presence or absence. It scores 0 by default, is excluded from the assessed-only reading, and is reported as uncertainty.
- **not_applicable** means the criterion is outside the product's archetype, or a scope fact switches it off. Only the exclusions in the model below are accepted. It is excluded from the denominator, passes any level condition that names it, and requires a specific rationale.

Read `archetypes.md` before scoring. Missing functionality is not non-applicability.

## Scope facts

Every assessment declares nine facts, each with evidence, for the default configuration. They decide which criteria and critical controls apply, so a stateless library is not failed on backups and a single-user tool is not failed on tenant isolation. A fact that is wrongly declared is a validation finding, not a shortcut.

| Fact | True when |
|---|---|
| `persistent_data` | The product stores durable user, tenant or operator data |
| `schema_changes` | The product, or its evolution path, changes stored data structures (database schema or definition-driven storage) |
| `multi_tenant` | One deployment serves several isolated tenants, workspaces or organisations |
| `hosted_service` | It runs as a long-lived networked service rather than a library, CLI or local single-user tool |
| `machine_actions` | Agents or automated clients can change the product's data or definitions through an API or tool surface |
| `agent_mutations` | The product's own agents or AI can change its definitions, skills, memory, configuration or data |
| `evolution_auto_apply` | A change produced by the evolution loop (an AI lane, a learning loop or self-modification) applies without human approval by default. Scheduled maintenance such as index or column tuning does not count |
| `definition_change_path` | Changes to the product's behaviour are made through definitions or configuration, by people or by the product |
| `code_release_path` | The product's evolution system ships code changes, not only definition changes |

At least one change path (`definition_change_path` or `code_release_path`) must be true. Rollback is required on each path that exists: GOV-05 for definition changes, DEL-11 for code changes, both when both exist.

## Scoring rules

1. Score what ships today, not the roadmap. Features in the repository but disabled behind a beta flag still ship.
2. **Score the default configuration.** `score` is the level in a standard installation with required credentials supplied. If an opt-in setting, beta flag or plugin that ships with the product raises the level, record that as `available_score`. The scorer reports both.
3. **Scope includes first-party companions.** Assess every first-party repository that implements the product's core behaviour. When the assessed repository delegates a capability to another repository, assess it there, or mark it `not_evidenced` and name where it lives.
4. **Self, not others.** Learning criteria, DEL-01, DEL-04 and EXP-04 to EXP-06 credit changes to the assessed product's own behaviour, including behaviour its operators configure in it (apps, workflows, skills, rules). Improvements the product makes to other software, such as pull requests against a customer's repository, are recorded in the reading but not scored.
5. Every assessed criterion cites evidence, including the inspected surface for an assessed 0.
6. A capability that exists for one entity family only scores at most 2 (`single_entity: true`).
7. A capability that has caused a production incident in the last 12 months loses one point (`incident: true`, with the incident cited in the evidence).
8. Criteria are integers. Area means and capability scores are computed from unrounded values and rounded half up to one decimal only for display.
9. Compliance and security are scored on whether they are structural and continuously verified. The latest audit result is an input, never a score.
10. Name the branch or tip the evidence was read from. A claim is branch-scoped until proven otherwise.
11. **Alternates are upward only.** `alt_score` is always `score + 1`: the higher reading that is also defensible. The default reading is therefore the low end of every range.
12. **Repository tooling counts only as a first-party evolution system.** For DEL-01, DEL-04, DEL-09 to DEL-11, LRN-03, LRN-05 to LRN-07 and EXP-04 to EXP-06, tooling counts only when it is executable, supported (documented and maintained as part of the product or an official first-party companion), bounded (subject to GOV-10 limits) and built to evolve this product from its requests, issues or opportunities. A team's ordinary CI, bots or scripts do not qualify; they still count for DEL-05 to DEL-08.
13. **Evidence facets and the depth cap.** For depth-capped criteria (every ARC criterion and every critical-control criterion), any score, alternate or opt-in reading of 3 or more records `facets`: `implemented`, `tested` (automated tests in scope exercise it) and `operated` (records show it working in production). `tested` and `operated` each require `implemented`, and are recorded separately so operated evidence never implies tested. A 3 needs `tested`, otherwise it counts as 2. A 4 needs `tested` and `operated`, otherwise it counts as 3 if tested and 2 if not.
14. **Coverage inventories.** ARC-08, ARC-09 and GOV-05 span several surfaces. When any reading (score, alternate or opt-in) is 3 or more, record `inventory`, a level per applicable surface; no reading of 3 or more can exceed the lowest of them, so one strong surface cannot hide a weak one. Below 3 the anchors already describe partial coverage, and an inventory is optional.

## Software Autonomy Levels

| Level | Name | What the product can do in a loop |
|---|---|---|
| L0 | Manual | Every change is engineers writing and releasing code. |
| L1 | Configurable | People make the change without bespoke engineering, through governed configuration or an AI-drafted change they finish, and can roll it back. |
| L2 | Assisted | The product structures the request, diagnoses the issue or drafts the proposal, and drafts the change. People build, check and release. |
| L3 | Supervised | The product carries the loop end to end, including verification, staged release and rollback. A person approves each release. Every applicable critical control passes. |
| L4 | Policy-bounded | Low-risk change classes ship without a person, under policy, with staged exposure, impact measurement and automatic rollback, on an architecture with tested evidence. |
| L5 | Self-directing | Across change classes, the product initiates, ships and measures change within policy, backed by operational evidence. |

A loop's level is the highest level whose conditions, and every lower level's conditions, all hold. The conditions fall into four parts: the loop's own **stages**, the shared **release spine** (Build, Verify, Stage, Release, Observe, Roll back), the **architecture** foundation and the **governance** ceiling, so the level is the lowest of the four. **Headline SAL** is the lower of Request → Release and Issue → Fix; Opportunity → Expansion is reported beside it. Critical controls are L3 conditions, so failing an applicable one caps every loop at L2.

In the conditions below, `path` is the loop's build path: the criteria through which people (`people`) or the product (`product`) build a change. `rollback` is the lower of GOV-05 when `definition_change_path` is true and DEL-11 when `code_release_path` is true. `every` applies a threshold to every applicable criterion of a capability. `operated` requires the operated facet.

## Scoring model

```json evolve-model
{
  "framework": "EVOLVE",
  "version": "0.4.0",
  "capabilities": {
    "ARC": "Elastic",
    "DEL": "Velocity",
    "MAL": "Open",
    "LRN": "Learn",
    "GOV": "Vet",
    "EXP": "Expand"
  },
  "scope_facts": [
    "persistent_data",
    "schema_changes",
    "multi_tenant",
    "hosted_service",
    "machine_actions",
    "agent_mutations",
    "evolution_auto_apply",
    "definition_change_path",
    "code_release_path"
  ],
  "change_path_facts": [
    "definition_change_path",
    "code_release_path"
  ],
  "applies_when": {
    "ARC-01": "persistent_data",
    "ARC-02": "schema_changes",
    "ARC-03": "hosted_service",
    "ARC-04": "hosted_service",
    "ARC-05": "multi_tenant",
    "ARC-06": "hosted_service",
    "ARC-07": "hosted_service",
    "ARC-09": "persistent_data",
    "DEL-11": "code_release_path",
    "GOV-05": "definition_change_path",
    "GOV-09": "machine_actions",
    "GOV-10": ["agent_mutations", "evolution_auto_apply"],
    "GOV-11": ["agent_mutations", "evolution_auto_apply"]
  },
  "depth_capped": [
    "ARC-01",
    "ARC-02",
    "ARC-03",
    "ARC-04",
    "ARC-05",
    "ARC-06",
    "ARC-07",
    "ARC-08",
    "ARC-09",
    "GOV-04",
    "GOV-05",
    "GOV-10",
    "LRN-08",
    "DEL-11"
  ],
  "inventories": {
    "ARC-08": [
      "connectors",
      "plugins",
      "ai_providers",
      "tenant_workloads",
      "internal_services"
    ],
    "ARC-09": [
      "data",
      "definitions",
      "files",
      "secrets"
    ],
    "GOV-05": null
  },
  "levels": [
    "Manual",
    "Configurable",
    "Assisted",
    "Supervised",
    "Policy-bounded",
    "Self-directing"
  ],
  "loops": {
    "request": "Request → Release",
    "fix": "Issue → Fix",
    "expansion": "Opportunity → Expansion"
  },
  "headline": [
    "request",
    "fix"
  ],
  "build_paths": {
    "request": {
      "people": [
        {
          "cap": "MAL"
        }
      ],
      "product": [
        {
          "c": "DEL-04"
        }
      ]
    },
    "fix": {
      "people": [
        {
          "cap": "MAL"
        }
      ],
      "product": [
        {
          "c": "DEL-04"
        },
        {
          "c": "LRN-07",
          "with": {
            "c": "LRN-08",
            "min": 2
          }
        }
      ]
    },
    "expansion": {
      "people": [
        {
          "c": "EXP-02"
        }
      ],
      "product": [
        {
          "c": "DEL-04"
        },
        {
          "c": "EXP-03"
        }
      ]
    }
  },
  "rollback": [
    {
      "c": "GOV-05",
      "when": "definition_change_path"
    },
    {
      "c": "DEL-11",
      "when": "code_release_path"
    }
  ],
  "archetype_exclusions": {
    "configurable-application-platform": [],
    "focused-application": [
      "MAL-01",
      "MAL-03",
      "MAL-04",
      "MAL-05",
      "MAL-08",
      "EXP-01",
      "EXP-02",
      "EXP-03"
    ],
    "agent-runtime": [
      "MAL-01",
      "MAL-02",
      "MAL-03",
      "MAL-04",
      "MAL-05",
      "MAL-08",
      "ARC-01"
    ],
    "developer-platform": [
      "MAL-07",
      "MAL-08",
      "MAL-09",
      "GOV-01"
    ],
    "other": "*"
  },
  "caps": {
    "grade_c_max": 2,
    "single_entity_max": 2,
    "incident_penalty": 1
  },
  "conditions": {
    "1": [
      {"part": "spine", "stage": "Build", "any": [{"path": "people", "min": 2}, {"path": "product", "min": 2}]},
      {"part": "spine", "stage": "Roll back", "rollback": 2},
      {"part": "stages", "stage": "Detect", "loop": "fix", "c": "LRN-03", "min": 2}
    ],
    "2": [
      {"part": "spine", "stage": "Build", "path": "product", "min": 2},
      {"part": "spine", "stage": "Verify", "c": "DEL-05", "min": 2},
      {"part": "stages", "stage": "Intake", "loop": "request", "c": "DEL-01", "min": 2},
      {"part": "stages", "stage": "Diagnose", "loop": "fix", "c": "LRN-05", "min": 2},
      {"part": "stages", "stage": "Propose", "loop": "fix", "c": "LRN-06", "min": 2},
      {"part": "stages", "stage": "Sense", "loop": "expansion", "c": "EXP-04", "min": 2},
      {"part": "stages", "stage": "Propose", "loop": "expansion", "c": "EXP-05", "min": 2},
      {"part": "architecture", "stage": "Foundation", "every": "ARC", "min": 1}
    ],
    "3": [
      {"part": "spine", "stage": "Build", "path": "product", "min": 3},
      {"part": "spine", "stage": "Verify", "c": "DEL-05", "min": 3},
      {"part": "spine", "stage": "Verify", "c": "DEL-06", "min": 3},
      {"part": "spine", "stage": "Verify", "c": "DEL-07", "min": 2},
      {"part": "spine", "stage": "Verify", "c": "DEL-08", "min": 2},
      {"part": "spine", "stage": "Stage", "c": "DEL-09", "min": 2},
      {"part": "spine", "stage": "Release", "c": "DEL-10", "min": 2},
      {"part": "spine", "stage": "Observe", "c": "LRN-09", "min": 2},
      {"part": "spine", "stage": "Roll back", "control": "Definition rollback", "c": "GOV-05", "min": 3},
      {"part": "spine", "stage": "Roll back", "control": "Release rollback", "c": "DEL-11", "min": 3},
      {"part": "stages", "stage": "Intake", "loop": "request", "c": "DEL-01", "min": 3},
      {"part": "stages", "stage": "Detect", "loop": "fix", "c": "LRN-03", "min": 3},
      {"part": "stages", "stage": "Diagnose", "loop": "fix", "c": "LRN-05", "min": 3},
      {"part": "stages", "stage": "Propose", "loop": "fix", "c": "LRN-06", "min": 3},
      {"part": "stages", "stage": "Sense", "loop": "expansion", "c": "EXP-04", "min": 3},
      {"part": "stages", "stage": "Propose", "loop": "expansion", "c": "EXP-05", "min": 3},
      {"part": "stages", "stage": "Launch", "loop": "expansion", "c": "EXP-06", "min": 2},
      {"part": "architecture", "stage": "Foundation", "every": "ARC", "min": 2},
      {"part": "architecture", "stage": "Foundation", "control": "Safe migrations", "c": "ARC-02", "min": 3},
      {"part": "architecture", "stage": "Foundation", "control": "Tested backup and restore", "c": "ARC-09", "min": 3},
      {"part": "architecture", "stage": "Foundation", "control": "Tenant isolation", "c": "ARC-05", "min": 3},
      {"part": "governance", "stage": "Ceiling", "control": "Security as infrastructure", "c": "GOV-04", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-02", "min": 2},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-06", "min": 2},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-08", "min": 2},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-09", "min": 2},
      {"part": "governance", "stage": "Ceiling", "control": "Bounded self-change", "when": ["agent_mutations", "evolution_auto_apply"], "all": [{"c": "GOV-10", "min": 3}, {"c": "LRN-08", "min": 2}]}
    ],
    "4": [
      {"part": "spine", "stage": "Build", "path": "product", "min": 3},
      {"part": "spine", "stage": "Build", "c": "DEL-02", "min": 2},
      {"part": "spine", "stage": "Build", "c": "DEL-03", "min": 2},
      {"part": "spine", "stage": "Verify", "c": "DEL-05", "min": 3},
      {"part": "spine", "stage": "Verify", "c": "DEL-06", "min": 3},
      {"part": "spine", "stage": "Verify", "c": "DEL-07", "min": 3},
      {"part": "spine", "stage": "Verify", "c": "DEL-08", "min": 3},
      {"part": "spine", "stage": "Stage", "c": "DEL-09", "min": 3},
      {"part": "spine", "stage": "Release", "c": "DEL-10", "min": 3},
      {"part": "spine", "stage": "Observe", "c": "LRN-09", "min": 3},
      {"part": "spine", "stage": "Roll back", "rollback": 4},
      {"part": "stages", "stage": "Launch", "loop": "expansion", "c": "EXP-06", "min": 3},
      {"part": "architecture", "stage": "Foundation", "every": "ARC", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-01", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-02", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-03", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-04", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-07", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-09", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-10", "min": 3},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-11", "min": 3}
    ],
    "5": [
      {"part": "spine", "stage": "Build", "path": "product", "min": 4},
      {"part": "spine", "stage": "Verify", "c": "DEL-05", "min": 4},
      {"part": "spine", "stage": "Verify", "c": "DEL-06", "min": 4},
      {"part": "spine", "stage": "Verify", "c": "DEL-07", "min": 4},
      {"part": "spine", "stage": "Verify", "c": "DEL-08", "min": 4},
      {"part": "spine", "stage": "Stage", "c": "DEL-09", "min": 4},
      {"part": "spine", "stage": "Release", "c": "DEL-10", "min": 4},
      {"part": "spine", "stage": "Observe", "c": "LRN-09", "min": 4, "operated": true},
      {"part": "spine", "stage": "Roll back", "rollback": 4, "operated": true},
      {"part": "stages", "stage": "Intake", "loop": "request", "c": "DEL-01", "min": 4},
      {"part": "stages", "stage": "Detect", "loop": "fix", "c": "LRN-03", "min": 4},
      {"part": "stages", "stage": "Diagnose", "loop": "fix", "c": "LRN-05", "min": 4},
      {"part": "stages", "stage": "Propose", "loop": "fix", "c": "LRN-06", "min": 4},
      {"part": "stages", "stage": "Sense", "loop": "expansion", "c": "EXP-04", "min": 4},
      {"part": "stages", "stage": "Propose", "loop": "expansion", "c": "EXP-05", "min": 4},
      {"part": "stages", "stage": "Launch", "loop": "expansion", "c": "EXP-06", "min": 4},
      {"part": "architecture", "stage": "Foundation", "every": "ARC", "min": 3, "operated": true},
      {"part": "architecture", "stage": "Foundation", "c": "ARC-06", "min": 4},
      {"part": "architecture", "stage": "Foundation", "c": "ARC-07", "min": 4},
      {"part": "architecture", "stage": "Foundation", "c": "ARC-08", "min": 4},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-07", "min": 4, "operated": true},
      {"part": "governance", "stage": "Ceiling", "c": "GOV-10", "min": 4, "operated": true}
    ]
  }
}
```

---

# Capability ARC: Elastic (architecture)

Can the product take the load and survive the change?

## Area: Data

### ARC-01 Indexed query path, never a scan of a generic store
**Definition.** Lists and filters over generic or defined entities go through an index; get-by-id goes to the store; caching is in place.
**Why it matters.** Generic storage is the classic performance trap of metadata platforms.
**Evidence.** Search index and mappings. Whether custom or defined fields are filterable at scale. Query paths for lists. Caching layers.
- **0** No index; scans.
- **1** Relational queries hand-tuned per feature.
- **2** Search index exists; generic or custom fields not filterable at scale.
- **3** Definitions drive index mappings; lists via index; caching.
- **4** Query plans derived from definitions with cost limits and observability.

### ARC-02 Safe schema and data migrations
**Definition.** Changes to stored data structures, including changes the product makes to its own definitions at runtime, run without downtime or data loss and can be reversed.
**Why it matters.** Every evolution loop eventually changes data shape. A migration that locks a table or drops a column is the most common way a small change becomes an outage.
**Evidence.** Migration framework and its down steps. CI jobs that run migrations against data. Online or expand-and-contract tooling. How runtime definition changes reach storage.
- **0** Schema changes are manual SQL or ad-hoc scripts.
- **1** Versioned migration files applied by engineers; no rollback path or online strategy.
- **2** Migration framework with up and down steps; locking or long-running changes handled by convention.
- **3** Migrations tested in CI against representative data; destructive changes use expand-and-contract or another online strategy enforced by tooling; definition changes made at runtime are migrated by the same mechanism.
- **4** The product plans, previews and validates migrations for AI-authored or self-made changes, refuses unsafe ones by policy, and can reverse them automatically.

## Area: Scale

### ARC-03 Horizontal scale of services
**Definition.** Serving capacity grows by adding instances, because services keep shared state in managed stores rather than in process memory or local disk.
**Why it matters.** A product that can only scale up hits a hard ceiling exactly when an evolution loop starts adding load.
**Evidence.** Session, cache, file and lock storage. Deployment manifests with replica counts. Documented scale-out guidance. Singletons and leader election.
- **0** A single process that holds state in memory or on local disk.
- **1** Multiple instances possible only with sticky sessions or manual coordination.
- **2** Multiple instances supported, with documented caveats (local caches, singletons, file storage).
- **3** Stateless services by design: shared state in managed stores, scale-out documented and exercised by tests or deployment manifests.
- **4** Services scale automatically on load signals, with scale-out behaviour verified in a performance environment.

### ARC-04 Reliable asynchronous work
**Definition.** Long or deferred work runs on queues with retries, idempotency and visibility, not in the request path.
**Why it matters.** Learning jobs, migrations, syncs and AI calls are long-running. Without reliable queues they either block users or silently fail.
**Evidence.** Queue or job framework. Retry and back-off settings. Dead-letter handling. Idempotency keys. Scheduler behaviour across instances.
- **0** Long work runs in the request path.
- **1** Background work is ad hoc (threads, cron inside the web process).
- **2** A job queue with retries.
- **3** Queued work is idempotent, retried with back-off, dead-lettered and observable; scheduled jobs run once across instances.
- **4** Per-tenant fairness and priorities in the queues, with back-pressure under load.

### ARC-05 Tenant isolation and noisy-neighbour controls
**Definition.** Tenants cannot degrade or read each other; per-tenant limits exist.
**Why it matters.** Malleable tenants generate unpredictable load.
**Evidence.** Tenancy model. Quotas. Isolation verification. Autoscaling per tenant.
- **0** None.
- **1** Shared without controls.
- **2** Shared with basic quotas, or single-tenant per deployment.
- **3** Per-tenant limits, noisy-neighbour detection, data isolation verified.
- **4** Elastic per-tenant scaling governed by policy.

## Area: Capacity

### ARC-06 Ceilings measured, not discovered in incidents
**Definition.** Scalability limits per surface are measured, documented and regression-tested.
**Why it matters.** Unknown ceilings become customer-found incidents.
**Evidence.** Load or performance suites. Documented limits. Incident history of performance failures.
- **0** Unknown.
- **1** Discovered in incidents.
- **2** Some load tests.
- **3** Documented limits per surface with a performance suite in CI.
- **4** Continuous performance regression gating against budgets.

### ARC-07 Service objectives defined and monitored
**Definition.** Core paths have published objectives for latency, availability or throughput, monitored with alerts.
**Why it matters.** An autonomous release can only be judged safe against an objective. Without one, "healthy" is whatever the last incident said.
**Evidence.** Published objectives. Metrics exported for core paths. Alert rules. Error budgets and how releases use them.
- **0** None.
- **1** Uptime checks only.
- **2** Latency or error metrics exported for core paths; no stated objectives.
- **3** Published objectives (latency, availability or throughput) for core paths, monitored with alerts.
- **4** Objectives and error budgets feed release decisions: rollout pauses or rolls back when a change burns the budget.

## Area: Resilience

### ARC-08 Failure isolation and graceful degradation
**Definition.** A failing connector, plugin, AI provider, tenant workload or internal service is contained to the affected feature or tenant.
**Why it matters.** Evolution adds dependencies. Each one must be able to fail without taking the core product down.
**Inventory.** Connectors and integrations; plugins and extensions; AI and model providers; tenant workloads; internal services. Record a level for each applicable surface; the score is the level every applicable surface reaches.
**Evidence.** Timeouts, retries, circuit breakers and bulkheads per surface. Fallbacks and their tests. Fault-injection suites.
- **0** One failing dependency fails the whole product.
- **1** Errors caught locally; no timeouts or isolation policy.
- **2** Timeouts and retries on outbound calls; some surfaces degrade gracefully.
- **3** Every surface in the inventory has timeouts and circuit breakers or bulkheads, with tested fallbacks; a failure is contained to the affected feature or tenant.
- **4** Degradation modes declared per capability, exercised by automated fault injection and switched by policy.

### ARC-09 Backup, restore and recovery
**Definition.** Everything needed to rebuild the product's state can be backed up and restored, and restore is proven.
**Why it matters.** A self-changing product will eventually make a change that rollback cannot undo. Restore is the last line of defence, and an untested restore is not one.
**Inventory.** Data; definitions and configuration; uploaded files; secrets and keys. Record a level for each applicable item; the score is the level every applicable item reaches.
**Evidence.** Backup and restore commands or features. Restore tests. Stated recovery point and time objectives. Drill records.
**Boundary.** Level 3 is tested recovery. Stated recovery objectives belong to level 4, because for self-hosted software the deployment operator often sets them.
- **0** No supported backup.
- **1** Documentation tells operators to back up the database themselves.
- **2** A built-in or documented backup command; restore manual and untested.
- **3** Backup and restore supported for every inventory item, with restore exercised by automated tests.
- **4** Recovery objectives (RPO, RTO) stated, point-in-time or per-tenant restore, and recorded restore drills.

# Capability DEL: Velocity (delivery)

Can a change get from request to clients quickly and safely?

## Area: Intake

### DEL-01 Request intake into a structured change specification
**Definition.** A user or operator request becomes a specification precise enough to build and test.
**Why it matters.** The request loop starts here. A free-text wish cannot be implemented, verified or measured.
**Evidence.** Request or feedback objects. Specification templates or generators. Acceptance criteria. Links to affected definitions. Clarifying-question flows.
- **0** Requests live outside the product (email, chat).
- **1** A feedback or feature-request form stores free text.
- **2** Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- **3** The product turns a request into a change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms.
- **4** The specification is machine-readable and drives the implementation lane and tests directly; the product asks clarifying questions when a request is ambiguous.

## Area: Build

### DEL-02 Layers deploy independently
**Definition.** Front end, API and core deploy independently, containerised, with no cross-layer build coupling.
**Why it matters.** Coupling forces every change onto the slowest layer's train. A well-bounded modular monolith with automated delivery is a legitimate choice and scores 1 or 2 here; this criterion measures independence, not architecture fashion.
**Evidence.** Deployables and their build dependencies. Containerisation. Release trains. Cross-layer artifacts consumed at build time.
- **0** One artifact, built and deployed by hand.
- **1** One artifact with automated build and deploy.
- **2** Separately containerised layers that are still built or released together.
- **3** Independently deployable services with contracts; no cross-layer build.
- **4** Progressive delivery per layer with automatic rollback.

### DEL-03 Module boundaries enforced by tooling
**Definition.** Architectural boundaries are enforced by the build or by tests, not by convention.
**Why it matters.** Unenforced boundaries erode, and erosion is what makes change expensive.
**Evidence.** Dependency graph enforcement. Architectural tests or lints. Contracts between modules.
- **0** None.
- **1** Convention.
- **2** Build-system enforced dependency graph.
- **3** Architectural tests or lints plus API contracts between modules.
- **4** Boundaries derived from definitions; violations blocked at PR with explanations.

### DEL-04 AI implementation lane
**Definition.** An accepted request, fix or proposal is implemented by an AI lane that is part of the product's first-party evolution system, either by authoring governed definitions or by producing a tested code change through the product's own pipeline.
**Why it matters.** Changes that need a person to hand-build each one do not scale. Both paths count: definitions where the product is malleable, code where it is not.
**Evidence.** The AI lane, what it can change and how it is invoked. Whether its output arrives as a proposal with verification evidence. Where changes apply. Scope limits.
**Boundary.** Credits a lane that changes this product: its definitions, or its own code under scoring rule 12. AI features that change users' other software are recorded, not scored.
- **0** None.
- **1** Manual per tenant or installation.
- **2** An AI lane drafts changes for narrow tasks on request; a person finishes them.
- **3** An AI lane implements accepted changes end to end, through definitions or a tested code change, under policy and wherever they apply; output arrives as a reviewable proposal with verification evidence.
- **4** The lane covers every change class, chooses the definition or code path itself, and its output is measured after release with rollback.

## Area: Verify

### DEL-05 Every change class has an automated pre-land check
**Definition.** Each kind of change has a deterministic check that runs before it can land, including schema build, lint, tests, accessibility and security, and drafts are included.
**Why it matters.** AI build throughput is only safe if the checks are automatic and unskippable.
**Evidence.** CI configuration. Which change classes have checks. Whether drafts skip CI. Flake handling. Incidents that passed CI.
- **0** None.
- **1** Manual QA.
- **2** CI on PRs with gaps: drafts skip, some classes uncovered.
- **3** Every change class has a deterministic pre-land check and drafts are included.
- **4** Checks generated from definitions and change class; flake quarantine; evidence attached to proposals.

### DEL-06 Verification surface
**Definition.** A machine-readable build and version endpoint, health, and a deployed-configuration snapshot.
**Why it matters.** A pipeline cannot verify what it cannot probe.
**Evidence.** Version or build endpoint. Health checks. Config snapshot. Deployment events.
- **0** None.
- **1** Version visible in the UI only.
- **2** Version endpoint or health, without a config snapshot.
- **3** Build and version endpoint, health, deployed-config snapshot, machine-readable.
- **4** Deployment events emitted and verification evidence attached automatically.

### DEL-07 Environment reproducibility
**Definition.** An instance can be created from a build id with seeded data, flags off first, and destroyed after.
**Why it matters.** Environment drift multiplies QA rounds and hides defects.
**Evidence.** Instance provisioning tooling. Time to create. Seed data. Sharing model. Configuration source and access.
- **0** Hand-built.
- **1** Long-lived shared environments.
- **2** Scripted instance build from a build id; hours; shared.
- **3** Ephemeral instance per change from a build id with seeded data, flags off, destroyed after.
- **4** On demand in minutes with production-shaped anonymised data and cost controls.

### DEL-08 Machine verifiability
**Definition.** Deterministic journeys across roles and devices, a changed-path to feature to journey map, and per-feature adoption instrumentation at ship.
**Why it matters.** Without this, acceptance is a human reading a screen.
**Evidence.** End-to-end suites and their state. Path-to-journey mapping. Adoption instrumentation coverage.
- **0** Manual testing.
- **1** Unit tests only.
- **2** End-to-end journeys exist but are partial or dormant; no path map; no adoption instrumentation.
- **3** Deterministic journeys across roles and devices, changed-path to journey map, per-feature adoption instrumentation at ship.
- **4** Journeys generated from definitions; verification evidence attached to proposals automatically.

## Area: Release

### DEL-09 Staged exposure
**Definition.** A change can reach a cohort, tenant or percentage of users before everyone.
**Why it matters.** Staging limits the blast radius of a bad change, and is what makes measured comparison possible.
**Evidence.** Feature flags, cohorts, per-tenant enablement, percentage rollouts. Which change classes they cover.
- **0** Every change reaches every user at once.
- **1** Global configuration toggles defined in code.
- **2** Feature flags or per-tenant enablement for some changes.
- **3** Any change class (code, definition or learned change) can go to a cohort, tenant or percentage first.
- **4** Exposure progresses or halts automatically on measured health and impact signals, under policy.

### DEL-10 Kill switch
**Definition.** A shipped change can be switched off at runtime without a release.
**Why it matters.** Rollback takes time; a kill switch stops harm now.
**Evidence.** Runtime disable controls. Scope (tenant, global). Audit of use. Automatic triggers.
- **0** Disabling a change needs a release.
- **1** Disabling needs an engineer to edit configuration and restart.
- **2** Some features can be switched off at runtime.
- **3** Any change shipped by the evolution system can be switched off at runtime, per tenant or globally, without a release; use is audited.
- **4** The kill switch triggers automatically on health or impact signals, under policy.

### DEL-11 Release rollback
**Definition.** A code release can be rolled back quickly and safely. GOV-05 covers rolling back definitions; this covers code.
**Why it matters.** When the evolution system ships code, a bad release must be reversible without a new build.
**Evidence.** Release tooling and rollback commands. Data compatibility across one release. Rollback tests. Automatic triggers.
- **0** No rollback; fixes roll forward only.
- **1** Rollback by rebuilding an old version by hand.
- **2** Previous versions can be redeployed; data compatibility not ensured.
- **3** One-step rollback to the previous release, tested, with schema and data changes kept backward-compatible across one release.
- **4** Rollback triggers automatically when verification, health or impact signals fail after release.

# Capability MAL: Open (malleability)

Can the product be reshaped without a code release?

## Area: Data model

### MAL-01 New entity type without code, DDL or deploy
**Definition.** A new kind of business object, with its own fields, storage, permissions and API presence, can be created and used without writing code, running a schema migration, or deploying.
**Why it matters.** Everything else in the framework generates from the type. If a type needs code, nothing downstream can be data.
**Evidence.** A type registry, enum or table that lists entity kinds and how it is populated. Whether adding a kind requires DDL. Any "custom object" UI or API. Whether a deploy is required.
- **0** Types are hard-coded and adding one is a project.
- **1** Adding a type is code plus migration plus release.
- **2** A runtime type registry or generic store exists but is populated by engineers through config, migration or API.
- **3** The operator defines types through a supported path, live, validated, with no deploy.
- **4** Types are machine-readable definitions an AI can author, validated with dry-run, versioned, and applied through a policy gate.

### MAL-02 Field definitions carry type and validation
**Definition.** Fields on any entity are declared with a data type and validation rules that forms, API and search all read.
**Why it matters.** Validation handled per feature is re-implemented on every surface; declared once, it is inherited. Privacy classification of fields is scored in GOV-03.
**Evidence.** Custom field types and their storage. Where validation rules live. Whether forms, API and search read the same definition.
- **0** Fields are database columns only.
- **1** Field additions are code.
- **2** Typed custom fields exist through API or files for engineers; validation partial.
- **3** The operator adds typed, validated fields through a supported path; the same definition drives forms and API.
- **4** Every field has type and validation in one machine-readable definition consumed by forms, API, search and erasure; AI-authorable.

### MAL-03 Relationships and lifecycle states declarable
**Definition.** Relationships between entities, or lifecycle states with transitions, are declared in the definition, not coded per feature.
**Why it matters.** Most product behaviour is a relationship or a state change. If those are code, so is the product.
**Evidence.** Generic association or relation tables. Workflow or state tables. Per-feature state enums in code. Any admin path for relations or states.
- **0** None.
- **1** Coded per feature.
- **2** A generic relation or state mechanism exists for engineers, not exposed.
- **3** The operator declares relations, or lifecycle states with transitions, through a supported path.
- **4** Both relations and states are declarable, with referential integrity and transition guards enforced by the platform from the definition; AI-authorable.

## Area: APIs

### MAL-04 API per entity is generic or generated
**Definition.** An entity's read and write API exists without an engineer writing a resolver or controller for that entity.
**Why it matters.** Hand-written API per entity is the largest fixed cost of a new type and the largest source of contract drift.
**Evidence.** Count of hand-written resolvers, registries or controllers. Any generic entity endpoint. Whether codegen starts from a hand-written schema or from definitions.
- **0** No API.
- **1** Hand-written per entity.
- **2** A generic surface exists for one entity family, or codegen runs from a hand-written schema.
- **3** API for defined entities is generic or generated from definitions with no per-entity code.
- **4** Generated API includes typed projections, filters and validation from the definition and updates at runtime.

### MAL-05 API reshapes at runtime from definitions
**Definition.** A definition change changes the API surface without a build or deploy.
**Why it matters.** This is what makes "no code release" literal rather than aspirational.
**Evidence.** How and when the schema is assembled. Cache invalidation triggers. Whether any resource change reshapes the schema live.
- **0** Schema is compiled into the artifact.
- **1** Any change needs a deploy.
- **2** Runtime schema assembly with invalidation exists, but only from engineer-managed resources.
- **3** Publishing a definition reshapes the API live for that tenant.
- **4** Reshaping is versioned per consumer with deprecation windows and dry-run.

### MAL-06 Machine-readable contract with introspection and dry-run
**Definition.** Callers can discover the API, generate typed clients, and validate or dry-run a mutation before executing it.
**Why it matters.** An AI or agent can only act safely on a contract it can read and test.
**Evidence.** Introspection or OpenAPI coverage. Client codegen. Structured validation errors. Any dry-run or preview mode. Published schema artifacts per build.
- **0** Documentation only.
- **1** Hand-written docs.
- **2** Partial machine-readable contract: introspection or partial OpenAPI.
- **3** Full introspection, typed client generation, structured server validation errors.
- **4** Dry-run mode for mutations, contract tests, versioned schema artifacts published per build.

## Area: Interface

### MAL-07 Layout is data, tenant-overridable, validated, previewable
**Definition.** Page structure, which components, where, with what props, is stored as validated data, overridable per tenant, previewable before publish.
**Why it matters.** Layout as data is where natural-language UI authoring becomes tractable, because the target is a constrained format.
**Evidence.** Layout files or tables and their schema. A page designer. Per-tenant override storage. Preview mechanism. Whether component props are schema-validated.
- **0** Layout is coded.
- **1** Templates in code.
- **2** Layout files as data, engineer-edited, no tenant override.
- **3** Operator layout editor with per-tenant overrides, schema validation, preview.
- **4** Layout and component props target a machine-validated schema; AI-authorable; versioned with rollback.

### MAL-08 Generic list, detail and intake widgets from definition plus view spec
**Definition.** List, detail and create or edit views render from the entity definition and a view spec, so a new type gets UI without new components.
**Why it matters.** Without generic widgets, every new type still needs a front-end feature.
**Evidence.** Whether forms render from a spec. Whether custom fields render generically. Any list or card component parameterised by type. A view spec format.
- **0** None.
- **1** Every view hand-built.
- **2** Partial generic rendering exists, such as forms from a spec or generic field display, but not list, detail and intake together.
- **3** Generic list, detail and intake widgets exist and the operator configures view specs.
- **4** View specs are machine-readable and AI-authorable with inherited accessibility and theme.

### MAL-09 Theme tokens and text are data with tenant overrides
**Definition.** Visual tokens and UI text are externalised data with tenant overrides and locale coverage.
**Why it matters.** Brand and language are the most frequent tenant changes; if they are code, tenants queue for releases.
**Evidence.** Token count and how they are served. A theme editor. Text storage, locale count, tenant override UI, translation pipeline.
- **0** Hard-coded.
- **1** CSS and strings in code.
- **2** Tokens and text externalised but engineer-managed.
- **3** Operator theme editor or validated theme definitions, per-tenant text overrides, locale pipeline.
- **4** Tokens and text carry a machine-readable schema, changes flow through the proposal path, AI translation and theming validated with contrast checks.

## Area: Behaviour

### MAL-10 Rules engine with declarative conditions and actions
**Definition.** Conditions and actions defined as data trigger behaviour such as notifications, role changes, webhooks and state transitions.
**Why it matters.** Most feature requests are behaviour. A rules engine turns them into configuration.
**Evidence.** Rule, condition and action classes or tables. Admin UI for rules. Whether rules cover custom or defined entities. Any simulation or test mode.
- **0** None.
- **1** Behaviour coded.
- **2** Engine exists but is engineer or API only, or narrow in scope.
- **3** The operator composes rules through a supported path across entities, with a test mode.
- **4** Rules are machine-readable, simulatable against history, versioned, AI-authorable, and cover defined entities.

### MAL-11 Event model with webhooks or subscriptions and retry
**Definition.** Entity lifecycle events publish to a durable bus and to outbound subscribers with retry and replay.
**Why it matters.** Integration and automation both hang off events; without durability they are best-effort.
**Evidence.** Event bus or listener framework. Webhook manager. Retry queue. Delivery logs. Replay capability.
- **0** None.
- **1** Per-feature listeners in code.
- **2** Event mechanism exists; webhooks limited or without retry.
- **3** The operator subscribes to events with webhooks, retry and delivery logs.
- **4** Event schema generated from definitions including defined entities; replay; per-tenant streams.

### MAL-12 Sandboxed server-side hooks
**Definition.** Custom server-side logic runs at defined hook points without deploying core, isolated by dependency allowlists, timeouts and egress control.
**Why it matters.** The residue rules cannot express needs code; unsandboxed code is how platforms become un-upgradable.
**Evidence.** Custom endpoint or hook framework. Trigger types. Allowlists. Runtime isolation. Egress control. Who can deploy hooks.
- **0** None.
- **1** Core code only.
- **2** Server-side extension exists but is unsandboxed or request-triggered only.
- **3** Sandboxed hooks with allowlists, timeouts and egress control, triggered by events and requests, deployable by partners.
- **4** Hooks are AI-authorable with a test harness, policy-gated, observable per hook.

## Area: Extensions

### MAL-13 Plugin lane breadth
**Definition.** Plugin points exist across UI components, layout, forms, theme, text and server, in both declarative and code forms.
**Why it matters.** Breadth decides how much can be extended without touching core.
**Evidence.** Plugin or SDK documentation. Plugin point types. Declarative versus code options.
- **0** None.
- **1** Fork the code.
- **2** Code plugins only, or narrow points.
- **3** Declarative and code plugin points across UI, layout, forms, theme, text and server, documented.
- **4** Plugin points generated from definitions; registry or marketplace; versioned.

### MAL-14 Runtime isolation and dependency control
**Definition.** Third-party or AI-written code runs isolated, with dependency allowlists, resource limits and egress control.
**Why it matters.** AI-authored code at volume is only safe inside a sandbox.
**Evidence.** Where plugin code executes. Allowlists and when they are enforced. CSP. Iframe or process isolation. Quotas.
- **0** Full trust.
- **1** Full trust with review.
- **2** Build-time allowlists and CSP; same process.
- **3** Runtime isolation, resource limits, egress control.
- **4** Per-plugin identity, quotas, observability, automatic disable on violation.

### MAL-15 Developer loop
**Definition.** Extension developers can preview against a real tenant, use staged branches, read logs, and validate before publishing.
**Why it matters.** A slow loop pushes developers to hack core instead.
**Evidence.** Preview tooling. Staging branches. Log access. Validators. Local development support.
- **0** None.
- **1** Build and deploy to test.
- **2** Local development possible; documentation.
- **3** Preview against a real tenant, staged branches, logs, validators.
- **4** Ephemeral preview environments per change with a test harness and AI assistance.

## Area: Integrations

### MAL-16 Canonical data model with a mapping layer
**Definition.** External systems integrate through a canonical model and a configurable mapping layer, so the second connector is field mapping, not core code.
**Why it matters.** The second integration should cost a fraction of the first.
**Evidence.** Canonical entity model. Mapping configuration or UI. How existing integrations were built. Count of bespoke modules.
- **0** None.
- **1** Bespoke integration per system.
- **2** Canonical model for one domain; mapping partly code.
- **3** Configurable mapping layer, so a second connector is mapping.
- **4** Mapping machine-readable, AI-proposed from the target schema, validated with sample sync.

### MAL-17 Connector definition or SDK
**Definition.** A connector definition or SDK covers authentication, sync, webhooks and lifecycle, so connectors are added without touching the kernel.
**Why it matters.** Without an SDK, every connector is a core project.
**Evidence.** Connector SDK or shared engine pattern. Lifecycle management. Who builds connectors. Admin install and configuration.
- **0** None.
- **1** Core code.
- **2** SDK exists for engineers; lifecycle manual.
- **3** Connector definition or SDK covers auth, sync, webhooks, lifecycle; partners build; admins install and configure.
- **4** Connectors generated or assisted from the target API spec; certified; observable.

### MAL-18 Stable versioned contracts
**Definition.** Inbound and outbound contracts are versioned with deprecation windows, idempotent sync and conflict handling.
**Why it matters.** Unstable contracts make every platform change a partner incident.
**Evidence.** API versioning scheme. Deprecation policy. Idempotency. Conflict resolution. Contract tests.
- **0** None.
- **1** Undocumented changes.
- **2** Documented API; versioning by path; no deprecation policy.
- **3** Versioned contracts, deprecation windows, idempotent sync, conflict handling.
- **4** Contract tests in both directions; compatibility guaranteed by policy; replay.

## Area: Agent interface

### MAL-19 Machine-readable capability surface for agents
**Definition.** The product exposes typed, discoverable tools (MCP or an equivalent agent protocol) generated from its definitions, with scoped auth and a current capability map.
**Why it matters.** Agents act on tools, not on documentation. The protocol is not the point; typed discovery and scoping are.
**Evidence.** MCP server or equivalent. Tool definitions and their source. Capability map. Auth scoping on tools.
- **0** None.
- **1** Hand-written API documentation.
- **2** Introspectable API; no tool surface.
- **3** A typed tool surface with scoped auth; a capability map exists.
- **4** Tools generated from definitions including defined entities; capability map machine-readable and current.

### MAL-20 Conversational operability for users and natural-language authoring for operators
**Definition.** End users complete tasks through a grounded conversational surface, and operators author definitions, layouts and text through natural language on the same surfaces the UI uses.
**Why it matters.** Conversation is increasingly how both users and operators reach a product; it only helps if it is grounded and shares the product's definitions.
**Evidence.** Chat or assistant surfaces. Grounding sources. Actions available conversationally. Operator natural-language authoring. Evaluation harness.
- **0** None.
- **1** FAQ or keyword bot.
- **2** Grounded conversational surface for one persona, or natural-language authoring for one surface.
- **3** Users complete tasks conversationally with grounding and actions; operators author through natural language with preview.
- **4** Conversation and UI share definitions; every UI action has a conversational equivalent; an evaluation harness measures groundedness.

# Capability LRN: Learn (learning)

Does the product notice what is wrong, work out why, and know whether its changes helped?

## Area: Sense

### LRN-01 Telemetry accessible to the platform in near real time
**Definition.** Usage and behaviour telemetry is available to platform features within minutes, not only to analysts nightly.
**Why it matters.** Self-evolution starts with seeing.
**Evidence.** Event pipeline and latency. Consumers inside the product. Per-feature instrumentation.
- **0** None.
- **1** Logs.
- **2** Batch analytics.
- **3** Near-real-time events available to platform features.
- **4** Streaming with per-entity and per-definition instrumentation added automatically.

### LRN-02 Structured learning signals
**Definition.** Feedback, corrections, ratings, evaluation outcomes and per-definition usage are recorded as structured signals linked to the definition and version they concern.
**Why it matters.** Free text cannot drive proposals; signals tied to what they concern can.
**Evidence.** Feedback or rating objects. Evaluation results. Usage counters per definition. What they link to. Triage.
- **0** None.
- **1** Free-text reports only.
- **2** Typed signals exist but are not linked to the definition and version they concern.
- **3** Typed signals linked to the definition and version they concern, with a triage or review workflow.
- **4** Signals are auto-classified and routed into proposals; the loop closes with the reporter.

### LRN-03 User-issue detection
**Definition.** The product detects that users are struggling, not only that servers are failing.
**Why it matters.** The fix loop starts with knowing what hurts users. Server errors are a small part of it.
**Evidence.** Error capture tied to user actions. Friction signals (abandoned flows, retries, corrections, negative feedback). Issue objects attributed to a capability.
- **0** No error or usage visibility in the product.
- **1** Server logs and error tracking for engineers.
- **2** User-facing errors and failed actions recorded with the product area and queryable.
- **3** The product detects friction patterns (repeated failures, abandoned flows, retries, corrections, negative feedback, support requests) and raises them as issues attributed to a capability, with affected users and frequency.
- **4** Detected issues are prioritised by impact and fed automatically into diagnosis and the change path.

### LRN-04 Cross-source mining inside the product
**Definition.** The product joins its own usage, feedback, error and change history into queryable models and mines them continuously.
**Why it matters.** Diagnosis needs joined data; analysis done outside the product does not compound.
**Evidence.** Joined stores and what they join. Mining jobs. Whether findings surface in the product.
- **0** None.
- **1** Manual analysis outside the product.
- **2** Some sources are joined or queryable together.
- **3** The product joins usage, feedback, errors and change history with queryable models.
- **4** Continuous mining producing candidate findings with provenance.

## Area: Diagnose and propose

### LRN-05 Automated diagnosis
**Definition.** For a detected issue, the product works out why it happens.
**Why it matters.** Detection without diagnosis produces a queue for engineers, not a fix.
**Evidence.** Failure grouping. Context attached to issues (traces, inputs, recent changes). Reproduction and root-cause features.
- **0** None.
- **1** Raw traces or logs that engineers read.
- **2** The product groups related failures and attaches context (traces, inputs, recent changes).
- **3** For a detected issue, the product produces a reproducible case and a likely cause, linked to the responsible definition, change or code area, for a person to confirm.
- **4** Diagnosis is validated by reproducing the failure and checking the proposed fix against it before the fix is proposed.

### LRN-06 Ranked, evidence-backed proposals for change
**Definition.** From observed data, the product produces ranked proposals to change its own behaviour or configured definitions, with evidence and expected impact.
**Why it matters.** This is the difference between a dashboard and a self-diagnosing system.
**Evidence.** Recommendation features. Proposal objects. Ranking and evidence. What the proposals target.
- **0** None.
- **1** Dashboards.
- **2** Recommendations or proposals for one area.
- **3** Ranked evidence-backed proposals across the product with expected impact.
- **4** Proposals carry definition diffs ready for the gate and post-apply impact measurement.

## Area: Learn from experience

### LRN-07 The product turns its own operating experience into candidate changes
**Definition.** The product observes its own runs, sessions or usage and, without being asked, produces candidate changes to its own behaviour or configured definitions (skills, rules, prompts, memory, configuration, indexes).
**Why it matters.** This is what "self-improving" means in practice. Governance (GOV) says whether such changes are safe; this says whether they happen at all.
**Evidence.** Background review or reflection jobs. Skill or rule creation from sessions. Automatic tuning from usage. Defaults.
- **0** None.
- **1** People turn experience into changes by hand.
- **2** The product captures experience and can generate candidate changes when asked.
- **3** The product continuously turns its own experience into candidate changes without being asked.
- **4** Candidates are prioritised by expected impact, and the product learns which kinds of change succeed.

### LRN-08 Learned changes are validated before they take effect
**Definition.** Changes the product proposes to itself are checked, and evaluated against the current baseline, before they apply.
**Why it matters.** A system that rewrites itself without evaluation is self-modifying, not self-improving.
**Evidence.** Scans and linters on learned changes. Evaluation datasets. Baseline comparison. Pass, revise or block decisions.
- **0** No checks.
- **1** Manual review only.
- **2** Automated checks (security scan, lint, schema) on learned changes.
- **3** Learned changes are evaluated against the current baseline on representative tasks or data, with a pass, revise or block decision before apply.
- **4** Evaluation is automatic for every learned change, uses held-out data, and its results feed the policy in GOV-07.

## Area: Measure

### LRN-09 Post-change impact is measured against a declared baseline
**Definition.** Every material applied change carries a baseline, intended outcome, observation window and decision to keep, revise or roll back.
**Why it matters.** Applying a proposal is not evidence that it improved the product or operation. A learning loop exists only when impact changes the next decision.
**Evidence.** Proposal-to-metric linkage. Baseline capture. Success thresholds. Observation windows. Segment or counterfactual comparison where practical. Recorded keep, revise or rollback decisions.
**Boundary.** Post-apply measurement only. Validation before a change takes effect is LRN-08.
- **0** No post-change outcome measurement.
- **1** Ad hoc manual before-and-after checks.
- **2** Relevant telemetry exists, but it is not bound to the proposal version, baseline and decision.
- **3** Applied proposals record a baseline, target metric, observation window and explicit keep, revise or rollback decision.
- **4** Instrumentation is created with the proposal; policy uses measured impact to promote, revise or reverse the change, with attribution limits recorded.

# Capability GOV: Vet (governance)

Is every change safe, accountable and reversible, including the changes the product makes to itself?

## Area: Compliance and security

### GOV-01 Accessibility inherited from a component kit and continuously verified
**Definition.** Accessibility comes from a component kit and design tokens and is verified continuously, not engineered per feature.
**Why it matters.** Per-feature accessibility is re-paid on every feature and fails audits.
**Evidence.** Component kit and token usage share. Automated scanners. Whether scans gate changes. Required accessible props enforced by lint. Conformance reporting.
- **0** No audit and no kit.
- **1** Manual audits; per-feature fixes.
- **2** Component kit and tokens; automated scans on demand.
- **3** Scans gate every change; the kit enforces required accessible props.
- **4** Continuous scanning with automatic fix proposals through the change path; conformance report generated with human sign-off where required.

### GOV-02 Audit generic over entities, definition changes and approvals
**Definition.** One audit trail records every entity mutation, definition change and approval, queryable by admins.
**Why it matters.** SOC 2 change control needs evidence per change; a generic trail makes it free.
**Evidence.** Audit table or service and its schema. Coverage across entities. Admin UI. Whether config or definition changes are recorded. Retention.
- **0** None.
- **1** Per-feature logs.
- **2** Generic audit store exists; coverage partial; no admin UI or definitions uncovered.
- **3** Admin UI; covers all entities, configuration and definition changes, and approvals; retention policy.
- **4** Audit events are structured, exportable, tamper-evident, and consumed by the advise loop.

### GOV-03 Privacy classification, export, erasure and retention generic over entities
**Definition.** Fields carry a privacy classification, and data-subject export, erasure and retention work for every entity based on it, not per-feature code.
**Why it matters.** A malleable product without this fails privacy law the first time an operator defines a personal field.
**Evidence.** Privacy or sensitivity tags on fields and their consumers. Erasure and export services and which entities they cover. Retention policies. Admin triggers. Verification reports.
- **0** None.
- **1** Manual or engineer-run scripts.
- **2** Implemented for one entity family only, or across entities through code-declared lists.
- **3** A field-level privacy classification drives operator-triggered export and erasure across entities; retention policies.
- **4** Automatic detection of untagged personal data with tagging proposals; verified erasure reports.

### GOV-04 Security as infrastructure
**Definition.** Authorisation derives from definitions, input validation is generic over entities, and vulnerability scanning is continuous and gates change.
**Why it matters.** Security handled per feature drifts; structural controls do not.
**Evidence.** Permission model and how new permissions are declared. Validation framework and whether it is mandatory. SAST, dependency and container scanning in CI. Whether scans block merges. Runtime policy enforcement.
- **0** None.
- **1** Per-feature checks; manual penetration tests.
- **2** Generic permission model and mandatory validation; scans on demand.
- **3** Scanning gates every change; authorisation generated per defined type.
- **4** Continuous scanning with auto-remediation proposals; runtime policy enforcement; incidents feed rules.

## Area: Change control

### GOV-05 Definitions and layouts versioned with rollback
**Definition.** Every definition, layout, text, theme and configuration change is a version that can be diffed and rolled back.
**Why it matters.** Malleability without rollback is risk; rollback is what lets a policy gate apply changes.
**Evidence.** Version storage for each customisation surface. Diff and history UI. Rollback path. Whether all surfaces are covered.
**Boundary.** Score the inventory of surfaces operators change by default, including any the product modifies itself, and list uncovered surfaces. Definition rollback only; code releases are DEL-11.
**Inventory.** One entry per customisation surface. When the score is 3 or more, record a level per applicable surface; the score is the level every surface reaches.
- **0** None.
- **1** Only in code version control, for engineers.
- **2** Versioning for some surfaces, or without a rollback UI.
- **3** The operator sees history and diffs, and rolls back, across all customisation surfaces.
- **4** Versions are addressable objects linked to proposals and evidence; rollback automatic on failed verification.

### GOV-06 Proposal, review, apply as a first-class object with preview
**Definition.** A change is a proposal carrying diff, rationale, evidence and preview, reviewed, then applied.
**Why it matters.** This is the object an AI produces and a gate consumes; without it, AI output is a chat message.
**Evidence.** Any proposal or change-request object. Stage and publish workflows. Preview on staging data. Who can create proposals.
- **0** None.
- **1** Pull requests for code only.
- **2** Stage and publish or GitOps flow for engineers.
- **3** The operator proposes, previews (on staging data or a staged copy) and applies with review.
- **4** Proposals are typed objects any actor can create; preview on production-shaped data; evidence attached automatically.

### GOV-07 Policy-based apply with recorded approvals and a movable human boundary
**Definition.** A policy decides which proposal classes apply automatically on passing checks and which need a human; approvals are recorded; the boundary moves with measured verifier trust.
**Why it matters.** Human gating everywhere does not scale; no gating anywhere fails audit. Policy is the middle.
**Evidence.** Policy object or configuration. Auto-apply classes. Approval records. Verifier false-pass measurement. Kill switch.
**Boundary.** Policies over changes to the product's own definitions and behaviour, including self-modification. Per-action tool permissions are GOV-09.
- **0** None.
- **1** Every change needs a human.
- **2** Auto-apply for narrow classes, such as deploy sync, without a policy object.
- **3** Policy object per change class with recorded approvals.
- **4** Policy adapts to verifier false-pass rates; full audit; kill switch.

### GOV-08 Upgrade safety
**Definition.** Tenant customisations and definitions survive a platform release without code migration.
**Why it matters.** Unlimited malleability at the code layer produced un-upgradable estates; this criterion scores that failure before it happens.
**Evidence.** Extension contract versioning. Compatibility checks. Migration tooling. History of customisations breaking on upgrade.
- **0** Customisations break each release.
- **1** Manual migration per tenant.
- **2** Versioned extension contracts; compatibility mostly manual.
- **3** Automated compatibility checks and migration tooling; customisations confined to stable contracts.
- **4** Backward compatibility guaranteed for definitions with automated migration proposals; breaking changes need a policy exception.

## Area: AI and self-change safety

### GOV-09 Agent-safe actions
**Definition.** Every mutation is scoped to a real identity rather than ambient authority, idempotent, previewable, audited and rate-limited.
**Why it matters.** An agent with ambient authority is an incident waiting for a prompt injection.
**Evidence.** Identity model for API callers. Token scoping. Idempotency keys. Dry-run. Rate limits. Audit rows. Kill switch.
**Boundary.** Covers every machine actor that can change the product through an API or tool surface: the product's own agents and external agents or automated clients. It applies when `machine_actions` is true.
- **0** Ambient authority.
- **1** Shared API keys.
- **2** Per-actor tokens and audit; no dry-run.
- **3** Scoped agent identity, idempotent mutations, preview or dry-run, rate limits, audit rows.
- **4** Policy-gated actions with kill switch, spend and rate budgets, per-action risk classification.

### GOV-10 Bounded self-change
**Definition.** Explicit, enforced limits on what the product, its AI lanes and its learning loops may change on their own.
**Why it matters.** Review gates decide whether a change is good. Bounds decide how much damage a bad one can do before anyone looks.
**Evidence.** Allow-lists and deny-lists for self-modification. Rate and volume limits. Blast-radius limits. Logs of blocked changes.
- **0** Self-modifications or AI-authored changes are unrestricted.
- **1** Limits exist only as prompt instructions or convention.
- **2** An allow-list or deny-list of what may change, enforced in code for some change paths.
- **3** Every self-change path is enforced against a declared scope (surfaces, tenants, changes per period) with a blast-radius limit; out-of-scope changes are blocked and logged.
- **4** Scopes are versioned, reviewed policy, tightened automatically after a failed or reverted change.

### GOV-11 Learning-input integrity
**Definition.** The inputs that drive change (requests, feedback, telemetry, memories, documents) cannot easily be poisoned or used to inject instructions.
**Why it matters.** A product that learns from its users can be taught the wrong thing by one of them.
**Evidence.** Provenance on learned items and AI-built changes. Separation of untrusted content from instructions. Injection scanning. Bulk revert by source.
- **0** Any input can be written straight into memory, skills, rules or a change.
- **1** Inputs stored with no provenance.
- **2** Changes record their source inputs; some inputs are filtered.
- **3** Provenance recorded for every learned or AI-built change; untrusted inputs are separated from instructions, scanned for injection, and cannot alone trigger an automatically applied change.
- **4** Changes can be bulk-reverted by source, and adversarial inputs are part of the automated evaluation.

# Capability EXP: Expand (expansion)

Can the product grow into adjacent value, and does it notice where to grow?

## Area: Expressible

### EXP-01 Kernel concepts are domain-neutral
**Definition.** The kernel holds domain-neutral primitives (for example identity, content, permission, workflow, messaging), with the product's domain expressed above it.
**Why it matters.** Domain nouns in the kernel make adjacent domains rewrites. The exact primitives depend on the product; neutrality is what is scored.
**Evidence.** Core entity names. Where domain-specific behaviour lives.
- **0** Single-purpose.
- **1** Domain baked in.
- **2** Some neutral primitives, but domain nouns remain in core.
- **3** Kernel primitives are domain-neutral; the domain is expressed above them.
- **4** Kernel primitives are themselves configurable definitions.

### EXP-02 A new domain is expressible without kernel change
**Definition.** An adjacent domain is built as definitions plus connectors plus rules, with no kernel change.
**Why it matters.** This tests whether the kernel really is neutral.
**Evidence.** Any adjacent domain shipped this way. What a new domain would need in core today.
- **0** Rewrite.
- **1** Major core work.
- **2** Mechanisms exist but a new domain needs core additions.
- **3** New domain as definitions, connectors and rules; proven by at least one adjacent domain shipped this way.
- **4** Multiple domains shipped as bundles with the kernel unchanged.

### EXP-03 A domain ships as an installable bundle
**Definition.** A domain or solution ships as a versioned bundle of definitions, layouts, rules and connectors that can be applied to a tenant.
**Why it matters.** Bundles are how a platform sells opinionated workflows instead of blank canvases.
**Evidence.** Export and import of assets. Templates. Bundle format and versioning.
- **0** None.
- **1** Manual setup.
- **2** Export and import of assets per tenant.
- **3** Installable bundle of definitions, layouts, rules and connectors, versioned.
- **4** Bundles composable, upgradeable, AI-assembled from requirements.

## Area: Discover

### EXP-04 Unmet-demand sensing
**Definition.** The product notices what users try to do that it does not serve.
**Why it matters.** Adjacent value is found in failed searches, unsupported requests and workarounds, long before anyone writes a feature request.
**Evidence.** Failed-search and unsupported-intent logs. Assistant refusals and fallbacks. Feature-request objects. Workaround signals (custom fields, exports, external tools).
- **0** None.
- **1** Free-text feedback only.
- **2** Unmet intents recorded in queryable form: failed searches, unsupported requests to an assistant, feature requests, heavy workaround use (custom fields, exports, external tools).
- **3** These signals are clustered into themes outside the current domain scope, with volume, trend and affected segments.
- **4** Demand signals combined across tenants under privacy controls and refreshed continuously.

### EXP-05 Evidence-backed opportunity proposals
**Definition.** The product proposes adjacent capabilities, with evidence, for a person to decide.
**Why it matters.** This is the step from "users want something" to "here is what we could become": a community platform proposing a course module, a professional network proposing gig matching.
**Evidence.** Opportunity or proposal objects for new capabilities. Evidence and sizing attached. Fit analysis against existing concepts.
- **0** None.
- **1** Raw demand data only.
- **2** Drafts an adjacent-capability proposal on request, citing some evidence.
- **3** Proposes adjacent capabilities on its own, each with evidence, sizing, fit with existing concepts (which entities, bundles and connectors it reuses) and a success metric, ranked for a person to decide.
- **4** Proposals include a buildable specification and a prototype assembled from bundles or the implementation lane.

## Area: Launch

### EXP-06 Cohort launch with keep-or-kill
**Definition.** An expansion launches to a small group first, against a declared success metric, and is kept or removed on the result.
**Why it matters.** New domains are bets. Launching them like bets keeps a failed one from becoming permanent weight.
**Evidence.** Per-tenant or per-cohort enablement of new capabilities or bundles. Success metrics and review dates. Removal paths. Recorded decisions.
- **0** New domains launch to everyone or not at all.
- **1** Manual beta run by engineering.
- **2** A new capability or bundle can be enabled for selected tenants or users.
- **3** An expansion launches to a cohort with a declared success metric, a review date and a clean removal path; the keep-or-kill decision is recorded.
- **4** The product measures the cohort against the metric and recommends keep, extend or kill under policy.
