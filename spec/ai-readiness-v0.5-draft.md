# EVOLVE v0.5: AI Readiness View (specification draft)

**Status: draft for review.** Nothing in `scripts/`, `references/rubric.md` or `assessments/` uses this yet. Implementation starts only after this specification is reviewed.

## 1. Two questions, kept separate

EVOLVE v0.4 answers one question. This draft adds a second, related one:

| Reading | Question |
|---|---|
| **Software Autonomy Level (SAL)** | How ready is the product to evolve itself safely? |
| **AI Readiness** | How ready is the product to build, operate and govern AI safely in production? |

They overlap but are not the same. A product can run AI features well while never changing itself (high AI Readiness, low SAL). Another can evolve itself through rules and configuration with no model involved (the reverse).

**The SAL calculation does not change.** The eight new checks feed only the AI Readiness View. They do not enter any loop condition, critical control or EVOLVE capability score. A test will prove that adding or removing them leaves every SAL result unchanged.

## 2. Structure

```
AI Readiness n/4 = weakest of four dimensions, capped at 2 if any AI gate fails

  Context        can AI reach the right product data and capabilities, without exceeding permissions?
  Intelligence   does AI do real product work: take requests, build changes, diagnose, propose?
  Assurance      is AI behaviour evaluated, gated before release, bounded, traceable?
  Operations     is AI portable, affordable and watched in production?

Example:  AI Readiness 2/4 · Context 3 · Intelligence 3 · Assurance 2 · Operations 2
```

Each dimension draws on:

- **new AI checks** (`AIR-01` to `AIR-08`), which are AI-specific by definition; and
- **existing criteria**, which count only through an **AI-qualified reading** (section 5).

## 3. The eight new checks

The four additions proposed in the last round each bundled separate concerns. Here they are split into eight checks, scored 0–4 on the usual ladder. The full anchors are in section 7.

| ID | Check | Dimension | Splits out of |
|---|---|---|---|
| AIR-01 | Model and provider portability and fallback | Operations | "model flexibility and cost" |
| AIR-02 | AI usage and per-customer cost controls | Operations | "model flexibility and cost" |
| AIR-03 | AI-ready data and context access | Context | "data readiness for AI" |
| AIR-04 | Permission-preserving retrieval and tool access (**gate**) | Context | "data readiness for AI" |
| AIR-05 | Offline AI evaluation | Assurance | "AI evaluation" |
| AIR-06 | Regression gating before release (**gate**) | Assurance | "AI evaluation" |
| AIR-07 | AI action tracing and auditability (**gate**) | Assurance | "AI monitoring" |
| AIR-08 | Production quality, drift and feedback monitoring | Operations | "AI monitoring" |

The pairs were split because each half can be present without the other:

- **Portability vs cost:** a product can switch models freely and have no spending limits, or the reverse.
- **Context vs permissions:** rich retrieval with an admin service account is the most dangerous combination, so permissions must be scored on their own.
- **Offline evaluation vs release gating:** many products have evaluation sets that nothing blocks on.
- **Tracing vs monitoring:** auditing what the AI did is a different capability from watching whether its answers are getting worse.

## 4. Overlap analysis of the 13 existing AI-related criteria

Several existing criteria are not inherently about AI. A form can be request intake; rules can do diagnosis; scripts are machine actors. Averaging them straight into an AI score would credit non-AI behaviour as AI readiness. Each one therefore either qualifies only under a stated interpretation, or is excluded.

