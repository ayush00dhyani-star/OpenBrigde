#!/bin/bash
# OpenBridge — Quick Start Script
# The absolute easiest way to get started

set -e

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║         🌉  O P E N B R I D G E   Q U I C K S T A R T  ║"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3.10+ from https://python.org"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if config exists
if [ ! -f config.yaml ]; then
    echo "📝 No configuration found. Starting setup wizard..."
    echo ""
    python3 wizard.py
    exit $?
fi

# Config exists, ask what to do
echo "✅ Configuration found!"
echo ""
echo "What would you like to do?"
echo "  1. Start OpenBridge (python main.py)"
echo "  2. Re-run setup wizard"
echo "  3. View current configuration"
echo "  4. Exit"
echo ""
read -p "Enter choice (1-4) [1]: " choice
choice=${choice:-1}

case $choice in
    1)
        echo ""
        echo "🚀 Starting OpenBridge..."
        echo ""
        python3 main.py
        ;;
    2)
        echo ""
        python3 wizard.py
        ;;
    3)
        echo ""
        echo "─" * 60
        cat config.yaml
        echo "─" * 60
        ;;
    4)
        echo ""
        echo "👋 Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
