#!/bin/bash
# =============================================================================
# UFO Galaxy 64-Core MCP Matrix - Bootstrap Script
# =============================================================================
# Intelligent cross-platform bootstrap with automatic environment detection
# and adaptive configuration.
#
# Usage:
#   ./bootstrap.sh [command] [options]
#
# Commands:
#   install     - Install dependencies and setup environment
#   start       - Start the UFO Galaxy system
#   stop        - Stop all services
#   status      - Show system status
#   logs        - View logs
#   test        - Run tests
#   dashboard   - Start the dashboard
#   help        - Show this help message
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="${SCRIPT_DIR}/config"
DATA_DIR="${SCRIPT_DIR}/data"
LOGS_DIR="${SCRIPT_DIR}/logs"

# =============================================================================
# Utility Functions
# =============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo ""
    echo -e "${CYAN}========================================${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo ""
}

# =============================================================================
# Environment Detection
# =============================================================================

detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if [ -f /etc/os-release ]; then
            . /etc/os-release
            OS=$NAME
            OS_VERSION=$VERSION_ID
        else
            OS="Linux"
            OS_VERSION="unknown"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macOS"
        OS_VERSION=$(sw_vers -productVersion)
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        OS="Windows"
        OS_VERSION="unknown"
    else
        OS="Unknown"
        OS_VERSION="unknown"
    fi
    
    log_info "Detected OS: $OS $OS_VERSION"
}

detect_container_runtime() {
    if command -v podman &> /dev/null; then
        CONTAINER_RUNTIME="podman"
        COMPOSE_CMD="podman-compose"
    elif command -v docker &> /dev/null; then
        CONTAINER_RUNTIME="docker"
        COMPOSE_CMD="docker-compose"
    else
        CONTAINER_RUNTIME="none"
        COMPOSE_CMD=""
    fi
    
    log_info "Container runtime: $CONTAINER_RUNTIME"
}

detect_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
    else
        PYTHON_CMD=""
        PYTHON_VERSION=""
    fi
    
    if [ -n "$PYTHON_CMD" ]; then
        log_info "Python: $PYTHON_VERSION"
    else
        log_warning "Python not found"
    fi
}

detect_hardware() {
    # CPU cores
    if [[ "$OS" == "macOS" ]]; then
        CPU_CORES=$(sysctl -n hw.ncpu)
    else
        CPU_CORES=$(nproc 2>/dev/null || echo "unknown")
    fi
    
    # Memory
    if [[ "$OS" == "macOS" ]]; then
        TOTAL_MEM=$(sysctl -n hw.memsize | awk '{print int($1/1024/1024/1024)"GB"}')
    else
        TOTAL_MEM=$(free -h 2>/dev/null | awk '/^Mem:/{print $2}' || echo "unknown")
    fi
    
    # GPU (NVIDIA)
    if command -v nvidia-smi &> /dev/null; then
        GPU_INFO=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)
        HAS_GPU=true
    else
        GPU_INFO="None detected"
        HAS_GPU=false
    fi
    
    log_info "CPU Cores: $CPU_CORES"
    log_info "Memory: $TOTAL_MEM"
    log_info "GPU: $GPU_INFO"
}

detect_android_devices() {
    if command -v adb &> /dev/null; then
        ANDROID_DEVICES=$(adb devices 2>/dev/null | grep -c "device$" || echo "0")
        log_info "Android devices: $ANDROID_DEVICES"
    else
        ANDROID_DEVICES=0
        log_info "ADB not found - Android features disabled"
    fi
}

# =============================================================================
# Configuration Generation
# =============================================================================

generate_config() {
    log_header "Generating Configuration"
    
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$DATA_DIR"
    mkdir -p "$LOGS_DIR"
    
    # Generate .env file
    cat > "$CONFIG_DIR/.env" << EOF
# UFO Galaxy Configuration
# Generated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")

# System
UFO_GALAXY_VERSION=2.0.0
ENVIRONMENT=production
LOG_LEVEL=INFO

# Container Runtime
CONTAINER_RUNTIME=${CONTAINER_RUNTIME}

# Hardware
CPU_CORES=${CPU_CORES}
HAS_GPU=${HAS_GPU}
ANDROID_DEVICES=${ANDROID_DEVICES}

# Network
STATE_MACHINE_PORT=8000
TRANSFORMER_PORT=8050
MODEL_ROUTER_PORT=8058
TELEMETRY_PORT=8064
LOGGER_PORT=8065
HEALTH_MONITOR_PORT=8067
BACKUP_PORT=8069

# Model Configuration (fill in your API keys)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
LOCAL_MODEL_URL=http://localhost:11434

# Data Directories
DATA_DIR=${DATA_DIR}
LOGS_DIR=${LOGS_DIR}

# Security
HMAC_SECRET=$(openssl rand -hex 32 2>/dev/null || echo "ufo-galaxy-default-secret")
EOF

    log_success "Configuration generated at $CONFIG_DIR/.env"
    
    # Generate adaptive compose file based on hardware
    generate_compose_override
}

