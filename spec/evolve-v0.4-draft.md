# EVOLVE v0.4: specification draft

**Status: draft for review.** Nothing in `scripts/` or `assessments/` uses this yet. The current scorer and rubric remain MSR v0.3 until this draft is agreed. Comment on any section; the open decisions are listed at the end.

## 1. The question EVOLVE answers

> How ready is a software product to evolve itself safely?

That breaks into three abilities, called **loops**:

| Loop | The product can... | Example |
|---|---|---|
| **Request → Release** | take a user or operator request, implement it properly and release it | "Add an approval step to expense claims" goes live for that customer |
| **Issue → Fix** | find problems users face, fix them and ship the fix | Users keep failing at checkout; the product finds why, fixes it and confirms the failures stopped |
| **Opportunity → Expansion** | notice adjacent needs it does not yet serve, and propose or launch them | A community platform sees members selling courses and proposes a course (LMS) module; a professional network sees skill posts and proposes gig matching |

Each loop is only as strong as its weakest stage. A product with a superb release pipeline that never notices problems cannot fix itself; a product that notices everything but cannot ship safely cannot either.

**What EVOLVE measures.** The product, as shipped: its code, configuration, companion repositories and documentation. It does not measure the team's delivery performance, and it is not a scale for AI coding assistants. Existing autonomy scales for coding agents (for example the L1–L5 scales published for agentic software engineering) ask how independently an AI writes code. EVOLVE asks whether the *product* is built so that it can be changed by request, fix itself and grow, safely.

## 2. Structure at a glance

```
Software Autonomy Level (SAL, L0–L5)          <- headline: what the product can do alone
  ├─ Request → Release   level
  ├─ Issue → Fix         level
  └─ Opportunity → Expansion level
        ▲ computed from stages, each backed by criteria
        │
Six capabilities (the EVOLVE profile)          <- diagnosis: where it is strong or weak
  E  Elastic   architecture: scales, survives failure, recovers data
  V  Velocity  factory: builds, verifies and releases changes quickly and safely
  O  Open      malleability: reshaped without a code release
  L  Learn     senses problems, diagnoses, proposes, measures
  V  Vet       governance: changes are reviewed, policy-gated, audited, reversible
  E  Expand    discovers and launches adjacent value
        +
Hard gates                                      <- critical controls that cap the level
```

## 3. Software Autonomy Levels

Modelled on the SAE driving-automation levels: each level says who does the work and where people stay in control.

| Level | Name | What the product can do in that loop |
|---|---|---|
| **L0** | Manual | Every change is engineers writing and releasing code. |
| **L1** | Configurable | People make the change without bespoke engineering: through governed configuration, or an AI-drafted change they finish. Changes are versioned. |
| **L2** | Assisted | The product does the thinking work for people: structures the request, diagnoses the issue or drafts the proposal, and drafts the change. People build, check and release. |
| **L3** | Supervised | The product carries the loop end to end, including verification and staged release. A person approves each release. All hard gates pass. |
| **L4** | Policy-bounded | Low-risk change classes ship without a person, under explicit policy, with staged rollout, impact measurement and automatic rollback. People handle exceptions. Gates are backed by tested evidence. |
| **L5** | Self-directing | Across change classes, the product initiates, ships and measures change within policy; people set policy and goals. Backed by operational evidence, not only code. |

Levels are cumulative per loop: a loop reaches a level only if it meets every condition for that level and all lower ones.

**Headline SAL** is the lower of the Request → Release and Issue → Fix levels. Opportunity → Expansion is reported next to it rather than inside it, because it is the aspiration on top of the two core loops:

> **SAL 2** · Request → Release L3 · Issue → Fix L2 · Expansion L1

## 4. The six capabilities and their criteria

Every criterion keeps the 0–4 anchored ladder from v0.3 (0 absent, 1 code-only, 2 mechanism, 3 productised, 4 generative and policy-gated). Capability scores are the mean of their area means. 49 criteria carry over from MSR v0.3 with their wording (subject to the clarifications in section 8); 13 are new. Total: 62.

IDs are renumbered with a capability prefix so that letters no longer collide (the old dimension O was adjacent expansion; the new O is Open). Section 9 maps every old ID.

### E — Elastic (architecture)

Can the product take the load and survive the change?

