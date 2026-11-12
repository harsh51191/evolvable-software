CREATE TABLE change_requests (
  id SERIAL PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organisations (id),
  requester TEXT NOT NULL, area TEXT NOT NULL, what TEXT NOT NULL,
  examples JSONB NOT NULL DEFAULT '[]', rule_keys JSONB NOT NULL DEFAULT '[]',
  status TEXT NOT NULL DEFAULT 'open', created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
-- Rule changes drafted by the AI lane. None is live until a lead publishes it.
CREATE TABLE drafts (
  id SERIAL PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organisations (id),
  key TEXT NOT NULL, body JSONB NOT NULL, check_errors JSONB NOT NULL,
  source_type TEXT NOT NULL CHECK (source_type IN ('failure_group', 'request')), source_ref TEXT NOT NULL,
  model TEXT NOT NULL, prompt_version TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'awaiting_review' CHECK (status IN ('awaiting_review', 'published', 'discarded')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE TABLE jobs (
  id SERIAL PRIMARY KEY,
  org_id INTEGER NOT NULL REFERENCES organisations (id),
  payload JSONB NOT NULL, attempts INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'queued', last_error TEXT
);
