# Answer Desk: a small product born evolvable

Answer Desk is a tiny help-desk answering service. It answers customers' questions from written answers, and passes the rest to the right team. It exists to show the twelve foundations in [`docs/born-evolvable.md`](../../docs/born-evolvable.md) working together in code that runs and is tested: people, an AI and the product itself all change it through one door, every change can be undone, every change is measured, written limits are enforced in code, and the loop's own checks and policy change through the same door.

It is a toy (see [What this is not](#what-this-is-not)). The design is in [`DESIGN.md`](DESIGN.md).

Python 3.9 or later, standard library only (SQLite 3.24 or later, which every supported Python ships). No network. Deterministic tests.

## The five-minute walkthrough

```bash
cd examples/born-evolvable
python3 walkthrough.py
```

It runs one story on a fresh, temporary store, with a fixed clock and simulated customers, and prints each step:

1. **Start.** Three answers, two routing rules, two checks and a policy. Answers and routing rules start at dial 3 (a person approves each release); the policy at dial 1 (people only).
2. **A request arrives.** Customers ask "How do I export my invoices?". The desk cannot answer, routes them to billing, and records each question as a signal. `signals --unmet` groups them.
3. **An AI draft.** The AI drafter (a rule-based stand-in, not a model) drafts an answer from `sources/help-centre.md`. The door checks it; the policy says a person approves; a person approves it.
4. **Gradual release and measurement.** It goes to half the sessions, with a baseline, a target and a window recorded. After more questions the product's scheduler measures it (answered in every candidate session, none in the control) and keeps it.
5. **An automatic reversal.** The AI drafts a "password rules" answer. It passes every check and a person approves it, but it also catches "How do I change my password?". The measure falls well below the control, so the scheduler reverses it, records a *wrong pass* against the checks that let it through, and proposes a new check from the failed question.
6. **A failure becomes a check.** A person approves the check. The same draft is now rejected at the door. A person writes a narrower answer; it passes the new check, is measured and kept.
7. **A limit enforced in code.** The AI drafts a change to the refunds answer from a help-centre page that says 5 days instead of 10. Refunds are protected, so the policy blocks it and logs why.
8. **The loop changes through the door.** The owner proposes letting answers ship without a person (dial 4). The policy is a definition, so this goes through the door too, and is rejected: the record shows 2 kept and 1 undone, and raising needs 3 kept and at most 25% undone.
9. **Self-description.** The capability map an agent reads: kinds, dials, who may propose.

### The same by hand

Every step is also a command. Output is JSON.

```bash
export ANSWER_DESK_STORE=/tmp/desk.db        # or pass --store PATH before the command
python3 -m answerdesk init
python3 -m answerdesk ask "How do I export my invoices?" --session a
python3 -m answerdesk signals --unmet
python3 -m answerdesk draft "How do I export my invoices?"        # AI draft -> awaiting_approval (change 9)
python3 -m answerdesk approve 9 --as person:sam                    # released to 50% with a baseline
python3 -m answerdesk ask "How do I export my invoices?" --session b
python3 -m answerdesk feedback 2 --unhelpful --expected-answer exporting-invoices
python3 -m answerdesk evaluate 9                                   # keep, revise, undo or waiting
python3 -m answerdesk tick                                         # the product's scheduler, once
python3 -m answerdesk off 9 --as person:sam                        # off switch
python3 -m answerdesk undo 9 --as person:sam --reason "not ready"  # one-step undo
python3 -m answerdesk draft "Do refunds go back to my card?"       # blocked: protected
python3 -m answerdesk audit --change 10                            # why
python3 -m answerdesk propose answers opening-hours --as person:sam --body '{"keywords":["hours"],"answer":"Always open."}'
python3 -m answerdesk changes --kind answers
python3 -m answerdesk describe                                     # capability map
python3 -m answerdesk backup /tmp/desk-backup.db
python3 -m answerdesk restore /tmp/desk-backup.db --into /tmp/desk-restored.db
python3 -m answerdesk --help
```

## Tests

From the repository root:

```bash
python3 -m unittest discover -s examples/born-evolvable/tests
```

41 tests, about five seconds. They cover undo of every kind; policy blocking out-of-policy AI and product changes, the daily limit and the dial; checks rejecting regressions and re-running at approval; gradual release, the off switch and automatic reversal; wrong passes and flagged failures becoming checks; policy changes through the door, raising a dial only on a record, and automatic lowering after reversals; measurement of check changes; the product drafting by itself at dial 5; backup and restore into a fresh location; schema migrations down and up; personal data removal and retention; the capability map and the command line generated from one definition; and the walkthrough itself.

## Where each foundation lives

| # | Foundation | Where |
|---:|---|---|
| 1 | Name your kinds of change first | `kinds.json`; `answerdesk/kinds.py` |
| 2 | Store them as versioned data | `answerdesk/store.py` (`changes`, `live`); validation in `answerdesk/kinds.py`; starting data in `seed/` |
| 3 | One door for every change | `answerdesk/door.py` (`submit`, `approve`); used by `cli.py`, `app.draft` and `scheduler.py` |
| 4 | Everything can be undone | `Door.undo`, `Door.switch_off`; `Store.backup` and `Store.restore`. (`Store.migrate` down steps drop tables: they reverse the storage layout, not the data, and are a gap.) |
| 5 | Signals from the first user, privacy designed in | `answerdesk/desk.py` (`ask`, `feedback`, `redact`, `unmet`); `Store.purge_signals` |
| 6 | Every change has a goal and is measured | `Door._traffic_plan`, `Door._loop_plan`, `Door.evaluate` |
| 7 | Checks are automatic and they grow | `answerdesk/checks.py`; `Door.check`; `Door.propose_check`; `scheduler._after_reversal` |
| 8 | Limits written down, outside the AI | `answerdesk/policy.py` (`decide`, `validate`); `seed/policy.json` |
| 9 | Gradual release, off switch, automatic reversal | `desk.bucket`, `Door._release`, `Door.switch_off`, `scheduler.tick` |
| 10 | The product describes itself | `answerdesk/describe.py` (`OPERATIONS`, `capability_map`); `cli.build_parser` |
| 11 | The loop itself is changeable | `checks` and `policy` kinds in `kinds.json`; `policy.validate`; `Door._loop_plan`; wrong-pass records |
| 12 | Build for the top, start the dial low | Dials 0 to 5 in `policy.py`; starting dials in `seed/policy.json`; raise rule and automatic lowering |

The AI drafter's interface is `Drafter.draft_answer` in `answerdesk/drafter.py`. `RuleDrafter` is a **deterministic stand-in**: it picks the help-centre section that shares most words with the question and copies its first sentences. It is not a language model. A real model would implement the same method, and its drafts would go through the same door, policy and checks.

## What this is not

- **A toy.** One process, one SQLite file, a command line. No server, no tenants, no concurrency beyond SQLite's.
- **No real model.** The drafter is a rule-based stand-in, so nothing here shows how a real model behaves, what it costs, or how it resists prompt injection.
- **No real traffic.** The measurements in the walkthrough and tests come from simulated customers, and the decision rule compares simple rates over small windows, with no statistical test.
- **No identities.** The command line takes `--as person:NAME` on trust; a real product needs authentication, scoped tokens and approval by someone other than the author.
- **No code releases.** Answer Desk changes only definitions through its loop. Code changes are the team's work, through their own delivery process, and are not rolled back by the product.
- **No operating record.** It has never run in production, so nothing here proves how it behaves over time.

No readiness level was claimed before it was assessed. A blind assessment by a separate rater, who saw only the skill and this folder, is in [`assessment/`](assessment/): **Built to Level 1, Configurable; Designed for Level 1; not proven in operation.** Its plain-language report is [`assessment/report.md`](assessment/report.md).

What held it at Level 1, in the rater's words: there is no AI implementation lane (the drafter is a rule-based stand-in, which the rubric does not count as AI), undo shows no differences between versions, data-layout changes are not online and their down steps drop tables, and there is no authentication or security scanning. The rater also found places where this README and DESIGN.md claimed more than the code did; those claims are corrected here and in DESIGN.md.
