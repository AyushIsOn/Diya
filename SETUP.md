# Diya Meditation — Setup & Commands

All the commands for installing, running, and auto-starting the kiosk on Ubuntu.
**Latest version: 1.5.0**

> Pick the package matching your machine's architecture
> (check with `dpkg --print-architecture`):
> - `amd64` -> normal x86 PCs
> - `arm64` -> Apple Silicon VMs / ARM devices

---

## Offline people-list mode (this build)

> This is the **offline** variant. No internet, no Render, no webpage. The kiosk
> loads a **fixed list of people** from a local **CSV or Excel (.xlsx)** file, and
> a person is identified by **scanning their pass** (USB QR scanner) or **typing
> their name**. Their details come straight from the file.

**How it works, end to end:**

1. **You prepare a list** — a CSV or `.xlsx` with a header row. Columns (any order,
   case-insensitive): `Id, Name, Email, Age`. `Id` is the value encoded in the QR.
   ```csv
   Id,Name,Email,Age
   P001,Asha Rao,asha@example.com,29
   P002,Maya Iyer,maya@example.com,31
   ```
2. **Generate the passes** (one QR per person) with the included tool:
   ```bash
   cd tools/PassGenerator
   dotnet run -- /path/to/people.csv ./passes
   # writes passes/<Id>_<Name>.png + passes/index.html (open it to print them all)
   ```
   Print the passes (or show them on a phone screen).
3. **Tell the kiosk which file to use.** Put your file where the app looks, or point
   to it explicitly (highest priority):
   ```bash
   DIYA_PEOPLE_FILE=/home/USER/people.csv diya-meditation
   ```
   Without the env var it searches: the current dir, then `/opt/diya-meditation/people.csv`
   (a sample ships there), then `~/diya-people.csv`.
4. **At the kiosk**, the person scans their pass with a **USB QR scanner** (it types
   the code + Enter into the focused box) — or types their name and presses Enter.
   Their details load instantly from the file.

**Testing on a VirtualBox / Ubuntu VM (no scanner handy):**
- A USB QR scanner acts as a keyboard — you can simulate it by just **typing the Id**
  (e.g. `P001`) into the scan box and pressing Enter.
- Drop your `people.csv` into the VM (shared folder / drag-drop) and launch with
  `DIYA_PEOPLE_FILE=/path/to/people.csv diya-meditation`.
- The bottom of the right panel shows **"Loaded N people from <file>"** so you can
  confirm the list was read.

---

## Which should I use? (.deb vs Docker)

- **`.deb` install (Section 1)** — the **real kiosk deployment**. Use this on the
  actual museum/Ubuntu machine. Gives true fullscreen, auto-start on boot,
  auto-restart on crash, and GNOME lockdown.
- **Docker (Section 11)** — **UI preview only**, viewed in a browser via noVNC.
  Handy for a quick look without installing anything system-wide. NOT a real
  kiosk: no boot autostart, no lockdown, no crash-restart.

**On a real Ubuntu machine, use the `.deb`.**

> **Online registration (v1.5.0+):** the kiosk shows a **QR code on screen**. The
> visitor scans it with their **phone**, fills in the registration form on their
> phone, and the kiosk **advances automatically** once they submit. No QR scanner
> or camera is needed at the kiosk — but the kiosk **must have internet** and know
> the API URL (see Sections 4 and 5). A name-entry fallback is also on screen.

---

## 1. Install on Ubuntu

### a) Download from GitHub and install
```bash
cd ~
rm -f diya-meditation_1.5.0_amd64.deb
wget https://github.com/AyushIsOn/Diya/raw/main/package/diya-meditation_1.5.0_amd64.deb
sudo dpkg -i ./diya-meditation_1.5.0_amd64.deb
```

If it ever complains about a missing dependency:
```bash
sudo apt -f install
```

### b) Already have the .deb file? (offline / no GitHub)
If the `.deb` is already on the machine (USB stick, shared folder, scp, etc.),
skip the download and install the local file directly — the package itself is
self-contained (bundles the .NET runtime):

