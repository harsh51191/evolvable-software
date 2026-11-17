# PostHog: how ready it is to evolve itself

A plain-language reading of an EVOLVE 0.7.0 assessment. Date 2026-09-30.

## In one paragraph

Built to Level 1, Configurable: the people running the product can make the changes they need most without engineers, and can undo them. Not yet proven in operation. In practice, someone running the product makes the change in the product itself, and can undo it. The biggest thing holding it back is that the product reports problems but does not work out their likely cause, so people have to investigate each one.

## Where it stands

The product is read on three loops. Its overall level is the lower of the first two; the third is reported beside it.

**From request to release.** Can the product take a user's request, build it properly and release it?

- Built to Level 2, Assisted. The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.
- Held at this level by the loop's own steps; the shared release steps; technical foundation; oversight and limits.
- Proven: not evidenced.

**From problem to fix.** Can the product find the problems users face, fix them and release the fix?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the loop's own steps.
- Proven: not evidenced.

**From unmet need to new offering.** Can the product notice needs it does not serve yet, and propose or launch something for them?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the loop's own steps.
- Proven: not evidenced.

Built to says what the product ships and can do. Proven says what operating records show it has done. The two are reported separately and never added together.

## The kinds of change

The changes the people running the product most often need, and how far each has come.

| Kind of change | Who makes it | How far it has come | Main kind |
|---|---|---|---|
| Charts, reports and dashboards | product and growth teams in a project | Drafted. The product drafts this kind of change, and a person completes and releases it. | Yes |
| Who sees which feature (feature flags) | engineers and product managers in a project | Drafted. The product drafts this kind of change, and a person completes and releases it. | Yes |
| A/B tests and experiments | product teams | Drafted. The product drafts this kind of change, and a person completes and releases it. | No |
| Where data is sent and how it is transformed | data and engineering teams | Drafted. The product drafts this kind of change, and a person completes and releases it. | No |
| Surveys shown to users | product and research teams | Drafted. The product drafts this kind of change, and a person completes and releases it. | No |
| New kinds of analysis and changes to PostHog's own screens | PostHog's users, through feature requests | Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it. | No |

2 of 2 main kinds are self-serve. Self-serve means: the people running the product make this kind of change themselves, without a release, and can undo it.

## What works today

The strongest parts of the product, rated 3 or more out of 4.

- **Technical foundation:** Fast lists and searches as data grows; Safe changes to how data is stored; Reliable background work.
- **Fast, safe delivery:** Parts of the product release separately; Internal boundaries checked automatically; A fresh test copy for each change.
- **Change without engineers:** New fields with built-in checks; An interface other software can explore; Automatic rules people can set up; Other systems told when things happen; and 4 more.
- **Learning from use:** Usage data available within minutes.
- **Oversight and limits:** Security checks built into every change; Written rules for what needs approval.
- **Safe AI features:** AI works from the product's own data; The AI sees only what the user may; Maintained test cases for AI features; A full record of AI actions; and 2 more.

## What holds it back

What each loop lacks for its next level, most widely felt first.

- **Build the change.** The product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one. Holds back: From request to release, on the way to Level 3.
- **Check the change.** Some kinds of change, or drafts, can take effect without passing automatic checks. Holds back: From request to release, on the way to Level 3.
- **Check the change.** The running product cannot report its version, its health and its live settings in a form software can read. Holds back: From request to release, on the way to Level 3.
- **Undo it.** Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to. Holds back: From request to release, on the way to Level 3.
- **Take in the request.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from. Holds back: From request to release, on the way to Level 3.
- **Technical foundation.** Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs. Holds back: From request to release, on the way to Level 3.
- **Technical foundation.** Nothing shows that customer organisations cannot see each other's data or slow each other down. Holds back: From request to release, on the way to Level 3.
- **Oversight and limits.** Limits on what the product and its AI may change on their own are missing, partial or written only as instructions. Holds back: From request to release, on the way to Level 3.
- **Oversight and limits.** Changes the product proposes to itself can take effect without being tested against how things work now. Holds back: From request to release, on the way to Level 3.
- **Work out the cause.** The product reports problems but does not work out their likely cause, so people have to investigate each one. Holds back: From problem to fix, on the way to Level 2.
- **Spot unmet needs.** Failed searches and unsupported requests are not gathered into themes that show what users want and cannot get. Holds back: From unmet need to new offering, on the way to Level 2.
- **Propose what to change.** The product does not propose new things to offer by itself, with evidence, for a person to decide. Holds back: From unmet need to new offering, on the way to Level 2.

## Safety gates

Safety gates must all pass before the product may carry changes from start to finish (Level 3). 2 of 6 that apply have passed.

