---
name: malleability-readiness-eval
description: >-
  Evaluate a software product's readiness for governed change and closed-loop
  improvement using the MSR framework. Produces an evidence-backed profile and
  four indexes (malleability, governance, learning, factory) with score ranges,
  default-versus-opt-in readings and a closed-loop check, plus a
  prerequisite-ordered remediation plan. Works for platforms, focused
  applications, developer platforms and agent runtimes. Use for malleability, self-evolution,
  metadata-driven maturity, software-factory readiness, agent-safe action
  readiness, or repeatable reassessment. Do not use as a security, accessibility,
  PR, or delivery-process audit.
allowed-tools: Read, Grep, Glob, Bash, Agent, Write
---

# Malleability and Self-Evolution Readiness Evaluation

## Purpose

Assess whether a software product can absorb governed change without turning every request into a bespoke code release, and whether it can safely learn from evidence. The assessment separates:

- **Malleability:** how much product shape can be changed through governed definitions.
- **Governance:** whether changes are versioned, proposed, reviewed, gated by policy, audited and reversible.
- **Learning:** whether the product observes its own use, turns experience into candidate changes, and measures whether they help.
- **Factory:** whether changes can be built and verified through reproducible machine-readable surfaces.

Self-evolution readiness is Governance and Learning read together, plus the closed-loop check.

The result is a profile, not a universal product leaderboard. Different software archetypes have different applicable criteria.

## Use It For

- A baseline before platform or architecture investment.
- Evidence-backed comparison of releases of the same software.
- Locating blockers in definition layers, governance, verification, or learning loops.
- Producing a remediation sequence after the current state is scored.

## Do Not Use It For

- Security or accessibility conformance.
- General code quality or pull-request review.
- Team delivery performance.
- Roadmap scoring or future-state promises.
- Declaring production readiness from repository evidence alone.

## Procedure

### 1. Establish Scope

Record the software name, repository paths, branches or immutable tips, assessment date, scope, and archetype.

Scope must include every first-party repository that implements the product's core behaviour (companion optimisers, agent servers, evaluation harnesses). Read the architecture docs: if the named repository delegates capabilities elsewhere, add that repository or record where they live.

Read `references/archetypes.md` before choosing among:

- `configurable-application-platform`
- `agent-runtime`
- `developer-platform`
- `focused-application`
- `other`

Assess only repositories and documents the user supplied or authorized. Never mutate the target repository. Ask before cloning or accessing a new remote source.

### 2. Create The Evidence Input

Generate an input file with the skill's own scripts (paths below are relative to this skill's directory, not the target repository). Write it outside the target repository, and never overwrite an earlier assessment:

```bash
python3 <skill-dir>/scripts/init_scores.py --product "<software name>" --archetype <type> --source "<repo and tip>" --out <outside-target>/<product>-<date>.json
```

Every criterion starts as `todo`. Replace each with one of:

- `assessed`: an anchored score from 0 to 4 supported by evidence.
- `not_evidenced`: the assessment looked but could not establish the capability.
- `not_applicable`: one of the exclusions the archetype allows (`references/archetypes.md`), with a rationale and, ideally, `if_applicable`.

Do not use `not_applicable` merely because a capability is missing. The scorer rejects exclusions the archetype does not allow.

### 3. Gather Evidence

Follow `references/evidence-plan.md`. Read the target at the named branch or tip. For any product that claims to learn or self-improve, work through the self-modification checklist in `references/archetypes.md` before scoring F, J, M or P. For parallel exploration, give each explorer only the relevant rubric dimensions and require file paths, short evidence summaries, who can make the change, and whether a deployment is required.

Evidence grades:

- `A`: verified in code at the named tip.
- `B`: verified in first-party documentation, audit material, or configuration supplied for the assessment.
- `C`: inferred from secondary material or product knowledge; scores are capped at 2.

`not_evidenced` is uncertainty, not proof of absence. Record where the assessment searched.

### 4. Score

Use the anchored levels in `references/rubric.md`. Between two levels, select the lower and record the higher as `alt_score`. Score what exists now, not what is planned. Score the default configuration; when a shipped opt-in setting raises a level, record it as `available_score`. Learning criteria credit changes to the product's own behaviour, including what its operators configure in it, not improvements it makes to other software.

```bash
python3 <skill-dir>/scripts/score.py <file>.json
```

The scorer validates coverage, evidence, statuses, archetype exclusions, caps and incident deductions, and reports ranges and the opt-in variant. Never recompute indexes manually.

### 5. Verify

Re-read primary evidence for every criterion at 3 or 4. For every assessed zero, cite the inspected surface. For every `not_evidenced`, state the search scope. Treat repository evidence as mechanism evidence, not proof of usability, adoption, hosted-edition parity, or business impact.

### 6. Prescribe

```bash
python3 <skill-dir>/scripts/score.py <file>.json --prescribe --target 3
```

Use `--target 4` only for a generative, policy-gated future state. The script orders changes by prerequisites. Projected scores are ceilings if every move lands, not forecasts. Re-estimate all sizes for the assessed software.

### 7. Report

Use `references/scorecard-template.md`. Report:

- the profile and the four indexes, with ranges and the opt-in column;
- coverage, uncertainty, and exclusions;
- largest blockers and strongest evidence;
- every applied cap or deduction;
- the closed-loop stages that fail, by default and with opt-in settings;
- repository and operational evidence limits;
- the remediation sequence when requested.

Do not label a product "self-evolving" because an average crossed a threshold. The scorer reports only whether the minimum closed-loop mechanisms are evidenced as a **candidate**; operational validation is still required. For comparisons across products, show ranges, and run a second independent pass on F, J, M and P.

## Public-Use Guardrails

- The framework contains no private product examples or employer-specific terminology. The field test in `assessments/` scores public open-source code only.
- Generated reports may name only the software the user explicitly asked to assess.
- Never include confidential repository excerpts, credentials, customer names, tenant identifiers, or internal URLs in a shared report.
- Do not publish comparative scores without giving maintainers a chance to correct factual evidence and without disclosing evidence limitations.
- Preserve prior score inputs for re-assessments; never overwrite historical evidence.

## Files

- `references/rubric.md`: criterion definitions and anchored levels.
- `references/archetypes.md`: applicability and profile guidance.
- `references/evidence-plan.md`: evidence collection instructions.
- `references/remediation.md`: prerequisite-aware moves to levels 3 and 4.
- `references/scorecard-template.md`: report structure.
- `scripts/init_scores.py`: score-input template generator.
- `tests/test_score.py`: scorer tests.
- `assessments/`: field-test results under this rubric.
- `scripts/score.py`: validator, scorer, profiler, and prescriber.
