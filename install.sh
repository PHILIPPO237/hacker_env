#!/bin/bash
# HACKER_ENV V2 - Installation Script
# Supports Termux, WSL, and native Linux

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Banner
echo -e "${CYAN}"
echo "  ╔══════════════════════════════════════════════════╗"
echo "  ║                                                  ║"
echo "  ║           HACKER_ENV V2 Installer                ║"
echo "  ║                                                  ║"
echo "  ╚══════════════════════════════════════════════════╝"
echo -e "${NC}"

# Detect platform
echo -e "${BLUE}Detecting platform...${NC}"

if [ -d "/data/data/com.termux" ]; then
    PLATFORM="termux"
    print_info "Platform: Termux"
elif grep -qi microsoft /proc/version 2>/dev/null || [ -f "/proc/sys/fs/binfmt_misc/WSLInterop" ]; then
    PLATFORM="wsl"
    print_info "Platform: WSL"
elif [ -f "/etc/os-release" ]; then
    PLATFORM="linux"
    DISTRO=$(grep "^NAME=" /etc/os-release | cut -d'"' -f2)
    print_info "Platform: Linux ($DISTRO)"
else
    PLATFORM="linux"
    print_info "Platform: Linux (unknown distro)"
fi

# Check Python
echo -e "\n${BLUE}Checking Python...${NC}"

if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    print_success "Python3 found: $PYTHON_VERSION"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    print_success "Python found: $PYTHON_VERSION"
else
    print_error "Python not found!"
    echo -e "${YELLOW}Please install Python first:${NC}"
    
    if [ "$PLATFORM" = "termux" ]; then
        echo "  pkg install python"
    elif [ "$PLATFORM" = "wsl" ] || [ "$PLATFORM" = "linux" ]; then
        echo "  sudo apt install python3 python3-pip"
    fi
    
    exit 1
fi

# Check pip
echo -e "\n${BLUE}Checking pip...${NC}"

if $PYTHON_CMD -m pip --version &> /dev/null; then
    print_success "pip available"
else
    print_warning "pip not found, installing..."
    
    if [ "$PLATFORM" = "termux" ]; then
        pkg install -y python-pip
    else
        $PYTHON_CMD -m ensurepip --default-pip 2>/dev/null || sudo apt install -y python3-pip
    fi
fi

# Check dependencies
echo -e "\n${BLUE}Checking dependencies...${NC}"

MISSING_DEPS=()

# Check for required modules
for module in os sys json shutil; do
    if $PYTHON_CMD -c "import $module" 2>/dev/null; then
        print_success "$module: OK"
    else
        print_error "$module: MISSING"
        MISSING_DEPS+=("$module")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    print_error "Missing dependencies: ${MISSING_DEPS[*]}"
    exit 1
fi

# Create backup directory
echo -e "\n${BLUE}Creating directories...${NC}"

BACKUP_DIR="$HOME/.hacker_env/backups"
LOG_DIR="$HOME/.hacker_env/logs"

mkdir -p "$BACKUP_DIR" 2>/dev/null || true
mkdir -p "$LOG_DIR" 2>/dev/null || true

print_success "Directories created"

# Backup existing configs
echo -e "\n${BLUE}Backing up existing configurations...${NC}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)

for config_file in ~/.zshrc ~/.bashrc ~/.profile; do
    if [ -f "$config_file" ]; then
        cp "$config_file" "$BACKUP_DIR/$(basename $config_file).backup.$TIMESTAMP"
        print_success "Backed up: $config_file"
    fi
done

# Run the main application
echo -e "\n${GREEN}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Setup complete! Launching HACKER_ENV V2...${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════${NC}"
echo ""

# Change to script directory
cd "$(dirname "$0")"

# Run the application
$PYTHON_CMD main.py