| Safety gate | Status | Why it matters |
|---|---|---|
| Undo for every change people and AI make in the product | Not yet | Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand. |
| Undo for a new version of the code | Does not apply |  |
| Safe changes to how data is stored | Passed |  |
| Backups that are proven to restore | Not yet | Without it, a mistake that undo cannot reach is permanent, because nobody knows whether the backup works. |
| Customer organisations kept apart | Not yet | Without it, one customer organisation could see another's data or slow the product down for everyone. |
| Security checks built into every change | Passed |  |
| Limits and checks on changes the product makes to itself | Not yet | Without it, one bad change the product makes on its own can spread widely before anyone looks. |

## How much AI does

How far the product's own AI carries each loop. Level 1 is people changing the product, so AI counts from Level 2, and never above the loop's own level.

- From request to release: AI does the work up to Level 2, Assisted.
- From problem to fix: AI does none of the steps on its own yet.
- From unmet need to new offering: AI does none of the steps on its own yet.

Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

How safe its AI features are to run for real customers: 2 out of 4. The weakest area sets this.

- What the AI knows and may see: 3 out of 4.
- How AI quality is tested: 2 out of 4.
- How AI actions are controlled: 2 out of 4.
- How the AI runs day to day: 2 out of 4.
- The AI sees only what the user may: passed.
- Worse AI results block a release: not yet.
- A full record of AI actions: passed.

Whatever else improves, it cannot rise above 2 until these pass: Worse AI results block a release.

## Does the loop improve itself

Do the checks, tests and rules that govern change get better from results? A loop whose checks never improve repeats its mistakes faster.

**By hand** (step 1 of 4). People improve the checks, tests and rules by hand after something goes wrong, outside the product.

## Has it been proven

Not yet proven in operation.

- From request to release: not evidenced. The rater looked for operating records and found none that show it.
- From problem to fix: not evidenced. The rater looked for operating records and found none that show it.
- From unmet need to new offering: not evidenced. The rater looked for operating records and found none that show it.

This reading comes from the product's code and documents alone. Nobody observed the product in operation, so the reading cannot say what it has been seen to do.

Built says what the product can do; proven says what it has been seen to do. A product should run at the level it has proven, and take on more as the proof grows.

## How sure this reading is

Of the 66 answers based on evidence, 14 are held with high confidence (the rater read the code and its tests), 51 with medium confidence (the rater read the code, but not every path through it) and 1 with low confidence (inferred from part of the evidence).

For the kinds of change: 2 high, 4 medium and 0 low.

The reading answers 75 questions: 66 from evidence, 0 where no evidence was found (counted as missing), and 9 that do not apply to this product.

The evidence behind the answers: 66 checked in the code, 0 taken from the product's own documents or settings and 0 inferred from other material.

With the higher readings some evidence also supports, From problem to fix would read Level 2, Assisted. The overall level would be Level 2, Assisted.

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

**From request to release, to Level 3, Supervised.** The check to run on the live product: A request goes in. The product writes a clear plan for the change, with how to tell it worked, what it affects and how risky it is, then builds and tests the change and shows the evidence. A person only approves. The change goes to a small group of users first, can be switched off, is measured against how things were before, and can be undone. Then run the safety drill: undo changes everywhere people and AI can make them; restore a backup into a fresh copy, with scheduled jobs held until checked; change how data is stored on a copy of real data without stopping the service; show that customer organisations cannot reach each other's data (where there are several); show security checks stopping a bad change; and show the product's own changes staying inside written limits.

**From problem to fix, to Level 2, Assisted.** The check to run on the live product: Cause a real failure. The product explains why it happened, with evidence, proposes what to change, and drafts the change for a person to finish.

For the overall level to rise, both checks must pass.

- For a plan of milestones that starts from a business goal, run `python3 scripts/blueprint.py <assessment.json> --goal "<business goal>"`.
- For the full list of what the next assessment must find, run `python3 scripts/score.py <assessment.json> --checklist 2`.

## For engineers

Headline as the scorer prints it: **Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L2 (AI L2) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)**

AI Readiness as the scorer prints it: AI Readiness L2 (Deployed with material control gaps) · Context 3 · Quality 2 · Governance 2 · Operations 2 · not production-governed.

Recursion: 1 By hand (LRN-10 at 1). 2 of 2 main kinds are self-serve.

Next-level blockers in the scorer's terms:

- Request → Release to L3: spine Build needs product build path ≥ 3 (has DEL-04 2); spine Verify needs DEL-05 ≥ 3 (has 2); spine Verify needs DEL-06 ≥ 3 (has 2); spine Roll back needs GOV-05 ≥ 3 (has 2); stages Intake needs DEL-01 ≥ 3 (has 2); architecture Foundation needs every applicable ARC ≥ 2 (has ARC-09 1); architecture Foundation needs ARC-09 ≥ 3 (has 1); architecture Foundation needs ARC-05 ≥ 3 (has 2); governance Ceiling needs GOV-10 ≥ 3 and LRN-08 ≥ 2 (has 2; 1)
- Issue → Fix to L2: stages Diagnose needs LRN-05 ≥ 2 (has 1)
- Opportunity → Expansion to L2: stages Sense needs EXP-04 ≥ 2 (has 1); stages Propose needs EXP-05 ≥ 2 (has 0)