| Criterion | Inherently AI? | Qualifying interpretation (what counts towards AI Readiness) | Dimension | Overlap handling |
|---|---|---|---|---|
| MAL-19 capability surface for agents | Mostly | A typed tool surface designed for AI agents (MCP or equivalent) with scoped auth. A plain REST API or OpenAPI document alone does not qualify. | Context | Distinct from AIR-04: MAL-19 is what agents can reach; AIR-04 is whether permissions hold when they do. |
| MAL-20 conversational operation and authoring | No | Only conversation backed by a language model grounded in product data. FAQ or keyword bots and scripted wizards do not qualify. | Intelligence | None. |
| DEL-01 request intake | No | Only intake where a model structures the request: clarifying questions, a generated plan or specification. A structured form does not qualify. | Intelligence | None. |
| DEL-04 AI implementation lane | Yes | As scored. | Intelligence | None. |
| LRN-05 automated diagnosis | No | Only diagnosis a model produces (likely cause, reproduction). Rule-based grouping and fingerprinting do not qualify. | Intelligence | None. |
| LRN-06 ranked proposals | No | Only proposals a model generates. Rule-based recommendations do not qualify. | Intelligence | None. |
| LRN-07 learning from experience | No | Only learning that uses a model (reflection or review that writes skills, memory or rules). Heuristic tuning, such as automatic column materialisation, does not qualify. | Intelligence | None. |
| LRN-08 learned changes validated | No | Only validation of AI-made changes. Lint and schema checks on human changes do not qualify. | Assurance | Distinct from AIR-05 and AIR-06: LRN-08 covers changes the product makes to itself; AIR-05 and AIR-06 cover the product's AI features (prompts, models, retrieval). |
| EXP-05 opportunity proposals | No | Only adjacent-capability proposals a model generates. | Intelligence | None. |
| GOV-09 agent-safe actions | No | Only the controls on AI agents: identity, scopes, idempotency, preview, rate limits. Scripts and integrations do not count. | Assurance | Audit rows are left out of this reading because AIR-07 scores tracing, so the same evidence is not counted twice. |
| GOV-10 bounded self-change | Partly | Only bounds on AI-driven changes. | Assurance | None. |
| GOV-11 learning-input integrity | Mostly | Only where the inputs feed a model, for example injection fencing and provenance of AI-made changes. | Assurance | Distinct from AIR-04: GOV-11 is about poisoned inputs; AIR-04 is about over-privileged access. |
| ARC-08 failure isolation | No | Only its AI-provider surface: timeouts, circuit breakers and containment when a model provider fails. Connectors, plugins, tenants and internal services do not count. | Operations | Distinct from AIR-01: ARC-08's AI surface is containing failure; AIR-01 is switching or falling back to another model. |

Leaving out LRN-09 (impact measurement) was deliberate. It measures any change against a baseline; production quality of AI features is AIR-08.

## 5. How reused criteria contribute

- **AI-qualified reading.** Each reused criterion carries an optional `ai` entry: `{"score": 0..4, "evidence": "..."}`. This is the level of the criterion's AI-qualified behaviour under the interpretation in section 4, with its own evidence.
- **No `ai` entry, product has AI features:** the criterion contributes **0**. AI readiness is not demonstrated by non-AI behaviour.
- **Criterion not applicable** (archetype or scope fact): it is left out of the dimension.
- **ARC-08:** the `ai` score must equal the level of the `ai_providers` surface whenever an inventory with that surface is recorded.
- **The AI-qualified score is independent of the criterion's general score.** For example, GOV-09 may score 2 overall because scripts use shared keys, while AI agents run with scoped identities and the AI reading is 3. The evidence must say which actors or paths it covers.

The general score is never changed by the `ai` entry, so SAL and the EVOLVE profile stay exactly as in v0.4.

## 6. Scoring the view

1. **Dimension level** = the floor of the mean of the dimension's contributing scores (new checks plus AI-qualified readings). Floor, not rounding, because a dimension should not claim a level most of its parts have not reached.
2. **Headline** = the lowest dimension level. One weak dimension (for example, no evaluation) cannot be hidden by strong others.
3. **AI gates** are three hard controls. Failing any applicable gate caps the headline at **2**, matching SAL, where a failed critical control caps a loop at L2.

   | Gate | Passes when | Applies when |
   |---|---|---|
   | Permission-preserving access | AIR-04 ≥ 3 | `ai_data_access` |
   | Regression evaluation before release | AIR-06 ≥ 3 | `ai_features` |
   | Traceability of consequential AI actions | AIR-07 ≥ 3 | `ai_actions` |

   The gate criteria are depth-capped, as v0.4 critical controls are: a 3 needs tested evidence.
4. **Report:** `AI Readiness 2/4 · Context 3 · Intelligence 3 · Assurance 2 · Operations 2`, plus:
   - each dimension's contributing scores;
   - which reused criteria had no AI-qualified evidence;
   - gate status;
   - the opt-in and alternate readings, as for SAL.

### New scope facts

| Fact | True when |
|---|---|
| `ai_features` | The product ships features that call a language or other ML model |
| `ai_data_access` | AI features read product data, or call tools that can |
| `ai_actions` | AI can take consequential actions: change data or definitions, send messages outside the product, or spend money |

If `ai_features` is false, the view reports `AI Readiness: no AI features`. It still shows the Context and Operations foundations, but gives no headline level.

## 7. Anchors for the eight checks

**Consequential action** means an action that changes data or definitions, sends messages outside the product, or spends money.

### AIR-01 Model and provider portability and fallback
- **0** One hard-coded model and provider.
- **1** Model name configurable by engineers in code or environment.
- **2** A provider abstraction supports several providers; switching needs configuration and a restart; no fallback.
- **3** Operators choose models per feature through a supported path, with automatic, tested fallback to another model or provider on failure or rate limit.
- **4** Models are routed by policy (cost, latency, quality), with evaluated equivalence before a switch.

