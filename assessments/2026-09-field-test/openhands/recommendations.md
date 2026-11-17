# OpenHands (Agent Canvas + software-agent-sdk): the next three moves

**Do this first.** Ship a supported backup for the automation service, and then let the agent draft automations from a request with a test run before they go live. Today automations are created from templates or chat and validated, but no backup exists and nothing turns a request into a plan. Level 2 also needs fix proposals and known capacity limits, listed below.

From the EVOLVE assessment of 2026-09-30 (github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product still reads Level 1.** The rest of the way to Level 2, in order: Ranked suggestions for change, with evidence; Known limits, tested regularly.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Have the product draft "Scheduled and event-driven automations" changes** (For the people running it) | The product drafts this kind of change, and a person completes and releases it. | 1 | Share of "Scheduled and event-driven automations" changes that start from the product's own draft or build, how much people edit them, and days from request to live. |
| 2 | **Requests become clear change plans** (For the loop) | A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved. | 1 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Backups that are proven to restore** (For safety) | A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves. | 1 | A restore drill passing on a schedule, and the time it takes. |

## 1. Have the product draft "Scheduled and event-driven automations" changes

*For the people running it.*

**Today.** Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.

**What users get.** The product drafts this kind of change, and a person completes and releases it. Made by: users and organisation admins.

**Next in line.** Skills, plugins and tool servers the agent uses; Which models it uses and how the agent behaves.

**Evidence.** Created from templates or the setup UI, where drafts are validated and materialised disabled until a test run (OpenHands src/routes/automation-setup-route.tsx, automation-templates.tsx; automation repository: draft_router.py), or by the agent in chat (create-instructions.tsx:58-61). Changed, disabled and deleted through the API and UI (router.py PATCH and DELETE /{automation_id}, lines 325 and 481). Undo is disabling or deleting; edits keep no earlier version unless git sync is set up (src/routes/automation-git-sync.tsx). Reach 1, not 2: the agent drafts automations, but DEL-04 is 1 under the self rule, so the criteria do not support reach 2. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.

**Track in real use.** Share of "Scheduled and event-driven automations" changes that start from the product's own draft or build, how much people edit them, and days from request to live.

**Done when:**

- [ ] Users and organisation admins can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- [ ] A person can stop, edit or reject what the product prepared, and undo it after release.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Scheduled and event-driven automations" at reach 2 (Drafted).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30). Read the code before changing it.
Goal for users: The product drafts this kind of change, and a person completes and releases it.
Today: Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.
Where it stands in the code (from the assessment): Created from templates or the setup UI, where drafts are validated and materialised disabled until a test run (OpenHands src/routes/automation-setup-route.tsx, automation-templates.tsx; automation repository: draft_router.py), or by the agent in chat (create-instructions.tsx:58-61). Changed, disabled and deleted through the API and UI (router.py PATCH and DELETE /{automation_id}, lines 325 and 481). Undo is disabling or deleting; edits keep no earlier version unless git sync is set up (src/routes/automation-git-sync.tsx). Reach 1, not 2: the agent drafts automations, but DEL-04 is 1 under the self rule, so the criteria do not support reach 2. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
Build the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it, for this kind of change: Scheduled and event-driven automations (made by users and organisation admins).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Users and organisation admins can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- A person can stop, edit or reject what the product prepared, and undo it after release.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Scheduled and event-driven automations" at reach 2 (Drafted).
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
You are working in github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30). Read the code before changing it.
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

## 3. Backups that are proven to restore

*For safety.*

**Today.** Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs.

**What users get.** A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves.

**Why it matters.** Without it, a mistake that undo cannot reach is permanent, because nobody knows whether the backup works.

**Evidence.** No backup command or documented backup for the Automation Service database or storage.

**Track in real use.** A restore drill passing on a schedule, and the time it takes.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Documentation tells operators to back up the database themselves.
- [ ] A fresh assessment scores ARC-09 at 1 or more: "Documentation tells operators to back up the database themselves."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/OpenHands/OpenHands @ 21cc5c6170fe093c0fcd23ffc61949f4933e17b9 (main) + github.com/OpenHands/software-agent-sdk @ 5ffdd2933c51423e302f5ee5e5b66df0ad9cc28a (main) + github.com/OpenHands/automation @ ec4c5cc0cb05f3fb01816b36ff6271f6680b6675 (main, 2026-09-30). Read the code before changing it.
Goal for users: A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves.
Today: Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs.
Where it stands in the code (from the assessment): No backup command or documented backup for the Automation Service database or storage.
Raise this to: Documentation tells operators to back up the database themselves.
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Shown on a demo or test installation, or in the product's own documentation: Documentation tells operators to back up the database themselves.
- A fresh assessment scores ARC-09 at 1 or more: "Documentation tells operators to back up the database themselves."
- It is on in the standard installation, with no optional setting or extra licence needed.
- An automated test performs the check and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## For engineers

After the three moves, the rest of the way to Level 2: `LRN-06` 0 → 2; `ARC-06` 0 → 1.

1. Change kind `automations` reach 1 → 2.
2. `DEL-01` 0 → 2 (request loop, Intake).
3. `ARC-09` 0 → 1 (request loop, Foundation, control: Tested backup and restore).
