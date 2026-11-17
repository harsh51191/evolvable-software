# LibreChat: the next three moves

**Do this first.** One gap holds LibreChat at Level 0: tool connections (MCP servers) can be added and removed but keep no history, so a changed server or credential cannot be put back. Keep a version of each change with one-step undo, as agents and prompts already have. That alone gives it Level 1. Its agent writing skills does not count until it drafts something users rely on, such as agents or model settings.

From the EVOLVE assessment of 2026-09-30 (github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main)). Advice only: it never changes a score. Each move must ship on in the standard installation, and counts only when a fresh assessment finds it.

**Today:** Built to SAL 0 (Manual) · Proven: not evidenced · AI-driven 0 · Request → Release L0 (AI L0) · Issue → Fix L0 (AI L0) · Opportunity → Expansion L1 (AI L0)

**Next level:** 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.

**With all three moves the product reads Level 1**, checked by re-running the scorer with each move landed.

| # | Move | What users get | Level with this move alone | Track in real use |
|---|---|---|---:|---|
| 1 | **Let administrators and users change "Tools and connected services (MCP servers)" themselves, with undo** (For the people running it) | The people running the product make this kind of change themselves, without a release, and can undo it. | 1 | Share of "Tools and connected services (MCP servers)" changes made without an engineer, days from request to live, and engineer tickets for it per month. |
| 2 | **Works out why a problem happens** (For the loop) | A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes). | 0 | Time from a problem being recorded to its cause being known. |
| 3 | **Undo for every change people and AI make in the product** (For safety) | It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? | 0 | Share of change types with one-step undo, and time to reverse a bad change. |

## 1. Let administrators and users change "Tools and connected services (MCP servers)" themselves, with undo

*For the people running it.*

**Today.** Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.

**What users get.** The people running the product make this kind of change themselves, without a release, and can undo it. Made by: administrators and users.

**Evidence.** Servers in librechat.yaml need a server edit and restart; servers added in the UI (api/server/routes/mcp.js:1261-1287) can be removed but keep no history of earlier settings or credentials, so a change cannot be undone through the product. A path without undo is reach 0.

**Track in real use.** Share of "Tools and connected services (MCP servers)" changes made without an engineer, days from request to live, and engineer tickets for it per month.

**Done when:**

- [ ] Administrators and users can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- [ ] They make one such change and then undo it, and the earlier behaviour is back.
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] A fresh assessment lists "Tools and connected services (MCP servers)" at reach 1 (Self-serve).
- [ ] An automated test performs the change and its undo, and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main). Read the code before changing it.
Goal for users: The people running the product make this kind of change themselves, without a release, and can undo it.
Today: Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
Where it stands in the code (from the assessment): Servers in librechat.yaml need a server edit and restart; servers added in the UI (api/server/routes/mcp.js:1261-1287) can be removed but keep no history of earlier settings or credentials, so a change cannot be undone through the product. A path without undo is reach 0.
Build a supported way for them to make it in the running product, and undo that restores the earlier behaviour, for this kind of change: Tools and connected services (MCP servers) (made by administrators and users).
Ship it on by default in the standard installation; do not hide it behind an optional setting.
Change existing stored data only through the product's own migration path, and keep every change reversible.
Done when:
- Administrators and users can do this in the running product: a supported way for them to make it in the running product, and undo that restores the earlier behaviour.
- They make one such change and then undo it, and the earlier behaviour is back.
- It is on in the standard installation, with no optional setting or extra licence needed.
- A fresh assessment lists "Tools and connected services (MCP servers)" at reach 1 (Self-serve).
- An automated test performs the change and its undo, and runs in CI.
Finish with: what you changed, the tests that prove it, and anything in this prompt that was wrong.
```

</details>

## 2. Works out why a problem happens

*For the loop.*

**Today.** The product reports problems but does not work out their likely cause, so people have to investigate each one.

**What users get.** A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes).

**Why it matters.** The product reports problems but does not work out their likely cause, so people have to investigate each one.

Move 1 alone gives the next level; this is what then holds the loop at Level 1.

**Evidence.** Engineers read logs.

**Track in real use.** Time from a problem being recorded to its cause being known.

**Done when:**

- [ ] Shown on a demo or test installation, or in the product's own documentation: The product groups related failures and attaches context (traces, inputs, recent changes).
- [ ] A fresh assessment scores LRN-05 at 2 or more: "The product groups related failures and attaches context (traces, inputs, recent changes)."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main). Read the code before changing it.
Goal for users: A first step towards "works out why a problem happens": the product groups related failures and attaches context (traces, inputs, recent changes).
Today: The product reports problems but does not work out their likely cause, so people have to investigate each one.
Where it stands in the code (from the assessment): Engineers read logs.
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

**Also failing for Level 3.** Backups that are proven to restore; Security checks built into every change; Safe changes to how data is stored; Limits and checks on changes the product makes to itself.

**Evidence.** Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Configuration is unversioned in the product.

**Track in real use.** Share of change types with one-step undo, and time to reverse a bad change.

**Done when:**

- [ ] In the running product: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change? Yes, shown on a demo or test installation.
- [ ] A fresh assessment scores GOV-05 at 3 or more: "The operator sees history and diffs, and rolls back, across all customisation surfaces."
- [ ] It is on in the standard installation, with no optional setting or extra licence needed.
- [ ] An automated test performs the check and runs in CI.

<details><summary>Prompt for a coding agent</summary>

```text
You are working in github.com/danny-avila/LibreChat @ 14f7b2865692d27364c934ecb9912496371018bb (main). Read the code before changing it.
Goal for users: It can answer yes to: can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Today: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
Where it stands in the code (from the assessment): Agents keep a versions history (packages/data-schemas/src/schema/agent.ts:125) and prompt groups keep versions with a chosen production version (promptGroup.ts:25); configuration is unversioned in the product. The higher reading of 3 was dropped under the inventory rule (a 3 needs every default surface at 3): Configuration is unversioned in the product.
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

1. Change kind `tools-mcp` reach 0 → 1.
2. `LRN-05` 1 → 2 (fix loop, Diagnose).
3. `GOV-05` 2 → 3 (request loop, Roll back, control: Definition rollback).
