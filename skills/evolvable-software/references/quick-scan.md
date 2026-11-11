# EVOLVE quick scan

The quick scan is the ten-minute front door to EVOLVE. A person or an agent answers 22 plain questions from what a product publishes: its README, its admin screens or admin guide, and its automated build configuration. The script turns the answers into an **indicative range** for each of the three loops, such as "likely L1 to L2", shows which safety gates look open, and says what a full assessment would check next.

> **A quick scan is indicative. It is not an EVOLVE assessment and must never be published as a level.** It reads what a product says about itself; a full assessment scores 75 criteria from the code, its tests and its records, with evidence for each. Use the quick scan to decide whether a full assessment is worth doing and where it should look first.

## How to answer

- Answer each question `yes`, `no` or `unsure`. **Yes is always the good answer.**
- Answer `yes` only when you can point at something: a page of the docs, a screen, a line of the build configuration. Write where in `notes`.
- Answer `unsure` when you cannot tell in the time. Unsure answers widen the range; they never count against the product at the high end or for it at the low end.
- Answer `no` when the product's own material shows the answer is no, or when the thing is clearly absent.
- Two safety gates apply only in some products. Answer `n/a` when the condition in their row holds. No other question accepts `n/a`.
- A question about "the changes they most often need" means the handful of recurring ways the product gets changed: an answer, a rule, a workflow, a price list, a report, a form.

## How the answers are read

- **Range.** For each loop, the low end counts every `unsure` as no and the high end counts every `unsure` as yes.
- **Levels build on each other.** A loop reaches a level only when every question for that level and for every lower level is yes. Level 1 needs either the people running the product to make their common changes, or the product to draft changes itself, as in the full framework.
- **Safety gates cap at Level 2.** If any applicable safety gate is anything but `yes` (including `unsure`), every loop is held at Level 2, because the framework never lets a loop above Level 2 until every critical control passes. The output says so when the cap bites.
- **Never Level 5.** Level 5 needs records of the product changing itself over a period of real operation. The quick scan stops at Level 4 and says so.
- **What would move it.** The script names the three answers that would change the range most, and for each loop the check a full assessment would run first.

The questions are a simplified view of the level conditions in `rubric.md`. Expansion's Level 3 and 4 launch steps (to a selected group, then keep or withdraw on results) are covered by the shared questions on carrying a change through, measuring it and shipping pre-approved kinds, not asked separately.

## How to run

```bash
python3 skills/evolvable-software/scripts/quick_scan.py --template > answers.json   # empty answers file
python3 skills/evolvable-software/scripts/quick_scan.py answers.json                # markdown reading
python3 skills/evolvable-software/scripts/quick_scan.py answers.json --json         # the same as data
```

The answers file:

```json
{"product": "Example",
 "answers": {"self-serve": "yes", "self-undo": "unsure", "gate-customer-isolation": "n/a", "...": "..."},
 "notes": {"self-serve": "Admin guide, 'Rules' page"}}
```

Every question must be answered. Unknown ids, missing ids, bad values and `n/a` on a question that always applies are errors (exit code 2). The `questions` key that `--template` prints is there to help whoever fills it in, and is ignored.

## The questions

The tables are generated from the json block below with `quick_scan.py --table`; a test keeps them in step.

<!-- quick-scan-table:start -->
### Kinds of change

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 1 | `self-serve` | Can the people who run the product make the changes they most often need (for example an answer, a rule, a workflow, a price list, a report or a form) themselves, in the running product, without an engineer or a new release? | Admin screens or the admin guide: which settings, editors and builders exist. | Kinds of change. Level 1 of Request → Release and Issue → Fix (a product that drafts changes itself also meets it). |
| 2 | `self-undo` | Can they undo each of those changes themselves, in the product? | Version history, restore or revert buttons, the admin guide. | Kinds of change. Level 1 of all three loops. |

