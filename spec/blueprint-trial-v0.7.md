# Blueprint trial: three products, three levels

Status: a trial of the v0.7 evolution blueprint (`evolution-blueprint-v0.7.md`), written by hand to test whether it gives changes a team could act on. Each product was read again at the same commit as the September 2026 field test. File paths are at that commit. Advisory only; nothing here changes a score.

| Product | Today | Target | Route |
|---|---|---|---|
| LibreChat | SAL 0 (Manual) | L1 | Overlay: no change to existing collections |
| Frappe | SAL 1 (Configurable) | L2 | Overlay, plus new DocTypes |
| n8n | SAL 2 (Assisted) | L3 | Overlay for every critical control; AI steps change existing modules |

## How to use a blueprint

Each product section answers three questions first: what changes for users, why that makes the product more self-evolving, and why it cannot go higher yet. Then come the steps. Each step has:

- **Change, untouched, moves:** what to build, what must not change, and which criteria it should raise;
- **Prompt:** paste it into Claude Code or Codex in the product's repository; the agent builds the step on a branch;
- **Done when:** a checklist for that step. Every box must be checked before the step counts.

A coding agent building a step is not the product evolving itself. The agent builds the machinery; the product has evolved when the **level challenge** passes on the running product. Each product section ends with that challenge and the command that prints the full evidence checklist:

```bash
python3 skills/evolvable-software/scripts/score.py <assessment>.json --checklist <level>
```

**The level is reached only when the challenge passes and a fresh EVOLVE assessment of the branch finds every item.**

---

## 1. LibreChat: SAL 0 → L1

**What changes for users.** Today, changing which models people see, an interface option or a default means an engineer edits `librechat.yaml` and restarts the server. After L1, an admin makes those changes in the admin panel, sees who changed what, and undoes a bad change. A tested backup means a mistake is recoverable.

**Why this is self-evolution.** At L0 only engineers can change LibreChat. At L1 the people running it can reshape it themselves, safely. Every higher level automates something people can already do safely at L1.

**Why not higher yet.** L2 needs the product itself to take in requests and draft changes. LibreChat has no request object for its own changes (DEL-01 0) and no lane that drafts them (DEL-04 0). L2 also needs every architecture criterion at 1 or more, and backup is at 0.

**What's missing, by building block.**

- **Change ledger.** No backup at all (ARC-09 0), and configuration changes made in the admin API are neither audited nor kept as history.
- **Contracts.** Only agents and skills have a machine-readable API contract. Conversations, messages, prompts, presets, memories, schedules and configuration have none.

### Step 1. Backup and restore (safety first)

- **Change.** Add `config/backup.js` and `config/restore.js` beside the existing `config/*.js` admin scripts. Back up MongoDB (`chat-mongodb`, `./data-node` in `docker-compose.yml`), the pgvector database (`vectordb`), uploaded files and images (`./uploads`, `./images`, or the configured S3, Azure Blob or Firebase source from `FileSources` in `packages/data-provider/src/types/files.ts`), skills (`./skill`), `librechat.yaml` and the secrets in `.env` (`CREDS_KEY`, `CREDS_IV`, `JWT_SECRET`, `JWT_REFRESH_SECRET`), encrypted. Skip Meilisearch: it is a derived index, and `config/reset-meili-sync.js` already rebuilds it. Restore schedules (`packages/data-schemas/src/schema/schedule.ts`) paused, list each with the user it runs as, and resume only those whose user still exists and whose keys still decrypt.
- **Untouched.** Every existing collection, schema and route.
- **Moves.** ARC-09 0 → 3. It doesn't move the L1 condition, but L2 needs every architecture criterion at 1 or more, and this is the only one at 0.

**Prompt**

