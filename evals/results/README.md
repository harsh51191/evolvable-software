# Results of the evaluation cases

Every run of a rater on a case is kept here, and never overwritten:

- `YYYY-MM-DD-<case>-<rater>.json`: the assessment the rater wrote;
- `YYYY-MM-DD-<case>-<rater>.run.json`: the output of `python3 evals/run.py evals/cases/<case> <assessment> --json`.

Add a row below for each run. "Change" is the rubric or skill change that prompted the run, or "baseline".

| Date | Change | Case | Rater | Met | Traps met | Levels | Notes |
|---|---|---|---|---:|---:|---|---|
| 2026-11-17 | baseline (v0.7.0) | static-notes | Claude Opus, blind | 40 of 44 (91%) | 5 of 5 | all L0, as expected | Missed the change-path scope facts (read every change as a code release path, not configuration), and the two criteria they switch: DEL-11 and GOV-05. The case and the rubric disagree on how to classify a product whose only changes are code; logged as open. |
| 2026-11-17 | baseline (v0.7.0) | rules-desk | Claude Opus, blind | 46 of 47 (98%) | 5 of 6 | L1, L1, L0, as expected | Missed the keyword-bot trap: scored the conversational criterion 0, not 1. |
| 2026-11-17 | baseline (v0.7.0) | drafting-desk | Claude Opus, blind | 55 of 56 (98%) | 8 of 9 | L2, L2, L1, as expected | Same keyword-bot miss. Caught every README claim the code does not back. |

The cases were written on 12 November 2026 for EVOLVE v0.7, and first rated blind on 17 November by a fresh rater that saw only the skill and each case's `repo/` folder. Their expected readings pass the scorer at both ends of every range (`tests/test_evals.py`), but that checks the expectations against the scorer, not a rater against the expectations. The first fresh-rater run of each case is the baseline.
