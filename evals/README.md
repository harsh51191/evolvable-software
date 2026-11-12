# Evaluation set for EVOLVE

EVOLVE asks a product to keep evaluation sets, to block changes that make things worse, and to learn from its own mistakes. This folder holds the framework to the same standard. It measures whether raters read the rubric the same way, and it turns every rater disagreement into a rubric change or an open question.

It has four parts:

| Part | What it is for |
|---|---|
| `cases/` | Three small fixture products with the readings a careful rater should reach |
| `run.py` | Compares one rater's assessment of a case with the expected readings |
| `agreement.py` | Compares two or more assessments of the same real product |
| `disagreements.md` | The log of every disagreement, its cause and the rubric change it led to |

`results/` keeps the result of every run of the cases.

**Limits, stated plainly.** The cases are synthetic and small: a few hundred lines each, written to make a named set of criteria unambiguous. Passing them shows that a rater reads those criteria as intended. It does not show that the rater reads a large real codebase well. Every rating in this repository so far, the field test and the expected readings in these cases alike, was made by an AI model. No human has rated any product yet. A human second rating is the most useful thing anyone can add.

## The cases

| Case | The product | What it tests |
|---|---|---|
| `static-notes` | A notes board where every change is code and a release. No backup, no undo, no signals, no AI. | Every kind of change at reach 0; every loop at Level 0; claims in the README that the code does not back up |
| `rules-desk` | A help desk whose leads change answers and routing rules in an admin page, with checks, history and undo. Failed questions are recorded. A backup command exists, with no restore test. No AI. | Main kinds self-serve (reach 1); Request → Release and Issue → Fix at Level 1; a setting with no undo stays at reach 0; keyword matching is not AI |
| `drafting-desk` | The same desk for several customer organisations, with request intake, grouped failed questions, and an AI lane that drafts routing rules for a lead to finish, within limits set in code. | The drafted kind at reach 2; Request → Release and Issue → Fix at Level 2; `agent_mutations` true; isolation tests that do not make tenant isolation a 3 |

Each case folder holds:

- `repo/`: the fixture repository. This is all a rater may see.
- `expected.json`: the expected readings. A rater must never see it.

`expected.json` names, for each of 15 to 25 criteria, an allowed `[min, max]` score range or an expected status, with a one-line reason and the fixture files that decide it. It also gives the archetype, every scope fact the fixture makes unambiguous, the expected kinds of change (how many are main, and the allowed reach of each kind, matched by keywords in its id or name), the AI-qualified readings where they matter, and the allowed level of each loop. Ranges are narrow where the fixture is clear and wider where the rubric allows two readings; the reason says which.

Expectations marked `"trap": true` are where a careless rater over-scores: a README that claims a feature the code does not have, a backup test that never restores, a security scan that runs only when started by hand, keyword matching sold as "smart", rule-based grouping credited to AI. `run.py` reports the share of traps met separately.

The tests in `tests/test_evals.py` build a reference reading of each case at the low end and at the high end of every range, run it through the real scorer, and check that every expectation holds, loop levels included. If a rubric change moves a case's levels, that test fails.

## Run a rater on a case

1. Copy the case's `repo/` folder somewhere new, on its own. Do not copy `expected.json`, and do not give the rater this repository.
2. Start a fresh agent session with only the skill (`skills/evolvable-software/`) installed and the copied folder as the product to assess. Ask for a full assessment of the default configuration, as the skill describes. Do not hint at the expected readings.
3. Save the assessment JSON the rater writes, for example as `evals/results/2026-11-12-rules-desk-claude.json`.
4. Compare it with the expectations:

   ```bash
   python3 evals/run.py evals/cases/rules-desk evals/results/2026-11-12-rules-desk-claude.json
   python3 evals/run.py evals/cases/rules-desk <assessment>.json --json      # data
   python3 evals/run.py evals/cases/rules-desk <assessment>.json --min 0.9   # stricter pass mark
   ```

   Each expectation is printed as met or missed, with the rater's value and evidence and the reason the expected value is right. The result gives the share met, overall and for the traps. The script exits with 1 when the share is below `--min` (0.8 by default) and 2 when a file cannot be read.

   Loop levels come from `skills/evolvable-software/scripts/score.py --json`. If the assessment does not validate, the levels are reported as unavailable, with the scorer's reasons, and left out of the share. `--no-levels` skips the scorer.