| ID | Criterion | Area | From |
|---|---|---|---|
| EL1 | Indexed query path, never a scan of a generic store | Data | G1 |
| EL2 | Safe schema and data migrations | Data | **new** |
| EL3 | Horizontal scale and asynchronous work | Scale | **new** |
| EL4 | Tenant isolation and noisy-neighbour controls | Scale | G2 |
| EL5 | Measured capacity and service objectives | Scale | G3, extended |
| EL6 | Failure isolation and graceful degradation | Resilience | **new** |
| EL7 | Backup, restore and disaster recovery | Resilience | **new** |

### V — Velocity (factory)

Can a change get from request to clients quickly and safely?

| ID | Criterion | Area | From |
|---|---|---|---|
| VE1 | Request intake into a structured change specification | Intake | **new** |
| VE2 | Layers deploy independently | Build | H1 |
| VE3 | Module boundaries enforced by tooling | Build | H2 |
| VE4 | AI implementation lane | Build | M3, moved from Learning |
| VE5 | Every change class has an automated pre-land check | Verify | H3 |
| VE6 | Verification surface | Verify | L1 |
| VE7 | Environment reproducibility | Verify | L2 |
| VE8 | Machine-verifiable release evidence | Verify | L3 |
| VE9 | Staged rollout, feature flags and kill switch | Release | **new** |

VE4 now credits **both** paths to a built change: an AI that authors governed definitions (configuration path), and an AI lane that turns an accepted request into a tested code change through the product's own committed pipeline (code path). v0.3 gave the code path almost no credit.

### O — Open (malleability)

Can the product be reshaped without a code release?

| ID | Criterion | Area | From |
|---|---|---|---|
| OP1–OP3 | Entity types, field definitions, relationships and lifecycle as data | Data model | A1–A3 |
| OP4–OP6 | Generated APIs, runtime reshaping, machine-readable contract | APIs | B1–B3 |
| OP7–OP9 | Layout as data, generic widgets, theme and text as data | Interface | C1–C3 |
| OP10–OP12 | Rules engine, event model, sandboxed hooks | Behaviour | D1–D3 |
| OP13–OP15 | Plugin lanes, plugin isolation, developer loop | Extensions | I1–I3 |
| OP16–OP18 | Canonical data model, connector SDK, versioned contracts | Integrations | N1–N3 |
| OP19–OP20 | Machine-readable capability surface for agents; conversational operation and authoring | Agent interface | K1–K2 |

### L — Learn

Does the product notice what is wrong, work out why, and know whether its changes helped?

| ID | Criterion | Area | From |
|---|---|---|---|
| LE1 | Telemetry accessible to the product in near real time | Sense | J1 |
| LE2 | Structured learning signals | Sense | J2 |
| LE3 | User-issue detection | Sense | **new** |
| LE4 | Cross-source mining inside the product | Sense | J3 |
| LE5 | Automated diagnosis | Diagnose and propose | **new** |
| LE6 | Ranked, evidence-backed proposals for change | Diagnose and propose | M1 |
| LE7 | Turns its own operating experience into candidate changes | Learn from experience | P1 |
| LE8 | Learned changes are validated before they take effect | Learn from experience | P2 |
| LE9 | Post-change impact measured against a declared baseline | Measure | M4 |

### V — Vet (governance)

Is every change safe, accountable and reversible, including the changes the product makes to itself?

| ID | Criterion | Area | From |
|---|---|---|---|
| VT1 | Accessibility inherited and continuously verified | Compliance and security | E1 |
| VT2 | Audit over entities, definition changes and approvals | Compliance and security | E2 |
| VT3 | Privacy classification, export, erasure and retention | Compliance and security | E3 |
| VT4 | Security as infrastructure | Compliance and security | E4 |
| VT5 | Definitions and layouts versioned with rollback | Change control | F1 |
| VT6 | Proposal, review and apply as a first-class object with preview | Change control | F2 |
| VT7 | Policy-based apply with a movable human boundary | Change control | F3 |
| VT8 | Upgrade safety | Change control | F4 |
| VT9 | Agent-safe actions | AI and self-change safety | K3 |
| VT10 | Bounded self-change | AI and self-change safety | **new** |
| VT11 | Learning-input integrity | AI and self-change safety | **new** |

### E — Expand

Can the product grow into adjacent value, and does it notice where to grow?

