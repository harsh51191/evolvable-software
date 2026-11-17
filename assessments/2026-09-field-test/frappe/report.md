# Frappe Framework: how ready it is to evolve itself

A plain-language reading of an EVOLVE 0.7.0 assessment. Date 2026-09-30.

## In one paragraph

Built to Level 1, Configurable: the people running the product can make the changes they need most without engineers, and can undo them. Not yet proven in operation. In practice, someone running the product makes the change in the product itself, and can undo it. The biggest thing holding it back is that the product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one.

## Where it stands

The product is read on three loops. Its overall level is the lower of the first two; the third is reported beside it.

**From request to release.** Can the product take a user's request, build it properly and release it?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the loop's own steps and the shared release steps.
- Proven: not evidenced.

**From problem to fix.** Can the product find the problems users face, fix them and release the fix?

- Built to Level 1, Configurable. The people running the product can make the changes they need most without engineers, and can undo them.
- Held at this level by the shared release steps.
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
| Record types, fields and form layouts | system managers | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Approval workflows, notifications and automation rules | system managers and process owners | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Who can see and change what (roles and permissions) | system managers | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Reports and printed documents | system managers and report users | Self-serve. The people running the product make this kind of change themselves, without a release, and can undo it. | Yes |
| Custom server-side logic, integrations and new apps | system managers, with engineers | Engineers only. This kind of change needs engineers to change code, make a release or edit files by hand. | No |

4 of 4 main kinds are self-serve. Self-serve means: the people running the product make this kind of change themselves, without a release, and can undo it.

## What works today

The strongest parts of the product, rated 3 or more out of 4.

- **Technical foundation:** Fast lists and searches as data grows.
- **Change without engineers:** New kinds of records without engineering; New fields with built-in checks; Links and statuses set without engineers; Other software can use new records; and 7 more.
- **Growing into new areas:** A general-purpose core; New business areas without core changes; Ready-made packages for a business area.

## What holds it back

What each loop lacks for its next level, most widely felt first.

- **Build the change.** The product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one. Holds back: From request to release, on the way to Level 2; From problem to fix, on the way to Level 2.
- **Take in the request.** Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from. Holds back: From request to release, on the way to Level 2.
- **Spot unmet needs.** Failed searches and unsupported requests are not gathered into themes that show what users want and cannot get. Holds back: From unmet need to new offering, on the way to Level 2.
- **Propose what to change.** The product does not propose new things to offer by itself, with evidence, for a person to decide. Holds back: From unmet need to new offering, on the way to Level 2.

## Safety gates

Safety gates must all pass before the product may carry changes from start to finish (Level 3). 0 of 5 that apply have passed.

| Safety gate | Status | Why it matters |
|---|---|---|
| Undo for every change people and AI make in the product | Not yet | Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand. |
| Undo for a new version of the code | Does not apply |  |
| Safe changes to how data is stored | Not yet | Without it, a small change can lock the product or lose data. |
| Backups that are proven to restore | Not yet | Without it, a mistake that undo cannot reach is permanent, because nobody knows whether the backup works. |
| Customer organisations kept apart | Not yet | Without it, one customer organisation could see another's data or slow the product down for everyone. |
| Security checks built into every change | Not yet | Without it, changes that arrive faster than people can review them will carry security holes into the product. |
| Limits and checks on changes the product makes to itself | Does not apply |  |

## How much AI does

How far the product's own AI carries each loop. Level 1 is people changing the product, so AI counts from Level 2, and never above the loop's own level.

- From request to release: AI does none of the steps on its own yet.
- From problem to fix: AI does none of the steps on its own yet.
- From unmet need to new offering: AI does none of the steps on its own yet.

Engineers build this product with AI coding agents or a delivery framework. That is AI-assisted engineering, not the product evolving itself. It is not installed, enforced and limited as part of the product, so it earns no credit.

The product has no AI features, so the checks on AI features do not apply.

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

Of the 64 answers based on evidence, 6 are held with high confidence (the rater read the code and its tests), 49 with medium confidence (the rater read the code, but not every path through it) and 9 with low confidence (inferred from part of the evidence).

For the kinds of change: 0 high, 4 medium and 1 low.

Check these first. The rater was least sure of them, and each one decides a level or a safety gate:

- Requests become clear change plans: holds From request to release, on the way to Level 2.
- Proposes new things to offer: holds From unmet need to new offering, on the way to Level 2.

The reading answers 75 questions: 64 from evidence, 0 where no evidence was found (counted as missing), and 11 that do not apply to this product.

The evidence behind the answers: 63 checked in the code, 1 taken from the product's own documents or settings and 0 inferred from other material.

Neither the higher readings some evidence also supports, nor settings that ship switched off, would change any level.

The overall level would drop if any of these were rated one step lower: Notices where users struggle; History and undo for every setting.

The reading treats the product as follows:

- It stores data that must not be lost.
- Changes to it can alter how data is stored.
- One installation serves several customer organisations that must be kept apart.
- It runs all the time as an online service.
- AI agents or other software can change its data or settings.
- Its behaviour is changed through settings and rules.

This is one rater's reading of the evidence. A second, independent reading may differ.

## What to do next

**From request to release, to Level 2, Assisted.** The check to run on the live product: A user describes a change in plain words inside the product. The product records it with structure (what, for whom, where) and drafts the change for a person to finish. Every change, drafted or not, passes automatic checks before it goes live, and a change that fails them is stopped.

**From problem to fix, to Level 2, Assisted.** The check to run on the live product: Cause a real failure. The product explains why it happened, with evidence, proposes what to change, and drafts the change for a person to finish.

For the overall level to rise, both checks must pass.

