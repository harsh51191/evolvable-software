# EVOLVE v0.4: specification draft (revision 2)

**Status: implemented on this branch for review, not yet merged.** `references/rubric.md`, `scripts/score.py` and the field test now implement this specification. "EVOLVE" and "SAL" are working names, not final (section 13). Decisions already taken are recorded in section 15; section 16 records where the implementation refined this text.

**Revision 2 changes**, from review of revision 1:

1. Architecture now caps every loop through an Architecture Foundation level (section 7.3). In revision 1 most architecture criteria could not affect the headline.
2. One shared release spine (Build → Verify → Stage → Release → Observe → Roll back) used by all three loops, replacing three slightly different lists. Automatic rollback is now required at L4, not just described (section 7.1).
3. Hard gates apply according to declared scope facts, and code-release rollback is separate from configuration rollback (sections 5 and 7.5).
4. Repository tooling counts only when it is a supported, first-party evolution system for the product (section 8.4).
5. Bundled architecture criteria split; multi-surface criteria use a coverage inventory (sections 4 and 8.3).
6. Descriptive IDs (`ARC-01`, `DEL-01`, ...) replace `EL`, `VE`, `LE`, `VT`, which were easy to confuse. Name not locked.

## 1. The question EVOLVE answers

> How ready is a software product to evolve itself safely?

It breaks into three **loops**:

| Loop | The product can... | Example |
|---|---|---|
| **Request → Release** | take a user or operator request, implement it properly and release it | "Add an approval step to expense claims" goes live for that customer |
| **Issue → Fix** | find problems users face, fix them and ship the fix | Users keep failing at checkout; the product finds why, fixes it and confirms the failures stopped |
| **Opportunity → Expansion** | notice adjacent needs it does not yet serve, and propose or launch them | A community platform sees members selling courses and proposes a course (LMS) module; a professional network sees skill posts and proposes gig matching |

**What EVOLVE measures.** The product as shipped: its code, configuration, first-party companion repositories and documentation. It does not measure a team's delivery performance. It is also not an autonomy scale for AI coding assistants, which ask how independently an AI writes code; EVOLVE asks whether the *product* is built to be changed by request, to fix itself and to grow, safely.

## 2. How a loop's level is decided

```
Loop level = min( loop stages,              what this loop specifically needs (section 7.2)
                  release spine,            build, verify, stage, release, observe, roll back (7.1)
                  architecture foundation,  can the system take the change and survive it (7.3)
                  governance ceiling )      is the change safe, accountable and bounded (7.4)

Headline SAL = min( Request → Release, Issue → Fix )
Expansion level is reported beside the headline, not inside it.
```

Every condition is a threshold on named criteria, so the scorer can always say exactly what blocks the next level.

## 3. Software Autonomy Levels (SAL)

| Level | Name | What the product can do in that loop |
|---|---|---|
| **L0** | Manual | Every change is engineers writing and releasing code. |
| **L1** | Configurable | People make the change without bespoke engineering, through governed configuration or an AI-drafted change they finish, and can roll it back. |
| **L2** | Assisted | The product does the thinking work: structures the request, diagnoses the issue or drafts the proposal, and drafts the change. People build, check and release. |
| **L3** | Supervised | The product carries the loop end to end, including verification, staged release and rollback. A person approves each release. Every applicable critical control passes. |
| **L4** | Policy-bounded | Low-risk change classes ship without a person, under explicit policy, with staged exposure, impact measurement and **automatic** rollback, on an architecture with tested evidence. People handle exceptions. |
| **L5** | Self-directing | Across change classes, the product initiates, ships and measures change within policy; people set policy and goals. Backed by operational evidence, not only code. |

Levels are cumulative: a level requires every condition for it and for all lower levels.

> Example headline: **SAL 2** · Request → Release L3 · Issue → Fix L2 · Expansion L1

## 4. Capabilities and criteria

EVOLVE is the profile of six capabilities. The letters are the display names; IDs use descriptive prefixes that survive any rename.

| Letter | Capability | ID prefix | Criteria |
|---|---|---|---|
| E | Elastic | `ARC` architecture | 9 |
| V | Velocity | `DEL` delivery | 11 |
| O | Open | `MAL` malleability | 20 |
| L | Learn | `LRN` learning | 9 |
| V | Vet | `GOV` governance | 11 |
| E | Expand | `EXP` expansion | 6 |

