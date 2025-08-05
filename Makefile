# Makefile for PZEM-004T Power Monitoring Project

.PHONY: help install install-dev test clean lint format docs run-monitor run-reset

# Default target
help:
	@echo "PZEM-004T Power Monitoring Project"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install dependencies"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean build artifacts"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code with black"
	@echo "  docs         - Generate documentation"
	@echo "  run-monitor  - Run the multi-sensor monitor"
	@echo "  run-reset    - Run the energy reset tool"

# Install dependencies
install:
	pip install -r requirements.txt

# Install with development dependencies
install-dev:
	pip install -r requirements.txt
	pip install flake8 pylint black pytest

# Run tests
test:
	@echo "No tests configured yet. Use 'make run-monitor' to test the system."

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Run linting
lint:
	@echo "Linting source code..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ tools/; \
	else \
		echo "flake8 not installed. Run 'make install-dev' first."; \
	fi
	@if command -v pylint >/dev/null 2>&1; then \
		pylint src/ tools/; \
	else \
		echo "pylint not installed. Run 'make install-dev' first."; \
	fi

# Format code
format:
	@echo "Formatting code..."
	@if command -v black >/dev/null 2>&1; then \
		black src/ tools/; \
	else \
		echo "black not installed. Run 'make install-dev' first."; \
	fi

# Generate documentation
docs:
	@echo "Documentation is in docs/ directory"
	@echo "- docs/PZEM004T.md: Library documentation"
	@echo "- docs/DATA_LOGGING.md: Data logging guide"
	@echo "- README.md: Main documentation"

# Run the multi-sensor monitor
run-monitor:
	python tools/read_ac_sensor.py

# Run the energy reset tool
run-reset:
	python tools/reset_energy.py

# Quick start
quick-start: install
	@echo "Installation complete!"
	@echo "Run 'make run-monitor' to start monitoring"
	@echo "Run 'make run-reset' to reset energy counters" 