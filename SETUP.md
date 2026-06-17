# Diya Meditation — Setup & Commands

All the commands for installing, running, and auto-starting the kiosk on Ubuntu.
**Latest version: 1.1.0**

> Pick the package matching your machine's architecture
> (check with `dpkg --print-architecture`):
> - `amd64` -> normal x86 PCs
> - `arm64` -> Apple Silicon VMs / ARM devices

---

## 1. Install on Ubuntu

### a) Download from GitHub and install
```bash
cd ~
rm -f diya-meditation_1.1.0_amd64.deb
wget https://github.com/AyushIsOn/Diya/raw/main/package/diya-meditation_1.1.0_amd64.deb
sudo dpkg -i ./diya-meditation_1.1.0_amd64.deb
```

If it ever complains about a missing dependency:
```bash
sudo apt -f install
```

### b) Already have the .deb file? (offline / no GitHub)
If the `.deb` is already on the machine (USB stick, shared folder, scp, etc.),
skip the download and install the local file directly. No internet needed —
the package is self-contained:

```bash
sudo dpkg -i ./diya-meditation_1.1.0_amd64.deb
sudo apt -f install     # only if it reports a missing dependency
```

Ways to get the file onto the machine without GitHub:
- **USB drive** — copy the `.deb` over and plug it in
- **VM shared folder** — drop it in the shared folder from the host
- **scp** — `scp diya-meditation_1.1.0_amd64.deb user@machine:~/`

## 2. Run it

```bash
diya-meditation
```

...or launch **"Diya Meditation"** from the app menu (press Super, search for it).
It opens **fullscreen**.

## 3. Exit the kiosk

Secret shortcut: **`Ctrl + Shift + Alt + Q`**

---

## 4. Auto-start on boot

### a) Create the autostart entry (with a startup delay + log)
The `sleep 4` waits for the Wayland desktop session to be ready (otherwise the app
can launch too early and fail silently). The log helps diagnose any failure.

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/diya-meditation.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Diya Meditation
Exec=sh -c 'sleep 4; /opt/diya-meditation/DiyaMeditation > /tmp/diya.log 2>&1'
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

## 5. Troubleshooting auto-start

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
- **binary missing** -> the v1.1.0 install did not complete; reinstall with `sudo dpkg -i ./diya-meditation_1.1.0_amd64.deb`.

---

## 6. General checks

```bash
# What's my session type? (wayland or x11)
echo $XDG_SESSION_TYPE

# What's my CPU architecture? (amd64 or arm64)
dpkg --print-architecture

# Run from terminal to see startup logs (look for "[Diya] ..." lines)
diya-meditation
```

## 7. Uninstall

```bash
sudo apt remove diya-meditation
rm -f ~/.config/autostart/diya-meditation.desktop
```

---

## 8. Build the .deb from source (optional)

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
./deploy/build-deb.sh 1.1.0 amd64     # x86 PCs
./deploy/build-deb.sh 1.1.0 arm64     # ARM devices / Apple Silicon VMs
# output: build/diya-meditation_1.1.0_<arch>.deb
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

## 9. Run with Docker (browser preview — dev only)

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
