#!/usr/bin/env python3
"""
OpenBridge — Interactive Setup Wizard
Makes setup foolproof with step-by-step guidance.
"""

import os
import sys
import yaml
import time
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("  🌉  O P E N B R I D G E   S E T U P   W I Z A R D")
    print("="*60)
    print()

def ask_question(question, default=None, choices=None):
    """Ask a question with optional default and choices."""
    if choices:
        print(f"\n{question}")
        for i, choice in enumerate(choices, 1):
            print(f"  {i}. {choice}")
        while True:
            answer = input(f"\nEnter choice (1-{len(choices)})" + (f" [{default}]" if default else "") + ": ").strip()
            if not answer and default:
                return choices[int(default)-1]
            if answer.isdigit() and 1 <= int(answer) <= len(choices):
                return choices[int(answer)-1]
            print("Invalid choice. Try again.")
    else:
        prompt = f"{question}"
        if default:
            prompt += f" [{default}]"
        prompt += ": "
        return input(prompt).strip() or default

def check_prerequisites():
    """Check if Python and required packages are installed."""
    print("\n📋 Checking prerequisites...")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 10):
        print("  ❌ Python 3.10+ required. Please upgrade Python.")
        return False
    print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Check if dependencies are installed
    try:
        import yaml
        print("  ✅ PyYAML installed")
    except ImportError:
        print("  ⚠️  PyYAML not found. Will install during setup.")
    
    try:
        import playwright
        print("  ✅ Playwright installed")
    except ImportError:
        print("  ⚠️  Playwright not found. Will install during setup.")
    
    return True

def create_config():
    """Create config.yaml interactively."""
    print("\n⚙️  Creating your configuration...")
    print()
    
    config = {}
    
    # Channel info
    print("─" * 40)
    print("CHANNEL SETTINGS")
    print("─" * 40)
    
    channel = ask_question(
        "What's your Twitch channel name? (lowercase)",
        default="your_channel"
    )
    config['channel'] = channel.lower().replace(' ', '')
    
    streamer = ask_question(
        "What's your display name?",
        default=channel.title()
    )
    config['streamer'] = streamer
    
    headless = ask_question(
        "Run browser invisibly? (good for servers)",
        default="no",
        choices=["yes", "no"]
    )
    config['headless'] = headless.lower() == 'yes'
    
    # Agent settings
    print("\n" + "─" * 40)
    print("AGENT SETTINGS")
    print("─" * 40)
    
    config['agents'] = {}
    
    # Chat Commander
    print("\n💬 Chat Commander - Auto-responds to chat")
    enabled = ask_question("Enable Chat Commander?", default="yes", choices=["yes", "no"])
    config['agents']['chat'] = {
        'enabled': enabled.lower() == 'yes',
        'hype_threshold': 15,
        'command_cooldown': 30,
        'welcome_raiders': True,
        'custom_commands': {
            'specs': "RTX 4090 | i9-13900K | 64GB RAM",
            'schedule': "Mon/Wed/Fri 7PM EST",
            'lurk': "Thanks for the lurk! Every view counts!",
            'discord': "Join our community: discord.gg/yourserver",
            'socials': "Follow on Twitter: @yourhandle"
        }
    }
    
    # Clip Sniper
    print("\n🎬 Clip Sniper - Auto-clips hype moments")
    enabled = ask_question("Enable Clip Sniper?", default="yes", choices=["yes", "no"])
    config['agents']['clip'] = {
        'enabled': enabled.lower() == 'yes',
        'clip_cooldown': 60
    }
    
    # Shield Guard
    print("\n🛡️  Shield Guard - Smart moderation")
    enabled = ask_question("Enable Shield Guard?", default="yes", choices=["yes", "no"])
    sensitivity = ask_question(
        "Moderation sensitivity?",
        default="medium",
        choices=["low", "medium", "high"]
    )
    config['agents']['shield'] = {
        'enabled': enabled.lower() == 'yes',
        'sensitivity': sensitivity,
        'timeout_duration': 600
    }
    
    # Growth Intel
    print("\n📊 Growth Intel - Stream analytics")
    enabled = ask_question("Enable Growth Intel?", default="yes", choices=["yes", "no"])
    config['agents']['intel'] = {
        'enabled': enabled.lower() == 'yes',
        'post_stream_summary': True
    }
    
    # Social Ghost
    print("\n👻 Social Ghost - Auto-post to social media")
    enabled = ask_question("Enable Social Ghost?", default="no", choices=["yes", "no"])
    config['agents']['social'] = {
        'enabled': enabled.lower() == 'yes',
        'platforms': ['twitter', 'discord'],
        'post_on_go_live': True,
        'post_clips': True,
        'discord_server': "Your Server Name",
        'discord_channel': "stream-announcements"
    }
    
    # Revenue Pilot
    print("\n💰 Revenue Pilot - Sub drives & merch drops")
    enabled = ask_question("Enable Revenue Pilot?", default="no", choices=["yes", "no"])
    config['agents']['revenue'] = {
        'enabled': enabled.lower() == 'yes'
    }
    
    # Platform settings
    print("\n" + "─" * 40)
    print("PLATFORM SETTINGS")
    print("─" * 40)
    
    config['platforms'] = {
        'twitch': {'enabled': True},
        'kick': {'enabled': False},
        'youtube': {'enabled': False}
    }
    
    # Save config
    config_path = Path("config.yaml")
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    
    print(f"\n✅ Configuration saved to {config_path}")
    return config

