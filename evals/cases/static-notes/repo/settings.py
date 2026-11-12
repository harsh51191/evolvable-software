"""Settings read from the environment when the container starts."""
import os

DATABASE_PATH = os.environ.get("NOTES_DB", "/data/notes.db")
PAGE_SIZE = int(os.environ.get("NOTES_PAGE_SIZE", "50"))
