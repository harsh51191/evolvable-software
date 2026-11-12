# Born evolvable: starting a product that can evolve itself

This guide is for a founder, product lead or tech lead starting a new product. It describes how to build it so that, from the first day, it is designed to take users' requests through to release, find and fix the problems they face, and spot new needs, with AI doing more of that work over time while people set the goals and the limits.

The short version: get twelve foundations right before the first user, so the product is **designed for** the top of the scale. Then switch autonomy on slowly, one kind of change at a time, as the records show it is safe. The records are the proof and the learning loop. They are not the design.

A small working example that follows every foundation is in [`examples/born-evolvable/`](../examples/born-evolvable/README.md).

## Why start this way

The parts that are hardest to add later are the ones everything else stands on: undo, versioned settings and content, one path for every change, and signals from users. Retrofitting them means touching every feature that was built without them.

The EVOLVE field test shows the cost. None of the eleven products assessed can undo changes on every surface the people running it change, and that alone holds every one of them below the supervised level. n8n's AI already builds workflows, yet it stays at the assisted level, because credentials, variables and settings cannot be rolled back in the product and its restore is untested. The AI is ahead of its safety net. A product that starts with the safety net never has that problem: AI can be given more of the work as soon as it earns it.

Starting this way costs days, not months, if the product is designed around the changes it will actually need (foundation 1) instead of around a generic platform.

## Designed for, built to, proven at

EVOLVE keeps three claims apart:

| Claim | What it rests on | What it says |
|---|---|---|
| **Designed for** | Design documents and architecture | The product is designed so that every level up to this one is possible without rework |
| **Built to** | What ships: code, with tests | What the product can do today |
| **Proven at** | Operating records: change history, release records, audit logs | What it has been seen to do, more than once, in a real deployment |

On day one a well-started product can honestly read **Designed for Level 5 · Built to Level 2 · Proven: not evidenced**. Each part means something different, and none stands in for another. A design reading is not comparable with a reading of shipped software, and every report says so.

Why not run at the top straight away? Because a product should run at the level it has **proven**, not the level it is designed for. Every kind of change has its own autonomy dial. It starts low, and rises one step when the record for that kind of change shows the step is safe. A bad result lowers it again, automatically. Designing for the top means that raising the dial is a policy change, not a rebuild.

## The twelve foundations

Each foundation has four parts: what it means, the smallest version that counts on day one, the mistake to avoid, and an engineering note.

### 1. Name your kinds of change first

**What it means.** List what the people running the product will need to change: answers, rules, workflows, prices, templates, forms. Usually there are three to eight. Design for those. Do not build a generic platform that can change anything.

**Day one.** A one-page list, in plain words, of each kind of change: what it is, who needs to make it, and whether it is one of the main ones. Every later design decision refers to it.

**Mistake to avoid.** Building "configure anything" because you cannot yet say what will change. Unlimited configurability is expensive to build, test and keep safe, and it hides the kinds that matter.

> **Engineering note.** Keep the list in one machine-readable file (for example `kinds.json`) with the fields and types of each kind; storage validation, the change path, the policy and the self-description all read it. Add a kind when real requests show it, not before. Leaving a kind out does not hide it: an assessment lists every kind operators need, including those they cannot change yet.

### 2. Store those things as versioned data, not code

**What it means.** Each kind of change lives as data the product reads at run time, with a history of versions, so changing it needs no release.

**Day one.** Every definition (each answer, rule or price list) has versions, an author, a status and a date. The product reads the current version; old ones stay.

**Mistake to avoid.** Keeping the things people change in code or in environment settings "for now". Every one of them later needs a migration, a screen and an undo path.

> **Engineering note.** Validate every version against its declared fields before it is stored. Small definitions can share one versioned table; business records (orders, tickets, events) get typed, indexed tables generated from their definitions, not a single generic key-value store. See "What to make data" below.

### 3. One door for every change