66 criteria: 49 carried over from MSR v0.3, 17 new. All use the v0.3 ladder (0 absent, 1 code-only, 2 mechanism, 3 productised, 4 generative and policy-gated). A capability score is the mean of its area means. "Applies when" refers to the scope facts in section 5; otherwise the criterion always applies.

### Elastic: architecture (`ARC`)

| ID | Criterion | Area | Applies when | From |
|---|---|---|---|---|
| ARC-01 | Indexed query path, never a scan of a generic store | Data | persistent_data | G1 |
| ARC-02 | Safe schema and data migrations | Data | schema_changes | **new** |
| ARC-03 | Horizontal scale of services | Scale | hosted_service | **new** |
| ARC-04 | Reliable asynchronous work | Scale | hosted_service | **new** |
| ARC-05 | Tenant isolation and noisy-neighbour controls | Scale | multi_tenant | G2 |
| ARC-06 | Capacity ceilings measured | Capacity | hosted_service | G3 |
| ARC-07 | Service objectives defined and monitored | Capacity | hosted_service | **new** |
| ARC-08 | Failure isolation and graceful degradation (inventory) | Resilience | always | **new** |
| ARC-09 | Backup, restore and recovery (inventory) | Resilience | persistent_data | **new** |

### Velocity: delivery (`DEL`)

| ID | Criterion | Area | From |
|---|---|---|---|
| DEL-01 | Request intake into a structured change specification | Intake | **new** |
| DEL-02 | Layers deploy independently | Build | H1 |
| DEL-03 | Module boundaries enforced by tooling | Build | H2 |
| DEL-04 | AI implementation lane | Build | M3, moved from Learning |
| DEL-05 | Every change class has an automated pre-land check | Verify | H3 |
| DEL-06 | Verification surface | Verify | L1 |
| DEL-07 | Environment reproducibility | Verify | L2 |
| DEL-08 | Machine-verifiable release evidence | Verify | L3 |
| DEL-09 | Staged exposure | Release | **new** |
| DEL-10 | Kill switch | Release | **new** |
| DEL-11 | Release rollback (applies when code_release_path) | Release | **new** |

DEL-04 credits both ways a change gets built: an AI that authors governed definitions, and an AI lane that turns an accepted request into a tested code change. The code lane counts only under the rule in section 8.4.

### Open: malleability (`MAL`)

| ID | Criterion | Area | From |
|---|---|---|---|
| MAL-01 – MAL-03 | Entity types; field definitions; relationships and lifecycle as data | Data model | A1–A3 |
| MAL-04 – MAL-06 | Generated APIs; runtime reshaping; machine-readable contract | APIs | B1–B3 |
| MAL-07 – MAL-09 | Layout as data; generic widgets; theme and text as data | Interface | C1–C3 |
| MAL-10 – MAL-12 | Rules engine; event model; sandboxed hooks | Behaviour | D1–D3 |
| MAL-13 – MAL-15 | Plugin lanes; plugin isolation; developer loop | Extensions | I1–I3 |
| MAL-16 – MAL-18 | Canonical data model; connector SDK; versioned contracts | Integrations | N1–N3 |
| MAL-19 – MAL-20 | Capability surface for agents; conversational operation and authoring | Agent interface | K1–K2 |

### Learn: learning (`LRN`)

| ID | Criterion | Area | From |
|---|---|---|---|
| LRN-01 | Telemetry accessible to the product in near real time | Sense | J1 |
| LRN-02 | Structured learning signals | Sense | J2 |
| LRN-03 | User-issue detection | Sense | **new** |
| LRN-04 | Cross-source mining inside the product | Sense | J3 |
| LRN-05 | Automated diagnosis | Diagnose and propose | **new** |
| LRN-06 | Ranked, evidence-backed proposals for change | Diagnose and propose | M1 |
| LRN-07 | Turns its own operating experience into candidate changes | Learn from experience | P1 |
| LRN-08 | Learned changes are validated before they take effect | Learn from experience | P2 |
| LRN-09 | Post-change impact measured against a declared baseline | Measure | M4 |

### Vet: governance (`GOV`)