```text
In this LibreChat repository, add supported backup and restore.

1. Create config/backup.js and config/restore.js, following the style of the other config/*.js admin scripts and their npm script entries in package.json.
2. Back up into one encrypted archive: the MongoDB database, the pgvector database used by the RAG API, uploaded files and images from whichever file source is configured (see FileSources in packages/data-provider/src/types/files.ts), the skill directory, librechat.yaml, and the secrets CREDS_KEY, CREDS_IV, JWT_SECRET and JWT_REFRESH_SECRET. Do not back up Meilisearch; after a restore, run the existing config/reset-meili-sync.js logic.
3. On restore, set every schedule (packages/data-schemas/src/schema/schedule.ts) to paused, print each with the user it runs as, and add a command that resumes only schedules whose user exists and whose stored keys decrypt with the restored secrets.
4. Do not change any existing schema, collection or route.
5. Add an automated test that seeds a conversation, an agent, an uploaded file, a user key and a schedule; backs up; wipes the databases and file store; restores; and checks that each comes back and the schedule is paused. Wire it into CI.
6. Document both commands in the docs.

Finish by listing the files you changed and showing the test passing.
```

**Done when**

- [ ] `config/backup.js` and `config/restore.js` exist, with npm scripts and docs.
- [ ] The archive covers data, vector data, files, skills, configuration and secrets, and is encrypted.
- [ ] The restore test runs in CI and passes: conversation, agent, file and user key come back.
- [ ] Restored schedules are paused and listed with their users; only valid ones resume.
- [ ] No existing schema or route changed (check the diff).
- [ ] A fresh EVOLVE assessment reads ARC-09 at 3, with the `tested` facet and every inventory surface at 3.

### Step 2. Configuration changes go into the ledger

- **Change.** `packages/data-schemas/src/types/admin.ts` already declares a `config` audit category but no config actions. Add `config.overrides_updated` and `config.field_patched`, written from the upsert and patch handlers in `packages/api/src/admin/config.ts` (served by `api/server/routes/admin/config.js`). On each write, save the previous `overrides` and `tombstones` to a new `configRevisions` collection keyed by `configVersion`, and add endpoints to list revisions and restore one. Today `configVersion` is used only to invalidate caches.
- **Untouched.** The `Config` schema and the merge order; revisions are a new collection.
- **Moves.** GOV-02 toward 3 for configuration. GOV-05: configuration gains history, diff and rollback beside agents and prompt groups. GOV-05 reaches 3 only when `librechat.yaml` itself is covered, for example by treating the base file as revision 0.

**Prompt**

```text
In this LibreChat repository, give admin configuration changes an audit trail, history and rollback.

1. In packages/data-schemas/src/types/admin.ts, add audit actions config.overrides_updated and config.field_patched in the existing config category, and map them in AUDIT_ACTION_CATEGORY.
2. In packages/api/src/admin/config.ts, write an audit entry from the upsert and field-patch handlers, with the actor, the principal and the changed paths. Never log secret values.
3. Before each write, save the previous overrides and tombstones to a new configRevisions collection (new schema in packages/data-schemas), keyed by principal and configVersion.
4. Add GET /api/admin/config/:principalType/:principalId/revisions and POST .../revisions/:version/restore in api/server/routes/admin/config.js, with the same admin permission checks as the existing routes. A restore is itself a new revision and is audited.
5. Do not change the Config schema or the merge order.
6. Add tests: a patch creates a revision and an audit entry; restore returns the previous effective configuration; a non-admin cannot restore.

Finish by listing the files you changed and showing the tests passing.
```

**Done when**

- [ ] Every configuration change writes an audit entry, visible in the admin audit log.
- [ ] Every change saves the previous version; an admin can list versions and restore one.
- [ ] A restore is audited and is itself revertible.
- [ ] The tests above pass in CI; the `Config` schema is unchanged.
- [ ] A fresh assessment records configuration as a surface with history and rollback in GOV-05's evidence.

### Step 3. One contract for the whole API (this reaches L1)

- **Change.** LibreChat already generates an OpenAPI spec from Zod schemas for agents and skills (`packages/api/src/openapi/registry.ts`, `agents.ts`, `skills.ts`), commits it (`packages/api/openapi/agents.openapi.json`) and checks it in CI (`.github/workflows/backend-review.yml:312`). Add contracts in the same pattern for `convos.js`, `messages.js`, `prompts.js`, `presets.js`, `memories.js`, `schedules.js`, `tags.js` and `admin/config.js` in `api/server/routes/`. Generate a typed client from the spec, and return Zod validation errors as structured field errors.
- **Untouched.** Every route's behaviour; only contracts are added.
- **Moves.** MAL-06 → 3. With it, malleability averages 2.0, so Request → Release and Issue → Fix reach L1 and **SAL becomes 1** (checked with the scorer). Opportunity → Expansion stays at L0: its people path is EXP-02, which doesn't apply to LibreChat. MAL-19 can then reach 2 (introspectable API).

