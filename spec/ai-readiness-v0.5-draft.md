# EVOLVE v0.5: AI Readiness View and AI Capability Footprint (specification, revision 2)

**Status: revised after review; implemented on this branch, not merged.** The results are provisional and single-rater.

**Changes from revision 1:**

1. The draft headline mixed two things: whether the product's AI is safe to run in production, and how widely AI is used. The first is now the **AI Readiness** headline. The second is a separate, descriptive **AI Capability Footprint** with no headline (section 6).
2. The Intelligence dimension is gone. Readiness is now **Context, Quality, Governance and Operations**.
3. AIR-03 applies only when AI reads product data. A prompt-only feature is not marked down for lacking retrieval.
4. Every reused criterion has explicit 0–4 anchors for its AI-qualified reading (section 5).
5. AI-qualified readings have explicit statuses and support grades, alternates, opt-in readings and facets, like any criterion.
6. AIR-01 recognises same-provider failover, self-hosted redundancy and controlled degradation, not only multi-provider fallback.
7. Headline levels are named, and a failed gate is labelled **"not production-governed"**.

## 1. Two questions, kept separate

| Reading | Question |
|---|---|
| **Software Autonomy Level (SAL)** | How ready is the product to evolve itself safely? |
| **AI Readiness** | How safely can the product run AI in production? |
| **AI Capability Footprint** (descriptive, non-headline) | What kinds of meaningful work can its AI actually do? |

**SAL does not change.** The eight new checks and the AI-qualified readings feed only the AI view. They never enter a loop condition, a critical control or an EVOLVE capability score. A test proves that SAL and the profile are identical with and without them.

## 2. AI Readiness at a glance

```
AI Readiness L2 (Deployed with material control gaps) · Context 3 · Quality 2 · Governance 2 · Operations 3
Gates: permissions ✓  regression gate ✗  traceability ✓   -> not production-governed
```

| Dimension | Contributors | Asks |
|---|---|---|
| **Context** | AIR-03, AIR-04 | Can AI reach the product data it needs, without exceeding the user's permissions? |
| **Quality** | AIR-05, AIR-06 | Is AI behaviour evaluated, and blocked from release when it gets worse? |
| **Governance** | AIR-07; AI-qualified GOV-09, GOV-10, GOV-11; AI-qualified LRN-08 when AI changes the product itself | Are AI actions traceable, bounded, scoped and protected from manipulated inputs? |
| **Operations** | AIR-01, AIR-02, AIR-08; the AI-provider surface of ARC-08 | Is AI portable, affordable, contained when it fails, and watched in production? |

### Headline levels

| Level | Name | Meaning |
|---|---|---|
| L0 | Foundational gap | At least one dimension lacks the basics, even if others are strong. |
| L1 | Experimental | Some foundations exist; most are partial or manual. |
| L2 | Deployed with material control gaps | AI runs with real mechanisms, but at least one dimension or gate falls short of production governance. |
| L3 | Production-governed | Every dimension at 3 and every applicable gate passes. |
| L4 | Adaptive and operationally proven | Every dimension at 4, with the gate criteria backed by operational evidence. |

### Scoring rules

1. **Dimension level** is the floor of the mean of its applicable contributors. Floor rather than rounding, so a dimension never claims a level most of its parts have not reached. A dimension with no applicable contributors (for example Context, when AI reads no product data) is not applicable and is left out.
2. **Headline** is the lowest applicable dimension. The weakest-link rule applies once, across dimensions, not again inside them.
3. **Gates.** Failing any applicable gate caps the headline at **L2**, and the report adds **"not production-governed"**:

   | Gate | Passes when | Applies when |
   |---|---|---|
   | Permission-preserving access | AIR-04 ≥ 3 | `ai_data_access` |
   | Regression evaluation before release | AIR-06 ≥ 3 | `ai_features` |
   | Traceability of consequential AI actions | AIR-07 ≥ 3 | `ai_actions` |

   The gate criteria are depth-capped, like v0.4 critical controls: a 3 needs tested evidence and a 4 needs operated evidence.
4. **Default and opt-in.**
   - The headline uses the default configuration, as SAL does.
   - The opt-in reading uses shipped opt-in settings: `available_score` on criteria and readings, and `available_value` on the AI scope facts. It is shown beside the headline.
   - When AI is off by default, the headline reads "no AI features by default" and the opt-in reading carries the score.

### New scope facts

| Fact | True when |
|---|---|
| `ai_features` | The product ships features that call a language or other ML model |
| `ai_data_access` | AI features read product data, or call tools that can (requires `ai_features`) |
| `ai_actions` | AI can take consequential actions (requires `ai_features`) |

