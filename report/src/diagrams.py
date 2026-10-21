"""Generates every diagram used in the internship report (PNG, 220 dpi)."""
import os
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)

INK = "#1F2937"
MUTED = "#6B7280"
C_US = "#DBEAFE"      # our components
C_US_E = "#1D4ED8"
C_HW = "#FDE68A"      # hardware team
C_HW_E = "#B45309"
C_EXT = "#E5E7EB"     # external / cloud
C_EXT_E = "#4B5563"
C_OK = "#DCFCE7"
C_OK_E = "#15803D"
C_RED = "#FEE2E2"
C_RED_E = "#B91C1C"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
})


def canvas(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w)
    ax.set_ylim(0, h)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, text, fc=C_US, ec=C_US_E, size=9.5, bold_first=True, r=0.08, ls="-"):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={r}",
                       fc=fc, ec=ec, lw=1.4, ls=ls)
    ax.add_patch(p)
    lines = text.split("\n")
    if bold_first and len(lines) > 1:
        sub = lines[1:]
        sub_size = size - 1.5
        title_h = size / 72 * 1.15
        sub_h = sub_size / 72 * 1.3 * len(sub)
        gap = 0.07
        block = title_h + gap + sub_h
        top = y + h / 2 + block / 2
        ax.text(x + w / 2, top, lines[0], ha="center", va="top",
                fontsize=size, fontweight="bold", color=INK)
        ax.text(x + w / 2, top - title_h - gap, "\n".join(sub),
                ha="center", va="top", fontsize=sub_size, color=MUTED, linespacing=1.3)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size,
                fontweight="bold" if bold_first else "normal", color=INK)
    return (x, y, w, h)


def arrow(ax, p1, p2, label=None, color=INK, ls="-", rad=0.0, lpos=0.5, loff=(0, 0.12), size=8, both=False):
    a = FancyArrowPatch(p1, p2, arrowstyle="<|-|>" if both else "-|>", mutation_scale=12,
                        color=color, lw=1.3, ls=ls, connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(a)
    if label:
        mx = p1[0] + (p2[0] - p1[0]) * lpos + loff[0]
        my = p1[1] + (p2[1] - p1[1]) * lpos + loff[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=size, color=color,
                bbox=dict(fc="white", ec="none", pad=1.2))


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


# ---------------------------------------------------------------- architecture
def architecture():
    fig, ax = canvas(11.6, 6.6)
    # zones
    for (x, y, w, h, title, ec) in [
        (0.2, 0.3, 3.0, 5.9, "Visitor / Admin devices", C_EXT_E),
        (3.5, 0.3, 3.6, 5.9, "Cloud (Render)", C_EXT_E),
        (7.4, 0.3, 4.1, 5.9, "Kiosk machine (Ubuntu · Wayland)", C_US_E),
    ]:
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="white", ec=ec, lw=1.0, ls="--"))
        ax.text(x + 0.15, y + h - 0.22, title, fontsize=9, color=ec, fontweight="bold", va="center")

    box(ax, 0.5, 4.3, 2.4, 1.0, "Admin PC (browser)\nadmin.html · SheetJS\nuploads .xlsx roster", C_EXT, C_EXT_E)
    box(ax, 0.5, 1.6, 2.4, 1.3, "Visitor's phone\nscan.html · html5-qrcode\nopens /p/<token>,\nscans kiosk QR", C_EXT, C_EXT_E)

    box(ax, 3.8, 3.4, 3.0, 1.6, "Backend API\nNode.js · Express\n/api/sessions · /api/claim\n/api/admin/upload · /api/people", C_US, C_US_E)
    box(ax, 3.8, 1.0, 3.0, 1.3, "PostgreSQL\nvisitors · sessions · people", C_US, C_US_E)

    box(ax, 7.7, 3.9, 2.8, 1.6, "Diya kiosk app\nC# · .NET 8 · Avalonia\nQR · polling · report view\n(self-contained .deb)", C_US, C_US_E)
    box(ax, 7.7, 2.2, 2.8, 1.1, "scripts/run1.sh\nbash pipeline + retries", C_US, C_US_E)
    box(ax, 7.7, 0.55, 2.8, 1.15, "Hardware team stack\nHOME/SHOOT/CHEST/EYE .py\nmeditation-app (.deb)", C_HW, C_HW_E)

    arrow(ax, (2.9, 4.8), (3.8, 4.55), "HTTPS\nroster upload", size=7.5, loff=(0, 0.28))
    arrow(ax, (2.9, 2.4), (3.8, 3.6), "HTTPS\nclaim", size=7.5, loff=(-0.15, 0.1))
    arrow(ax, (5.3, 3.4), (5.3, 2.3), "SQL", both=True, size=7.5, loff=(0.3, 0))
    arrow(ax, (7.7, 4.7), (6.8, 4.5), "HTTPS: create\nsession / poll", size=7.5, loff=(0, 0.3), both=True)
    arrow(ax, (7.7, 3.95), (2.9, 1.75), None, color=C_HW_E, ls=":", rad=-0.12)
    ax.text(5.25, 0.62, "phone camera reads the QR shown on the kiosk screen", ha="center",
            fontsize=7.5, color=C_HW_E, bbox=dict(fc="white", ec="none", pad=1))
    arrow(ax, (9.1, 3.9), (9.1, 3.3), None)
    ax.text(9.2, 3.6, "on claim", fontsize=7.5, color=MUTED, va="center")
    arrow(ax, (9.1, 2.2), (9.1, 1.7), None)
    ax.text(9.2, 1.95, "spawns", fontsize=7.5, color=MUTED, va="center")
    arrow(ax, (10.5, 1.2), (10.5, 3.9), None, color=C_HW_E, ls=":", rad=0.5)
    ax.text(11.05, 2.55, "report PDF\nwritten to\n/opt/meditation-\napp/data", ha="center", va="center",
            fontsize=7, color=C_HW_E, bbox=dict(fc="white", ec="none", pad=1))

    # legend
    ax.add_patch(FancyBboxPatch((0.4, -0.35), 0.3, 0.2, boxstyle="round,pad=0.01", fc=C_US, ec=C_US_E))
    ax.text(0.8, -0.25, "Built during this internship", fontsize=8, va="center")
    ax.add_patch(FancyBboxPatch((3.4, -0.35), 0.3, 0.2, boxstyle="round,pad=0.01", fc=C_HW, ec=C_HW_E))
    ax.text(3.8, -0.25, "Collaborating hardware/CV team", fontsize=8, va="center")
    ax.add_patch(FancyBboxPatch((6.6, -0.35), 0.3, 0.2, boxstyle="round,pad=0.01", fc=C_EXT, ec=C_EXT_E))
    ax.text(7.0, -0.25, "User devices", fontsize=8, va="center")
    ax.set_ylim(-0.5, 6.6)
    save(fig, "fig_architecture.png")