**Prompt**

```text
In this LibreChat repository, extend the generated OpenAPI contract from agents and skills to the rest of the API.

1. Study packages/api/src/openapi/ (registry.ts, agents.ts, skills.ts, adapter.ts, generate.ts). Follow exactly the same pattern.
2. Add contract files for the routes in api/server/routes/convos.js, messages.js, prompts.js, presets.js, memories.js, schedules.js, tags.js and admin/config.js, reusing the Zod schemas in packages/data-provider where they exist. Register them in registry.ts.
3. Regenerate the committed spec with npm run -w @librechat/api openapi:generate, so the existing openapi:check CI step covers it.
4. Generate a typed client from the spec, and add a CI check that the client matches it.
5. Make request validation failures on these routes return a structured body listing each invalid field and its message.
6. Do not change any route's behaviour beyond the error format.

Finish by listing the routes covered, the files changed, and showing openapi:check and the tests passing.
```

**Done when**

- [ ] The committed spec covers every listed route, and `openapi:check` passes in CI.
- [ ] A generated typed client exists and is checked against the spec.
- [ ] Invalid requests return structured field errors.
- [ ] Route behaviour is unchanged: the existing tests pass.
- [ ] A fresh assessment reads MAL-06 at 3.

### LibreChat L1: done when

**Challenge** (Request → Release, from the rubric): *Take a change users often ask for (a field, a rule, a workflow step, a setting). An admin makes it in the running product, with no engineer, code change or redeploy, then undoes it.* For LibreChat: an admin changes which model specs a group sees, through the admin configuration API, and restores the previous version.

**Evidence:** `score.py librechat/assessment.json --checklist 1` lists two conditions per core loop. Rollback is already met. Build needs the Open capability at 2 or more, which step 3 provides.

**Next, toward L2.** A request object for changes to LibreChat itself (DEL-01), and an AI lane that drafts agent, prompt or configuration changes as reviewable revisions (DEL-04), using the revisions from step 2.

---

## 2. Frappe: SAL 1 → L2

**What changes for users.** Today an admin can add fields and DocTypes in Desk, but has to know exactly what to change, and cannot undo a customisation from its history. After L2, a sales user clicks "Request a change" on a Sales Order and writes "we need a delivery date, required for export orders". Frappe drafts the field and the rule in Customize Form. The admin reviews and saves, and can revert to any earlier version.

**Why this is self-evolution.** At L1 the product can be changed. At L2 the product takes part in changing itself: it captures what users need, in context, and drafts the change. People still decide and finish.

**Why not higher yet.** L3 needs the product to carry the change end to end with a person only approving, and every critical control to pass. All five that apply to Frappe fail today: definition rollback, safe migrations, tested restore, tenant isolation and security. Automating more before those pass would let mistakes become permanent.

**What's missing, by building block.**

- **Evolution engine.** No request intake and no drafting lane.
- **Guardrails.** Suggested changes are not checked before they apply.
- **Change ledger.** Customisations are versioned but cannot be reverted.

### Step 1. Revert for definition changes (safety first)

- **Change.** Custom Field, Property Setter, DocType and Workflow all have `track_changes` on, so the Version DocType already stores a diff of every customisation (`frappe/core/doctype/version/version.py`, `get_diff`). Add a whitelisted `revert` and a "Revert to this version" action in `version.js`, applying the old values through the same validation Customize Form uses (`save_customization` in `frappe/custom/doctype/customize_form/customize_form.py`).
- **Untouched.** The Version schema and the customisation tables.
- **Moves.** GOV-05 toward 3. Fields, properties, DocTypes and workflows gain revert; layouts and settings need the same before the control passes.

**Prompt**

