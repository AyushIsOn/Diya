#!/usr/bin/env bash
# =============================================================================
# fullscreen-fixer.sh
#
# Forces the external meditation-app's OpenCV windows to open FULLSCREEN — i.e.
# with NO title bar and NO minimise/close buttons — WITHOUT modifying or
# recompiling the meditation-app. It simply asks the window manager to fullscreen
# any window whose title matches one of the names below, as soon as it appears.
#
# Requirements / scope:
#   - X11 only (uses `wmctrl`). On Wayland this is a safe no-op.
#   - If `wmctrl` is not installed, it exits quietly (install: sudo apt install wmctrl).
#
# The two windows that actually pop up with chrome during a session are:
#   - "Front"                     (bin/Front)
#   - "FRONT AND SIDE ADJUSTMENT" (depth_bin/adjustment_test_updated)
# Add more titles here if other windows appear with a title bar.
#
# Usage: run in the background before launching meditation-app, then kill it when
# the session ends (see run1.sh).
# =============================================================================

set -u

# Window titles to fullscreen (matched as a substring of the window title).
TITLES=(
    "Front"
    "FRONT AND SIDE ADJUSTMENT"
)

if ! command -v wmctrl >/dev/null 2>&1; then
    echo "[fullscreen-fixer] wmctrl not found — skipping (install: sudo apt install wmctrl)."
    exit 0
fi

# Only meaningful on X11. On Wayland, wmctrl can't manage windows; no-op.
if [[ "${XDG_SESSION_TYPE:-}" == "wayland" ]]; then
    echo "[fullscreen-fixer] Wayland session detected — skipping (X11 recommended)."
    exit 0
fi

echo "[fullscreen-fixer] watching for meditation-app windows to fullscreen ..."
while true; do
    for title in "${TITLES[@]}"; do
        if wmctrl -l 2>/dev/null | grep -qF -- "$title"; then
            wmctrl -r "$title" -b add,fullscreen 2>/dev/null || true
        fi
    done
    sleep 0.5
done
