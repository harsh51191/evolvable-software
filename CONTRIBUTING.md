# Contributing to EVOLVE

Thank you for helping. EVOLVE is young, and every result in this repository is provisional. Every score so far was made by an AI model, and no product has had a human rating. **A human second rating of any product in the field test is the most valuable contribution you can make.**

## How the repository is laid out

| Path | What it holds |
|---|---|
| `skills/evolvable-software/` | The agent skill: `SKILL.md`, `references/` and `scripts/` |
| `skills/evolvable-software/references/rubric.md` | Every criterion, its anchored levels, and the scoring model |
| `skills/evolvable-software/references/remediation.md` | The moves that take each criterion to levels 3 and 4 |
| `skills/evolvable-software/scripts/` | `score.py` (validate and score), `init_scores.py`, `report.py`, `quick_scan.py`, `blueprint.py` |
| `spec/` | The design and decisions for each version; `spec/evolve-v0.7.md` is the current contract |
| `assessments/2026-09-field-test/` | Eleven open-source products assessed with EVOLVE, and the blind second-rating study |
| `evals/` | The framework's own evaluation set: fixture cases, `run.py`, `agreement.py`, the disagreement log |
| `examples/`, `docs/` | A small reference product and guides |
| `tests/` | Unit tests for the scripts and the evaluation set |

## One source of truth

- `rubric.md` is the only place criteria and the scoring model live: criterion ids, anchors, scope facts, applicability, loop conditions, critical controls, caps. `score.py` reads them from it. Never copy a threshold into code or another document.
- `remediation.md` is the only place moves live.
- Plain-language names for business readers live in `references/plain-language.md`.

## Run the tests

```bash
python3 -m unittest discover -s tests -v
```

The scripts use the Python standard library only and support Python 3.9 and later.

To regenerate the field test, run `python3 tools/build.py` from `assessments/2026-09-field-test/`. Then check `git diff`. CI fails on any difference, so every change in a generated file must be one you can explain.

## What a change to the rubric must include

1. **Tests** for any new rule, condition or check in `score.py`.
2. **The evaluation cases re-run.** `tests/test_evals.py` must pass. Also run a fresh rater on every case and record the result in `evals/results/`. See `evals/README.md`.
3. **A changelog entry** in `CHANGELOG.md`, saying what changed and why, in plain words.
4. **The field test rebuilt**, with every difference explained in the pull request. An unexplained difference is a bug.
5. If the change settles a disagreement, close its row in `evals/disagreements.md`.

## Report a score you believe is wrong

Open an issue. Name the assessment file and the criterion, and give the file and line in the assessed product that shows the score is wrong, at the commit the assessment names. One citation beats a paragraph of argument. Corrections are logged in `evals/disagreements.md` and applied in the next field-test rebuild.

## Add a second rating

Rate a product from the field test blind: do not read its existing assessment first. Use the skill's procedure and the same commit. Then compare your rating with the first one:

```bash
python3 evals/agreement.py assessments/2026-09-field-test/<product>/assessment.json your-rating.json
```

Submit your assessment JSON and the comparison. Say whether you are a person or an AI model, and which one. Log each disagreement in `evals/disagreements.md`.

## Writing style

- Plain words and short sentences. British spelling.
- Evidence for every claim: a file and line, a document and section, or a test.
- No criterion codes in text meant for business readers. Use the plain names in `references/plain-language.md`; codes belong in engineering appendices.
- Say what is not known. "Not evidenced" is a finding, not a failure to hide.
- Results are provisional readings of repository evidence, not verdicts on a product. Say so wherever results are quoted.
