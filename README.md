# 🌉 OpenBridge

**Your invisible stream crew. 100% free. No API keys. No setup hell.**

OpenBridge is an open-source AI agent that runs alongside your stream and handles everything — chat moderation, auto-clipping, cross-posting, analytics — so you can focus on playing.

It works on **any platform** without needing API access, because it controls a real browser exactly like a human would.

---

## 🚀 Get Started in 30 Seconds

### Windows
```powershell
git clone https://github.com/yourname/openbridge
cd openbridge
install.bat      # One-click installer
start.bat        # Launch OpenBridge
```

### macOS & Linux
```bash
git clone https://github.com/yourname/openbridge
cd openbridge
bash install.sh  # One-click installer
./start.sh       # Launch OpenBridge
```

**That's it!** The installer handles everything automatically.

**See [QUICKSTART.md](QUICKSTART.md) for the full quick start guide.**

---

## What it does

| Agent | What it handles |
|-------|----------------|
| **Chat Commander** | Monitors chat, responds to `!commands`, welcomes raiders, detects hype |
| **Clip Sniper** | Auto-clips when chat goes crazy. No manual clipping ever again |
| **Shield Guard** | Moderation that understands gaming culture — won't nuke "gg ez" |
| **Growth Intel** | Tracks your stream silently, posts a full report when you go offline |
| **Social Ghost** | Posts clips and announcements to Twitter and Discord automatically |
| **Revenue Pilot** | Fires sub drives and merch drops at viewer milestones |

---

## Setup (2 minutes)

### Option 1: One-Click Installer (Recommended for all users)

**Windows:**
```bash
install.bat
```

**macOS & Linux:**
```bash
bash install.sh
```

The installer will automatically:
- ✅ Check/install Python 3.10+
- ✅ Create a virtual environment
- ✅ Install all dependencies
- ✅ Install Chromium browser
- ✅ Create required directories
- ✅ Setup configuration file
- ✅ Optionally run the setup wizard

### Option 2: Interactive Wizard (If already installed)

```bash
python wizard.py
```

The wizard will:
- Check your system requirements
- Ask you questions about your channel
- Create a personalized config.yaml
- Install all dependencies
- Optionally start OpenBridge immediately

### Option 3: Quick Start Menu

**Windows:** `start.bat`  
**macOS & Linux:** `./start.sh`

This shows an interactive menu to:
- Start/stop OpenBridge
- View status and logs
- Reconfigure settings
- Run the wizard

### Option 4: Manual Setup (Advanced users)

```bash
# 1. Clone
git clone https://github.com/yourname/openbridge
cd openbridge

# 2. Setup (installs everything)
bash setup.sh        # macOS/Linux
install.bat          # Windows

# 3. Configure
cp config.example.yaml config.yaml
# Open config.yaml and set your channel name

# 4. Run
python main.py
```

That's it. A browser window will open, navigate to your channel, and your crew starts working.

---

## Requirements

- Python 3.10+
- A Twitch account (logged in once, then session is saved)
- That's it!

**No API keys. No OAuth tokens. No credit card.**

📖 **New to Python?** See [EASY_INSTALL.md](EASY_INSTALL.md) for one-click installers on Windows, Mac, and Linux!  
📖 **Detailed guide:** See [INSTALL.md](INSTALL.md) for step-by-step installation instructions.

---

## How it works

Most stream bots need API keys, OAuth tokens, and platform approval.

OpenBridge doesn't. It opens a real browser, logs in once (you do this manually the first time), and then controls it like a human — reading chat from the DOM, clicking the clip button, typing into message inputs.

**Platforms that work right now:**
- ✅ Twitch
- ✅ Kick (no API exists — we're the only solution)
- ✅ YouTube Live
- ✅ TikTok
- ✅ Twitter / X
- ✅ Discord

---

## Configuration

Open `config.yaml`. The important ones:

```yaml
channel:  your_twitch_channel   # your Twitch channel, lowercase
streamer: YourName              # your display name
headless: false                 # false = see the browser; true = invisible

agents:
  chat:
    hype_threshold: 15          # chat messages in 10s that trigger a clip
    custom_commands:
      specs:    "RTX 4090, i9, 64GB RAM"
      schedule: "Mon/Wed/Fri 7PM EST"
```

---

## First run — logging in

On first run, the browser will open and you'll need to log into Twitch manually. After that, OpenBridge saves your session and you never need to do it again.

**Quick Start Checklist:**
- [ ] Run `python wizard.py` (or `./start.sh` and choose option 5)
- [ ] Edit config.yaml with your channel name (wizard does this automatically)
- [ ] Run `python main.py` (or `./start.sh` and choose option 1)
- [ ] Log into Twitch when the browser opens
- [ ] Navigate to your channel page
- [ ] Go live and let OpenBridge handle the rest!

**Pro Tips:**
- Use `./dashboard.py` for an interactive control panel
- Check `./start.sh` for a simple menu interface
- Your session is saved in the `sessions/` folder
- Logs are written to `logs/openbridge.log`

---

## Works with AI models too

OpenBridge exposes an MCP server so Claude and other AI models can use it as an action layer:

```bash
python integrations/mcp_server.py
```

Then add it as an MCP tool in your AI model of choice.

---

## Contributing

PRs welcome. The most useful contributions right now:

- Better DOM selectors for each platform (they change often)
- New `!command` types
- Platform connectors (Instagram, Facebook Gaming, etc.)
- Bug fixes
- UX improvements for the wizard and dashboard

---

## Command Reference

### Installation Commands

**First Time Setup:**

| Platform | Command | Description |
|----------|---------|-------------|
| **Windows** | `install.bat` | One-click installer (recommended) |
| **macOS/Linux** | `bash install.sh` | One-click installer (recommended) |

**Quick Start:**

| Platform | Command | Description |
|----------|---------|-------------|
| **Windows** | `start.bat` | Interactive menu |
| **macOS/Linux** | `./start.sh` | Interactive menu |

**Other Commands:**

```bash
python wizard.py    # Setup wizard (interactive configuration)
python dashboard.py # Status & control panel
python main.py      # Start OpenBridge directly
bash setup.sh       # Legacy setup script (macOS/Linux)
```

### Chat Commands (for your viewers)

Once running, your viewers can use these in chat:

- `!specs` - Your PC specs (customizable)
- `!schedule` - Stream schedule (customizable)
- `!lurk` - Lurk message
- `!socials` - Social media links
- `!discord` - Discord invite
- `!uptime` - Stream uptime

Add more custom commands in `config.yaml`!

---

## License

MIT. Free forever for personal use.

---

*Built by streamers, for streamers.*
*Zero API keys. Zero monthly fees. Just your crew.*