| ID | Criterion | Area | From |
|---|---|---|---|
| GOV-01 | Accessibility inherited and continuously verified | Compliance and security | E1 |
| GOV-02 | Audit over entities, definition changes and approvals | Compliance and security | E2 |
| GOV-03 | Privacy classification, export, erasure and retention | Compliance and security | E3 |
| GOV-04 | Security as infrastructure | Compliance and security | E4 |
| GOV-05 | Definitions versioned with rollback (inventory) | Change control | F1 |
| GOV-06 | Proposal, review and apply as a first-class object with preview | Change control | F2 |
| GOV-07 | Policy-based apply with a movable human boundary | Change control | F3 |
| GOV-08 | Upgrade safety | Change control | F4 |
| GOV-09 | Agent-safe actions (applies when agent_mutations) | AI and self-change safety | K3 |
| GOV-10 | Bounded self-change | AI and self-change safety | **new** |
| GOV-11 | Learning-input integrity | AI and self-change safety | **new** |

### Expand: expansion (`EXP`)

| ID | Criterion | Area | From |
|---|---|---|---|
| EXP-01 | Kernel concepts are domain-neutral | Expressible | O1 |
| EXP-02 | A new domain is expressible without kernel change | Expressible | O2 |
| EXP-03 | A domain ships as an installable bundle | Expressible | O3 |
| EXP-04 | Unmet-demand sensing | Discover | **new** |
| EXP-05 | Evidence-backed opportunity proposals | Discover | **new** |
| EXP-06 | Cohort launch with keep-or-kill | Launch | **new** |

## 5. Scope facts

Each assessment declares these facts, each with evidence. They decide which criteria and critical controls apply, so a stateless library is not failed on backups and a single-user tool is not failed on tenant isolation. A fact that is wrongly declared is a validation finding, not a shortcut.

| Fact | True when | Turns on |
|---|---|---|
| `persistent_data` | The product stores durable user, tenant or operator data | ARC-01, ARC-09 and the backup control |
| `schema_changes` | The product, or its evolution path, changes stored data structures (database schema or definition-driven storage) | ARC-02 and the migration control |
| `multi_tenant` | One deployment serves several isolated tenants, workspaces or organisations | ARC-05 and the isolation control |
| `hosted_service` | It runs as a long-lived networked service rather than a library, CLI or local single-user tool | ARC-03, ARC-04, ARC-06, ARC-07 |
| `machine_actions` | Agents or automated clients can change the product's data or definitions through an API or tool surface | GOV-09 |
| `agent_mutations` | The product's own agents or AI can change its definitions, skills, memory, configuration or data | GOV-10, GOV-11 and the self-change control |
| `evolution_auto_apply` | A change produced by the evolution loop applies without human approval by default (scheduled maintenance does not count) | GOV-10, GOV-11 and the self-change control |
| `definition_change_path` | Behaviour changes are made through definitions or configuration | GOV-05 and the definition-rollback control |
| `code_release_path` | The product's evolution system ships code changes, not only definition changes | DEL-11 and the release-rollback control |

At least one change path must be true, and rollback is required on each path that exists. (Revision 2 listed seven facts; section 16 explains the two added and the one renamed.)

## 6. Anchored levels for the new criteria

The 49 carried-over criteria keep their v0.3 anchors in `references/rubric.md`, with the clarifications in section 9.

### ARC-02 Safe schema and data migrations
- **0** Schema changes are manual SQL or ad-hoc scripts.
- **1** Versioned migration files applied by engineers; no rollback path or online strategy.
- **2** Migration framework with up and down steps; locking or long-running changes handled by convention.
- **3** Migrations tested in CI against representative data; destructive changes use expand-and-contract or another online strategy enforced by tooling; definition changes made at runtime are migrated by the same mechanism.
- **4** The product plans, previews and validates migrations for AI-authored or self-made changes, refuses unsafe ones by policy, and can reverse them automatically.

### ARC-03 Horizontal scale of services
- **0** A single process that holds state in memory or on local disk.
- **1** Multiple instances possible only with sticky sessions or manual coordination.
- **2** Multiple instances supported, with documented caveats (local caches, singletons, file storage).
- **3** Stateless services by design: shared state in managed stores, scale-out documented and exercised by tests or deployment manifests.
- **4** Services scale automatically on load signals, with scale-out behaviour verified in a performance environment.

### ARC-04 Reliable asynchronous work
- **0** Long work runs in the request path.
- **1** Background work is ad hoc (threads, cron inside the web process).
- **2** A job queue with retries.
- **3** Queued work is idempotent, retried with back-off, dead-lettered and observable; scheduled jobs run once across instances.
- **4** Per-tenant fairness and priorities in the queues, with back-pressure under load.

