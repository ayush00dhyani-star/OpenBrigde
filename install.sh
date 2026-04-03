#!/bin/bash
# OpenBridge Universal Installer for macOS and Linux
# The absolute easiest way to install OpenBridge on any Unix-like system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo ""
    echo -e "${BLUE}╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║${NC}        🌉  O P E N B R I D G E   I N S T A L L E R       ${BLUE}║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

check_python() {
    print_info "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Found Python $PYTHON_VERSION"
        PYTHON_CMD="python3"
        return 0
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        print_success "Found Python $PYTHON_VERSION"
        PYTHON_CMD="python"
        return 0
    else
        return 1
    fi
}

install_python() {
    print_info "Python not found. Installing Python..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install python@3.11
        else
            print_error "Homebrew not found. Please install Python manually:"
            print_info "1. Install Homebrew: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            print_info "2. Then run: brew install python@3.11"
            print_info "Or download from: https://python.org/downloads"
            exit 1
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm python python-pip
        elif command -v zypper &> /dev/null; then
            sudo zypper install -y python3 python3-pip
        else
            print_error "Unsupported Linux distribution. Please install Python 3.10+ manually."
            print_info "Download from: https://python.org/downloads"
            exit 1
        fi
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    
    if ! check_python; then
        print_error "Failed to install Python. Please install manually."
        exit 1
    fi
}

install_dependencies() {
    print_info "Installing Python dependencies..."
    
    # Create virtual environment (recommended)
    if [ ! -d "venv" ]; then
        print_info "Creating virtual environment..."
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    print_info "Upgrading pip..."
    pip install --upgrade pip --quiet
    
    # Install requirements
    print_info "Installing required packages..."
    pip install -r requirements.txt --quiet
    
    print_success "Dependencies installed"
}

install_browser() {
    print_info "Installing Chromium browser (this may take a few minutes)..."
    playwright install chromium
    
    # Install system dependencies for Linux
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Installing browser system dependencies..."
        if command -v apt &> /dev/null; then
            playwright install-deps chromium 2>/dev/null || {
                print_info "Some system dependencies may need manual installation"
                print_info "Run: sudo apt install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2"
            }
        elif command -v dnf &> /dev/null; then
            playwright install-deps chromium 2>/dev/null || true
        fi
    fi
    
    print_success "Browser installed"
}

create_directories() {
    print_info "Creating required directories..."
    mkdir -p logs sessions data
    print_success "Directories created"
}

setup_config() {
    if [ ! -f config.yaml ]; then
        print_info "Creating configuration file..."
        cp config.example.yaml config.yaml
        print_success "Configuration file created"
        print_info "Edit config.yaml to set your channel name"
    else
        print_success "Configuration file already exists"
    fi
}

make_scripts_executable() {
    print_info "Making scripts executable..."
    chmod +x start.sh wizard.py dashboard.py setup.sh 2>/dev/null || true
    print_success "Scripts ready"
}

run_wizard() {
    echo ""
    read -p "Would you like to run the setup wizard now? (Y/n) " choice
    choice=${choice:-Y}
    
    if [[ $choice =~ ^[Yy]$ ]]; then
        echo ""
        print_info "Starting setup wizard..."
        if [ -d "venv" ]; then
            source venv/bin/activate
        fi
        $PYTHON_CMD wizard.py
    else
        echo ""
        print_info "You can run the wizard later with: python wizard.py"
        print_info "Or start OpenBridge with: ./start.sh"
    fi
}

show_completion() {
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║           🎉  INSTALLATION COMPLETE! 🎉              ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. Edit config.yaml to set your channel name"
    echo "  2. Run ./start.sh to launch OpenBridge"
    echo "  3. Log into Twitch when the browser opens"
    echo "  4. Go live and let OpenBridge handle the rest!"
    echo ""
    echo -e "${YELLOW}Quick commands:${NC}"
    echo "  ./start.sh        - Interactive menu"
    echo "  python wizard.py  - Setup wizard"
    echo "  python main.py    - Start directly"
    echo ""
}

# Main installation flow
main() {
    print_header
    
    # Check if running in OpenBridge directory
    if [ ! -f "requirements.txt" ]; then
        print_error "Please run this script from the OpenBridge directory"
        print_info "Usage: cd openbridge && bash install.sh"
        exit 1
    fi
    
    # Step 1: Check/install Python
    if ! check_python; then
        install_python
    fi
    
    # Step 2: Install dependencies
    install_dependencies
    
    # Step 3: Install browser
    install_browser
    
    # Step 4: Create directories
    create_directories
    
    # Step 5: Setup config
    setup_config
    
    # Step 6: Make scripts executable
    make_scripts_executable
    
    # Step 7: Optional wizard
    run_wizard
    
    # Show completion message
    show_completion
}

# Handle command line arguments
case "${1:-}" in
    --no-wizard)
        NO_WIZARD=true
        main
        ;;
    --help|-h)
        echo "OpenBridge Universal Installer"
        echo ""
        echo "Usage: bash install.sh [OPTIONS]"
        echo ""
        echo "Options:"
        echo "  --no-wizard    Skip the setup wizard at the end"
        echo "  --help, -h     Show this help message"
        echo ""
        echo "This script will:"
        echo "  ✓ Check/install Python 3.10+"
        echo "  ✓ Create a virtual environment"
        echo "  ✓ Install all dependencies"
        echo "  ✓ Install Chromium browser"
        echo "  ✓ Create required directories"
        echo "  ✓ Setup configuration file"
        echo ""
        exit 0
        ;;
    *)
        main
        ;;
esac
