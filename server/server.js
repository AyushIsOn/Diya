// Diya Meditation — visitor registration API.
//
// Endpoints:
//   GET  /api/health           -> { ok: true }
//   POST /api/visitors         -> body { name, email, age } -> 201 { id }
//   GET  /api/visitors/:id     -> { id, name, email, age } | 404
//
// Also serves the static registration website from ../registration so the
// whole thing runs as a single Render web service.

const path = require('path');
const crypto = require('crypto');
const express = require('express');
const cors = require('cors');
const { pool, init } = require('./db');

const app = express();
app.use(cors());
app.use(express.json());

// Serve the registration website (../registration/index.html) at "/"
app.use(express.static(path.join(__dirname, '..', 'registration')));

// Short, human-friendly id. Excludes ambiguous chars (0/O/1/I/L).
const ID_ALPHABET = 'ABCDEFGHJKMNPQRSTUVWXYZ23456789';
function makeId(len = 8) {
  const bytes = crypto.randomBytes(len);
  let out = '';
  for (let i = 0; i < len; i++) out += ID_ALPHABET[bytes[i] % ID_ALPHABET.length];
  return out;
}

app.get('/api/health', (_req, res) => res.json({ ok: true }));

// Register a visitor and return the generated id (this id is what the QR encodes).
app.post('/api/visitors', async (req, res) => {
  try {
    const name = String(req.body?.name ?? '').trim();
    const email = String(req.body?.email ?? '').trim();
    let age = Number.parseInt(req.body?.age, 10);
    if (!Number.isFinite(age) || age < 0) age = 0;

    if (!name) return res.status(400).json({ error: 'name is required' });

    // Retry a few times in the rare event of an id collision.
    for (let attempt = 0; attempt < 5; attempt++) {
      const id = makeId(8);
      try {
        await pool.query(
          'INSERT INTO visitors (id, name, email, age) VALUES ($1, $2, $3, $4)',
          [id, name, email, age]
        );
        return res.status(201).json({ id });
      } catch (err) {
        if (err.code === '23505') continue; // unique_violation -> new id
        throw err;
      }
    }
    return res.status(500).json({ error: 'could not allocate a unique id' });
  } catch (err) {
    console.error('POST /api/visitors failed:', err);
    return res.status(500).json({ error: 'internal error' });
  }
});

// Look up a visitor by id (what the kiosk calls after scanning the QR).
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
