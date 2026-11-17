# Blind second rating of the critical controls

**Date:** 14 October 2026. **Framework:** EVOLVE v0.6.1.

## What was done

A second rater scored three products on the eight criteria behind the seven critical controls, and set the nine scope facts that decide which of them apply. The products were n8n, OpenClaw and Dify, read at the same commits as the field test. The criteria were GOV-05, DEL-11, ARC-02, ARC-09, ARC-05, GOV-04, GOV-10 and LRN-08.

The rater was blind. It was a separate AI agent (Claude), given only the skill and its references plus the three source trees. It had no access to the first rating, the evidence files or the results. Its raw ratings, with file and line evidence, are in `n8n.json`, `openclaw.json` and `dify.json`.

## Agreement

| | Count |
|---|---|
| Criterion ratings both raters assessed | 18 |
| Exact agreement | 13 (72%) |
| Within one level | 17 (94%) |
| Both raters marked not applicable | 4 |
| Applicability differed because a scope fact differed | 2 |
| Scope facts that differed | 3 of 27 |

## Where the raters differed

| Product | Criterion | First | Second | Why |
|---|---|---:|---:|---|
| n8n | GOV-04 security as infrastructure | 3 | 2 | The second rater found that PR security scans cover only workflow-file changes. |
| n8n | LRN-08 validation of learned changes | 2 | 1 | The raters read "learned changes" differently for a product with no learning loop. |
| OpenClaw | ARC-09 backup and restore | 3 | 2 | Scheduled-work surface: the second rater found no check of each job's current permissions and credentials before it runs. |
| OpenClaw | LRN-08 validation of learned changes | 2 | 0 | Skill changes auto-apply by default with no check first; scanning comes only with the opt-in propose mode. |
| Dify | ARC-09 backup and restore | 1 | 0 | The second rater found no supported backup for the database, files or vector store. |
| OpenClaw | DEL-11 release rollback | n/a | 2 | Scope fact `code_release_path`: the second rater counted plugins the agent builds and activates as code releases. |
| Dify | GOV-10 bounded self-change | n/a | 2 | Scope fact `agent_mutations`: the second rater counted the agent writing its own build draft. |

## What changes and what does not

- **The headline finding holds.** Both raters fail definition rollback (GOV-05 = 2) for all three products, so no product reaches L3 under either rating.
- **Two control verdicts flip:**
  - n8n security, pass under the first rating and fail under the second;
  - OpenClaw tested backup and restore, pass under the first and fail under the second.

  The OpenClaw restore result rests on the new scheduled-work surface. The first rating scored it 3 and the second 2. That surface needs adjudication before the field-test results are updated.
- **Two rubric clarifications are needed:**
  - how LRN-08 applies to products with no learning loop;
  - what counts as a code release path and as an agent mutation.

The first rating's field-test results are left unchanged until these differences are adjudicated.

## Third rater: ChatGPT (Codex)

A third rater, ChatGPT in Codex, ran the same blind task with the same rules. It read the code through GitHub's web pages at the pinned commits because it could not clone, so its absence findings are bounded by the files it opened. Its scores, with abbreviated evidence, are in `chatgpt-n8n.json`, `chatgpt-openclaw.json` and `chatgpt-dify.json`.

| Product | Criterion | First | Second | Third |
|---|---|---:|---:|---:|
| n8n | GOV-05 definition rollback | 2 | 2 | 2 |
| n8n | ARC-02 migrations | 2 | 2 | 2 |
| n8n | ARC-09 backup and restore | 2 | 2 | 1 |
| n8n | ARC-05 tenant isolation | n/a | n/a | 2 |
| n8n | GOV-04 security | 3 | 2 | 2 |
| n8n | GOV-10 bounded self-change | 2 | 2 | 2 |
| n8n | LRN-08 learned-change validation | 2 | 1 | 0 |
| OpenClaw | GOV-05 definition rollback | 2 | 2 | 2 |
| OpenClaw | DEL-11 release rollback | n/a | 2 | n/a |
| OpenClaw | ARC-02 migrations | 2 | 2 | 1 |
| OpenClaw | ARC-09 backup and restore | 3 | 2 | 2 |
| OpenClaw | ARC-05 tenant isolation | n/a | n/a | 2 |
| OpenClaw | GOV-04 security | 3 | 3 | 2 |
| OpenClaw | GOV-10 bounded self-change | 2 | 2 | 2 |
| OpenClaw | LRN-08 learned-change validation | 2 | 0 | 1 |
| Dify | GOV-05 definition rollback | 2 | 2 | 2 |
| Dify | ARC-02 migrations | 2 | 2 | 2 |
| Dify | ARC-09 backup and restore | 1 | 0 | 0 |
| Dify | ARC-05 tenant isolation | 2 | 2 | 2 |
| Dify | GOV-04 security | 2 | 2 | 1 |
| Dify | GOV-10 bounded self-change | n/a | 2 | 2 |
| Dify | LRN-08 learned-change validation | 1 | 1 | 0 |

"n/a" means the rater found the criterion not applicable because a scope fact was false. Rows where all three raters marked it not applicable are omitted.

### Three-rater agreement

Across the 18 ratings that all three raters assessed:

- **All three gave the same score** on 8 of 18.
- **All three were within one level** on 16 of 18. Both exceptions are LRN-08, the criterion whose definition is unclear for products with no learning loop.

Exact agreement between each pair of raters:

