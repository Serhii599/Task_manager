# Task Manager

Django-based task and project management app with authentication, projects, tasks, collaboration, and reporting. Includes full test suite, coverage reporting, Docker setup, and CI/CD via CircleCI.

## Features
- User auth (register/login/logout) and role-aware access
- Projects with collaborators and tasks
- Task workflow: priorities, statuses, deadlines, assignees
- My tasks, user tasks, project views, reports (HTML/Excel)
- CRUD for projects and tasks with validations
- Admin panel enabled

## Tech Stack
- Python 3.12, Django 5.x
- PostgreSQL
- Gunicorn + Docker (dev/prod compose files)
- CircleCI pipeline for tests and deployment

## Project Layout (key paths)
- `apps/authentication/` — auth views, forms, models
- `apps/main_app/` — projects, tasks, views, forms, factories, tests
- `config/settings/` — base, docker, prod settings
- `templates/` and `static/` — UI templates and styles
- `docker-compose.yml`, `docker-compose.prod.yml` — dev/prod stacks
- `.circleci/config.yml` — CI/CD pipeline
- `Makefile` — shortcuts for common tasks

## Prerequisites (local)
- Python 3.12
- PostgreSQL running and reachable
- `pip install -r requirements.txt` (and `requirements-dev.txt` for tooling/tests)

## Environment Variables (common)
Set these for local/dev (adapt for prod):
- `DJANGO_SETTINGS_MODULE=config.settings.base` (or `config.settings.docker`/`config.settings.prod`)
- `DB_ENGINE=django.db.backends.postgresql`
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`
- `SECRET_KEY`
- `DEBUG` (True/False)
- `ALLOWED_HOSTS` (comma-separated)

## Quick Start (local)
```bash
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py runserver
```
Visit http://127.0.0.1:8000

## Docker (dev)
```bash
docker compose up --build
```

## Docker (prod-style)
```bash
docker compose -f docker-compose.prod.yml up --build -d
```

## Tests & Coverage
- Run all tests: `make test`
- Run with coverage: `make coverage` then open `htmlcov/index.html`
- Focused suites: `make test-models`, `make test-views`, `make test-forms`, `make test-auth`

## Makefile Cheatsheet (popular)
- `make test`, `make coverage`
- `make migrate`, `make makemigrations`
- `make runserver`, `make shell`, `make createsuperuser`
- `make docker-test`, `make docker-shell`
(See `Makefile` for the full list.)

## CI/CD (CircleCI)
- Workflow: tests (Django + coverage) → deploy (Docker compose on server, main branch)
- Uses PostgreSQL service in CI and `config.settings.base` for test settings

## Useful Paths
- Admin: `/admin/`
- Auth: `/auth/login/`, `/auth/register/`
- Projects: `/projects/`
- Tasks: `/tasks/`

## Notes
- Coverage config: `.coveragerc` (87.97% overall at last run)
- Factories for tests live in `apps/main_app/factories.py`
- Templates and static files are already wired for Django static collection