| Plain name | Code | Score |
|---|---|---|
| Fast lists and searches as data grows | ARC-01 | 3 |
| Safe changes to how data is stored | ARC-02 | 3 |
| More capacity by adding servers | ARC-03 | 2 |
| Reliable background work | ARC-04 | 3 |
| Customer organisations kept apart | ARC-05 | 2 |
| Known limits, tested regularly | ARC-06 | 2 |
| Service targets, watched with alerts | ARC-07 | 2 |
| One failure does not spread | ARC-08 | 2 |
| Backups that are proven to restore | ARC-09 | 1 |
| Requests become clear change plans | DEL-01 | 2 |
| Parts of the product release separately | DEL-02 | 3 |
| Internal boundaries checked automatically | DEL-03 | 3 |
| AI builds accepted changes | DEL-04 | 2 |
| Automatic checks before any change lands | DEL-05 | 2 |
| The product reports what is running | DEL-06 | 2 |
| A fresh test copy for each change | DEL-07 | 3 |
| User journeys tested automatically | DEL-08 | 2 |
| Release to a small group first | DEL-09 | 2 |
| Off switch for any change | DEL-10 | 2 |
| Undo for a new version of the code | DEL-11 | does not apply |
| New kinds of records without engineering | MAL-01 | does not apply |
| New fields with built-in checks | MAL-02 | 3 |
| Links and statuses set without engineers | MAL-03 | does not apply |
| Other software can use new records | MAL-04 | does not apply |
| Changes reach other software at once | MAL-05 | does not apply |
| An interface other software can explore | MAL-06 | 3 |
| Page layouts changed without engineers | MAL-07 | 2 |
| Screens appear for new records | MAL-08 | does not apply |
| Branding and wording changed without engineers | MAL-09 | 1 |
| Automatic rules people can set up | MAL-10 | 3 |
| Other systems told when things happen | MAL-11 | 3 |
| Custom logic that runs safely | MAL-12 | 2 |
| Add-ons can extend most of the product | MAL-13 | 2 |
| Outside code runs fenced off | MAL-14 | 2 |
| Add-on builders can test before publishing | MAL-15 | 3 |
| New connections by matching fields | MAL-16 | 2 |
| A kit for building connectors | MAL-17 | 3 |
| Stable, versioned interfaces for other software | MAL-18 | 1 |
| Ready-made tools for AI agents | MAL-19 | 3 |
| Use and change the product by chat | MAL-20 | 3 |
| Usage data available within minutes | LRN-01 | 3 |
| Feedback tied to what it concerns | LRN-02 | 1 |
| Notices where users struggle | LRN-03 | 2 |
| Usage, feedback, errors and changes joined | LRN-04 | 2 |
| Works out why a problem happens | LRN-05 | 1 |
| Ranked suggestions for change, with evidence | LRN-06 | 2 |
| Learns from its own use, unprompted | LRN-07 | 2 |
| Self-made changes tested before use | LRN-08 | 1 |
| Every change measured after release | LRN-09 | 2 |
| The checks themselves get better | LRN-10 | 1 |
| Accessibility built in and checked | GOV-01 | 1 |
| One record of every change | GOV-02 | 2 |
| Personal data marked, exportable and erasable | GOV-03 | 2 |
| Security checks built into every change | GOV-04 | 3 |
| History and undo for every setting | GOV-05 | 2 |
| Propose, preview, review, then apply | GOV-06 | 2 |
| Written rules for what needs approval | GOV-07 | 3 |
| Customisations survive product upgrades | GOV-08 | 2 |
| Safe actions for AI and automation | GOV-09 | 2 |
| Firm limits on self-made changes | GOV-10 | 2 |
| Protection against planted instructions | GOV-11 | 2 |
| A general-purpose core | EXP-01 | does not apply |
| New business areas without core changes | EXP-02 | does not apply |
| Ready-made packages for a business area | EXP-03 | does not apply |
| Notices needs it does not serve | EXP-04 | 1 |
| Proposes new things to offer | EXP-05 | 0 |
| Trial launches, kept or removed on results | EXP-06 | 2 |
| AI works from the product's own data | AIR-03 | 3 |
| The AI sees only what the user may | AIR-04 | 3 |
| Maintained test cases for AI features | AIR-05 | 3 |
| Worse AI results block a release | AIR-06 | 2 |
| A full record of AI actions | AIR-07 | 3 |
| Changeable AI models, planned failure handling | AIR-01 | 3 |
| AI spending limits per customer | AIR-02 | 3 |
| AI quality watched in real use | AIR-08 | 2 |
