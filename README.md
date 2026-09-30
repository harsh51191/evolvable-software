# Malleability and Self-Evolution Readiness

![Malleable Software: How ready is your software to self-evolve?](assets/malleable-software-social-preview.png)

An open, evidence-backed framework and agent skill for assessing whether a software product can absorb governed change and safely improve from evidence.

The framework asks four related questions, each reported as its own index:

1. **Malleability:** Can the product's shape change through governed definitions instead of another bespoke release?
2. **Governance:** Are changes versioned, proposed, reviewed, gated by policy, audited and reversible?
3. **Learning:** Does the product observe its own use, turn experience into candidate changes, and measure whether they help?
4. **Factory:** Can changes be built and verified through reproducible, machine-readable surfaces?

Self-evolution readiness is Governance and Learning together, plus a closed-loop check that every stage (observe, propose, review, gate, apply and roll back, measure, verify) is present.

This is a **public beta**. It is designed to create a falsifiable assessment, not a universal software leaderboard.

## What Is Included

- 16 dimensions and 49 anchored criteria.
- Evidence grades and explicit uncertainty handling, with alternate readings reported as ranges.
- Default-configuration scoring, with shipped opt-in settings reported separately.
- Enforced archetype exclusions and an interpretation guide for agent runtimes and developer platforms.
- Seven profiles and four non-overlapping indexes.
- A closed-loop check with a minimum level per stage.
- A deterministic Python scorer with tests.
- A prerequisite-ordered remediation generator.
- A reusable `SKILL.md` for compatible coding agents.
- A field test on 11 open-source systems in `assessments/2026-09-field-test/`, scored from public source code and not yet reviewed by their maintainers.

The framework itself contains no private repository evidence, client examples, or employer-specific terminology.

## Install As A Skill

For Claude Code:

```bash
git clone https://github.com/harsh51191/malleablesoftware.git \
  ~/.claude/skills/malleability-readiness-eval
```

For Codex:

```bash
git clone https://github.com/harsh51191/malleablesoftware.git \
  ~/.codex/skills/malleability-readiness-eval
```

Restart or refresh Codex after installation. The skill can then be discovered for requests involving software malleability, self-evolution, governed product change, factory readiness, or agent-safe action surfaces.

For other agents that support `SKILL.md` packages, clone the repository into the tool's configured skills directory.

## Run The Scorer Directly

Requires Python 3.8 or later. It uses only the standard library.

Create an evidence-input template outside the repository you are assessing:

```bash
python3 scripts/init_scores.py \
  --product "Example Software" \
  --archetype focused-application \
  --source "repository @ immutable-tip" \
  --out ~/msr/example-2026-09-30.json
```

Every criterion starts as `todo`, and the scorer refuses the file until each one is assessed, marked `not_evidenced` with a search scope, or excluded as the archetype allows.

Complete the file using `references/rubric.md` and `references/evidence-plan.md`, then run:

```bash
python3 scripts/score.py ~/msr/example-2026-09-30.json
```

Generate a prerequisite-ordered path to level 3:

```bash
python3 scripts/score.py ~/msr/example-2026-09-30.json --prescribe --target 3
```

Use `--target 4` only for a generative, policy-gated future state.

## Evidence States

Every criterion must be one of:

- `assessed`: assigned an anchored score from 0 to 4 with evidence.
- `not_evidenced`: applicable, but available sources cannot establish presence or absence.
- `not_applicable`: one of the exclusions the declared archetype allows, with a specific rationale.

Missing capability is not the same as non-applicability. Optional fields: `alt_score` (an adjacent level that is also defensible), `available_score` (the level with shipped opt-in settings enabled), `if_applicable` (what an excluded criterion would score).

## Software Archetypes

- Configurable application platform
- Agent runtime
- Developer platform
- Focused application
- Other, with an explicit applicability explanation

Read `references/archetypes.md` before scoring. It lists the allowed exclusions per archetype and explains how to read the rubric for agent runtimes and developer platforms.

## Important Limits

- Repository evidence establishes that a mechanism exists in the inspected source. It does not prove usability, adoption, hosted-edition parity, production reliability, or business impact.
- A closed-loop candidate signal is not a production-readiness certification.
- Cross-product comparison is defensible only when scope, archetype, evidence depth, and applicability decisions are comparable.
- Give maintainers an opportunity to correct factual evidence before publishing comparative scores.
- Do not include credentials, customer identifiers, confidential excerpts, internal URLs, or proprietary evidence in shared scorecards.

## Repository Structure

```text
SKILL.md                         Agent instructions
metadata.yaml                    Package metadata
references/rubric.md             Anchored assessment criteria
references/archetypes.md         Applicability guidance
references/evidence-plan.md      Evidence collection plan
references/remediation.md        Level 3 and 4 improvement moves
references/scorecard-template.md Reporting structure
scripts/init_scores.py           Neutral input generator
scripts/score.py                 Validator, scorer, profiler and prescriber
tests/test_score.py              Scorer tests (python3 -m unittest discover -s tests)
assessments/                     Field-test results
CHANGELOG.md                     Version history
```

## Version

Public Beta 3 (v0.3.0), 30 September 2026. See `CHANGELOG.md` for what changed and why.

## License

MIT. See `LICENSE`.
