# The approach: how to make a product evolve itself

One method for products that exist and one for products not yet built. Both end in the same loop. Each step says what to run, and what has to be true before you move on.

## The idea in one paragraph

A product evolves itself when the people running it, and then the product itself, can make the changes users need, safely, without waiting for engineers. So the work always starts from the **kinds of change** users need, such as an answer, a rule, a workflow or a connection. Then it asks how far each kind has come: engineers only, self-serve with undo, drafted by the product, carried end to end, pre-approved under rules, or self-chosen. A level is earned only when a fresh assessment finds the work, running and on by default. A level is worth something only when a real measure moves with it.

## Existing products

**1. Assess.**
- In ten minutes, `quick_scan.py` gives a likely range.
- In hours, the skill gives a full assessment with evidence.
- The part that matters most is the list of kinds of change, and which ones people cannot make or undo themselves.

**2. Take the three next moves.** Run `recommend.py assessment.json`. It always gives three moves:

| Move | What it is | Why this one |
|---|---|---|
| 1. For the people running it | The main kind of change furthest behind, moved one step: engineers only to self-serve with undo, self-serve to drafted, drafted to carried | This is what users notice. No AI lane lifts a product until it serves a main kind of change. |
| 2. For the loop | The one stage that most holds the product back: turning requests into plans, noticing problems, explaining them, or proposing fixes | Moves 1 and 3 make change possible and safe; this one makes the product help. |
| 3. For safety | The control the next level needs, or else the Level 3 control nearest to passing | The safety net is ready before autonomy grows. It is never the only recommendation. |

Each move comes with:
- what users get;
- the evidence it starts from;
- a measure to track in real use;
- a "done when" list;
- a prompt for a coding agent.

The tool re-runs the scorer with the moves landed, so it says whether the three moves reach the next level. If they don't, it lists the rest of the way. Use `blueprint.py` only when you need the road over several levels.

**3. Ship each move on by default.** A feature behind an optional setting counts only toward the opt-in reading, never the level. The Brand AI Apps trial showed why: an AI drafting feature built behind three unset environment variables moved nothing for any user.

**4. Measure for two to four weeks.** Track the measure each move names. Examples:
- the share of credential changes made without an engineer;
- the time from a problem being recorded to its cause being known.

**5. Re-assess blind.** A rater who has not seen the plan assesses again. The level counts only if that assessment finds the work.
- If the level moved but the measure did not, the move was the wrong one: record it in the product's own log, and pick again.
- If the measure moved but the level did not, the rubric may be missing something: record that in `evals/disagreements.md`.

**6. Repeat.** Never have more than three moves in flight. Never chase a criterion that changes nothing a user can see, unless it is a safety control the next level needs.

## New products

**1. Name the kinds of change before the data model.** List the five to eight things the people running the product will change most often. Store them as versioned data, not code. Give every one a supported way to change it, and undo, from the first release. This is foundation 1 of [Born evolvable](born-evolvable.md).

**2. Build the twelve foundations.** They are in [Born evolvable](born-evolvable.md). For example:
- one door for every change;
- signals captured from the first user;
- limits written down outside the AI;
- release to a small group first, with an off switch.

A design assessment (`--basis design`) gives a "Designed for" reading. A product can be designed for Level 5 on day one.

**3. Ship with the dial low.** The first release should be Built to Level 1: every main kind self-serve with undo, and nothing behind optional settings. Raise autonomy one kind of change at a time. [Answer Desk](../examples/born-evolvable/) is a worked example: designed for Level 5 and built to Level 1.

**4. Then run the same loop as an existing product**, from step 2.

## What the field test taught, and why the approach looks like this

- **Undo is the gap users feel.** No product of the eleven reaches Level 3. Definition rollback fails in all of them: credentials in n8n, memory in OpenClaw and Hermes, tool connections in LibreChat, the data model in Directus.
- **AI ahead of the safety net does not count.** n8n's AI builds workflows, yet its credentials cannot be undone. LibreChat's agent writes skills, but users cannot undo a change to a tool connection. A lane that drafts something nobody relies on lifts nothing.
- **One rater is not enough.** Blind second ratings matched 98% of scores within one point. Even so, two of three overall levels differed, each on one judgement about kinds of change. Those judgements are now rules. Re-assess blind before you claim a level.
- **Plans fail in predictable ways.** The Brand AI Apps plan targeted a kind of change owners could already make, and its feature shipped switched off. Hence moves start from the kinds people cannot make, and must be on by default.