```text
In this Frappe repository, let admins revert a customisation to an earlier version.

1. Version (frappe/core/doctype/version/) already stores diffs for Custom Field, Property Setter, DocType and Workflow, which have track_changes on. Add a whitelisted method revert(version_name) in version.py that restores the document to its state before that version's change.
2. Allow it only for those definition DocTypes, and only for users with write permission on the reverted document.
3. Apply the restored values through normal document save and validation, including the checks Customize Form runs (see save_customization in frappe/custom/doctype/customize_form/customize_form.py), so a revert cannot create an invalid definition. Clear the meta cache afterwards.
4. Add a "Revert to this version" button in version.js for those DocTypes, with a confirmation that shows the diff.
5. The revert creates its own Version entry, so it can be reverted too.
6. Add tests: add a Custom Field, change its label, revert, and check the label; change a Workflow transition, revert, and check it; a user without permission cannot revert.

Finish by listing the files changed and showing the tests passing.
```

**Done when**

- [ ] "Revert to this version" works for Custom Field, Property Setter, DocType and Workflow.
- [ ] Reverts go through normal validation and create their own Version entry.
- [ ] The tests above pass in CI.
- [ ] A fresh assessment's GOV-05 inventory shows these surfaces with rollback. GOV-05 reaches 3 only when every customisation surface, including layouts and settings, can be reverted.

### Step 2. Change requests in Desk

- **Change.** Ship a `Change Request` DocType in `frappe/desk/doctype/change_request/` with requester, Module Def, reference DocType and document (Dynamic Link), description, an examples table and a status. Add "Request a change" to the form menu, prefilled with the open DocType and document.
- **Untouched.** Every existing DocType. This is a new definition, which Frappe turns into a new table.
- **Moves.** DEL-01 0 → 2.

**Prompt**

```text
In this Frappe repository, let users request a change to the system from where they work.

1. Create a standard DocType "Change Request" in frappe/desk/doctype/change_request/ with fields: requester (Link User, default the session user), module (Link Module Def), reference_doctype (Link DocType), reference_name (Dynamic Link on reference_doctype), title, description (Text Editor), examples (child table with an example and expected result), and status (Open, In Review, Drafted, Done, Rejected).
2. Give it permissions: any desk user can create and read their own; System Manager can read and update all.
3. Add a "Request a change" item to the form toolbar menu (frappe/public/js/frappe/form/toolbar.js), which opens a new Change Request prefilled with the current DocType, document and module.
4. Add tests: creating a request from a form prefills the references; a user sees only their own requests; status changes are tracked.

Finish by listing the files changed and showing the tests passing.
```

**Done when**

- [ ] Any desk user can raise a Change Request from any form, prefilled with what they were looking at.
- [ ] Requests carry requester, area, the DocType and document involved, and examples.
- [ ] The tests above pass in CI.
- [ ] A fresh assessment reads DEL-01 at 2.

### Step 3. An AI lane that drafts customisations

- **Change.** A whitelisted method that sends a Change Request, plus the target DocType's metadata (`frappe.get_meta`), to a configured model. It returns proposed Custom Field and Property Setter changes, loaded into Customize Form as unsaved changes. A System Manager reviews them and saves through `save_customization`; nothing applies until a person saves. The provider and key live in a new `AI Settings` DocType, with the key in a Password field.
- **Untouched.** Customize Form's save path, which every draft still goes through.
- **Moves.** DEL-04 0 → 2, which clears the build-path condition for both core loops, so **SAL becomes 2** (checked with the scorer).
- **Consequence.** Frappe now ships AI, so the eight AI Readiness checks start to apply, including offline evaluation (AIR-05) and action tracing (AIR-07).

**Prompt**

