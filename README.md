# EVOLVE: how ready is your software to evolve itself?

An open, evidence-backed framework and agent skill that answers one question: **how ready is a software product to evolve itself safely?**

## What evolvable software means

**Evolvable software improves itself.** It takes in what users ask for, notices what goes wrong, and spots needs it does not serve yet. Then it changes its own behaviour to meet them, safely, within limits people set.

At the top of the scale the improvement becomes **recursive**. The product measures the effect of every change it makes, and uses the results to improve how it changes itself: its checks, its policies and its choice of what to do next. It is recursive self-improvement applied to software products, with safety built in. In the rubric, recursion is concrete:
- at L4, measured impact decides whether a change is kept, revised or rolled back (LRN-09);
- at L5, the product's policy adapts to how often its own checks wrongly passed a change (GOV-07), the results of evaluating its learned changes feed that policy (LRN-08), and it learns which kinds of change succeed (LRN-07).

Three things it is not:

- **Not an AI coding agent editing your repository.** An agent can build the machinery. The product has evolved when users can do something *in the running product* that they could not do before.
- **Not AI features bolted on.** A product can have a lot of AI and evolve itself not at all. EVOLVE reports both: how far the product evolves, and how much of that AI does.
- **Not autonomy without limits.** Each level adds autonomy only on top of the safety to undo it.

**Why a product cannot jump levels.** Each level rests on the ones below, and the level is set by the weakest link. A product cannot be trusted to change itself until every change can be undone and a backup restored, so seven critical controls must pass before L3. And it cannot automate what people cannot yet do safely by hand. n8n shows this in the field test: its AI already builds workflows, yet it stays at L2, because credentials, variables and settings cannot be rolled back in the product and its restore is untested. The AI is ahead of its safety net.

**What done means.** For any target level, the scorer prints a definition of done for each loop: a **challenge** to run on the running product, and the **evidence** the next assessment must find, taken from the rubric itself.

```bash
python3 skills/evolvable-software/scripts/score.py assessment.json --checklist 2
```

A loop is done when its challenge passes and a fresh assessment finds every item. A level is never claimed from a plan, a prompt or a pull request alone.

## Four ways to use it

| You want | Run | Time |
|---|---|---|
| A quick, indicative reading | `scripts/quick_scan.py`: about twenty plain yes/no questions, a likely range per loop. Never published as a level. | Ten minutes |
| A full assessment | The skill, in Claude Code, Codex or Gemini CLI, scores every criterion from the code and runs `scripts/score.py`. | Hours |
| A report a business reader can follow | `scripts/report.py assessment.json`: plain words, codes only in a section for engineers. | Seconds |
| A plan to move up | `scripts/blueprint.py assessment.json --goal "<your goal>"`: milestones led by what users gain, each with a check to run, a prompt for a coding agent and a "done when" list. | Minutes, plus the agent's writing |

**Starting a new product?** Read [Born evolvable](docs/born-evolvable.md): twelve foundations for a product designed for Level 5 from day one, and [Answer Desk](examples/born-evolvable/), a small working product that follows them.

## The three loops and six levels

The question breaks into three loops:

| Loop | Can the product... |
|---|---|
| **Request → Release** | take a user's request, implement it properly and release it? |
| **Issue → Fix** | find the problems users face, fix them and ship the fix? |
| **Opportunity → Expansion** | notice adjacent needs it does not serve yet, and propose or launch them? |

Each loop gets a **Software Autonomy Level (SAL)** from L0 to L5, modelled on the levels used for self-driving cars:

| Level | Name | What the product can do | What users and admins experience |
|---|---|---|---|
| L0 | Manual | The changes that matter most need engineers writing and releasing code. | Most changes are tickets that wait for a release. |
| L1 | Configurable | People make the product's main kinds of change without bespoke engineering, and can undo them. | An admin makes the change in the product and can undo it. |
| L2 | Assisted | The product structures the request, diagnoses the issue or drafts the proposal, and drafts the change. People build and release. | You describe the need in the product; it asks questions and drafts the change. It explains problems and proposes fixes. An admin finishes. |
| L3 | Supervised | The product carries the loop end to end; a person approves each release. Every critical control passes. | The product builds and tests the change, releases it to a few users first and rolls it back if it is bad. It notices and diagnoses problems itself. A person only approves. |
| L4 | Policy-bounded | Low-risk changes ship without a person, under policy, with staged exposure, measurement and automatic rollback. | Routine changes and fixes ship on their own, within rules the company set, and undo themselves when they make things worse. |
| L5 | Self-directing | The product initiates, ships and measures change within policy, and improves its own checks and rules from the results. | The product decides what to improve next, does it, and gets better at deciding, within policy. |