| Pair | Exact |
|---|---|
| First and second | 13 of 18 |
| First and third | 8 of 18 |
| Second and third | 12 of 19 |

### What the three raters show

- **Definition rollback (GOV-05) scored 2 in every rating:** all three raters, all three products. The finding that none of these products reaches L3 does not depend on the rater.
- **The first rating was the most generous on two control criteria.** The other two raters both scored lower on n8n security (GOV-04) and on OpenClaw backup and restore (ARC-09, the scheduled-work surface). Both should be adjudicated down to 2.
- **Three rubric points need tightening:**
  - LRN-08 for products with no learning loop;
  - when a product counts as multi-tenant (the third rater counted n8n projects and OpenClaw workspaces);
  - what counts as a code release path or an agent mutation.

All three raters are AI models. A human second rater is the next step.

## What changed as a result (EVOLVE v0.7)

- **Definitions tightened.** The rubric now says when a product is multi-tenant (workspaces and projects with their own members count; one person's several workspaces do not), what counts as a code release path (code the product's own AI writes and activates), what counts as an agent mutation (including drafts stored awaiting approval), and how to read LRN-08 for products that make no learned or AI-made changes.
- **Corrections.**
  - n8n security (GOV-04) is now 2. Re-reading the code confirmed both raters: the pull-request security job runs only when GitHub workflow files change, and the container scan never fails a build.
  - OpenClaw scheduled-work restore (ARC-09) is being lowered to 2 in the v0.7 migration.
- **Re-reading under the new definitions changed two scope facts.** n8n's team projects make it multi-tenant, and its agent builder writes code that runs, so tenant isolation and release rollback now apply to it. Its level did not change.
- **The study is now repeatable.** `evals/agreement.py` compares any two or more assessments of a product and reproduces every number above. `evals/disagreements.md` logs each disagreement and the rubric change it led to.

## Full blind second rating under v0.7 (November 2026)

**Date:** 17 November 2026. **Framework:** EVOLVE v0.7.0.

### What was done

Three products were rated again from scratch on all 75 criteria, with scope facts, kinds of change, confidence and AI delivery: n8n (a level 2 product), LibreChat (published at 0) and Frappe (published at 1), at the same commits as the field test. Each rater was a separate AI agent (Claude) given only the skill folder and the product source. It had no access to `assessments/`, `evals/`, `spec/`, the README or the CHANGELOG. Its raw ratings are `v07-n8n.json`, `v07-librechat.json` and `v07-frappe.json`. Every number below comes from `evals/agreement.py`, comparing each with the product's published `assessment.json`.

### Agreement

| Product | Scores both assessed | Exact | Within one | Level 3 controls agree | Scope facts differ | Overall level, published · blind |
|---|---:|---:|---:|---|---:|---|
| n8n | 73 | 48 (66%) | 72 (99%) | 6 of 8 (the other 2 differ only through scope facts) | 3 of 12 | SAL 2 · SAL 2 |
| LibreChat | 63 | 45 (71%) | 60 (95%) | 6 of 8 | 1 of 12 | SAL 0 · SAL 1; SAL 0 under the settled rules |
| Frappe | 64 | 56 (88%) | 64 (100%) | 8 of 8 | 0 of 12 | SAL 1 · SAL 0 |
| **All three** | **200** | **149 (74%)** | **196 (98%)** | | | |

After the LibreChat corrections below, LibreChat's exact agreement is 48 of 63 (76%) and within one is 62 of 63 (98%).

### What the raters agree on

- **No product reaches Level 3.** Every applicable Level 3 control fails under both raters for all three products. Definition rollback (GOV-05) is 2 in all six ratings.
- **Scores rarely differ by more than one point.** Of 200 shared scores, four differ by two: LibreChat's job queue, AI lane and integration mapping, and n8n's AI access check.

### Where the overall level differs, and why

The overall level can turn on a single judgement, usually about kinds of change.

- **LibreChat: published 0, blind 1. Settled at 0.** Re-reading the code at the pinned commit confirmed three errors in the published rating, now corrected: the product's agent writes skills on request inside permission and content checks, which scoring rule 4 counts as an AI lane (DEL-04 0 to 2); a leased job queue with retries and dead letters exists (ARC-04 1 to 3); and the upgrade guide tells operators to back up MongoDB (ARC-09 0 to 1). The blind rater's Level 1 came from that skills lane. Skills are not a main kind of change, and under the settled rule an AI lane counts only when it serves one, so LibreChat stays at 0. Its one blocking gap: tool connections cannot be undone.
- **Frappe: published 1, blind 0. Settled at 1.** Both raters agree that custom server logic needs an engineer, because Server Scripts are off by default. The published rating judged it not a main kind of change; the blind rater judged it main. Under the settled test, a kind the product offers only to developers is not main, so Frappe stays at Level 1.
- **n8n: both 2.** The raters differ on three scope facts: whether licence-gated team projects make it multi-tenant, whether AI-written code inside a workflow is a code release, and whether saved "always allow" preferences mean changes apply automatically. None moves the level. The blind rater also reads the fix loop as AI-driven at L2 (published AI L0).

### What changed as a result

- LibreChat corrected (above) and its report regenerated.
- The five questions the raters split on are now rules: what makes a kind of change main; what counts as self-serve and as undo; an AI lane counts only when it serves a main kind; scope facts follow the scored installation; code inside a sandboxed, versioned definition is part of it. See `CHANGELOG.md`.

All raters are still AI models. A human second rating remains the next step.
