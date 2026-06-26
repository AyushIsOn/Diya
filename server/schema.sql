-- Reference schema (the server also creates this automatically on startup via db.js init()).

CREATE TABLE IF NOT EXISTS visitors (
  id         TEXT PRIMARY KEY,        -- short code (e.g. "7F3KM9AC")
  name       TEXT NOT NULL,
  email      TEXT NOT NULL DEFAULT '',
  age        INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Model B: kiosk-initiated sessions. The kiosk shows a QR of <site>/?session=<token>;
-- the phone registers against it; the kiosk polls until the session is "claimed".
CREATE TABLE IF NOT EXISTS sessions (
  token      TEXT PRIMARY KEY,        -- URL-safe random token shown in the kiosk QR
  status     TEXT NOT NULL DEFAULT 'pending',  -- 'pending' | 'claimed'
  visitor_id TEXT,                     -- set when claimed
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  claimed_at TIMESTAMPTZ
);
