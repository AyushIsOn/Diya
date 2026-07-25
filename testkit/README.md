# Diya test kit — run the whole flow without cameras

This folder lets you test the **Diya app** end-to-end on any Ubuntu machine with
**no cameras** and **without the hardware team's meditation-app**.

It works by faking the pipeline: instead of running the real cameras, a mock
script waits a few seconds and drops a sample PDF into the folder the app watches.
The app then does everything it normally does — shows the QR, waits for a login,
shows a "please wait" state while the "session" runs, then displays the report.

> **This kit is NOT part of the app.** It is driven entirely by two environment
> variables. To run the real pipeline, simply **don't set them** (and you can
> delete this `testkit/` folder). The app then uses the real bundled
> `scripts/run1.sh` and `/opt/meditation-app/data`. There is no mock code inside
> the app to remove.

## Files
- `run1.mock.sh` — the fake pipeline (waits, then drops the sample PDF).
- `sample-report.pdf` — a stand-in report shown on screen.

## How to run
1. Install / run the Diya app (from the `.deb`, or `dotnet run` in `DiyaMeditation/`).
2. In the same shell, point the app at the mock and a writable report folder:
   ```bash
   chmod +x testkit/run1.mock.sh
   export DIYA_PIPELINE_SCRIPT="$(pwd)/testkit/run1.mock.sh"
   export DIYA_REPORT_DIR=/tmp/diya-reports
   diya-meditation          # or:  cd DiyaMeditation && dotnet run
   ```
3. Start a "session" one of two ways:
   - **No phone needed:** type any name in the on-screen box and click **Start**, or
   - scan the QR with your phone and register (the server is online).
4. You'll see the app show **"please wait"** for ~5 seconds, then the **sample
   report** appears on screen. Press **Return** to reset for the next person.

## Options
- `DIYA_MOCK_DELAY` — change the fake session length, e.g. `export DIYA_MOCK_DELAY=2`.

## What this proves (and what it doesn't)
- ✅ Login, the "please wait" state, report display, and reset.
- ❌ The real cameras, the meditation-app, and the terminal pop-up — those need
  the hardware and can only be verified on the kiosk machine.
