#!/bin/bash
# OpenBridge — One-command setup

set -e

echo ""
echo "  🌉  🌉  OpenBridge Setup"
echo "  ==================="
echo ""

# Check Python
python3 --version || { echo "Python 3.10+ required"; exit 1; }

# Install deps
echo "→ Installing dependencies..."
pip install -r requirements.txt --quiet

# Install browser
echo "→ Installing Chromium browser..."
playwright install chromium

# Create dirs
mkdir -p logs sessions

# Copy config if not exists
if [ ! -f config.yaml ]; then
  cp config.example.yaml config.yaml
  echo "→ Created config.yaml — edit it with your channel name"
fi

echo ""
echo "  ✅ Setup complete!"
echo ""
echo "  Next steps:"
echo "  1. Edit config.yaml — set your channel name"
echo "  2. Run: python main.py"
echo ""