# ---------------------------------------------------------------- state machine
def visitor_flow():
    fig, ax = canvas(11, 3.6)
    states = [
        ("IDLE\nsession created,\nQR on screen", C_EXT, C_EXT_E),
        ("CLAIMED\nname + photo\nshown", C_US, C_US_E),
        ("SESSION\nrun1.sh running,\nlive status line", C_HW, C_HW_E),
        ("REPORT\nnewest PDF rendered\n+ thank-you", C_OK, C_OK_E),
    ]
    xs = [0.3, 3.0, 5.7, 8.4]
    for x, (t, fc, ec) in zip(xs, states):
        box(ax, x, 1.5, 2.2, 1.3, t, fc, ec, size=10)
    labels = ["phone claims\nthe session", "auto-start\n(or Start)", "script exits"]
    for i in range(3):
        arrow(ax, (xs[i] + 2.2, 2.15), (xs[i + 1], 2.15), labels[i], size=7.5, loff=(0, 0.35))
    # return loop (routed underneath the boxes)
    ax.plot([9.5, 9.5], [1.5, 0.75], color=INK, lw=1.3)
    ax.plot([9.5, 1.4], [0.75, 0.75], color=INK, lw=1.3)
    arrow(ax, (1.4, 0.75), (1.4, 1.5), None)
    ax.text(5.45, 0.75, "\"Return\" pressed → new session token → back to IDLE", ha="center", va="center",
            fontsize=8, color=INK, bbox=dict(fc="white", ec="none"))
    # manual fallback (routed above)
    ax.plot([1.4, 1.4], [2.8, 3.35], color=MUTED, lw=1.1, ls="--")
    ax.plot([1.4, 4.1], [3.35, 3.35], color=MUTED, lw=1.1, ls="--")
    arrow(ax, (4.1, 3.35), (4.1, 2.8), None, color=MUTED, ls="--")
    ax.text(2.75, 3.35, "manual name entry (offline fallback)", ha="center", va="center", fontsize=7.5,
            color=MUTED, bbox=dict(fc="white", ec="none", pad=1))
    ax.text(1.5, 1.3, "\"New code\" re-issues the token", ha="left", fontsize=7, color=MUTED)
    ax.set_ylim(0.4, 3.6)
    save(fig, "fig_visitor_flow.png")


