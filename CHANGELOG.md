# Changelog

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
