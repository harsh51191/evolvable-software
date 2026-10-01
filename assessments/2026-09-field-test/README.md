# Field test: 11 open-source systems, September 2026

This folder scores 11 open-source products with rubric v0.3 in this repository. The first version of this study ran v0.2 unchanged. It found that the framework's criteria were usable, but its headline numbers depended too much on who did the scoring. v0.3 is designed to address that, and these are the results under it. They come from one rater, so they show whether v0.3's ordering is more plausible (face validity), not whether two raters now agree; that needs a second independent pass.

> **Not maintainer-reviewed.** These are one rater's scores of real products, read from public source code. Before quoting or comparing them publicly, give each project's maintainers a chance to correct the evidence, as the framework's own guidelines require.

## Results (default configuration)

| System | Archetype | Malleability | Governance | Learning | Learning range | Factory | Closed loop (default / opt-in) |
|---|---|---:|---:|---:|---|---:|---|
| Hermes Agent | agent runtime | 2.4 | 2.3 | **2.5** | 2.3–3.1 | 2.0 | no / **yes** |
| OpenClaw | agent runtime | 2.4 | 2.4 | 2.4 | 2.2–2.9 | **2.7** | no / no |
| PostHog | focused application | 2.6 | 2.3 | 2.0 | 1.8–2.8 | **2.7** | no / no |
| n8n | configurable platform | 2.4 | **2.8** | 1.8 | 1.8–2.5 | 2.5 | no / no |
| Dify | configurable platform | 2.5 | 1.9 | 1.6 | 1.5–1.8 | 2.3 | no / no |
| Discourse | focused application | 2.1 | 1.8 | 1.5 | 1.4–1.6 | 1.7 | no / no |
| Frappe | configurable platform | **2.8** | 1.9 | 1.3 | 1.2–1.6 | 1.7 | no / no |
| Directus | configurable platform | 2.6 | 1.8 | 1.1 | 0.9–1.2 | 2.0 | no / no |
| LibreChat | focused application | 1.8 | 1.9 | 1.0 | 0.9–1.0 | 2.0 | no / no |
| OpenHands (canvas + SDK) | agent runtime | 2.1 | 1.6 | 1.0 | 1.0–1.0 | 2.2 | no / no |
| OpenCode | agent runtime | 2.3 | 1.5 | 0.9 | 0.9–1.0 | 2.2 | no / no |

Ranges, opt-in effects, failing closed-loop stages, profiles and the v0.2 numbers are in `comparison.md`. Each system folder has `scope.md`, `evidence.md` (every score with file paths), `assessment.json` (the scorer input), `result.json` and `scorecard.md`.

## What the results say

- **The ordering is closer to what the products are designed to do.** This is face validity from one rater, not evidence of agreement between raters.
  - The no-code platforms lead Malleability, with Frappe at 2.8. Under v0.2 they came 3rd and 5th.
  - Hermes, OpenClaw and PostHog lead Learning, but their ranges overlap (2.3–3.1, 2.2–2.9, 1.8–2.8), so this study cannot rank them against each other. Under v0.2 another rater put the two agents near the bottom.
  - n8n leads Governance.
- **Almost no system closes the loop.** Only Hermes passes every closed-loop stage, and only with its opt-in approval gates and optimiser.
- **"Measure" is the common gap.** Nine of the eleven systems fail it by default: nobody evaluates a learned or proposed change against a baseline and keeps or reverts it on the result.
- **Defaults matter.**
  - Hermes and OpenClaw apply self-modifications automatically out of the box.
  - Discourse's most governed features are off-by-default betas.
  - v0.3 reports both states instead of blending them.

## How the scores were produced

- **Evidence.** Shallow clones of each project's default branch on 30 September 2026. Every score cites code or in-repository documentation at the named commit. No running instances were used.
- **Scorer.** `scripts/score.py` from this repository computes every number. `tools/build.py` regenerates all outputs.
- **Ambiguity.** Where an adjacent level was also defensible, it is recorded as `alt_score` with an `alt_note`. The scorer moves each criterion independently to its lower and higher reading, so the reported range is the full span those readings allow.
- **Defaults.** Where a shipped opt-in setting changes a level, it is recorded as `available_score`.
- **Rater.** Claude, as a single rater. A second independent pass on the F, J, M and P dimensions would strengthen these results; see `references/evidence-plan.md`.

## How the scores moved from v0.2 to v0.3

`tools/migrate_v03.py` records every change made to the v0.2 inputs, each with its evidence:

- M2 was removed.
- P1 and P2 were added.
- J2 was rescored under its new definition.
- A2 and A3 were rescored after being separated from privacy and lifecycle states.
- Opt-in settings were split into `available_score`.
- PostHog's Learning criteria were rescored under the self rule.
- OpenHands was rescored with its agent SDK in scope.

All other scores are unchanged from the v0.2 pass. The v0.2 outputs are kept in `tools/v02_comparison.json`.

## Regenerate

```bash
cd assessments/2026-09-field-test
python3 tools/build.py
git diff --exit-code .   # no differences means the committed outputs match the inputs
```

CI runs the same check on every push and pull request (`.github/workflows/ci.yml`).
