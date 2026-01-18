# =============================================================================
# UFO Galaxy 64-Core MCP Matrix - Makefile
# =============================================================================

.PHONY: all install start stop status logs test dashboard build clean help

# Default target
all: help

# Install to system
install:
	@./install.sh

# Start all services
start:
	@./bootstrap.sh start

# Stop all services
stop:
	@./bootstrap.sh stop

# Show status
status:
	@./bootstrap.sh status

# View logs
logs:
	@./bootstrap.sh logs

# Run tests
test:
	@./bootstrap.sh test

# Start dashboard
dashboard:
	@./bootstrap.sh dashboard

# Build/rebuild containers
build:
	@podman-compose build

# Build without cache
rebuild:
	@podman-compose build --no-cache

# Clean up
clean:
	@podman-compose down --rmi local
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Deep clean (removes volumes too)
clean-all: clean
	@podman-compose down -v --rmi all

# Run local tests (no containers)
test-local:
	@python3 tests/local_verify.py
	@python3 tests/test_phase2.py

# Show help
help:
	@echo ""
	@echo "UFO Galaxy 64-Core MCP Matrix"
	@echo "=============================="
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  install    - Install to /opt/ufo-galaxy"
	@echo "  start      - Start all services"
	@echo "  stop       - Stop all services"
	@echo "  status     - Show service status"
	@echo "  logs       - View logs"
	@echo "  test       - Run all tests"
	@echo "  test-local - Run local tests (no containers)"
	@echo "  dashboard  - Start monitoring dashboard"
	@echo "  build      - Build containers"
	@echo "  rebuild    - Rebuild containers (no cache)"
	@echo "  clean      - Remove containers and images"
	@echo "  clean-all  - Remove everything including volumes"
	@echo "  help       - Show this help"
	@echo ""