A **consequential action** changes data or definitions, sends a message outside the product, or spends money.

Each AI fact may carry `available_value` for the opt-in reading. If `ai_features` is false, the view reports "no AI features" and the eight checks are not applicable.

## 3. The eight new checks

| ID | Check | Dimension | Applies when |
|---|---|---|---|
| AIR-01 | Model and provider portability and resilience | Operations | `ai_features` |
| AIR-02 | AI usage and per-customer cost controls | Operations | `ai_features` |
| AIR-03 | AI-ready data and context access | Context | `ai_data_access` |
| AIR-04 | Permission-preserving retrieval and tool access (**gate**) | Context | `ai_data_access` |
| AIR-05 | Offline AI evaluation | Quality | `ai_features` |
| AIR-06 | Regression gating before release (**gate**) | Quality | `ai_features` |
| AIR-07 | AI action tracing and auditability (**gate when `ai_actions`**) | Governance | `ai_features` |
| AIR-08 | Production quality, drift and feedback monitoring | Operations | `ai_features` |

The checks are not part of any EVOLVE capability, so they never move the six-capability profile.

## 4. Anchors for the eight checks

### AIR-01 Model and provider portability and resilience
Any mature resilience strategy counts: fallback to another model or provider, same-provider failover (region or deployment), self-hosted redundancy, or controlled degradation, where the feature switches off cleanly, queues, or answers without AI. Multi-provider fallback is not required.
- **0** One hard-coded model; its failure breaks the feature.
- **1** The model is configurable by engineers in code or environment.
- **2** An abstraction supports several models or providers, switched by configuration; failure handling is ad hoc.
- **3** Operators choose models per feature through a supported path, and model failure is handled by a declared, tested resilience strategy.
- **4** Models are routed by policy (cost, latency, quality), with evaluated equivalence before a switch.

### AIR-02 AI usage and per-customer cost controls
- **0** None.
- **1** Only the provider's dashboard, or raw logs.
- **2** Tokens and cost are recorded per request and per user or tenant, and are queryable.
- **3** Per-tenant or per-user budgets or quotas are enforced in the product, with an admin view.
- **4** Spend policy degrades gracefully (cheaper model, queueing) and forecasts usage.

### AIR-03 AI-ready data and context access
- **0** Applicable, but AI sees only the prompt.
- **1** Engineers assemble context in code for each feature.
- **2** Retrieval or indexing (search, embeddings) covers some data; sync is manual or partial.
- **3** Product data and definitions reach AI through a governed context layer (retrieval, tools, schema-aware context). The layer stays fresh automatically and attributes its sources.
- **4** The context layer is generated from definitions, so new entities reach AI without code, and retrieval quality is measured.

### AIR-04 Permission-preserving retrieval and tool access (gate)
- **0** AI uses an admin or service account.
- **1** Restrictions live only in prompt instructions.
- **2** Permissions are enforced for some sources or tools; others run with elevated access.
- **3** Every retrieval and tool call AI makes runs with the requesting user's permissions, or a scoped agent identity, enforced in code. Tests show a user cannot obtain through AI what they cannot access directly.
- **4** Row- and field-level policy and tenant isolation are covered by automated adversarial tests, and denials are audited.

### AIR-05 Offline AI evaluation
- **0** None.
- **1** Manual spot checks.
- **2** An evaluation harness or datasets exist for some features and are run on request.
- **3** Each AI feature has a maintained evaluation set with metrics (accuracy, groundedness, safety). Evaluations run reproducibly, and results are stored per prompt and model version.
- **4** Evaluation sets grow automatically from production failures and feedback, and include adversarial cases.

### AIR-06 Regression gating before release (gate)
- **0** AI changes ship unevaluated.
- **1** Prompt or model changes are reviewed manually.
- **2** Evaluations run in CI but do not block, or cover only some AI features.
- **3** Changes to prompts, models, tools or retrieval are blocked from release when evaluation scores regress past declared thresholds.
- **4** Gating covers every AI change class, including learned and self-made changes, with canary comparison in production.

### AIR-07 AI action tracing and auditability (gate when `ai_actions`)
- **0** None.
- **1** Application logs only.
- **2** Model calls (prompts, responses) can be traced for engineers, often through an opt-in integration.
- **3** Every consequential AI action records what triggered it, for whom, the inputs, the model and prompt version, the tool calls, and the output and resulting change. Operators can query these records, and they are retained.
- **4** Traces are linked to approvals and reversals, can be replayed, and are tamper-evident.