# ---------------------------------------------------------------- ER diagram
def er_diagram():
    fig, ax = canvas(10, 4.4)

    def table(x, y, name, cols, w=2.9):
        rh = 0.3
        h = rh * (len(cols) + 1)
        ax.add_patch(FancyBboxPatch((x, y - h), w, h, boxstyle="round,pad=0.0,rounding_size=0.05",
                                    fc="white", ec=C_US_E, lw=1.3))
        ax.add_patch(FancyBboxPatch((x, y - rh), w, rh, boxstyle="round,pad=0.0,rounding_size=0.05",
                                    fc=C_US_E, ec=C_US_E, lw=1.3))
        ax.text(x + w / 2, y - rh / 2, name, ha="center", va="center", color="white", fontweight="bold")
        for i, (c, t, k) in enumerate(cols):
            yy = y - rh * (i + 1.5)
            ax.text(x + 0.12, yy, ("🔑 " if False else "") + c, va="center", fontsize=8.5,
                    fontweight="bold" if k == "PK" else "normal", color=INK)
            ax.text(x + w - 0.12, yy, t + (f"  {k}" if k else ""), va="center", ha="right", fontsize=7.5,
                    color=MUTED)
        return (x, y - h, w, h)

    table(0.2, 4.2, "people  (admin roster)", [
        ("token", "TEXT", "PK"), ("name", "TEXT", ""), ("role", "TEXT", ""), ("aadhar", "TEXT", "private"),
        ("email", "TEXT", ""), ("image_url", "TEXT", ""), ("created_at", "TIMESTAMPTZ", "")])
    table(4.4, 4.2, "visitors", [
        ("id", "TEXT", "PK"), ("name", "TEXT", ""), ("email", "TEXT", ""), ("age", "INTEGER", ""),
        ("image_url", "TEXT", ""), ("created_at", "TIMESTAMPTZ", "")])
    table(8.6, 4.2, "sessions", [
        ("token", "TEXT", "PK"), ("status", "pending|claimed", ""), ("visitor_id", "TEXT", "FK"),
        ("created_at", "TIMESTAMPTZ", ""), ("claimed_at", "TIMESTAMPTZ", "")], w=2.9)
    arrow(ax, (3.1, 3.45), (4.4, 3.45), None, color=MUTED, ls="--")
    ax.text(3.75, 2.95, "copied into a\nvisitor row\non /api/claim", ha="center", va="top", fontsize=7.5,
            color=MUTED)
    arrow(ax, (8.6, 3.15), (7.3, 3.75), None)
    ax.text(7.95, 2.75, "visitor_id →\nvisitors.id\n(set when\nclaimed)", ha="center", va="top", fontsize=7.5,
            color=INK)
    ax.set_xlim(0, 11.7)
    ax.set_ylim(1.8, 4.4)
    save(fig, "fig_er_diagram.png")


# ---------------------------------------------------------------- hardware block diagram
def hardware():
    fig, ax = canvas(11, 5.4)
    box(ax, 4.0, 2.2, 3.0, 1.2, "Kiosk PC (Ubuntu)\nDiya app · run1.sh\nCV scripts · meditation-app", C_US, C_US_E, size=10)
    cams = [
        ("Logitech C920 webcam\nface / gaze", 0.2, 4.2),
        ("Intel RealSense D435\ndepth", 0.2, 3.0),
        ("Arducam 8MP\nfront / posture", 0.2, 1.8),
        ("USB thermal camera\nthermal capture", 0.2, 0.6),
    ]
    for t, x, y in cams:
        box(ax, x, y, 2.8, 0.85, t, C_EXT, C_EXT_E)
        arrow(ax, (x + 2.8, y + 0.42), (4.0, 2.8), None, color=C_EXT_E)
    ax.text(3.5, 5.0, "cameras on USB (V4L2)", fontsize=8, color=C_EXT_E, ha="center")

    box(ax, 8.1, 3.7, 2.7, 1.1, "Arduino controller\nserial 115200 baud\nASCII command protocol", C_HW, C_HW_E)
    box(ax, 8.1, 1.95, 2.7, 1.2, "Motors M1 / M2\nM1 chest axis · M2 eye axis\nhoming · actuator 'shoot'", C_HW, C_HW_E)
    box(ax, 8.1, 0.3, 2.7, 1.2, "Safety inputs\nNO+NC home limit switches\ncollision switch · prox sensors", C_HW, C_HW_E)
    box(ax, 4.15, 0.3, 2.7, 1.1, "LD2410 mmWave radar\nseat presence (650–1050 mm)\nserial 256000 baud", C_HW, C_HW_E)
    box(ax, 4.15, 4.2, 2.7, 0.9, "Display (fullscreen)\nkiosk UI · meditation video", C_EXT, C_EXT_E)

    arrow(ax, (7.0, 3.1), (8.1, 4.1), "USB serial", both=True, size=7.5, loff=(0, 0.15))
    arrow(ax, (9.45, 3.7), (9.45, 3.15), None, both=True)
    arrow(ax, (9.45, 1.5), (9.45, 1.95), None)
    arrow(ax, (5.5, 1.4), (5.5, 2.2), "USB serial", size=7.5, loff=(0.55, 0))
    arrow(ax, (5.5, 3.4), (5.5, 4.2), "HDMI", size=7.5, loff=(0.4, 0))
    save(fig, "fig_hardware_block.png")