### ARC-07 Service objectives defined and monitored
- **0** None.
- **1** Uptime checks only.
- **2** Latency or error metrics exported for core paths; no stated objectives.
- **3** Published objectives (latency, availability or throughput) for core paths, monitored with alerts.
- **4** Objectives and error budgets feed release decisions: rollout pauses or rolls back when a change burns the budget.

### ARC-08 Failure isolation and graceful degradation (inventory)
Inventory: connectors and integrations, plugins and extensions, AI and model providers, tenant workloads, internal services. The score is the level every applicable surface reaches.
- **0** One failing dependency fails the whole product.
- **1** Errors caught locally; no timeouts or isolation policy.
- **2** Timeouts and retries on outbound calls; some surfaces degrade gracefully.
- **3** Every surface in the inventory has timeouts and circuit breakers or bulkheads, with tested fallbacks; a failure is contained to the affected feature or tenant.
- **4** Degradation modes declared per capability, exercised by automated fault injection and switched by policy.

### ARC-09 Backup, restore and recovery (inventory)
Inventory: data, definitions and configuration, uploaded files, secrets and keys. The score is the level every applicable item reaches.
- **0** No supported backup.
- **1** Documentation tells operators to back up the database themselves.
- **2** A built-in or documented backup command; restore manual and untested.
- **3** Backup and restore supported for every inventory item, restore exercised by automated tests, recovery objectives (RPO, RTO) stated.
- **4** Point-in-time and per-tenant restore, with recorded restore drills.

### DEL-01 Request intake into a structured change specification
- **0** Requests live outside the product (email, chat).
- **1** A feedback or feature-request form stores free text.
- **2** Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- **3** The product turns a request into a change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms.
- **4** The specification is machine-readable and drives the implementation lane and tests directly; the product asks clarifying questions when a request is ambiguous.

### DEL-09 Staged exposure
- **0** Every change reaches every user at once.
- **1** Global configuration toggles defined in code.
- **2** Feature flags or per-tenant enablement for some changes.
- **3** Any change class (code, definition or learned change) can go to a cohort, tenant or percentage first.
- **4** Exposure progresses or halts automatically on measured health and impact signals, under policy.

### DEL-10 Kill switch
- **0** Disabling a change needs a release.
- **1** Disabling needs an engineer to edit configuration and restart.
- **2** Some features can be switched off at runtime.
- **3** Any change shipped by the evolution system can be switched off at runtime, per tenant or globally, without a release; use is audited.
- **4** The kill switch triggers automatically on health or impact signals, under policy.

### DEL-11 Release rollback (code path)
GOV-05 covers rolling back definitions. This covers rolling back a code release.
- **0** No rollback; fixes roll forward only.
- **1** Rollback by rebuilding an old version by hand.
- **2** Previous versions can be redeployed; data compatibility not ensured.
- **3** One-step rollback to the previous release, tested, with schema and data changes kept backward-compatible across one release.
- **4** Rollback triggers automatically when verification, health or impact signals fail after release.

### LRN-03 User-issue detection
- **0** No error or usage visibility in the product.
- **1** Server logs and error tracking for engineers.
- **2** User-facing errors and failed actions recorded with the product area and queryable.
- **3** The product detects friction patterns (repeated failures, abandoned flows, retries, corrections, negative feedback, support requests) and raises them as issues attributed to a capability, with affected users and frequency.
- **4** Detected issues are prioritised by impact and fed automatically into diagnosis and the change path.

### LRN-05 Automated diagnosis
- **0** None.
- **1** Raw traces or logs that engineers read.
- **2** The product groups related failures and attaches context (traces, inputs, recent changes).
- **3** For a detected issue, the product produces a reproducible case and a likely cause, linked to the responsible definition, change or code area, for a person to confirm.
- **4** Diagnosis is validated by reproducing the failure and checking the proposed fix against it before the fix is proposed.

### GOV-10 Bounded self-change
- **0** Self-modifications or AI-authored changes are unrestricted.
- **1** Limits exist only as prompt instructions or convention.
- **2** An allow-list or deny-list of what may change, enforced in code for some change paths.
- **3** Every self-change path is enforced against a declared scope (surfaces, tenants, changes per period) with a blast-radius limit; out-of-scope changes are blocked and logged.
- **4** Scopes are versioned, reviewed policy, tightened automatically after a failed or reverted change.