| ID | Criterion | Area | From |
|---|---|---|---|
| EX1 | Kernel concepts are domain-neutral | Expressible | O1 |
| EX2 | A new domain is expressible without kernel change | Expressible | O2 |
| EX3 | A domain ships as an installable bundle | Expressible | O3 |
| EX4 | Unmet-demand sensing | Discover | **new** |
| EX5 | Evidence-backed opportunity proposals | Discover | **new** |
| EX6 | Cohort launch with keep-or-kill | Launch | **new** |

v0.3 only asked whether a product *could* express a new domain (EX1–EX3). EX4–EX6 ask whether it *notices* the demand, *proposes* the expansion with evidence, and *launches* it safely to a small group first.

## 5. Anchored levels for the new criteria

The 49 carried-over criteria keep their v0.3 anchors in `references/rubric.md`, with the section 8 clarifications.

### EL2 Safe schema and data migrations
Schema and data changes, including changes the product makes to its own definitions, run without downtime or data loss and can be reversed.
- **0** Schema changes are manual SQL or ad-hoc scripts.
- **1** Versioned migration files, applied by engineers; no rollback path or online strategy.
- **2** Migration framework with up and down steps; long-running or locking changes are handled by convention only.
- **3** Migrations are tested in CI against representative data; destructive changes use an expand-and-contract or online strategy enforced by tooling; definition changes made at runtime are migrated by the same mechanism.
- **4** The product plans, previews and validates migrations for AI-authored or self-made changes, refuses unsafe ones by policy, and can roll them back automatically.

### EL3 Horizontal scale and asynchronous work
- **0** Single process holding state; long work runs in the request path.
- **1** Background work exists but is ad hoc (threads, cron in the web process).
- **2** A job queue with retries; services can run as multiple instances with documented caveats.
- **3** Stateless services by design; queued work is idempotent, retried with back-off and dead-lettered; scale-out is documented and supported.
- **4** Workers and services scale automatically on load signals, with per-tenant fairness in the queues.

### EL5 Measured capacity and service objectives (extends G3)
Adds to G3: level 3 requires published service objectives (latency, availability or throughput) for core paths; level 4 requires those objectives to be monitored in the product and to feed rollout or rollback decisions.

### EL6 Failure isolation and graceful degradation
A failing plugin, connector, AI provider or tenant workload does not take the core product down.
- **0** One failing dependency fails the whole product.
- **1** Errors are caught locally; no timeouts or isolation policy.
- **2** Timeouts and retries on outbound calls; some components degrade gracefully.
- **3** Timeouts, circuit breakers or bulkheads around external calls, plugins and AI providers, with tested fallbacks; failures are contained to the affected feature or tenant.
- **4** Degradation modes are declared per capability, exercised by automated fault injection, and switched by policy.

### EL7 Backup, restore and disaster recovery
- **0** No supported backup.
- **1** Documentation tells operators to back up the database themselves.
- **2** A built-in or documented backup command covering data and definitions; restore is manual and untested.
- **3** Backup and restore of data, definitions and uploaded files is supported, restore is exercised by automated tests, and recovery objectives (RPO, RTO) are stated.
- **4** Point-in-time recovery, per-tenant restore, and restore drills with recorded results.

### VE1 Request intake into a structured change specification
A user or operator request becomes a specification precise enough to build and test.
- **0** Requests live outside the product (email, chat).
- **1** A feedback or feature-request form stores free text.
- **2** Requests are captured in the product with structure (affected area, requester, examples), linked to the entities or screens involved.
- **3** The product turns a request into a structured change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms.
- **4** The specification is machine-readable, drives the AI implementation lane and tests directly, and the product asks clarifying questions when the request is ambiguous.

### VE9 Staged rollout, feature flags and kill switch
- **0** Every change reaches every user at once.
- **1** Configuration toggles exist but are global and code-defined.
- **2** Feature flags or per-tenant enablement exist for some changes.
- **3** Any change class (code, definition or learned change) can be rolled out to a cohort, tenant or percentage first, with a kill switch that takes effect without a release.
- **4** Rollouts progress or halt automatically on measured health and impact signals, under policy.

### LE3 User-issue detection
The product detects that users are struggling, not only that servers are failing.
- **0** No error or usage visibility in the product.
- **1** Server logs and error tracking exist for engineers.
- **2** User-facing errors and failed actions are recorded with the product area involved and can be queried.
- **3** The product detects friction patterns (repeated failures, abandoned flows, retries, corrections, negative feedback, support requests) and raises them as issues attributed to a capability, with affected users and frequency.
- **4** Detected issues are prioritised by impact and fed automatically into diagnosis and the change path.

