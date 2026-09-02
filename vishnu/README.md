# Vishnu — Diya codebase

Snapshot of the local Diya working tree, contributed as a single folder so it
can be reviewed without disturbing the existing project layout at the repo root.

## Contents

| Folder | What it is |
|---|---|
| `Diya-main/` | Avalonia .NET 8 meditation app (`DiyaMeditation`) — views, services, deploy scripts |
| `deb/` | `.deb` packaging tree for `meditation-app` — control scripts, desktop entry, systemd unit, data assets |
| `latest_A/` | Calibration stage |
| `am-mock-server/` | FastAPI mock attendance/FRS server |
| `am-mock-client/` | Mock client, incl. face recognition + diagnostic mode |
| `mark1/` | Early prototype |
| `DIYA-SYSTEM-ANALYSIS.md` | System analysis notes |

## Not included

Excluded via `.gitignore` because they are regenerable, re-downloadable, or
exceed GitHub's 100 MB per-file limit:

- Python virtualenvs (`.venv/`, `venv/`) and `__pycache__/`
- Build output — `bin/`, `obj/`, `build/`, `dist/`, `depth_bin/`
- Compiled binaries (212–252 MB each) and bundled Ubuntu dependency `.deb` files
- Videos, and ML model weights (`*.pt`, `*.pth`, `*.npz`)
- `meditation_gui_updated/` — legacy GUI, kept out of the current workflow

Rebuild the .NET app with `dotnet build`; recreate the Python environments from
each project's `requirements.txt`; re-fetch system packages with `apt`.
