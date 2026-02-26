# 🌉 OpenBridge

**Your invisible stream crew. 100% free. No API keys. No setup hell.**

OpenBridge is an open-source AI agent that runs alongside your stream and handles everything — chat moderation, auto-clipping, cross-posting, analytics — so you can focus on playing.

It works on **any platform** without needing API access, because it controls a real browser exactly like a human would.

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

```bash
# 1. Clone
git clone https://github.com/yourname/openbridge
cd openbridge

# 2. Setup (installs everything)
bash setup.sh

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
- That's it

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

---

## License

MIT. Free forever for personal use.

---

*Built by streamers, for streamers.*
*Zero API keys. Zero monthly fees. Just your crew.*