**What it means.** People, AI and the product itself all change the product through the same path: propose, check, release, measure. There is no side door for admins, scripts or the AI.

**Day one.** A single function or service that every change goes through, recording who proposed it and why. The admin screen, the AI and the scheduler all call it.

**Mistake to avoid.** Giving the AI its own write path because it is "only drafting". The day it stops drafting, nothing governs it.

> **Engineering note.** Make the proposal a first-class object: a diff, a rationale, provenance (what it was drafted from), the check results and the decision. Give every caller a real identity (person, AI, product), never shared or ambient authority. Every step writes to one audit trail.

### 4. Everything can be undone

**What it means.** Every change can be reversed in one step: content and settings, code releases, data changes and schema changes. A backup that has been restored is the last line of defence.

**Day one.** One-step undo for every kind of change; a backup command and a test that restores it into a fresh location; database migrations with down steps; a way to roll back a code release to the previous one.

**Mistake to avoid.** Undo for the main screen but not for settings, credentials or the things the AI changes. A product is only as reversible as its least reversible surface.

> **Engineering note.** Undo restores the version a change replaced, one step at a time. Keep schema and data changes compatible across one release so code can roll back. Restore into a fresh copy with scheduled jobs held until checked, and test it in CI. An off switch (foundation 9) stops harm now; undo removes it.

### 5. Capture signals from the first user

**What it means.** Record requests, failures, feedback and unmet needs as structured data from the first day, with privacy designed in.

**Day one.** Every user action that matters is a typed record: what was asked or done, what the product did, which version of which definition served it, and the outcome. Unmet requests are kept and grouped. Personal data is removed or classified before storage, and a retention period applies.

**Mistake to avoid.** Logs and free-text feedback only. Nothing can learn from them, and they fill with personal data.

> **Engineering note.** Link each signal to the definition and version it concerns, so a change can be measured against it. Hash session identifiers, strip personal data on the way in, and give every field a privacy class that drives export, erasure and retention. Treat signals as untrusted input: they can inform a change, never instruct one.

### 6. Every change has a goal and is measured

**What it means.** A change states what it should improve before it is released. Afterwards the product compares the result with a baseline and decides: keep, revise or undo.

**Day one.** Each kind of change names its measure. Each released change records its baseline, its target and how long to watch, and a person or the product records the decision.

**Mistake to avoid.** Treating "released" as "done". Without a measured decision there is no learning loop, only a stream of changes.

> **Engineering note.** Count only the users the change could affect, and compare them with a control group seeing the previous version over the same period where you can. Record the decision against the change, so the record can later justify raising or lowering autonomy (foundation 12).

### 7. Checks are automatic and they grow

**What it means.** Tests run on every change, whoever made it, and every failure seen in production becomes a new test.

**Day one.** A check suite that runs before any change is released, including AI drafts. A path, through the same door, that turns a recorded failure into a new check.

**Mistake to avoid.** Checks only for code, or checks that drafts skip. And a fixed suite: a loop whose checks never grow repeats its mistakes faster.

> **Engineering note.** Store check cases as definitions. Reject a change that breaks a check that passes today; let a new failing check record a known problem without blocking unrelated work. When a change that passed every check is later reversed, record a "wrong pass" against those checks and propose a check from the failure.

### 8. Limits are written down, outside the AI

**What it means.** A written policy says which kinds of change may ship without a person, which need one, and which are blocked, with limits on scope and rate. Code enforces it, not the model's judgement.

**Day one.** A policy definition per kind of change, enforced at the door, with blocked attempts logged. Some limits are hard-coded and no policy can remove them, for example: the AI may never change the policy alone, or weaken a check.

**Mistake to avoid.** Limits written into prompts. A model's belief that a change is safe is never permission.

> **Engineering note.** Limits per kind: who may propose, the share of traffic a release starts at, changes per day without a person, protected items, and what may not be removed. The policy is itself a kind of change (foundation 11), so changes to it are versioned, checked and auditable.