## Compare two raters on a real product

Give two or more raters the same product at the same commit, each blind to the others, and save their assessments. Then:

```bash
python3 evals/agreement.py first.json second.json [third.json ...]
python3 evals/agreement.py first.json second.json --json
python3 evals/agreement.py first.json second.json --criteria GOV-05,DEL-11,ARC-02,ARC-09,ARC-05,GOV-04,GOV-10,LRN-08
python3 evals/agreement.py a.json b.json c.json --labels first,second,third
```

For each pair of raters, overall and per capability, it reports: criteria both assessed, exact agreement, agreement within one level, ranges that overlap once alternates are counted, the mean absolute difference, and criteria where one rater says not applicable or not evidenced and the other assessed. It lists the scope facts that differ, the critical-control criteria separately (they decide whether a loop can pass Level 3), every criterion where the raters differ, and the kinds of change: how many, how many are main, and the reach of kinds whose ids or names match. AI-qualified readings are compared the same way as scores. With three or more raters it adds "all the same" and "all within one".

It accepts older files without the v0.7 fields and abbreviated files that hold only some criteria. A criterion missing from one file counts as "not in both files", never as a disagreement.

Run on the 14 October 2026 second-rating study (one product at a time, then summed over n8n, OpenClaw and Dify), it reproduces that study's numbers: first and second raters exact on 13 of 18 and within one on 17 of 18, both not applicable on 4, applicability different on 2, scope facts different on 3 of 27; all three the same on 8 of 18 and within one on 16 of 18.

```bash
cd assessments/2026-09-field-test
python3 ../../evals/agreement.py n8n/assessment.json second-rating/n8n.json second-rating/chatgpt-n8n.json \
  --labels first,second,third --criteria GOV-05,DEL-11,ARC-02,ARC-09,ARC-05,GOV-04,GOV-10,LRN-08
```

## The rule: rubric changes re-run the cases

Any change to `skills/evolvable-software/references/rubric.md` or to the skill's instructions (`SKILL.md` and the other references) must:

1. pass `python3 -m unittest discover -s tests`, which includes the reference readings of every case;
2. re-run at least one fresh rater on every case, as above, and save each assessment and its `run.py --json` output in `results/`, named `YYYY-MM-DD-<case>-<rater>.json` and `YYYY-MM-DD-<case>-<rater>.run.json`;
3. add a line to `results/README.md`: the date, the change, the rater, and the share met overall and for traps per case.

A case whose share falls below the pass mark blocks the change until the cause is found: either the change made the rubric less clear, or the case's expectation was wrong. Either way, record it in `disagreements.md`.

## How a disagreement becomes a rubric change

1. **Log it.** Every disagreement between raters, every missed expectation in a case, and every error found on re-reading gets a row in `disagreements.md`: the date, the product, the criterion or fact, each reading, and the cause as far as it is known.
2. **Find the cause.** Re-read the evidence both raters cited. The cause is one of: a rater error (the rubric was clear and one rater missed evidence), an unclear definition or anchor (both readings are defensible from the rubric's text), or a missing rule (the rubric says nothing about the case).
3. **Change the rubric** for the last two causes: tighten the definition, anchor or boundary in `rubric.md`, add a case or an expectation that pins the new reading, and record the change in `CHANGELOG.md`. For a rater error, correct the published assessment and say so.
4. **Close the row** with the rubric change, or leave it "open" with what is needed to decide it.
