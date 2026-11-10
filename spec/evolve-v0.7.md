# EVOLVE v0.7: design

Status: approved in principle by the repository owner on 10 November 2026 ("fix every gap found"). This file is the contract for the v0.7 work. Where it and an older spec disagree, this file wins.

## 1. Why

A critical review of v0.6 found that the scoring engine was sound but the framework did not yet deliver its vision: software that improves itself, driven by its users' requests and its own usage data, with people setting goals and limits, and with the loop improving itself. The gaps, and the change that closes each:

| # | Gap | Change |
|---|---|---|
| 1 | Level 1 measured how platform-like a product is (an average of 20 malleability criteria), not whether people can make the changes they need | Kinds of change (§2) |
| 2 | Nothing checked that a loop actually runs; and a new product designed well scored L0 | Designed, Built, Proven (§3) |
| 3 | Recursion, the headline idea, was barely measured | New criterion LRN-10 (§4) |
| 4 | AI-built change through coding agents and delivery frameworks got no visibility | AI delivery record and rule 12 (§5) |
| 5 | Levels 3 to 5 had no example | A reference product, assessed blind (§11) |
| 6 | Reliability was tested on 8 of 74 criteria, by AI raters only | Full blind second ratings of three products (§12) |
| 7 | Ratings claimed certainty they did not have | Confidence on every score (§6) |
| 8 | Known errors stayed published | Corrections (§12) |
| 9 | The framework had no evaluation set of its own | `evals/` (§10) |
| 10 | Reports were tables of codes | Plain-language report (§7) |
| 11 | No quick version | Quick scan (§8) |
| 12 | No blueprint had been run | One real run, re-assessed blind (§13) |
| 13 | No guidance for new products, no contributor guide, confusing names | Born-evolvable guide, CONTRIBUTING, glossary (§11, §14) |
| B | Blueprint: safety-first ordering, level-first goals, score-chasing steps, no effort or payoff, not built, engineering taxonomy, no people or risk sections, weak checks | Blueprint v2 (§9) |

## 2. Kinds of change

**Idea.** A product is changed in a handful of recurring ways: an answer, a rule, a workflow, a price list, a report, a form. Level 1 asks whether the people running the product can make those changes themselves and undo them.

**Assessment field.** Top-level `change_kinds`, a list of 1 to 8 entries:

```json
{"id": "answers", "name": "What the assistant tells customers", "who": "brand owners",
 "main": true, "reach": 1, "evidence": "path/to/file:line …", "confidence": "high"}
```

- `id`: lowercase letters, digits and hyphens, unique.
- `name`: plain words, no jargon. `who`: who needs to make this change.
- `main`: true when this kind makes up a large share of the changes the product's operators and users actually need. At least one kind is main.
- `reach`: how far this kind of change has come, 0 to 5:

| Reach | Name | Meaning |
|---:|---|---|
| 0 | Engineers only | Needs a code change, a deploy, or an engineer editing files or running scripts |
| 1 | Self-serve | The people running the product make it through a supported path, with no deploy, and can undo it |
| 2 | Drafted | The product drafts this kind of change; a person completes and releases it |
| 3 | Carried | The product builds, checks and releases it end to end; a person approves |
| 4 | Pre-approved | It ships without a person under a written policy, and is reversed automatically when it makes things worse |
| 5 | Self-chosen | The product also decides when to make this kind of change, within policy |

**Rules for raters (rubric text).**
- List every kind of change operators or users commonly need, from the product's own documentation, admin surfaces and request history, including kinds they cannot make themselves. A kind left out to raise the level is a finding, like a wrongly declared scope fact.
- Record the evidence for each kind and for its reach.
- Reach 1 needs both the supported path and undo. A path with no undo is reach 0, and the evidence says so.

**Scoring.**
- The `people` build path for Request → Release and Issue → Fix becomes `{"kinds": "main"}`: its value is 2 when every main kind has reach 1 or more, otherwise 1 when any kind has reach 1 or more, otherwise 0. The level-1 condition is unchanged in form (`people ≥ 2` or `product ≥ 2`).
- Opportunity → Expansion keeps EXP-02 as its people path.
- The Open (MAL) capability stays in the profile and no longer gates Level 1.
- Consistency checks (validation errors): reach ≥ 2 needs DEL-04 ≥ 2, or LRN-07 ≥ 2 with LRN-08 ≥ 2; reach ≥ 3 needs DEL-04 ≥ 3; reach ≥ 4 needs GOV-07 ≥ 3; reach 5 needs LRN-07 ≥ 3. These use default scores.
- `change_kinds` is required. An assessment without it fails validation.
- The scorer reports a table of kinds with their reach, and "n of m main kinds are self-serve".

## 3. Designed, Built, Proven

Three different claims, never mixed:

