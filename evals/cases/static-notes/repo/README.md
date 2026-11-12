# Static Notes

A small notes board for the support team. People post short notes ("printer on floor 3 is down", "new refund policy from 1 May") and read them by category.

It runs as one container on one host behind the office VPN. There are no accounts: anyone on the VPN can post, read and delete notes.

## Run locally

    pip install -r requirements.txt
    sqlite3 notes.db < schema.sql
    NOTES_DB=notes.db flask --app app run

## Features

- Notes by category, newest first.
- Search across all notes.
- Admins can rename categories from the settings page.
- We track searches that find nothing, so we know which notes to write next.

## How things change

Everything about how Static Notes behaves is in the code:

- the categories and the help text on each page: `content.py`;
- the page size and the database path: `settings.py` (environment variables);
- the database table: `schema.sql`.

To change any of these, open a pull request. When it is merged, tag a release (`git tag v1.4.0 && git push --tags`). The release workflow builds and pushes the image, and the on-call engineer runs `./deploy.sh v1.4.0` on the host.

To change the table, edit `schema.sql` and run the matching `ALTER TABLE` by hand on the host before deploying.

Ask for changes in the #notes-team chat channel. `docs/change-requests.md` counts what people asked for last quarter.

## Backups

See `make backup`.
