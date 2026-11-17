# EVOLVE v0.7: the evolution blueprint (superseded)

Status: superseded by `evolve-v0.7.md` §9 (Blueprint v2), `skills/evolvable-software/references/blueprint-template.md` (the format) and `skills/evolvable-software/scripts/blueprint.py` (the skeleton). This note keeps only the reasoning from the earlier draft that still holds. The hand-written trial in `blueprint-trial-v0.7.md` is superseded too.

## What was dropped, and why

A critical review (spec §1, row B) rejected four ideas in the draft:

- **Safety-first ordering.** Blocks holding a failing critical control came first. A team then spends its first months on backups and rollback with nothing for users to see. Now value leads: a safety gate is attached to the first milestone that needs it (Level 3 for the seven critical controls), never front-loaded.
- **Level-first goals.** The draft asked "which loops, to what level". A blueprint now starts from the owner's business goal, in their words, and the kinds of change that serve it.
- **Codes in reader text.** Steps were described by criterion and building block. Reader text now uses `plain-language.md` only; codes appear under "For engineers".
- **Steps that only move a score.** Every step now names a gain a user can see, or is labelled a gate.

## What was kept

**The eight building blocks, as an internal grouping.** A product that evolves itself has an evolution system made of eight blocks: definition model; contracts and extensions; change ledger; sensing; evolution engine; governed release; guardrails; runtime foundation. Every criterion belongs to exactly one block (the map is data in `blueprint.py`, tested). Grouping a product's gaps by block shows their shared cause: in the September field test, three of n8n's four failing critical controls sat in the change ledger. The blocks guide the agent and appear under "For engineers"; they never appear in the reader's text (§9 rule 11). They are not new criteria and have no score.

**What "entity-based" should mean (definition model).** Definitions are data; storage stays typed: a new entity type generates real tables, columns and indexes through the product's migration path, never a generic key-value store for everything. Hybrid is normal: hot core tables stay hand-modelled, extension fields go in indexed JSON or generated columns. Flexibility is not scale: scale comes from the runtime foundation.

**Routes.** The constraint most teams start with is what they cannot touch. The blueprint takes a route:

| Route | What changes | What stays untouched |
|---|---|---|
| Overlay (default) | Built beside the product, joined at seams: hooks, middleware, events, change capture | Existing tables, data and core logic |
| Incremental | The core, part by part, with expand-and-contract migrations | Data, through migration; public contracts, through versioning |
| Re-platform | A new core on a definition model, with data moved over | Little |

Under overlay, `blueprint.py` flags any move whose remediation text implies changing existing storage as needing a design decision (a documented keyword rule). The draft's finer `Touches:` vocabulary (`new`, `seam`, `config`, `process`, `core-code`, `schema`, `data`) and per-route ceilings remain a possible refinement of that rule. Some criteria have no overlay variant by nature (a new entity type without code needs a definition model at the core, or a new definition-driven store beside it), and a blueprint states such limits.

**Acceptance evidence, prompts and done-when lists.** Each step names what the next assessment must find (the rubric's anchor for the target score, with the `tested` facet where the depth cap needs it), a self-contained prompt for a coding agent, and a done-when checklist that names an automated test performing the check.

**The loop closes by re-assessing.** Plans never change a score. A level counts only when a fresh assessment, made without sight of the blueprint, finds the evidence and the level challenge passes on the running product.

**One company delivery process, one evolution system per product.** A delivery framework such as an AI software factory changes code from outside; the evolution system lives inside each product. The rule-12 clarification for when such a framework counts is now in spec §5.