### AIR-08 Production quality, drift and feedback monitoring
- **0** None.
- **1** Feedback is collected but not analysed.
- **2** Feedback and quality signals are recorded per AI feature and version, and are visible.
- **3** Quality metrics (feedback, evaluator scores, failure and refusal rates) are monitored continuously per feature and model version, with alerts on drift.
- **4** Drift triggers re-evaluation, rollback or a model switch under policy.

## 5. AI-qualified readings of existing criteria

Thirteen existing criteria describe behaviour that may or may not involve AI. A form can be request intake, rules can diagnose, and scripts are machine actors. Each of the thirteen therefore carries a separate **AI-qualified reading** (`ai` in the assessment) that scores only its AI-backed behaviour, against the anchors below.

**The reading is a full entry:**

- **Status:** `assessed`, `not_evidenced` or `not_applicable`.
- **Fields:** `score`, `grade`, `evidence`, `alt_score` (upward only), `available_score` and `facets`. Depth caps apply where the parent criterion is depth-capped.
- **When it is required:** for every one of the thirteen whenever `ai_features` is true, in the default or opt-in reading.
- **Not evidenced:** computes as 0 but is reported separately from a confirmed 0.
- **When `not_applicable` is allowed:**
  - when the parent criterion is not applicable;
  - for GOV-09 when `ai_actions` is false;
  - for LRN-08 when `agent_mutations` is false.

  Nowhere else, so a missing AI behaviour scores 0 rather than disappearing.
- **ARC-08:** when its inventory records the `ai_providers` surface, the reading must equal that level, and its alternate and opt-in readings may not exceed it. The scorer also caps every variant at that level.
- **The general criterion score is never changed**, so SAL and the profile are unaffected.

| Criterion | Used in | AI-qualified anchors (0 · 1 · 2 · 3 · 4) |
|---|---|---|
| MAL-19 agent tool surface | Footprint: Operate | 0 none · 1 documentation only · 2 an API agents can call, but no typed agent tools · 3 a typed tool surface for AI agents (MCP or equivalent) with scoped auth · 4 tools generated from definitions, including defined entities, with a current capability map |
| MAL-20 model-backed conversation | Footprint: Operate | 0 no model-backed conversation (keyword or FAQ bots count as 0) · 1 model answers without grounding in product data · 2 a grounded assistant for one persona or surface · 3 users complete tasks and operators author through a grounded assistant, with preview · 4 the assistant covers every UI action, and groundedness is evaluated |
| DEL-01 AI intake | Footprint: Build | 0 no model in intake (forms count as 0) · 1 a model summarises or rewrites requests · 2 a model asks clarifying questions or drafts a structured plan · 3 a model produces a change specification with acceptance criteria, impact and risk class, which a person confirms · 4 the specification is machine-readable and drives implementation and tests |
| DEL-04 AI implementation lane | Footprint: Build | Same anchors as DEL-04, which is inherently AI |
| LRN-05 AI diagnosis | Footprint: Diagnose and improve | 0 no model diagnosis (rule-based grouping counts as 0) · 1 a model explains a pasted error on request · 2 a model explains failures with attached context on request · 3 for detected issues, a model produces a reproducible case and likely cause linked to the responsible area · 4 a model validates its diagnosis by reproduction |
| LRN-06 AI proposals | Footprint: Diagnose and improve | 0 none (rule-based recommendations count as 0) · 1 a model suggests changes on request, without evidence · 2 a model drafts proposals for one area, citing evidence · 3 ranked, model-generated proposals across the product, with evidence and expected impact · 4 proposals carry ready changes and post-apply measurement |
| LRN-07 AI learning | Footprint: Diagnose and improve | 0 none (heuristic tuning counts as 0) · 1 people ask a model to write rules or skills · 2 a model drafts candidate changes from experience on request · 3 a model reviews experience continuously and drafts changes unprompted · 4 it also prioritises them and learns which kinds of change succeed |
| LRN-08 validation of AI-made changes | Footprint: Diagnose and improve; Governance when `agent_mutations` | 0 none · 1 manual review only · 2 automated scans or lint on AI-made changes · 3 AI-made changes are evaluated against a baseline before apply, with a pass, revise or block decision · 4 automatic, on held-out data, feeding policy |
| EXP-05 AI opportunity proposals | Footprint: Expand | 0 none · 1 a model summarises demand on request · 2 a model drafts an adjacent-capability proposal on request · 3 a model proposes unprompted, with evidence, sizing and fit · 4 it also produces a buildable specification and a prototype |
| GOV-09 AI agent action safety | Governance (n/a when `ai_actions` is false) | 0 AI acts with admin or ambient authority · 1 shared keys · 2 per-user or per-agent identity for AI actions, but no preview · 3 scoped AI identity, idempotent actions, preview or approval for mutations, rate limits · 4 policy-gated with per-action risk classification, budgets and a kill switch. Audit trails are left out here because AIR-07 scores them. |
| GOV-10 bounds on AI-driven change | Governance | 0 unrestricted · 1 prompt instructions only · 2 an allow or deny list in code for some AI paths · 3 every AI change path enforced against a declared scope, with a blast-radius limit · 4 versioned policy, tightened automatically after failures |
| GOV-11 model-input integrity | Governance | 0 untrusted content goes straight into prompts that can trigger changes · 1 no provenance · 2 some filtering or fencing · 3 untrusted content fenced as data, injection-scanned, with provenance recorded; it cannot alone trigger an auto-applied change · 4 adversarial inputs in automated evaluation, and changes revertible by source |
| ARC-08 AI-provider containment | Operations | 0 a provider failure breaks the product · 1 errors caught locally · 2 timeouts and retries on model calls · 3 timeouts and circuit breakers or bulkheads around model calls, with tested fallback behaviour; failure is contained to the AI feature · 4 degradation modes declared and exercised by fault injection |