### Request → Release

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 3 | `request-capture` | When a user asks for a change, does the product capture the request in a structured way (what is wanted, for whom, where in the product), rather than as free text in an email, chat or ticket? | Request or feedback forms inside the product; the README's feature list. | Request → Release, Level 2. |
| 4 | `drafts-change` | Does the product draft changes itself (for example it writes the new rule, workflow or text) for a person to check, finish and release? | Assistant or AI features in the README and the admin guide. | Request → Release and Opportunity → Expansion, Level 2 (also meets Level 1 of every loop). |
| 5 | `checks-before-live` | Do automatic checks (tests and validations) run on every change before it goes live, including changes made in the admin screens, and stop a change that fails? | The automated build configuration (for example .github/workflows); validation in the admin screens. | All three loops, Level 2. |
| 6 | `carries-end-to-end` | Can the product carry a change all the way through itself (build it, test it, release it to a few users first, switch it off if needed), with a person only approving the release? | Release and approval docs; preview, gradual release or on/off switch features. | All three loops, Level 3. |
| 7 | `ships-pre-approved` | Do low-risk kinds of change that people have pre-approved in written rules go live with no person involved, and get reversed automatically when they make things worse? | Automation or policy settings; docs on applying changes automatically and undoing them automatically. | All three loops, Level 4. |

### Issue → Fix

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 8 | `notices-problems` | Does the product record the problems users hit (failed actions, errors, complaints, negative feedback) where a person can look them up by part of the product? | Error, feedback or health screens inside the product; monitoring docs. | Issue → Fix, Level 1. |
| 9 | `explains-why` | When something goes wrong, does the product explain why it happened, with evidence a person can check? | Diagnosis, explain-this-error or root-cause features. | Issue → Fix, Level 2. |
| 10 | `proposes-fixes` | Does the product propose a fix for a problem, with the evidence behind it, and draft that fix for a person to finish? | Suggested-fix or self-improvement features in the README and the admin guide. | Issue → Fix, Level 2 (also meets its Level 1). |

### Opportunity → Expansion

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 11 | `adds-new-kinds` | Can the people running the product add support for a whole new kind of need (a new app, area or bundle of features) without an engineer, and remove it again? | App, template or extension catalogue; the admin guide. | Opportunity → Expansion, Level 1. |
| 12 | `notices-unmet-needs` | Does the product show the needs it does not serve yet (for example searches that found nothing, requests it could not handle, features people keep asking for)? | Insight or analytics screens; feedback and request tooling. | Opportunity → Expansion, Level 2. |
| 13 | `proposes-capabilities` | Does the product propose new capabilities to meet those needs, with the evidence behind each proposal? | Insight, suggestion or roadmap features inside the product. | Opportunity → Expansion, Level 2. |

### Measurement

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 14 | `measured-against-baseline` | Is each change measured against how things were before it (a baseline), so people can see whether it helped or hurt? | Experiment or impact reports; before-and-after numbers in release records. | Measurement. All three loops, Level 3. |

### Recursion

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 15 | `checks-improve` | When a check misses a problem or a rule turns out to be wrong, are the checks and rules themselves improved from those results, through the same approved way of making changes? | How tests, evaluation cases and policies change; whether failures become new tests. | Recursion. All three loops, Level 4. |

### Safety gates

| # | Id | Question | Where to look | Maps to |
|---:|---|---|---|---|
| 16 | `gate-undo-every-change` | Can every kind of change made in the product be undone, not only some (including settings, connections, stored passwords and keys, AI memory and permissions), and is that tested? | Version history across every admin area; tests of undo. | Safety gate: undo for every change. Every applicable gate must be yes for any loop to read above Level 2. |
| 17 | `gate-restore-release` | If a new release of the software goes wrong, can the previous release be put back quickly, in a documented and tested way? | Upgrade and release docs; the release steps in the build configuration. | Safety gate: previous release can be restored. |
| 18 | `gate-data-changes` | When a release changes how stored data is organised, are those changes tested before they go live and can they be reversed? | Upgrade notes; data change files and their tests. | Safety gate: data changes are tested and reversible. |
| 19 | `gate-backup-restored` | Has a backup actually been restored, in an automated test or a recorded drill, and checked to be complete (data, files and settings)? | Backup and restore docs; restore tests; drill records. | Safety gate: a backup has been restored in a test or drill. |
| 20 | `gate-customer-isolation` | Is one customer organisation unable to see or change another's data, and is that tested? | Docs on organisations or workspaces; access tests. | Safety gate: one customer cannot see another's data. Answer n/a when: each installation serves only one customer organisation. |
| 21 | `gate-security-checks` | Do automatic security checks (for example scans for known weaknesses and for leaked passwords or keys) stop a change from going live when they find a serious problem? | The automated build configuration; the security policy. | Safety gate: security checks block a bad change. |
| 22 | `gate-ai-limits` | Are there written limits on what AI or automation may change in the product by itself, enforced by the product and recorded each time they are used? | AI and automation settings; docs on permissions for agents. | Safety gate: limits on what AI may change by itself. Answer n/a when: neither AI nor any automation in the product can change its behaviour, settings, memory or data by itself. |
<!-- quick-scan-table:end -->

