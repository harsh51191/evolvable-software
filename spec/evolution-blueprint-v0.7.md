# EVOLVE v0.7: the evolution blueprint

Status: draft for the repository owner's review. Nothing here changes how EVOLVE scores. Not implemented.

## 1. Why

EVOLVE tells a team how far its product can evolve itself safely, how much of that AI drives, and what blocks the next level. It does not yet tell them how to get there in a way they can act on.

The current plan (`score.py --prescribe`) has three weaknesses:

1. **It is criterion by criterion.** For n8n it lists 51 criteria below 3, each with a move from a catalogue. Many low scores share one structural cause, and the list hides it.
2. **It is generic.** Each move is the same text for every product. It names no table, file or feature in the product assessed.
3. **It assumes in-place change.** It ignores the constraint most teams start with, such as "the production database cannot change", and some moves quietly imply a rebuild.

The blueprint replaces the flat list with a systems view: what a self-evolving product is made of, which parts this product is missing, which of those block the level the team wants, and which route gets there within the team's constraints. It then hands the work to the team's delivery process, such as the AI Software Factory, and re-assesses.

## 2. The evolution system: eight building blocks

A product that evolves itself safely has an **evolution system**, the term rule 12 of the rubric already uses. It is made of eight building blocks. Every EVOLVE criterion, including the AIR checks, belongs to exactly one block.

| Block | What it does | Criteria |
|---|---|---|
| **1. Definition model** | Entities, fields, relations, layouts, rules and domains are stored as validated data, so behaviour changes without code | MAL-01 to MAL-05, MAL-07 to MAL-10, MAL-16, ARC-01, EXP-01 to EXP-03 |
| **2. Contracts and extensions** | Machine-readable contracts, events, hooks, plugins, connectors and agent surfaces, with stable versions and isolated extension code | MAL-06, MAL-11 to MAL-15, MAL-17 to MAL-20, DEL-02, DEL-03 |
| **3. Change ledger** | Every change, by a person or AI, is a versioned object: proposed, reviewed, applied, audited, reversible and restorable, and it survives upgrades | GOV-02, GOV-05 to GOV-08, ARC-02, ARC-09, AIR-07 |
| **4. Sensing** | Usage, errors, feedback, friction and unmet demand become typed signals, and every change is measured against a baseline | LRN-01 to LRN-04, LRN-09, EXP-04, AIR-08 |
| **5. Evolution engine** | Requests, issues and opportunities become specified, diagnosed and built changes, increasingly by AI | DEL-01, DEL-04, LRN-05 to LRN-07, EXP-05, AIR-05 |
| **6. Governed release** | Every change class is checked, verified, staged, switchable and rolled back | DEL-05 to DEL-11, EXP-06, AIR-06 |
| **7. Guardrails** | Self-change stays in scope, learned and AI-made changes are validated, tenants are isolated, and security, privacy and accessibility are structural | GOV-01, GOV-03, GOV-04, GOV-09 to GOV-11, LRN-08, ARC-05, AIR-04 |
| **8. Runtime foundation** | The product scales, runs background work reliably, knows its limits and objectives, degrades gracefully, and runs its AI portably and within cost | ARC-03, ARC-04, ARC-06 to ARC-08, AIR-01 to AIR-03 |

The mapping is data in the rubric's scoring model (a `blocks` map), so the scorer and the tests use it, and a criterion cannot be left out or counted twice.

Two notes:

- **The blocks are not new criteria.** They group the existing ones. A block has no score of its own. The blueprint reports the criteria in it.
- **A block is not an AI factory.** The evolution system lives inside the product and changes the product's own behaviour. A factory changes the product's code from outside. See section 7.

### What "entity-based" should mean (block 1)

The definition model is where a product gets flexibility. Three rules keep it from costing scale or integrity:

1. **Definitions are data; storage stays typed.** A new entity type is a definition that generates real tables, columns and indexes through the product's migration path. Frappe's DocTypes work this way. A single generic key-value or entity-attribute-value store for everything is the anti-pattern; ARC-01 already scores it down ("never a scan of a generic store").
2. **Hybrid is normal.** Hot core tables stay hand-modelled. Extension fields go in indexed JSON or generated columns. New types come from definitions.
3. **Flexibility is not scale.** Scale comes from block 8. A definition model on a fragile runtime only fails faster.

A product needs as much of block 1 as its target requires. Issue → Fix at L3 does not need a definition model. Opportunity → Expansion at L4 does, because new capability must ship without a deploy. The blueprint derives this from the loop rules (section 4), not from a separate table.

## 3. Inputs: ask, don't guess

The code cannot say what the business wants or what it cannot touch. Before planning, the skill asks up to three questions:

1. **Target.** Which loops matter, and to what level? Default: the next level for Request → Release and Issue → Fix.
2. **Route.** What can change? Offer the three routes in section 5. Default: overlay, the least invasive, with its ceiling shown.
3. **Off limits.** Anything else fixed: a vendor database, a public API that cannot break, a team that cannot be retrained.

If the person does not answer, the skill uses the defaults and says so.

## 4. The blueprint

The blueprint is a section of the scorecard, or a separate `blueprint.md`, with five parts. Parts 1 to 3 and the route ceiling are computed by `score.py`. The product-specific steps are written by the agent from the evidence.

### 4.1 Diagnosis

The headline, the critical controls and the blockers for the target, as today.

### 4.2 Root causes: blockers grouped by block

The scorer groups the target's blockers by building block. Each block shows the conditions it holds, the critical controls among them, and its other criteria below target.

Worked from the published n8n field-test scores (Request → Release and Issue → Fix to L3):

| Block | Blocking conditions | Critical controls |
|---|---|---|
| Change ledger | GOV-05 2, ARC-02 2, ARC-09 2 | 3: definition rollback, safe migrations, tested backup and restore |
| Guardrails | GOV-10 2 | 1: bounded self-change |
| Evolution engine | DEL-01 2, product build path (DEL-04 2, LRN-07 1), LRN-05 2, LRN-06 2 | – |
| Governed release | DEL-06 2 | – |
| Sensing | LRN-03 2 | – |

Ten conditions sit in five blocks, and three of n8n's four failing critical controls sit in one: the change ledger. That is the root cause the flat list hides. (If n8n GOV-04 is adjudicated down to 2, as the second rating recommends, Guardrails gains the security control.)

### 4.3 Target and order

Order is fixed by one principle: **safety before autonomy.**

1. **Blocks that hold a failing critical control.** No loop passes L2 until they pass, and raising AI's part before they pass only lets AI make changes that cannot be undone.
2. **Blocks that hold other target blockers,** ordered by the prerequisites in `remediation.md` (`Requires:`).
3. **Everything else** is listed as out of scope for this target, not planned. A blueprint to L3 is a short list, not a backlog.

### 4.4 Route and ceiling

The route sets which moves are allowed (section 5). The scorer projects the target assuming every allowed move lands, and reports the **ceiling under each route**: the highest level per loop each route can reach. When the chosen route cannot reach the target, the blueprint says which blocks need a more invasive route and why.

The opt-in readings come first, as one line: "Before you build: these shipped settings raise the following criteria." They are a note, not a route.

### 4.5 Steps

For each block in order, the agent writes a small number of product-specific steps. Each step states:

- **What changes,** naming the files, tables, services or settings from the evidence;
- **What stays untouched;**
- **Criteria it moves,** from what level to what level;
- **Acceptance evidence:** what the next assessment will look for, taken from the rubric's anchor for the target level, including the facets the depth cap needs (a 3 needs `tested`);
- **Touches** (section 5) and the **suggested lane** for the delivery process;
- **Relative size,** re-estimated for this product.
- **Prompt:** a self-contained prompt for a coding agent such as Claude Code or Codex, run in the product's repository, naming the files and patterns to follow, what must not change, and the tests to add;
- **Done when:** a checklist for the step: the tests that must pass, the behaviour a person can see, what must be unchanged, and the criterion reading the next assessment must find.

Each product's blueprint ends with the **level challenge** from the rubric's scoring model, made concrete for that product, and the evidence checklist from `score.py --checklist <level>`. A level is reached only when the challenge passes on the running product and a fresh assessment finds every item, never from a prompt or a pull request alone.

A step that cannot cite evidence for what it changes is marked as a design question, not a step.

## 5. Routes

| Route | What changes | What stays untouched | Moves allowed |
|---|---|---|---|
| **Overlay** | The evolution system is built beside the product, joined at seams: hooks, middleware, events, change capture | Existing tables, existing data, existing core logic | `new`, `seam`, `config`, `process` |
| **Incremental** | The core is changed module by module, with expand-and-contract migrations, strangling old paths | Data, through migration; public contracts, through versioning | all |
| **Re-platform** | A new core built on a definition model, with data migrated | Little | all, with blocks 1, 3 and 6 built natively first |

Each move in `remediation.md` gains a `Touches:` line using a fixed vocabulary:

| Tag | Meaning |
|---|---|
| `new` | A new store, service or component beside the existing ones |
| `seam` | A hook added at an existing extension point or boundary, without changing core logic |
| `config` | Product configuration or settings |
| `process` | How people work; no software change |
| `core-code` | Changes existing core logic |
| `schema` | Alters existing tables or storage structures |
| `data` | Rewrites existing data |

A move that touches `core-code`, `schema` or `data` may add an `Overlay:` line: a variant that reaches the same level through `new` and `seam` only. Under the overlay route, a move with neither a compatible `Touches:` line nor an `Overlay:` variant is not allowed, and the criterion stays at its current level in the projection. That is how the ceiling is computed, deterministically.