### LE5 Automated diagnosis
- **0** None.
- **1** Raw traces or logs that engineers read.
- **2** The product groups related failures and attaches context (traces, inputs, recent changes).
- **3** For a detected issue, the product produces a reproducible case and a likely cause, linked to the definition, change or code area responsible, for a person to confirm.
- **4** Diagnosis is validated by reproducing the failure and checking the proposed fix against it before the fix is proposed.

### VT10 Bounded self-change
Explicit limits on what the product, its AI lanes and its learning loops may change on their own.
- **0** Self-modifications or AI-authored changes are unrestricted.
- **1** Limits exist only as prompt instructions or convention.
- **2** A configured allow-list or deny-list of what may be changed, enforced in code for some change paths.
- **3** Every self-change path is enforced against a declared scope (which surfaces, which tenants, how many changes per period) with a blast-radius limit; out-of-scope changes are blocked and logged.
- **4** Scopes are policy, versioned and reviewed like other definitions, with automatic tightening after a failed or reverted change.

### VT11 Learning-input integrity
The signals, memories and feedback that drive learning cannot easily be poisoned or used to inject instructions.
- **0** Any input can be written straight into memory, skills or rules.
- **1** Inputs are stored with no provenance.
- **2** Learned items record their source; some inputs are filtered or sanitised.
- **3** Provenance is recorded for every learned change; untrusted inputs are separated from instructions, scanned for injection, and cannot alone trigger an auto-applied change.
- **4** Learned changes are traceable to inputs, can be bulk-reverted by source, and adversarial inputs are part of the automated evaluation.

### EX4 Unmet-demand sensing
The product notices what users try to do that it does not serve.
- **0** None.
- **1** Free-text feedback only.
- **2** The product records unmet intents in queryable form: failed searches, unsupported requests to an assistant, feature requests, or heavy workaround use (custom fields, exports, external tools).
- **3** It clusters these signals into themes outside its current domain scope, with volume, trend and affected segments.
- **4** Demand signals are combined across tenants under privacy controls and continuously refreshed.

### EX5 Evidence-backed opportunity proposals
- **0** None.
- **1** The product can surface raw demand data only.
- **2** It drafts an adjacent-capability proposal on request (for example "a course module"), citing some evidence.
- **3** It proposes adjacent capabilities on its own, each with evidence, sizing, fit with existing concepts (which entities, bundles and connectors it reuses) and a success metric, ranked for a person to decide.
- **4** Proposals include a buildable specification and a prototype assembled from bundles or the AI lane.

### EX6 Cohort launch with keep-or-kill
- **0** New domains launch to everyone or not at all.
- **1** Manual beta by engineering.
- **2** A new capability or bundle can be enabled for selected tenants or users.
- **3** An expansion launches to a cohort with a declared success metric, a review date and a clean removal path; the keep-or-kill decision is recorded.
- **4** The product measures the cohort against the metric and recommends keep, extend or kill under policy.

## 6. How each loop's level is computed

A stage condition such as `VE4 ≥ 3` uses the criterion's effective score (after caps). `Open` means the Open capability score. "Gates" means every applicable hard gate passes (section 7).

### Request → Release

| Level | Conditions (in addition to the level below) |
|---|---|
| L1 | Build: `Open ≥ 2` or `VE4 ≥ 2`; versioning: `VT5 ≥ 2` |
| L2 | `VE1 ≥ 2`, `VE4 ≥ 2`, `VE5 ≥ 2` |
| L3 | `VE1 ≥ 3`, `VE4 ≥ 3`, `VE5 ≥ 3`, `VE6 ≥ 3`, `VT6 ≥ 2`, `VE9 ≥ 2`; gates |
| L4 | `VT7 ≥ 3`, `VE9 ≥ 3`, `LE9 ≥ 3`, `VT10 ≥ 3`; gates at depth *tested* |
| L5 | Every criterion named above at 4; gates and `LE9`, `VT7` at depth *operated* |

### Issue → Fix

