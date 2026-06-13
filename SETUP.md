# Diya Meditation — Setup & Commands

All the commands for installing, running, and auto-starting the kiosk on Ubuntu.
**Latest version: 1.0.2**

> Pick the package matching your machine's architecture
> (check with `dpkg --print-architecture`):
> - `amd64` -> normal x86 PCs
> - `arm64` -> Apple Silicon VMs / ARM devices

---

## 1. Install on Ubuntu

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

### a) Create the autostart entry
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/diya-meditation.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Diya Meditation
Exec=/opt/diya-meditation/DiyaMeditation
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

## 5. Verify / troubleshoot

```bash
# Is the app installed where expected?
ls -l /opt/diya-meditation/DiyaMeditation

# What's my session type? (wayland or x11)
echo $XDG_SESSION_TYPE

# What's my CPU architecture? (amd64 or arm64)
dpkg --print-architecture

# Run from terminal to see startup logs (look for "[Diya] ..." lines)
diya-meditation
```

## 6. Uninstall

```bash
sudo apt remove diya-meditation
# remove autostart entry too
rm -f ~/.config/autostart/diya-meditation.desktop
```

---

## 7. Build the .deb from source (optional)

Requires the .NET 8 SDK.

```bash
cd DiyaMeditation
./deploy/build-deb.sh 1.0.2 amd64     # x86 PCs
./deploy/build-deb.sh 1.0.2 arm64     # ARM devices / Apple Silicon VMs
# output: build/diya-meditation_1.0.2_<arch>.deb
```
