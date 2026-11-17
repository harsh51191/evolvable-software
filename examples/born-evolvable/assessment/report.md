# Answer Desk: how ready it is to evolve itself

A plain-language reading of an EVOLVE 0.7.0 assessment. Date 2026-11-17.

## In one paragraph

Built to Level 1, Configurable: the people running the product can make the changes they need most without engineers, and can undo them. Not yet proven in operation. In practice, someone running the product makes the change in the product itself, and can undo it. The biggest thing holding it back is that the product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one.

## Where it stands

The product is read on three loops. Its overall level is the lower of the first two; the third is reported beside it.

**From request to release.** Can the product take a user's request, build it properly and release it?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the shared release steps.
- Proven: not evidenced.

**From problem to fix.** Can the product find the problems users face, fix them and release the fix?

- Built to Level 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.
- Held at this level by the loop's own steps; the shared release steps; technical foundation; oversight and limits.
- Proven: not evidenced.

**From unmet need to new offering.** Can the product notice needs it does not serve yet, and propose or launch something for them?

- Built to Level 0, Manual. The changes that matter most are made by engineers writing and releasing code.
- Held at this level by the shared release steps.
- Proven: not evidenced.

Built to says what the product ships and can do. Proven says what operating records show it has done. The two are reported separately and never added together.

## The kinds of change

The changes the people running the product most often need, and how far each has come.

| Kind of change | Who makes it | How far it has come | Main kind |
|---|---|---|---|
| What the desk tells customers | support lead | Drafted. The product drafts this kind of change, and a person completes and releases it. | Yes |
| Which team gets a question the desk cannot answer | support lead | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| The questions every change is checked against | support lead; the product from failures | Drafted. The product drafts this kind of change, and a person completes and releases it. | No |
| What may change without a person, and within which limits | product owner | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | No |
| The help-centre pages the drafter copies from | support lead or content owner | Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand. | No |
| How questions are matched, and the reply sent when a question is passed on | support lead | Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand. | No |

2 of 2 main kinds are self-serve. Self-serve means: the people running the product make this kind of change themselves, without a release, and can undo it.

## What works today

The strongest parts of the product, rated 3 or more out of 4.

- **Technical foundation:** Backups that are proven to restore.
- **Fast, safe delivery:** Off switch for any change.
- **Learning from use:** Usage data available within minutes; Self-made changes tested before use; Every change measured after release; The checks themselves get better.
- **Oversight and limits:** Propose, preview, review, then apply; Written rules for what needs approval; Firm limits on self-made changes.

## What holds it back

What each loop lacks for its next level, most widely felt first.

- **Build the change.** The product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one. Holds back: From request to release, on the way to Level 2; From problem to fix, on the way to Level 3.
- **Check the change.** Some kinds of change, or drafts, can take effect without passing automatic checks. Holds back: From problem to fix, on the way to Level 3.
- **Check the change.** The running product cannot report its version, its health and its live settings in a form software can read. Holds back: From problem to fix, on the way to Level 3.
- **Undo it.** Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to. Holds back: From problem to fix, on the way to Level 3.
- **Notice the problem.** The product does not yet notice and raise, by itself, the places where users struggle. Holds back: From problem to fix, on the way to Level 3.
- **Work out the cause.** The product reports problems but does not work out their likely cause, so people have to investigate each one. Holds back: From problem to fix, on the way to Level 3.
- **Propose what to change.** The product shows data but does not turn it into ranked suggestions for change with evidence and expected gain. Holds back: From problem to fix, on the way to Level 3.
- **Technical foundation.** Lists and searches, including on fields people added themselves, are not set up to stay fast as data grows. Holds back: From problem to fix, on the way to Level 3.
- **Technical foundation.** A failing connected system, add-on or AI provider can take down more than the feature that uses it. Holds back: From problem to fix, on the way to Level 3.
- **Technical foundation.** Changes to how data is stored are not tested on realistic data, or can cause downtime or data loss. Holds back: From problem to fix, on the way to Level 3.
- **Oversight and limits.** Security scans do not block unsafe changes, or permissions have to be added by hand for each new kind of record. Holds back: From problem to fix, on the way to Level 3.
- **Oversight and limits.** A product upgrade can break what customer organisations have customised, and repairing it is manual work. Holds back: From problem to fix, on the way to Level 3.
- **Oversight and limits.** AI agents and automated tools act with broad or shared access, without previews, rate limits or a record tied to each one. Holds back: From problem to fix, on the way to Level 3.
- **Build the change.** Serving a new business area needs changes to the product's core, and none has yet been added through settings and rules alone. Nor does the product build the change itself yet. Holds back: From unmet need to new offering, on the way to Level 1.

## Safety gates

Safety gates must all pass before the product may carry changes from start to finish (Level 3). 2 of 5 that apply have passed.

