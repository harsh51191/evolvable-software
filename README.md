# Malleability and Self-Evolution Readiness

An open, evidence-backed framework and agent skill for assessing whether a software product can absorb governed change and safely improve from evidence.

The framework asks three related questions:

1. **Malleability:** Can the product's shape change through governed definitions instead of another bespoke release?
2. **Self-Evolution:** Can observations become evidence-backed proposals, pass policy, be applied, measured, and reversed?
3. **Factory Readiness:** Can changes be built and verified through reproducible, machine-readable surfaces?

This is a **public beta**. It is designed to create a falsifiable assessment, not a universal software leaderboard.

## What Is Included

- 15 dimensions and 48 anchored criteria.
- Evidence grades and explicit uncertainty handling.
- Archetype-aware applicability.
- Seven profile views plus three aggregate indexes.
- Critical closed-loop floors.
- A deterministic Python scorer.
- A prerequisite-ordered remediation generator.
- A reusable `SKILL.md` for compatible coding agents.

The package contains no real-product fixtures, private repository evidence, client examples, or employer-specific terminology.

## Install As A Codex Skill

```bash
git clone https://github.com/harsh51191/malleablesoftware.git \
  ~/.codex/skills/malleability-readiness-eval
```

Restart or refresh Codex after installation. The skill can then be discovered for requests involving software malleability, self-evolution, governed product change, factory readiness, or agent-safe action surfaces.

For other agents that support `SKILL.md` packages, clone the repository into the tool's configured skills directory.

## Run The Scorer Directly

Requires Python 3.8 or later. It uses only the standard library.

Create a neutral evidence-input template:

```bash
python3 scripts/init_scores.py \
  --product "Example Software" \
  --archetype focused-application \
  --source "repository @ immutable-tip" > scores.json
```

Complete `scores.json` using `references/rubric.md` and `references/evidence-plan.md`, then run:

```bash
python3 scripts/score.py scores.json
```

Generate a prerequisite-ordered path to level 3:

```bash
python3 scripts/score.py scores.json --prescribe --target 3
```

Use `--target 4` only for a generative, policy-gated future state.

## Evidence States

Every criterion must be one of:

- `assessed`: assigned an anchored score from 0 to 4 with evidence.
- `not_evidenced`: applicable, but available sources cannot establish presence or absence.
- `not_applicable`: outside the declared product archetype, with a specific rationale.

Missing capability is not the same as non-applicability.

## Software Archetypes

- Configurable application platform
- Agent runtime
- Developer platform
- Focused application
- Other, with an explicit applicability explanation

Read `references/archetypes.md` before interpreting or comparing results.

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
```

## Version

Public Beta 2, released 29 September 2026.

The beta adds archetype-aware assessment, distinguishes absence from uncertainty and non-applicability, introduces profile reporting, adds post-change impact measurement, and replaces a binary readiness verdict with a minimum closed-loop candidate signal requiring operational validation.

## License

MIT. See `LICENSE`.
