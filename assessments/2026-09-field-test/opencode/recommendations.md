# OpenCode: the next three moves

**Do this first.** OpenCode's own agents and commands are files the user must version in their own git; the agent generator writes outside any session, so its output cannot be reverted. Give agent and command changes a history with undo inside OpenCode. That is what Level 1 needs, and the first move alone does not reach it because undo for its own definitions (move 3) is also required.

From the EVOLVE assessment of 2026-09-30 (github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 0 (Manual) · Proven: not evidenced · AI-driven 0 · Request → Release L0 (AI L0) · Issue → Fix L0 (AI L0) · Opportunity → Expansion L0 (AI L0)

**Next level:** 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.

**With all three moves the product reads Level 1**, checked by re-running the scorer with each move landed.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Let the developer using OpenCode change "Custom agents and commands" themselves, with undo** (For the people running it) | The people running the product make this kind of change themselves, without a release, and can undo it. | 0 | Share of "Custom agents and commands" changes made without an engineer, days from request to live, and engineer tickets for it per month. |
| 2 | **Notices where users struggle** (For the loop) | A first step towards "notices where users struggle": user-facing errors and failed actions recorded with the product area and queryable. | 0 | Share of user-visible failures the product records with the part involved, and time to notice them. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | A first step towards "history and undo for every setting": versioning for some surfaces, or without a rollback UI. | 0 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Let the developer using OpenCode change "Custom agents and commands" themselves, with undo

*For the people running it.*

**Today.** Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.

**What users get.** The people running the product make this kind of change themselves, without a release, and can undo it. Made by: the developer using OpenCode.

**Evidence.** Markdown or JSON files in .opencode or the global config (packages/opencode/src/config/agent.ts, command.ts); `opencode agent create` drafts an agent with the model (cli/cmd/agent.ts). No supported undo: the files are versioned only by the user's own git (GOV-05 1), and the generator writes outside any session, so session revert does not cover it. Reach 0 because the path has no undo; the AI draft would otherwise read as reach 2, which DEL-04 1 would not support.

**Track in real use.** Share of "Custom agents and commands" changes made without an engineer, days from request to live, and engineer tickets for it per month.

**Done when:**

- [ ] The developer using OpenCode can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- [ ] They make one such change and then undo it, and the earlier behaviour is back.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Custom agents and commands" at reach 1 (Self-serve).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev). Read the code before changing it.
Goal for users: The people running the product make this kind of change themselves, without a release, and can undo it.
Today: Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
Where it stands in the code (from the assessment): Markdown or JSON files in .opencode or the global config (packages/opencode/src/config/agent.ts, command.ts); `opencode agent create` drafts an agent with the model (cli/cmd/agent.ts). No supported undo: the files are versioned only by the user's own git (GOV-05 1), and the generator writes outside any session, so session revert does not cover it. Reach 0 because the path has no undo; the AI draft would otherwise read as reach 2, which DEL-04 1 would not support.
Build a supported way for them to make it in the running product, and undo that restores the earlier behaviour, for this kind of change: Custom agents and commands (made by the developer using OpenCode).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- The developer using OpenCode can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- They make one such change and then undo it, and the earlier behaviour is back.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Custom agents and commands" at reach 1 (Self-serve).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Notices where users struggle

*For the loop.*

**Today.** The product does not yet notice and raise, by itself, the places where users struggle.

**What users get.** A first step towards "notices where users struggle": user-facing errors and failed actions recorded with the product area and queryable.

**Why it matters.** The product does not yet notice and raise, by itself, the places where users struggle.

Move 1 alone gives the next level; this is what then holds the loop at Level 1.

**Evidence.** Logs for engineers.

**Track in real use.** Share of user-visible failures the product records with the part involved, and time to notice them.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: User-facing errors and failed actions recorded with the product area and queryable.
- [ ] A fresh assessment scores LRN-03 at 2 or more: "User-facing errors and failed actions recorded with the product area and queryable."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev). Read the code before changing it.
Goal for users: A first step towards "notices where users struggle": user-facing errors and failed actions recorded with the product area and queryable.
Today: The product does not yet notice and raise, by itself, the places where users struggle.
Where it stands in the code (from the assessment): Logs for engineers.
Raise this to: User-facing errors and failed actions recorded with the product area and queryable.
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Shown on a demo or test installation, or in the product's own documentation: User-facing errors and failed actions recorded with the product area and queryable.
- A fresh assessment scores LRN-03 at 2 or more: "User-facing errors and failed actions recorded with the product area and queryable."
- It is on in the standard installation, with no optional setting or extra licence needed.
- An automated test performs the check and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 3. Undo for every change people and AI make in the product

*For safety.*

**Today.** Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.

**What users get.** A first step towards "history and undo for every setting": versioning for some surfaces, or without a rollback UI.

**Why it matters.** Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand.

**Evidence.** Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Versioning for some surfaces, or without a rollback UI.
- [ ] A fresh assessment scores GOV-05 at 2 or more: "Versioning for some surfaces, or without a rollback UI."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/anomalyco/opencode @ 2fa3363c924c5c3e367b84a87ae478296a0ed59b (dev). Read the code before changing it.
Goal for users: A first step towards "history and undo for every setting": versioning for some surfaces, or without a rollback UI.
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Agents, commands, themes and configuration are files versioned only by the user's own git. Git snapshots with session revert roll back the agent's edits to the user's code (packages/opencode/src/snapshot, session/revert.ts), not OpenCode's own definitions.
Raise this to: Versioning for some surfaces, or without a rollback UI.
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Shown on a demo or test installation, or in the product's own documentation: Versioning for some surfaces, or without a rollback UI.
- A fresh assessment scores GOV-05 at 2 or more: "Versioning for some surfaces, or without a rollback UI."
- It is on in the standard installation, with no optional setting or extra licence needed.
- An automated test performs the check and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## For engineers

1. Change kind `agents-commands` reach 0 → 1.
2. `LRN-03` 1 → 2 (fix loop, Detect).
3. `GOV-05` 1 → 2 (request loop, Roll back, control: Definition rollback).
