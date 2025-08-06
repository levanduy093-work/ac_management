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
	@echo "  run-monitor  - Run the multi-sensor monitor (CSV storage)"
	@echo "  run-monitor-db - Run the multi-sensor monitor (Database storage)"
	@echo "  run-reset    - Run the energy reset tool"
	@echo "  db-stats     - Show database statistics"
	@echo "  db-sensors   - Show sensor summary"
	@echo "  db-latest    - Show latest 20 measurements"
	@echo "  db-cleanup   - Clean up old data (30 days)"
	@echo "  migrate-csv  - Migrate CSV data to database"
	@echo "  migrate-csv-dry - Dry run CSV migration"
	@echo "  db-gui       - Interactive database GUI tool"

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

# Run the multi-sensor monitor (CSV storage)
run-monitor:
	python tools/read_ac_sensor.py

# Run the multi-sensor monitor (Database storage)
run-monitor-db:
	python tools/read_ac_sensor_db.py

# Run the energy reset tool (AN TOÀN - KHÔNG thay đổi địa chỉ)
run-reset:
	python tools/reset_energy_no_address_change.py

# Database operations
db-stats:
	python tools/query_database.py --stats

db-sensors:
	python tools/query_database.py --sensors

db-latest:
	python tools/query_database.py --latest 20

db-cleanup:
	python tools/query_database.py --cleanup 30

# Migration
migrate-csv:
	python tools/migrate_csv_to_db.py

migrate-csv-dry:
	python tools/migrate_csv_to_db.py --dry-run

# GUI Tools
db-gui:
	python tools/database_gui.py

# Quick start
quick-start: install
	@echo "Installation complete!"
	@echo "Run 'make run-monitor' to start monitoring (CSV storage)"
	@echo "Run 'make run-monitor-db' to start monitoring (Database storage)"
	@echo "Run 'make run-reset' to reset energy counters" 