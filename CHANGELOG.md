# Changelog

## Public Beta 4 (EVOLVE v0.4.0), 2026-10-01

The framework is renamed from Malleability and Self-Evolution Readiness (MSR) to **EVOLVE** and re-centred on one question: how ready is a product to evolve itself safely? `spec/evolve-v0.4-draft.md` records the design, the two review rounds and every decision.

### What it reports

- **Software Autonomy Levels (L0 to L5)** for three loops: Request → Release, Issue → Fix and Opportunity → Expansion. The headline is the lower of the first two. These replace v0.3's four indexes and its single closed-loop flag.
- **Each loop's level is the lowest of four parts:**
  - the loop's own stages;
  - a shared release spine (build, verify, stage, release, observe, roll back);
  - an architecture foundation;
  - a governance ceiling.

  The scorer names every condition that blocks the next level.
- **Seven critical controls**, each an L3 condition: definition rollback, release rollback, safe migrations, tested backup and restore, tenant isolation, security, and bounded self-change. A failed applicable control caps every loop at L2.
- **The six-capability EVOLVE profile** replaces the indexes and profiles: Elastic (ARC), Velocity (DEL), Open (MAL), Learn (LRN), Vet (GOV), Expand (EXP). Each capability score is the mean of its area means.

### What moved, and why

- **Architecture is back in the headline.** v0.3 left performance (G) and agent readiness (K) only in profiles, an undisclosed loss. G is now the core of Elastic, and every applicable architecture criterion constrains every loop. K1 and K2 joined Open; K3 joined Vet.
- **The implementation lane (M3) moved to Velocity** as DEL-04, and now credits code changes made through the product's own pipeline, not only definition changes.
- **Adjacent-domain expansion (O) moved to Expand**, joined by criteria for sensing unmet demand, proposing adjacent capabilities and launching them to a cohort first.
- **Criterion ids are descriptive** (`ARC-01` and so on). The mapping from every v0.3 id is in the specification, section 12.

### New criteria (17)

- Architecture:
  - ARC-02 safe migrations;
  - ARC-03 horizontal scale;
  - ARC-04 reliable asynchronous work;
  - ARC-07 service objectives;
  - ARC-08 failure isolation;
  - ARC-09 backup, restore and recovery.
- Delivery:
  - DEL-01 request intake;
  - DEL-09 staged exposure;
  - DEL-10 kill switch;
  - DEL-11 release rollback.
- Learning:
  - LRN-03 user-issue detection;
  - LRN-05 automated diagnosis.
- Governance:
  - GOV-10 bounded self-change;
  - GOV-11 learning-input integrity.
- Expansion:
  - EXP-04 unmet-demand sensing;
  - EXP-05 opportunity proposals;
  - EXP-06 cohort launch with keep-or-kill.

### How it is applied

- **Scope facts.** Nine facts, declared with evidence, decide which criteria and controls apply: persistent data, schema changes, multi-tenant, hosted service, machine actions, agent mutations, evolution auto-apply, definition change path, and code release path.
- **Rollback follows the change paths.** Definition rollback is required where behaviour changes through definitions, release rollback where the evolution system ships code, both where both exist.
- **Backup is tested recovery.** ARC-09 level 3 needs tested restore of every surface. Stated recovery objectives are level 4.
- **Evidence facets and a depth cap.** Implemented, tested and operated are recorded separately. Architecture and control criteria need tested evidence for a 3 and operated evidence for a 4.
- **Coverage inventories.** Failure isolation, backup and definition rollback list their surfaces. No reading of 3 or more, including alternate and opt-in readings, can exceed the weakest surface.
- **Alternates are upward only.** `alt_score` must be `score + 1`, which enforces the rubric's "take the lower reading" rule. The 49 downward alternates in the field test were flipped.
- **Repository tooling counts only as a first-party evolution system** for intake, implementation, release, detection, diagnosis, learning and expansion criteria.
- **Round 2 boundary clarifications.** A second rater rescored the v0.3 Learn and Vet criteria; that dataset is not yet in this repository. The four boundaries the raters disputed are now explicit:
  - definition rollback covers all default surfaces;
  - impact measurement is post-apply only;
  - the policy criterion covers self-changes, while per-action permissions belong to agent-safe actions;
  - the implementation lane credits changes to the product itself.

### Field test

All 11 systems were migrated and scored on the new criteria. The OpenHands Automation Service was added to OpenHands' scope.

- Results are provisional: one rater, repository evidence only, not maintainer-reviewed.
- n8n and OpenClaw reach SAL 2. No system reached L3 in this assessment.
- Definition rollback fails in all eleven.

### Scorer and tooling

