// Postgres connection + schema bootstrap.
//
// DATABASE_URL is required. It works with any hosted Postgres:
//   - Render Postgres   (note: the FREE plan database is deleted after 30 days)
//   - Neon              (free tier, persistent)  <-- recommended
//   - Supabase          (free tier, persistent)
//
// Hosted Postgres requires SSL. For a LOCAL postgres without SSL, set PGSSL=disable.

const { Pool } = require('pg');

const connectionString = process.env.DATABASE_URL;
if (!connectionString) {
  console.error('FATAL: DATABASE_URL is not set. See server/.env.example');
  process.exit(1);
}

const ssl =
  process.env.PGSSL === 'disable' ? false : { rejectUnauthorized: false };

const pool = new Pool({ connectionString, ssl });

async function init() {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS visitors (
      id         TEXT PRIMARY KEY,
      name       TEXT NOT NULL,
      email      TEXT NOT NULL DEFAULT '',
      age        INTEGER NOT NULL DEFAULT 0,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);
}

module.exports = { pool, init };
