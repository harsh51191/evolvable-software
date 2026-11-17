# OpenHands (Agent Canvas + software-agent-sdk): how ready it is to evolve itself

A plain-language reading of an EVOLVE 0.7.0 assessment. Date 2026-09-30.

## In one paragraph

Built to Level 1, Configurable: the people running the product can make the changes they need most without engineers, and can undo them. Not yet proven in operation. In practice, someone running the product makes the change in the product itself, and can undo it. The biggest thing holding it back is that nobody knows how much load each part of the product can take until something breaks.

## Where it stands

The product is read on three loops. Its overall level is the lower of the first two; the third is reported beside it.

**From request to release.** Can the product take a user's request, build it properly and release it?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the loop's own steps, the shared release steps and technical foundation.
- Proven: not evidenced.

**From problem to fix.** Can the product find the problems users face, fix them and release the fix?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the loop's own steps, the shared release steps and technical foundation.
- Proven: not evidenced.

**From unmet need to new offering.** Can the product notice needs it does not serve yet, and propose or launch something for them?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the loop's own steps and technical foundation.
- Proven: not evidenced.

Built to says what the product ships and can do. Proven says what operating records show it has done. The two are reported separately and never added together.

## The kinds of change

The changes the people running the product most often need, and how far each has come.

| Kind of change | Who makes it | How far it has come | Main kind |
|---|---|---|---|
| Scheduled and event-driven automations | users and organisation admins | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Skills, plugins and tool servers the agent uses | users | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Which models it uses and how the agent behaves | users | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Which agent actions need a person's approval | users | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | No |
| Interface extensions and themes | users and organisation admins | Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand. | No |

3 of 3 main kinds are self-serve. Self-serve means: the people running the product make this kind of change themselves, without a release, and can undo it.

## What works today

The strongest parts of the product, rated 3 or more out of 4.

- **Fast, safe delivery:** Parts of the product release separately.
- **Change without engineers:** Other systems told when things happen; New connections by matching fields.
- **Oversight and limits:** Customisations survive product upgrades.
- **Safe AI features:** AI works from the product's own data; The AI sees only what the user may; Maintained test cases for AI features; A full record of AI actions; and 1 more.

## What holds it back

What each loop lacks for its next level, most widely felt first.

- **Technical foundation.** Nobody knows how much load each part of the product can take until something breaks. Holds back all three loops.
- **Technical foundation.** Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs. Holds back all three loops.
- **Build the change.** The product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one. Holds back: From request to release, on the way to Level 2; From problem to fix, on the way to Level 2.
- **Take in the request.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from. Holds back: From request to release, on the way to Level 2.
- **Propose what to change.** The product shows data but does not turn it into ranked suggestions for change with evidence and expected gain. Holds back: From problem to fix, on the way to Level 2.
- **Spot unmet needs.** Failed searches and unsupported requests are not gathered into themes that show what users want and cannot get. Holds back: From unmet need to new offering, on the way to Level 2.
- **Propose what to change.** The product does not propose new things to offer by itself, with evidence, for a person to decide. Holds back: From unmet need to new offering, on the way to Level 2.

## Safety gates

Safety gates must all pass before the product may carry changes from start to finish (Level 3). 0 of 6 that apply have passed.

| Safety gate | Status | Why it matters |
|---|---|---|
| Undo for every change people and AI make in the product | Not yet | Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand. |
| Undo for a new version of the code | Does not apply |  |
| Safe changes to how data is stored | Not yet | Without it, a small change can lock the product or lose data. |
| Backups that are proven to restore | Not yet | Without it, a mistake that undo cannot reach is permanent, because nobody knows whether the backup works. |
| Customer organisations kept apart | Not yet | Without it, one customer organisation could see another's data or slow the product down for everyone. |
| Security checks built into every change | Not yet | Without it, changes that arrive faster than people can review them will carry security holes into the product. |
| Limits and checks on changes the product makes to itself | Not yet | Without it, one bad change the product makes on its own can spread widely before anyone looks. |

## How much AI does

How far the product's own AI carries each loop. Level 1 is people changing the product, so AI counts from Level 2, and never above the loop's own level.

- From request to release: AI does none of the steps on its own yet.
- From problem to fix: AI does none of the steps on its own yet.
- From unmet need to new offering: AI does none of the steps on its own yet.

Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

How safe its AI features are to run for real customers: 1 out of 4. The weakest area sets this.

- What the AI knows and may see: 3 out of 4.
- How AI quality is tested: 2 out of 4.
- How AI actions are controlled: 1 out of 4.
- How the AI runs day to day: 2 out of 4.
- The AI sees only what the user may: passed.
- Worse AI results block a release: not yet.
- A full record of AI actions: passed.

