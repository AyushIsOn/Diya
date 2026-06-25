-- Reference schema (the server also creates this automatically on startup via db.js init()).
CREATE TABLE IF NOT EXISTS visitors (
  id         TEXT PRIMARY KEY,        -- short code encoded in the QR (e.g. "7F3KM9AC")
  name       TEXT NOT NULL,
  email      TEXT NOT NULL DEFAULT '',
  age        INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
