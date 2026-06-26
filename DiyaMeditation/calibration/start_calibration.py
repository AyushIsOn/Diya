#!/usr/bin/env python3
"""
start_calibration.py — entry point the kiosk runs when "Start Calibration" is pressed.

The kiosk launches this with `python3 start_calibration.py` and watches its stdout.
If ANY output appears, the kiosk shows "Starting calibration".

Right now there is no camera/servo hardware attached, so this just runs the camera
discovery from camera_utils.py and prints status (the "serial output"). When the
real hardware is ready, add the camera capture / servo / serial code below and
repackage the .deb (see SETUP.md -> "Update the calibration script & repackage").

NOTE: camera_utils.py is intentionally left unmodified. Put hardware logic here,
or in new modules imported here.
"""

import sys
from datetime import datetime

try:
    from camera_utils import find_cameras_by_name, get_camera_index
except Exception as exc:  # keep going even if the import has an issue
    find_cameras_by_name = None
    get_camera_index = None
    _import_error = exc
else:
    _import_error = None


def log(message: str) -> None:
    # flush=True so the kiosk sees output immediately (line-buffered "serial" feed).
    print(f"[{datetime.now():%H:%M:%S}] {message}", flush=True)


def main() -> int:
    log("[calibration] starting Diya calibration sequence")

    if _import_error is not None:
        log(f"[calibration] camera_utils import issue: {_import_error}")

    # --- Camera discovery (hardware optional right now) -------------------
    if find_cameras_by_name is not None:
        try:
            detected = find_cameras_by_name()
            log(f"[camera] detected: {detected if detected else 'none (hardware pending)'}")
        except Exception as exc:
            log(f"[camera] detection error: {exc}")

    for cam in ("logitech", "arducam"):
        if get_camera_index is None:
            break
        try:
            src = get_camera_index(cam)
            log(f"[camera] {cam} -> {src}")
        except Exception as exc:
            log(f"[camera] {cam} unavailable: {exc}")

    # --- Servo / serial placeholder (no hardware yet) ---------------------
    # TODO: open the servo serial port and run the calibration routine here.
    log("[servo] initializing servo controller ... (hardware pending)")

    log("[calibration] READY")
    return 0


if __name__ == "__main__":
    sys.exit(main())
