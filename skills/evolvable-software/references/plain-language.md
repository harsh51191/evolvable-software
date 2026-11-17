# Plain language for EVOLVE reports

This file gives every code used in an EVOLVE assessment a plain name and a plain question, so that a business or product reader can follow a report without knowing the codes. The report generator uses only this text in the body of a report, and refuses to run when an entry is missing. Writing rules: short, concrete, active sentences in British spelling; codes appear only as the `###` keys; no engineering jargon; and the same idea always gets the same words (undo, the people running the product, customer organisation, written rules).

## Levels
### L0
Name: Manual
Product: The changes that matter most are made by engineers writing and releasing code.
People: Most changes are requests that wait for engineers and for the next release.
### L1
Name: Configurable
Product: The people running the product can make the changes they need most without engineers, and can undo them.
People: Someone running the product makes the change in the product itself, and can undo it.
### L2
Name: Assisted
Product: The product takes in requests, explains problems and drafts the change, and a person completes it and releases it.
People: You describe what you need in the product, it drafts the change and explains what went wrong, and someone running the product finishes and releases it.
### L3
Name: Supervised
Product: The product carries a change from start to finish, including checks, release to a small group of users first and undo, and every safety gate passes.
People: The product builds, checks and releases changes and notices problems by itself, and a person only approves.
### L4
Name: Policy-bounded
Product: Low-risk changes are released without a person, within written rules, to a small group of users first, then measured and undone automatically when they make things worse.
People: Routine changes and fixes arrive on their own, within written rules the company set, and undo themselves when they make things worse.
### L5
Name: Self-directing
Product: The product decides what to change, releases and measures it within written rules, and uses the results to improve its own checks and rules.
People: The product decides what to improve next, does it and gets better at deciding, while people set the goals and the limits.

## Loops
### request
Name: From request to release
Question: Can the product take a user's request, build it properly and release it?
### fix
Name: From problem to fix
Question: Can the product find the problems users face, fix them and release the fix?
### expansion
Name: From unmet need to new offering
Question: Can the product notice needs it does not serve yet, and propose or launch something for them?

## Parts
### stages
Name: The loop's own steps
Meaning: The steps only this loop has, such as taking in a request, working out why a problem happens or spotting an unmet need.
### spine
Name: The shared release steps
Meaning: The steps every change goes through whatever started it, which are build, check, try on a small group of users first, release, measure and undo.
### architecture
Name: Technical foundation
Meaning: Whether the product can carry more load, survive failures and recover its data while it keeps changing.
### governance
Name: Oversight and limits
Meaning: Whether every change is reviewed, recorded, kept within set limits and able to be undone.

## Stages
### Build
Name: Build the change
### Verify
Name: Check the change
### Stage
Name: Try it on a small group of users first
### Release
Name: Release it, with an off switch
### Observe
Name: Measure the effect
### Roll back
Name: Undo it
### Intake
Name: Take in the request
### Detect
Name: Notice the problem
### Diagnose
Name: Work out the cause
### Propose
Name: Propose what to change
### Sense
Name: Spot unmet needs
### Launch
Name: Launch to a trial group
### Foundation
Name: Technical foundation
### Ceiling
Name: Oversight and limits

## Controls
### Definition rollback
Name: Undo for every change people and AI make in the product
Why: Without it, a bad change to settings, rules or layouts stays in place until an engineer repairs it by hand.
### Release rollback
Name: Undo for a new version of the code
Why: Without it, a bad release stays live until engineers can build and release a repair.
### Safe migrations
Name: Safe changes to how data is stored
Why: Without it, a small change can lock the product or lose data.
### Tested backup and restore
Name: Backups that are proven to restore
Why: Without it, a mistake that undo cannot reach is permanent, because nobody knows whether the backup works.
### Tenant isolation
Name: Customer organisations kept apart
Why: Without it, one customer organisation could see another's data or slow the product down for everyone.
### Security as infrastructure
Name: Security checks built into every change
Why: Without it, changes that arrive faster than people can review them will carry security holes into the product.
### Bounded self-change
Name: Limits and checks on changes the product makes to itself
Why: Without it, one bad change the product makes on its own can spread widely before anyone looks.