**Overlaps resolved:**
- **ARC-08 and AIR-01:** ARC-08's AI surface scores containment (a model failure stays inside the AI feature). AIR-01 scores portability and the declared strategy for continuing or degrading the AI service.
- **GOV-09 and AIR-07:** audit trails count only under AIR-07, never under GOV-09.
- **LRN-08 and AIR-05/06:** LRN-08 covers changes the product makes to itself; AIR-05 and AIR-06 cover its AI features.
- **GOV-11 and AIR-04:** GOV-11 is about poisoned inputs; AIR-04 is about over-privileged access.
- **LRN-09 is left out.** Production AI quality is AIR-08.

## 6. AI Capability Footprint (descriptive, non-headline)

The footprint shows what the product's AI does, without judging readiness. A focused product with excellent AI governance is not marked down for lacking AI that builds changes or proposes products.

| Area | AI-qualified readings |
|---|---|
| Operate | MAL-19, MAL-20 |
| Build | DEL-01, DEL-04 |
| Diagnose and improve | LRN-05, LRN-06, LRN-07, LRN-08 |
| Expand | EXP-05 |

Each area shows its readings and their floor-of-mean. There is no footprint headline, and the footprint never affects AI Readiness or SAL.

## 7. Report

```
AI Readiness L2 (Deployed with material control gaps) · Context 3 · Quality 2 · Governance 2 · Operations 3
  not production-governed: regression gate fails (AIR-06 = 2, needs 3)
  with opt-in settings: L2 · alternate readings: L3
  contributors: Context AIR-03 3, AIR-04 3 · Quality AIR-05 2, AIR-06 2 · ...
  not evidenced: GOV-11 (AI)
AI Capability Footprint: Operate 3 · Build 2 · Diagnose and improve 1 · Expand 0
```

## 8. Tests that must hold (adversarial)

**SAL isolation**
- SAL, loop levels, controls and the EVOLVE profile are identical with and without the AI view.

**AI-qualified readings**
- A reused criterion with a high general score adds nothing unless its AI-qualified reading supports it.
- A missing AI-qualified reading is rejected when `ai_features` is true.
- `not_applicable` outside the allowed cases is rejected.
- `not_evidenced` computes as 0 and is reported separately.
- An ARC-08 reading that contradicts the `ai_providers` inventory level is rejected, and so is an alternate or opt-in reading above it.
- An AI-qualified alternate must be one level up, and an opt-in reading cannot be lower than the score.

**Scope facts**
- AI facts that contradict each other (data access or actions without AI features) are rejected.
- A prompt-only product (no `ai_data_access`) has no Context dimension, and its headline is not lowered by it.
- A product with no AI features gets no headline.

**Headline and gates**
- One weak dimension sets the headline, whatever the other three score.
- Dimension levels use floor, not rounding.
- A failed gate caps the headline at L2 and labels it "not production-governed"; a non-applicable gate does neither.
- Gate criteria at 3 need tested evidence (depth cap).

**Footprint**
- Footprint scores never change the readiness headline.

## 9. Decisions recorded from review

1. Dimension level is the floor of the mean; the weakest-link rule applies once, across dimensions.
2. The headline uses the default configuration; the opt-in reading is shown separately.
3. No breadth check inside readiness. Breadth is the separate footprint.
4. A failed gate caps the headline at L2, labelled "not production-governed".
5. L0 is named "Foundational gap", not "No production AI foundation": one missing dimension sets it, even when others are strong (Directus has Context 3 and Quality 0).
6. The footprint is described as descriptive and non-headline, not unscored: each area has a descriptive level, but nothing aggregates it.
