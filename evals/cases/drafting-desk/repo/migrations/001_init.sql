CREATE TABLE organisations (id SERIAL PRIMARY KEY, name TEXT NOT NULL UNIQUE, widget_key TEXT NOT NULL UNIQUE);
CREATE TABLE users (
  name TEXT PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organisations (id),
  role TEXT NOT NULL CHECK (role IN ('agent', 'lead')),
  token TEXT NOT NULL UNIQUE
);
-- Answers and routing rules per organisation. Every save adds a version; the highest version is live.
CREATE TABLE definition_versions (
  id SERIAL PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organisations (id),
  kind TEXT NOT NULL CHECK (kind IN ('answer', 'rule')),
  key TEXT NOT NULL,
  version INTEGER NOT NULL,
  body JSONB NOT NULL,
  author TEXT NOT NULL,
  note TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (org_id, kind, key, version)
);
CREATE TABLE settings (org_id INTEGER NOT NULL REFERENCES organisations (id), name TEXT NOT NULL,
                       value TEXT NOT NULL, PRIMARY KEY (org_id, name));
CREATE TABLE failed_lookups (
  id SERIAL PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organisations (id),
  question TEXT NOT NULL, normalised TEXT NOT NULL, area TEXT NOT NULL, channel TEXT NOT NULL,
  rules_version INTEGER NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX failed_lookups_org_normalised ON failed_lookups (org_id, normalised, created_at);