```bash
sudo dpkg -i ./diya-meditation_1.5.0_amd64.deb
sudo apt -f install     # only if it reports a missing dependency
```

Ways to get the file onto the machine without GitHub:
- **USB drive** — copy the `.deb` over and plug it in
- **VM shared folder** — drop it in the shared folder from the host
- **scp** — `scp diya-meditation_1.5.0_amd64.deb user@machine:~/`

## 2. Run it

```bash
diya-meditation
```

...or launch **"Diya Meditation"** from the app menu (press Super, search for it).
It opens **fullscreen**.

## 3. Exit the kiosk

Secret shortcut: **`Ctrl + Shift + Alt + Q`**

---

## 4. Point the kiosk at the registration API (`DIYA_API_BASE`)

When a visitor scans their QR pass, the kiosk reads the short id and fetches their
details from the registration API. Tell the kiosk where that API lives with the
`DIYA_API_BASE` environment variable.

- Default (baked into the build): `https://diya-registration.onrender.com`
- Change it to **your** deployed URL (from Section 5) in whichever way matches how
  you start the app:

**If you auto-start via the systemd service** (`/usr/lib/systemd/user/diya-meditation.service`),
it already contains a line you can edit:
```ini
Environment=DIYA_API_BASE=https://YOUR-SERVICE.onrender.com
```
Then:
```bash
systemctl --user daemon-reload
systemctl --user restart diya-meditation
```

**If you launch it from the autostart `.desktop`** (Section 6), the `Exec` line
exports it (see that section).

**If you run it by hand:**
```bash
DIYA_API_BASE=https://YOUR-SERVICE.onrender.com diya-meditation
```

> Quick check the kiosk can reach the API:
> ```bash
> curl https://YOUR-SERVICE.onrender.com/api/health   # expect {"ok":true}
> ```

---

## 5. Deploy the registration website + API (Render, free)

The `server/` folder is a small Node/Express API that also serves the
registration website (`registration/index.html`). It stores visitors in Postgres.

### a) Pick a database
- **Render Postgres** (one click via `render.yaml`) — easiest, but the **free**
  Render database is **deleted after 30 days**.
- **Neon / Supabase** free Postgres — persistent; recommended for anything lasting.

### b) Deploy on Render
1. Push this repo to GitHub.
2. Render Dashboard -> **New -> Blueprint** -> select this repo.
   Render reads `render.yaml` and creates the web service (root dir `server/`).
   - Using Render Postgres: the blueprint also creates the DB and wires
     `DATABASE_URL` automatically.
   - Using Neon/Supabase: in the service's **Environment**, set `DATABASE_URL`
     to your connection string (and you can delete the `databases:` block).
3. After it deploys, note the URL, e.g. `https://diya-registration.onrender.com`.
   - Registration website: open that URL in a browser.
   - Health check: `GET /api/health` -> `{"ok":true}`.
4. Put that URL into the kiosk via `DIYA_API_BASE` (Section 4).

> Free Render web services sleep after ~15 min idle; the first request then
> cold-starts in ~30–50s. The kiosk's lookup timeout accounts for this.

### c) Run the server locally (optional, for testing)
```bash
cd server
cp .env.example .env        # then edit DATABASE_URL (use PGSSL=disable for local PG)
npm install
npm start                   # serves site + API on http://localhost:3000
```

---

## 6. Auto-start on boot

