#!/bin/bash

# UFO Galaxy 70-Core Matrix - One-Click Installer
# Version: 2.2 (Aligned & Automated)

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

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_DIR="${1:-/opt/ufo-galaxy}"
SERVICE_NAME="ufo-galaxy"

echo -e "${CYAN}=== UFO Galaxy 70-Core Matrix Installer ===${NC}"

# 1. Root Check
if [[ "$TARGET_DIR" == /opt/* ]] && [[ $EUID -ne 0 ]]; then
    log_warning "Installing to $TARGET_DIR requires root privileges."
    log_info "Re-running with sudo..."
    exec sudo "$0" "$@"
fi

# 2. Runtime Check
if command -v podman &> /dev/null; then
    CONTAINER_RUNTIME="podman"
    COMPOSE_CMD="podman-compose"
elif command -v docker &> /dev/null; then
    CONTAINER_RUNTIME="docker"
    COMPOSE_CMD="docker-compose"
else
    log_error "Neither Podman nor Docker found. Please install one first."
    exit 1
fi

# 3. Installation
log_info "Installing to: $TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -r "$SCRIPT_DIR"/* "$TARGET_DIR/"
chmod +x "$TARGET_DIR/bootstrap.sh"
chmod +x "$TARGET_DIR/install.sh"

# 4. Data Directories
mkdir -p "$TARGET_DIR/data/redis" "$TARGET_DIR/data/qdrant" "$TARGET_DIR/data/sqlite" "$TARGET_DIR/data/logs" "$TARGET_DIR/data/backups"

# 5. Systemd Service
if [[ -d /etc/systemd/system ]] && [[ $EUID -eq 0 ]]; then
    log_info "Creating systemd service..."
    cat > /etc/systemd/system/${SERVICE_NAME}.service << EOF
[Unit]
Description=UFO Galaxy 70-Core Matrix
After=network.target podman.service docker.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$TARGET_DIR
ExecStart=$TARGET_DIR/bootstrap.sh start
ExecStop=$TARGET_DIR/bootstrap.sh stop
Restart=always

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
    log_success "Systemd service created: $SERVICE_NAME"
fi

log_success "Installation Complete!"
echo -e "Start with: ${GREEN}cd $TARGET_DIR && ./bootstrap.sh start${NC}"