### AIR-02 AI usage and per-customer cost controls
- **0** None.
- **1** Only the provider's own dashboard, or raw logs.
- **2** Tokens and cost recorded per request and user or tenant, queryable.
- **3** Per-tenant or per-user budgets or quotas enforced in the product, with an admin view and alerts.
- **4** Spend policy degrades gracefully (cheaper model, queueing) and forecasts usage.

### AIR-03 AI-ready data and context access
- **0** AI sees only the prompt.
- **1** Engineers assemble context in code per feature.
- **2** Retrieval or indexing (search, embeddings) for some data; sync is manual or partial.
- **3** Product data and definitions reach AI features through a governed context layer (retrieval, tools, schema-aware context) that stays fresh automatically and attributes sources.
- **4** The context layer is generated from definitions, so new entities reach AI without code, and retrieval quality is measured.

### AIR-04 Permission-preserving retrieval and tool access (gate)
- **0** AI uses an admin or service account.
- **1** Restrictions live only in prompt instructions.
- **2** Permissions are enforced for some sources or tools; others run with elevated access.
- **3** Every retrieval and tool call made by AI runs with the requesting user's permissions, or a scoped agent identity, enforced in code. Tests show a user cannot obtain through AI what they cannot access directly.
- **4** Row- and field-level policy and tenant isolation are covered by automated adversarial tests, and denials are audited.

### AIR-05 Offline AI evaluation
- **0** None.
- **1** Manual spot checks.
- **2** An evaluation harness or datasets exist for some features and are run on request.
- **3** Each AI feature has a maintained evaluation set with metrics (accuracy, groundedness, safety), run reproducibly, with results stored per prompt and model version.
- **4** Evaluation sets grow automatically from production failures and feedback, and include adversarial cases.

### AIR-06 Regression gating before release (gate)
- **0** AI changes ship unevaluated.
- **1** Manual review of prompt or model changes.
- **2** Evaluations run in CI but do not block, or cover only some AI features.
- **3** Changes to prompts, models, tools or retrieval for AI features are blocked from release when evaluation scores regress past declared thresholds.
- **4** Gating covers every AI change class, including learned and self-made changes, with canary comparison in production.

### AIR-07 AI action tracing and auditability (gate)
- **0** None.
- **1** Application logs only.
- **2** Model calls (prompts, responses) can be traced for engineers, often through an opt-in integration.
- **3** Every consequential AI action records:
  - what triggered it, and for whom;
  - its inputs;
  - the model and prompt version;
  - its tool calls;
  - its output and the resulting change.

  Records are queryable by operators and retained.
- **4** Traces are linked to approvals and reversals, can be replayed, and are tamper-evident.

### AIR-08 Production quality, drift and feedback monitoring
- **0** None.
- **1** Feedback is collected but not analysed.
- **2** Feedback and quality signals are recorded per AI feature and version, and are visible.
- **3** Quality metrics (feedback, evaluator scores, failure and refusal rates) are monitored continuously per feature and model version, with alerts on drift.
- **4** Drift triggers re-evaluation, rollback or a model switch under policy.

## 8. Implementation plan (after review)

1. **Rubric:**
   - an "AI readiness checks" section with AIR-01 to AIR-08;
   - an `ai_view` block in the model (dimensions, contributors, qualifying notes, gates, the three new facts);
   - qualifying notes added to the 13 reused criteria.

   The AIR checks are kept out of the EVOLVE capabilities.
2. **Scorer:**
   - the AI Readiness View, including the `ai` entry validation (evidence required, the ARC-08 inventory link);
   - the report section and JSON output;
   - SAL code untouched.
3. **Adversarial tests:**
   - a reused criterion with a high general score but no `ai` entry adds nothing;
   - one weak dimension sets the headline whatever the other three score;
   - a failed gate caps the headline at 2, and a non-applicable gate does not;
   - an `ai` score without evidence is rejected;
   - an ARC-08 `ai` score that contradicts its inventory is rejected;
   - SAL results are identical with and without the view;
   - a product without AI features gets no headline;
   - floor rather than rounding in dimension levels.
4. **Field test:**
   - provisionally score all 11 products on AIR-01 to AIR-08, the three facts and the 13 AI-qualified readings;
   - every result labelled single-rater until independently reviewed.

## 9. Open questions for review

1. **Dimension level as the floor of the mean.** The alternative is weakest-check-within-dimension, which is stricter. Is the floor of the mean right, given that the headline already takes the weakest dimension?
2. **Default or opt-in.** Several products ship AI that is off by default (Discourse AI, LibreChat memory). Should the headline use the default configuration, consistent with SAL, with the opt-in reading shown beside it?
3. **Intelligence has no new checks.** It is built entirely from AI-qualified readings of existing criteria. Is that acceptable, or should it have a check of its own (for example, breadth of AI features across the product)?
4. **Gate cap at 2.** Same cap as SAL. Agreed?
