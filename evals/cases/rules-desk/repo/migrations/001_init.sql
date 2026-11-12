CREATE TABLE users (
  name TEXT PRIMARY KEY,
  role TEXT NOT NULL CHECK (role IN ('agent', 'lead')),
  token TEXT NOT NULL UNIQUE
);

-- Answers and routing rules. Every save adds a version; the highest version is live.
CREATE TABLE definition_versions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kind TEXT NOT NULL CHECK (kind IN ('answer', 'rule')),
  key TEXT NOT NULL,
  version INTEGER NOT NULL,
  body TEXT NOT NULL,
  author TEXT NOT NULL,
  note TEXT NOT NULL DEFAULT '',
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (kind, key, version)
);

-- Greeting and opening hours: one current value each.
CREATE TABLE settings (name TEXT PRIMARY KEY, value TEXT NOT NULL);
