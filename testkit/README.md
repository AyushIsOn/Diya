# Diya test kit — run the whole flow without cameras

Exercise the kiosk end to end (**login → session → report → "Thank you"**) on any
Linux machine with **no cameras, no meditation-app, and no server**.

## What's here
- **`run1.mock.sh`** — a stand-in for the real `run1.sh`. It prints a few status
  lines (so you can watch the live status update), waits ~8s, then copies a sample
  report PDF into your report folder so the app displays it.
- **`sample-report.pdf`** — the stand-in report (a copy of
  `docs/Diya-Codebase-Overview.pdf`).

It is driven purely by two environment variables, so there is **no test/mock code
inside the app** and **nothing is bundled in the `.deb`**.

## Run it
```bash
# from the repo root, on the machine running the kiosk (Linux)
export DIYA_PIPELINE_SCRIPT="$(pwd)/testkit/run1.mock.sh"
export DIYA_REPORT_DIR=/tmp/diya-reports
mkdir -p /tmp/diya-reports

diya-meditation        # or, from source:  cd DiyaMeditation && dotnet run
```
On the welcome screen, **type a name and press Start** (the name-entry fallback
needs no phone/QR/server). You will see:
1. the **live status line** update ("Calibrating cameras…", "Running t3 (PDF
   report)…", …),
2. the app **display the sample report**, then
3. **"Thank you, &lt;name&gt;"** with a **Return** button.

## Back to the real pipeline
Just unset the two variables (or launch the app without them):
```bash
unset DIYA_PIPELINE_SCRIPT DIYA_REPORT_DIR
```

> Note: this only needs a Linux desktop to run the app — it does **not** need X11
> or `wmctrl` (those are only for fullscreening the real meditation-app's windows).
