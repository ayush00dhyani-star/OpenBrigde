# 🔧 Installation Guide

## System Requirements

### Minimum
- Python 3.10 or higher
- 2GB RAM free
- Modern CPU (Intel i3 / AMD Ryzen 3 or better)
- Internet connection

### Recommended
- Python 3.11+
- 4GB RAM free
- Intel i5 / AMD Ryzen 5 or better
- SSD storage

---

## Step-by-Step Installation

### 1. Install Python

**Windows:**
1. Download from https://python.org/downloads
2. Run installer
3. ✅ Check "Add Python to PATH"
4. Click "Install Now"

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora/RHEL
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

### 2. Verify Installation

```bash
python --version  # Should show 3.10+
pip --version     # Should work
```

### 3. Clone OpenBridge

```bash
git clone https://github.com/yourname/openbridge
cd openbridge
```

Or [download as ZIP](link) and extract it.

### 4. Run the Wizard

```bash
python wizard.py
```

The wizard will:
- ✅ Check your Python version
- ✅ Create your configuration
- ✅ Install dependencies automatically
- ✅ Optionally start OpenBridge

That's it! 🎉

---

## Manual Installation

If you prefer manual control:

### Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### Create Configuration

```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your channel name
```

### Start OpenBridge

```bash
python main.py
```

---

## Troubleshooting

### "Python not found"

Make sure Python is installed and added to your PATH:
- Windows: Re-run installer, check "Add to PATH"
- Mac/Linux: Try `python3` instead of `python`

### "Permission denied" on Linux/Mac

```bash
chmod +x start.sh wizard.py setup.sh
```

### "Module not found" errors

```bash
pip install -r requirements.txt --upgrade
```

### Browser won't start

```bash
playwright install chromium
playwright install-deps chromium  # Linux only
```

### Can't log into Twitch

- Make sure you're using a real browser window (headless: false)
- Complete any CAPTCHAs that appear
- Your session is saved after first login

### High CPU usage

- Set `headless: true` in config.yaml if running on a server
- Disable agents you don't need
- Increase poll intervals in advanced settings

---

## Next Steps

After installation:

1. **Run the wizard**: `python wizard.py`
2. **Start OpenBridge**: `./start.sh` → Option 1
3. **Log into Twitch** when browser opens
4. **Go live** and watch the magic happen!

Need more help? Check:
- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [README.md](README.md) - Full documentation
- Logs in `logs/` folder