| Claim | Evidence | Where |
|---|---|---|
| **Designed for** | Design documents and architecture, before or beside the code | An assessment with `"basis": "design"` |
| **Built to** | What ships: code, with tests where the depth cap needs them | An assessment with `"basis": "shipped"` (the default) |
| **Proven at** | Operating records showing real changes going through the loop | `proven` in a shipped assessment |

**Design basis.** `"basis": "design"` allows evidence grade `D` (a design document, cited by path and section). Grade D is an error in a shipped assessment. In a design assessment, facets are not required and the depth cap does not apply; inventories still apply. Every headline and report says "Designed for", and states that a design reading is not comparable with a shipped one. `proven` is not allowed.

**Proven.** Optional top-level field in a shipped assessment:

```json
"proven": {
  "request": {"level": 1, "evidence": "…"},
  "fix": {"status": "not_evidenced", "searched": "…"},
  "expansion": {"status": "not_evidenced", "searched": "…"}
}
```

A loop is proven at level N when operating records (change history, release records, audit logs, published changelogs, incident records) show real changes going through the loop at that level, more than once, in a real deployment. `level` is 0 to the loop's built level; a higher value is a validation error. The headline proven level is the lower of Request → Release and Issue → Fix; when either is missing or not evidenced, the headline says "Proven: not evidenced". From a repository alone, proven is usually not evidenced, and the report says so plainly.

**Operated moves out of Built.** The `operated` flags are removed from the level-5 conditions, and scoring rule 13 becomes: a 3 or a 4 on a depth-capped criterion needs `tested`. The `operated` facet is still recorded and reported, as support for a Proven reading. Built says what the product can do; Proven says what it has been seen to do. A product should run at the level it has proven, and raise autonomy as proof accumulates.

**Headline.** `Built to SAL 2 (Assisted) · Proven: not evidenced · AI-driven 0 · Request → Release L2 (AI L2) · …`. In a design assessment: `Designed for SAL 4 (Policy-bounded) · …`.

## 4. LRN-10: the improvement loop improves itself

New criterion in capability LRN, area "Measure", after LRN-09. It always applies.

**Definition.** The checks, evaluation sets, policies and prompts that govern change are themselves changed through the governed path, driven by measured results.

**Why it matters.** This is what makes self-improvement recursive. A loop whose own checks never improve repeats its mistakes at higher speed.

**Evidence.** Where checks, evaluation cases, policies and prompts live and how they change. Whether a production failure or a wrong pass is recorded against the check that missed it. Whether new tests or evaluation cases are created from failures. Whether policy changes cite measured results.

- **0** The checks, evaluation sets, policies and prompts that govern change are fixed in code and change only when engineers edit them.
- **1** People improve them by hand after incidents, outside the product.
- **2** They are versioned definitions that change through the product's governed change path, but nothing links those changes to measured results.
- **3** Results drive them: failures and wrong passes are recorded against the check, evaluation case or policy involved, and the product turns them into proposed changes to those checks, cases and policies (for example, a production failure becomes a new test), which a person approves.
- **4** The product makes such changes itself within policy, measures whether they improved later decisions, and reverses those that did not.

**Conditions.** Level 4 adds LRN-10 ≥ 2 (part `spine`, stage `Observe`). Level 5 adds LRN-10 ≥ 4 (same part and stage). The scorer reports a **Recursion** line from the LRN-10 score: 0 Fixed, 1 By hand, 2 Governed, 3 Results-driven, 4 Self-improving.

The rubric then has 67 criteria and 8 AI Readiness checks, 75 in all.

## 5. AI delivery and rule 12

**Record.** Optional top-level field:

```json
"ai_delivery": {"present": true, "qualifies": false, "evidence": "AGENTS.md; .github/workflows/…", "note": "…"}
```

`present`: engineers build this product with AI coding agents or a delivery framework (agent instruction files, agent workflows in CI, an installed AI software factory). `qualifies`: it meets rule 12, so DEL-01, DEL-04 and the other rule-12 criteria may credit it. `qualifies` true needs `present` true. The record never changes a score by itself; credit flows through the criteria. Reports say, in plain words, that AI-assisted engineering is not the product evolving itself, and whether it counts.

**Rule 12, clarified.** Add: "An installed delivery framework, such as an AI software factory, or a repository's agent workflows count as a first-party evolution system when, in the assessed repository: they are installed at a pinned version and maintained with the product; their enforcement runs (authority and merge checks are required checks, not documents); their limits meet GOV-10 for the changes they make; and their product layer describes this product. Instruction files, rules and templates alone are documentation and count for nothing. A framework that ships code sets `code_release_path`, so release rollback (DEL-11) applies."

## 6. Confidence

Each assessed criterion, each assessed AI reading and each kind of change may record `confidence`: `high` (read the code path and its tests), `medium` (read the code, not every path), or `low` (inferred from part of the evidence). All or nothing: if any assessed criterion has it, every assessed criterion must. The skill requires it for new assessments. The scorer reports the counts and lists low-confidence criteria that hold a blocker or a critical control, as "check these first".

