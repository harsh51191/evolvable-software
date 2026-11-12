# Answer Desk: design

Status: design document for the reference product in this folder. Section numbers are stable so that an assessment can cite them (for example `examples/born-evolvable/DESIGN.md §4`). Where the code differs from this document, the document says so in §11.

## 1. Purpose

Answer Desk answers customers' help-desk questions from a set of written answers, and passes the questions it cannot answer to the right team. It is small on purpose. Its job in this repository is to show the twelve foundations of `docs/born-evolvable.md` working together in running code: a product designed from its first day so that people, an AI and the product itself can change it through one governed path, with autonomy raised one kind of change at a time as the record supports it.

## 2. Kinds of change

The people running Answer Desk need to change four things. They are declared once, in `kinds.json`, with their fields and types; every other part of the product reads that file.

| Kind | What it is | Who changes it | Main | Released to a share of traffic |
|---|---|---|---|---|
| `answers` | What the desk tells customers: keywords, the answer text and its source | Support lead; the AI drafter; the product at the top of the dial | Yes | Yes |
| `routing-rules` | Which team gets a question the desk cannot answer | Support lead | Yes | Yes |
| `checks` | The questions every change is checked against, and the outcome each must get | Support lead; the product, from recorded failures | No | No (applies at once) |
| `policy` | Who may make which kind of change, the limits, and the dial per kind | Product owner only | No | No (applies at once) |

`checks` and `policy` are the loop's own rules. Making them kinds of change is what lets the loop improve itself (§8).

Out of scope on purpose: prices, user accounts, layouts, a plugin system. Answer Desk is not a platform. A new kind of change is added by an engineer to `kinds.json` and the code, when real requests show the need.

## 3. Data model

One SQLite file. Schema changes are numbered migrations with up and down steps (`answerdesk/store.py`, `MIGRATIONS`).

- **`changes`**: every version of every definition. Columns: kind, key, version number, body (JSON, validated against `kinds.json`; empty means "remove"), author type (`person`, `ai`, `product`) and name, note, provenance (what it was drafted from), status, policy decision, share of traffic, the version it replaced, and the measurement record (baseline, target, window, tolerance, result).
- **`live`**: for each definition, the stable version everyone sees and at most one candidate version being released.
- **`events`**: the audit trail. Every proposal, policy decision, check result, approval, release, switch, measurement, reversal and wrong pass, with the actor and time.
- **`signals`**: one row per question: time, a hashed session id, the question with personal data removed, the answer or team it got, the version that served it, the feedback, and (for staff) the outcome it should have had.
- **`exposures`**: which questions were exposed to which candidate change, and in which arm (candidate or control).

Definitions are small documents, so one versioned table holds them all. Records about the business (here, signals) get their own typed tables and indexes rather than going into a generic store.

Statuses of a change: `proposed`, then `blocked` (policy), `rejected` (checks), `awaiting_approval`, `live` (released to a share), `off` (switched off), `kept` (released to everyone) or `undone`.

## 4. The door

Every change goes through `Door.submit` (`answerdesk/door.py`), whoever makes it:

1. **Propose.** A version is recorded with its author and provenance.
2. **Policy decision** (§6), in code: `blocked`, `needs_person` or `pre_approved`. A blocked change stops here and the reason is logged.
3. **Check** (§7): validation against `kinds.json`, one change in flight per definition, the check suite, and for a policy change the raise rules.
4. **Release.** Pre-approved changes are released at once; others wait for a person, and approval runs steps 2 and 3 again on the current state. Answers and routing rules go to the share of traffic the policy sets; checks and policy apply at once.
5. **Measure** (§5) over a window, then **keep, revise or undo**.

People use the command line (`propose`, `approve`, `keep`, `off`, `on`, `undo`). The AI drafter calls the door as `ai:rule-drafter`. The product's scheduler (`tick`) calls it as `product:scheduler`. There is no other write path, except `init`, which records the starting definitions as version 1 by `person:founder` before a policy exists.

## 5. Signals and measurement

**Signals.** Every question is a structured row (§3). Email addresses and long numbers are removed before storage, session ids are hashed, and `purge-signals` deletes rows past a retention period. Unmet questions are grouped by `signals --unmet`.

**Measures.** Each kind names its measure in `kinds.json`:
- `answers`: answered, and not marked unhelpful.
- `routing-rules`: routed to a named team, and not marked as the wrong team.
- `checks`, `policy`: the share of later changes that were kept rather than undone.

