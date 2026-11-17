# Blueprint template (EVOLVE v0.7)

A blueprint tells a product team, in plain words, how to move its product up the EVOLVE levels: what users gain at each milestone, a check anyone can run to confirm it, and the engineering steps with a prompt for a coding agent. This file defines the one format. Spec §9 sets the rules; this file says how each section follows them.

```bash
python3 scripts/blueprint.py <assessment.json> --goal "<owner's goal, in their words>" \
        [--target LEVEL] [--route overlay|incremental|re-platform] [--json]
```

The script prints the skeleton. It fills in everything that can be computed from the assessment, the scoring model, `remediation.md` and `plain-language.md`, and marks the rest `TODO(agent): …` with an instruction. The agent replaces every `TODO(agent)` line from the evidence it already has and never invents evidence. Defaults: target two levels above today (at most 5); route overlay.

## Rules (spec §9)

1. **Start from a business goal,** in the owner's words, and name the kinds of change that serve it.
2. **Value leads.** Milestones are ordered by what users gain. A safety gate is attached to the first milestone that needs it, never front-loaded.
3. **Every step names a gain a user can see,** or is labelled a gate. A step that only moves a score is not allowed.
4. **A progress map** from today to Level 5: milestone, what users get, the level after it, and a check a person can run on the live product.
5. **Effort and payoff:** a relative size (S, M, L) and the measure the milestone should move.
6. **Risks and what a step brings into scope** (adding AI brings the AI Readiness checks, privacy and cost).
7. **People:** who approves, who sets the policy for what ships without a person, and what changes in roles.
8. **Engineering notes, a prompt for a coding agent and a "done when" checklist** under each milestone.
9. **Checks are scripts where possible:** the done-when list names an automated test that performs the challenge.
10. **Re-assess fresh:** the level counts only when a new assessment, made without sight of the blueprint, finds the evidence.
11. **Building blocks stay internal.** The eight blocks may guide the agent; they do not appear in the reader's text.

## Writing rules

- Reader text uses the words in `plain-language.md`: no criterion codes, no jargon, the same idea always in the same words (undo, the people running the product, customer organisation, written rules).
- Codes, rubric anchors, building blocks and remediation moves appear only under **For engineers**.
- Name the product's own screens, files and data. A step that cannot cite evidence for what it changes is a design question, not a step.
- Advice only: a blueprint never changes a score. Projected levels are ceilings, not forecasts.

## Sections, in order

| # | Section | What it holds | Computed | Agent writes |
|---|---|---|---|---|
| 1 | **Goal** | The owner's words; the measure that shows progress; the kinds of change that serve it (rule 1) | The words; the list of kinds to choose from | The measure with today's value and source; which kinds serve the goal |
| 2 | **In one paragraph** | What the product does, what already works toward the goal, what is missing, what the plan adds | Level, loops, kinds of change, number of milestones | The paragraph |
| 3 | **What this does and does not change** | It does not redesign journeys; it lets users' requests and the product's own data drive change, with people deciding; the route | Fixed text and the route | What stays as it is in this product |
| 4 | **Where it stands today** | The level in words; the kinds of change and how far each has come; Designed, Built and Proven; whether its checks improve; what is in place and what holds it back | All of it | What works today, in the product's words |
| 5 | **The destination** | A story told stage by stage, from today to Level 5, through one example that serves the goal | What each level means for people | One example per stage |
| 6 | **The progress map** | Per milestone: what users get, the level after it, the check, the size, the measure it should move (rules 4, 5) | Gains, level after (re-scored), size | The measure; sizes for kinds of change |
| 7 | **Milestone N** (one per level) | See below | Most of it | Name, story, concrete check steps, files, prompt |
| 8 | **Safety gates** | Each gate attached to the first milestone that needs it; the seven safety gates of Level 3 and their state | All of it | Nothing, unless a reading is wrong |
| 9 | **Beyond** | The levels after the target: what they mean and what they need | All of it | One example per level |
| 10 | **How the level will be confirmed** | A fresh assessment made without sight of the blueprint, and the level challenge (rule 10) | All of it | Nothing |
| 11 | **Notes on the assessment** | Date, commit, headline, how sure the reading is, what is not evidenced | All of it | What was re-checked, and readings you think are wrong |

### Each milestone

| Part | Rule | What it holds |
|---|---|---|
| **What changes for users** | 3 | The kinds of change that reach the milestone's reach, and each user-visible gain, in plain words. If there is none, the skeleton says `TODO(agent): describe the gain a user can see; if there is none, mark this step as a gate.` |
| **Why this moves the product up** | – | What the level means, and the level the product reads after the milestone if every step lands |
| **The check** | 4, 9 | The level challenge for each headline loop, from the scoring model; at Level 1, the main kinds of change to try. The agent turns it into steps on the live product or its demo. |
| **Risks and what it brings into scope** | 6 | AI coming into scope (AI Readiness checks, privacy, cost); the gates it touches; steps the route flags; what self-change without a person brings in at Level 4 |
| **People** | 7 | Who makes the change, who approves, who sets the rules for what ships without a person, what changes in roles |
| **For engineers** | 8, 11 | Per item: code, title, building block, now → needed, which loop and stage need it, size, prerequisites, the move from `remediation.md`, the evidence the next assessment must find, depth and inventory notes, route flags; alternatives; the optional third loop |
| **Prompt for a coding agent** | 8 | A self-contained prompt: files and patterns to follow, what to deliver, what must not change, the automated test that performs the check |
| **Done when** | 8, 9, 10 | One box per gain and gate; the check passes on the running product; a named automated test performs it; a fresh assessment finds the evidence |

