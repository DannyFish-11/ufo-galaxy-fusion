#!/bin/bash

# UFO Galaxy 70-Core Matrix - Smart Bootstrap Script
# Version: 3.2 (One-Click Optimized & Aligned)

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}=== UFO Galaxy 70-Core Matrix Bootstrap ===${NC}"

# 1. Environment Check
echo -e "${YELLOW}[1/4] Checking Environment...${NC}"
if command -v podman-compose &> /dev/null; then
    COMPOSE_CMD="podman-compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}Error: Neither podman-compose nor docker-compose found.${NC}"
    exit 1
fi
echo -e "Using: $COMPOSE_CMD"

# 2. Configuration Initialization
echo -e "${YELLOW}[2/4] Initializing Configuration...${NC}"
if [ ! -f config/.env ]; then
    if [ -f config/.env.example ]; then
        cp config/.env.example config/.env
        echo -e "Created config/.env from example."
    else
        touch config/.env
        echo -e "Created empty config/.env."
    fi
fi

# 3. Network & Volume Setup
echo -e "${YELLOW}[3/4] Preparing Resources...${NC}"
mkdir -p data/redis data/qdrant data/sqlite data/logs data/backups

# 4. Launch System
echo -e "${YELLOW}[4/4] Launching 70-Node Matrix...${NC}"
case "$1" in
    start)
        $COMPOSE_CMD up -d
        echo -e "${GREEN}System started in background.${NC}"
        ;;
    stop)
        $COMPOSE_CMD down
        echo -e "${YELLOW}System stopped.${NC}"
        ;;
    restart)
        $COMPOSE_CMD restart
        echo -e "${GREEN}System restarted.${NC}"
        ;;
    status)
        $COMPOSE_CMD ps
        ;;
    logs)
        $COMPOSE_CMD logs -f
        ;;
    test)
        python3 tests/test_all_nodes.py
        ;;
    dashboard)
        echo -e "${BLUE}Starting Dashboard on http://localhost:8080...${NC}"
        python3 dashboard/app.py
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|test|dashboard}"
        exit 1
        ;;
esac

echo -e "${GREEN}=== Operation Complete ===${NC}"
