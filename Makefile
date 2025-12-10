.PHONY: help test test-models test-views test-forms test-auth test-all test-verbose coverage clean migrate shell runserver docker-test

help:
	@echo "Task Manager - Makefile Commands"
	@echo "=================================="
	@echo ""
	@echo "Testing Commands:"
	@echo "  make test              - Run all tests"
	@echo "  make test-models       - Run model tests only"
	@echo "  make test-views        - Run view tests only"
	@echo "  make test-forms        - Run form tests only"
	@echo "  make test-auth         - Run authentication tests only"
	@echo "  make test-verbose      - Run all tests with verbose output"
	@echo "  make coverage          - Run tests with coverage report"
	@echo "  make coverage-report   - Show coverage report (from last run)"
	@echo "  make coverage-html     - Generate HTML coverage report"
	@echo "  make coverage-xml      - Generate XML coverage report"
	@echo "  make coverage-json     - Generate JSON coverage report"
	@echo "  make coverage-erase    - Clear coverage data"
	@echo ""
	@echo "Development Commands:"
	@echo "  make migrate           - Run database migrations"
	@echo "  make makemigrations    - Create new migrations"
	@echo "  make shell             - Open Django shell"
	@echo "  make runserver         - Run development server"
	@echo "  make createsuperuser   - Create a superuser"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make docker-test       - Run tests in Docker container"
	@echo "  make docker-shell      - Open Django shell in Docker"
	@echo "  make docker-migrate    - Run migrations in Docker"
	@echo ""
	@echo "Utility Commands:"
	@echo "  make clean             - Remove Python cache files"
	@echo "  make requirements      - Install Python dependencies"
	@echo ""

# ========================================
# Testing Commands
# ========================================

test:
	@echo "Running all tests..."
	python manage.py test apps.main_app.test_models apps.main_app.test_views apps.main_app.test_forms apps.authentication.test_authentication --keepdb

test-models:
	@echo "Running model tests..."
	python manage.py test apps.main_app.test_models --keepdb

test-views:
	@echo "Running view tests..."
	python manage.py test apps.main_app.test_views --keepdb

test-forms:
	@echo "Running form tests..."
	python manage.py test apps.main_app.test_forms --keepdb

test-auth:
	@echo "Running authentication tests..."
	python manage.py test apps.authentication.test_authentication --keepdb

test-all:
	@echo "Running all tests (creating fresh database)..."
	python manage.py test apps

test-verbose:
	@echo "Running all tests with verbose output..."
	python manage.py test apps.main_app.test_models apps.main_app.test_views apps.main_app.test_forms apps.authentication.test_authentication --verbosity=2

coverage:
	@echo "Running tests with coverage..."
	@command -v coverage >/dev/null 2>&1 || { echo "Installing coverage..."; pip install coverage; }
	coverage run --source='apps' manage.py test apps.main_app.test_models apps.main_app.test_views apps.main_app.test_forms apps.authentication.test_authentication
	@echo ""
	@echo "Coverage Report:"
	@echo "================"
	coverage report
	@echo ""
	@echo "Generating HTML coverage report..."
	coverage html
	@echo "HTML report generated in htmlcov/index.html"
	@echo ""
	@echo "To view the report, run: open htmlcov/index.html"

coverage-report:
	@echo "Displaying coverage report..."
	coverage report

coverage-html:
	@echo "Generating HTML coverage report..."
	coverage html
	@echo "HTML report generated in htmlcov/index.html"
	@echo "To view: open htmlcov/index.html"

coverage-xml:
	@echo "Generating XML coverage report..."
	coverage xml
	@echo "XML report generated: coverage.xml"

coverage-json:
	@echo "Generating JSON coverage report..."
	coverage json
	@echo "JSON report generated: coverage.json"

coverage-erase:
	@echo "Erasing coverage data..."
	coverage erase
	@echo "Coverage data cleared!"

# ========================================
# Development Commands
# ========================================

migrate:
	@echo "Running migrations..."
	python manage.py migrate

makemigrations:
	@echo "Creating new migrations..."
	python manage.py makemigrations

shell:
	@echo "Opening Django shell..."
	python manage.py shell

runserver:
	@echo "Starting development server..."
	python manage.py runserver

createsuperuser:
	@echo "Creating superuser..."
	python manage.py createsuperuser

# ========================================
# Docker Commands
# ========================================

docker-test:
	@echo "Running tests in Docker container..."
	docker compose exec web python manage.py test apps.main_app.test_models apps.main_app.test_views apps.main_app.test_forms apps.authentication.test_authentication --keepdb

docker-shell:
	@echo "Opening Django shell in Docker..."
	docker compose exec web python manage.py shell

docker-migrate:
	@echo "Running migrations in Docker..."
	docker compose exec web python manage.py migrate

docker-makemigrations:
	@echo "Creating migrations in Docker..."
	docker compose exec web python manage.py makemigrations

docker-coverage:
	@echo "Running tests with coverage in Docker..."
	docker compose exec web bash -c "pip install coverage && coverage run --source='apps' manage.py test apps && coverage report && coverage html"
	@echo ""
	@echo "Copying coverage report from Docker container..."
	docker compose cp web:/app/htmlcov ./htmlcov
	@echo "HTML report available at htmlcov/index.html"

# ========================================
# Utility Commands
# ========================================

clean:
	@echo "Cleaning Python cache files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage coverage.xml coverage.json
	@echo "Clean complete!"

requirements:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

requirements-dev:
	@echo "Installing development dependencies..."
	pip install -r requirements-dev.txt

# ========================================
# Quick Test Shortcuts
# ========================================

# Run specific test class
test-class:
	@read -p "Enter test class path (e.g., apps.main_app.test_models.TaskModelTests): " class; \
	python manage.py test $$class --keepdb

# Run specific test method
test-method:
	@read -p "Enter test method path (e.g., apps.main_app.test_models.TaskModelTests.test_create_task): " method; \
	python manage.py test $$method --keepdb