## Capabilities
### ARC
Name: Technical foundation
Asks: Can the product carry more load, survive failures and recover its data?
### DEL
Name: Fast, safe delivery
Asks: Can a change be built, checked and released quickly and safely?
### MAL
Name: Change without engineers
Asks: Can the product be reshaped without engineers releasing new code?
### LRN
Name: Learning from use
Asks: Does the product notice what is wrong, work out why, and measure whether its changes helped?
### GOV
Name: Oversight and limits
Asks: Is every change reviewed, recorded, kept within limits and able to be undone, including the changes the product makes to itself?
### EXP
Name: Growing into new areas
Asks: Does the product find and launch new things worth offering?
### AIR
Name: Safe AI features
Asks: Are the product's AI features safe to run for real customers?

## Scope facts
### persistent_data
Name: It stores data that must not be lost
### schema_changes
Name: Changes to it can alter how data is stored
### multi_tenant
Name: One installation serves several customer organisations that must be kept apart
### hosted_service
Name: It runs all the time as an online service
### machine_actions
Name: AI agents or other software can change its data or settings
### agent_mutations
Name: Its own AI can change its settings, skills, memory or data
### evolution_auto_apply
Name: Changes it makes to itself take effect without a person's approval
### definition_change_path
Name: Its behaviour is changed through settings and rules
### code_release_path
Name: Its own improvement system releases new code, not only new settings and rules
### ai_features
Name: It has AI features
### ai_data_access
Name: Its AI can read the product's data
### ai_actions
Name: Its AI can change data or settings, send messages outside the product or spend money

## Reach
### 0
Name: Engineers only
Meaning: This kind of change needs engineers to change code, make a release or edit files by hand, or the people running the product can make it but cannot undo it.
### 1
Name: Self-serve
Meaning: The people running the product make this kind of change themselves, without a release, and can undo it.
### 2
Name: Drafted
Meaning: The product drafts this kind of change, and a person completes and releases it.
### 3
Name: Carried
Meaning: The product builds, checks and releases this kind of change from start to finish, and a person approves.
### 4
Name: Pre-approved
Meaning: This kind of change is released without a person under written rules, and is undone automatically when it makes things worse.
### 5
Name: Self-chosen
Meaning: The product also decides when to make this kind of change, within written rules.

## Recursion
### 0
Name: Fixed
Meaning: The checks, tests and rules that govern change improve only when engineers rewrite them in code.
### 1
Name: By hand
Meaning: People improve the checks, tests and rules by hand after something goes wrong, outside the product.
### 2
Name: Governed
Meaning: The checks, tests and rules have versions and change through the same reviewed path as any other change, but results do not yet drive those changes.
### 3
Name: Results-driven
Meaning: The product records which check missed each failure and proposes better checks, tests and rules, which a person approves.
### 4
Name: Self-improving
Meaning: The product improves its own checks, tests and rules within written rules, measures whether that helped and undoes what did not.

## AI readiness
### Context
Name: What the AI knows and may see
Asks: Does the AI work from the product's own up-to-date data, and only from data the person it works for may see?
### Quality
Name: How AI quality is tested
Asks: Are AI features tested on maintained sets of test cases, and is a change stopped when the scores get worse?
### Governance
Name: How AI actions are controlled
Asks: Can AI actions be traced, kept within limits and protected from planted instructions?
### Operations
Name: How the AI runs day to day
Asks: Does the AI keep working when a provider fails, stay within cost limits and get watched for falling quality?
### Permission-preserving access
Name: The AI sees only what the user may
Asks: Is the AI held to the permissions of the person it works for?
### Regression evaluation before release
Name: Worse AI results block a release
Asks: Is a change to an AI feature stopped from release when its test scores fall?
### Traceability of consequential AI actions
Name: A full record of AI actions
Asks: Can the people running the product see what the AI did, why and for whom?

