# Diya Meditation — Setup & Commands

All the commands for installing, running, and auto-starting the kiosk on Ubuntu.
**Latest version: 1.0.2**

> Pick the package matching your machine's architecture
> (check with `dpkg --print-architecture`):
> - `amd64` -> normal x86 PCs
> - `arm64` -> Apple Silicon VMs / ARM devices

---

## 1. Install on Ubuntu

### a) Download from GitHub and install
```bash
cd ~
rm -f diya-meditation_1.0.2_amd64.deb
wget https://github.com/AyushIsOn/Diya/raw/main/package/diya-meditation_1.0.2_amd64.deb
sudo dpkg -i ./diya-meditation_1.0.2_amd64.deb
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
sudo dpkg -i ./diya-meditation_1.0.2_amd64.deb
sudo apt -f install     # only if it reports a missing dependency
```

Ways to get the file onto the machine without GitHub:
- **USB drive** — copy the `.deb` over and plug it in
- **VM shared folder** — drop it in the shared folder from the host
- **scp** — `scp diya-meditation_1.0.2_amd64.deb user@machine:~/`

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
- **binary missing** -> the v1.0.2 install did not complete; reinstall with `sudo dpkg -i ./diya-meditation_1.0.2_amd64.deb`.

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

Requires the .NET 8 SDK.

```bash
cd DiyaMeditation
./deploy/build-deb.sh 1.0.2 amd64     # x86 PCs
./deploy/build-deb.sh 1.0.2 arm64     # ARM devices / Apple Silicon VMs
# output: build/diya-meditation_1.0.2_<arch>.deb
```

<!-- push test -->