### GOV-11 Learning-input integrity
Covers every input that can drive a change: requests, feedback, telemetry, memories and documents.
- **0** Any input can be written straight into memory, skills, rules or a change.
- **1** Inputs stored with no provenance.
- **2** Changes record their source inputs; some inputs are filtered.
- **3** Provenance recorded for every learned or AI-built change; untrusted inputs are separated from instructions, scanned for injection, and cannot alone trigger an automatically applied change.
- **4** Changes can be bulk-reverted by source, and adversarial inputs are part of the automated evaluation.

### EXP-04 Unmet-demand sensing
- **0** None.
- **1** Free-text feedback only.
- **2** Unmet intents recorded in queryable form: failed searches, unsupported requests to an assistant, feature requests, heavy workaround use (custom fields, exports, external tools).
- **3** These signals are clustered into themes outside the current domain scope, with volume, trend and affected segments.
- **4** Demand signals combined across tenants under privacy controls and refreshed continuously.

### EXP-05 Evidence-backed opportunity proposals
- **0** None.
- **1** Raw demand data only.
- **2** Drafts an adjacent-capability proposal on request, citing some evidence.
- **3** Proposes adjacent capabilities on its own, each with evidence, sizing, fit with existing concepts (which entities, bundles and connectors it reuses) and a success metric, ranked for a person to decide.
- **4** Proposals include a buildable specification and a prototype assembled from bundles or the implementation lane.

### EXP-06 Cohort launch with keep-or-kill
- **0** New domains launch to everyone or not at all.
- **1** Manual beta run by engineering.
- **2** A new capability or bundle can be enabled for selected tenants or users.
- **3** An expansion launches to a cohort with a declared success metric, a review date and a clean removal path; the keep-or-kill decision is recorded.
- **4** The product measures the cohort against the metric and recommends keep, extend or kill under policy.

## 7. Level conditions

A condition such as `DEL-05 ≥ 3` uses the criterion's effective score after caps. A criterion that is not applicable under the scope facts is skipped. "Open" means the Open capability score.

### 7.1 Release spine (all three loops)

**Build path.** How the loop gets a change built:

| Loop | People build it with | The product builds it with |
|---|---|---|
| Request → Release | Open (governed configuration) | DEL-04 |
| Issue → Fix | Open | DEL-04, or LRN-07 with LRN-08 ≥ 2 |
| Opportunity → Expansion | EXP-02 | DEL-04, or EXP-03 |

**Rollback path.** GOV-05 for definition changes; DEL-11 as well when `code_release_path` is true. The spine uses the lower of the two.

| Stage | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|
| **Build** | people's path ≥ 2, or product's path ≥ 2 | product's path ≥ 2 | product's path ≥ 3 | product's path ≥ 3; DEL-02 ≥ 2, DEL-03 ≥ 2 | product's path = 4 |
| **Verify** | – | DEL-05 ≥ 2 | DEL-05 ≥ 3, DEL-06 ≥ 3, DEL-07 ≥ 2, DEL-08 ≥ 2 | DEL-05 – DEL-08 all ≥ 3 | all = 4 |
| **Stage** | – | – | DEL-09 ≥ 2 | DEL-09 ≥ 3 | DEL-09 = 4 |
| **Release** | – | – | DEL-10 ≥ 2 | DEL-10 ≥ 3 | DEL-10 = 4 |
| **Observe** | – | – | LRN-09 ≥ 2 | LRN-09 ≥ 3 | LRN-09 = 4, operated |
| **Roll back** | rollback path ≥ 2 | ≥ 2 | ≥ 3 | = 4 (automatic) | = 4, operated |

### 7.2 Loop stages

| Loop | Stage | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|---|
| Request → Release | Intake: DEL-01 | – | ≥ 2 | ≥ 3 | ≥ 3 | = 4 |
| Issue → Fix | Detect: LRN-03 | ≥ 2 | ≥ 2 | ≥ 3 | ≥ 3 | = 4 |
| | Diagnose: LRN-05 | – | ≥ 2 | ≥ 3 | ≥ 3 | = 4 |
| | Propose: LRN-06 | – | ≥ 2 | ≥ 3 | ≥ 3 | = 4 |
| Opportunity → Expansion | Sense: EXP-04 | – | ≥ 2 | ≥ 3 | ≥ 3 | = 4 |
| | Propose: EXP-05 | – | ≥ 2 | ≥ 3 | ≥ 3 | = 4 |
| | Launch: EXP-06 | – | – | ≥ 2 | ≥ 3 | = 4 |

### 7.3 Architecture foundation (all loops)

