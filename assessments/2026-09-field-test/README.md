# Field test: 11 open-source systems under EVOLVE v0.5

This folder scores 11 open-source products with EVOLVE from this repository: SAL under the v0.4 rules, and AI Readiness under v0.5. The same systems were scored under MSR v0.2 and v0.3 in September 2026; this pass migrates those inputs and adds the 17 new criteria, scope facts, evidence facets and inventories.

> **Provisional.** These results come from one rater reading public source code. They are not maintainer-reviewed, and the 17 new criteria have not had a second independent assessment. Where repository evidence is missing, a criterion scores 0, which can understate products whose capabilities live elsewhere. Before quoting or comparing these results, give each project's maintainers a chance to correct the evidence.

## Results (default configuration)

Each loop shows its level and how many of the next level's applicable conditions it already meets. Conditions switched off by a scope fact count in neither number.

| System | Archetype | SAL | Request → Release | Issue → Fix | Opportunity → Expansion | With every alternate reading |
|---|---|---:|---|---|---|---:|
| n8n | configurable platform | **2** | L2 (12/19) | L2 (12/21) | L1 (3/5) | 2 |
| OpenClaw | agent runtime | **2** | L2 (12/19) | L2 (13/21) | L1 (3/5) | 2 |
| Hermes Agent | agent runtime | **1** | L1 (3/4) | L2 (13/22) | L1 (3/5) | 2 |
| PostHog | focused application | **1** | L2 (11/20) | L1 (4/5) | L1 (3/5) | 2 |
| Dify | configurable platform | **1** | L1 (2/4) | L1 (2/5) | L1 (2/5) | 1 |
| Directus | configurable platform | **1** | L1 (1/4) | L1 (1/5) | L1 (2/5) | 1 |
| Frappe | configurable platform | **1** | L1 (2/4) | L1 (4/5) | L1 (3/5) | 1 |
| OpenHands (canvas, SDK, automation) | agent runtime | **1** | L1 (1/4) | L1 (2/5) | L1 (2/5) | 1 |
| Discourse | focused application | **1** | L1 (2/4) | L1 (4/5) | L0 (1/2) | 1 |
| LibreChat | focused application | **0** | L0 (1/2) | L0 (2/3) | L0 (1/2) | 1 |
| OpenCode | agent runtime | **0** | L0 (1/2) | L0 (1/3) | L0 (1/2) | 0 |

Opt-in settings change no headline level. `comparison.md` also covers:

- the parts that hold each loop back;
- the sensitivity of each headline;
- the critical controls;
- the six-capability profile with ranges;
- the scope facts and the v0.3 numbers.

Each system folder has `scope.md`, `evidence.md` (every score with file paths), `assessment.json` (the scorer input), `result.json` and `scorecard.md`.

## AI Readiness (provisional, single rater)

> **Not independently reviewed.** AI Readiness was added in v0.5 and scored by one rater from public source code. Treat every level below as provisional until a second rater and the maintainers have checked the evidence.

| System | AI Readiness | Context | Quality | Governance | Operations | Gates failed |
|---|---|---:|---:|---:|---:|---|
| n8n | **L2** Deployed with material control gaps | 3 | 2 | 2 | 2 | evals, traces |
| OpenHands | **L2** Deployed with material control gaps | 3 | 2 | 2 | 2 | evals |
| PostHog | **L2** Deployed with material control gaps | 3 | 2 | 2 | 2 | evals |
| Dify | **L1** Experimental | 2 | 1 | 2 | 2 | access, evals |
| Discourse | no AI by default; **L1** Experimental with opt-in | 3 | 1 | 3 | 2 | evals |
| Hermes Agent | **L1** Experimental | 3 | 1 | 2 | 2 | evals |
| OpenClaw | **L1** Experimental | 3 | 1 | 2 | 2 | evals |
| OpenCode | **L1** Experimental | 3 | 1 | 2 | 1 | evals |
| Directus | **L0** Foundational gap | 3 | 0 | 1 | 1 | evals, traces |
| LibreChat | **L0** Foundational gap | 2 | 0 | 2 | 2 | access, evals, traces |
| Frappe | no AI features | – | – | – | – | – |

Discourse ships its AI plugin switched off, so its default reading is "no AI features" and the row shows the opt-in reading. `comparison.md` adds the alternate readings and the descriptive AI Capability Footprint.

What the results say:

- **Quality is the weakest dimension almost everywhere.** No product blocks a release on an AI regression: the best (PostHog, n8n, OpenHands) run evaluations on labelled or path-filtered pull requests or on releases, without a blocking threshold. Every product with AI therefore fails the regression gate and is capped at L2.
- **Context is the strongest.** Most products ground the model in live product data and run tools with the user's permissions. Dify and LibreChat retrieve with the app's or agent's knowledge rather than each end user's permissions, so they fail the access gate.
- **Traceability splits the field.** Discourse, Dify, PostHog and the agent runtimes log every model call and tool action against a user. Directus, n8n and LibreChat trace only optionally or without the model and prompt.
- **What AI does is narrower than how widely it is deployed.** The footprint shows AI operating the product (assistants, MCP servers) in nearly every case, but diagnosing or improving the product itself only in Hermes and OpenClaw, and proposing adjacent capabilities nowhere above 1.

