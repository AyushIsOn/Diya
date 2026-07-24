#!/usr/bin/env bash
# =============================================================================
# run1.mock.sh  -  FAKE pipeline for testing the Diya app WITHOUT cameras.
#
# This is NOT part of the app. It stands in for the real scripts/run1.sh so you
# can exercise the whole Diya flow (login -> pipeline -> report) on any machine
# with no RealSense/USB cameras and without the hardware team's meditation-app.
#
# It simply:
#   1. waits a few seconds (pretending the meditation session ran), then
#   2. copies a sample PDF into the report directory the app watches.
#
# Use it by pointing the app at it with two environment variables (see README):
#   export DIYA_PIPELINE_SCRIPT=/path/to/testkit/run1.mock.sh
#   export DIYA_REPORT_DIR=/tmp/diya-reports
#
# To hand the build to the hardware team, just DON'T set those variables — the
# app then uses the real bundled scripts/run1.sh and /opt/meditation-app/data.
# Nothing to remove from the app itself.
# =============================================================================
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="${DIYA_REPORT_DIR:-/tmp/diya-reports}"
DELAY="${DIYA_MOCK_DELAY:-5}"

echo "[mock] pretending to run the meditation session (${DELAY}s)..."
sleep "${DELAY}"

mkdir -p "${DEST}"
cp "${HERE}/sample-report.pdf" "${DEST}/report_$(date +%s).pdf"

echo "[mock] wrote a sample report to ${DEST}"
echo "[mock] done."