**At release** the change records a baseline (the measure over the recent questions it would have affected), a target (baseline plus the policy's minimum gain), a window (questions in the candidate arm) and a tolerance.

**Exposure.** A question is counted for a change only when the change could affect its outcome: the change's definition is the answer or rule chosen with or without the change. Arms are assigned by a hash of the change and the session, so a session always sees the same arm.

**Decision** once the window is full: **undo** when the candidate arm is worse than the baseline or the control arm by more than the tolerance; **keep** when it reaches the target; otherwise **revise**, which leaves the change where it is for a person.

## 6. Policy and the dial

The policy is one definition (`policy/main`), versioned like any other. For each kind it sets a dial and limits.

| Dial | Name | Who may propose | Release |
|---:|---|---|---|
| 0 | Engineers only | Nobody: only engineers, in code | — |
| 1 | Self-serve | People | A person releases |
| 2 | Drafted | People, the AI | A person releases |
| 3 | Carried | People, the AI, the product | A person approves; the product carries release, measurement and keep |
| 4 | Pre-approved | As 3 | AI and product changes within limits ship without a person |
| 5 | Self-chosen | As 4 | The product also chooses what to change (drafts answers for frequent unmet questions) |

**Limits per kind:** the share of traffic a release starts at, a daily cap on changes shipped without a person, protected keys only people may change, and the measurement window, minimum gain and tolerance.

**Invariants held in code** (`answerdesk/policy.py`), which no policy version can change:
- AI and the product may not remove definitions, change protected keys, or change or remove a check (they may add checks).
- The policy never ships without a person (its dial is capped at 3), except a change that only lowers dials, which the product may make.
- A dial rises one step at a time, and only when the kind's record shows at least `min_kept` kept changes and at most `max_reversal_rate` undone. The rule in force decides, so a raise cannot loosen the rule in the same change.
- Undoing a policy change needs a person.

**Starting dials:** answers 3, routing rules 3, checks 3, policy 1.

**Losing autonomy is automatic.** When reversals of pre-approved changes of one kind reach `demote_after_reversals`, the scheduler lowers that kind's dial by one, through the door. Other kinds are untouched.

## 7. Checks that grow

A check is a question and the outcome it must get (`checks` kind). Before a change to answers or routing rules is released, every check runs against today's definitions and against them with the change applied. A change that makes a passing check fail is rejected. A check that fails today records a known problem: it does not block unrelated changes, the change that fixes it is reported as fixing it, and from then on it guards against the problem returning.

Checks grow from two kinds of failure, both through the door:
- **Flagged failure.** Staff mark an answer unhelpful and say what it should have been; the scheduler proposes a check from it.
- **Wrong pass.** When a change that passed every check is reversed for making things worse, the scheduler records a `wrong_pass` event against the check versions that passed it, and proposes a check from the first failed question, expecting what the stable version gives.

## 8. The loop improves itself

Checks and the policy are kinds of change, so they are versioned, proposed, checked, released, undone and measured like answers. A check or policy change is measured by the share of later changes that were kept. Raising autonomy requires a measured record (§6), and repeated reversals lower it. Wrong passes are recorded against the checks that missed them and become new checks.

## 9. Self-description

`describe` prints a capability map in JSON: the kinds of change with their fields, measures, dial, who may propose, limits and the number of definitions; the door's steps; the actors; the policy invariants; and every operation with its arguments. The operations table (`answerdesk/describe.py`) is the single definition the command-line parser is generated from, so the map cannot drift from what the product accepts.

## 10. Recovery

- **Undo** of any version in one step: a candidate is withdrawn; a kept version is replaced by the version it replaced. Undo is one step at a time, so a later version must be undone first.
- **Off switch** per change, at once, by a person or the product; a person can switch it back on.
- **Backup** copies the whole store; **restore** writes it into a fresh location only, checks integrity and schema version, and refuses to overwrite.
- **Schema migrations** go up and down.

## 11. Limits of this design and of the build

- One process and one SQLite file. No concurrency control beyond SQLite's, no service, no tenants.
- No authentication: the command line takes the actor's name on trust (`--as person:NAME`) and only accepts people there. A real product needs identities, scoped tokens and approval by someone other than the author.
- The AI drafter is a deterministic rule-based stand-in (`answerdesk/drafter.py`), not a language model. A real model would plug in behind the same interface; it would then need evaluation sets, cost limits and injection defences of its own.
- Answer Desk ships no code changes through its loop, so there is no code release to roll back in the product. Code changes are the team's work, through their delivery process.
- Measurements use simple rates on small windows, with no statistical test.
- Changes to checks and policy are measured and a recommendation is recorded, but they are not reversed automatically.
- Only answers are drafted by the product at the top of the dial; it does not yet choose work across other kinds, and it does not cluster unmet questions into themes.
