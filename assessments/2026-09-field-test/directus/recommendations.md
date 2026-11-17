# Directus: the next three moves

**Do this first.** Make data-model changes undoable. Admins already change collections, fields and relations in the Data Model screen, and the AI assistant drafts them, but no change keeps its prior state, so a wrong field change cannot be reversed in the product. That one gap is what users feel. Pair it with a supported backup, which Directus does not ship today.

From the EVOLVE assessment of 2026-09-30 (github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product still reads Level 1.** The rest of the way to Level 2, in order: Works out why a problem happens; Ranked suggestions for change, with evidence; Known limits, tested regularly.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Let project admins change "What data is kept (collections and fields)" themselves, with undo** (For the people running it) | The people running the product make this kind of change themselves, without a release, and can undo it. | 1 | Share of "What data is kept (collections and fields)" changes made without an engineer, days from request to live, and engineer tickets for it per month. |
| 2 | **Requests become clear change plans** (For the loop) | A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved. | 1 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Backups that are proven to restore** (For safety) | A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves. | 1 | A restore drill passing on a schedule, and the time it takes. |

## 1. Let project admins change "What data is kept (collections and fields)" themselves, with undo

*For the people running it.*

**Today.** Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.

**What users get.** The people running the product make this kind of change themselves, without a release, and can undo it. Made by: project admins.

**Evidence.** Admins create and change collections, fields and relations in the Data Model UI with no deploy (api/src/services/collections.ts, fields.ts), and the AI assistant drafts them behind per-call approval (api/src/ai/tools/collections, fields, relations; registry.ts:198-214). But there is no undo: schema changes record no prior state and have no rollback in the UI (GOV-05), deleting or retyping a field drops data, and schema snapshot, diff and apply (api/src/controllers/schema.ts) is an engineer flow between instances. Only an addition can be reversed, by deleting it. A path without undo is reach 0.

**Track in real use.** Share of "What data is kept (collections and fields)" changes made without an engineer, days from request to live, and engineer tickets for it per month.

**Done when:**

- [ ] Project admins can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- [ ] They make one such change and then undo it, and the earlier behaviour is back.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "What data is kept (collections and fields)" at reach 1 (Self-serve).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main). Read the code before changing it.
Goal for users: The people running the product make this kind of change themselves, without a release, and can undo it.
Today: Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
Where it stands in the code (from the assessment): Admins create and change collections, fields and relations in the Data Model UI with no deploy (api/src/services/collections.ts, fields.ts), and the AI assistant drafts them behind per-call approval (api/src/ai/tools/collections, fields, relations; registry.ts:198-214). But there is no undo: schema changes record no prior state and have no rollback in the UI (GOV-05), deleting or retyping a field drops data, and schema snapshot, diff and apply (api/src/controllers/schema.ts) is an engineer flow between instances. Only an addition can be reversed, by deleting it. A path without undo is reach 0.
Build a supported way for them to make it in the running product, and undo that restores the earlier behaviour, for this kind of change: What data is kept (collections and fields) (made by project admins).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Project admins can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- They make one such change and then undo it, and the earlier behaviour is back.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "What data is kept (collections and fields)" at reach 1 (Self-serve).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Requests become clear change plans

*For the loop.*

**Today.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**What users get.** A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.

**Why it matters.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**Evidence.** Requests reach the AI assistant as free-text chat (api/src/ai/chat); nothing structures them into a specification.

**Track in real use.** Share of requests captured as a plan a person confirmed, and days from request to release.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- [ ] A fresh assessment scores DEL-01 at 2 or more: "Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main). Read the code before changing it.
Goal for users: A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
Today: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
Where it stands in the code (from the assessment): Requests reach the AI assistant as free-text chat (api/src/ai/chat); nothing structures them into a specification.
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

**Evidence.** Corrected from 1 to 0 at the v0.7 migration, applying the anchor as the second rating did for Dify: level 1 needs documentation telling operators to back up, and this repository has none. No backup or restore command or feature for the database, files or settings; searched every file outside node_modules for 'backup' and 'back up' (only icon names in app/src). Schema snapshot and apply move the data model, not data …

**Track in real use.** A restore drill passing on a schedule, and the time it takes.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Documentation tells operators to back up the database themselves.
- [ ] A fresh assessment scores ARC-09 at 1 or more: "Documentation tells operators to back up the database themselves."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/directus/directus @ 2878b4ef8ea9c1d09201debe89b3a5dc1d0bf93a (main). Read the code before changing it.
Goal for users: A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves.
Today: Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs.
Where it stands in the code (from the assessment): Corrected from 1 to 0 at the v0.7 migration, applying the anchor as the second rating did for Dify: level 1 needs documentation telling operators to back up, and this repository has none. No backup or restore command or feature for the database, files or settings; searched every file outside node_modules for 'backup' and 'back up' (only icon names in app/src). Schema snapshot and apply move the data model, not data …
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

After the three moves, the rest of the way to Level 2: `LRN-05` 1 → 2; `LRN-06` 0 → 2; `ARC-06` 0 → 1.

1. Change kind `data-model` reach 0 → 1.
2. `DEL-01` 1 → 2 (request loop, Intake).
3. `ARC-09` 0 → 1 (request loop, Foundation, control: Tested backup and restore).
