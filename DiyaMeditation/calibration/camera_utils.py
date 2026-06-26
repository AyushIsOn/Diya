# camera_utils.py
import os
import subprocess
import re

CAMERA_CONFIG = {
    "logitech": "/dev/v4l/by-id/usb-Logitech_HD_Pro_Webcam_C920_XXXX-video-index0",
    "arducam":  "/dev/v4l/by-id/usb-ArduCam_XXXX-video-index0",
}

def find_cameras_by_name():
    cameras = {}
    try:
        result = subprocess.run(
            ['v4l2-ctl', '--list-devices'],
            capture_output=True, text=True, timeout=5
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("[WARN] v4l2-ctl not available.")
        return cameras

    current_name = ""
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line.startswith('/dev/video'):
            current_name = line.lower()
        else:
            m = re.search(r'/dev/video(\d+)', line)
            if not m:
                continue
            index = int(m.group(1))
            if 'hd pro webcam' in current_name and 'logitech' not in cameras:
                cameras['logitech'] = index
            elif 'arducam' in current_name and 'arducam' not in cameras:
                cameras['arducam'] = index
    return cameras

def resolve_camera(name: str, fallback_index: int | None = None):
    path = CAMERA_CONFIG.get(name)
    if path and os.path.exists(path):
        print(f"[{name}] Using stable path: {path}")
        return path
    print(f"[{name}] Stable path not found, falling back to index {fallback_index}")
    return fallback_index

def get_camera_index(name: str) -> int | str | None:
    """
    Returns the OpenCV-openable path or integer index for `name`.
    Call this once at startup; pass the result to cv2.VideoCapture().
    """
    detected = find_cameras_by_name()
    src = resolve_camera(name, detected.get(name))
    if src is None:
        raise RuntimeError(
            f"[camera_utils] Could not resolve camera '{name}'. "
            "Check the connection or update CAMERA_CONFIG."
        )
    return src