**Kinds of change.** Levels are judged on what the people running the product actually need to change: an answer, a rule, a workflow, a price list. Each assessment lists those kinds and how far each has come, from *engineers only* through *self-serve*, *drafted*, *carried* and *pre-approved* to *self-chosen*. Level 1 needs every main kind to be self-serve. A product does not need to be a generic platform to evolve itself.

**Designed for, Built to, Proven at.** Three claims, never mixed. *Designed for* reads design documents, so a new product can be designed for Level 5 from day one. *Built to* reads what ships, with tests. *Proven at* reads operating records of real changes going through the loop. A product should run at the level it has proven, and raise autonomy as proof accumulates.

**Recursion.** A separate line says whether the loop improves its own checks, evaluation sets, policies and prompts from results: *fixed*, *by hand*, *governed*, *results-driven* or *self-improving*.

Beside each loop's level, EVOLVE reports how far **AI itself** carries that loop. Each loop is re-scored with its AI-performable stages (turning requests into specifications, building changes, diagnosing issues, proposing fixes, learning from experience, proposing new capabilities) read only on what AI does there. AI first drives a stage at L2, and never above the loop's own level; **AI L0** means AI drives no stage.

The headline is the lower of the first two loops, with Expansion reported beside it, for example **Built to SAL 2 · Proven: not evidenced · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L2 (AI L0) · Expansion L1 (AI L0)**. The first number says how far the product can evolve itself; the second, how much of that AI does. The scorer always names what blocks the next level, for the product and for its AI.

Behind the levels is the **EVOLVE profile**: six capabilities, each scored 0 to 4.

| | Capability | Asks |
|---|---|---|
| **E** | Elastic (`ARC`) | Does the architecture scale, survive failure and recover its data? |
| **V** | Velocity (`DEL`) | Can a change be built, verified and released quickly and safely? |
| **O** | Open (`MAL`) | Can the product be reshaped without a code release? |
| **L** | Learn (`LRN`) | Does it notice what is wrong, work out why, and measure whether changes helped? |
| **V** | Vet (`GOV`) | Is every change reviewed, policy-gated, audited and reversible, including the changes it makes to itself? |
| **E** | Expand (`EXP`) | Does it find and launch adjacent value? |

As a supporting view, EVOLVE reports **AI Readiness** for products with AI features: whether the AI features themselves are safe to run in production. It never changes SAL or the AI-driven levels.

| Dimension | Checks |
|---|---|
| Context | grounding in the product's own data (AIR-03); permission-preserving access (AIR-04) |
| Quality | evaluation sets (AIR-05); regression evaluation before release (AIR-06) |
| Governance | AI action traceability (AIR-07), plus the AI-specific readings of agent authority, scope limits and untrusted-input handling |
| Operations | provider resilience (AIR-01), cost controls (AIR-02), quality monitoring (AIR-08), plus the AI-provider part of failure isolation |

Each dimension is the floor of its mean; the headline is the weakest dimension, from **L0 Foundational gap** to **L4 Adaptive and operationally proven**. Three gates (permission-preserving access, regression evaluation, traceability) cap it at L2, labelled *not production-governed*. A descriptive **AI Capability Footprint** shows what the AI does (operate, build, diagnose and improve, expand) with a level per area but no headline; it never changes AI Readiness or SAL.

This is a **public beta**. It is designed to produce a falsifiable assessment, not a universal software leaderboard. `spec/evolve-v0.4-draft.md` explains the design and every decision behind it; `spec/ai-readiness-v0.5-draft.md` covers AI Readiness, and `spec/ai-driven-v0.6.md` the AI-driven levels.

## Field-test results

