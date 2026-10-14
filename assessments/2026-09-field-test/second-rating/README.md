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
