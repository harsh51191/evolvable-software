# PostHog: the next three moves

**Do this first.** PostHog's AI already drafts charts, dashboards and flags, and its activity log records before-and-after values. What holds it at Level 1 is the fix loop: errors are grouped, but nothing works out their likely cause. Explaining a grouped error with the recent change behind it reaches Level 2. Then make the activity log revertible across surfaces, which is the main gap before Level 3.

From the EVOLVE assessment of 2026-09-30 (github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product reads Level 2**, checked by re-running the scorer with each move landed.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Have the product carry "Charts, reports and dashboards" changes end to end** (For the people running it) | The product builds, checks and releases this kind of change from start to finish, and a person approves. | 1 | Share of "Charts, reports and dashboards" changes that start from the product's own draft or build, how much people edit them, and days from request to live. |
| 2 | **Works out why a problem happens** (For the loop) | A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes). | 2 | Time from a problem being recorded to its cause being known. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 1 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Have the product carry "Charts, reports and dashboards" changes end to end

*For the people running it.*

**Today.** Drafted. The product drafts this kind of change, and a person completes and releases it.

**What users get.** The product builds, checks and releases this kind of change from start to finish, and a person approves. Made by: product and growth teams in a project.

The next level does not need this; it prepares the build path for Level 3.

**Next in line.** Who sees which feature (feature flags).

**Evidence.** Members build insights and dashboards in the UI with live preview; PostHog AI drafts them on request (ee/hogai/tools/create_insight.py; ee/hogai/tools/upsert_dashboard/tool.py:116, with a confirmation preview for updates that remove insights at :125-139) and the member keeps or edits the result. Undo: a deleted dashboard and its tiles are restored through undo-delete (products/dashboards/backend/api/dashboard.py:2424, :2747; posthog/api/file_system/deletion.py), and edits are recorded in the activity log with before and after values; there is no one-step revert to an earlier version of a dashboard or insight, so undoing an edit means editing it back from the logged values. Reach 2 rests on DEL-04 2.

**Track in real use.** Share of "Charts, reports and dashboards" changes that start from the product's own draft or build, how much people edit them, and days from request to live.

**Done when:**

- [ ] Product and growth teams in a project can do this in the running product: the product building, checking and releasing this change end to end (DEL-04 3), with a person approving.
- [ ] A person can stop, edit or reject what the product prepared, and undo it after release.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Charts, reports and dashboards" at reach 3 (Carried).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master). Read the code before changing it.
Goal for users: The product builds, checks and releases this kind of change from start to finish, and a person approves.
Today: Drafted. The product drafts this kind of change, and a person completes and releases it.
Where it stands in the code (from the assessment): Members build insights and dashboards in the UI with live preview; PostHog AI drafts them on request (ee/hogai/tools/create_insight.py; ee/hogai/tools/upsert_dashboard/tool.py:116, with a confirmation preview for updates that remove insights at :125-139) and the member keeps or edits the result. Undo: a deleted dashboard and its tiles are restored through undo-delete (products/dashboards/backend/api/dashboard.py:2424, :2747; posthog/api/file_system/deletion.py), and edits are recorded in the activity log with before and after values; there is no one-step revert to an earlier version of a dashboard or insight, so undoing an edit means editing it back from the logged values. Reach 2 rests on DEL-04 2.
Build the product building, checking and releasing this change end to end (DEL-04 3), with a person approving, for this kind of change: Charts, reports and dashboards (made by product and growth teams in a project).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Product and growth teams in a project can do this in the running product: the product building, checking and releasing this change end to end (DEL-04 3), with a person approving.
- A person can stop, edit or reject what the product prepared, and undo it after release.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Charts, reports and dashboards" at reach 3 (Carried).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Works out why a problem happens

*For the loop.*

**Today.** The product reports problems but does not work out their likely cause, so people have to investigate each one.

**What users get.** A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes).

**Why it matters.** The product reports problems but does not work out their likely cause, so people have to investigate each one.

**Evidence.** Exceptions are grouped into issues with stack traces by the error tracking product used on itself.

**Track in real use.** Time from a problem being recorded to its cause being known.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: The product groups related failures and attaches context (traces, inputs, recent changes).
- [ ] A fresh assessment scores LRN-05 at 2 or more: "The product groups related failures and attaches context (traces, inputs, recent changes)."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master). Read the code before changing it.
Goal for users: A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes).
Today: The product reports problems but does not work out their likely cause, so people have to investigate each one.
Where it stands in the code (from the assessment): Exceptions are grouped into issues with stack traces by the error tracking product used on itself.
Raise this to: The product groups related failures and attaches context (traces, inputs, recent changes).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Shown on a demo or test installation, or in the product's own documentation: The product groups related failures and attaches context (traces, inputs, recent changes).
- A fresh assessment scores LRN-05 at 2 or more: "The product groups related failures and attaches context (traces, inputs, recent changes)."
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

The next level does not need it yet, but Level 3 does, and it is the control nearest to passing.

**Also failing for Level 3.** Backups that are proven to restore; Limits and checks on changes the product makes to itself; Customer organisations kept apart.

**Evidence.** The activity log records before-and-after changes for flags, insights, dashboards and more; no general revert across customisation surfaces. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Revert is not available across customisation surfaces.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/PostHog/posthog @ 645e1a78140757ea1bb9ddeb0ff9d3915c60b6f6 (master). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): The activity log records before-and-after changes for flags, insights, dashboards and more; no general revert across customisation surfaces. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Revert is not available across customisation surfaces.
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

1. Change kind `dashboards-insights` reach 2 → 3.
2. `LRN-05` 1 → 2 (fix loop, Diagnose).
3. `GOV-05` 2 → 3 (fix loop, Roll back, control: Definition rollback).