## How the skeleton is computed

- **Milestones.** One per level, from today's headline level + 1 up to the target. A milestone holds the conditions of its level that the headline loops (from request to release, from problem to fix) do not meet yet, evaluated after the earlier milestones land. Where a condition has alternatives, the people path (kinds of change) is chosen first, then the alternative needing the fewest new items; the others are listed for engineers. The third loop (from unmet need to new offering) is listed as optional.
- **Kinds of change.** Each milestone moves every main kind to its reach: Level 1 Self-serve, Level 2 Drafted, Level 3 Carried, Level 4 Pre-approved, Level 5 Self-chosen, with the criteria the model's `reach_needs` require for that reach. At Level 1 this is the scoring condition itself; above it, kinds are how users see the level.
- **Value leads.** Every criterion is classified as user-visible or gate (data in the script, tested). User-visible items come first. Critical controls are Level 3 conditions, so they join the Level 3 milestone and never an earlier one.
- **Size.** The largest remediation size among the milestone's criteria (S < M < L). Kinds of change are sized by the agent.
- **Level after.** The assessment is re-scored with every item of this and earlier milestones in place; each milestone must reach its level.
- **Risks.** Raising an AI stage (requests become plans, AI builds changes, diagnosis, proposals, learning from use, proposing new offerings) when the product has no AI features brings the AI Readiness checks into scope, with privacy and cost prompts. Every gate the milestone touches is named.
- **Routes.** *Overlay:* built beside the product, joined at its existing extension points; existing stored data and core logic stay untouched. *Incremental:* the core is changed part by part, with expand-and-contract migrations and versioned interfaces. *Re-platform:* a new core with data moved over, used only when the others cannot reach the goal. Under overlay, a move whose remediation text names migrations, tables, columns, DDL, stores or storage, index mappings, the data model, or "schema and data" is flagged as needing a design decision. This is a keyword rule and can flag a move that only adds new storage beside the product; the agent decides each flag.

## Worked example: Brand AI Apps (updated for v0.7)

Assessment of 8 November 2026. Today: Built to Level 0 (Manual); 1 of 2 main kinds of change self-serve; proven not evidenced. Command: `blueprint.py assessment.json --goal "More customer questions resolved without a person"`.

**Goal.** *More customer questions resolved without a person.* Measure: the share of customer questions answered without a hand-off to a person, read from Insights, with today's value per brand (the agent records it; a blueprint never guesses a number). Kinds that serve it: what the assistant tells customers; products and prices the assistant shows.

**Where it stands.** Owners already change answers themselves, preview, release and undo them. The products and prices the assistant shows still come from files engineers load, so under v0.7 the product reads Level 0, even though its most important kind of change is self-serve. (The v0.6 blueprint read Level 0 for a different reason: an average of how changeable the whole product was.)

**Progress map.**

| # | Milestone | What users get | Level after it | Check | Size | Measure it should move |
|---|---|---|---|---|---|---|
| 1 | Owners edit their catalogue | Brand owners change products and prices in the console, preview what the assistant will say, release and undo | Level 1 (Configurable) | An owner changes a price, the assistant quotes it, the owner undoes it | M (agent's estimate; the script leaves kinds of change unsized) | Hand-offs about prices and stock |
| 2 | AI drafts answers and explains problems | Unanswered questions get a draft answer from the brand's own pages in one click; each rise in refusals comes with its likely cause | Level 2 (Assisted) | An unanswered topic gets a draft citing an official page; the owner releases it; a stricter rule's rise in refusals is linked to that version | L | Share of questions answered without a person |

**Milestone 2, abridged.**

- *What changes for users.* On Insights, an unanswered topic's "Add an approved answer" form gets **Draft with AI**: a short answer quoting only the brand's own source page, which the owner edits, previews and releases as today. Insights also says why refusals rose: which rule, which version was live, and when it changed.
- *Risks.* The product already has AI features; these AI safety gates do not pass yet: the AI sees only what the user may; worse AI results block a release; a full record of AI actions. Privacy: only the brand's public pages are sent, never customer text. Cost: one model call per draft, capped per brand.
- *People.* Brand owners finish and release every draft; nothing reaches customers without them. No written rules for changes without a person are needed before Level 4.
- *For engineers.* `DEL-04` 0 → 2 (Evolution engine, L): a new `packages/core/src/answer-drafts.ts` called from `rules/new-answer`; `LRN-05` 1 → 2 (L): `diagnoseRules()` in `packages/core/src/insights.ts` joining `insight_daily` with settings history.
- *Done when.* Every draft names its source page and ungrounded drafts are rejected; `answer-drafts.test.ts` performs the check on recorded model responses in CI; a fresh assessment, made without sight of this blueprint, reads Level 2.

The safety gates of Level 3 (undo for every change, undo for a code release, tested restore, security checks on every change) appear first in milestone 3, not before the drafting work.