EVOLVE was run on 11 open-source products from their public source code; each name links to the project, and the field-test README lists the exact commit read. Full tables, evidence and per-product scorecards are in [`assessments/2026-09-field-test/`](assessments/2026-09-field-test/README.md).

> **Provisional.** These readings come from AI raters and have not been reviewed by the projects' maintainers. Eight control criteria on three products had a blind second and third rating, and n8n, LibreChat and Frappe had a blind second rating of every criterion under v0.7 (see `second-rating/`). In those full ratings 74% of scores matched exactly and 98% were within one point, every Level 3 control failed under both raters, and the overall level matched for n8n and differed for LibreChat and Frappe, each on one judgement about kinds of change. Those judgements are now settled rules (see `CHANGELOG.md`). Read them as findings to check, not rankings. Brought to EVOLVE v0.7 in November 2026 at the same commits.

| Product | Archetype | SAL (built) | Request → Release | Issue → Fix | Expansion | Main kinds self-serve | Recursion | AI Readiness |
|---|---|---:|---|---|---|---|---|---|
| [n8n](https://github.com/n8n-io/n8n) | configurable platform | **2** | L2 (AI L2) | L2 (AI L0) | L1 (AI L0) | 1 of 2 | By hand | L2 Deployed with material control gaps |
| [OpenClaw](https://github.com/openclaw/openclaw) | agent runtime | **2** | L2 (AI L2) | L2 (AI L0) | L1 (AI L0) | 2 of 3 | Fixed | L1 Experimental |
| [PostHog](https://github.com/PostHog/posthog) | focused application | **1** | L2 (AI L2) | L1 (AI L0) | L1 (AI L0) | 2 of 2 | By hand | L2 Deployed with material control gaps |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | agent runtime | **1** | L1 (AI L0) | L2 (AI L0) | L1 (AI L0) | 2 of 3 | By hand | L1 Experimental |
| [OpenHands](https://github.com/OpenHands/OpenHands) | agent runtime | **1** | L1 (AI L0) | L1 (AI L0) | L1 (AI L0) | 3 of 3 | Fixed | L1 Experimental |
| [Dify](https://github.com/langgenius/dify) | configurable platform | **1** | L1 (AI L0) | L1 (AI L0) | L1 (AI L0) | 3 of 3 | Fixed | L1 Experimental |
| [Discourse](https://github.com/discourse/discourse) | focused application | **1** | L1 (AI L0) | L1 (AI L0) | L0 (AI L0) | 3 of 3 | Fixed | no AI by default; L1 Experimental with opt-in |
| [Directus](https://github.com/directus/directus) | configurable platform | **1** | L1 (AI L0) | L1 (AI L0) | L1 (AI L0) | 2 of 3 | Fixed | L0 Foundational gap |
| [Frappe](https://github.com/frappe/frappe) | configurable platform | **1** | L1 (AI L0) | L1 (AI L0) | L1 (AI L0) | 4 of 4 | By hand | no AI features |
| [LibreChat](https://github.com/danny-avila/LibreChat) | focused application | **0** | L0 (AI L0) | L0 (AI L0) | L1 (AI L0) | 2 of 3 | By hand | L0 Foundational gap |
| [OpenCode](https://github.com/anomalyco/opencode) | agent runtime | **0** | L0 (AI L0) | L0 (AI L0) | L0 (AI L0) | 2 of 3 | Fixed | L1 Experimental |

Every product is built to the level shown and **not proven** in operation: a repository holds no operating records of a product's own loop. Each product folder has a plain-language `report.md`.

No product's AI drives both the request and the fix loop, so every AI-driven headline is 0.

What stands out:

- **AI builds changes, but does not yet fix the product.** In n8n, OpenClaw and PostHog, AI turns requests into plans and drafts the change (Request → Release, AI L2). In no product does AI diagnose issues well enough to drive the fix loop. Hermes and OpenClaw come closest: their AI learns from experience and proposes skill changes, but only explains errors when asked.
- **No product reaches SAL 3.** Definition rollback fails in all eleven: each rolls back some surfaces (workflows, skills) but not all (credentials, memory, configuration).
- **No product blocks a release on an AI regression.** Every product with AI fails the regression-evaluation gate, so none can reach AI Readiness L3 yet.
- **No product's checks improve from results yet.** The best Recursion reading is *by hand*: people update evaluation sets and rules after the fact. None records a wrong pass against the check that missed it.
- **The kinds of change people cannot undo are telling.** n8n credentials, the agent runtimes' memory and persona, Directus's data model and LibreChat's model configuration can be changed but not undone, so those products reach Level 1 only where AI drafting covers the gap, or not at all.
- **Expansion is the least developed loop.** No product clusters unmet demand into themes or proposes an adjacent capability on its own.

## What is included

- 67 anchored criteria in six capabilities, each with a 0–4 ladder, plus eight AI Readiness checks (AIR) and AI-qualified readings of 13 existing criteria. Every criterion also has a plain name and a plain question.
- Kinds of change with a reach from 0 to 5, Designed/Built/Proven readings, a Recursion line, confidence on every score, and a record of AI-assisted engineering that says whether it counts.
- An AI-driven level per loop: how far AI itself carries the loop, with what it needs for its next level.
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
- Twelve scope facts (nine for change, three for AI) that decide which criteria and controls apply, so a local tool is not failed on tenant isolation and a product that only changes through code is not failed on definition rollback.
- Evidence grades, evidence facets (implemented, tested, operated) and a depth cap: architecture and control criteria need tested evidence for a 3 or a 4. Operated evidence supports a Proven reading.
- Scoring of the default configuration, with shipped opt-in settings and higher alternate readings reported separately.
- Enforced archetype exclusions and an interpretation guide for agent runtimes and developer platforms.
- A deterministic Python scorer with tests, a plain-language report, a blueprint generator, a definition-of-done checklist and a quick scan.
- An evaluation set for the framework itself (`evals/`): test products with expected readings and traps, a runner that scores a rater against them, an agreement tool for comparing raters, and a log of disagreements and the rubric changes they led to.
- A guide and a working reference product for building a product that is evolvable from day one (`docs/born-evolvable.md`, `examples/born-evolvable/`).
- A reusable agent skill (`skills/evolvable-software/`), packaged as a plugin for Claude Code and Codex.
- A field test on 11 open-source systems in `assessments/2026-09-field-test/`, scored from public source code and not yet reviewed by their maintainers.

The framework itself contains no private repository evidence, client examples or employer-specific terminology.

## Install

**Claude Code** (plugin):

```bash
claude plugin marketplace add harsh51191/evolvable-software
claude plugin install evolvable-software@evolvable-software
```

Or from inside a session: `/plugin install evolvable-software --marketplace harsh51191/evolvable-software`. Update later with `claude plugin update evolvable-software@evolvable-software`.

**Codex** (plugin):

```bash
codex plugin marketplace add harsh51191/evolvable-software
codex plugin add evolvable-software@evolvable-software
```

**Gemini CLI** (extension):

```bash
gemini extensions install https://github.com/harsh51191/evolvable-software
```

**Cursor, Copilot, Claude Code, Codex and 40+ other agents** (via [skills.sh](https://skills.sh)):

```bash
npx skills add harsh51191/evolvable-software
```

**Any agent that reads skill folders** (copy the skill):

```bash
git clone https://github.com/harsh51191/evolvable-software.git
cp -r evolvable-software/skills/evolvable-software ~/.claude/skills/   # or ~/.codex/skills/
```

Restart or refresh the agent after installation. The skill can then be discovered for requests about self-evolution readiness, software autonomy levels, AI-driven change, governed product change, architecture readiness for autonomous change, or agent-safe action surfaces. It works best where it can read the repository being assessed, such as Claude Code, Codex or Cowork.

## What the plugin runs and sends

- **Reads** only the repositories and documents you point it at. It asks before cloning or opening any new remote source, and never changes the repository it assesses.
- **Writes** one assessment input file (JSON), at a path you choose outside the assessed repository, and the reports you ask for.
- **Runs** bundled Python scripts in the skill's `scripts/` folder (`init_scores.py`, `score.py`, `report.py`, `blueprint.py`, `quick_scan.py`), which use the standard library only. They make no network calls and install nothing.
- **Sends** nothing to any service. The plugin has no hooks, no MCP servers and no telemetry.

## Run the scorer directly

Requires Python 3.8 or later. It uses only the standard library.

Create an input template outside the repository you are assessing:

```bash
python3 skills/evolvable-software/scripts/init_scores.py \
  --product "Example Software" \
  --archetype focused-application \
  --source "repository @ immutable-tip" \
  --out ~/evolve/example-2026-10-01.json
```

Every scope fact starts empty and every criterion starts as `todo`. The scorer refuses the file until each of these holds:

- each fact is true or false, with evidence;
- each criterion is assessed, marked `not_evidenced` with a search scope, or excluded as the archetype or a scope fact allows.

Complete the file using the skill's `references/rubric.md` and `references/evidence-plan.md`, then run:

```bash
python3 skills/evolvable-software/scripts/score.py ~/evolve/example-2026-10-01.json
```

A report for business readers, and a plan from your goal:

```bash
python3 skills/evolvable-software/scripts/report.py ~/evolve/example-2026-10-01.json
python3 skills/evolvable-software/scripts/blueprint.py ~/evolve/example-2026-10-01.json --goal "More questions resolved without a person"
```

The older criterion-by-criterion plan is still available with `score.py --prescribe --target 3`.

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
- `ai`: an AI-qualified reading of the 13 criteria that AI Readiness reuses, scored only on AI-backed behaviour. Required when `ai_features` is true.
- `confidence`: high, medium or low, on every assessed criterion, AI reading and kind of change.

Top-level fields: `basis` (shipped or design), `change_kinds` (required), `proven`, `ai_delivery`.

## Important limits

- Repository evidence establishes that a mechanism exists in the inspected source. It does not prove usability, adoption, hosted-edition parity, production reliability or business impact. That is why Proven is reported separately, and is usually not evidenced from a repository alone.
- Every rating so far is by AI models. Rater agreement has been measured on a small sample: individual scores agree closely, but a single judgement about a kind of change can move a product's overall level; see `evals/` and `assessments/2026-09-field-test/second-rating/`. A human second rating is the most valuable contribution anyone can make.
- A Software Autonomy Level is a readiness reading, not a production certification.
- Cross-product comparison is defensible only when scope, archetype, scope facts, evidence depth and applicability decisions are comparable.
- Give maintainers an opportunity to correct factual evidence before publishing comparative scores.
- Do not include credentials, customer identifiers, confidential excerpts, internal URLs or proprietary evidence in shared scorecards.

## Repository structure

```text
.claude-plugin/marketplace.json       Claude Code marketplace entry
.codex-plugin/                        Codex plugin manifest
.agents/plugins/marketplace.json      Codex marketplace entry
skills/evolvable-software/            The skill, which is also the Claude plugin folder
  .claude-plugin/                     Claude plugin manifest and icon
  SKILL.md                            Agent instructions
  references/rubric.md                Criteria, anchored levels and the scoring model
  references/archetypes.md            Applicability and interpretation guidance
  references/evidence-plan.md         Evidence collection plan
  references/remediation.md           Level 3 and 4 improvement moves
  references/scorecard-template.md    Reporting structure
  scripts/init_scores.py              Input template generator
  references/plain-language.md        Plain names and questions for every criterion and level
  references/blueprint-template.md    The blueprint format
  references/quick-scan.md            Quick-scan questions
  scripts/score.py                    Validator, scorer, prescriber and checklist
  scripts/report.py                   Plain-language report
  scripts/blueprint.py                Blueprint skeleton
  scripts/quick_scan.py               Quick scan
docs/born-evolvable.md                Building a product evolvable from day one
examples/born-evolvable/              Answer Desk, a working reference product
evals/                                The framework's own evaluation set and agreement tool
spec/                                 Design and decisions for each version
tests/                                Tests (python3 -m unittest discover -s tests)
CONTRIBUTING.md                       How to contribute
assessments/                          Field-test results
metadata.yaml                         Package metadata
CHANGELOG.md                          Version history
```

## Name and version

EVOLVE v0.7.0, public beta 7, November 2026. EVOLVE was previously the Malleability and Self-Evolution Readiness (MSR) framework; see `CHANGELOG.md` for what changed and why. "EVOLVE" and "Software Autonomy Level" are working names until a trademark and prior-use search is complete.

## License

MIT. See `LICENSE`.
