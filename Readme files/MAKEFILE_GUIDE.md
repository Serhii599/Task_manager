# Task Manager - Makefile Quick Reference

## Available Commands

### Help
```bash
make help
# Shows all available commands with descriptions
```

## Testing Commands

### Run All Tests
```bash
make test
# Runs all test suites (models, views, forms, authentication)
# Uses --keepdb for faster execution
```

### Run Specific Test Suites
```bash
make test-models      # Run only model tests
make test-views       # Run only view tests  
make test-forms       # Run only form tests
make test-auth        # Run only authentication tests
```

### Advanced Testing
```bash
make test-all         # Run all tests with fresh database
make test-verbose     # Run tests with detailed output (verbosity=2)
make coverage         # Run tests and generate coverage report
```

## Development Commands

### Database
```bash
make migrate              # Apply database migrations
make makemigrations       # Create new migrations
```

### Development Server
```bash
make runserver            # Start Django development server
make shell                # Open Django interactive shell
make createsuperuser      # Create admin user
```

## Docker Commands

All testing and development commands have Docker equivalents:

```bash
make docker-test              # Run tests in Docker container
make docker-migrate           # Run migrations in Docker
make docker-makemigrations    # Create migrations in Docker
make docker-shell             # Open Django shell in Docker
make docker-coverage          # Run coverage in Docker
```

## Utility Commands

```bash
make clean                # Remove Python cache files (__pycache__, *.pyc)
make requirements         # Install Python dependencies
make requirements-dev     # Install development dependencies
```

## Common Workflows

### Starting Development
```bash
make migrate              # Setup database
make runserver            # Start server
```

### Running Tests During Development
```bash
make test                 # Quick test run
make test-models          # Test specific area you're working on
```

### Before Committing Code
```bash
make test                 # Ensure all tests pass
make coverage             # Check code coverage
make clean                # Clean up cache files
```

### Testing in Docker
```bash
docker compose up -d      # Start containers
make docker-test          # Run tests in container
make docker-shell         # Debug in Django shell
```

## Examples

### Test Specific Class
```bash
python manage.py test apps.main_app.test_models.TaskModelTests --keepdb
```

### Test Specific Method
```bash
python manage.py test apps.main_app.test_models.TaskModelTests.test_create_task --keepdb
```

### View Coverage Report
```bash
make coverage
# Opens coverage report in htmlcov/index.html
```

## Tips

1. **Use --keepdb**: All Makefile test commands include `--keepdb` by default for faster test runs
2. **Test small**: Run `make test-models` or similar when working on specific areas
3. **Coverage regularly**: Run `make coverage` to identify untested code
4. **Clean before deploy**: Run `make clean` to remove development artifacts
5. **Docker for CI/CD**: Use `docker-test` commands in CI/CD pipelines

## Troubleshooting

### Tests failing after model changes
```bash
make makemigrations
make migrate
make test-all  # Fresh database
```

### Slow tests
```bash
# Run specific suite instead of all
make test-models
# Or use Docker
make docker-test
```

### Import errors
```bash
make requirements  # Reinstall dependencies
make clean         # Clear cache
```

## Test Statistics

Current test count:
- Model tests: 70+
- View tests: 50+
- Form tests: 20+
- Authentication tests: 25+
- **Total: 165+ tests**

## Additional Documentation

See `TESTING.md` for comprehensive testing documentation including:
- Detailed test descriptions
- How to write new tests
- Factory usage examples
- Coverage interpretation
- Best practices
