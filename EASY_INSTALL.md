# 🚀 Easy Installation Guide

**OpenBridge works on ANY device** - Windows, Mac, Linux, even Raspberry Pi!

---

## ⚡ One-Click Installation

Choose your operating system:

### Windows Users
```powershell
# 1. Download and extract OpenBridge (or clone with git)
# 2. Double-click install.bat
# That's it!
```

**Or use Command Prompt:**
```cmd
git clone https://github.com/yourname/openbridge
cd openbridge
install.bat
```

### Mac Users
```bash
git clone https://github.com/yourname/openbridge
cd openbridge
bash install.sh
```

### Linux Users
```bash
git clone https://github.com/yourname/openbridge
cd openbridge
bash install.sh
```

---

## 🎯 What the Installer Does

The `install.bat` (Windows) or `install.sh` (Mac/Linux) script automatically:

1. ✅ **Checks Python** - Installs Python 3.10+ if missing
2. ✅ **Creates Virtual Environment** - Keeps dependencies isolated
3. ✅ **Installs Packages** - All required Python libraries
4. ✅ **Downloads Browser** - Chromium for browser automation
5. ✅ **Creates Folders** - logs/, sessions/, data/
6. ✅ **Sets Up Config** - Copies example configuration
7. ✅ **Offers Wizard** - Optional interactive setup

**Total time: 2-5 minutes** (depending on internet speed)

---

## 🖥️ Platform-Specific Notes

### Windows

**Requirements:**
- Windows 10/11
- PowerShell or Command Prompt
- Administrator rights (for Python installation)

**Troubleshooting:**
- If you see "Python not found", the installer will offer to download it
- Make sure to check "Add Python to PATH" during Python installation
- Run as Administrator if you encounter permission errors

### macOS

**Requirements:**
- macOS 10.15 (Catalina) or later
- Terminal app
- Homebrew (recommended, installer will help)

**Troubleshooting:**
- If Homebrew isn't installed, the installer will guide you
- You may need to approve Terminal in System Preferences → Security
- On Apple Silicon (M1/M2), Rosetta 2 may be required

### Linux

**Requirements:**
- Ubuntu 20.04+, Fedora 33+, Debian 11+, or similar
- Terminal
- sudo privileges

**Distribution-specific commands:**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
bash install.sh
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-pip
bash install.sh
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
bash install.sh
```

---

## 🚀 After Installation

### Start OpenBridge

**Windows:** Double-click `start.bat` or run:
```cmd
start.bat
```

**Mac/Linux:** Run:
```bash
./start.sh
```

### First Run Checklist

1. ✅ Run the installer (`install.bat` or `bash install.sh`)
2. ✅ Launch OpenBridge (`start.bat` or `./start.sh`)
3. ✅ Log into Twitch when the browser opens
4. ✅ Navigate to your channel page
5. ✅ Go live and enjoy!

---

## ❓ Common Issues

### "Python not found"
**Solution:** The installer will offer to download Python. Accept and rerun.

### "Permission denied" (Mac/Linux)
**Solution:** 
```bash
chmod +x install.sh start.sh
bash install.sh
```

### "Module not found" errors
**Solution:** 
```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Then reinstall
pip install -r requirements.txt
```

### Browser won't start
**Solution:**
```bash
playwright install chromium
# Linux only:
playwright install-deps chromium
```

### High CPU usage
**Solution:** Set `headless: true` in config.yaml if running on a server

---

## 📱 Mobile & Remote Access

While OpenBridge runs on a computer, you can:

- **Monitor remotely** via logs synced to cloud storage
- **Configure** by editing config.yaml from any device
- **Control** via SSH if running on a remote server

**Recommended setup for 24/7 operation:**
- Raspberry Pi 4 (4GB+) with headless mode
- Old laptop/PC running in background
- Cloud VPS (DigitalOcean, Linode, AWS)

---

## 🎓 Next Steps

After installation:

1. **Read [QUICKSTART.md](QUICKSTART.md)** - Get up and running fast
2. **Check [README.md](README.md)** - Full documentation
3. **Join the community** - Get help and share tips
4. **Customize config.yaml** - Make OpenBridge yours

---

## 💡 Pro Tips

- **Virtual Environment:** The installer creates one automatically. Use it!
- **Session Persistence:** Your login is saved. Only log in once.
- **Headless Mode:** Set `headless: true` for server deployments
- **Auto-start:** Add OpenBridge to startup for 24/7 operation
- **Logs:** Check `logs/` folder for troubleshooting

---

## 🆘 Need Help?

1. Check the logs in `logs/openbridge.log`
2. Review [INSTALL.md](INSTALL.md) for detailed setup instructions
3. Read [QUICKSTART.md](QUICKSTART.md) for quick tips
4. Open an issue on GitHub with your error logs

**You're all set! Happy streaming! 🎮🎬**
