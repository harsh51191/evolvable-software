# n8n: the next three moves

**Do this first.** n8n's AI already drafts workflows, which is why it leads at Level 2. Level 3 is a programme, not a step: it needs about fourteen changes. Start with what hurts users most: credentials have no history and deletion is permanent, so a wrong edit breaks every workflow that uses it. Give credentials versions and restore, as workflows already have, and extend undo to variables, data tables and settings.

From the EVOLVE assessment of 2026-09-30 (github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 2 (Assisted) · Proven: not evidenced · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 3, Supervised. The product carries a change from start to finish, including checks, release to a small group of users first and undo, and every safety gate passes.

**With all three moves the product still reads Level 2.** The rest of the way to Level 3, in order: Notices where users struggle; Works out why a problem happens; Ranked suggestions for change, with evidence; The product reports what is running; Safe changes to how data is stored; Customer organisations kept apart; Backups that are proven to restore; Security checks built into every change; Firm limits on self-made changes; Have the product draft "Connections to other services (credentials)" changes; Have the product carry "Automations: workflows and their steps" changes end to end.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Let workflow builders and instance admins change "Connections to other services (credentials)" themselves, with undo** (For the people running it) | The people running the product make this kind of change themselves, without a release, and can undo it. | 2 | Share of "Connections to other services (credentials)" changes made without an engineer, days from request to live, and engineer tickets for it per month. |
| 2 | **Requests become clear change plans** (For the loop) | It can answer yes to: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk? | 2 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 2 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Let workflow builders and instance admins change "Connections to other services (credentials)" themselves, with undo

*For the people running it.*

**Today.** Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.

**What users get.** The people running the product make this kind of change themselves, without a release, and can undo it. Made by: workflow builders and instance admins.

**Evidence.** Created and edited in the UI with no deploy (packages/cli/src/credentials/credentials.controller.ts:217, 264), but there is no history of earlier values and deletion is permanent (credentials.controller.ts:479); source control carries credential stubs without secrets. A path without undo is reach 0.

**Track in real use.** Share of "Connections to other services (credentials)" changes made without an engineer, days from request to live, and engineer tickets for it per month.

**Done when:**

- [ ] Workflow builders and instance admins can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- [ ] They make one such change and then undo it, and the earlier behaviour is back.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Connections to other services (credentials)" at reach 1 (Self-serve).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master). Read the code before changing it.
Goal for users: The people running the product make this kind of change themselves, without a release, and can undo it.
Today: Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
Where it stands in the code (from the assessment): Created and edited in the UI with no deploy (packages/cli/src/credentials/credentials.controller.ts:217, 264), but there is no history of earlier values and deletion is permanent (credentials.controller.ts:479); source control carries credential stubs without secrets. A path without undo is reach 0.
Build a supported way for them to make it in the running product, and undo that restores the earlier behaviour, for this kind of change: Connections to other services (credentials) (made by workflow builders and instance admins).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Workflow builders and instance admins can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- They make one such change and then undo it, and the earlier behaviour is back.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Connections to other services (credentials)" at reach 1 (Self-serve).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Requests become clear change plans

*For the loop.*

**Today.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**What users get.** It can answer yes to: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk?

**Why it matters.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**Evidence.** The AI workflow builder plans before building: it asks typed clarifying questions and produces a plan with a trigger, steps, suggested nodes and specifications that the user approves (packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts, agents/planner.agent.ts). The plan has no acceptance criteria or risk class.

**Track in real use.** Share of requests captured as a plan a person confirmed, and days from request to release.

**Done when:**

- [ ] In the running product: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores DEL-01 at 3 or more: "The product turns a request into a change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master). Read the code before changing it.
Goal for users: It can answer yes to: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk?
Today: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
Where it stands in the code (from the assessment): The AI workflow builder plans before building: it asks typed clarifying questions and produces a plan with a trigger, steps, suggested nodes and specifications that the user approves (packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts, agents/planner.agent.ts). The plan has no acceptance criteria or risk class.
Raise this to: The product turns a request into a change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms.
A known way to get there: Capture requests in the product with structure, and turn each into a change specification with acceptance criteria, affected definitions and a risk class for a person to confirm.
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- In the running product: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk? Yes, shown on a demo or test installation.
- A fresh assessment scores DEL-01 at 3 or more: "The product turns a request into a change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms."
- It is on in the standard installation, with no optional setting or extra licence needed.
- An automated test performs the check and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 3. Undo for every change people and AI make in the product

*For safety.*

**Today.** Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.

**What users get.** It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?

**Why it matters.** Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand.

**Also failing for Level 3.** Backups that are proven to restore; Security checks built into every change; Safe changes to how data is stored; Limits and checks on changes the product makes to itself; Customer organisations kept apart.

**Evidence.** Workflow history with versions and restore (packages/cli/src/workflows/workflow-history); other surfaces (credentials, variables, data tables, settings) roll back only through source control. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Credentials, variables, data tables and settings roll back only through source control.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/n8n-io/n8n @ c17c48043eb1080e5ae9795ea3a384960f8748f1 (master). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Workflow history with versions and restore (packages/cli/src/workflows/workflow-history); other surfaces (credentials, variables, data tables, settings) roll back only through source control. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Credentials, variables, data tables and settings roll back only through source control.
Raise this to: The operator sees history and diffs, and rolls back, across all customisation surfaces.
A known way to get there: Version every customisation surface (definitions, layouts, text, theme, config) with history, diff and rollback in the admin UI.
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- It is on in the standard installation, with no optional setting or extra licence needed.
- An automated test performs the check and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## For engineers

After the three moves, the rest of the way to Level 3: `LRN-03` 2 → 3; `LRN-05` 2 → 3; `LRN-06` 2 → 3; `DEL-06` 2 → 3; `ARC-02` 2 → 3; `ARC-05` 2 → 3; `ARC-09` 2 → 3; `GOV-04` 2 → 3; `GOV-10` 2 → 3; `credentials` 1 → 2; `workflows` 2 → 3.

1. Change kind `credentials` reach 0 → 1.
2. `DEL-01` 2 → 3 (request loop, Intake).
3. `GOV-05` 2 → 3 (request loop, Roll back, control: Definition rollback).
