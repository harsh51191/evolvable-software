# Rules Desk

Rules Desk answers customer questions in the help widget and sends everything it cannot answer to the right support queue. One company runs one Rules Desk; its support leads look after it.

## Who changes what

| Change | Who | How |
|---|---|---|
| New or edited answer | support leads | Admin page (`/admin`), live as soon as it passes the checks |
| Routing rule | support leads | Admin page, live as soon as it passes the checks; try a question against it first |
| Greeting and opening hours | support leads | Admin page, settings |
| New queue | engineers | `config/queues.yaml` and a release |
| Widget look and text | engineers | front-end code and a release |

Every admin change can be undone.

Before an answer or rule goes live, `desk/checks.py` checks it: keywords present and not a copy of another answer, a pattern that compiles, a queue that exists, a priority from 1 to 100. A change that fails is refused with the reasons. Every saved answer and rule is kept as a numbered version with its author; the history and the Undo button are on the admin page.

## Smart matching

Rules Desk uses smart matching to find the best answer for each question and the right queue for the rest (`desk/matching.py`).

## Questions we could not answer

Each question with no matching answer is stored with the page of the site it came from (`area`) and the channel. Leads review `/admin/failed-lookups?area=billing` each week and write the missing answers.

## Running

    pip install -r requirements.txt
    python deskctl.py migrate
    python deskctl.py add-user alice lead
    flask --app desk.app run

The service keeps its SQLite database at `DESK_DB` (default `/data/desk.db`). `docs/change-requests.md` counts what people asked to change last quarter.

## Backups

`python deskctl.py backup /backups` copies the database to a dated file. Backups are tested in CI (`tests/test_backup.py`).
