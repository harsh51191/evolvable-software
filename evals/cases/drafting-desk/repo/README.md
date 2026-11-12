# Drafting Desk

Drafting Desk answers customer questions in the help widget and sends everything it cannot answer to the right support queue. One deployment serves several customer organisations. Each organisation has its own leads, agents, answers, routing rules, settings and widget key, and cannot see another organisation's data.

## Who changes what

| Change | Who | How |
|---|---|---|
| New or edited answer | the organisation's leads | Admin page (`/admin`), live as soon as it passes the checks |
| Routing rule | the organisation's leads, or an AI draft a lead finishes | Admin page; AI drafts wait for a lead to publish them |
| Greeting and opening hours | the organisation's leads | Admin page, settings |
| New queue | engineers | `config/queues.yaml` and a release |

Before an answer or rule goes live, `desk/checks.py` checks it, including AI drafts. Every saved answer and rule is a numbered version with its author, with history and undo on the admin page.

## Asking for a change

Agents and leads ask for changes inside the product: `POST /requests` with the area, what they want, example questions and the rules involved. Leads see open requests at `/admin/requests`.

## Questions we could not answer

Each failed lookup is stored with the area, the channel and the rules version that was live. `/admin/failure-groups` groups them by question, with counts, sample questions, areas, and when each group was first and last seen.

## AI drafts

From a failure group or a request, a lead can ask for a draft routing rule. A worker (`python -m desk.drafter`) asks the model, keeps the draft only inside its limits (routing rules only, priority 50 or lower), runs the same checks as a hand-made change, and stores it awaiting review with its source, model and prompt version. A lead edits it if needed and publishes it; nothing the AI drafts goes live on its own.

The AI is limited to 20 drafts per organisation per day, and every blocked draft is written to the audit log. Prompt changes are checked in CI (the `prompt-check` job).

## Smart matching

Answers and queues are found by smart matching (`desk/matching.py`).

## Running

    pip install -r requirements.txt
    export DATABASE_URL=postgresql://desk@localhost/desk LLM_API_URL=https://llm.internal/v1/complete
    python deskctl.py migrate
    python deskctl.py add-org acme && python deskctl.py add-user alice acme lead
    gunicorn desk.app:app & python -m desk.drafter

`docs/operations.md` covers scaling, limits, monitoring and backups. `docs/change-requests.md` counts last quarter's change requests.

## Backups

`python deskctl.py backup /backups` writes a `pg_dump` file. Backups are tested in CI (`tests/test_backup.py`).