| Safety gate | Status | Why it matters |
|---|---|---|
| Undo for every change people and AI make in the product | Not yet | Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand. |
| Undo for a new version of the code | Does not apply |  |
| Safe changes to how data is stored | Not yet | Without it, a small change can lock the product or lose data. |
| Backups that are proven to restore | Passed |  |
| Customer organisations kept apart | Does not apply |  |
| Security checks built into every change | Not yet | Without it, changes that arrive faster than people can review them will carry security holes into the product. |
| Limits and checks on changes the product makes to itself | Passed |  |

## How much AI does

How far the product's own AI carries each loop. Level 1 is people changing the product, so AI counts from Level 2, and never above the loop's own level.

- From request to release: AI does none of the steps on its own yet.
- From problem to fix: AI does none of the steps on its own yet.
- From unmet need to new offering: AI does none of the steps on its own yet.

Engineers are not seen building this product with AI coding agents or a delivery framework. Any self-evolution scored here is the product's own.

The product has no AI features, so the checks on AI features do not apply.

## Does the loop improve itself

Do the checks, tests and rules that govern change get better from results? A loop whose checks never improve repeats its mistakes faster.

**Results-driven** (step 3 of 4). The product records which check missed each failure and proposes better checks, tests and rules, which a person approves.

## Has it been proven

Not yet proven in operation.

- From request to release: not evidenced. The rater looked for operating records and found none that show it.
- From problem to fix: not evidenced. The rater looked for operating records and found none that show it.
- From unmet need to new offering: not evidenced. The rater looked for operating records and found none that show it.

This reading comes from the product's code and documents alone. Nobody observed the product in operation, so the reading cannot say what it has been seen to do.

Built says what the product can do; proven says what it has been seen to do. A product should run at the level it has proven, and take on more as the proof grows.

## How sure this reading is

Of the 53 answers based on evidence, 20 are held with high confidence (the rater read the code and its tests), 31 with medium confidence (the rater read the code, but not every path through it) and 2 with low confidence (inferred from part of the evidence).

For the kinds of change: 5 high, 1 medium and 0 low.

Check these first. The rater was least sure of them, and each one decides a level or a safety gate:

- AI builds accepted changes: holds From request to release, on the way to Level 2; From problem to fix, on the way to Level 3; From unmet need to new offering, on the way to Level 1.
- Customisations survive product upgrades: holds From problem to fix, on the way to Level 3.

The reading answers 75 questions: 53 from evidence, 0 where no evidence was found (counted as missing), and 22 that do not apply to this product.

The evidence behind the answers: 53 checked in the code, 0 taken from the product's own documents or settings and 0 inferred from other material.

With the higher readings some evidence also supports, From request to release would read Level 2, Assisted; From unmet need to new offering would read Level 1, Configurable. The overall level would be Level 2, Assisted.

The overall level would drop if any of these were rated one step lower: Notices where users struggle; History and undo for every setting.

The reading treats the product as follows:

- It stores data that must not be lost.
- Changes to it can alter how data is stored.
- AI agents or other software can change its data or settings.
- Its own AI can change its settings, skills, memory or data.
- Its behaviour is changed through settings and rules.

This is one rater's reading of the evidence. A second, independent reading may differ.

## What to do next

**From request to release, to Level 2, Assisted.** The check to run on the live product: A user describes a change in plain words inside the product. The product records it with structure (what, for whom, where) and drafts the change for a person to finish. Every change, drafted or not, passes automatic checks before it goes live, and a change that fails them is stopped.

**From problem to fix, to Level 3, Supervised.** The check to run on the live product: Break something on purpose. Without being asked, the product raises it as an issue with the users affected and how often, works out why, proposes a fix with evidence, and releases it after a person approves: to a small group first, measured, and with undo. The safety drill from the request-to-release check must also pass.

For the overall level to rise, both checks must pass.

- For a plan of milestones that starts from a business goal, run `python3 scripts/blueprint.py <assessment.json> --goal "<business goal>"`.
- For the full list of what the next assessment must find, run `python3 scripts/score.py <assessment.json> --checklist 2`.

## For engineers

Headline as the scorer prints it: **Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L2 (AI L0) · Opportunity → Expansion L0 (AI L0)**

AI Readiness as the scorer prints it: no AI features.

Recursion: 3 Results-driven (LRN-10 at 3). 2 of 2 main kinds are self-serve.

Next-level blockers in the scorer's terms:

- Request → Release to L2: spine Build needs product build path ≥ 2 (has DEL-04 1)
- Issue → Fix to L3: spine Build needs product build path ≥ 3 (has DEL-04 1, LRN-07 2); spine Verify needs DEL-05 ≥ 3 (has 2); spine Verify needs DEL-06 ≥ 3 (has 2); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Detect needs LRN-03 ≥ 3 (has 2); stages Diagnose needs LRN-05 ≥ 3 (has 2); stages Propose needs LRN-06 ≥ 3 (has 2); architecture Foundation needs every applicable ARC ≥ 2 (has ARC-01 1, ARC-08 1); architecture Foundation needs ARC-02 ≥ 3 (has 2); governance Ceiling needs GOV-04 ≥ 3 (has 1); governance Ceiling needs GOV-08 ≥ 2 (has 1); governance Ceiling needs GOV-09 ≥ 2 (has 0)
- Opportunity → Expansion to L1: spine Build needs people build path ≥ 2 or product build path ≥ 2 (has EXP-02 n/a; DEL-04 1, EXP-03 n/a)