```text
In this Frappe repository, add an AI lane that drafts customisations from a Change Request, for a person to review and save.

1. Add a single DocType "AI Settings" with provider, model and an API key in a Password field. Only System Manager can read or write it.
2. Add a whitelisted method draft_customization(change_request) that is allowed only for System Manager. It sends the request (title, description, examples) and the reference DocType's metadata from frappe.get_meta to the configured model, and asks for a JSON list of Custom Field and Property Setter changes. Validate the response against a strict schema; reject unknown field types and changes to standard fields that Customize Form would refuse.
3. Load the valid changes into Customize Form for that DocType as unsaved changes, and show a summary of each. Nothing is saved until the System Manager saves through the existing save_customization path.
4. Record the request, the model, the prompt version, the proposed changes and the person's decision on the Change Request, and set its status to Drafted.
5. Add an evaluation set: at least ten Change Requests with expected drafts, and a test that runs the validator on recorded model responses (no network in CI).
6. Add tests: an invalid or unsafe draft is rejected; nothing is saved without a person; a non-System Manager cannot call the method.

Finish by listing the files changed and showing the tests passing.
```

**Done when**

- [ ] A System Manager can turn a Change Request into a draft in Customize Form, and nothing applies until they save.
- [ ] Unsafe or invalid drafts are rejected by schema checks.
- [ ] Each draft is recorded with its model, prompt version and the person's decision.
- [ ] The evaluation set and tests pass in CI without network access.
- [ ] A fresh assessment reads DEL-04 at 2, with an AI reading of 2, and scores the AI Readiness checks.

### Step 4 (optional). Check index suggestions before they apply

- **Change.** Before a Recorder suggestion applies (`frappe/core/doctype/recorder/db_optimizer.py`), run `EXPLAIN` on the recorded queries with and without the index and show the difference; block it if the index is unused.
- **Moves.** LRN-08 1 → 2. This lifts Issue → Fix to L2 without any AI, but the headline stays at 1 without step 3.

**Done when**

- [ ] A suggested index cannot be applied without an automated check showing the queries it affects use it.
- [ ] A test covers both an accepted and a blocked suggestion.
- [ ] A fresh assessment reads LRN-08 at 2.

### Frappe L2: done when

**Challenge** (Request → Release, from the rubric): *A user describes a change in plain words inside the product. The product captures it with structure (what, who, where) and drafts the change for a person to finish. Every change, drafted or not, passes automated checks before it lands.* For Frappe: a user raises "add a delivery date, required for export orders" from a Sales Order; a System Manager gets a draft field and property change in Customize Form and saves it; then reverts it from its version history.

**Evidence:** `score.py frappe/assessment.json --checklist 2` lists four conditions for Request → Release (two met today) and five for Issue → Fix (four met). Steps 2 and 3 meet the rest.

**Before L3.** The first fixes:

- a restore test that includes the site config and encryption key (ARC-09);
- down steps or an enforced online strategy for patches (ARC-02);
- isolation checks between sites (ARC-05);
- blocking security checks (GOV-04).

---

## 3. n8n: SAL 2 → L3

**What changes for users.** Today AI builds a workflow when asked. But if it starts failing at 2am, someone has to notice; and a bad change to a credential, variable or setting cannot be undone in the product. After L3, n8n notices the failures, says how many runs and users are affected, diagnoses them, and proposes a fix as a review request with test results attached. An admin approves; the fix goes live and can be rolled back, like anything else in the instance. The AI can only change the projects it is allowed to.

**Why this is self-evolution.** At L2 the product drafts changes when asked. At L3 it carries the whole loop, from noticing a problem to shipping a verified fix, and people only approve. Building that safely means every change must be undoable and recoverable first, which is why the safety steps come before the AI steps.

**Why not higher yet.** L4 lets low-risk changes ship with no person involved. That needs a written policy per kind of change (GOV-07 3), automatic rollback when a change makes things worse, and every architecture criterion at 3 with tests. None of this exists yet, and it shouldn't be attempted until L3 has run in practice.

**What's missing, by building block.**

| Block | Blocking today |
|---|---|
| Change ledger | Definition rollback (GOV-05 2), safe migrations (ARC-02 2), tested restore (ARC-09 2) |
| Guardrails | Bounded self-change (GOV-10 2) |
| Evolution engine | Intake (DEL-01 2), build path (DEL-04 2), diagnosis (LRN-05 2), proposals (LRN-06 2) |
| Governed release | Verification surface (DEL-06 2) |
| Sensing | Issue detection (LRN-03 2) |

n8n has two seams that make an overlay possible: **event relays** (`packages/cli/src/events/relays/`) and the **policy infrastructure** (`packages/cli/src/modules/policy-infrastructure/`), which is on by default and runs checks at save, publish, start, import and credential decrypt.

