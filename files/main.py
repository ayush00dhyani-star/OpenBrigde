"""
OpenBridge — Run this to start your crew.

  python main.py

First time? Run setup first:
  bash setup.sh
"""

import asyncio
import logging
import os
import sys
import yaml

# ── Dirs ──────────────────────────────────────────────────────
os.makedirs("logs",    exist_ok=True)
os.makedirs("sessions", exist_ok=True)

# ── Logging ───────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/openbridge.log", mode="a"),
    ],
)
logger = logging.getLogger("openbridge")

# ── Suppress noisy libs ───────────────────────────────────────
logging.getLogger("playwright").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)


def load_config() -> dict:
    path = "config.yaml"
    if not os.path.exists(path):
        print("\n  ❌  config.yaml not found.")
        print("  Run: cp config.example.yaml config.yaml")
        print("  Then edit it with your channel name.\n")
        sys.exit(1)
    with open(path) as f:
        cfg = yaml.safe_load(f)
    if cfg.get("channel") in (None, "your_twitch_channel", ""):
        print("\n  ❌  Open config.yaml and set your channel name first.\n")
        sys.exit(1)
    return cfg


async def main():
    cfg = load_config()

    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║         🌉  O P E N B R I D G E        ║")
    print("  ╚══════════════════════════════════════╝")
    print(f"  Channel  : #{cfg['channel']}")
    print(f"  Streamer : {cfg.get('streamer', cfg['channel'])}")
    print(f"  Headless : {cfg.get('headless', False)}")
    print()

    from core.orchestrator import OpenBridge
    crew = OpenBridge(cfg)
    await crew.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  🌉  OpenBridge stopped. See you next stream.\n")