- The scorer reads capabilities and areas from rubric headings, and everything else from the `evolve-model` block, including the level conditions as data.
- It validates:
  - scope facts and fact-driven applicability;
  - facets and inventories;
  - upward-only alternates.
- It reports SAL for the default, opt-in and alternate readings.
- It reports progress toward the next level for each loop, counting only conditions that apply, and the criteria whose one-level change would move the headline.
- Inventories for failure isolation and backup must list every named surface, with "n/a" where one does not apply.
- The prescriber lists the next-level blockers before the criterion plan.
- 52 tests.

## Public Beta 3 (v0.3.0), 2026-09-30

A field test on 11 open-source systems found that the criteria were usable, but the headline numbers depended too much on who did the scoring. Two independent runs of v0.2 ranked the same systems with a rank correlation of about 0.4. This release changes what the framework measures, and how the scorer computes it, and is designed to reduce that rater dependence. Whether it does is not yet shown: the v0.3 field test is a single rater. Showing it needs a second independent v0.3 pass that reports rank correlation and criterion-level agreement.

### What the framework measures

- **Self-evolution is no longer a single average.** The old Self-Evolution index blended change control with learning, so a product could score well without learning anything, or badly despite learning a lot. There are now four non-overlapping indexes: Malleability (A, B, C, D, I, N, O), Governance (E, F), Learning (J, M, P) and Factory (H, L). The seven profiles are unchanged in meaning.
- **New dimension P, Learn from experience.** P1 asks whether the product turns its own operating experience into candidate changes without being asked. P2 asks whether learned changes are evaluated against the current baseline before they take effect.
- **Removed M2 (process-change proposals).** It scored 0 in every system tested and measured a business model, not software.
- **J2 is now "structured learning signals"**: feedback, ratings, corrections, evaluation results and per-definition usage, linked to what they concern.
- **Separated bundled properties.** A2 no longer needs a privacy tag (privacy classification moved to E3). A3 accepts relations or lifecycle states at level 3. O1 no longer prescribes specific kernel primitives. K1 accepts MCP or an equivalent typed tool surface. H1's level 0 and level 1 anchors are now distinct.
- **Product-specific wording removed** from the rubric and remediation catalogue ("the existing endpoint lane", GraphQL and search-engine terms, "members", "moderation reports", named vendors).

### How it is applied

- **Default configuration is scored.** Shipped opt-in settings are recorded as `available_score` and reported as a separate variant.
- **Scope includes first-party companions**, and delegated capabilities are assessed where they live.
- **Self, not others.** Learning criteria credit improvements to the product's own behaviour, not improvements it makes to other software.
- **The ladder measures how governed and supported a change path is**, not whether it has a graphical UI. Terms are defined: operator, tenant, customisation surface, AI-authorable.
- **Archetype exclusions are enforced** by the scorer, and `archetypes.md` adds an interpretation guide for agent runtimes and developer platforms, plus a checklist of where self-modification lives.
- **Closed-loop check** now names seven stages, with a minimum level for each. The measure stage requires level 3 (M4 or P2), which v0.2's "at least 2" contradicted.
- **Neutral band names** (code-only, mechanism, productised, generative and policy-gated), applied to every index. Thresholds sit at .5.

### Scorer and tooling

- The scoring model (indexes, profiles, floors, bands, exclusions, caps) is read from `rubric.md`; the scorer refuses a rubric whose dimensions are missing from the model.
- Validation rejects string booleans, non-object entries, template placeholders and exclusions the archetype does not allow.
- `alt_score` must be an adjacent level (score ± 1) with an `alt_note`, and is allowed only on assessed criteria; `available_score` only on assessed and `if_applicable` only on not_applicable criteria.
- Ranges move every criterion independently to its lower and higher defensible level, so opposite-direction alternates cannot cancel out.
- Index membership must be non-overlapping and every dimension must sit in exactly one profile; the scorer refuses a rubric that breaks either rule.
- The scorer reports an opt-in variant, an assessed-only index and the grade mix.
- Values are rounded half up, once, for display only.
- Markdown tables escape pipes and newlines.
- The command line uses argparse.
- The prescriber:
  - separates hard (`Requires:`) from soft (`Helps:`) prerequisites;
  - fails on dependency cycles;
  - lists `not_evidenced` criteria as "investigate first" instead of scheduling them as build work.
- `init_scores.py` writes `todo` entries and refuses to overwrite an existing file.
- Added `tests/test_score.py` (27 tests) and CI that runs them and regenerates the field test, failing if any committed output differs.
- Added `assessments/2026-09-field-test/` with inputs (`assessment.json`) and results for 11 systems under v0.3.

## Public Beta 2, 2026-09-29

Archetype-aware assessment, distinction between absence, uncertainty and non-applicability, profile reporting, post-change impact measurement, and a minimum closed-loop candidate signal.