### Step 1. History and rollback for every surface, not just workflows (safety)

- **Change.** Workflows already have history and restore (`packages/cli/src/workflows/workflow-history/`). Credentials, variables, data tables and settings don't. Add a `change-ledger.event-relay.ts` beside `activity.event-relay.ts`, which is already registered from `BaseCommand` as a core relay. It listens to the `credentials-*`, `variable-*`, `data-table-*` and settings events in `events/maps/relay.event-map.ts`. These events carry only IDs, so on each one the relay snapshots the current row into a new `entity_history` table, keeping credentials in their encrypted form. Add restore endpoints modelled on `workflow-history.controller.ts`.
- **Untouched.** Every existing entity and table. One additive migration creates `entity_history`.
- **Moves.** GOV-05 2 → 3, once every surface has history, diff and rollback.

**Prompt**

```text
In this n8n repository, give credentials, variables, data tables and settings the same history and restore that workflows have.

1. Read packages/cli/src/workflows/workflow-history/ and packages/cli/src/events/relays/activity.event-relay.ts; follow their patterns.
2. Add an entity_history entity and one additive migration for PostgreSQL and SQLite in packages/@n8n/db: id, entity type, entity id, version, snapshot (JSON), actor, created at. Do not alter any existing table.
3. Add packages/cli/src/events/relays/change-ledger.event-relay.ts, registered like activity.event-relay.ts. On credentials-created/updated/deleted, variable-created/updated/deleted, the data-table events, and the settings events in packages/cli/src/events/maps/relay.event-map.ts (such as source-control-settings-updated, ldap-settings-updated and instance-ai-settings-updated), load the current row and store a snapshot. Where a settings surface emits no event, add one. Store credential data only in its existing encrypted form. On first start, store a baseline snapshot of each existing row.
4. Add a controller with list, get-diff and restore endpoints per entity type, with the same permission scopes as editing that entity; restoring a credential needs credential:update on it. A restore is audited and creates a new snapshot.
5. Add tests for each entity type: change, list history, diff, restore; a user without permission cannot restore; credential snapshots are never stored decrypted.

Finish by listing the files changed and showing the tests passing.
```

**Done when**

- [ ] Credentials, variables, data tables and settings each show history and diffs, and restore, with permissions enforced.
- [ ] Credential snapshots stay encrypted.
- [ ] Only additive migrations; no existing table changed.
- [ ] The tests above pass in CI.
- [ ] A fresh assessment reads GOV-05 at 3, with every surface at 3 in its inventory and the `tested` facet.

### Step 2. One backup command and a restore test (safety)

- **Change.** `export:entities` and `import:entities` (`packages/cli/src/commands/export/entities.ts`) move the database entities, but binary data and the encryption key travel separately, and nothing tests a restore. Add `n8n backup` and `n8n restore` commands that bundle entities with data-table rows, binary data and the encryption key, encrypted. Restore active workflows as inactive, list each scheduled trigger with the project it runs as, and activate after confirmation or a check that each workflow's credentials still decrypt.
- **Untouched.** The existing export and import commands, which the new ones call.
- **Moves.** ARC-09 2 → 3.

**Prompt**

```text
In this n8n repository, add a single backup and restore with a tested recovery.

1. Add commands backup and restore in packages/cli/src/commands/, reusing export:entities and import:entities (with data-table rows). Add binary data for the filesystem and S3 modes, and the instance encryption key, into one archive encrypted with an operator-supplied passphrase.
2. On restore, import every workflow inactive. Print each workflow that has a schedule or polling trigger, with its project and owner. Add a flag to activate only those whose credentials decrypt with the restored key, and an interactive confirmation otherwise.
3. Do not change the behaviour of the existing export and import commands.
4. Add an integration test: seed workflows (one active with a schedule trigger), a credential, a variable, a data table with rows and a binary file; back up; wipe the database and binary store; restore; check each comes back, the scheduled workflow is inactive until confirmed, and a workflow using the credential and the file runs.
5. Document both commands.

Finish by listing the files changed and showing the test passing.
```

