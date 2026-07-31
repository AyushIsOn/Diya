# Diya — Handoff & Current State

A living "where things stand + what's next" doc, so anyone (a new developer, a new
chat session, or the Kiro CLI) can pick up quickly. For depth see `PROJECT.md`
(overview), `SETUP.md` (all commands), `FAQ.md` (Q&A), and
`docs/Diya-Codebase-Overview.pdf` (file-by-file).

> Keep this updated as work lands. It is a snapshot, not the source of truth —
> trust the code and `SETUP.md` over anything here that looks stale.

---

## 1. What it is
An unattended meditation kiosk. Two parts we own:
- **Kiosk app** — `DiyaMeditation/` — C#/.NET 8 + Avalonia, shipped as a `.deb`. Version **1.5.0**.
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
   -> kiosk renders the newest PDF on a WHITE report screen
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
- `testkit/` — no-camera test kit (mock pipeline + sample PDF). Not bundled in the `.deb`.

## 4. Environment variables
- Kiosk: `DIYA_API_BASE`, `DIYA_PIPELINE_SCRIPT`, `DIYA_BASH`, `DIYA_REPORT_DIR`.
- Server: `DATABASE_URL`, `PORT`, `PGSSL`, `ADMIN_KEY`.

## 5. Test the flow WITHOUT cameras
```bash
chmod +x testkit/run1.mock.sh
export DIYA_PIPELINE_SCRIPT="$(pwd)/testkit/run1.mock.sh"
export DIYA_REPORT_DIR=/tmp/diya-reports
diya-meditation        # type a name -> Start (no phone/cameras needed)
```
To run the real pipeline, just don't set those two vars.

## 6. Open PRs to resolve
- **Merge `#28`** — removes a window self-minimize that broke on Wayland (app appeared to close on login) and makes the report screen **white**. Rebuilt both 1.5.0 `.deb`s.
- **Close `#27`** — superseded by #28 and conflicted.
- (#25 window-handoff/testkit and #26 SETUP docs are already merged; #28 corrects the minimize they introduced.)

## 7. Backlog / open items (priority order)
1. **CI to build the `.deb`s and publish as GitHub Releases** — stop committing ~40 MB binaries every change (biggest quality win).
2. **Terminal pop-up** — the hardware team's software opens a stray terminal. `execsnoop` fails on their kernel; use **`forkstat`** (`sudo apt install forkstat; sudo forkstat -e exec | grep -i term`). Need their **source** (the `~/Desktop/mark1` scripts + `paths.py`) to locate exactly what opens it.
3. **meditation-app OpenCV windows** (e.g. "Chest_Check") show title bars / aren't fullscreen — needs `cv::setWindowProperty(name, WND_PROP_FULLSCREEN, WINDOW_FULLSCREEN)` in **their** code.
4. **Consent/privacy screen** before a session (cameras + Aadhaar stored).
5. **Reconcile `PROJECT.md` / `FAQ.md`** with the real current state (they still describe aspirational/branch-only features + an old version table).
6. **Centralise the version string** (currently in `.csproj`, `build-deb.sh`, `SETUP.md`).

## 8. Gotchas / lessons learned
- **Render:** must track the `main` branch with **Auto-Deploy ON**, or merges never go live. `ADMIN_KEY` is set in the Render dashboard (not in `render.yaml`).
- **Reinstalling the `.deb`:** stop the running app first (`systemctl --user stop diya-meditation; pkill -f DiyaMeditation`) — `dpkg -i` replaces files but the old process keeps running.
- **Editing C# source does NOT update the committed `.deb`** — rebuild with `deploy/build-deb.sh 1.5.0 <arch>`.
- **"Couldn't connect to the server" on the kiosk/VM** is usually a **wrong clock** — a VM clock in the past makes HTTPS certs "not yet valid". Fix: `sudo timedatectl set-ntp true` (or set-time manually) and enable host time-sync in the VM.
- **Wayland** blocks an app from hiding *other* apps' windows AND from un-minimising/raising *itself* — that's why the session-minimize was removed, and why the stray terminal can't be hidden from our side on Wayland.
- The `meditation-app` package is huge (compiled CV binaries + videos + bundled deps). **Do not upload it to GitHub** (100 MB/file limit). Only the small **source text** is useful to share.

## 9. Working preference
Each distinct change gets **its own branch and its own PR** (don't stack follow-up commits onto an existing PR).
