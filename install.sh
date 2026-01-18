#!/bin/bash
# =============================================================================
# UFO Galaxy 64-Core MCP Matrix - One-Click Installer
# =============================================================================
# This script installs UFO Galaxy into your UFO3 environment.
#
# Usage:
#   ./install.sh [target_dir]
#
# Default target: /opt/ufo-galaxy (requires sudo)
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# =============================================================================
# Configuration
# =============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-/opt/ufo-galaxy}"
SERVICE_NAME="ufo-galaxy"

# =============================================================================
# Pre-flight Checks
# =============================================================================

echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         🛸 UFO Galaxy 64-Core MCP Matrix Installer 🛸         ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if running as root for system installation
if [[ "$TARGET_DIR" == /opt/* ]] && [[ $EUID -ne 0 ]]; then
    log_warning "Installing to $TARGET_DIR requires root privileges."
    log_info "Re-running with sudo..."
    exec sudo "$0" "$@"
fi

# Check for Podman or Docker
if command -v podman &> /dev/null; then
    CONTAINER_RUNTIME="podman"
    COMPOSE_CMD="podman-compose"
elif command -v docker &> /dev/null; then
    CONTAINER_RUNTIME="docker"
    COMPOSE_CMD="docker-compose"
else
    log_error "Neither Podman nor Docker found. Please install one first."
    echo ""
    echo "Install Podman:"
    echo "  Ubuntu/Debian: sudo apt install podman podman-compose"
    echo "  Fedora/RHEL:   sudo dnf install podman podman-compose"
    echo "  macOS:         brew install podman podman-compose"
    echo ""
    exit 1
fi

log_info "Using container runtime: $CONTAINER_RUNTIME"

# Check for compose
if ! command -v $COMPOSE_CMD &> /dev/null; then
    log_warning "$COMPOSE_CMD not found. Installing..."
    if [[ "$CONTAINER_RUNTIME" == "podman" ]]; then
        pip3 install podman-compose 2>/dev/null || sudo pip3 install podman-compose
    fi
fi

# =============================================================================
# Installation
# =============================================================================

log_info "Installing UFO Galaxy to: $TARGET_DIR"

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy files
log_info "Copying files..."
cp -r "$SCRIPT_DIR"/* "$TARGET_DIR/"

# Set permissions
chmod +x "$TARGET_DIR/bootstrap.sh"
chmod +x "$TARGET_DIR/install.sh"
chmod +x "$TARGET_DIR/scripts/launcher_v2.py"

# Create data directories
mkdir -p "$TARGET_DIR/data"
mkdir -p "$TARGET_DIR/logs"
mkdir -p "$TARGET_DIR/backups"

# =============================================================================
# Configuration
# =============================================================================

log_info "Setting up configuration..."

# Generate secure HMAC secret if not exists
if ! grep -q "HMAC_SECRET=" "$TARGET_DIR/config/.env" 2>/dev/null || \
   grep -q "HMAC_SECRET=$" "$TARGET_DIR/config/.env" 2>/dev/null; then
    HMAC_SECRET=$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xxd -p)
    if grep -q "HMAC_SECRET=" "$TARGET_DIR/config/.env" 2>/dev/null; then
        sed -i "s/HMAC_SECRET=.*/HMAC_SECRET=$HMAC_SECRET/" "$TARGET_DIR/config/.env"
    else
        echo "HMAC_SECRET=$HMAC_SECRET" >> "$TARGET_DIR/config/.env"
    fi
    log_info "Generated new HMAC secret"
fi

# =============================================================================
# Systemd Service (Optional)
# =============================================================================

if [[ -d /etc/systemd/system ]] && [[ $EUID -eq 0 ]]; then
    log_info "Creating systemd service..."
    
    cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=UFO Galaxy 64-Core MCP Matrix
After=network.target

[Service]
Type=simple
WorkingDirectory=$TARGET_DIR
ExecStart=$TARGET_DIR/bootstrap.sh start
ExecStop=$TARGET_DIR/bootstrap.sh stop
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    log_success "Systemd service created: $SERVICE_NAME"
    log_info "Enable with: sudo systemctl enable $SERVICE_NAME"
fi

# =============================================================================
# Create convenience symlinks
# =============================================================================

if [[ $EUID -eq 0 ]] && [[ -d /usr/local/bin ]]; then
    ln -sf "$TARGET_DIR/bootstrap.sh" /usr/local/bin/ufo-galaxy
    log_success "Created symlink: ufo-galaxy -> $TARGET_DIR/bootstrap.sh"
fi

# =============================================================================
# Final Summary
# =============================================================================

echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              ✅ Installation Complete! ✅                     ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "Installation directory: ${CYAN}$TARGET_DIR${NC}"
echo -e "Container runtime:      ${CYAN}$CONTAINER_RUNTIME${NC}"
echo ""
echo -e "${YELLOW}Next Steps:${NC}"
echo ""
echo "1. Configure API keys (optional):"
echo "   vim $TARGET_DIR/config/.env"
echo ""
echo "2. Start UFO Galaxy:"
echo "   cd $TARGET_DIR && ./bootstrap.sh start"
echo ""
if [[ -f /etc/systemd/system/${SERVICE_NAME}.service ]]; then
echo "3. Or use systemd:"
echo "   sudo systemctl start $SERVICE_NAME"
echo "   sudo systemctl enable $SERVICE_NAME  # Auto-start on boot"
echo ""
fi
echo "4. Check status:"
echo "   ./bootstrap.sh status"
echo ""
echo "5. View dashboard:"
echo "   ./bootstrap.sh dashboard"
echo "   Open http://localhost:8080"
echo ""
echo -e "${CYAN}Documentation: $TARGET_DIR/README.md${NC}"
echo ""
