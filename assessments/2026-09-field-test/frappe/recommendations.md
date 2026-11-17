# Frappe Framework: the next three moves

**Do this first.** Frappe already lets system managers change forms, workflows, permissions and reports themselves, with history. The next level is the product helping: capture a change request inside Desk and draft the customisation for a person to finish. Add revert-to-version for definitions, which Version records already make possible, and the three moves reach Level 2.

From the EVOLVE assessment of 2026-09-30 (github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product reads Level 2**, checked by re-running the scorer with each move landed.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Have the product draft "Record types, fields and form layouts" changes** (For the people running it) | The product drafts this kind of change, and a person completes and releases it. | 1 | Share of "Record types, fields and form layouts" changes that start from the product's own draft or build, how much people edit them, and days from request to live. |
| 2 | **Requests become clear change plans** (For the loop) | A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved. | 1 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 1 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Have the product draft "Record types, fields and form layouts" changes

*For the people running it.*

**Today.** Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.

**What users get.** The product drafts this kind of change, and a person completes and releases it. Made by: system managers.

**Next in line.** Approval workflows, notifications and automation rules; Who can see and change what (roles and permissions); Reports and printed documents.

**Evidence.** Custom DocTypes, Custom Fields and Customize Form changes are made in Desk with no deploy (frappe/core/doctype/doctype/doctype.py:329-340, 539-546; frappe/custom/doctype/customize_form). Undo: DocType, Custom Field and Property Setter track changes, so every change keeps a Version with the earlier values (their .json: track_changes 1); Customize Form resets a form's layout or all its customisations (customize_form.py:635-660, 692-712); deleted documents can be restored for 180 days (frappe/core/doctype/deleted_document/deleted_document.py:32-70). No one-step revert to an earlier version (GOV-05 is 2), so undo is by hand from the recorded history.

**Track in real use.** Share of "Record types, fields and form layouts" changes that start from the product's own draft or build, how much people edit them, and days from request to live.

**Done when:**

- [ ] System managers can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- [ ] A person can stop, edit or reject what the product prepared, and undo it after release.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Record types, fields and form layouts" at reach 2 (Drafted).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop). Read the code before changing it.
Goal for users: The product drafts this kind of change, and a person completes and releases it.
Today: Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.
Where it stands in the code (from the assessment): Custom DocTypes, Custom Fields and Customize Form changes are made in Desk with no deploy (frappe/core/doctype/doctype/doctype.py:329-340, 539-546; frappe/custom/doctype/customize_form). Undo: DocType, Custom Field and Property Setter track changes, so every change keeps a Version with the earlier values (their .json: track_changes 1); Customize Form resets a form's layout or all its customisations (customize_form.py:635-660, 692-712); deleted documents can be restored for 180 days (frappe/core/doctype/deleted_document/deleted_document.py:32-70). No one-step revert to an earlier version (GOV-05 is 2), so undo is by hand from the recorded history.
Build the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it, for this kind of change: Record types, fields and form layouts (made by system managers).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- System managers can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- A person can stop, edit or reject what the product prepared, and undo it after release.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Record types, fields and form layouts" at reach 2 (Drafted).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Requests become clear change plans

*For the loop.*

**Today.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**What users get.** A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.

**Why it matters.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**Evidence.** No request or feature-request object for changing the product was found; requests live outside it.

**Track in real use.** Share of requests captured as a plan a person confirmed, and days from request to release.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- [ ] A fresh assessment scores DEL-01 at 2 or more: "Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop). Read the code before changing it.
Goal for users: A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
Today: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
Where it stands in the code (from the assessment): No request or feature-request object for changing the product was found; requests live outside it.
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

**Also failing for Level 3.** Backups that are proven to restore; Security checks built into every change; Safe changes to how data is stored; Customer organisations kept apart.

**Evidence.** Document changes are versioned with diffs (Version, Audit Trail); deleted documents can be restored (frappe/core/doctype/deleted_document/deleted_document.py:43). No revert-to-version for definitions, layouts or configuration.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/frappe/frappe @ 82b0384810030c8d347780538821a3b006375d28 (develop). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Document changes are versioned with diffs (Version, Audit Trail); deleted documents can be restored (frappe/core/doctype/deleted_document/deleted_document.py:43). No revert-to-version for definitions, layouts or configuration.
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

1. Change kind `forms-fields` reach 1 → 2.
2. `DEL-01` 0 → 2 (request loop, Intake).
3. `GOV-05` 2 → 3 (request loop, Roll back, control: Definition rollback).