Whatever else improves, it cannot rise above 2 until these pass: Worse AI results block a release.

## Does the loop improve itself

Do the checks, tests and rules that govern change get better from results? A loop whose checks never improve repeats its mistakes faster.

**Fixed** (step 0 of 4). The checks, tests and rules that govern change improve only when engineers rewrite them in code.

## Has it been proven

Not yet proven in operation.

- From request to release: not evidenced. The rater looked for operating records and found none that show it.
- From problem to fix: not evidenced. The rater looked for operating records and found none that show it.
- From unmet need to new offering: not evidenced. The rater looked for operating records and found none that show it.

This reading comes from the product's code and documents alone. Nobody observed the product in operation, so the reading cannot say what it has been seen to do.

Built says what the product can do; proven says what it has been seen to do. A product should run at the level it has proven, and take on more as the proof grows.

## How sure this reading is

Of the 67 answers based on evidence, 11 are held with high confidence (the rater read the code and its tests), 32 with medium confidence (the rater read the code, but not every path through it) and 24 with low confidence (inferred from part of the evidence).

For the kinds of change: 0 high, 3 medium and 2 low.

Check these first. The rater was least sure of them, and each one decides a level or a safety gate:

- Known limits, tested regularly: holds From request to release, on the way to Level 2; From problem to fix, on the way to Level 2; From unmet need to new offering, on the way to Level 2.
- Backups that are proven to restore: holds From request to release, on the way to Level 2; From problem to fix, on the way to Level 2; From unmet need to new offering, on the way to Level 2; the safety gate backups that are proven to restore.
- Requests become clear change plans: holds From request to release, on the way to Level 2.
- AI builds accepted changes: holds From request to release, on the way to Level 2; From problem to fix, on the way to Level 2.
- Ranked suggestions for change, with evidence: holds From problem to fix, on the way to Level 2.
- Self-made changes tested before use: holds the safety gate limits and checks on changes the product makes to itself.
- Firm limits on self-made changes: holds the safety gate limits and checks on changes the product makes to itself.
- Notices needs it does not serve: holds From unmet need to new offering, on the way to Level 2.
- Proposes new things to offer: holds From unmet need to new offering, on the way to Level 2.

The reading answers 75 questions: 67 from evidence, 0 where no evidence was found (counted as missing), and 8 that do not apply to this product.

The evidence behind the answers: 67 checked in the code, 0 taken from the product's own documents or settings and 0 inferred from other material.

Neither the higher readings some evidence also supports, nor settings that ship switched off, would change any level.

The overall level would drop if any of these were rated one step lower: Notices where users struggle; History and undo for every setting.

The reading treats the product as follows:

- It stores data that must not be lost.
- Changes to it can alter how data is stored.
- One installation serves several customer organisations that must be kept apart.
- It runs all the time as an online service.
- AI agents or other software can change its data or settings.
- Its own AI can change its settings, skills, memory or data.
- Its behaviour is changed through settings and rules.
- It has AI features.
- Its AI can read the product's data.
- Its AI can change data or settings, send messages outside the product or spend money.

This is one rater's reading of the evidence. A second, independent reading may differ.

## What to do next

**From request to release, to Level 2, Assisted.** The check to run on the live product: A user describes a change in plain words inside the product. The product records it with structure (what, for whom, where) and drafts the change for a person to finish. Every change, drafted or not, passes automatic checks before it goes live, and a change that fails them is stopped.

**From problem to fix, to Level 2, Assisted.** The check to run on the live product: Cause a real failure. The product explains why it happened, with evidence, proposes what to change, and drafts the change for a person to finish.

For the overall level to rise, both checks must pass.

- For a plan of milestones that starts from a business goal, run `python3 scripts/blueprint.py <assessment.json> --goal "<business goal>"`.
- For the full list of what the next assessment must find, run `python3 scripts/score.py <assessment.json> --checklist 2`.

## For engineers

Headline as the scorer prints it: **Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)**

AI Readiness as the scorer prints it: AI Readiness L1 (Experimental) · Context 3 · Quality 2 · Governance 1 · Operations 2 · not production-governed.

Recursion: 0 Fixed (LRN-10 at 0). 3 of 3 main kinds are self-serve.

Next-level blockers in the scorer's terms:

- Request → Release to L2: spine Build needs product build path ≥ 2 (has DEL-04 1); stages Intake needs DEL-01 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- Issue → Fix to L2: spine Build needs product build path ≥ 2 (has DEL-04 1, LRN-07 1); stages Propose needs LRN-06 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)
- Opportunity → Expansion to L2: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0); architecture Foundation needs every applicable ARC ≥ 1 (has ARC-06 0, ARC-09 0)