# ---------------------------------------------------------------- run1.sh flowchart
def pipeline():
    fig, ax = canvas(11, 4.4)
    steps = [("HOME1.py", "home both axes"), ("SHOOT1.py", "deploy actuators"),
             ("CHEST1.py", "align chest camera"), ("EYE1.py", "align eye camera"),
             ("meditation-app", "session + PDF report")]
    xs = [0.2, 2.35, 4.5, 6.65, 8.8]
    for x, (n, d) in zip(xs, steps):
        fc, ec = (C_HW, C_HW_E)
        box(ax, x, 2.0, 1.9, 0.95, f"{n}\n{d}", fc, ec, size=9.5)
    for i in range(4):
        arrow(ax, (xs[i] + 1.9, 2.47), (xs[i + 1], 2.47), "ok", size=7.5, loff=(0, 0.17), color=C_OK_E)
    # self retry loops
    for i in range(2):
        x = xs[i]
        a = FancyArrowPatch((x + 1.4, 2.95), (x + 0.5, 2.95), arrowstyle="-|>", mutation_scale=11,
                            color=C_RED_E, lw=1.2, connectionstyle="arc3,rad=1.4")
        ax.add_patch(a)
        ax.text(x + 0.95, 3.85, "fail → retry itself", ha="center", fontsize=7.5, color=C_RED_E)
    # restart from HOME (routed underneath as an elbow line)
    for i, yy in ((2, 1.45), (3, 1.05)):
        ax.plot([xs[i] + 0.95, xs[i] + 0.95], [2.0, yy], color=C_RED_E, lw=1.2)
        ax.plot([xs[i] + 0.95, xs[0] + 0.95 - (0.2 if i == 3 else 0)], [yy, yy], color=C_RED_E, lw=1.2)
        x0 = xs[0] + 0.95 - (0.2 if i == 3 else 0)
        arrow(ax, (x0, yy), (x0, 2.0), None, color=C_RED_E)
        ax.text(xs[i] + 1.0, yy + 0.08, "fail", fontsize=7.5, color=C_RED_E, ha="left")
    ax.text(4.0, 0.65, "CHEST1 / EYE1 failure → restart the whole pipeline from HOME1", ha="center",
            fontsize=8, color=C_RED_E)
    ax.text(9.75, 1.55, "writes report.pdf to\n/opt/meditation-app/data", ha="center", fontsize=7.5, color=C_HW_E)
    ax.text(5.5, 4.25, "fullscreen-fixer.sh runs alongside (X11 only) and is stopped by an EXIT trap",
            ha="center", fontsize=8, color=MUTED)
    save(fig, "fig_pipeline.png")


# ---------------------------------------------------------------- deployment
def deployment():
    fig, ax = canvas(11, 4.6)
    box(ax, 0.2, 2.6, 2.6, 1.4, "Source (GitHub)\nC# · Node · bash\nfeature branch → PR", C_EXT, C_EXT_E)
    box(ax, 3.4, 3.1, 3.0, 1.2, "deploy/build-deb.sh\ndotnet publish, self-contained,\nsingle file · amd64 / arm64", C_US, C_US_E)
    box(ax, 3.4, 0.9, 3.0, 1.2, "Render blueprint\nrender.yaml → Node web service\n+ PostgreSQL (auto-deploy main)", C_US, C_US_E)
    box(ax, 7.1, 3.0, 3.7, 1.45, "Kiosk (Ubuntu)\n/opt/diya-meditation/DiyaMeditation\nsystemd user service (Restart=always)\nautostart .desktop + auto-login", C_US, C_US_E)
    box(ax, 7.1, 0.8, 3.7, 1.4, "Hosted service (Render)\ndiya-registration.onrender.com\n/admin · /p/<token> · /api/*\nHTTPS (needed for phone camera)", C_EXT, C_EXT_E)
    arrow(ax, (2.8, 3.5), (3.4, 3.7), None)
    arrow(ax, (2.8, 3.0), (3.4, 1.5), None)
    arrow(ax, (6.4, 3.7), (7.1, 3.7), "dpkg -i\n.deb", size=7.5, loff=(0, 0.3))
    arrow(ax, (6.4, 1.5), (7.1, 1.5), "git push\n→ build", size=7.5, loff=(0, 0.3))
    arrow(ax, (8.95, 3.0), (8.95, 2.2), "DIYA_API_BASE", both=True, size=7.5, loff=(0.75, 0))
    save(fig, "fig_deployment.png")