## Model

The script reads this block. Each loop lists, per level, the questions that must all be yes; `{"any": [...]}` is met when any one of them is yes. Questions with a `gate` are the safety gates.

```json quick-scan
{
  "version": "0.7.0",
  "max_level": 4,
  "gate_cap": 2,
  "level_names": ["Manual", "Configurable", "Assisted", "Supervised", "Policy-bounded", "Self-directing"],
  "questions": [
    {
      "id": "self-serve",
      "section": "Kinds of change",
      "question": "Can the people who run the product make the changes they most often need (for example an answer, a rule, a workflow, a price list, a report or a form) themselves, in the running product, without an engineer or a new release?",
      "where": "Admin screens or the admin guide: which settings, editors and builders exist.",
      "maps_to": "Kinds of change. Level 1 of Request → Release and Issue → Fix (a product that drafts changes itself also meets it)."
    },
    {
      "id": "self-undo",
      "section": "Kinds of change",
      "question": "Can they undo each of those changes themselves, in the product?",
      "where": "Version history, restore or revert buttons, the admin guide.",
      "maps_to": "Kinds of change. Level 1 of all three loops."
    },
    {
      "id": "request-capture",
      "section": "Request → Release",
      "question": "When a user asks for a change, does the product capture the request in a structured way (what is wanted, for whom, where in the product), rather than as free text in an email, chat or ticket?",
      "where": "Request or feedback forms inside the product; the README's feature list.",
      "maps_to": "Request → Release, Level 2."
    },
    {
      "id": "drafts-change",
      "section": "Request → Release",
      "question": "Does the product draft changes itself (for example it writes the new rule, workflow or text) for a person to check, finish and release?",
      "where": "Assistant or AI features in the README and the admin guide.",
      "maps_to": "Request → Release and Opportunity → Expansion, Level 2 (also meets Level 1 of every loop)."
    },
    {
      "id": "checks-before-live",
      "section": "Request → Release",
      "question": "Do automatic checks (tests and validations) run on every change before it goes live, including changes made in the admin screens, and stop a change that fails?",
      "where": "The automated build configuration (for example .github/workflows); validation in the admin screens.",
      "maps_to": "All three loops, Level 2."
    },
    {
      "id": "carries-end-to-end",
      "section": "Request → Release",
      "question": "Can the product carry a change all the way through itself (build it, test it, release it to a few users first, switch it off if needed), with a person only approving the release?",
      "where": "Release and approval docs; preview, gradual release or on/off switch features.",
      "maps_to": "All three loops, Level 3."
    },
    {
      "id": "ships-pre-approved",
      "section": "Request → Release",
      "question": "Do low-risk kinds of change that people have pre-approved in written rules go live with no person involved, and get reversed automatically when they make things worse?",
      "where": "Automation or policy settings; docs on applying changes automatically and undoing them automatically.",
      "maps_to": "All three loops, Level 4."
    },
    {
      "id": "notices-problems",
      "section": "Issue → Fix",
      "question": "Does the product record the problems users hit (failed actions, errors, complaints, negative feedback) where a person can look them up by part of the product?",
      "where": "Error, feedback or health screens inside the product; monitoring docs.",
      "maps_to": "Issue → Fix, Level 1."
    },
    {
      "id": "explains-why",
      "section": "Issue → Fix",
      "question": "When something goes wrong, does the product explain why it happened, with evidence a person can check?",
      "where": "Diagnosis, explain-this-error or root-cause features.",
      "maps_to": "Issue → Fix, Level 2."
    },
    {
      "id": "proposes-fixes",
      "section": "Issue → Fix",
      "question": "Does the product propose a fix for a problem, with the evidence behind it, and draft that fix for a person to finish?",
      "where": "Suggested-fix or self-improvement features in the README and the admin guide.",
      "maps_to": "Issue → Fix, Level 2 (also meets its Level 1)."
    },
    {
      "id": "adds-new-kinds",
      "section": "Opportunity → Expansion",
      "question": "Can the people running the product add support for a whole new kind of need (a new app, area or bundle of features) without an engineer, and remove it again?",
      "where": "App, template or extension catalogue; the admin guide.",
      "maps_to": "Opportunity → Expansion, Level 1."
    },
    {
      "id": "notices-unmet-needs",
      "section": "Opportunity → Expansion",
      "question": "Does the product show the needs it does not serve yet (for example searches that found nothing, requests it could not handle, features people keep asking for)?",
      "where": "Insight or analytics screens; feedback and request tooling.",
      "maps_to": "Opportunity → Expansion, Level 2."
    },
    {
      "id": "proposes-capabilities",
      "section": "Opportunity → Expansion",
      "question": "Does the product propose new capabilities to meet those needs, with the evidence behind each proposal?",
      "where": "Insight, suggestion or roadmap features inside the product.",
      "maps_to": "Opportunity → Expansion, Level 2."
    },
    {
      "id": "measured-against-baseline",
      "section": "Measurement",
      "question": "Is each change measured against how things were before it (a baseline), so people can see whether it helped or hurt?",
      "where": "Experiment or impact reports; before-and-after numbers in release records.",
      "maps_to": "Measurement. All three loops, Level 3."
    },
    {
      "id": "checks-improve",
      "section": "Recursion",
      "question": "When a check misses a problem or a rule turns out to be wrong, are the checks and rules themselves improved from those results, through the same approved way of making changes?",
      "where": "How tests, evaluation cases and policies change; whether failures become new tests.",
      "maps_to": "Recursion. All three loops, Level 4."
    },
    {
      "id": "gate-undo-every-change",
      "section": "Safety gates",
      "gate": "Undo for every change",
      "question": "Can every kind of change made in the product be undone, not only some (including settings, connections, stored passwords and keys, AI memory and permissions), and is that tested?",
      "where": "Version history across every admin area; tests of undo.",
      "maps_to": "Safety gate: undo for every change. Every applicable gate must be yes for any loop to read above Level 2."
    },
    {
      "id": "gate-restore-release",
      "section": "Safety gates",
      "gate": "Previous release can be restored",
      "question": "If a new release of the software goes wrong, can the previous release be put back quickly, in a documented and tested way?",
      "where": "Upgrade and release docs; the release steps in the build configuration.",
      "maps_to": "Safety gate: previous release can be restored."
    },
    {
      "id": "gate-data-changes",
      "section": "Safety gates",
      "gate": "Data changes tested and reversible",
      "question": "When a release changes how stored data is organised, are those changes tested before they go live and can they be reversed?",
      "where": "Upgrade notes; data change files and their tests.",
      "maps_to": "Safety gate: data changes are tested and reversible."
    },
    {
      "id": "gate-backup-restored",
      "section": "Safety gates",
      "gate": "Backup restored in a test or drill",
      "question": "Has a backup actually been restored, in an automated test or a recorded drill, and checked to be complete (data, files and settings)?",
      "where": "Backup and restore docs; restore tests; drill records.",
      "maps_to": "Safety gate: a backup has been restored in a test or drill."
    },
    {
      "id": "gate-customer-isolation",
      "section": "Safety gates",
      "gate": "Customers kept apart",
      "question": "Is one customer organisation unable to see or change another's data, and is that tested?",
      "where": "Docs on organisations or workspaces; access tests.",
      "maps_to": "Safety gate: one customer cannot see another's data.",
      "allows_na": "each installation serves only one customer organisation."
    },
    {
      "id": "gate-security-checks",
      "section": "Safety gates",
      "gate": "Security checks block a bad change",
      "question": "Do automatic security checks (for example scans for known weaknesses and for leaked passwords or keys) stop a change from going live when they find a serious problem?",
      "where": "The automated build configuration; the security policy.",
      "maps_to": "Safety gate: security checks block a bad change."
    },
    {
      "id": "gate-ai-limits",
      "section": "Safety gates",
      "gate": "Limits on what AI may change by itself",
      "question": "Are there written limits on what AI or automation may change in the product by itself, enforced by the product and recorded each time they are used?",
      "where": "AI and automation settings; docs on permissions for agents.",
      "maps_to": "Safety gate: limits on what AI may change by itself.",
      "allows_na": "neither AI nor any automation in the product can change its behaviour, settings, memory or data by itself."
    }
  ],
  "consistency": [
    {
      "when": "ships-pre-approved",
      "is": "yes",
      "id": "gate-ai-limits",
      "not": "n/a",
      "why": "Changes that go live with no person involved are changes the product makes by itself, so its limits apply."
    }
  ],
  "loops": [
    {
      "id": "request",
      "name": "Request → Release",
      "levels": {
        "1": [{"any": ["self-serve", "drafts-change"]}, "self-undo"],
        "2": ["request-capture", "drafts-change", "checks-before-live"],
        "3": ["carries-end-to-end", "measured-against-baseline"],
        "4": ["ships-pre-approved", "checks-improve"]
      }
    },
    {
      "id": "fix",
      "name": "Issue → Fix",
      "levels": {
        "1": [{"any": ["self-serve", "drafts-change", "proposes-fixes"]}, "self-undo", "notices-problems"],
        "2": ["checks-before-live", "explains-why", "proposes-fixes"],
        "3": ["carries-end-to-end", "measured-against-baseline"],
        "4": ["ships-pre-approved", "checks-improve"]
      }
    },
    {
      "id": "expansion",
      "name": "Opportunity → Expansion",
      "levels": {
        "1": [{"any": ["adds-new-kinds", "drafts-change"]}, "self-undo"],
        "2": ["checks-before-live", "drafts-change", "notices-unmet-needs", "proposes-capabilities"],
        "3": ["carries-end-to-end", "measured-against-baseline"],
        "4": ["ships-pre-approved", "checks-improve"]
      }
    }
  ],
  "challenges": {
    "request": {
      "1": "Take a change people often ask for (an answer, a rule, a workflow step, a setting). Someone running the product makes it in the running product, with no engineer and no new release, then undoes it.",
      "2": "A user describes a change in plain words inside the product. The product captures it with structure (what, who, where) and drafts the change for a person to finish. Every change, drafted or not, passes automatic checks before it goes live.",
      "3": "A request goes in. The product writes down what done means, builds the change with tests and shows the evidence; a person approves. The change goes to a few users first, can be switched off, is compared with how things were before, and can be undone. Then the safety drill: undo changes of every kind, restore a backup into a fresh copy, change stored data on a copy of real data, show customers cannot reach each other's data, show security checks stopping a bad change, and show the product's own changes staying inside their limits.",
      "4": "A low-risk change goes from request to live with no person involved, under a written rule for that kind of change. It goes to a few users first, is measured, and is undone automatically when its measure gets worse; every automatic decision is recorded, and the checks and rules improve from the results."
    },
    "fix": {
      "1": "Make the product fail the way a user would see it. The product records the problem where a person can look it up, with the part of the product affected. Someone running the product then changes the behaviour without an engineer, and can undo it.",
      "2": "Cause a real failure. The product explains why it happened, proposes what to change with evidence, and drafts the fix for a person to finish. The fix passes automatic checks before it goes live.",
      "3": "Break something on purpose. Without being asked, the product raises it as a problem with the users affected and how often, explains it, proposes a fix with evidence, and ships it after a person approves: to a few users first, measured, and reversible. The safety drill must also pass.",
      "4": "A low-risk fix ships with no person involved, under a written rule, and is undone automatically if the problem does not improve or something else gets worse."
    },
    "expansion": {
      "1": "Someone running the product adds support for a new kind of need (a new app, area or bundle) without an engineer, and removes it again.",
      "2": "The product shows needs it does not serve yet, such as searches that found nothing or requests it could not handle, and proposes a new capability with evidence.",
      "3": "From real use, the product spots an unmet need, proposes a capability with evidence, and launches it to a selected group of users after a person approves. The safety drill must also pass.",
      "4": "A new capability launches to a selected group and is kept or withdrawn on its measured results, under a written rule, with the decision recorded."
    }
  },
  "level5_check": "Level 5 is beyond a quick scan. A full assessment would look for records showing the product choosing, shipping and measuring its own changes over a period of real operation, with its rules adapting to how often its own checks wrongly passed a change.",
  "always_checks": [
    "List every kind of change the people running the product commonly need, including the ones they cannot make themselves, with evidence for how far each has come.",
    "Read the code and its tests, not only the documentation: a full assessment scores 75 criteria, each with cited evidence and a confidence.",
    "Look for records showing real changes going through each loop (proven), not only that the product can do it (built)."
  ]
}
```
