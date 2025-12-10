# Test Coverage Guide

## Overview

The project uses `coverage.py` to measure test coverage. Current coverage: **87.97%**

## Quick Start

```bash
# Run tests with coverage
make coverage

# View coverage report in terminal
make coverage-report

# Generate HTML report
make coverage-html

# Open HTML report in browser
open htmlcov/index.html
```

## Coverage Configuration

Coverage is configured via `.coveragerc` file with the following settings:

### What's Included
- All files in `apps/` directory
- Branch coverage enabled
- Detailed missing line reports

### What's Excluded
- Migration files (`*/migrations/*`)
- Test files (`test_*.py`, `tests.py`)
- Cache directories (`__pycache__`)
- Virtual environments
- Configuration files (`settings/`, `wsgi.py`, `asgi.py`)
- `manage.py`

## Current Coverage Report

```
Name                            Stmts   Miss Branch BrPart   Cover   Missing
----------------------------------------------------------------------------
apps/authentication/admin.py        7      0      0      0 100.00%
apps/authentication/apps.py         4      0      0      0 100.00%
apps/authentication/forms.py       11      0      0      0 100.00%
apps/authentication/models.py      14      0      0      0 100.00%
apps/authentication/urls.py         4      0      0      0 100.00%
apps/authentication/views.py       27      0      0      0 100.00%
apps/main_app/admin.py              6      0      0      0 100.00%
apps/main_app/apps.py               4      0      0      0 100.00%
apps/main_app/factories.py        107      4     22      0  96.90%
apps/main_app/forms.py             24      0      0      0 100.00%
apps/main_app/models.py            40      0      0      0 100.00%
apps/main_app/urls.py               4      0      0      0 100.00%
apps/main_app/views.py            176     34     32      4  74.04%
----------------------------------------------------------------------------
TOTAL                             428     38     54      4  87.97%
```

### Coverage Breakdown

| Component | Coverage | Status |
|-----------|----------|--------|
| **Authentication** | 100% | ✅ Complete |
| **Admin** | 100% | ✅ Complete |
| **Models** | 100% | ✅ Complete |
| **Forms** | 100% | ✅ Complete |
| **URLs** | 100% | ✅ Complete |
| **Factories** | 96.90% | ✅ Excellent |
| **Views** | 74.04% | ⚠️ Good (some views not fully tested) |
| **TOTAL** | **87.97%** | ✅ **Excellent** |

## Available Commands

### Basic Coverage Commands

```bash
# Run tests and generate coverage
make coverage

# Show coverage report from last run
make coverage-report

# Generate HTML report
make coverage-html

# Generate XML report (for CI/CD)
make coverage-xml

# Generate JSON report
make coverage-json

# Clear coverage data
make coverage-erase
```

### Docker Coverage Commands

```bash
# Run coverage in Docker container
make docker-coverage
```

## Understanding Coverage Reports

### Terminal Report

The terminal report shows:
- **Stmts**: Total statements
- **Miss**: Statements not executed
- **Branch**: Total branches
- **BrPart**: Partially covered branches
- **Cover**: Coverage percentage
- **Missing**: Line numbers not covered

### HTML Report

The HTML report (`htmlcov/index.html`) provides:
- **Interactive file browser**
- **Line-by-line coverage highlighting**
  - Green: Covered
  - Red: Not covered
  - Yellow: Partially covered branches
- **Detailed statistics per file**
- **Sortable columns**

#### Viewing HTML Report

```bash
# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html

# Windows
start htmlcov/index.html

# Or use make command
make coverage-html && open htmlcov/index.html
```

## Improving Coverage

### Areas Needing Improvement

Based on current report, these views have lower coverage:

#### `apps/main_app/views.py` (74.04%)

Missing coverage on lines:
- Lines 38, 97, 101: Edge case handling
- Lines 116-148: Excel export view (ProjectReportExcelView)
- Lines 183, 231-240, 244-256: Search and comment views

