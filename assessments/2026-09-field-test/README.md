# Field test: 11 open-source systems under EVOLVE v0.4

This folder scores 11 open-source products with EVOLVE v0.4 from this repository. The same systems were scored under MSR v0.2 and v0.3 in September 2026; this pass migrates those inputs and adds the 17 new criteria, scope facts, evidence facets and inventories. The scores come from one rater, so they show whether EVOLVE's readings are plausible (face validity), not whether two raters agree.

> **Not maintainer-reviewed.** These are one rater's scores of real products, read from public source code. Before quoting or comparing them publicly, give each project's maintainers a chance to correct the evidence, as the framework's own guidelines require.

## Results (default configuration)

| System | Archetype | SAL | Request → Release | Issue → Fix | Opportunity → Expansion | With every alternate reading |
|---|---|---:|---:|---:|---:|---:|
| n8n | configurable platform | **2** | L2 | L2 | L1 | 2 |
| OpenClaw | agent runtime | **2** | L2 | L2 | L1 | 2 |
| Hermes Agent | agent runtime | **1** | L1 | L2 | L1 | 2 |
| PostHog | focused application | **1** | L2 | L1 | L1 | 2 |
| Dify | configurable platform | **1** | L1 | L1 | L1 | 1 |
| Frappe | configurable platform | **1** | L1 | L1 | L1 | 1 |
| OpenHands (canvas, SDK, automation) | agent runtime | **1** | L1 | L1 | L1 | 1 |
| Discourse | focused application | **1** | L1 | L1 | L0 | 1 |
| Directus | configurable platform | **0** | L1 | L0 | L1 | 1 |
| LibreChat | focused application | **0** | L0 | L0 | L0 | 1 |
| OpenCode | agent runtime | **0** | L0 | L0 | L0 | 0 |

Opt-in settings change no headline level. `comparison.md` has the parts that hold each loop back, the critical controls, the six-capability profile with ranges, the scope facts and the v0.3 numbers. Each system folder has `scope.md`, `evidence.md` (every score with file paths), `assessment.json` (the scorer input), `result.json` and `scorecard.md`.

## What the results say

- **No system can reach L3 today.** Every system fails at least one critical control, and two controls fail in all eleven:
  - **Definition rollback.** Rollback covers some surfaces but not all of them: workflows but not credentials, or skills but not memory and configuration.
  - **Tested backup and restore.** Frappe, Discourse, Hermes and OpenClaw back up and restore with tests, but none states recovery objectives, so each sits at 2 with 3 as its higher reading. The rest have no tested restore at all.
- **Request intake decides Request → Release L2.** Only three systems structure a request before acting on it:
  - n8n's planner asks clarifying questions and produces a plan for approval.
  - OpenClaw's `/learn` stages a pending proposal.
  - PostHog AI has a plan mode.

  Everywhere else, requests are free text or live outside the product.
- **Issue → Fix is where the agent runtimes lead.** Hermes and OpenClaw turn observed failures and corrections into skill changes by default. n8n gets there through failure rates per workflow and AI-assisted debugging.
- **Nobody senses or proposes adjacent value.** No system clusters unmet demand into themes (EXP-04 is at most 2, from Discourse's search logs), and none proposes an adjacent capability on its own (EXP-05 is at most 1). Expansion is the least developed loop in the sample.
- **Architecture caps three systems.** Directus, Dify and OpenHands have no load or capacity evidence (ARC-06 0), which holds their architecture foundation at L1. OpenHands and LibreChat also have no backup (ARC-09 0).
- **Hermes is no longer the stand-out.** Under v0.3 it was the only closed-loop candidate with opt-in settings. Under EVOLVE its Issue → Fix loop reaches L2, but requests have no specification step, its backups lack recovery objectives and its background changes have no declared scope. Its opt-in approval gates change none of those.

## What changed from v0.3

`tools/migrate_v04.py` records every change, each with its evidence:

1. **Renamed criteria.** Every criterion now uses its EVOLVE id (`spec/evolve-v0.4-draft.md`, section 12).
2. **Flipped alternates.** 49 downward alternates were flipped under rule 11: the lower reading is now the score and the original score is the higher reading. Together with the regrouping (K1 and K2 joined Open; adjacent-domain criteria moved to Expand), this lowers several scores relative to v0.3. Open moved most: Frappe's Malleability index was 2.8, and its Open score is 2.3.
3. **Scope facts.** All seven were declared with evidence. Criteria they switch off, such as tenant isolation for single-user agents and capacity for local tools, are now `not_applicable`, with the earlier score kept as `if_applicable`.
4. **New criteria.** All 17 were scored for each system, with facets and inventories where the rules need them.
5. **Re-scores under the new definitions:**
   - Hermes and OpenClaw definition rollback, 3 to 2: under the inventory rule, configuration and memory lack the rollback that skills have.
   - OpenCode and OpenHands implementation lane, 2 to 1: the self rule and rule 12 exclude AI that works on users' repositories or is the team's own tooling.
   - OpenHands impact measurement, 0 to 1: variant tags in automations.
6. **OpenHands scope.** The OpenHands Automation Service (`OpenHands/automation`) was added after the inter-rater study found it missing.

The v0.3 headline numbers are kept in `tools/v03_comparison.json`, and the v0.2 numbers in `tools/v02_comparison.json`.

## How the scores were produced

- **Evidence.** Shallow clones of each project's default branch, read on 30 September 2026 (1 October for the automation repository). Every score cites code or in-repository documentation at the named commit. No running instances were used, so no criterion has the operated facet.
- **Scorer.** `scripts/score.py` from this repository computes every number. `tools/build.py` regenerates all outputs.
- **Ambiguity.** Where the next level up was also defensible, it is recorded as `alt_score` with an `alt_note`, and the "with every alternate reading" column shows its effect.
- **Defaults.** Where a shipped opt-in setting changes a level, it is recorded as `available_score`.
- **Rater.** Claude, as a single rater. The Round 2 inter-rater study (118 of 132 criteria in exact agreement on the v0.3 Learn and Vet criteria) is not yet in this repository. Its boundary findings are applied as rubric clarifications. The new criteria need their own second pass.

## Regenerate

```bash
cd assessments/2026-09-field-test
python3 tools/build.py
git diff --exit-code .   # no differences means the committed outputs match the inputs
```

CI runs the same check on every push and pull request (`.github/workflows/ci.yml`).