## 7. Plain-language report

`scripts/report.py <assessment.json>` prints a report a business or product reader can follow. No criterion codes in the body; an appendix maps plain names to codes for engineers.

Content comes from `references/plain-language.md` (new), which holds for every criterion a short plain name and a plain question, and plain text for the levels, loops, parts, controls and capabilities. The script refuses to run when any criterion or control lacks plain text.

Sections, in order: In one paragraph. Where it stands (the level, in words, and what it means for the people using and running the product). The kinds of change. What works today. What holds it back. Safety gates. How much AI does. Has it been proven. How sure this reading is. What to do next (the next level's challenge). For engineers (codes).

The agent adds the product's story on top; the script supplies everything that can be computed.

## 8. Quick scan

`scripts/quick_scan.py <answers.json>` and `references/quick-scan.md`: about 18 plain yes/no/unsure questions that take ten minutes from a README, an admin surface and the CI configuration. It prints an indicative range per loop ("likely L1 to L2"), the safety gates that look open, and what a full assessment would check. It is always labelled indicative, never a level, and cannot be published as a result.

## 9. Blueprint v2

`scripts/blueprint.py <assessment.json> --goal "<business goal>"` prints the skeleton; `references/blueprint-template.md` (new) defines the format. This replaces `evolution-blueprint-v0.7.md` and the hand-written trials.

Rules:
1. **Start from a business goal,** in the owner's words, and name the kinds of change that serve it.
2. **Value leads.** Milestones are ordered by what users gain. A safety gate is attached to the first milestone that needs it, never front-loaded.
3. **Every step names a gain a user can see,** or is labelled a gate. A step that only moves a score is not allowed.
4. **A progress map** from today to Level 5: milestone, what users get, the level after it, and a check a person can run on the live product.
5. **Effort and payoff:** a relative size (S, M, L) and the measure the milestone should move.
6. **Risks and what a step brings into scope** (for example, adding AI brings the AI Readiness checks, privacy and cost).
7. **People:** who approves, who sets the policy for what ships without a person, and what changes in roles.
8. **Engineering notes, a prompt for a coding agent and a "done when" checklist** under each milestone.
9. **Checks are scripts where possible:** the done-when list names an automated test that performs the challenge.
10. **Re-assess fresh:** the level counts only when a new assessment, made without sight of the blueprint, finds the evidence.
11. **Building blocks stay internal.** The eight blocks may guide the agent; they do not appear in the reader's text.

## 10. Evaluation set for the framework

`evals/`: small fixture repositories with expected readings for named criteria, kinds of change and scope facts; `evals/run.py` compares an assessment with the expectations and reports agreement; `evals/agreement.py` compares two assessments. `evals/disagreements.md` logs every rater disagreement and the rubric change it led to. Three definitions are tightened now: LRN-08 for products with no learning loop, `multi_tenant`, and `code_release_path` with `agent_mutations`.

## 11. New products: born evolvable

`docs/born-evolvable.md`: the twelve foundations for a product designed for Level 5 from day one, a day-0 checklist, what to make data and what to leave as code, and how to get a "Designed for" reading. `examples/born-evolvable/`: a small reference product that follows the foundations, with tests. It is assessed blind and its result published, whatever it is; it is the first example above Level 2.

## 12. Field test

All 11 products are brought to v0.7 at their pinned commits: kinds of change, LRN-10, confidence, the AI delivery record and a proven reading. Three known corrections are applied: n8n GOV-04 to 2, OpenClaw ARC-09 scheduled work to 2, LibreChat MAL-06 to 2. Three products (LibreChat, Frappe, n8n) get a full blind second rating across every criterion.

## 13. One real run

Brand AI Apps milestone 1 (AI-drafted answers) is built on a branch of its own repository from the blueprint's prompt, and re-assessed by a rater that has not seen the blueprint. The result stays in that private repository.

## 14. Housekeeping

`CONTRIBUTING.md`; a glossary of plain names and codes; README, SKILL, CHANGELOG and manifests at 0.7.0.

## 15. Tests that must hold

- An assessment without `change_kinds` fails validation; every consistency check in §2 has a test.
- A product whose main kinds are all self-serve reaches the level-1 build condition whatever its MAL score; one main kind at reach 0 fails it.
- Grade D is valid only in a design assessment; `proven` is invalid there; a proven level above the built level is an error.
- No level condition requires `operated`; a 4 on a depth-capped criterion needs `tested` only.
- LRN-10 is required at levels 4 and 5 as stated; the Recursion line follows its score.
- `ai_delivery` never changes a score.
- Confidence is all or nothing.
- Every criterion and control has plain text; the report body contains no criterion code.
- The field test regenerates with no difference.