Example: ARC-09 to 3 in place (`schema`, `core-code`) versus overlay (`new`, `seam`). Overlay: a backup and restore service beside the product that covers data, definitions, files, secrets and scheduled work, restores into a copy in CI as its test, and checks each scheduled job's owner and credentials through a hook before the job runs.

Some criteria have no overlay variant by nature. MAL-01 ("new entity type without code, DDL or deploy") needs a definition model at the core or a new definition-driven store beside it whose types live only there. The blueprint states such limits rather than hiding them.

## 6. The loop closes: re-assess

Each step records the criterion moves it predicts. After the work lands, the team re-runs EVOLVE. The blueprint's predictions are compared with the new scores:

- moves that landed;
- moves that landed below their target, with the missing evidence or facet;
- moves that changed other criteria.

This makes the plan itself measurable: assess, plan, change, re-assess. Plans never change a score. A score changes only when the re-assessment finds the evidence.

## 7. Hand-off to a delivery process, and how a factory counts

The blueprint is delivery-neutral. Each step can be exported as a work item in the AI Software Factory format (`templates/work-item.md`): the goal from the step, acceptance criteria from the acceptance evidence, and the lane from the touches. A step that touches `schema` or `data`, or adds public interfaces, is suggested as Guarded, matching the factory's own lane rules; the factory's guard scan can only make a lane stricter.

**One company factory, one evolution system per product.** A factory is how a company changes code, and its policy and authority are shared across products. The evolution system is part of each product. Every product needs its own, sized to its target. A factory alone does not make a product self-evolving; the factory's own alignment document says the same.

**When a factory counts in EVOLVE.** Rubric rule 12 credits repository tooling for DEL-01, DEL-04, DEL-09 to DEL-11, LRN-03, LRN-05 to LRN-07 and EXP-04 to EXP-06 only when it is a first-party evolution system. Proposed clarification to rule 12, for approval, as a separate change:

> An installed delivery framework, such as an AI software factory, counts as a first-party evolution system when, in the assessed repository: it is installed at a pinned version and maintained with the product; its enforcement runs (authority and merge checks are required checks, not documents); its limits meet GOV-10 for the changes it makes; and its product layer describes this product. Rules and templates alone are documentation and count for nothing. A factory that ships code sets `code_release_path`, so release rollback (DEL-11) applies.

## 8. What the scorer and the skill do

**`score.py`** (deterministic, no network):

- `--blueprint` with `--target request:L3,fix:L3` and `--route overlay|incremental|re-platform`;
- groups blockers by block, marks critical controls, orders by safety then prerequisites;
- projects each route's ceiling;
- emits the step skeleton (block, criteria, target, touches, acceptance anchor) for the agent to fill;
- `--compare <old.json> <new.json> <blueprint.json>` for section 6.

**Skill** (`SKILL.md`):

- a new optional step after scoring: ask the inputs (section 3), run `--blueprint`, write the product-specific steps from the evidence already collected, and never invent evidence;
- label every blueprint as advisory, with projected levels as ceilings.

**References:**

- `rubric.md`: the `blocks` map in the scoring model; block names in the scorecard;
- `remediation.md`: a `Touches:` line on all 74 entries, and `Overlay:` variants where one exists;
- `scorecard-template.md`: the blueprint section.

## 9. Tests that must hold

- Every criterion and AIR check is in exactly one block.
- The blueprint never changes a score, a level or a control.
- The blockers grouped by block are exactly the scorer's blocker list for the target, with none lost or duplicated.
- Blocks holding a failing critical control always come first.
- Under the overlay route, no step uses a move tagged `core-code`, `schema` or `data` without an `Overlay:` variant.
- For every loop, the re-platform ceiling is at least the incremental ceiling, which is at least the overlay ceiling.
- Output is deterministic for the same inputs.

## 10. Field test

Run `--blueprint` on all 11 field-test products at L3 under each route, and publish:

- one worked example in full: n8n to L3, overlay route, with product-specific steps;
- a table of route ceilings for all 11 products, showing how far each can go without touching its database.

## 11. Out of scope

- Cost or time estimates. Sizes stay relative.
- Vendor or tool recommendations.
- Scoring plans or roadmaps. Only shipped evidence scores.
- General refactoring advice unrelated to the evolution system.

## 12. Open questions for the owner

1. Block names and boundaries, especially GOV-07 (in the change ledger, not guardrails) and LRN-09 (in sensing, not release).
2. Whether the blueprint is a scorecard section or a separate file.
3. The rule 12 clarification in section 7, as its own change.
4. Whether to adjudicate n8n GOV-04 and OpenClaw ARC-09 before the worked example, so it starts from corrected scores.
