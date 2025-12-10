# Task Manager - Testing Documentation

## Overview

This project includes comprehensive unit tests for all major components:
- **Models**: Tests for User, Project, Task models and their relationships
- **Views**: Tests for all views including list, detail, create, update, delete operations
- **Forms**: Tests for TaskCreationForm and ProjectCreationForm
- **Authentication**: Tests for user registration, login, logout, and permissions
- **Factories**: Helper functions for generating test data

## Quick Start

### Running All Tests

```bash
make test
```

### Running Specific Test Suites

```bash
# Model tests only
make test-models

# View tests only
make test-views

# Form tests only
make test-forms

# Authentication tests only
make test-auth
```

### Running Tests with Coverage

```bash
make coverage
```

This will generate a coverage report in the terminal and an HTML report in `htmlcov/index.html`.

## Test Organization

### Test Files

- `apps/main_app/test_models.py` - Model tests (70+ tests)
- `apps/main_app/test_views.py` - View tests (50+ tests)
- `apps/main_app/test_forms.py` - Form tests (20+ tests)
- `apps/authentication/test_authentication.py` - Auth tests (25+ tests)
- `apps/main_app/factories.py` - Test data factories

### Factory Classes

The `factories.py` file provides convenient functions for creating test data:

```python
from apps.main_app.factories import UserFactory, TaskFactory, ProjectFactory, DataSetFactory

# Create a single user
user = UserFactory.create_user(email="test@example.com")

# Create multiple users
users = UserFactory.create_users(count=5)

# Create a task
task = TaskFactory.create_task(creator=user, assignee=user)

# Create an overdue task
overdue_task = TaskFactory.create_overdue_task(creator=user)

# Create a complete dataset
dataset = DataSetFactory.create_full_dataset()
# Returns: {'creator', 'users', 'projects', 'tasks', 'overdue_task', 'urgent_task', 'completed_task'}

# Create a project with full data
data = DataSetFactory.create_project_with_full_data(creator=user)
# Returns: {'project', 'creator', 'collaborators', 'tasks', 'overdue_task', 'completed_task'}
```

## Test Categories

### Model Tests (`test_models.py`)

Tests cover:
- User model creation and authentication
- Project model CRUD operations
- Task model CRUD operations
- Many-to-many relationships (collaborators, project tasks)
- Model signals (task count updates)
- Status and priority choices
- String representations

**Example:**
```bash
# Run all model tests
make test-models

# Run specific test class
python manage.py test apps.main_app.test_models.TaskModelTests --keepdb

# Run specific test
python manage.py test apps.main_app.test_models.TaskModelTests.test_create_task --keepdb
```

### View Tests (`test_views.py`)

Tests cover:
- Authentication requirements (LoginRequiredMixin)
- List views (MyTasksListView, ProjectsListView, etc.)
- Detail views (OneTaskDetailView, OneProjectListView)
- Create views (TaskCreateView, ProjectCreateView)
- Update views (TaskUpdateView, ProjectUpdateView)
- Delete views (TaskDeleteView, ProjectDeleteView)
- Filtering and sorting functionality
- Context data correctness

**Example:**
```bash
# Run all view tests
make test-views

# Run specific view test class
python manage.py test apps.main_app.test_views.MyTasksListViewTests --keepdb
```

### Form Tests (`test_forms.py`)

Tests cover:
- Form field validation
- Required fields
- Field widgets and attributes
- Form saving functionality
- Many-to-many field handling (collaborators, tasks)
- Edge cases (max length, empty values)

**Example:**
```bash
# Run all form tests
make test-forms
```

### Authentication Tests (`test_authentication.py`)

Tests cover:
- User registration
- User login/logout
- Password validation
- Email uniqueness
- Custom user creation form
- User model authentication features
- Permission requirements

**Example:**
```bash
# Run all authentication tests
make test-auth
```

## Docker Testing

If you're running the project in Docker:

```bash
# Run all tests in Docker
make docker-test

# Run tests with coverage in Docker
make docker-coverage

# Run migrations in Docker
make docker-migrate

# Open Django shell in Docker
make docker-shell
```

## Advanced Usage

### Running Tests with Verbose Output

```bash
make test-verbose
```

### Running Tests Without Keepdb

By default, tests use `--keepdb` to speed up subsequent test runs. To force a fresh database:

```bash
make test-all
```

### Running Specific Test Class

```bash
python manage.py test apps.main_app.test_models.ProjectModelTests --keepdb
```

### Running Specific Test Method

```bash
python manage.py test apps.main_app.test_models.ProjectModelTests.test_create_project --keepdb
```

### Interactive Test Selection

```bash
# Will prompt for test class path
make test-class

# Will prompt for test method path
make test-method
```

## Coverage Reports

After running `make coverage`, you can:

1. View terminal output for a quick overview
2. Open `htmlcov/index.html` in your browser for detailed line-by-line coverage
3. Identify untested code paths

Coverage report includes:
- Statement coverage percentage
- Missing lines
- Branch coverage
- Per-file coverage details

## Writing New Tests

### Example Test Structure

```python
from django.test import TestCase
from apps.main_app.factories import UserFactory, TaskFactory

class MyNewTests(TestCase):
    """Tests for new feature"""
    
    def setUp(self):
        """Run before each test"""
        self.user = UserFactory.create_user()
        self.task = TaskFactory.create_task(creator=self.user)
    
    def test_something(self):
        """Test description"""
        # Arrange
        # ... setup test data
        
        # Act
        # ... perform action
        
        # Assert
        self.assertEqual(expected, actual)
```

### Best Practices

1. **Use factories** instead of manually creating objects
2. **Test one thing** per test method
3. **Use descriptive names** for test methods
4. **Keep tests isolated** - don't depend on other tests
5. **Use setUp/tearDown** for common test setup
6. **Test edge cases** and error conditions
7. **Use --keepdb** during development for faster test runs

## Continuous Integration

Tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run tests
  run: make test

- name: Generate coverage
  run: make coverage
```

## Troubleshooting

### Tests are slow
- Use `--keepdb` flag (already included in Makefile commands)
- Run specific test suites instead of all tests
- Use SQLite for testing (faster than PostgreSQL)

### Import errors
- Ensure all dependencies are installed: `make requirements`
- Check that apps are in `INSTALLED_APPS`
- Verify correct Python path

### Database errors
- Run migrations: `make migrate`
- Try without `--keepdb`: `make test-all`
- Reset database if needed

## Test Statistics

Current test coverage:
- **Total Tests**: 165+
- **Model Tests**: 70+
- **View Tests**: 50+
- **Form Tests**: 20+
- **Authentication Tests**: 25+

## Additional Resources

- Django Testing Documentation: https://docs.djangoproject.com/en/stable/topics/testing/
- Python unittest: https://docs.python.org/3/library/unittest.html
- Coverage.py: https://coverage.readthedocs.io/