| Level | Conditions (in addition to the level below) |
|---|---|
| L1 | `LE3 ≥ 2`; build: `Open ≥ 2` or `VE4 ≥ 2`; `VT5 ≥ 2` |
| L2 | `LE5 ≥ 2`, `LE6 ≥ 2`, `VE5 ≥ 2` |
| L3 | `LE3 ≥ 3`, `LE5 ≥ 3`; fix: `VE4 ≥ 3`, or `LE7 ≥ 3` with `LE8 ≥ 2`; `VE5 ≥ 3`, `VT6 ≥ 2`, `VE9 ≥ 2`, `LE9 ≥ 2`; gates |
| L4 | `VT7 ≥ 3`, `VE9 ≥ 3`, `LE9 ≥ 3`, `VT10 ≥ 3`, `VT11 ≥ 3`; gates at depth *tested* |
| L5 | Every criterion named above at 4; gates and `LE9`, `VT7` at depth *operated* |

### Opportunity → Expansion

| Level | Conditions (in addition to the level below) |
|---|---|
| L1 | `EX2 ≥ 2`, `VT5 ≥ 2` |
| L2 | `EX4 ≥ 2`, `EX5 ≥ 2` |
| L3 | `EX4 ≥ 3`, `EX5 ≥ 3`; assemble: `EX3 ≥ 3` or `VE4 ≥ 3`; `VT6 ≥ 2`, `EX6 ≥ 2`; gates |
| L4 | `EX6 ≥ 3`, `VT7 ≥ 3`, `LE9 ≥ 3`, `VT10 ≥ 3`; gates at depth *tested* |
| L5 | Every criterion named above at 4; gates and `LE9`, `VT7` at depth *operated* |

The scorer reports, for each loop, the level reached and the exact conditions that block the next level. This replaces v0.3's single closed-loop yes or no.

## 7. Hard gates

Some controls are not averageable: missing one makes autonomous change dangerous however good everything else is. Failing any applicable gate caps every loop at **L2**: the product may draft, but people must build and release.

| Gate | Passes when | Applies |
|---|---|---|
| Rollback | `VT5 ≥ 3` | always |
| Safe migrations | `EL2 ≥ 3` | always |
| Tested backup and restore | `EL7 ≥ 3` | always |
| Tenant isolation | `EL4 ≥ 3` | multi-tenant products only |
| Security as infrastructure | `VT4 ≥ 3` | always |
| Bounded self-change | `VT10 ≥ 3` and `LE8 ≥ 2` | when any self-change path is on by default (`LE7 ≥ 3`, or `VT7 ≥ 3` allowing automatic apply) |

The last gate is conditional. It catches products that already change themselves by default without limits; agent runtimes that write their own skills and memory out of the box are the current example.

## 8. Scoring rules: carried over and changed

Carried over from v0.3 unchanged: score what ships; score the default configuration and record opt-ins as `available_score`; first-party companion repositories are in scope; the self rule; evidence grades with the grade C cap; the single-entity cap; the incident deduction; `not_evidenced` scores 0 by default and is excluded in the assessed-only reading; rounding half up, once.

**Changed:**

1. **Evidence depth.** Every assessed criterion records `depth`: `designed` (the code or documentation exists), `tested` (automated tests in the repository exercise it), or `operated` (records of it working in production: drill reports, incident reviews, dashboards). For Elastic criteria and every gate criterion, a 3 needs `tested` and a 4 needs `operated`; otherwise the score is capped at 2. A repository alone cannot prove production behaviour, and this makes that limit visible instead of silent.
2. **`alt_score` is only ever the higher reading** (`score + 1`). The rubric already said "take the lower level"; the validator now enforces it. The 49 downward alternates in the September field test will be flipped. With this rule the default reading is also the low end of every range.
3. **Round 2 boundary clarifications**, from the inter-rater study (118 of 132 exact agreement):
   - **VT5 (F1)** scores the surfaces in the product's change-surface inventory. Level 3 needs versioning and rollback on the surfaces operators change by default, including any the product modifies itself; uncovered surfaces are listed.
   - **LE9 (M4)** is post-apply measurement only. Validation before a change takes effect belongs to LE8 (P2).
   - **VT7 (F3)** covers policies over changes to the product's own definitions and behaviour, including self-modification. Per-action tool permissions belong to VT9 (K3).
   - **VE4 (M3)** credits an AI lane that changes this product (its definitions, or its own code through its committed pipeline), not AI features that change users' other software.
4. **Code-path evidence.** VE1, VE4 and VE9 may be met by tooling committed to the product's repositories (for example a workflow that turns an accepted issue into a tested pull request). Team practices that leave no artefact in scope are not scored, consistent with "not a delivery-process audit".

## 9. Archetypes