## What the SAL results say

- **No system reached L3 in this repository-based, single-rater assessment.** Each fails at least one critical control:
  - **Definition rollback fails in all eleven.** Rollback covers some surfaces but not all: workflows but not credentials, or skills but not memory and configuration.
  - **Tested backup and restore passes in three.** Discourse, Hermes and OpenClaw back up and restore every applicable surface, with tests. Frappe's restore is tested, except for the site secrets.
- **Request intake decides Request → Release L2.** Only three systems structure a request before acting on it:
  - n8n's planner asks clarifying questions and produces a plan for approval.
  - OpenClaw's `/learn` stages a pending proposal.
  - PostHog AI has a plan mode.

  For Hermes this single criterion is the difference between SAL 1 and SAL 2.
- **Issue → Fix is where the agent runtimes lead.** Hermes and OpenClaw turn observed failures and corrections into skill changes by default. n8n gets there through failure rates per workflow and AI-assisted debugging.
- **Nobody senses or proposes adjacent value.** No system clusters unmet demand into themes (EXP-04 is at most 2, from Discourse's search logs), and none proposes an adjacent capability on its own (EXP-05 is at most 1). Expansion is the least developed loop in the sample.
- **Architecture caps three systems.** Directus, Dify and OpenHands have no load or capacity evidence (ARC-06 0), which holds their architecture foundation at L1.
- **Headlines rest on a few criteria.** The sensitivity table shows which ones:
  - User-issue detection (LRN-03) and definition rollback (GOV-05) hold up most of the L1 and L2 readings.
  - For the two SAL 2 systems, the headline rests on six or seven criteria, mostly in delivery and learning.

  These are the scores to check first in a second pass.

## What changed from v0.3

`tools/migrate_v04.py` records every change, each with its evidence:

1. **Renamed criteria.** Every criterion now uses its EVOLVE id (`spec/evolve-v0.4-draft.md`, section 12).
2. **Flipped alternates.** 49 downward alternates were flipped under rule 11: the lower reading is now the score and the original score is the higher reading. Together with the regrouping, this lowers several scores relative to v0.3. In the regrouping, K1 and K2 joined Open and the adjacent-domain criteria moved to Expand. Open moved most: Frappe's Malleability index was 2.8, and its Open score is 2.3.
3. **Scope facts.** All nine were declared with evidence. Criteria they switch off, such as tenant isolation for single-user agents and capacity for local tools, are now `not_applicable`, with the earlier score kept as `if_applicable`.
4. **New criteria.** All 17 were scored for each system, with facets and inventories where the rules need them.
5. **Removed alternates.** Five definition-rollback and four failure-isolation higher readings of 3 were removed. The inventory rule cannot support them, because some surfaces sit below 3.
6. **Re-scores under the new definitions:**
   - Hermes and OpenClaw definition rollback, 3 to 2: under the inventory rule, configuration and memory lack the rollback that skills have.
   - OpenCode and OpenHands implementation lane, 2 to 1: the self rule and rule 12 exclude AI that works on users' repositories or is the team's own tooling.
   - OpenHands impact measurement, 0 to 1: variant tags in automations.
7. **OpenHands scope.** The OpenHands Automation Service (`OpenHands/automation`) was added after an inter-rater review found it missing.

The v0.3 headline numbers are kept in `tools/v03_comparison.json`, and the v0.2 numbers in `tools/v02_comparison.json`.

## What changed in v0.5

`tools/migrate_v05.py` adds the three AI scope facts, the eight AIR checks and an AI-qualified reading of 13 existing criteria for every product with AI features, each with its evidence. It does not change any SAL input, so every SAL result above is unchanged.

## How the scores were produced

- **Evidence.** Shallow clones of each project's default branch, read on 30 September 2026 (1 October for the automation repository). Every score cites code or in-repository documentation at the named commit. No running instances were used, so no criterion has the operated facet.
- **Scorer.** `scripts/score.py` from this repository computes every number. `tools/build.py` regenerates all outputs.
- **Ambiguity.** Where the next level up was also defensible, it is recorded as `alt_score` with an `alt_note`, and the "with every alternate reading" column shows its effect.
- **Defaults.** Where a shipped opt-in setting changes a level, it is recorded as `available_score`.
- **Rater.** Claude, as a single rater.
  - A second rater independently rescored the v0.3 Learn and Vet criteria. Its boundary disagreements are applied as rubric clarifications, but that dataset is not yet in this repository, so its agreement figures are not quoted here.
  - The 17 new criteria need their own second pass, and so do the eight AIR checks and the 13 AI-qualified readings.

## Regenerate

```bash
cd assessments/2026-09-field-test
python3 tools/build.py
git diff --exit-code .   # no differences means the committed outputs match the inputs
```

CI runs the same check on every push and pull request (`.github/workflows/ci.yml`).