### 9. Release gradually, with an off switch and automatic reversal

**What it means.** A change reaches a small share of users first. Any change can be switched off at once. When its measure gets worse, it is reversed automatically.

**Day one.** Every kind of change that users see can go to a share of traffic, has an off switch, and is reversed by the product when its measure falls below the baseline.

**Mistake to avoid.** Feature flags for code only, while settings and content changes reach everyone at once.

> **Engineering note.** Assign users to the candidate or control group by a stable hash, so each sees one version consistently. Reversal is a safety action: allow it whatever the dial says. Record every automatic decision.

### 10. The product describes itself in a machine-readable way

**What it means.** The product publishes what can be changed, how, by whom and within which limits, so agents can act on it without reading the code.

**Day one.** A capability map (kinds of change, their fields, the operations, the policy and the current dial) generated from the same definitions the product runs on.

**Mistake to avoid.** Hand-written API documentation that drifts from what the product accepts.

> **Engineering note.** Generate the tool surface (command line, API, or MCP tools) from one operations table, with typed arguments and scoped identities, and include a health and version endpoint plus a snapshot of the live configuration.

### 11. The loop itself is changeable

**What it means.** The checks, the policy and the prompts that govern change are versioned and go through the same door, so they improve too. This is the recursive part.

**Day one.** Checks and policy are kinds of change in the list from foundation 1, with versions, undo and measurement. A policy change that raises autonomy must cite a measured record.

**Mistake to avoid.** Hard-coding the checks and the policy, so the only way to improve the loop is an engineer editing it after an incident.

> **Engineering note.** Measure a change to the loop by its effect on later decisions: the share of later changes kept rather than reversed, and how often the checks wrongly passed a change. Feed wrong passes back into new checks and into the policy.

### 12. Build for the top level, start the dial low

**What it means.** Build the machinery for full autonomy now, but run each kind of change at a low setting, and raise it one step at a time as results come in.

**Day one.** An autonomy dial per kind of change. Most start at "drafted" or "carried": the product drafts or carries the change and a person approves each release. The policy itself stays with people.

**Mistake to avoid.** One global "AI on" switch. Raising autonomy for answers says nothing about prices.

> **Engineering note.** The dial follows the six settings EVOLVE uses for a kind of change: engineers only, self-serve, drafted, carried, pre-approved, self-chosen. Enforce in code that a dial rises one step at a time, only on a record (for example three kept changes and no more than a quarter reversed), and falls automatically after repeated reversals.

## What to make data, and what to leave as code

| Make it data | Leave it as code |
|---|---|
| The kinds of change in your list: answers, rules, workflows, prices, templates | The hot core logic that uses them: matching, pricing calculation, the workflow engine |
| Checks, policy, prompts and the dial | The door, the policy enforcement and the invariants no policy can change |
| Measures, targets and release shares | Storage, migrations, backup and restore |

Three rules keep this honest:
- **Kinds of change are data; the engine that runs them is code.** A rule is data; the rules engine is code, tested and released through the team's own delivery process.
- **Definitions generate typed storage.** When a definition describes business records, generate typed, indexed tables from it. One generic store for everything becomes the classic performance trap.
- **Do not build an infinitely generic platform.** Opinionated defaults, a strong domain model and well-placed extension points beat unlimited configurability; every axis of variation must be justified by real customers (AI Software Factory rule CFG-21).

## Day-0 checklist

Each line can be checked by running something or reading one file.