| Plain name | Code | Score |
|---|---|---|
| Fast lists and searches as data grows | ARC-01 | does not apply |
| Safe changes to how data is stored | ARC-02 | 2 |
| More capacity by adding servers | ARC-03 | 2 |
| Reliable background work | ARC-04 | 2 |
| Customer organisations kept apart | ARC-05 | 2 |
| Known limits, tested regularly | ARC-06 | 0 |
| Service targets, watched with alerts | ARC-07 | 1 |
| One failure does not spread | ARC-08 | 2 |
| Backups that are proven to restore | ARC-09 | 0 |
| Requests become clear change plans | DEL-01 | 0 |
| Parts of the product release separately | DEL-02 | 3 |
| Internal boundaries checked automatically | DEL-03 | 2 |
| AI builds accepted changes | DEL-04 | 1 |
| Automatic checks before any change lands | DEL-05 | 2 |
| The product reports what is running | DEL-06 | 2 |
| A fresh test copy for each change | DEL-07 | 2 |
| User journeys tested automatically | DEL-08 | 2 |
| Release to a small group first | DEL-09 | 2 |
| Off switch for any change | DEL-10 | 2 |
| Undo for a new version of the code | DEL-11 | does not apply |
| New kinds of records without engineering | MAL-01 | does not apply |
| New fields with built-in checks | MAL-02 | does not apply |
| Links and statuses set without engineers | MAL-03 | does not apply |
| Other software can use new records | MAL-04 | does not apply |
| Changes reach other software at once | MAL-05 | does not apply |
| An interface other software can explore | MAL-06 | 2 |
| Page layouts changed without engineers | MAL-07 | 2 |
| Screens appear for new records | MAL-08 | does not apply |
| Branding and wording changed without engineers | MAL-09 | 2 |
| Automatic rules people can set up | MAL-10 | 2 |
| Other systems told when things happen | MAL-11 | 3 |
| Custom logic that runs safely | MAL-12 | 2 |
| Add-ons can extend most of the product | MAL-13 | 2 |
| Outside code runs fenced off | MAL-14 | 1 |
| Add-on builders can test before publishing | MAL-15 | 2 |
| New connections by matching fields | MAL-16 | 3 |
| A kit for building connectors | MAL-17 | 2 |
| Stable, versioned interfaces for other software | MAL-18 | 2 |
| Ready-made tools for AI agents | MAL-19 | 2 |
| Use and change the product by chat | MAL-20 | 2 |
| Usage data available within minutes | LRN-01 | 2 |
| Feedback tied to what it concerns | LRN-02 | 1 |
| Notices where users struggle | LRN-03 | 2 |
| Usage, feedback, errors and changes joined | LRN-04 | 1 |
| Works out why a problem happens | LRN-05 | 2 |
| Ranked suggestions for change, with evidence | LRN-06 | 0 |
| Learns from its own use, unprompted | LRN-07 | 1 |
| Self-made changes tested before use | LRN-08 | 1 |
| Every change measured after release | LRN-09 | 1 |
| The checks themselves get better | LRN-10 | 0 |
| Accessibility built in and checked | GOV-01 | 1 |
| One record of every change | GOV-02 | 1 |
| Personal data marked, exportable and erasable | GOV-03 | 1 |
| Security checks built into every change | GOV-04 | 1 |
| History and undo for every setting | GOV-05 | 2 |
| Propose, preview, review, then apply | GOV-06 | 1 |
| Written rules for what needs approval | GOV-07 | 2 |
| Customisations survive product upgrades | GOV-08 | 3 |
| Safe actions for AI and automation | GOV-09 | 2 |
| Firm limits on self-made changes | GOV-10 | 1 |
| Protection against planted instructions | GOV-11 | 1 |
| A general-purpose core | EXP-01 | 2 |
| New business areas without core changes | EXP-02 | 2 |
| Ready-made packages for a business area | EXP-03 | 2 |
| Notices needs it does not serve | EXP-04 | 0 |
| Proposes new things to offer | EXP-05 | 0 |
| Trial launches, kept or removed on results | EXP-06 | 1 |
| AI works from the product's own data | AIR-03 | 3 |
| The AI sees only what the user may | AIR-04 | 3 |
| Maintained test cases for AI features | AIR-05 | 3 |
| Worse AI results block a release | AIR-06 | 2 |
| A full record of AI actions | AIR-07 | 3 |
| Changeable AI models, planned failure handling | AIR-01 | 3 |
| AI spending limits per customer | AIR-02 | 2 |
| AI quality watched in real use | AIR-08 | 1 |
