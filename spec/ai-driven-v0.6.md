# EVOLVE v0.6: AI-driven loop levels

Status: implemented and released in v0.6.0 with the repository owner's approval. Field-test results are provisional and single-rater.

## 1. Why

EVOLVE asks how ready a product is to evolve itself safely: to take requests through to release, fix the issues users face, and find adjacent opportunities, increasingly with AI doing the work. The Software Autonomy Level (SAL) answers how far the product can carry each loop by any means: people configuring it, rules, or AI. It does not say how much of that AI does.

v0.5 recorded AI's part in two places that were off the headline: the AI-qualified readings of 13 criteria, and the descriptive AI Capability Footprint. v0.6 brings AI's part onto the headline, beside each loop.

## 2. The AI-driven level

For each loop, the scorer re-runs the loop rules with the loop's AI-performable stage criteria replaced by their AI-qualified readings:

| Loop | Stage criteria read on AI only |
|---|---|
| Request → Release | DEL-01 request into specification; DEL-04 implementation lane |
| Issue → Fix | LRN-05 diagnosis; LRN-06 improvement proposals; LRN-07 learning from experience; LRN-08 validation of AI-made changes |
| Opportunity → Expansion | EXP-05 adjacent-capability proposals |

Everything else is unchanged: the release spine, the architecture foundation, the governance ceiling and the critical controls. An AI-driven loop still needs them to be safe.

Rules:

1. **Never above the loop.** The AI-driven level is at most the loop's own level.
2. **AI starts at L2.** L1 is people configuring the product without engineering; no stage is performed by the product there. Below L2 the AI-driven level is 0, named "AI drives no stage".
3. **Missing AI is zero.** A stage with no AI-qualified reading, or a `not_evidenced` one, counts as 0. A stage whose parent criterion does not apply stays excluded.
4. **Headline.** AI-driven is the lower of the Request → Release and Issue → Fix AI levels, matching SAL.
5. **Variants.** The opt-in and alternate readings are computed the same way from the AI readings' `available_score` and `alt_score`.
6. **Blockers.** For each loop the scorer lists the conditions with an AI stage criterion that the AI-only run must meet for its next level.

The headline reads, for example: **SAL 2 · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0)**.

## 3. What did not change

- SAL, loop levels, critical controls and the EVOLVE profile are computed exactly as before.
- No new criteria. The AI-qualified readings that v0.5 already required supply all the evidence.
- AI Readiness stays, as a supporting view: whether the AI features themselves are safe to run. It moves below the profile in the scorecard and never changes SAL or the AI-driven levels.
- The AI Capability Footprint stays as a descriptive view, including the Operate area (assistants and agent tool surfaces), which is not a loop stage.

## 4. Tests that must hold

- A product with no AI features is AI-driven 0 in every loop, whatever its SAL.
- The AI-driven level never exceeds the loop level, however high the AI readings.
- Rule-based diagnosis does not count: a fix loop at L3 with an AI diagnosis reading of 0 is AI-driven 0, and the blocker names LRN-05.
- The headline is the lower of the request and fix AI levels.
- A `not_evidenced` AI reading counts as 0.
- An AI `alt_score` moves only the alternate reading.
- SAL is identical with and without AI evidence.

## 5. Field-test result

AI drives Request → Release at L2 in n8n, OpenClaw and PostHog. It drives Issue → Fix and Opportunity → Expansion nowhere, so every AI-driven headline is 0. In Hermes and OpenClaw a single reading holds the fix loop: AI learns from experience and proposes skill changes, but explains errors only when asked (LRN-05 AI 1).
