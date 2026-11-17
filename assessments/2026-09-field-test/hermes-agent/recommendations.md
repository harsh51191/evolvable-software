# Hermes Agent: the next three moves

**Do this first.** Give memory and persona an undo. The agent rewrites what it remembers about a user, and nothing keeps the previous version, so a bad memory edit is permanent. Skills already have a ledger with rollback; extend it to memory files. That is the change users feel; the change that reaches Level 2 is turning a request into a plan before the agent creates a skill (move 2).

From the EVOLVE assessment of 2026-09-30 (github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.

**With all three moves the product reads Level 2**, checked by re-running the scorer with each move landed.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Let the person running the agent change "What the agent remembers and how it presents itself" themselves, with undo** (For the people running it) | The people running the product make this kind of change themselves, without a release, and can undo it. | 1 | Share of "What the agent remembers and how it presents itself" changes made without an engineer, days from request to live, and engineer tickets for it per month. |
| 2 | **Requests become clear change plans** (For the loop) | A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved. | 2 | Share of requests captured as a plan a person confirmed, and days from request to release. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 1 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Let the person running the agent change "What the agent remembers and how it presents itself" themselves, with undo

*For the people running it.*

**Today.** Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.

**What users get.** The people running the product make this kind of change themselves, without a release, and can undo it. Made by: the person running the agent.

**Evidence.** The memory tool and the background review write MEMORY.md and USER.md, with scans and delete gates (tools/memory_tool.py); SOUL.md and other protected instruction files need a person (cli-config.yaml.example:573-576). No supported undo: memory files keep no history (GOV-05 inventory: memory 1). Reach 0 because the path has no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.

**Track in real use.** Share of "What the agent remembers and how it presents itself" changes made without an engineer, days from request to live, and engineer tickets for it per month.

**Done when:**

- [ ] The person running the agent can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- [ ] They make one such change and then undo it, and the earlier behaviour is back.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "What the agent remembers and how it presents itself" at reach 1 (Self-serve).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17). Read the code before changing it.
Goal for users: The people running the product make this kind of change themselves, without a release, and can undo it.
Today: Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
Where it stands in the code (from the assessment): The memory tool and the background review write MEMORY.md and USER.md, with scans and delete gates (tools/memory_tool.py); SOUL.md and other protected instruction files need a person (cli-config.yaml.example:573-576). No supported undo: memory files keep no history (GOV-05 inventory: memory 1). Reach 0 because the path has no undo. Undo rule used in this field test: a kind has undo when the product keeps the earlier version, or when the change is a selection, toggle or add-and-remove that the same supported path reverses exactly; free-text or multi-field edits with no kept version have none.
Build a supported way for them to make it in the running product, and undo that restores the earlier behaviour, for this kind of change: What the agent remembers and how it presents itself (made by the person running the agent).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- The person running the agent can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- They make one such change and then undo it, and the earlier behaviour is back.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "What the agent remembers and how it presents itself" at reach 1 (Self-serve).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Requests become clear change plans

*For the loop.*

**Today.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**What users get.** A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.

**Why it matters.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.

**Evidence.** Requests are chat turns; the agent can create a skill when asked, without a specification step.

**Track in real use.** Share of requests captured as a plan a person confirmed, and days from request to release.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
- [ ] A fresh assessment scores DEL-01 at 2 or more: "Requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17). Read the code before changing it.
Goal for users: A first step towards "requests become clear change plans": requests captured in the product with structure (area, requester, examples) and linked to the entities or screens involved.
Today: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
Where it stands in the code (from the assessment): Requests are chat turns; the agent can create a skill when asked, without a specification step.
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

**Also failing for Level 3.** Undo for a new version of the code; Safe changes to how data is stored; Limits and checks on changes the product makes to itself.

**Evidence.** Skills have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py) and curator archives are restorable, but configuration has only point-in-time copies on some writes (hermes_cli/config_backups.py) and memory files have no history. Under the inventory rule a 3 needs every default surface at 3.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/NousResearch/hermes-agent @ bddd22be7c2e5f7630c3d90507e6e7280ff092e3 (main) + github.com/NousResearch/hermes-agent-self-evolution @ 0a929e3aa20e15cf04dc7c28492a7d41a5139125 (main, last commit 2026-06-17). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Skills have a per-mutation ledger with single-edit rollback that fails closed (tools/skill_ledger.py) and curator archives are restorable, but configuration has only point-in-time copies on some writes (hermes_cli/config_backups.py) and memory files have no history. Under the inventory rule a 3 needs every default surface at 3.
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

1. Change kind `memory-persona` reach 0 → 1.
2. `DEL-01` 1 → 2 (request loop, Intake).
3. `GOV-05` 2 → 3 (request loop, Roll back, control: Definition rollback).