1. [ ] One file lists the kinds of change, with who needs each and which are main.
2. [ ] Each kind is stored as validated, versioned data with an author and a status, and changes with no release.
3. [ ] Every change, by a person, the AI or the product, goes through one function, and the audit trail shows it.
4. [ ] Every kind can be undone in one step; a code release can be rolled back; migrations have down steps; a backup restores into a fresh location in a test.
5. [ ] Requests, failures, feedback and unmet needs are stored as typed records linked to the version that served them, with personal data removed.
6. [ ] Each kind names its measure; each release records a baseline, a target and a window; a command recommends keep, revise or undo.
7. [ ] Checks run on every change, drafts included, and a recorded failure can become a check through the door.
8. [ ] A policy per kind says who may propose and what ships without a person; a test shows an out-of-policy AI change blocked and logged.
9. [ ] User-facing kinds release to a share of traffic, have an off switch, and are reversed automatically when their measure worsens; a test shows it.
10. [ ] A capability map is generated from the same definitions the product runs on.
11. [ ] Checks and policy are kinds of change; a test shows a policy change going through the door.
12. [ ] Each kind has a dial; raising it needs a measured record and is enforced in code.

## The first 90 days

Raise one kind of change at a time, and only on its own record.

| When | Dial settings | What justifies the step |
|---|---|---|
| Day 0 | Main kinds at drafted or carried (the AI drafts, a person approves each release). Checks: carried. Policy: people only. | The day-0 checklist passes in tests |
| Weeks 1–4 | No raises. Run every change through the door; turn every failure into a check. | Each released change has a recorded keep, revise or undo decision |
| Weeks 4–8 | Raise the lowest-risk main kind (often answers or content) to pre-approved, with a small daily cap and a small starting share. | That kind's record: a set number of kept changes (for example 10), few reversals, no wrong pass left without a new check, and a restore drill passed |
| Weeks 8–12 | Raise a second kind, or widen the first one's limits. Let the product propose checks from failures on its own. | The first kind's pre-approved record: kept changes, automatic reversals that worked, no change that escaped its limits |
| After day 90 | Consider self-chosen for one kind: the product chooses what to improve. Keep the policy with people. | A record over real operation, which is what a "Proven at" reading rests on |

Lower a dial whenever the record turns: a reversal that was not caught automatically, a wrong pass, or a change outside its limits. Lowering should be automatic; raising should always be a recorded decision by a person.

## Getting a "Designed for" reading

You can assess the design before the code exists, with the EVOLVE skill (`skills/evolvable-software/`).

1. Write the design down: the kinds of change, the door, the policy and the dial, the data model, undo and recovery, signals and measurement. `examples/born-evolvable/DESIGN.md` shows a compact form, with numbered sections so they can be cited.
2. Ask the skill for a design assessment, or start the file yourself:
   ```bash
   python3 skills/evolvable-software/scripts/init_scores.py --product "Your product" \
     --archetype focused-application --source "design documents @ date" --basis design --out ~/evolve/design.json
   ```
3. Evidence for a design assessment may use grade **D**: a design document cited by path and section, for example `docs/design.md §4`. Kinds of change and inventories are still required; evidence facets and the depth cap are not. The headline reads "Designed for", and it cannot carry a proven reading.

It becomes **Built to** when a fresh assessment of the shipped code (the default basis) finds each mechanism in the code, with tests where the rubric needs them; design documents count for nothing there. It becomes **Proven at** when a shipped assessment's `proven` reading finds operating records showing real changes going through each loop at that level, more than once, in a real deployment. Each reading is made fresh, without leaning on the one before.

## How the AI Software Factory fits

Two different systems change a product, and a born-evolvable product needs both.