| Level | Every applicable ARC criterion | Plus |
|---|---|---|
| L1 | – | – |
| L2 | ≥ 1 (nothing absent) | – |
| L3 | ≥ 2 | ARC-02, ARC-05, ARC-09 ≥ 3 where applicable (critical controls) |
| L4 | ≥ 3 (so tested, by section 8.1) | – |
| L5 | ≥ 3 with operated evidence | ARC-06, ARC-07, ARC-08 = 4 |

This is what stops a product with poor query paths, no horizontal scaling, unknown capacity or weak failure isolation from claiming autonomous release, however good its workflow is.

### 7.4 Governance ceiling (all loops)

| Level | Conditions |
|---|---|
| L1, L2 | – |
| L3 | GOV-04 ≥ 3 (critical control); GOV-02 ≥ 2; GOV-06 ≥ 2; GOV-08 ≥ 2; GOV-09 ≥ 2 if `agent_mutations`; GOV-10 ≥ 3 and LRN-08 ≥ 2 if `agent_mutations` or `automatic_apply` (critical control) |
| L4 | GOV-01 – GOV-04 all ≥ 3 where applicable; GOV-07 ≥ 3; GOV-10 ≥ 3; GOV-11 ≥ 3; GOV-09 ≥ 3 if `agent_mutations` |
| L5 | GOV-07 = 4 and GOV-10 = 4, operated |

### 7.5 Critical controls

These are not averaged. Each is an L3 condition in one of the sections above, so failing any applicable control caps every loop at **L2**: the product may draft, but people build and release.

| Control | Passes when | Applies when | Section |
|---|---|---|---|
| Definition rollback | GOV-05 ≥ 3 | always | 7.1 |
| Release rollback | DEL-11 ≥ 3 | `code_release_path` | 7.1 |
| Safe migrations | ARC-02 ≥ 3 | `schema_changes` | 7.3 |
| Tested backup and restore | ARC-09 ≥ 3 | `persistent_data` | 7.3 |
| Tenant isolation | ARC-05 ≥ 3 | `multi_tenant` | 7.3 |
| Security as infrastructure | GOV-04 ≥ 3 | always | 7.4 |
| Bounded self-change | GOV-10 ≥ 3 and LRN-08 ≥ 2 | `agent_mutations` or `automatic_apply` | 7.4 |

## 8. Evidence rules

### 8.1 Evidence facets and the depth cap
Every assessed criterion records three cumulative facets:

- `implemented`: the capability exists in code or shipped configuration;
- `tested`: automated tests in scope exercise it;
- `operated`: records show it working in production, such as drill reports, incident reviews or dashboards.

The facets are recorded separately so operated evidence never implies tested evidence. `tested` and `operated` both require `implemented`.

**Depth cap.** For every ARC criterion and every critical-control criterion, a 3 needs `implemented` and `tested`, and a 4 needs all three facets. Otherwise the score is capped at 2. A repository alone cannot prove production behaviour; this makes that limit visible.

### 8.2 Grades, defaults and alternates
Carried over: evidence grades A, B, C (C capped at 2); score the default configuration and record opt-ins as `available_score`; `not_evidenced` scores 0 by default and is excluded in the assessed-only reading; single-entity cap; incident deduction; rounding half up, once.

Changed: **`alt_score` is only ever the higher reading** (`score + 1`). The validator enforces the rubric's existing "take the lower level" rule, and the default reading becomes the low end of every range. The 49 downward alternates in the September field test will be flipped.

### 8.3 Coverage inventories
ARC-08, ARC-09 and GOV-05 span several surfaces. The assessment records the inventory of applicable surfaces with a level for each; the criterion score is the level every surface reaches, so one strong surface cannot hide a weak one. The report shows the strongest and weakest surface.

### 8.4 When repository tooling counts
The criteria that make the product drive its own change (DEL-01, DEL-04, DEL-09 – DEL-11, LRN-03, LRN-05 – LRN-07, EXP-04 – EXP-06) count tooling only when it is a **first-party evolution system for this product**. It must be all of:

1. **Executable:** it runs, rather than being described.
2. **Supported:** documented and maintained as part of the product or an official first-party companion.
3. **Bounded:** subject to declared scope limits (GOV-10).
4. **Built to evolve this product** from its requests, issues or opportunities.

A team's ordinary CI, bots or scripts do not qualify. They still count for the verification criteria (DEL-05 – DEL-08), as in v0.3, because those measure whether a change can be verified, not who drives it.

