# Results of the evaluation cases

Every run of a rater on a case is kept here, and never overwritten:

- `YYYY-MM-DD-<case>-<rater>.json`: the assessment the rater wrote;
- `YYYY-MM-DD-<case>-<rater>.run.json`: the output of `python3 evals/run.py evals/cases/<case> <assessment> --json`.

Add a row below for each run. "Change" is the rubric or skill change that prompted the run, or "baseline".

| Date | Change | Case | Rater | Met | Traps met | Levels | Notes |
|---|---|---|---|---:|---:|---|---|

No rater has been run on the cases yet. The cases were written on 12 November 2026 for EVOLVE v0.7. Their expected readings pass the scorer at both ends of every range (`tests/test_evals.py`), but that checks the expectations against the scorer, not a rater against the expectations. The first fresh-rater run of each case is the baseline.