The five archetypes stay. Exclusions map to the new IDs:

| Archetype | May exclude |
|---|---|
| configurable-application-platform | nothing |
| focused-application | OP1, OP3, OP4, OP5, OP8 and EX1–EX3 (not EX4–EX6: a focused product should still notice unmet demand) |
| agent-runtime | OP1–OP5, OP8, EL1 |
| developer-platform | OP7–OP9, VT1, only with no end-user interface |
| other | anything, with a rationale |

EL4 and its gate may be excluded by any archetype that is single-tenant by design.

## 10. Report format

```
EVOLVE assessment: <product> EL <tip>, <date>, archetype <type>

SAL 2  ·  Request → Release L3  ·  Issue → Fix L2  ·  Expansion L1
         (with opt-in settings: SAL 3)
Gates: rollback ✓  migrations ✓  backup ✗ (EL7 = 2, designed only)  isolation n/a  security ✓  self-change ✓

Profile      Elastic 2.1  Velocity 2.7  Open 2.6  Learn 2.0 (2.0–2.6)  Vet 2.3  Expand 1.2
Next level   Issue → Fix L3 is blocked by: LE5 = 1 (needs 3), LE9 = 1 (needs 2)
```

Plus the per-criterion table, evidence, ranges, caps applied and the remediation plan, as today.

## 11. What moves from MSR v0.3, and why

| Old ID | New ID | | Old ID | New ID | | Old ID | New ID |
|---|---|---|---|---|---|---|---|
| A1–A3 | OP1–OP3 | | G1 | EL1 | | J1, J2 | LE1, LE2 |
| B1–B3 | OP4–OP6 | | G2 | EL4 | | J3 | LE4 |
| C1–C3 | OP7–OP9 | | G3 | EL5 | | M1 | LE6 |
| D1–D3 | OP10–OP12 | | H1, H2 | VE2, VE3 | | M3 | VE4 |
| E1–E4 | VT1–VT4 | | H3 | VE5 | | M4 | LE9 |
| F1–F4 | VT5–VT8 | | L1–L3 | VE6–VE8 | | P1, P2 | LE7, LE8 |
| I1–I3 | OP13–OP15 | | K1, K2 | OP19, OP20 | | O1–O3 | EX1–EX3 |
| N1–N3 | OP16–OP18 | | K3 | VT9 | | | |

Why:

- **G and K return to the headline.** v0.3 left them only in profiles, which hid architecture and agent readiness from the headline. That was a mistake. G becomes the core of Elastic; K1 and K2 join Open; K3 joins Vet.
- **M3 moves to Velocity.** Implementing a change is building, not learning, and the move lets the code path count.
- **O moves to Expand**, joined by the new criteria that ask whether the product finds its adjacent opportunities.
- **Learning and Factory stay separate capabilities** but feed the same loops. Averaging them would hide which half of the loop is broken.
- **The closed-loop flag becomes three loop levels**, so "how far along" is visible instead of a single yes or no.
- **The name changes from MSR to EVOLVE.** "Malleable software" is an established term for user-reshapable tools and described only one capability. Before formal launch, run a trademark and prior-use check; a first search found no software-readiness framework of this name (there is an "A-EVOLVE" research term for closed-loop systems).

## 12. Delivery plan once agreed

1. Rubric: renumber, add the 13 new criteria, the loop conditions, gates, depth and archetype table; machine-readable model block updated.
2. Scorer: loop levels with blocking conditions, gates, depth caps, upward-only `alt_score`; tests for each.
3. Migration script from v0.3 assessments (ID mapping, flip downward alternates).
4. Field test: score the 13 new criteria and depth for the 11 systems, add the `OpenHands/automation` repository, publish SAL results.
5. Inter-rater: add the Round 2 dataset (mapped to new IDs) and run a second rater on the new criteria.
6. Rename the skill, README and metadata; changelog entry disclosing every move above.

## 13. Open decisions

1. **Headline SAL = lower of Request → Release and Issue → Fix**, with Expansion beside it. Or should Expansion count in the headline?
2. **Gates cap at L2.** Is that the right cap, and is the gate list complete?
3. **Depth rule** caps Elastic and gate criteria at 2 without tested evidence. Too strict for repository-only assessments, or right?
4. **Code-path evidence** (section 8.4): acceptable widening of scope?
5. **Repository name**: keep `malleablesoftware` for now, or rename (for example `evolve`) with this release?