| Plain name | Code | Score |
|---|---|---|
| Fast lists and searches as data grows | ARC-01 | 1 |
| Safe changes to how data is stored | ARC-02 | 2 |
| More capacity by adding servers | ARC-03 | does not apply |
| Reliable background work | ARC-04 | does not apply |
| Customer organisations kept apart | ARC-05 | does not apply |
| Known limits, tested regularly | ARC-06 | does not apply |
| Service targets, watched with alerts | ARC-07 | does not apply |
| One failure does not spread | ARC-08 | 1 |
| Backups that are proven to restore | ARC-09 | 3 |
| Requests become clear change plans | DEL-01 | 2 |
| Parts of the product release separately | DEL-02 | 0 |
| Internal boundaries checked automatically | DEL-03 | 1 |
| AI builds accepted changes | DEL-04 | 1 |
| Automatic checks before any change lands | DEL-05 | 2 |
| The product reports what is running | DEL-06 | 2 |
| A fresh test copy for each change | DEL-07 | 2 |
| User journeys tested automatically | DEL-08 | 2 |
| Release to a small group first | DEL-09 | 2 |
| Off switch for any change | DEL-10 | 3 |
| Undo for a new version of the code | DEL-11 | does not apply |
| New kinds of records without engineering | MAL-01 | does not apply |
| New fields with built-in checks | MAL-02 | 2 |
| Links and statuses set without engineers | MAL-03 | does not apply |
| Other software can use new records | MAL-04 | does not apply |
| Changes reach other software at once | MAL-05 | does not apply |
| An interface other software can explore | MAL-06 | 2 |
| Page layouts changed without engineers | MAL-07 | 0 |
| Screens appear for new records | MAL-08 | does not apply |
| Branding and wording changed without engineers | MAL-09 | 1 |
| Automatic rules people can set up | MAL-10 | 2 |
| Other systems told when things happen | MAL-11 | 1 |
| Custom logic that runs safely | MAL-12 | 1 |
| Add-ons can extend most of the product | MAL-13 | 1 |
| Outside code runs fenced off | MAL-14 | 0 |
| Add-on builders can test before publishing | MAL-15 | 2 |
| New connections by matching fields | MAL-16 | 0 |
| A kit for building connectors | MAL-17 | 0 |
| Stable, versioned interfaces for other software | MAL-18 | 1 |
| Ready-made tools for AI agents | MAL-19 | 2 |
| Use and change the product by chat | MAL-20 | 1 |
| Usage data available within minutes | LRN-01 | 3 |
| Feedback tied to what it concerns | LRN-02 | 2 |
| Notices where users struggle | LRN-03 | 2 |
| Usage, feedback, errors and changes joined | LRN-04 | 2 |
| Works out why a problem happens | LRN-05 | 2 |
| Ranked suggestions for change, with evidence | LRN-06 | 2 |
| Learns from its own use, unprompted | LRN-07 | 2 |
| Self-made changes tested before use | LRN-08 | 3 |
| Every change measured after release | LRN-09 | 3 |
| The checks themselves get better | LRN-10 | 3 |
| Accessibility built in and checked | GOV-01 | 0 |
| One record of every change | GOV-02 | 2 |
| Personal data marked, exportable and erasable | GOV-03 | 2 |
| Security checks built into every change | GOV-04 | 1 |
| History and undo for every setting | GOV-05 | 2 |
| Propose, preview, review, then apply | GOV-06 | 3 |
| Written rules for what needs approval | GOV-07 | 3 |
| Customisations survive product upgrades | GOV-08 | 1 |
| Safe actions for AI and automation | GOV-09 | 0 |
| Firm limits on self-made changes | GOV-10 | 3 |
| Protection against planted instructions | GOV-11 | 2 |
| A general-purpose core | EXP-01 | does not apply |
| New business areas without core changes | EXP-02 | does not apply |
| Ready-made packages for a business area | EXP-03 | does not apply |
| Notices needs it does not serve | EXP-04 | 2 |
| Proposes new things to offer | EXP-05 | 1 |
| Trial launches, kept or removed on results | EXP-06 | 2 |
| AI works from the product's own data | AIR-03 | does not apply |
| The AI sees only what the user may | AIR-04 | does not apply |
| Maintained test cases for AI features | AIR-05 | does not apply |
| Worse AI results block a release | AIR-06 | does not apply |
| A full record of AI actions | AIR-07 | does not apply |
| Changeable AI models, planned failure handling | AIR-01 | does not apply |
| AI spending limits per customer | AIR-02 | does not apply |
| AI quality watched in real use | AIR-08 | does not apply |