# ---------------------------------------------------------------- evolution timeline
def evolution():
    fig, ax = plt.subplots(figsize=(9.2, 3.6))
    ax.axis("off")
    events = [
        (date(2026, 6, 11), "v1.0", "Fullscreen kiosk\nshell + .deb"),
        (date(2026, 6, 17), "v1.1", "Offline QR pass\n(data inside QR)"),
        (date(2026, 6, 19), "v1.2", "Online lookup:\nQR holds an ID"),
        (date(2026, 6, 26), "v1.3/1.4", "Reverse QR:\nkiosk shows QR,\nphone registers"),
        (date(2026, 7, 3), "PR #12", "Admin roster +\nper-person\nlogin link"),
        (date(2026, 7, 11), "v1.5", "Auto pipeline +\nin-app PDF\nreport"),
        (date(2026, 7, 31), "v1.6", "Report-ready flow,\nlive status,\nthank-you"),
    ]
    xs = [mdates.date2num(d) for d, _, _ in events]
    ax.plot([xs[0] - 2, xs[-1] + 2], [0, 0], color=INK, lw=2)
    for i, ((d, v, t), x) in enumerate(zip(events, xs)):
        up = 1 if i % 2 == 0 else -1
        ax.plot([x, x], [0, 0.5 * up], color=C_US_E, lw=1)
        ax.scatter([x], [0], s=60, color=C_US_E, zorder=3)
        ax.text(x, 0.58 * up, f"{v} · {d.strftime('%d %b')}", ha="center", va="bottom" if up > 0 else "top",
                fontsize=9.5, fontweight="bold", color=C_US_E)
        ax.text(x, 0.82 * up if up > 0 else -0.82, t, ha="center", va="bottom" if up > 0 else "top",
                fontsize=9, color=INK)
    ax.set_ylim(-2.0, 2.0)
    ax.set_xlim(xs[0] - 3, xs[-1] + 3)
    save(fig, "fig_evolution.png")


# ---------------------------------------------------------------- gantt
def gantt():
    tasks = [
        ("Orientation, requirement study, tech selection", date(2026, 6, 1), date(2026, 6, 10)),
        ("Kiosk shell, Wayland fullscreen, .deb packaging", date(2026, 6, 8), date(2026, 6, 15)),
        ("QR visitor pass + online registration API", date(2026, 6, 15), date(2026, 6, 20)),
        ("Reverse-QR (phone) flow, calibration hook", date(2026, 6, 20), date(2026, 6, 27)),
        ("Alternative designs (offline Excel, full flow)", date(2026, 6, 26), date(2026, 7, 1)),
        ("Admin roster upload, phone login, visitor photo", date(2026, 7, 1), date(2026, 7, 10)),
        ("Pipeline integration + in-app PDF report", date(2026, 7, 8), date(2026, 7, 15)),
        ("Window management experiments, test kit", date(2026, 7, 15), date(2026, 7, 26)),
        ("Stabilise v1.6.0, documentation, handoff", date(2026, 7, 24), date(2026, 7, 31)),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 4.8))
    for i, (name, s, e) in enumerate(tasks):
        y = len(tasks) - i
        ax.barh(y, (e - s).days + 1, left=mdates.date2num(s), height=0.55, color=C_US, edgecolor=C_US_E)
        ax.text(mdates.date2num(s) - 0.6, y, name, ha="right", va="center", fontsize=9.5, color=INK)
    ax.set_yticks([])
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b"))
    ax.set_xlim(mdates.date2num(date(2026, 6, 1)) - 0.5, mdates.date2num(date(2026, 8, 1)))
    ax.grid(axis="x", color="#E5E7EB")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="x", labelsize=8)
    plt.subplots_adjust(left=0.42)
    save(fig, "fig_gantt.png")


if __name__ == "__main__":
    architecture()
    visitor_flow()
    er_diagram()
    hardware()
    pipeline()
    deployment()
    evolution()
    gantt()
