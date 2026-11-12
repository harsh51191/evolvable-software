CREATE TABLE failed_lookups (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  question TEXT NOT NULL,
  normalised TEXT NOT NULL,
  area TEXT NOT NULL,
  channel TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX failed_lookups_area ON failed_lookups (area, created_at);