- For a plan of milestones that starts from a business goal, run `python3 scripts/blueprint.py <assessment.json> --goal "<business goal>"`.
- For the full list of what the next assessment must find, run `python3 scripts/score.py <assessment.json> --checklist 2`.

## For engineers

Headline as the scorer prints it: **Built to SAL 1 (Configurable) · Proven: not evidenced · AI-driven 0 · Request → Release L1 (AI L0) · Issue → Fix L1 (AI L0) · Opportunity → Expansion L1 (AI L0)**

AI Readiness as the scorer prints it: no AI features.

Recursion: 1 By hand (LRN-10 at 1). 4 of 4 main kinds are self-serve.

Next-level blockers in the scorer's terms:

- Request → Release to L2: spine Build needs product build path ≥ 2 (has DEL-04 0); stages Intake needs DEL-01 ≥ 2 (has 0)
- Issue → Fix to L2: spine Build needs product build path ≥ 2 (has DEL-04 0, LRN-07 2 with LRN-08 1)
- Opportunity → Expansion to L2: stages Sense needs EXP-04 ≥ 2 (has 0); stages Propose needs EXP-05 ≥ 2 (has 0)

| Plain name | Code | Score |
|---|---|---|
| Fast lists and searches as data grows | ARC-01 | 3 |
| Safe changes to how data is stored | ARC-02 | 1 |
| More capacity by adding servers | ARC-03 | 2 |
| Reliable background work | ARC-04 | 2 |
| Customer organisations kept apart | ARC-05 | 2 |
| Known limits, tested regularly | ARC-06 | 2 |
| Service targets, watched with alerts | ARC-07 | 1 |
| One failure does not spread | ARC-08 | 2 |
| Backups that are proven to restore | ARC-09 | 2 |
| Requests become clear change plans | DEL-01 | 0 |
| Parts of the product release separately | DEL-02 | 1 |
| Internal boundaries checked automatically | DEL-03 | 1 |
| AI builds accepted changes | DEL-04 | 0 |
| Automatic checks before any change lands | DEL-05 | 2 |
| The product reports what is running | DEL-06 | 2 |
| A fresh test copy for each change | DEL-07 | 2 |
| User journeys tested automatically | DEL-08 | 2 |
| Release to a small group first | DEL-09 | 2 |
| Off switch for any change | DEL-10 | 1 |
| Undo for a new version of the code | DEL-11 | does not apply |
| New kinds of records without engineering | MAL-01 | 3 |
| New fields with built-in checks | MAL-02 | 3 |
| Links and statuses set without engineers | MAL-03 | 3 |
| Other software can use new records | MAL-04 | 3 |
| Changes reach other software at once | MAL-05 | 3 |
| An interface other software can explore | MAL-06 | 2 |
| Page layouts changed without engineers | MAL-07 | 3 |
| Screens appear for new records | MAL-08 | 3 |
| Branding and wording changed without engineers | MAL-09 | 2 |
| Automatic rules people can set up | MAL-10 | 3 |
| Other systems told when things happen | MAL-11 | 3 |
| Custom logic that runs safely | MAL-12 | 3 |
| Add-ons can extend most of the product | MAL-13 | 3 |
| Outside code runs fenced off | MAL-14 | 1 |
| Add-on builders can test before publishing | MAL-15 | 2 |
| New connections by matching fields | MAL-16 | 1 |
| A kit for building connectors | MAL-17 | 2 |
| Stable, versioned interfaces for other software | MAL-18 | 2 |
| Ready-made tools for AI agents | MAL-19 | 2 |
| Use and change the product by chat | MAL-20 | 0 |
| Usage data available within minutes | LRN-01 | 2 |
| Feedback tied to what it concerns | LRN-02 | 1 |
| Notices where users struggle | LRN-03 | 2 |
| Usage, feedback, errors and changes joined | LRN-04 | 1 |
| Works out why a problem happens | LRN-05 | 2 |
| Ranked suggestions for change, with evidence | LRN-06 | 2 |
| Learns from its own use, unprompted | LRN-07 | 2 |
| Self-made changes tested before use | LRN-08 | 1 |
| Every change measured after release | LRN-09 | 0 |
| The checks themselves get better | LRN-10 | 1 |
| Accessibility built in and checked | GOV-01 | 1 |
| One record of every change | GOV-02 | 2 |
| Personal data marked, exportable and erasable | GOV-03 | 2 |
| Security checks built into every change | GOV-04 | 2 |
| History and undo for every setting | GOV-05 | 2 |
| Propose, preview, review, then apply | GOV-06 | 2 |
| Written rules for what needs approval | GOV-07 | 1 |
| Customisations survive product upgrades | GOV-08 | 2 |
| Safe actions for AI and automation | GOV-09 | 2 |
| Firm limits on self-made changes | GOV-10 | does not apply |
| Protection against planted instructions | GOV-11 | does not apply |
| A general-purpose core | EXP-01 | 3 |
| New business areas without core changes | EXP-02 | 3 |
| Ready-made packages for a business area | EXP-03 | 3 |
| Notices needs it does not serve | EXP-04 | 0 |
| Proposes new things to offer | EXP-05 | 0 |
| Trial launches, kept or removed on results | EXP-06 | 2 |
| AI works from the product's own data | AIR-03 | does not apply |
| The AI sees only what the user may | AIR-04 | does not apply |
| Maintained test cases for AI features | AIR-05 | does not apply |
| Worse AI results block a release | AIR-06 | does not apply |
| A full record of AI actions | AIR-07 | does not apply |
| Changeable AI models, planned failure handling | AIR-01 | does not apply |
| AI spending limits per customer | AIR-02 | does not apply |
| AI quality watched in real use | AIR-08 | does not apply |
