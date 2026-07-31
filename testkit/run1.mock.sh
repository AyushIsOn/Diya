#!/usr/bin/env bash
# =============================================================================
# run1.mock.sh — no-camera TEST pipeline for the Diya kiosk (v1.6.0)
#
# Exercises the whole flow (login -> session -> report -> "Thank you") WITHOUT
# any cameras, the external meditation-app, or the server. Point the kiosk at
# this script and a writable report dir, then run it:
#
#   export DIYA_PIPELINE_SCRIPT="$(pwd)/testkit/run1.mock.sh"
#   export DIYA_REPORT_DIR=/tmp/diya-reports
#   mkdir -p /tmp/diya-reports
#   diya-meditation        # type a name -> Start (no phone/server needed)
#
# It prints a few status lines (so you see the live status update on screen),
# waits a few seconds, then drops a sample report PDF into DIYA_REPORT_DIR with a
# fresh timestamp, so the app displays it exactly like a real session's report.
# =============================================================================
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${DIYA_REPORT_DIR:-/tmp/diya-reports}"
mkdir -p "$DEST"

# Use the bundled sample; fall back to the repo's codebase-overview PDF.
SAMPLE=""
for candidate in "$HERE/sample-report.pdf" "$HERE/../docs/Diya-Codebase-Overview.pdf"; do
    if [ -f "$candidate" ]; then SAMPLE="$candidate"; break; fi
done

echo "Calibrating cameras...";                     sleep 2
echo "Running meditation session...";              sleep 3
echo "Analysing posture, gaze, thermal, depth..."; sleep 2
echo "Running t3 (PDF report)...";                 sleep 1

if [ -z "$SAMPLE" ]; then
    echo "No sample PDF found (expected testkit/sample-report.pdf)." >&2
    exit 1
fi

cp -f "$SAMPLE" "$DEST/Complete_Report_Sub_2.pdf"
touch "$DEST/Complete_Report_Sub_2.pdf"   # fresh mtime = counts as THIS session's report
echo "All tasks completed successfully."