**Done when**

- [ ] One command produces one encrypted archive covering data, definitions, files, secrets and scheduled work.
- [ ] Restored scheduled workflows stay inactive until confirmed or checked.
- [ ] The restore integration test passes in CI.
- [ ] A fresh assessment reads ARC-09 at 3, with every inventory surface at 3.

### Step 3. Online migrations, enforced (safety)

- **Change.** Migrations already have down steps and tests (`packages/@n8n/db/src/migrations`). Add a CI lint that rejects destructive operations unless the migration is marked as the contract step of an expand-and-contract pair, and run the migration suite against a populated database from the previous release.
- **Untouched.** Existing migrations.
- **Moves.** ARC-02 2 → 3.

**Prompt**

```text
In this n8n repository, enforce safe, online database migrations.

1. Add a lint step in CI that scans new migrations in packages/@n8n/db/src/migrations and fails on destructive operations: dropping or renaming a column or table, changing a column type, or adding a NOT NULL column without a default. Allow them only when the migration declares itself the contract step of an expand-and-contract pair and names the earlier expand migration.
2. Exempt existing migrations by a recorded baseline, so only new ones are checked.
3. Add a CI job that restores a populated database from the previous release, runs all new migrations up and down, and checks the data survives.
4. Document the expand-and-contract rule for contributors.

Finish by listing the files changed and showing the lint failing on a deliberately destructive test migration and passing on the real ones.
```

**Done when**

- [ ] A destructive migration without a declared expand step fails CI.
- [ ] Migrations are tested up and down against populated data from the previous release.
- [ ] The rule is documented.
- [ ] A fresh assessment reads ARC-02 at 3.

### Step 4. Limits on what AI may change (safety)

- **Change.** Add an `AiChangeScopeCheck` as a new `@PolicyCheck()` class, the same way `type-availability-policies` is built. For saves and publishes made by Instance AI or the workflow builder, it enforces the projects and folders the AI may change, a cap on AI saves per period, a ban on creating credentials, and a ban on publishing an AI-authored version without a person's approval.
- **Design question.** Confirm that the check context says the caller was AI; if not, add the caller at the Instance AI call site.
- **Untouched.** Existing policies and save paths.
- **Moves.** GOV-10 2 → 3, which passes bounded self-change (LRN-08 is already 2).

**Prompt**

```text
In this n8n repository, bound what AI may change.

1. Read packages/cli/src/modules/policy-infrastructure/README.md and the type-availability-policies module; build a new module the same way.
2. Ensure the policy check context identifies when a save or publish comes from Instance AI or the AI workflow builder. If it does not, add the caller at those call sites without changing behaviour for people.
3. Add AiChangeScopeCheck as a @PolicyCheck for workflowSave, workflowPublish and credentialSave. For AI callers it enforces an admin-set scope: allowed projects and folders, a maximum number of AI saves per hour, no credential creation, and no publish of an AI-authored version until a person approves it.
4. Store the scope in the module's own settings, editable by admins, with defaults that allow nothing outside the user's current project.
5. Blocked actions use the existing policy verdict and audit path.
6. Add tests for each limit, and that people are never affected by it.

Finish by listing the files changed and showing the tests passing.
```

**Done when**

- [ ] AI saves and publishes are identified as AI in the policy context.
- [ ] Each limit blocks and audits out-of-scope AI changes; people are unaffected.
- [ ] AI-authored versions cannot be published without a person.
- [ ] The tests above pass in CI.
- [ ] A fresh assessment reads GOV-10 at 3, and the bounded self-change control passes.

### Step 5. A deployed-configuration snapshot

- **Change.** `/healthz` and the instance version history exist. Add an endpoint returning the running version, commit, enabled modules, licence features and a hash of the effective configuration, with secrets redacted.
- **Moves.** DEL-06 2 → 3.

**Prompt**

```text
In this n8n repository, add a machine-readable snapshot of what is deployed.

1. Add an authenticated endpoint that returns the running version and commit, enabled and disabled modules, licence features in use, the instance type, and a stable hash of the effective configuration, with every secret value excluded from both the output and the hash input.
2. Reuse the instance version history module for version data.
3. Add tests: secrets never appear; the hash changes when a non-secret setting changes and not otherwise.

Finish by listing the files changed and showing the tests passing.
```

