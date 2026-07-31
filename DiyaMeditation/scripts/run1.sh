#!/usr/bin/env bash
# =============================================================================
# run_pipeline.sh
# Pipeline: HOME1 → SHOOT1 → CHEST1 → EYE1 → meditation-app
#
# Retry logic (mirrors the diagram):
#   HOME1  : failure → retry HOME1  (loop on itself)
#   SHOOT1 : failure → retry SHOOT1 (loop on itself)
#   CHEST1 : failure → restart from HOME1
#   EYE1   : failure → restart from HOME1
# =============================================================================

set -euo pipefail

WORK_DIR="$HOME/Desktop/mark1"
PYTHON="python3.10"

# ── colours for readability ──────────────────────────────────────────────────
RED='\033[0;31m'
GRN='\033[0;32m'
YLW='\033[1;33m'
BLU='\033[0;34m'
NC='\033[0m'   # reset

log_info()  { echo -e "${BLU}[INFO ]${NC}  $*"; }
log_ok()    { echo -e "${GRN}[OK   ]${NC}  $*"; }
log_warn()  { echo -e "${YLW}[RETRY]${NC}  $*"; }
log_err()   { echo -e "${RED}[FAIL ]${NC}  $*"; }

# ── helpers ──────────────────────────────────────────────────────────────────

# run_step <label> <script_or_cmd...>
#   Runs the command from WORK_DIR.
#   Returns 0 on success, 1 on failure.
run_step() {
    local label="$1"
    shift
    log_info "Running $label ..."
    if (cd "$WORK_DIR" && "$@"); then
        log_ok "$label succeeded."
        return 0
    else
        local code=$?
        log_err "$label exited with code $code."
        return 1
    fi
}

# ── sanity checks ────────────────────────────────────────────────────────────
if [[ ! -d "$WORK_DIR" ]]; then
    log_err "Work directory not found: $WORK_DIR"
    exit 1
fi

for script in HOME1.py SHOOT1.py CHEST1.py EYE1.py; do
    if [[ ! -f "$WORK_DIR/$script" ]]; then
        log_err "Missing script: $WORK_DIR/$script"
        exit 1
    fi
done

if ! command -v meditation-app &>/dev/null; then
    log_err "meditation-app is not installed or not in PATH. Install it with:"
    log_err "  sudo apt install meditation-app_1.0_amd64.deb"
    exit 1
fi

# ── window fix: fullscreen the meditation-app's OpenCV windows (X11 only) ─────
# Removes the title bar / minimise-close buttons on the external app's windows
# without modifying it. Runs alongside the pipeline; safe no-op on Wayland or if
# wmctrl is missing. Stopped after the pipeline finishes (see end of file).
FIXER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/fullscreen-fixer.sh"
FIXER_PID=""
if [[ -f "$FIXER" ]]; then
    bash "$FIXER" &
    FIXER_PID=$!
    log_info "Started window fullscreen-fixer (pid $FIXER_PID)."
    # Ensure the fixer is stopped on ANY exit (normal, error, or signal).
    trap '[[ -n "${FIXER_PID:-}" ]] && kill "$FIXER_PID" 2>/dev/null || true' EXIT
fi

# ── main pipeline loop ───────────────────────────────────────────────────────
while true; do

    # ── STEP 1: HOME1.py — retry itself on failure ───────────────────────
    while true; do
        if run_step "HOME1.py" "$PYTHON" HOME1.py; then
            break          # success → proceed to SHOOT1
        fi
        log_warn "HOME1.py failed — retrying HOME1.py ..."
        sleep 1
    done

    # ── STEP 2: SHOOT1.py — retry itself on failure ──────────────────────
    while true; do
        if run_step "SHOOT1.py" "$PYTHON" SHOOT1.py; then
            break          # success → proceed to CHEST1
        fi
        log_warn "SHOOT1.py failed — retrying SHOOT1.py ..."
        sleep 1
    done

    # ── STEP 3: CHEST1.py — failure restarts from HOME1 ─────────────────
    if ! run_step "CHEST1.py" "$PYTHON" CHEST1.py; then
        log_warn "CHEST1.py failed — restarting pipeline from HOME1.py ..."
        sleep 1
        continue           # jump back to top of outer while-loop
    fi

    # ── STEP 4: EYE1.py — failure restarts from HOME1 ───────────────────
    if ! run_step "EYE1.py" "$PYTHON" EYE1.py; then
        log_warn "EYE1.py failed — restarting pipeline from HOME1.py ..."
        sleep 1
        continue           # jump back to top of outer while-loop
    fi

    # ── STEP 5: meditation-app ────────────────────────────────────────────
    log_info "Launching meditation-app ..."
    if meditation-app; then
        log_ok "meditation-app exited cleanly. Pipeline complete."
    else
        log_err "meditation-app exited with an error."
    fi

    # Pipeline finished (successfully or app error) — exit the outer loop
    break

done

# ── cleanup: stop the fullscreen-fixer if it was started ─────────────────────
if [[ -n "${FIXER_PID:-}" ]]; then
    kill "$FIXER_PID" 2>/dev/null || true
    log_info "Stopped window fullscreen-fixer."
fi
