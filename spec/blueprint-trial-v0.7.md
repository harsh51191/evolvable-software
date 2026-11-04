# Blueprint trial: three products, three levels

Status: a trial of the v0.7 evolution blueprint (`evolution-blueprint-v0.7.md`), written by hand to test whether it gives changes a team could act on. Each product was read again at the same commit as the September 2026 field test. File paths are at that commit. Advisory only; nothing here changes a score.

| Product | Today | Target | Route |
|---|---|---|---|
| LibreChat | SAL 0 (Manual) | L1 | Overlay: no change to existing collections |
| Frappe | SAL 1 (Configurable) | L2 | Overlay, plus new DocTypes |
| n8n | SAL 2 (Assisted) | L3 | Overlay for every critical control; AI steps change existing modules |

Each step says what to change, what stays untouched, which criteria it moves, and what the next EVOLVE run will look for.

---

## 1. LibreChat: SAL 0 → L1

**What L1 needs.** People can change the product without engineering, and roll the change back. LibreChat already passes rollback (GOV-05 2) and issue detection (LRN-03 2). One condition fails: its malleability averages 1.7 and must reach 2.

**What's missing, by building block.**

- **Change ledger.** No backup at all (ARC-09 0), and configuration changes made in the admin API are neither audited nor kept as history.
- **Contracts.** Only agents and skills have a machine-readable API contract. Conversations, messages, prompts, presets, memories, schedules and configuration have none.

### Step 1. Backup and restore (safety first)

- **Change.** Add `config/backup.js` and `config/restore.js` beside the existing `config/*.js` admin scripts. Back up MongoDB (`chat-mongodb`, `./data-node` in `docker-compose.yml`), the pgvector database (`vectordb`), uploaded files and images (`./uploads`, `./images`, or the configured S3, Azure Blob or Firebase source from `FileSources` in `packages/data-provider/src/types/files.ts`), skills (`./skill`), `librechat.yaml` and the secrets in `.env` (`CREDS_KEY`, `CREDS_IV`, `JWT_SECRET`, `JWT_REFRESH_SECRET`), encrypted. Skip Meilisearch: it is a derived index, and `config/reset-meili-sync.js` already rebuilds it.
- **Scheduled work.** Restore schedules (`packages/data-schemas/src/schema/schedule.ts`) paused. List each one with the user it runs as, and resume only those whose user still exists and whose keys still decrypt.
- **Test.** A CI job that seeds a stack, backs it up, wipes it, restores it, and checks that a conversation, an agent, an uploaded file and a user key all come back.
- **Untouched.** Every existing collection, schema and route.
- **Moves.** ARC-09 0 → 3 (a 3 needs every surface restored, with automated tests). It doesn't move the L1 condition, but L2 needs every architecture criterion at 1 or more, and this is the only one at 0.
- **EVOLVE will look for.** The two commands, the restore test in CI, and the schedule hold.

### Step 2. Configuration changes go into the ledger

- **Change.** `packages/data-schemas/src/types/admin.ts` already declares a `config` audit category but no config actions. Add `config.overrides_updated` and `config.field_patched`. Write them from the upsert and patch handlers in `packages/api/src/admin/config.ts`, which serve `PUT` and `PATCH /api/admin/config/:principalType/:principalId` (`api/server/routes/admin/config.js`). On each write, save the previous `overrides` and `tombstones` to a new `configRevisions` collection keyed by `configVersion`. Add `GET …/revisions` and `POST …/revisions/:version/restore`. Today `configVersion` is used only to invalidate caches.
- **Untouched.** The `Config` schema and the merge order; revisions are a new collection.
- **Moves.** GOV-02 toward 3 for configuration. GOV-05: configuration gains history, diff and rollback beside agents and prompt groups. GOV-05 reaches 3 only when `librechat.yaml` itself is covered, for example by treating the base file as revision 0.
- **EVOLVE will look for.** Audit entries for configuration changes, revision history, and a tested restore.

### Step 3. One contract for the whole API (this reaches L1)

- **Change.** LibreChat already generates an OpenAPI spec from Zod schemas for agents and skills (`packages/api/src/openapi/registry.ts`, `agents.ts`, `skills.ts`), commits it (`packages/api/openapi/agents.openapi.json`) and checks it in CI (`.github/workflows/backend-review.yml:312`). Add contract files in the same pattern for the routes in `api/server/routes/`: `convos.js`, `messages.js`, `prompts.js`, `presets.js`, `memories.js`, `schedules.js`, `tags.js` and `admin/config.js`. Generate the typed client from the spec, not by hand in `packages/data-provider`, and return Zod validation errors as structured field errors.
- **Untouched.** Every route's behaviour; only contracts are added.
- **Moves.** MAL-06 → 3. With it, malleability averages 2.0, so Request → Release and Issue → Fix reach L1 and **SAL becomes 1** (checked with the scorer). Opportunity → Expansion stays at L0: its people path is EXP-02, which doesn't apply to LibreChat. MAL-19 can then reach 2 (introspectable API).
- **EVOLVE will look for.** Full coverage in the committed spec, a generated client, and structured validation errors.

