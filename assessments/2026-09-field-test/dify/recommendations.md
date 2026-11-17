# Dify: the next three moves

**Do this first.** Start with safety, not features: Dify ships no supported backup for its database, uploaded files or vector store, so one lost volume erases every app and knowledge base. A documented backup and restore command is small work and is required for Level 2. Then make knowledge edits reversible and drafted: builders already upload and re-index documents themselves, but chunk and retrieval edits keep no history.

From the EVOLVE assessment of 2026-09-30 (github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product still reads Level 1.** The rest of the way to Level 2, in order: Requests become clear change plans; Ranked suggestions for change, with evidence; Known limits, tested regularly.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Have the product draft "Knowledge the apps answer from" changes** (For the people running it) | The product drafts this kind of change, and a person completes and releases it. | 1 | Share of "Knowledge the apps answer from" changes that start from the product's own draft or build, how much people edit them, and days from request to live. |
| 2 | **Works out why a problem happens** (For the loop) | A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes). | 1 | Time from a problem being recorded to its cause being known. |
| 3 | **Backups that are proven to restore** (For safety) | A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves. | 1 | A restore drill passing on a schedule, and the time it takes. |

## 1. Have the product draft "Knowledge the apps answer from" changes

*For the people running it.*

**Today.** Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.

**What users get.** The product drafts this kind of change, and a person completes and releases it. Made by: app builders and knowledge owners.

**Evidence.** Builders upload, sync and re-index documents and set retrieval in the console with no deploy. Undo: documents can be disabled, re-enabled, archived and un-archived (api/controllers/console/datasets/datasets_document.py:731) or deleted; edits to chunks and retrieval settings keep no history.

**Track in real use.** Share of "Knowledge the apps answer from" changes that start from the product's own draft or build, how much people edit them, and days from request to live.

**Done when:**

- [ ] App builders and knowledge owners can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- [ ] A person can stop, edit or reject what the product prepared, and undo it after release.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Knowledge the apps answer from" at reach 2 (Drafted).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main). Read the code before changing it.
Goal for users: The product drafts this kind of change, and a person completes and releases it.
Today: Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it.
Where it stands in the code (from the assessment): Builders upload, sync and re-index documents and set retrieval in the console with no deploy. Undo: documents can be disabled, re-enabled, archived and un-archived (api/controllers/console/datasets/datasets_document.py:731) or deleted; edits to chunks and retrieval settings keep no history.
Build the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it, for this kind of change: Knowledge the apps answer from (made by app builders and knowledge owners).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- App builders and knowledge owners can do this in the running product: the product drafting this change on request (an AI or rule-based lane, DEL-04 2), with a person finishing it.
- A person can stop, edit or reject what the product prepared, and undo it after release.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Knowledge the apps answer from" at reach 2 (Drafted).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Works out why a problem happens

*For the loop.*

**Today.** The product reports problems but does not work out their likely cause, so people have to investigate each one.

**What users get.** A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes).

**Why it matters.** The product reports problems but does not work out their likely cause, so people have to investigate each one.

**Evidence.** Run traces show node-level errors per run; there is no grouping.

**Track in real use.** Time from a problem being recorded to its cause being known.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: The product groups related failures and attaches context (traces, inputs, recent changes).
- [ ] A fresh assessment scores LRN-05 at 2 or more: "The product groups related failures and attaches context (traces, inputs, recent changes)."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main). Read the code before changing it.
Goal for users: A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes).
Today: The product reports problems but does not work out their likely cause, so people have to investigate each one.
Where it stands in the code (from the assessment): Run traces show node-level errors per run; there is no grouping.
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

## 3. Backups that are proven to restore

*For safety.*

**Today.** Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs.

**What users get.** A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves.

**Why it matters.** Without it, a mistake that undo cannot reach is permanent, because nobody knows whether the backup works.

**Evidence.** Corrected from 1 after the second-rating study. No supported backup or restore of the database, uploaded files or vector store, and no repository documentation telling operators to back them up: searched api/commands, docker/README.md, docs/, README.md and every *.md, *.sh and *.yaml for backup. The only backup is of the .env file before an env sync (docker/dify-env-sync.sh:82-97, docker/README.md:72-80); the app …

**Track in real use.** A restore drill passing on a schedule, and the time it takes.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Documentation tells operators to back up the database themselves.
- [ ] A fresh assessment scores ARC-09 at 1 or more: "Documentation tells operators to back up the database themselves."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/langgenius/dify @ ea38e484b81b4104736d2484aaa1d0d7ea99627e (main). Read the code before changing it.
Goal for users: A first step towards "backups that are proven to restore": documentation tells operators to back up the database themselves.
Today: Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs.
Where it stands in the code (from the assessment): Corrected from 1 after the second-rating study. No supported backup or restore of the database, uploaded files or vector store, and no repository documentation telling operators to back them up: searched api/commands, docker/README.md, docs/, README.md and every *.md, *.sh and *.yaml for backup. The only backup is of the .env file before an env sync (docker/dify-env-sync.sh:82-97, docker/README.md:72-80); the app …
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

After the three moves, the rest of the way to Level 2: `DEL-01` 0 → 2; `LRN-06` 1 → 2; `ARC-06` 0 → 1.

1. Change kind `knowledge` reach 1 → 2.
2. `LRN-05` 1 → 2 (fix loop, Diagnose).
3. `ARC-09` 0 → 1 (request loop, Foundation, control: Tested backup and restore).