**How to improve:**
```python
# Add tests for Excel export
def test_project_report_excel_download(self):
    response = self.client.get(
        reverse('main_app:project_report_excel', 
        kwargs={'project_id': self.project.id})
    )
    self.assertEqual(response.status_code, 200)
    self.assertEqual(
        response['Content-Type'],
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

# Add tests for search functionality
def test_search_with_query(self):
    response = self.client.get(reverse('main_app:search'), {'q': 'test'})
    self.assertEqual(response.status_code, 200)
    self.assertIn('query', response.context)
```

#### `apps/main_app/factories.py` (96.90%)

Missing coverage on lines 98-101 (minor, factory-specific code).

## Coverage Best Practices

### 1. Run Coverage Regularly

```bash
# During development
make test-models
make coverage

# Before committing
make test
make coverage
```

### 2. Target Critical Code First

Priority for coverage:
1. ✅ Models - 100%
2. ✅ Forms - 100%
3. ⚠️ Views - 74% (add more integration tests)
4. ✅ Authentication - 100%

### 3. Don't Aim for 100% Blindly

Some code doesn't need coverage:
- Debug/development utilities
- Abstract methods
- Defensive assertions
- Type checking blocks

These are excluded in `.coveragerc`:
```ini
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    if __name__ == .__main__.:
```

### 4. Use Branch Coverage

Branch coverage ensures all code paths are tested:
```python
# This function has 2 branches
def process_task(task, user):
    if task.assignee == user:  # Branch 1
        return True
    else:  # Branch 2
        return False

# Test should cover both branches
def test_process_task_as_assignee(self):
    # Tests branch 1
    ...

def test_process_task_not_assignee(self):
    # Tests branch 2
    ...
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install coverage
      
      - name: Run tests with coverage
        run: make coverage
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v2
        with:
          file: ./coverage.xml
```

### GitLab CI Example

```yaml
test:
  script:
    - pip install -r requirements.txt
    - pip install coverage
    - make coverage
    - make coverage-xml
  coverage: '/TOTAL.*\s+(\d+%)$/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
```

## Troubleshooting

### Coverage Not Found

```bash
# Install coverage
pip install coverage

# Or use requirements
make requirements-dev
```

### Old Coverage Data

```bash
# Clear old data
make coverage-erase

# Run fresh coverage
make coverage
```

### HTML Report Not Generating

```bash
# Ensure coverage ran successfully first
make coverage

# Then generate HTML
make coverage-html
```

### Docker Coverage Issues

```bash
# Ensure Docker containers are running
docker compose up -d

# Run coverage in Docker
make docker-coverage
```

## Coverage Targets

### Current Status: 87.97% ✅

**Excellent!** Industry standards:
- 80%+ : Excellent
- 70-80%: Good
- 60-70%: Acceptable
- <60%: Needs improvement

### Recommended Targets

| Component | Current | Target |
|-----------|---------|--------|
| Models | 100% | 100% ✅ |
| Forms | 100% | 100% ✅ |
| Views | 74% | 85% 📈 |
| Authentication | 100% | 100% ✅ |
| **Overall** | **88%** | **90%** 📈 |

## Report Types

### 1. Terminal Report (Default)
```bash
make coverage-report
```
Quick overview in terminal.

### 2. HTML Report (Interactive)
```bash
make coverage-html
open htmlcov/index.html
```
Best for detailed analysis.

### 3. XML Report (CI/CD)
```bash
make coverage-xml
```
For continuous integration systems.

### 4. JSON Report (Programmatic)
```bash
make coverage-json
```
For custom tooling and scripts.

## Advanced Usage

### Focus on Specific Module

```bash
coverage run --source='apps/main_app' manage.py test
coverage report --include='apps/main_app/views.py'
```

### Show Missing Branches

```bash
coverage report --show-missing
```

### Fail if Coverage Below Threshold

```bash
coverage report --fail-under=85
```

Add to CI/CD:
```bash
make coverage
coverage report --fail-under=85 || exit 1
```

## Summary

✅ **Coverage configured and working**
✅ **87.97% overall coverage**
✅ **HTML reports generated**
✅ **Multiple report formats available**
✅ **CI/CD ready**

**Next steps to reach 90%:**
1. Add tests for Excel export view
2. Add tests for search functionality
3. Add tests for comment views (if not on main branch)

Run `make coverage` regularly to monitor your test coverage!
