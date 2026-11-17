# OpenClaw: the next three moves

**Do this first.** Give the assistant's memory and persona a real undo. Dreaming is on by default and rewrites what the assistant remembers, and the workspace is never committed, so a bad rewrite cannot be reversed. Commit the workspace on each change and expose restore, as skill collections already have. Level 3 is a longer programme: about fifteen changes, led by undo and tested restore.

From the EVOLVE assessment of 2026-09-30 (github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 2 (Assisted) · Proven: not evidenced · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 3, Supervised. The product carries a change from start to finish, including checks, release to a small group of users first and undo, and every safety gate passes.

**With all three moves the product still reads Level 2.** The rest of the way to Level 3, in order: Notices where users struggle; Works out why a problem happens; Ranked suggestions for change, with evidence; Automatic checks before any change lands; Release to a small group first; Undo for a new version of the code; Safe changes to how data is stored; Backups that are proven to restore; Self-made changes tested before use; Firm limits on self-made changes; Have the product draft "What the assistant remembers and how it presents itself" changes; Have the product carry "What the assistant knows how to do (skills)" changes end to end.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Let the person running the assistant change "What the assistant remembers and how it presents itself" themselves, with undo** (For the people running it) | The people running the product make this kind of change themselves, without a release, and can undo it. | 2 | Share of "What the assistant remembers and how it presents itself" changes made without an engineer, days from request to live, and engineer tickets for it per month. |
| 2 | **Requests become clear change plans** (For the loop) | It can answer yes to: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk? | 2 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 2 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Let the person running the assistant change "What the assistant remembers and how it presents itself" themselves, with undo

*For the people running it.*

**Today.** Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.

**What users get.** The people running the product make this kind of change themselves, without a release, and can undo it. Made by: the person running the assistant.

**Evidence.** Memory and persona files (MEMORY.md, SOUL.md, AGENTS.md in the workspace) change in chat and through dreaming, which is on by default (docs/concepts/dreaming.md). No supported undo: the workspace is only `git init`-ed at creation and never committed (src/agents/workspace.ts:682-708); dreaming keeps MEMORY.md preimages in plugin state but offers no restore command; `memory forget` deletes by source session, it does not revert (docs/cli/memory.md). Reach 0 because the path has no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.

**Track in real use.** Share of "What the assistant remembers and how it presents itself" changes made without an engineer, days from request to live, and engineer tickets for it per month.

**Done when:**

- [ ] The person running the assistant can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- [ ] They make one such change and then undo it, and the earlier behaviour is back.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "What the assistant remembers and how it presents itself" at reach 1 (Self-serve).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main). Read the code before changing it.
Goal for users: The people running the product make this kind of change themselves, without a release, and can undo it.
Today: Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
Where it stands in the code (from the assessment): Memory and persona files (MEMORY.md, SOUL.md, AGENTS.md in the workspace) change in chat and through dreaming, which is on by default (docs/concepts/dreaming.md). No supported undo: the workspace is only `git init`-ed at creation and never committed (src/agents/workspace.ts:682-708); dreaming keeps MEMORY.md preimages in plugin state but offers no restore command; `memory forget` deletes by source session, it does not revert (docs/cli/memory.md). Reach 0 because the path has no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
Build a supported way for them to make it in the running product, and undo that restores the earlier behaviour, for this kind of change: What the assistant remembers and how it presents itself (made by the person running the assistant).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- The person running the assistant can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- They make one such change and then undo it, and the earlier behaviour is back.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "What the assistant remembers and how it presents itself" at reach 1 (Self-serve).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Requests become clear change plans

*For the loop.*

**Today.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**What users get.** It can answer yes to: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk?

**Why it matters.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**Evidence.** The /learn command turns a request into requirements and sources and stages a pending skill proposal for review, revising existing Workshop skills before creating new ones (src/skills/workshop/learn-prompt.ts). No acceptance criteria or risk class.

**Track in real use.** Share of requests captured as a plan a person confirmed, and days from request to release.

**Done when:**

- [ ] In the running product: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores DEL-01 at 3 or more: "The product turns a request into a change specification with acceptance criteria, impact on existing definitions and a risk class, which a person confirms."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main). Read the code before changing it.
Goal for users: It can answer yes to: does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk?
Today: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
Where it stands in the code (from the assessment): The /learn command turns a request into requirements and sources and stages a pending skill proposal for review, revising existing Workshop skills before creating new ones (src/skills/workshop/learn-prompt.ts). No acceptance criteria or risk class.
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

**Also failing for Level 3.** Undo for a new version of the code; Backups that are proven to restore; Safe changes to how data is stored; Limits and checks on changes the product makes to itself.

**Evidence.** Workshop skill collections are backed up and can be restored or rolled back with revision hashes (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); configuration has rotating backups and recovery (src/config/backup-rotation.ts, recovery-policy.ts) but no operator rollback with diffs. Under the inventory rule a 3 needs every default surface at 3.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/openclaw/openclaw @ df2a29cac9ad37c31a0f5a0d977ba3e4fd833cb0 (main). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Workshop skill collections are backed up and can be restored or rolled back with revision hashes (src/skills/workshop/collection-backup.ts, collection-restore.ts, collection-rollback.ts); configuration has rotating backups and recovery (src/config/backup-rotation.ts, recovery-policy.ts) but no operator rollback with diffs. Under the inventory rule a 3 needs every default surface at 3.
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

After the three moves, the rest of the way to Level 3: `LRN-03` 2 → 3; `LRN-05` 2 → 3; `LRN-06` 2 → 3; `DEL-05` 2 → 3; `DEL-09` 1 → 2; `DEL-11` 2 → 3; `ARC-02` 2 → 3; `ARC-09` 2 → 3; `LRN-08` 1 → 2; `GOV-10` 2 → 3; `memory-persona` 1 → 2; `skills` 2 → 3.

1. Change kind `memory-persona` reach 0 → 1.
2. `DEL-01` 2 → 3 (request loop, Intake).
3. `GOV-05` 2 → 3 (request loop, Roll back, control: Definition rollback).
