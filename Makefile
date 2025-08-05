# Makefile for PZEM-004T Power Monitoring Project

.PHONY: help install install-dev test clean lint format docs run-monitor run-reset run-example

# Default target
help:
	@echo "PZEM-004T Power Monitoring Project"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install      - Install the library and dependencies"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  test         - Run tests"
	@echo "  clean        - Clean build artifacts"
	@echo "  lint         - Run linting"
	@echo "  format       - Format code with black"
	@echo "  docs         - Generate documentation"
	@echo "  run-monitor  - Run the multi-sensor monitor"
	@echo "  run-reset    - Run the energy reset tool"
	@echo "  run-example  - Run the example usage script"

# Install the library
install:
	pip install -e .

# Install with development dependencies
install-dev:
	pip install -e .[dev]

# Run tests
test:
	python -m pytest tests/ -v

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Run linting
lint:
	flake8 src/ tools/ examples/
	pylint src/ tools/ examples/

# Format code
format:
	black src/ tools/ examples/

# Generate documentation
docs:
	@echo "Documentation is in docs/ directory"
	@echo "- PZEM004T.md: Library documentation"
	@echo "- DATA_LOGGING.md: Data logging guide"

# Run the multi-sensor monitor
run-monitor:
	python tools/read_ac_sensor.py

# Run the energy reset tool
run-reset:
	python tools/reset_energy.py

# Run the example usage script
run-example:
	python examples/example_usage.py

# Quick start
quick-start: install
	@echo "Installation complete!"
	@echo "Run 'make run-example' to see examples"
	@echo "Run 'make run-monitor' to start monitoring"
	@echo "Run 'make run-reset' to reset energy counters" 