**Next, toward L2.** A request object for changes to LibreChat itself (DEL-01), and an AI lane that drafts agent, prompt or configuration changes as reviewable revisions (DEL-04), using the revisions from step 2.

---

## 2. Frappe: SAL 1 → L2

**What L2 needs.** The product itself takes in a request and drafts the change; a person finishes it. Frappe has a rich definition model (MAL-01 3: DocTypes created in Desk generate real tables), but nothing takes in requests (DEL-01 0) and nothing drafts a change (DEL-04 0). Its fix loop is one condition short: the Recorder's index suggestions have no automated check before they apply (LRN-08 1).

**What's missing, by building block.**

- **Evolution engine.** No request intake and no drafting lane.
- **Guardrails.** Suggested changes are not checked before they apply.
- **Change ledger.** Customisations are versioned but cannot be reverted.

### Step 1. Revert for definition changes (safety first)

- **Change.** Custom Field, Property Setter, DocType and Workflow all have `track_changes` on, so the Version DocType already stores a diff of every customisation (`frappe/core/doctype/version/version.py`, `get_diff`). Add a whitelisted `revert` to `version.py`, and a "Revert to this version" action in `version.js` for definition DocTypes. Apply the old values through the same validation Customize Form uses (`save_customization` in `frappe/custom/doctype/customize_form/customize_form.py`), so a revert cannot bypass it.
- **Untouched.** The Version schema and the customisation tables.
- **Moves.** GOV-05 toward 3. Fields, properties, DocTypes and workflows gain revert; layouts and settings need the same before the control passes.
- **EVOLVE will look for.** A revert action, with tests that revert a field change and a workflow change.

### Step 2. Change requests in Desk

- **Change.** Ship a `Change Request` DocType in `frappe/desk/doctype/change_request/` with: requester, Module Def, reference DocType and document (Dynamic Link), description, an examples table and a status. Add "Request a change" to the form menu, prefilled with the open DocType and document.
- **Untouched.** Every existing DocType. This is a new definition, which Frappe turns into a new table.
- **Moves.** DEL-01 0 → 2.
- **EVOLVE will look for.** Requests captured in the product, with structure, linked to the DocTypes involved.

### Step 3. An AI lane that drafts customisations

- **Change.** A whitelisted method that sends a Change Request, plus the target DocType's metadata (`frappe.get_meta`), to a configured model. It returns proposed Custom Field and Property Setter changes, loaded into Customize Form as unsaved changes. A System Manager reviews them and saves through `save_customization`; nothing applies until a person saves. The provider and key live in a new `AI Settings` DocType, with the key in a Password field.
- **Untouched.** Customize Form's save path, which every draft still goes through.
- **Moves.** DEL-04 0 → 2, which clears the build-path condition for both core loops, so **SAL becomes 2** (checked with the scorer).
- **Consequence.** Frappe now ships AI, so the eight AI Readiness checks start to apply, including offline evaluation (AIR-05) and action tracing (AIR-07). Plan an evaluation set of change requests with expected drafts from the start.

### Step 4 (optional). Check index suggestions before they apply

- **Change.** Before a Recorder suggestion applies (`frappe/core/doctype/recorder/db_optimizer.py`), run `EXPLAIN` on the recorded queries with and without the index and show the difference; block it if the index is unused.
- **Moves.** LRN-08 1 → 2. This lifts Issue → Fix to L2 without any AI, but the headline stays at 1 without step 3.

**Before L3.** All five applicable critical controls fail today. The first fixes:

- a restore test that includes the site config and encryption key (ARC-09);
- down steps or an enforced online strategy for patches (ARC-02);
- isolation checks between sites (ARC-05);
- blocking security checks (GOV-04).

---

## 3. n8n: SAL 2 → L3