- **The factory is how the team and its agents change the code.** The [AI Software Factory](https://github.com/harsh51191/ai-software-factory) is an open operating system for AI-first delivery: an authority policy enforced outside the model, lanes by risk, a merge gate, proof levels, and authority earned per kind of action from verified results.
- **The evolution system is inside the product.** It changes the product's behaviour through its own definitions, in the running product, for the people who run it: the twelve foundations above.

There is one factory per company and one evolution system per product. They should share the same ideas (a written policy enforced in code, authority earned per kind of change and lost automatically, evidence before claims) and, ideally, the same policy and audit records. The factory builds the evolution system and the core code; the evolution system carries routine change; when the same kind of code change keeps recurring, that is the signal to make it a new kind of change in the product (factory rules CFG-19 and CFG-20). AI-assisted engineering through the factory is not the product evolving itself, and an assessment says so.

## Appendix: for engineers

How each foundation maps to EVOLVE criteria and level conditions (v0.7). "Ln" is the level whose conditions name the criterion; a critical control failing caps every loop at Level 2.

| # | Foundation | Criteria | Level conditions |
|---:|---|---|---|
| 1 | Kinds of change | `change_kinds` and reach; EXP-02 for expansion | L1 people path: every main kind at reach ≥ 1 |
| 2 | Versioned data | GOV-05, MAL-02, ARC-01, ARC-02 | GOV-05 ≥ 3 and ARC-02 ≥ 3 (critical controls) at L3; ARC ≥ 3 at L4 |
| 3 | One door | GOV-06, GOV-02, GOV-09, DEL-01, DEL-04 | Build path (DEL-04) ≥ 2 at L2, ≥ 3 at L3, ≥ 4 at L5; DEL-01 ≥ 2/3/4 at L2/L3/L5; GOV-06 ≥ 2 and GOV-09 ≥ 2 at L3 |
| 4 | Undo everything | GOV-05, DEL-11, ARC-02, ARC-09 | Rollback ≥ 2 at L1, ≥ 4 at L4; definition rollback, release rollback, safe migrations and tested restore are critical controls at L3 |
| 5 | Signals | LRN-01, LRN-02, LRN-03, EXP-04, GOV-03, GOV-11 | LRN-03 ≥ 2/3/4 at L1/L3/L5; EXP-04 ≥ 2/3/4 at L2/L3/L5; GOV-03 ≥ 3 and GOV-11 ≥ 3 at L4 |
| 6 | Goal and measure | LRN-09, EXP-06, ARC-07 | LRN-09 ≥ 2/3/4 at L3/L4/L5; EXP-06 ≥ 2/3/4 at L3/L4/L5 |
| 7 | Checks that grow | DEL-05, DEL-08, LRN-08, LRN-10, AIR-05, AIR-06 | DEL-05 ≥ 2/3/4 at L2/L3/L5; LRN-08 ≥ 2 within bounded self-change at L3 |
| 8 | Limits outside the AI | GOV-07, GOV-10, GOV-09, GOV-11 | Bounded self-change (GOV-10 ≥ 3) at L3 when the product changes itself; GOV-07 ≥ 3 at L4, ≥ 4 at L5; GOV-10 ≥ 4 at L5 |
| 9 | Gradual release | DEL-09, DEL-10, DEL-11, ARC-07 | DEL-09 and DEL-10 ≥ 2/3/4 at L3/L4/L5; ARC-07 ≥ 4 at L5 |
| 10 | Self-description | MAL-19, MAL-06, DEL-06 | DEL-06 ≥ 3 at L3 and L4, ≥ 4 at L5 |
| 11 | The loop is changeable | LRN-10, GOV-07, LRN-08 | LRN-10 ≥ 2 at L4, ≥ 4 at L5 (the Recursion line) |
| 12 | Dial per kind | reach per kind; GOV-07 (movable human boundary); `proven` | Reach ≥ 4 needs GOV-07 ≥ 3; reach 5 needs LRN-07 ≥ 3; Proven is reported separately from Built |

Notes:
- The dial in this guide is the reach scale of a kind of change: 0 engineers only, 1 self-serve, 2 drafted, 3 carried, 4 pre-approved, 5 self-chosen.
- In a design assessment, grade D evidence is allowed and the depth cap does not apply; in a shipped assessment, a 3 or 4 on a depth-capped criterion needs tested evidence.
- Factory rules referred to: CFG-19 to CFG-21 (`rules/22-core-vs-custom-and-configuration.md`) and AUT-8 to AUT-10 on earning and losing authority (`rules/01-authority-and-decisions.md`).