## 9. Round 2 boundary clarifications

From the Round 2 inter-rater study of the v0.3 Learn and Vet criteria. Its dataset is not yet in this repository, so its agreement figures are not quoted; these four boundaries are the ones the two raters disputed:

- **GOV-05 (F1)** scores the inventory of surfaces operators change by default, including any the product modifies itself. Uncovered surfaces are listed.
- **LRN-09 (M4)** is post-apply measurement only. Validation before a change takes effect is LRN-08 (P2).
- **GOV-07 (F3)** covers policies over changes to the product's own definitions and behaviour, including self-modification. Per-action tool permissions are GOV-09 (K3).
- **DEL-04 (M3)** credits a lane that changes this product (its definitions, or its own code under section 8.4), not AI features that change users' other software.

## 10. Archetypes

The five archetypes stay; scope facts now handle applicability for architecture.

| Archetype | May exclude |
|---|---|
| configurable-application-platform | nothing |
| focused-application | MAL-01, MAL-03, MAL-04, MAL-05, MAL-08, EXP-01 – EXP-03 (not EXP-04 – EXP-06: a focused product should still notice unmet demand) |
| agent-runtime | MAL-01 – MAL-05, MAL-08, ARC-01 |
| developer-platform | MAL-07 – MAL-09, GOV-01, only with no end-user interface |
| other | anything, with a rationale |

## 11. Report format

```
EVOLVE assessment: <product> @ <tip>, <date>, archetype <type>
Scope: persistent_data, schema_changes, hosted_service, agent_mutations; not multi_tenant, automatic_apply, code_release_path

SAL 2  ·  Request → Release L2  ·  Issue → Fix L2  ·  Expansion L1   (with opt-in settings: SAL 2)

Request → Release   stages L3 · spine L3 · architecture L2 · governance L3   -> L2
Critical controls   definition rollback ✓  migrations ✓  backup ✗ (ARC-09 = 2: restore untested)  security ✓  self-change ✓

Profile    Elastic 2.1  Velocity 2.7  Open 2.6  Learn 2.0 (2.0–2.6)  Vet 2.3  Expand 1.2
Next level Request → Release L3 is blocked by: ARC-09 = 2 (needs 3, tested), ARC-03 = 1 (needs 2)
```

Plus the per-criterion table, evidence, inventories, ranges, caps applied and the remediation plan.

## 12. What moves from MSR v0.3

| v0.3 | v0.4 | | v0.3 | v0.4 | | v0.3 | v0.4 |
|---|---|---|---|---|---|---|---|
| A1–A3 | MAL-01 – 03 | | G1 | ARC-01 | | J1, J2 | LRN-01, 02 |
| B1–B3 | MAL-04 – 06 | | G2 | ARC-05 | | J3 | LRN-04 |
| C1–C3 | MAL-07 – 09 | | G3 | ARC-06 | | M1 | LRN-06 |
| D1–D3 | MAL-10 – 12 | | H1, H2 | DEL-02, 03 | | M3 | DEL-04 |
| E1–E4 | GOV-01 – 04 | | H3 | DEL-05 | | M4 | LRN-09 |
| F1–F4 | GOV-05 – 08 | | L1–L3 | DEL-06 – 08 | | P1, P2 | LRN-07, 08 |
| I1–I3 | MAL-13 – 15 | | K1, K2 | MAL-19, 20 | | O1–O3 | EXP-01 – 03 |
| N1–N3 | MAL-16 – 18 | | K3 | GOV-09 | | | |

Why:

- **Architecture affects the headline.** v0.3 left G only in a profile; revision 1 showed it but most criteria could not move the level. Now every applicable ARC criterion constrains every loop through the foundation level.
- **K returns.** K1 and K2 join Open; K3 joins Vet and the governance ceiling.
- **M3 moves to Delivery.** Implementing a change is building, not learning, and the move lets a code lane count.
- **O moves to Expand**, joined by criteria that ask whether the product finds its adjacent opportunities.
- **Learning and delivery stay separate capabilities** but meet in the loops, where the weakest stage sets the level. Averaging them would hide which half is broken.
- **The single closed-loop flag becomes three loop levels**, with named blockers.

## 13. Name and identifiers

