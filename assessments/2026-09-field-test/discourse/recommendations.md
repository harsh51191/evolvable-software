# Discourse: the next three moves

**Do this first.** Discourse is the best-governed product here for people making changes by hand: settings and text keep their old values and can be reverted. What it lacks is the product helping: no draft of a settings or text change from a request. Turning a top-voted feature topic into a drafted settings change is the move that takes it to Level 2, and the three moves together get there.

From the EVOLVE assessment of 2026-09-30 (github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L0 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product reads Level 2**, checked by re-running the scorer with each move landed.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Have the product draft "How the forum behaves and what it says (settings and wording)" changes** (For the people running it) | The product drafts this kind of change, and a person completes and releases it. | 1 | Share of "How the forum behaves and what it says (settings and wording)" changes that start from the product's own draft or build, how much people edit them, and days from request to live. |
| 2 | **Requests become clear change plans** (For the loop) | A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved. | 1 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 1 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Have the product draft "How the forum behaves and what it says (settings and wording)" changes

*For the people running it.*

**Today.** Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.

**What users get.** The product drafts this kind of change, and a person completes and releases it. Made by: site admins.

**Next in line.** Categories and who can see or post in them; Look and layout (themes and components).

**Evidence.** Admins change typed, validated site settings and override any interface text in the admin UI with no deploy. Undo: every setting change is logged with its previous and new value (app/services/staff_action_logger.rb:280-296), a setting can be reset to its default, and text overrides log old and new text (:513) and can be reverted to the default; there is no one-step revert to an earlier value, so undo is setting the logged value back.

**Track in real use.** Share of "How the forum behaves and what it says (settings and wording)" changes that start from the product's own draft or build, how much people edit them, and days from request to live.

**Done when:**

- [ ] Site admins can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- [ ] A person can stop, edit or reject what the product prepared, and undo it after release.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "How the forum behaves and what it says (settings and wording)" at reach 2 (Drafted).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main). Read the code before changing it.
Goal for users: The product drafts this kind of change, and a person completes and releases it.
Today: Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.
Where it stands in the code (from the assessment): Admins change typed, validated site settings and override any interface text in the admin UI with no deploy. Undo: every setting change is logged with its previous and new value (app/services/staff_action_logger.rb:280-296), a setting can be reset to its default, and text overrides log old and new text (:513) and can be reverted to the default; there is no one-step revert to an earlier value, so undo is setting the logged value back.
Build the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it, for this kind of change: How the forum behaves and what it says (settings and wording) (made by site admins).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Site admins can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- A person can stop, edit or reject what the product prepared, and undo it after release.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "How the forum behaves and what it says (settings and wording)" at reach 2 (Drafted).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Requests become clear change plans

*For the loop.*

**Today.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**What users get.** A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.

**Why it matters.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**Evidence.** Communities collect requests as topics; the bundled topic-voting plugin ranks them (plugins/discourse-topic-voting). They are not linked to the settings or screens involved.

**Track in real use.** Share of requests captured as a plan a person confirmed, and days from request to release.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- [ ] A fresh assessment scores DEL-01 at 2 or more: "Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main). Read the code before changing it.
Goal for users: A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
Today: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
Where it stands in the code (from the assessment): Communities collect requests as topics; the bundled topic-voting plugin ranks them (plugins/discourse-topic-voting). They are not linked to the settings or screens involved.
Raise this to: Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Shown on a demo or test installation, or in the product's own documentation: Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- A fresh assessment scores DEL-01 at 2 or more: "Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved."
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

**Also failing for Level 3.** Backups that are proven to restore; Security checks built into every change; Customer organisations kept apart.

**Evidence.** Site-setting history in staff logs, revertible post revisions, versioned published workflows (workflow_snapshot.rb) and git-backed remote themes; no admin rollback for settings or themes.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/discourse/discourse @ 2590ea9db1b7c38dcf80298aefd3e7cb3afe1f2b (main). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Site-setting history in staff logs, revertible post revisions, versioned published workflows (workflow_snapshot.rb) and git-backed remote themes; no admin rollback for settings or themes.
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

1. Change kind `site-settings` reach 1 → 2.
2. `DEL-01` 1 → 2 (request loop, Intake).
3. `GOV-05` 2 → 3 (request loop, Roll back, control: Definition rollback).
