-- Run once on a new host: sqlite3 /data/notes.db < schema.sql
-- To change the table, edit this file and run the matching ALTER TABLE on the host by hand.
CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  category TEXT NOT NULL,
  body TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