- **Working names only.** "EVOLVE" and "Software Autonomy Level" are not locked. A published npm package already calls itself an "Evolve Multi-Agent SDLC framework" and reports architecture health and evolution readiness (`@huutq88/evolve`). "Software autonomy levels" is also used in self-driving laboratory research. Neither proves a trademark conflict, but both rule out claiming the space is empty. A trademark and prior-use search is required before any public launch.
- **Stable IDs.** Criterion IDs use descriptive prefixes (`ARC`, `DEL`, `MAL`, `LRN`, `GOV`, `EXP`), so they survive a rename of the framework or of the capability display names.
- **Names in use.** The repository owner chose EVOLVE as the framework name and `evolvable-software` as the repository and skill name (1 October 2026). The skill and package metadata already use `evolvable-software`. The GitHub repository is still `malleablesoftware` until the owner renames it, and GitHub then redirects the old URL. All of these remain working names until the trademark search below.

## 14. Delivery plan once agreed

1. Rubric: new IDs, the 17 new criteria, scope facts, the four level sections, facets, inventories and archetype table, with the machine-readable model updated.
2. Scorer: per-loop levels with named blockers; foundation and ceiling; critical controls driven by scope facts; depth cap; inventories; upward-only `alt_score`. Tests for each.
3. Migration script from v0.3 assessments: ID mapping and flipping downward alternates.
4. Field test: score the new criteria, facets, inventories and scope facts for the 11 systems; add the `OpenHands/automation` repository; publish SAL results.
5. Inter-rater: add the Round 2 dataset, mapped to new IDs, and run a second rater on the new criteria.
6. Rename the skill, README and metadata once the names are settled; changelog entry disclosing every move.

## 15. Decisions

**Taken (review of revision 1):**

1. Headline SAL = min(Request → Release, Issue → Fix). Expansion is reported separately.
2. Failing a critical control caps at L2, with each control applied only where its scope fact holds and to the path being assessed.
3. Strict depth rule, with separate cumulative facets: implemented, tested, operated.
4. Repository tooling counts only as a first-party evolution system (section 8.4).
5. Repository and skill name: `evolvable-software`.

**Open:**

1. **Final framework name**, after the trademark and prior-use search.
2. **Strictness at L4.** Every applicable ARC criterion at 3 with tested evidence. Right bar, or too high for products that are otherwise strong?

## 16. Refinements made during implementation and review

Building the scorer, rescoring 11 systems and a review of the implementation led to these changes to the text above. The rubric is authoritative.

1. **Scope facts: nine, not seven.**
   - `machine_actions` (new) scopes GOV-09 (agent-safe actions) to products that agents or automated clients can change through an API or tool surface. Revision 2 tied GOV-09 to `agent_mutations` in one place and required it everywhere in another.
   - `definition_change_path` (new) makes rollback path-aware: GOV-05 is required when behaviour changes through definitions, DEL-11 when the evolution system ships code, and both when both exist. A product that evolves only through code is not failed on definition rollback.
   - `automatic_apply` is renamed `evolution_auto_apply` and covers only changes produced by the evolution loop. Scheduled maintenance, such as PostHog's automatic column materialisation, does not count.
2. **GOV-10 and GOV-11 apply only when self-change is possible** (`agent_mutations` or `evolution_auto_apply`).
3. **Backup is tested recovery.** ARC-09 level 3 is backup and restore of every applicable surface, with restore tested. Stated recovery objectives (RPO and RTO) moved to level 4, because for self-hosted software the deployment operator often sets them. The control is named for what it checks: tested backup and restore.
4. **Facets are required where they change the outcome:** on depth-capped criteria, for any reading of 3 or more. A 4 without operated evidence counts as 3 when tested.
5. **Inventories cap every reading.** When any reading (score, alternate or opt-in) is 3 or more, an inventory is required, and no such reading may exceed the weakest surface. The scorer also caps every variant at the weakest surface, so an alternate reading cannot bypass the rule. Below 3, the anchors already describe partial coverage.
6. **Request intake credits AI planners.** An AI lane that asks clarifying questions and produces a structured plan for approval before building is request intake at level 2 or above, provided it meets rule 12.
7. **Progress and sensitivity.**
   - Each loop reports how many of the next level's conditions it already meets, so products at the same level can be told apart without lowering the bar.
   - The scorer lists the criteria whose one-level change would move the headline, so a fragile reading is visible.

The field-test results are in `assessments/2026-09-field-test/README.md`, and they are provisional:

- n8n and OpenClaw lead at SAL 2.
- No system reached L3 in this repository-based, single-rater assessment.
- Definition rollback fails in all eleven.
