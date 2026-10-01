# EVOLVE: how ready is your software to evolve itself?

An open, evidence-backed framework and agent skill that answers one question: **how ready is a software product to evolve itself safely?**

The question breaks into three loops:

| Loop | Can the product... |
|---|---|
| **Request → Release** | take a user's request, implement it properly and release it? |
| **Issue → Fix** | find the problems users face, fix them and ship the fix? |
| **Opportunity → Expansion** | notice adjacent needs it does not serve yet, and propose or launch them? |

Each loop gets a **Software Autonomy Level (SAL)** from L0 to L5, modelled on the levels used for self-driving cars:

| Level | Name | What the product can do |
|---|---|---|
| L0 | Manual | Every change is engineers writing and releasing code. |
| L1 | Configurable | People make the change without bespoke engineering, and can roll it back. |
| L2 | Assisted | The product structures the request, diagnoses the issue or drafts the proposal, and drafts the change. People build and release. |
| L3 | Supervised | The product carries the loop end to end; a person approves each release. Every critical control passes. |
| L4 | Policy-bounded | Low-risk changes ship without a person, under policy, with staged exposure, measurement and automatic rollback. |
| L5 | Self-directing | The product initiates, ships and measures change within policy, backed by operational evidence. |

The headline is the lower of the first two loops, with Expansion reported beside it, for example **SAL 2 · Request → Release L2 · Issue → Fix L2 · Expansion L1**. The scorer always names what blocks the next level.

Behind the levels is the **EVOLVE profile**: six capabilities, each scored 0 to 4.

| | Capability | Asks |
|---|---|---|
| **E** | Elastic (`ARC`) | Does the architecture scale, survive failure and recover its data? |
| **V** | Velocity (`DEL`) | Can a change be built, verified and released quickly and safely? |
| **O** | Open (`MAL`) | Can the product be reshaped without a code release? |
| **L** | Learn (`LRN`) | Does it notice what is wrong, work out why, and measure whether changes helped? |
| **V** | Vet (`GOV`) | Is every change reviewed, policy-gated, audited and reversible, including the changes it makes to itself? |
| **E** | Expand (`EXP`) | Does it find and launch adjacent value? |

This is a **public beta**. It is designed to produce a falsifiable assessment, not a universal software leaderboard. `spec/evolve-v0.4-draft.md` explains the design and every decision behind it.

## What is included

- 66 anchored criteria in six capabilities, each with a 0–4 ladder.
- Three loops, each scored by its weakest stage. A loop's level is the lowest of four parts: the loop's own stages, a shared release spine (build, verify, stage, release, observe, roll back), an architecture foundation and a governance ceiling.
- Seven critical controls:
  - definition rollback;
  - release rollback;
  - safe migrations;
  - tested backup and restore;
  - tenant isolation;
  - security;
  - bounded self-change.

  A failed applicable control caps every loop at L2.
- Seven scope facts that decide which criteria and controls apply, so a local tool is not failed on tenant isolation.
- Evidence grades, evidence facets (implemented, tested, operated) and a depth cap: architecture and control criteria need tested evidence for a 3 and operated evidence for a 4.
- Scoring of the default configuration, with shipped opt-in settings and higher alternate readings reported separately.
- Enforced archetype exclusions and an interpretation guide for agent runtimes and developer platforms.
- A deterministic Python scorer with tests, and a remediation generator that orders work by prerequisites.
- A reusable `SKILL.md` for compatible coding agents.
- A field test on 11 open-source systems in `assessments/2026-09-field-test/`, scored from public source code and not yet reviewed by their maintainers.

The framework itself contains no private repository evidence, client examples or employer-specific terminology.

## Install as a skill

For Claude Code:

```bash
git clone https://github.com/harsh51191/malleablesoftware.git \
  ~/.claude/skills/evolvable-software
```

For Codex:

```bash
git clone https://github.com/harsh51191/malleablesoftware.git \
  ~/.codex/skills/evolvable-software
```

Restart or refresh the agent after installation. The skill can then be discovered for requests about self-evolution readiness, software autonomy levels, governed product change, architecture readiness for autonomous change, or agent-safe action surfaces.

## Run the scorer directly

Requires Python 3.8 or later. It uses only the standard library.

Create an input template outside the repository you are assessing:

```bash
python3 scripts/init_scores.py \
  --product "Example Software" \
  --archetype focused-application \
  --source "repository @ immutable-tip" \
  --out ~/evolve/example-2026-10-01.json
```

Every scope fact starts empty and every criterion starts as `todo`. The scorer refuses the file until each of these holds:

- each fact is true or false, with evidence;
- each criterion is assessed, marked `not_evidenced` with a search scope, or excluded as the archetype or a scope fact allows.

Complete the file using `references/rubric.md` and `references/evidence-plan.md`, then run:

```bash
python3 scripts/score.py ~/evolve/example-2026-10-01.json
```

Generate a plan that starts with what blocks the next level:

```bash
python3 scripts/score.py ~/evolve/example-2026-10-01.json --prescribe --target 3
```

## Evidence states and fields

Every criterion must be one of:

- `assessed`: an anchored score from 0 to 4 with evidence.
- `not_evidenced`: applicable, but the sources cannot establish presence or absence.
- `not_applicable`: an exclusion the archetype allows, or a criterion a false scope fact switches off, with a rationale.

Optional fields:

- `alt_score`: the next level up, also defensible.
- `available_score`: the level with shipped opt-in settings on.
- `facets`: implemented, tested, operated.
- `inventory`: a level per surface, for criteria that span several surfaces.
- `if_applicable`: what an excluded criterion would score.

## Important limits

- Repository evidence establishes that a mechanism exists in the inspected source. It does not prove usability, adoption, hosted-edition parity, production reliability or business impact. The operated facet makes this limit visible.
- A Software Autonomy Level is a readiness reading, not a production certification.
- Cross-product comparison is defensible only when scope, archetype, scope facts, evidence depth and applicability decisions are comparable.
- Give maintainers an opportunity to correct factual evidence before publishing comparative scores.
- Do not include credentials, customer identifiers, confidential excerpts, internal URLs or proprietary evidence in shared scorecards.

## Repository structure

```text
SKILL.md                          Agent instructions
metadata.yaml                     Package metadata
spec/evolve-v0.4-draft.md         Design and decisions
references/rubric.md              Criteria, anchored levels and the scoring model
references/archetypes.md          Applicability and interpretation guidance
references/evidence-plan.md       Evidence collection plan
references/remediation.md         Level 3 and 4 improvement moves
references/scorecard-template.md  Reporting structure
scripts/init_scores.py            Input template generator
scripts/score.py                  Validator, scorer and prescriber
tests/test_score.py               Scorer tests (python3 -m unittest discover -s tests)
assessments/                      Field-test results
CHANGELOG.md                      Version history
```

## Name and version

EVOLVE v0.4.0, public beta 4, 1 October 2026. EVOLVE was previously the Malleability and Self-Evolution Readiness (MSR) framework; see `CHANGELOG.md` for what changed and why. "EVOLVE" and "Software Autonomy Level" are working names until a trademark and prior-use search is complete.

## License

MIT. See `LICENSE`.