generate_compose_override() {
    local COMPOSE_OVERRIDE="$SCRIPT_DIR/podman-compose.override.yml"
    
    cat > "$COMPOSE_OVERRIDE" << EOF
# UFO Galaxy - Adaptive Configuration Override
# Generated based on detected hardware

version: '3.8'

services:
EOF

    # Adjust resources based on available hardware
    if [ "$CPU_CORES" -ge 8 ]; then
        cat >> "$COMPOSE_OVERRIDE" << EOF
  node_00_statemachine:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  node_58_modelrouter:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
EOF
    else
        cat >> "$COMPOSE_OVERRIDE" << EOF
  node_00_statemachine:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M

  node_58_modelrouter:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
EOF
    fi

    # Add GPU support if available
    if [ "$HAS_GPU" = true ]; then
        cat >> "$COMPOSE_OVERRIDE" << EOF

  node_52_qiskit:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
EOF
    fi

    log_success "Compose override generated"
}

# =============================================================================
# Installation
# =============================================================================

install_dependencies() {
    log_header "Installing Dependencies"
    
    # Check container runtime
    if [ "$CONTAINER_RUNTIME" = "none" ]; then
        log_warning "No container runtime found. Installing Podman..."
        
        if [[ "$OS" == *"Ubuntu"* ]] || [[ "$OS" == *"Debian"* ]]; then
            sudo apt-get update
            sudo apt-get install -y podman podman-compose
        elif [[ "$OS" == *"Fedora"* ]] || [[ "$OS" == *"CentOS"* ]] || [[ "$OS" == *"Red Hat"* ]]; then
            sudo dnf install -y podman podman-compose
        elif [[ "$OS" == "macOS" ]]; then
            brew install podman podman-compose
        else
            log_error "Please install Podman manually: https://podman.io/getting-started/installation"
            exit 1
        fi
        
        detect_container_runtime
    fi
    
    # Install Python dependencies for local testing
    if [ -n "$PYTHON_CMD" ]; then
        log_info "Installing Python dependencies..."
        $PYTHON_CMD -m pip install --user fastapi uvicorn httpx redis pydantic 2>/dev/null || true
    fi
    
    log_success "Dependencies installed"
}

# =============================================================================
# Service Management
# =============================================================================

start_services() {
    log_header "Starting UFO Galaxy"
    
    if [ "$CONTAINER_RUNTIME" = "none" ]; then
        log_error "No container runtime available. Run './bootstrap.sh install' first."
        exit 1
    fi
    
    # Load environment
    if [ -f "$CONFIG_DIR/.env" ]; then
        export $(grep -v '^#' "$CONFIG_DIR/.env" | xargs)
    fi
    
    cd "$SCRIPT_DIR"
    
    # Start with compose
    if [ -f "podman-compose.override.yml" ]; then
        $COMPOSE_CMD -f podman-compose.yml -f podman-compose.override.yml up -d
    else
        $COMPOSE_CMD up -d
    fi
    
    log_success "UFO Galaxy started"
    
    # Wait for services
    log_info "Waiting for services to be ready..."
    sleep 5
    
    show_status
}

stop_services() {
    log_header "Stopping UFO Galaxy"
    
    cd "$SCRIPT_DIR"
    
    if [ -n "$COMPOSE_CMD" ]; then
        $COMPOSE_CMD down
    fi
    
    log_success "UFO Galaxy stopped"
}

show_status() {
    log_header "System Status"
    
    if [ -n "$COMPOSE_CMD" ]; then
        cd "$SCRIPT_DIR"
        $COMPOSE_CMD ps
    fi
    
    echo ""
    log_info "Checking node health..."
    
    # Check each node
    check_node "Node 00 (StateMachine)" "http://localhost:8000/health"
    check_node "Node 50 (Transformer)" "http://localhost:8050/health"
    check_node "Node 58 (ModelRouter)" "http://localhost:8058/health"
    check_node "Node 64 (Telemetry)" "http://localhost:8064/health"
    check_node "Node 65 (Logger)" "http://localhost:8065/health"
    check_node "Node 67 (HealthMonitor)" "http://localhost:8067/health"
    check_node "Node 69 (Backup)" "http://localhost:8069/health"
}

check_node() {
    local name=$1
    local url=$2
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null | grep -q "200"; then
        echo -e "  ${GREEN}✓${NC} $name"
    else
        echo -e "  ${RED}✗${NC} $name"
    fi
}

show_logs() {
    log_header "Viewing Logs"
    
    local service=$1
    
    if [ -n "$COMPOSE_CMD" ]; then
        cd "$SCRIPT_DIR"
        if [ -n "$service" ]; then
            $COMPOSE_CMD logs -f "$service"
        else
            $COMPOSE_CMD logs -f
        fi
    fi
}

# =============================================================================
# Testing
# =============================================================================

run_tests() {
    log_header "Running Tests"
    
    if [ -n "$PYTHON_CMD" ]; then
        cd "$SCRIPT_DIR"
        
        # Run local verification
        if [ -f "tests/local_verify.py" ]; then
            log_info "Running local verification..."
            $PYTHON_CMD tests/local_verify.py
        fi
        
        # Run mission tests
        if [ -f "tests/test_mission.py" ]; then
            log_info "Running mission tests..."
            $PYTHON_CMD tests/test_mission.py
        fi
    else
        log_error "Python not found. Cannot run tests."
        exit 1
    fi
}