**Done when**

- [ ] A release can be checked against the snapshot automatically.
- [ ] No secret appears in the output.
- [ ] The tests above pass.
- [ ] A fresh assessment reads DEL-06 at 3.

### Steps 6–9. The AI loop, after the safety steps pass

These change existing modules, so they need the incremental route. Run them only once steps 1–4 are done.

| Step | Change | Moves | Done when |
|---|---|---|---|
| 6 | Add acceptance criteria, impact and a risk class to the builder's plan (`packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts`), confirmed by the user | DEL-01 → 3 | Every plan shows acceptance criteria, affected workflows and a risk class, and needs the user's confirmation; tests cover it |
| 7 | Deliver builder output as a workflow review request (`modules/workflow-reviews.ee`), with an evaluation run against the draft (`evaluation.ee`) attached | DEL-04 → 3 | No AI-built change publishes without a review request carrying passing evaluation results |
| 8 | Turn Insights failure rates (`modules/insights/insights.service.ts`) into issues attributed to a workflow, with affected runs and frequency | LRN-03 → 3 | Repeated failures appear as issues without anyone asking, with counts; tests cover detection |
| 9 | Diagnose failed executions automatically, and rank fix proposals with evidence | LRN-05, LRN-06 → 3 | Each new issue gets a diagnosis and a ranked proposal automatically; evaluated on a recorded set |

Each needs its own prompt in the same form; they are left as a table here because they depend on the safety steps landing first.

### n8n L3: done when

**Challenge** (Issue → Fix, from the rubric): *Break something on purpose. Without being asked, the product raises it as an issue with the users affected and how often, diagnoses it, proposes a fix with evidence, and ships it after a person approves: staged, measured and reversible. The safety drill for Request → Release must also pass.* For n8n: make a scheduled workflow fail by revoking its credential; n8n raises the issue, diagnoses the credential, proposes a fix as a review request with an evaluation attached; an admin approves; the fix ships; the admin rolls back both the workflow and the credential change.

**Safety drill:** restore last night's backup into a fresh instance with scheduled workflows held; roll back a variable and a credential; run a new migration on a copy of production data; show an AI save outside its scope being blocked.

**Evidence:** `score.py n8n/assessment.json --checklist 3` lists 19 conditions for Request → Release (12 met today) and 21 for Issue → Fix (12 met). If steps 1–9 land with tests, both reach L3, so SAL 3 (checked with the scorer). That is a ceiling, not a forecast.

**If n8n GOV-04 is corrected to 2,** as both second raters recommend, add a step: make the Trivy scan blocking (`.github/workflows/security-trivy-scan-callable.yml:51` sets `exit-code: '0'`) and extend the pull-request security scan beyond workflow-file changes.

---

## 4. What the trial showed

1. **Exact recommendations are possible when they build on the product's own patterns.** Each step copies something the product already does: workflow history extended to credentials, the OpenAPI registry extended to every route, Version diffs gaining a revert. That makes the advice concrete, and credible to the product's own engineers.
2. **The product's seams decide the route.** n8n can fix all four failing controls without touching existing tables, because it has event relays and a policy layer. A product without seams needs the incremental route for the same fixes.
3. **Re-reading code catches scoring errors.** LibreChat has a generated, CI-checked OpenAPI spec for agents and skills, but the field test scored MAL-06 at 1 ("no published contract"). That reads as a 2. It doesn't change LibreChat's level, but it should be corrected.
4. **The L1 rule can be met in a way that misses its intent.** LibreChat reaches L1 through an API contract, because L1 is an average of malleability criteria. The change that actually lets people reshape LibreChat without engineering is step 2 (configuration with history). This is worth a rubric review.
5. **Adding AI has consequences the plan must state.** Frappe's AI lane brings eight AI Readiness checks into scope.
6. **Not verified.** Sizes, whether n8n's policy checks can tell AI callers apart today, how n8n restores active workflows, and whether LibreChat's validation errors are already structured. Each is marked where it matters. None of the prompts has been run yet.
