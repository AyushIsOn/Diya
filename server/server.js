// Diya Meditation — visitor registration API (Model B: phone-scans-kiosk).
//
// Flow:
//   1. Kiosk:  POST /api/sessions            -> { token }
//      Kiosk shows a QR of  <site>/?session=<token>
//   2. Phone:  opens that URL, fills the form, submits:
//              POST /api/visitors { name, email, age, session } -> { id, linked }
//      (linked=true means the session was matched and claimed)
//   3. Kiosk:  polls GET /api/sessions/:token
//              -> { status:"pending" }                     (waiting)
//              -> { status:"claimed", visitor:{...} }       (done -> kiosk advances)
//
// Legacy/fallback still supported:
//   GET /api/visitors/:id   -> look up a standalone pass by id
//
// Also serves the static registration website from ../registration.

const path = require('path');
const crypto = require('crypto');
const express = require('express');
const cors = require('cors');
const { pool, init } = require('./db');

const app = express();
app.use(cors());
app.use(express.json());

app.use(express.static(path.join(__dirname, '..', 'registration')));

// Short, human-friendly visitor id. Excludes ambiguous chars (0/O/1/I/L).
const ID_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
function makeId(len = 8) {
  const bytes = crypto.randomBytes(len);
  let out = '';
  for (let i = 0; i < len; i++) out += ID_ALPHABET[bytes[i] % ID_ALPHABET.length];
  return out;
}

// URL-safe random session token (hard to guess).
function makeToken() {
  return crypto.randomBytes(9).toString('base64url'); // ~12 chars
}

app.get('/api/health', (_req, res) => res.json({ ok: true }));

// ---- Sessions (Model B) -------------------------------------------------

// Kiosk starts a session and shows its token as a QR.
app.post('/api/sessions', async (_req, res) => {
  try {
    for (let attempt = 0; attempt < 5; attempt++) {
      const token = makeToken();
      try {
        await pool.query('INSERT INTO sessions (token) VALUES ($1)', [token]);
        return res.status(201).json({ token });
      } catch (err) {
        if (err.code === '23505') continue; // collision -> retry
        throw err;
      }
    }
    return res.status(500).json({ error: 'could not allocate a session' });
  } catch (err) {
    console.error('POST /api/sessions failed:', err);
    return res.status(500).json({ error: 'internal error' });
  }
});

// Kiosk polls this until the visitor registers on their phone.
app.get('/api/sessions/:token', async (req, res) => {
  try {
    const token = String(req.params.token || '');
    const { rows } = await pool.query(
      `SELECT s.status, v.id, v.name, v.email, v.age
         FROM sessions s
         LEFT JOIN visitors v ON v.id = s.visitor_id
        WHERE s.token = $1`,
      [token]
    );
    if (rows.length === 0) return res.status(404).json({ status: 'not_found' });

    const r = rows[0];
    if (r.status === 'claimed' && r.id) {
      return res.json({
        status: 'claimed',
        visitor: { id: r.id, name: r.name, email: r.email, age: r.age },
      });
    }
    return res.json({ status: 'pending', visitor: null });
  } catch (err) {
    console.error('GET /api/sessions/:token failed:', err);
    return res.status(500).json({ error: 'internal error' });
  }
});

// ---- Visitors -----------------------------------------------------------

// Register a visitor. If a session token is supplied (phone opened the kiosk's
// QR link), claim that session and link it to the new visitor.
app.post('/api/visitors', async (req, res) => {
  try {
    const name = String(req.body?.name ?? '').trim();
    const email = String(req.body?.email ?? '').trim();
    let age = Number.parseInt(req.body?.age, 10);
    if (!Number.isFinite(age) || age < 0) age = 0;
    const session = req.body?.session ? String(req.body.session) : null;

    if (!name) return res.status(400).json({ error: 'name is required' });

    let id = null;
    for (let attempt = 0; attempt < 5; attempt++) {
      const candidate = makeId(8);
      try {
        await pool.query(
          'INSERT INTO visitors (id, name, email, age) VALUES ($1, $2, $3, $4)',
          [candidate, name, email, age]
        );
        id = candidate;
        break;
      } catch (err) {
        if (err.code === '23505') continue; // unique_violation -> new id
        throw err;
      }
    }
    if (!id) return res.status(500).json({ error: 'could not allocate a unique id' });

    let linked = false;
    if (session) {
      const upd = await pool.query(
        `UPDATE sessions
            SET visitor_id = $1, status = 'claimed', claimed_at = now()
          WHERE token = $2 AND status = 'pending'`,
        [id, session]
      );
      linked = upd.rowCount > 0;
    }

    return res.status(201).json({ id, linked });
  } catch (err) {
    console.error('POST /api/visitors failed:', err);
    return res.status(500).json({ error: 'internal error' });
  }
});

// Legacy: look up a standalone pass by id.
app.get('/api/visitors/:id', async (req, res) => {
  try {
    const id = String(req.params.id || '').trim().toUpperCase();
    const { rows } = await pool.query(
      'SELECT id, name, email, age FROM visitors WHERE id = $1',
      [id]
    );
    if (rows.length === 0) return res.status(404).json({ error: 'not found' });
    return res.json(rows[0]);
  } catch (err) {
    console.error('GET /api/visitors/:id failed:', err);
    return res.status(500).json({ error: 'internal error' });
  }
});

const PORT = process.env.PORT || 3000;
init()
  .then(() => app.listen(PORT, () => console.log(`Diya registration server listening on :${PORT}`)))
  .catch((err) => {
    console.error('DB init failed:', err);
    process.exit(1);
  });
