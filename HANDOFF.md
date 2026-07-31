# Diya — Handoff & Current State

A living "where things stand + what's next" doc so anyone (a new developer, a new
chat session, or the Kiro CLI) can pick up quickly. For depth see `PROJECT.md`
(overview), `SETUP.md` (commands), `FAQ.md` (Q&A), and
`docs/Diya-Codebase-Overview.pdf` (file-by-file).

> Snapshot, not the source of truth — trust the code and `SETUP.md` over anything
> here that looks stale.

---

## 0. IMPORTANT — this PR rolls the code back to the PR #24 baseline
A lot of the changes merged **after PR #24 were unnecessary / did not work
reliably**, so this branch returns the codebase to the **#24 state**. The following
post-#24 work is **removed** here and should be considered scrapped:
- `#25` window hand-off + test kit — introduced a self-minimise that **broke on Wayland** (the app appeared to close on login and couldn't restore itself).
- `#26` SETUP no-camera docs.
- `#28` remove-minimise + white report screen.

If any individual piece is wanted again (e.g. the **white report screen** or a
**no-camera test kit**), **re-do it cleanly on top of this baseline** — do not
restore the old branches.

## 1. What it is
An unattended meditation kiosk. Two parts we own:
- **Kiosk app** — `DiyaMeditation/` — C#/.NET 8 + Avalonia, shipped as a `.deb`. Version **1.6.0**.
- **Backend + web** — `server/` (Node/Express/Postgres) + `registration/` (static pages), hosted on **Render** at `https://diya-registration.onrender.com`.

The camera/CV pipeline and the `meditation-app` (which produces the report PDF) are the **hardware team's**; our app calls them and shows the result.

## 2. Runtime flow
```
Admin uploads XLSX roster at /admin (needs ADMIN_KEY)
   -> each person gets a login link  /p/<token>
Person opens their link on phone -> "Proceed" -> camera scanner
   -> scans the kiosk's QR -> POST /api/claim -> session claimed
Kiosk (polling) shows the person's name + photo
   -> AUTO-runs scripts/run1.sh (waits for it to finish)
      run1.sh: HOME1/SHOOT1/CHEST1/EYE1 (~/Desktop/mark1, python3.10) + meditation-app
      meditation-app's `t3` step writes a PDF to /opt/meditation-app/data
   -> kiosk renders the newest PDF on the report screen
   -> "Return" resets for the next person
```

## 3. Key files
- `DiyaMeditation/Views/HomeView.axaml(.cs)` — main screen: QR, poll, photo, auto-run pipeline, report overlay, Return.
- `DiyaMeditation/Views/MainWindow.axaml(.cs)` — fullscreen shell; closable (Alt+F4) + minimisable; no secret shortcut.
- `DiyaMeditation/Services/PipelineRunner.cs` — runs `scripts/run1.sh` via bash, waits for exit.
- `DiyaMeditation/Services/ReportRenderer.cs` — finds newest `*.pdf` in the report dir, renders pages (PDFtoImage/PDFium).
- `DiyaMeditation/scripts/run1.sh` — the editable pipeline (bundled into the `.deb`).
- `server/server.js` `db.js` `schema.sql` — API + Postgres (tables: `visitors`, `sessions`, `people`).
- `registration/index.html` `admin.html` `scan.html` — phone registration, admin roster upload, per-person login.

## 4. Environment variables
- Kiosk: `DIYA_API_BASE`, `DIYA_PIPELINE_SCRIPT`, `DIYA_BASH`, `DIYA_REPORT_DIR`.
- Server: `DATABASE_URL`, `PORT`, `PGSSL`, `ADMIN_KEY`.

## 5. Test the flow WITHOUT cameras (test kit)
The real pipeline needs the cameras + `meditation-app`. To exercise just our app
(login → session → report → **Thank you**) on any Linux desktop, use the bundled
`testkit/` — a mock pipeline that prints status lines and drops a sample PDF:
```bash
export DIYA_PIPELINE_SCRIPT="$(pwd)/testkit/run1.mock.sh"
export DIYA_REPORT_DIR=/tmp/diya-reports
mkdir -p /tmp/diya-reports
diya-meditation        # type a name -> Start (no phone/cameras/server needed)
```
The test kit is external (not bundled in the `.deb`); see `testkit/README.md`.

**Fullscreen fix (v1.6.0):** the meditation-app's OpenCV windows are fullscreened
by `scripts/fullscreen-fixer.sh` (launched from `run1.sh`) — needs **X11** +
`wmctrl` (`sudo apt install -y wmctrl`); safe no-op on Wayland. The report screen
is now white with a **Thank-you** message, and shows only *this* session's PDF.

## 6. Backlog / open items (priority order)
1. **CI to build the `.deb`s and publish as GitHub Releases** — stop committing ~40 MB binaries every change (biggest quality win).
2. **Terminal pop-up** — the hardware team's software opens a stray terminal. `execsnoop` fails on their kernel; use **`forkstat`** (`sudo apt install forkstat; sudo forkstat -e exec | grep -i term`). Need their **source** (`~/Desktop/mark1` + `paths.py`) to locate it.
3. **meditation-app OpenCV windows** (e.g. "Chest_Check") show title bars / aren't fullscreen — needs `cv::setWindowProperty(name, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)` in **their** code.
4. ~~White report screen~~ — **done in v1.6.0** (report overlay restyled white to match the welcome screen, with a Thank-you message).
5. **Consent/privacy screen** before a session (cameras + Aadhaar stored).
6. **Reconcile `PROJECT.md` / `FAQ.md`** with the real current state.
7. **Centralise the version string** (`.csproj`, `build-deb.sh`, `SETUP.md`).

## 7. Gotchas / lessons learned
- **Render:** must track `main` with **Auto-Deploy ON**, or merges never go live. `ADMIN_KEY` is set in the Render dashboard (not in `render.yaml`).
- **Reinstalling the `.deb`:** stop the running app first (`systemctl --user stop diya-meditation; pkill -f DiyaMeditation`) — `dpkg -i` replaces files but the old process keeps running.
- **Editing C# source does NOT update the committed `.deb`** — rebuild with `deploy/build-deb.sh 1.6.0 <arch>`.
- **"Couldn't connect to the server" on the kiosk/VM** is usually a **wrong clock** — a VM clock in the past makes HTTPS certs "not yet valid". Fix: `sudo timedatectl set-ntp true` and enable host time-sync in the VM.
- **Wayland** blocks an app from hiding *other* apps' windows AND from un-minimising/raising *itself* (this is why the post-#24 self-minimise was a bad idea).
- The `meditation-app` package is huge (compiled CV binaries + videos + bundled deps). **Do not upload it to GitHub** (100 MB/file limit). Only the small **source text** is useful to share.

## 8. Working preference
Each distinct change gets **its own branch and its own PR**.