# =============================================================================
# Dashboard
# =============================================================================

start_dashboard() {
    log_header "Starting Dashboard"
    
    if [ -n "$PYTHON_CMD" ]; then
        cd "$SCRIPT_DIR"
        
        if [ -f "dashboard/app.py" ]; then
            log_info "Starting dashboard on http://localhost:8080"
            $PYTHON_CMD dashboard/app.py
        else
            log_warning "Dashboard not found. Creating basic dashboard..."
            create_dashboard
            $PYTHON_CMD dashboard/app.py
        fi
    else
        log_error "Python not found. Cannot start dashboard."
        exit 1
    fi
}

create_dashboard() {
    mkdir -p "$SCRIPT_DIR/dashboard"
    
    cat > "$SCRIPT_DIR/dashboard/app.py" << 'DASHBOARD_EOF'
"""
UFO Galaxy Dashboard
Simple monitoring dashboard for the 64-core system.
"""

import os
import json
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import httpx

app = FastAPI(title="UFO Galaxy Dashboard")

NODES = {
    "Node_00_StateMachine": "http://localhost:8000",
    "Node_50_Transformer": "http://localhost:8050",
    "Node_58_ModelRouter": "http://localhost:8058",
    "Node_64_Telemetry": "http://localhost:8064",
    "Node_65_LoggerCentral": "http://localhost:8065",
    "Node_67_HealthMonitor": "http://localhost:8067",
    "Node_69_BackupRestore": "http://localhost:8069",
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>UFO Galaxy Dashboard</title>
    <meta http-equiv="refresh" content="10">
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #1a1a2e; color: #eee; }
        h1 { color: #00d4ff; text-align: center; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #16213e; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
        .card h3 { margin-top: 0; color: #00d4ff; }
        .status { display: inline-block; padding: 5px 10px; border-radius: 5px; font-weight: bold; }
        .healthy { background: #00c853; color: #fff; }
        .unhealthy { background: #ff1744; color: #fff; }
        .unknown { background: #ffc107; color: #000; }
        .metric { margin: 10px 0; }
        .metric-label { color: #888; }
        .metric-value { font-size: 1.2em; font-weight: bold; }
        .timestamp { text-align: center; color: #666; margin-top: 20px; }
    </style>
</head>
<body>
    <h1>🛸 UFO Galaxy 64-Core Dashboard</h1>
    <div class="grid">
        {cards}
    </div>
    <p class="timestamp">Last updated: {timestamp}</p>
</body>
</html>
"""

async def check_node(name: str, url: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{url}/health")
            if response.status_code == 200:
                data = response.json()
                return {"name": name, "status": "healthy", "data": data}
    except:
        pass
    return {"name": name, "status": "unhealthy", "data": {}}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    cards = []
    
    for name, url in NODES.items():
        node = await check_node(name, url)
        status_class = node["status"]
        
        card = f"""
        <div class="card">
            <h3>{name}</h3>
            <span class="status {status_class}">{status_class.upper()}</span>
            <div class="metric">
                <span class="metric-label">URL:</span>
                <span class="metric-value">{url}</span>
            </div>
        </div>
        """
        cards.append(card)
    
    html = HTML_TEMPLATE.format(
        cards="\n".join(cards),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    
    return HTMLResponse(content=html)

@app.get("/api/status")
async def api_status():
    results = {}
    for name, url in NODES.items():
        results[name] = await check_node(name, url)
    return results

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
DASHBOARD_EOF

    log_success "Dashboard created"
}

# =============================================================================
# Help
# =============================================================================

show_help() {
    echo ""
    echo -e "${CYAN}UFO Galaxy 64-Core MCP Matrix${NC}"
    echo ""
    echo "Usage: ./bootstrap.sh [command] [options]"
    echo ""
    echo "Commands:"
    echo "  install     Install dependencies and setup environment"
    echo "  start       Start the UFO Galaxy system"
    echo "  stop        Stop all services"
    echo "  status      Show system status"
    echo "  logs [svc]  View logs (optionally for specific service)"
    echo "  test        Run tests"
    echo "  dashboard   Start the monitoring dashboard"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./bootstrap.sh install    # First-time setup"
    echo "  ./bootstrap.sh start      # Start all services"
    echo "  ./bootstrap.sh status     # Check system health"
    echo "  ./bootstrap.sh logs       # View all logs"
    echo ""
}

# =============================================================================
# Main
# =============================================================================

main() {
    log_header "UFO Galaxy Bootstrap"
    
    # Detect environment
    detect_os
    detect_container_runtime
    detect_python
    detect_hardware
    detect_android_devices
    
    # Parse command
    local command=${1:-help}
    shift || true
    
    case $command in
        install)
            install_dependencies
            generate_config
            ;;
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        status)
            show_status
            ;;
        logs)
            show_logs "$@"
            ;;
        test)
            run_tests
            ;;
        dashboard)
            start_dashboard
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $command"
            show_help
            exit 1
            ;;
    esac
}

main "$@"