### a) Create the autostart entry (with a startup delay + API URL + log)
The `sleep 4` waits for the Wayland desktop session to be ready (otherwise the app
can launch too early and fail silently). `DIYA_API_BASE` points it at your API.
The log helps diagnose any failure.

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/diya-meditation.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Diya Meditation
Exec=sh -c 'sleep 4; DIYA_API_BASE=https://YOUR-SERVICE.onrender.com /opt/diya-meditation/DiyaMeditation > /tmp/diya.log 2>&1'
X-GNOME-Autostart-enabled=true
Terminal=false
EOF
```

### b) Enable automatic login (so it boots straight in, no password prompt)
Easiest: **Settings -> System -> Users -> Automatic Login -> ON**

Or via terminal:
```bash
sudo tee /etc/gdm3/custom.conf > /dev/null <<EOF
[daemon]
AutomaticLoginEnable=true
AutomaticLogin=$USER
EOF
```

### c) Reboot to test
```bash
reboot
```

---

## 7. Troubleshooting auto-start

If the app does not appear after reboot, run this and read the output:

```bash
echo "--- did it start? ---"; pgrep -fa DiyaMeditation || echo "NOT running"
echo "--- startup log ---"; cat /tmp/diya.log 2>/dev/null || echo "no log file"
echo "--- autostart entry ---"; cat ~/.config/autostart/diya-meditation.desktop
echo "--- autologin config ---"; grep -iA3 daemon /etc/gdm3/custom.conf 2>/dev/null
echo "--- binary present? ---"; ls -l /opt/diya-meditation/DiyaMeditation
```

What it tells you:
- **NOT running + a log error** -> the app crashed on launch; the log shows why.
- **NOT running + no log** -> the autostart entry never fired (check auto-login actually boots to the desktop without a password prompt).
- **binary missing** -> the v1.5.0 install did not complete; reinstall with `sudo dpkg -i ./diya-meditation_1.5.0_amd64.deb`.
- **scans say "Couldn't reach the server"** -> the kiosk has no internet or
  `DIYA_API_BASE` is wrong (Section 4); test with the `curl .../api/health` check.

---

## 8. General checks

```bash
# What's my session type? (wayland or x11)
echo $XDG_SESSION_TYPE

# What's my CPU architecture? (amd64 or arm64)
dpkg --print-architecture

# Run from terminal to see startup logs (look for "[Diya] ..." lines)
diya-meditation
```

## 9. Uninstall

```bash
sudo apt remove diya-meditation
rm -f ~/.config/autostart/diya-meditation.desktop
```

---

## 10. Build the .deb from source (optional)

### a) Install the .NET 8 SDK on Ubuntu (one time)
```bash
sudo apt update
sudo apt install -y dotnet-sdk-8.0
dotnet --version        # should print 8.0.x
```

> If `dotnet-sdk-8.0` is not found in the default repos on your Ubuntu version,
> add Microsoft's feed first:
> ```bash
> sudo apt install -y wget
> wget https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O /tmp/ms.deb
> sudo dpkg -i /tmp/ms.deb
> sudo apt update
> sudo apt install -y dotnet-sdk-8.0
> ```

### b) Build the package
```bash
cd DiyaMeditation
./deploy/build-deb.sh 1.5.0 amd64     # x86 PCs
./deploy/build-deb.sh 1.5.0 arm64     # ARM devices / Apple Silicon VMs
# output: build/diya-meditation_1.5.0_<arch>.deb
```

> Note: `build-deb.sh` wipes the `build/` directory at the start of every run,
> so if you build both architectures, copy the first `.deb` out before building
> the second (otherwise the first one gets deleted).

### c) Run directly from source (no packaging)
```bash
cd DiyaMeditation
dotnet run            # builds + launches fullscreen
```

---

## 11. Run with Docker (browser preview — dev only)

This runs the app on a virtual display (Xvfb) exposed through noVNC, so you can
view it in a web browser. This is for **previewing the UI only** — it is NOT the
real kiosk deployment (use the `.deb` for that).

### a) Install Docker Engine on Ubuntu (one time)
```bash
# Quick install via Docker's convenience script
curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
sudo sh /tmp/get-docker.sh

# Allow running docker without sudo (log out / back in after this)
sudo usermod -aG docker "$USER"
newgrp docker            # apply the group in the current shell

docker --version         # verify
```

### b) Build the image
```bash
cd DiyaMeditation
docker build -t diya-preview -f docker/Dockerfile .
```

### c) Run the container
```bash
docker run --rm -p 8080:8080 diya-preview
```

### d) View it
Open in a browser on the same machine:

```
http://localhost:8080/vnc.html
```

Click **Connect**. Exit the app inside the view with **`Ctrl + Shift + Alt + Q`**.

To stop the container: press `Ctrl + C` in the terminal running it (the `--rm`
flag removes it automatically on exit).