**What L3 needs.** The product carries a change end to end, a person approves each release, and every critical control passes. n8n is two steps away in its stages (AI drafts but doesn't yet carry changes or diagnose by itself) and fails four controls.

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

- **Change.** Workflows already have history and restore (`packages/cli/src/workflows/workflow-history/`). Credentials, variables, data tables and settings don't. Add a `change-ledger.event-relay.ts` beside `activity.event-relay.ts`, which is already registered from `BaseCommand` as a core relay. It listens to `credentials-*`, `variable-*` and `data-table-*` events and the settings events in `events/maps/relay.event-map.ts`. These events carry only IDs, so on each one the relay snapshots the current row into a new `entity_history` table, keeping credentials in their encrypted form. Take a baseline snapshot on first start. Add restore endpoints modelled on `workflow-history.controller.ts`; restoring a credential requires the credential owner's permission.
- **Untouched.** Every existing entity and table. One additive migration creates `entity_history`.
- **Moves.** GOV-05 2 → 3, once every surface in the inventory has history, diff and rollback.
- **EVOLVE will look for.** History and restore for each surface, with tests.

### Step 2. One backup command and a restore test (safety)

- **Change.** `export:entities` and `import:entities` (`packages/cli/src/commands/export/entities.ts`) move the database entities, but binary data and the encryption key travel separately, and nothing tests a restore. Add `n8n backup` and `n8n restore` commands that bundle entities with data-table rows, binary data (filesystem or S3 mode) and the encryption key, encrypted. Restore active workflows as inactive and list each scheduled trigger with the project it runs as. Activate only after an operator confirms, or after a check that each workflow's credentials still decrypt (the `credentialDecrypt` policy point). Add a CI test: seed, back up, wipe, restore, then run a workflow that uses a credential and a binary file.
- **Untouched.** The existing export and import commands, which the new ones call.
- **Moves.** ARC-09 2 → 3.

### Step 3. Online migrations, enforced (safety)

- **Change.** Migrations already have down steps and tests (`packages/@n8n/db/src/migrations`). Add a CI lint that rejects destructive operations (dropping or renaming a column or table, adding a non-null column without a default) unless the migration is marked as the contract step of an expand-and-contract pair. Run the migration suite against a populated database from the previous release.
- **Untouched.** Existing migrations.
- **Moves.** ARC-02 2 → 3.

### Step 4. Limits on what AI may change (safety)

- **Change.** Add an `AiChangeScopeCheck` as a new `@PolicyCheck()` class, the same way `type-availability-policies` is built. For saves and publishes made by Instance AI or the workflow builder, it enforces:
  - the projects and folders the AI may change;
  - a cap on AI saves per period;
  - a ban on creating credentials;
  - a ban on publishing an AI-authored version without a person's approval.

  Blocks are audited like any policy verdict.
- **Design question.** The policy README lists Instance AI as a save call site. Confirm that the check context says the caller was AI; if not, add the caller at that call site.
- **Untouched.** Existing policies and save paths.
- **Moves.** GOV-10 2 → 3, which passes bounded self-change (LRN-08 is already 2).

### Step 5. A deployed-configuration snapshot

- **Change.** `/healthz` and the instance version history exist. Add an endpoint returning the running version, commit, enabled modules, licence features and a hash of the effective configuration, with secrets redacted, so a release can be checked against what is actually running.
- **Moves.** DEL-06 2 → 3 (the rule-11 doubt in the evidence goes away).

### Steps 6–9. The AI loop, after the controls pass

These change existing modules, so they need the incremental route.

| Step | Change | Moves |
|---|---|---|
| 6 | Add acceptance criteria and a risk class to the builder's plan (`packages/@n8n/ai-workflow-builder.ee/src/types/planning.ts`), confirmed by the user | DEL-01 → 3 |
| 7 | Deliver builder output as a workflow review request (`modules/workflow-reviews.ee`), with an evaluation run against the draft (`evaluation.ee`) attached as verification evidence | DEL-04 → 3 |
| 8 | Turn Insights failure rates (`modules/insights/insights.service.ts`) into issues attributed to a workflow, with affected runs and frequency | LRN-03 → 3 |
| 9 | Diagnose failed executions automatically, not only when asked, and rank fix proposals with evidence | LRN-05, LRN-06 → 3 |

**Projected.** If steps 1–9 land with tests, both core loops reach L3, so SAL 3 (checked with the scorer). That is a ceiling, not a forecast.

**If n8n GOV-04 is corrected to 2,** as both second raters recommend, add a step: make the Trivy scan blocking (`.github/workflows/security-trivy-scan-callable.yml:51` sets `exit-code: '0'`) and extend the pull-request security scan beyond workflow-file changes.

---

## 4. What the trial showed

1. **Exact recommendations are possible when they build on the product's own patterns.** Each step copies something the product already does: workflow history extended to credentials, the OpenAPI registry extended to every route, Version diffs gaining a revert. That makes the advice concrete, and credible to the product's own engineers.
2. **The product's seams decide the route.** n8n can fix all four failing controls without touching existing tables, because it has event relays and a policy layer. A product without seams needs the incremental route for the same fixes. The blueprint should find seams first.
3. **Re-reading code catches scoring errors.** LibreChat has a generated, CI-checked OpenAPI spec for agents and skills, but the field test scored MAL-06 at 1 ("no published contract"). That reads as a 2. It doesn't change LibreChat's level, but it should be corrected.
4. **The L1 rule can be met in a way that misses its intent.** LibreChat reaches L1 through an API contract, because L1 is an average of malleability criteria. The change that actually lets people reshape LibreChat without engineering is step 2 (configuration with history). This is worth a rubric review.
5. **Adding AI has consequences the plan must state.** Frappe's AI lane brings eight AI Readiness checks into scope. The blueprint should say what a step brings into scope, not only what it fixes.
6. **Not verified.** Sizes, whether n8n's policy checks can tell AI callers apart today, how n8n restores active workflows, and whether LibreChat's validation errors are already structured. Each is marked where it matters.
