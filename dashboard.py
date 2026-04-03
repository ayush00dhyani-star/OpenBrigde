"""
OpenBridge — Interactive Status Dashboard
Shows real-time status and lets you control agents.
"""

import os
import sys
import time
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("  🌉  O P E N B R I D G E   S T A T U S")
    print("="*60)
    print()

def check_running():
    """Check if OpenBridge is currently running."""
    import subprocess
    try:
        result = subprocess.run(
            ["pgrep", "-f", "python.*main.py"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0 and bool(result.stdout.strip())
    except Exception:
        return False

def get_config_summary():
    """Read and summarize config.yaml."""
    import yaml
    config_path = Path("config.yaml")
    if not config_path.exists():
        return None
    
    with open(config_path) as f:
        config = yaml.safe_load(f)
    
    summary = {
        'channel': config.get('channel', 'Not configured'),
        'streamer': config.get('streamer', 'Unknown'),
        'headless': config.get('headless', False),
        'agents': {}
    }
    
    for agent, settings in config.get('agents', {}).items():
        summary['agents'][agent] = settings.get('enabled', False)
    
    return summary

def show_status():
    """Display current status."""
    print_header()
    
    # Check if running
    is_running = check_running()
    status_icon = "🟢 RUNNING" if is_running else "🔴 STOPPED"
    print(f"Status: {status_icon}")
    print()
    
    # Config summary
    config = get_config_summary()
    if config:
        print(f"Channel: #{config['channel']}")
        print(f"Streamer: {config['streamer']}")
        print(f"Headless: {'Yes' if config['headless'] else 'No'}")
        print()
        print("Agents:")
        for agent, enabled in config['agents'].items():
            icon = "✅" if enabled else "❌"
            name = agent.title().replace('_', ' ')
            print(f"  {icon} {name}")
    else:
        print("⚠️  No configuration found!")
        print("   Run: python wizard.py")
    print()
    
    # Quick stats
    logs_dir = Path("logs")
    if logs_dir.exists():
        log_files = list(logs_dir.glob("*.log"))
        if log_files:
            latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
            size_mb = latest_log.stat().st_size / (1024 * 1024)
            print(f"Latest log: {latest_log.name} ({size_mb:.1f} MB)")
    
    sessions_dir = Path("sessions")
    if sessions_dir.exists():
        session_count = len(list(sessions_dir.iterdir()))
        print(f"Saved sessions: {session_count}")
    
    print()

def main_menu():
    """Show interactive menu."""
    while True:
        show_status()
        
        print("What would you like to do?")
        print("  1. Start OpenBridge")
        print("  2. Stop OpenBridge")
        print("  3. View logs (last 20 lines)")
        print("  4. Edit configuration")
        print("  5. Run setup wizard")
        print("  6. Exit")
        print()
        
        choice = input("Enter choice (1-6) [6]: ").strip() or "6"
        
        if choice == "1":
            if check_running():
                print("\n⚠️  OpenBridge is already running!")
                input("Press Enter to continue...")
            else:
                print("\n🚀 Starting OpenBridge...")
                print("(OpenBridge will run in the foreground. Use Ctrl+C to stop.)")
                print()
                import subprocess
                subprocess.run([sys.executable, "main.py"])
        
        elif choice == "2":
            if check_running():
                print("\n⏹️  Stopping OpenBridge...")
                import subprocess
                subprocess.run(["pkill", "-f", "python.*main.py"])
                print("Stopped!")
            else:
                print("\nℹ️  OpenBridge is not running.")
            input("Press Enter to continue...")
        
        elif choice == "3":
            log_file = Path("logs/openbridge.log")
            if log_file.exists():
                print("\n" + "="*60)
                print("LAST 20 LOG LINES:")
                print("="*60)
                with open(log_file) as f:
                    lines = f.readlines()[-20:]
                    for line in lines:
                        print(line.rstrip())
                print("="*60)
            else:
                print("\n⚠️  No log file found.")
            input("Press Enter to continue...")
        
        elif choice == "4":
            config_file = Path("config.yaml")
            if config_file.exists():
                print(f"\nOpening {config_file} in default editor...")
                print("(Close the editor to return)")
                import subprocess
                editor = os.environ.get('EDITOR', 'nano')
                subprocess.run([editor, str(config_file)])
            else:
                print("\n⚠️  No config.yaml found. Run the wizard first.")
            input("Press Enter to continue...")
        
        elif choice == "5":
            print("\n📝 Running setup wizard...")
            import subprocess
            subprocess.run([sys.executable, "wizard.py"])
        
        elif choice == "6":
            print("\n👋 Goodbye!\n")
            break
        
        else:
            print("\n⚠️  Invalid choice. Try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nDashboard closed.")
        sys.exit(0)