## Criteria
### ARC-01
Name: Fast lists and searches as data grows
Question: Do lists and searches stay fast as data grows, including on fields people added themselves?
Gap: Lists and searches, including on fields people added themselves, are not set up to stay fast as data grows.
### ARC-02
Name: Safe changes to how data is stored
Question: Are changes to how data is stored tested on realistic data and made without downtime or data loss?
Gap: Changes to how data is stored are not tested on realistic data, or can cause downtime or data loss.
### ARC-03
Name: More capacity by adding servers
Question: Can the product serve more users simply by adding servers, and is that tested or shown in its standard setup?
Gap: Adding servers does not reliably add capacity, because parts of the product keep their data on a single machine.
### ARC-04
Name: Reliable background work
Question: Is long-running work done in the background, retried safely when it fails, never run twice and visible when stuck?
Gap: Background work can fail silently, run twice or be lost, and nobody can see when it is stuck.
### ARC-05
Name: Customer organisations kept apart
Question: Is each customer organisation's data shown to be separate, with limits so that one cannot slow down the others?
Gap: Nothing shows that customer organisations cannot see each other's data or slow each other down.
### ARC-06
Name: Known limits, tested regularly
Question: Are the product's limits for load and size written down and tested automatically as it changes?
Gap: Nobody knows how much load each part of the product can take until something breaks.
### ARC-07
Name: Service targets, watched with alerts
Question: Does the product publish service targets for speed or availability, and raise an alert when it misses them?
Gap: There are no published service targets with alerts, so nobody can say whether a change left the product healthy.
### ARC-08
Name: One failure does not spread
Question: When a connected system, add-on or AI provider fails, does only the affected feature stop, with a tested fallback?
Gap: A failing connected system, add-on or AI provider can take down more than the feature that uses it.
### ARC-09
Name: Backups that are proven to restore
Question: Can data, settings, files, secrets and scheduled jobs all be backed up and restored, with the restore tested automatically?
Gap: Restoring from a backup is not tested for everything the product needs, which is data, settings, files, secrets and scheduled jobs.
### DEL-01
Name: Requests become clear change plans
Question: Does the product turn a request into a plan a person confirms, with how to tell it is done, what it affects and its risk?
Gap: Requests stay as loose text, and the product does not turn them into a plan a person can confirm and build from.
### DEL-02
Name: Parts of the product release separately
Question: Can each main part of the product, such as its screens and its services, be released without rebuilding the others?
Gap: The main parts of the product must be built or released together, so every change waits for the slowest part.
### DEL-03
Name: Internal boundaries checked automatically
Question: Do automated checks stop one part of the code from reaching into another in ways its design forbids?
Gap: The boundaries between parts of the code are kept by habit and not by automated checks, so they wear away.
### DEL-04
Name: AI builds accepted changes
Question: Does the product's own AI build an accepted change from start to finish and present it for review with proof that it works?
Gap: The product's own AI does not build accepted changes from start to finish, so a person still builds or completes each one.
### DEL-05
Name: Automatic checks before any change lands
Question: Does every kind of change, drafts included, pass automatic checks before it can take effect?
Gap: Some kinds of change, or drafts, can take effect without passing automatic checks.
### DEL-06
Name: The product reports what is running
Question: Can software ask the running product which version it is, whether it is healthy and which settings are live?
Gap: The running product cannot report its version, its health and its live settings in a form software can read.
### DEL-07
Name: A fresh test copy for each change
Question: Can each change be tried in its own fresh copy of the product, with sample data, that is removed afterwards?
Gap: Changes are tried in shared, long-lived test copies of the product and not in a fresh copy made for each change.
### DEL-08
Name: User journeys tested automatically
Question: Do automated tests walk the main user journeys for each role and device, and is the use of each new feature counted?
Gap: Whether a change works for users is judged by a person looking at screens and not by automated tests of user journeys.
### DEL-09
Name: Release to a small group first
Question: Can any kind of change go to a small group of users or one customer organisation before everyone gets it?
Gap: Some or all kinds of change reach every user at once, with no way to try them on a small group of users first.
### DEL-10
Name: Off switch for any change
Question: Can any change the product releases be switched off at once, without a new release, with a record of each use?
Gap: Switching off a change that causes harm needs an engineer or a new release.
### DEL-11
Name: Undo for a new version of the code
Question: Can a new version of the product's code be undone in one tested step, with the data still working afterwards?
Gap: Going back to the previous version of the code is not a tested, one-step action that keeps the data working.
### MAL-01
Name: New kinds of records without engineering
Question: Can the people running the product add a new kind of record, with its own fields and permissions, without engineers or a release?
Gap: Adding a new kind of record needs engineers and a release.
### MAL-02
Name: New fields with built-in checks
Question: Can the people running the product add a field with a type and checks that forms and other software then follow?
Gap: Adding a field with its type and checks needs engineers, or the checks are repeated in each place the field appears.
### MAL-03
Name: Links and statuses set without engineers
Question: Can the people running the product set how records link together, or which statuses they move through, without engineers?
Gap: The links between records and the statuses they move through are fixed in code.
### MAL-04
Name: Other software can use new records
Question: When a new kind of record is added, can other software read and write it without an engineer writing code for it?
Gap: Engineers must write code for each kind of record before other software can read or write it.
### MAL-05
Name: Changes reach other software at once
Question: When a kind of record or a field changes, does other software see the change straight away, without a release?
Gap: Other software sees a changed record or field only after engineers build and release a new version.
### MAL-06
Name: An interface other software can explore
Question: Can other software discover everything the product lets it do, and get clear, structured errors when a request is wrong?
Gap: Other software, AI included, cannot fully discover what the product lets it do or why a request was refused.
### MAL-07
Name: Page layouts changed without engineers
Question: Can the people running the product rearrange pages for each customer organisation, with checks and a preview before publishing?
Gap: Page layouts are fixed in code or changed only by engineers, with no preview before publishing.
### MAL-08
Name: Screens appear for new records
Question: Does a new kind of record get list, detail and entry screens automatically, which the people running the product can adjust?
Gap: Each new kind of record needs engineers to build its list, detail and entry screens.
### MAL-09
Name: Branding and wording changed without engineers
Question: Can the people running the product change colours, wording and languages for each customer organisation without a release?
Gap: Colours, wording and translations are fixed in code or managed by engineers.
### MAL-10
Name: Automatic rules people can set up
Question: Can the people running the product set up rules of the form 'when this happens, do that' and test them first?
Gap: Automatic behaviour, such as notices and status changes, is written in code and not set up as rules people can change and test.
### MAL-11
Name: Other systems told when things happen
Question: Can the people running the product have other systems told when something happens, with retries and a delivery record?
Gap: Other systems cannot be told reliably when something happens, because there are no retries or no record of delivery.
### MAL-12
Name: Custom logic that runs safely
Question: Can partners add their own logic at set points, run within strict limits on time, code libraries and outside connections?
Gap: Custom logic cannot be added without changing the core product, or it runs without limits on what it can do.
### MAL-13
Name: Add-ons can extend most of the product
Question: Can add-ons extend screens, layouts, forms, branding, wording and server behaviour, through settings as well as code?
Gap: Add-ons can extend only a few parts of the product, or only by writing code.
### MAL-14
Name: Outside code runs fenced off
Question: Does code from third parties or written by AI run fenced off from the product, with limits on resources and outside connections?
Gap: Code from third parties or written by AI runs with full trust inside the product.
### MAL-15
Name: Add-on builders can test before publishing
Question: Can add-on builders preview their work in a real customer organisation, see its error records and check it before publishing?
Gap: People building add-ons cannot preview and check their work in a real customer organisation before publishing.
### MAL-16
Name: New connections by matching fields
Question: Is connecting a second outside system a matter of matching its fields to the product's, with no new core code?
Gap: Each outside system is connected with its own custom code, so every new connection costs as much as the first.
### MAL-17
Name: A kit for building connectors
Question: Can partners build connectors to outside systems with a supported kit, which the people running the product install and set up?
Gap: Every connector to an outside system has to be built into the core product by its engineers.
### MAL-18
Name: Stable, versioned interfaces for other software
Question: Do interfaces for other software have versions, notice before removals and safe handling of repeated or conflicting updates?
Gap: Interfaces for other software can change without versions or notice, which breaks partners' connections.
### MAL-19
Name: Ready-made tools for AI agents
Question: Does the product give AI agents clearly described tools, limited to what each agent may do, and a list of what it can do?
Gap: AI agents have no clearly described, permission-limited tools for working with the product.
### MAL-20
Name: Use and change the product by chat
Question: Can users finish tasks in a chat based on the product's own data, and can the people running it change it in plain words?
Gap: Users cannot finish tasks by chat, or the people running the product cannot change it by describing what they want in plain words.
### LRN-01
Name: Usage data available within minutes
Question: Can the product's own features see usage and error data within minutes, and not only analysts the next day?
Gap: Usage and error data reaches analysts in daily batches and does not reach the product's own features within minutes.
### LRN-02
Name: Feedback tied to what it concerns
Question: Is feedback, such as ratings and corrections, recorded against the exact item and version it concerns, and reviewed?
Gap: Feedback is free text, or is not tied to the exact item and version it concerns, so it cannot drive a change.
### LRN-03
Name: Notices where users struggle
Question: Does the product notice by itself where users struggle and raise it as a problem, with who is affected and how often?
Gap: The product does not yet notice and raise, by itself, the places where users struggle.
### LRN-04
Name: Usage, feedback, errors and changes joined
Question: Does the product bring its usage, feedback, errors and history of changes together so they can be searched as one?
Gap: Usage, feedback, errors and the history of changes sit in separate places, so a problem cannot be connected to its cause.
### LRN-05
Name: Works out why a problem happens
Question: For a problem it finds, does the product show how to repeat it and the likely cause, pointing to the setting or change behind it?
Gap: The product reports problems but does not work out their likely cause, so people have to investigate each one.
### LRN-06
Name: Ranked suggestions for change, with evidence
Question: Does the product suggest changes to itself across the whole product, ranked, each with evidence and the gain it expects?
Gap: The product shows data but does not turn it into ranked suggestions for change with evidence and expected gain.
### LRN-07
Name: Learns from its own use, unprompted
Question: Does the product keep reviewing how it is used and draft improvements to itself without being asked?
Gap: The product drafts improvements from its own use only when someone asks, or not at all.
### LRN-08
Name: Self-made changes tested before use
Question: Before a change the product proposes to itself takes effect, is it tested against how things work now and passed, revised or blocked?
Gap: Changes the product proposes to itself can take effect without being tested against how things work now.
### LRN-09
Name: Every change measured after release
Question: After a change is released, does the product compare results with a starting point and record whether to keep, revise or undo it?
Gap: Released changes are not measured against a starting point, so nobody knows whether to keep, revise or undo them.
### LRN-10
Name: The checks themselves get better
Question: When a check lets a bad change through, does the product record it and propose a better check or rule for a person to approve?
Gap: When a check lets a bad change through, nothing feeds that back into better checks, tests or rules.
### GOV-01
Name: Accessibility built in and checked
Question: Is every change checked automatically for accessibility, using shared building blocks that are accessible by design?
Gap: Accessibility is checked by hand or feature by feature, and not automatically on every change.
### GOV-02
Name: One record of every change
Question: Can the people running the product look up who changed what and who approved it, for all data and settings, kept for a set time?
Gap: There is no single, complete record of who changed what and who approved it that the people running the product can search.
### GOV-03
Name: Personal data marked, exportable and erasable
Question: Is personal data marked field by field, so one person's data can be exported or erased across the whole product on request?
Gap: Personal data is not marked field by field, so exporting or erasing one person's data needs engineers or misses parts of the product.
### GOV-04
Name: Security checks built into every change
Question: Does a security scan block every unsafe change, and does every new kind of record get permission rules automatically?
Gap: Security scans do not block unsafe changes, or permissions have to be added by hand for each new kind of record.
### GOV-05
Name: History and undo for every setting
Question: Can the people running the product see the history of every setting, rule and layout, compare versions and undo any change?
Gap: Undo does not cover everything people can change, so some settings, rules or layouts have no history to go back to.
### GOV-06
Name: Propose, preview, review, then apply
Question: Can the people running the product propose a change, preview it on a safe copy and have it reviewed before it takes effect?
Gap: Changes take effect directly, without a proposal that can be previewed and reviewed first.
### GOV-07
Name: Written rules for what needs approval
Question: Is there a written rule for each kind of change saying whether it needs a person's approval, with every approval recorded?
Gap: No written rules say which kinds of change may go ahead without a person, or approvals are not recorded.
### GOV-08
Name: Customisations survive product upgrades
Question: When the product is upgraded, do automatic checks and tools keep each customer organisation's customisations working?
Gap: A product upgrade can break what customer organisations have customised, and repairing it is manual work.
### GOV-09
Name: Safe actions for AI and automation
Question: Does each AI agent or automated tool act under its own limited identity, with previews, safe repeats, rate limits and records?
Gap: AI agents and automated tools act with broad or shared access, without previews, rate limits or a record tied to each one.
### GOV-10
Name: Firm limits on self-made changes
Question: Are there enforced limits on what the product and its AI may change on their own, with anything outside them blocked and recorded?
Gap: Limits on what the product and its AI may change on their own are missing, partial or written only as instructions.
### GOV-11
Name: Protection against planted instructions
Question: Is outside content treated as information and never as instructions, with each self-made change traceable to its sources?
Gap: A user or a document could plant instructions that change the product, and changes cannot be traced back to what caused them.
### EXP-01
Name: A general-purpose core
Question: Is the product's core built from general parts, such as people, content and permissions, with the specific business on top?
Gap: The product's core is built around one line of business, so serving a neighbouring need means rewriting it.
### EXP-02
Name: New business areas without core changes
Question: Has at least one new business area been added using only settings, rules and connectors, with no change to the core?
Gap: Serving a new business area needs changes to the product's core, and none has yet been added through settings and rules alone.
### EXP-03
Name: Ready-made packages for a business area
Question: Can a business area be installed as one versioned package of settings, layouts, rules and connectors?
Gap: A new business area has to be set up piece by piece and cannot be installed as one versioned package.
### EXP-04
Name: Notices needs it does not serve
Question: Does the product group what users try and fail to do into themes, with how many ask, the trend and who is affected?
Gap: Failed searches and unsupported requests are not gathered into themes that show what users want and cannot get.
### EXP-05
Name: Proposes new things to offer
Question: Does the product propose new things to offer, unprompted and ranked, each with evidence, size, fit and a measure of success?
Gap: The product does not propose new things to offer by itself, with evidence, for a person to decide.
### EXP-06
Name: Trial launches, kept or removed on results
Question: Does a new offering go to a small group first, with a measure of success, a review date and a recorded decision to keep it?
Gap: New offerings launch to everyone or to nobody, with no trial group, measure of success or recorded decision to keep or remove them.
### AIR-01
Name: Changeable AI models, planned failure handling
Question: Can the people running the product choose the AI model for each feature, and is there a tested plan for when a model fails?
Gap: The AI model is fixed by engineers, or there is no tested plan for when the model or its provider fails.
### AIR-02
Name: AI spending limits per customer
Question: Does the product enforce an AI usage or spending limit for each customer organisation or user, which its administrators can see?
Gap: AI use is not limited for each customer organisation or user, so one heavy user can run up the cost for everyone.
### AIR-03
Name: AI works from the product's own data
Question: Does the AI get the product's own up-to-date data and settings through one managed route, and say which sources it used?
Gap: The AI sees little of the product's own data, or engineers connect it by hand for each feature and it goes out of date.
### AIR-04
Name: The AI sees only what the user may
Question: Is the AI held to the permissions of the person it works for, with tests showing it cannot reveal what they may not see?
Gap: The AI can reach data with wider access than the person it works for, so it could reveal what they may not see.
### AIR-05
Name: Maintained test cases for AI features
Question: Does each AI feature have a maintained set of test cases with scores, run the same way each time and kept for each version?
Gap: AI features have no maintained sets of test cases, so nobody knows whether a change made the answers better or worse.
### AIR-06
Name: Worse AI results block a release
Question: Is a change to an AI feature stopped from release when its test scores fall below a set threshold?
Gap: A change that makes the AI's answers worse can still be released, because nothing blocks a release on the test scores.
### AIR-07
Name: A full record of AI actions
Question: For each AI action that changes data, sends messages or spends money, is there a searchable record of what, why and for whom?
Gap: What the AI did, why and for whom cannot be fully reconstructed by the people running the product.
### AIR-08
Name: AI quality watched in real use
Question: Is the quality of each AI feature measured continuously in real use, with an alert when it gets worse?
Gap: Nobody would be alerted if the AI's answers slowly got worse in real use.
