# 🚀 Quick Start Guide

**The fastest way to get OpenBridge running!**

## One-Command Start (Recommended)

```bash
./start.sh
```

That's it! This script will:
1. Check if you have Python installed
2. If no config exists → run the setup wizard automatically
3. If config exists → let you choose to start, reconfigure, or view settings

## What Happens Next?

### First Time Users
The wizard will ask you:
- Your Twitch channel name
- Your display name  
- Which features to enable (chat bot, auto-clipping, moderation, etc.)
- Whether to install dependencies now

Then you can optionally start OpenBridge immediately!

### Returning Users
Just run `./start.sh` and choose option 1 to launch OpenBridge.

---

## Manual Alternative

If you prefer manual control:

```bash
# Setup (one time only)
python wizard.py

# Start OpenBridge
python main.py
```

---

## First Run Experience

1. **Browser Opens** - A Chromium browser window will appear
2. **Log In** - Sign into your Twitch account (only needed once)
3. **Navigate** - Go to your channel page when prompted
4. **Session Saved** - Your login is saved for future runs
5. **Go Live** - Start streaming and OpenBridge takes over!

---

## Common Questions

**Q: Do I need API keys?**  
A: No! OpenBridge works like a human user controlling a browser.

**Q: Is this safe?**  
A: Yes! Your session is stored locally in the `sessions/` folder. Nothing is sent to external servers.

**Q: Can I use this on Kick/YouTube?**  
A: Yes! Enable other platforms in your config.yaml after setup.

**Q: How do I stop it?**  
A: Press `Ctrl+C` in the terminal.

**Q: Where are the logs?**  
A: Check the `logs/` folder for detailed activity logs.

---

## Need Help?

- Run `python wizard.py` anytime to reconfigure
- Edit `config.yaml` directly for advanced settings
- Check `logs/openbridge.log` for troubleshooting
- Visit our GitHub for issues and discussions

**Happy Streaming! 🎮**