def run_setup_script():
    """Run the bash setup script."""
    print("\n📦 Installing dependencies...")
    print("(This may take a few minutes)")
    print()
    
    import subprocess
    
    # Install Python dependencies
    result = subprocess.run(
        ["pip", "install", "-r", "requirements.txt", "--quiet"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("  ✅ Python dependencies installed")
    else:
        print("  ⚠️  Some dependencies failed to install")
    
    # Install Playwright browser
    print("\n  Installing Chromium browser...")
    result = subprocess.run(
        ["playwright", "install", "chromium"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("  ✅ Chromium browser installed")
    else:
        print("  ⚠️  Browser installation had issues")
    
    # Create directories
    for dir_name in ["logs", "sessions", "data"]:
        Path(dir_name).mkdir(exist_ok=True)
    print("  ✅ Created data directories")

def show_next_steps(config):
    """Show the user what to do next."""
    print("\n" + "="*60)
    print("  ✨  SETUP COMPLETE!")
    print("="*60)
    print()
    print(f"  Your channel: #{config['channel']}")
    print(f"  Display name: {config['streamer']}")
    print(f"  Headless mode: {'Yes' if config['headless'] else 'No'}")
    print()
    print("  Enabled agents:")
    for agent, settings in config.get('agents', {}).items():
        if settings.get('enabled'):
            emoji = {'chat': '💬', 'clip': '🎬', 'shield': '🛡️', 'intel': '📊', 'social': '👻', 'revenue': '💰'}
            print(f"    {emoji.get(agent, '•')} {agent.title().replace('_', ' ')}")
    print()
    print("─" * 60)
    print("  NEXT STEPS:")
    print("─" * 60)
    print()
    print("  1. Run OpenBridge:")
    print("     python main.py")
    print()
    print("  2. First time login:")
    print("     - A browser window will open")
    print("     - Log into your Twitch account")
    print("     - Navigate to your channel page")
    print("     - Your session is saved automatically")
    print()
    print("  3. Start streaming!")
    print("     - Go live on Twitch")
    print("     - OpenBridge will start working immediately")
    print()
    print("  💡 Tips:")
    print("     - Use !help in chat to see available commands")
    print("     - Edit config.yaml to customize settings")
    print("     - Check logs/ folder for activity logs")
    print()
    print("="*60)

def main():
    """Main wizard flow."""
    print_header()
    
    print("Welcome to OpenBridge! This wizard will set up everything for you.")
    print()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\nPlease fix the issues above and run again.")
        sys.exit(1)
    
    # Check if config already exists
    if Path("config.yaml").exists():
        overwrite = ask_question(
            "\nconfig.yaml already exists. Overwrite?",
            default="no",
            choices=["yes", "no"]
        )
        if overwrite.lower() != 'yes':
            print("\nUsing existing configuration.")
            print("Run 'python main.py' to start OpenBridge.")
            sys.exit(0)
    
    # Create config
    config = create_config()
    
    # Ask if they want to install now
    print("\n" + "─" * 40)
    install_now = ask_question(
        "Install dependencies now?",
        default="yes",
        choices=["yes", "no"]
    )
    
    if install_now.lower() == 'yes':
        run_setup_script()
    
    # Show next steps
    show_next_steps(config)
    
    # Offer to start now
    print()
    start_now = ask_question(
        "Start OpenBridge now?",
        default="no",
        choices=["yes", "no"]
    )
    
    if start_now.lower() == 'yes':
        print("\n🚀 Starting OpenBridge...\n")
        import subprocess
        subprocess.run([sys.executable, "main.py"])
    else:
        print("\nYou can start OpenBridge anytime with: python main.py")
        print("\nHappy streaming! 🎮\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled. You can run this wizard again anytime.")
        sys.exit(0)
