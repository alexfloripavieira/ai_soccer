# Repository Guidelines

## Project Structure & Module Organization
- `core/`: Global settings, URLs, base templates.
- `accounts/`, `performance/`, `scouting/`, `business/`: Django apps by domain.
- `docs/`: Full documentation (architecture, coding, setup).
- `manage.py`: Django management entrypoint.
- Common assets: `templates/` and `static/` (as introduced per feature).

## Build, Test, and Development Commands
- Create/activate venv:
  - Linux/macOS: `python -m venv .venv && source .venv/bin/activate`
  - Windows: `python -m venv .venv && .venv\\Scripts\\activate`
- Install deps: `pip install -r requirements.txt`
- Migrations: `python manage.py makemigrations && python manage.py migrate`
- Run local server: `python manage.py runserver`
- Create admin: `python manage.py createsuperuser`
- Collect static (when needed): `python manage.py collectstatic`

## Coding Style & Naming Conventions
- Python: PEP 8, 4-space indent, single quotes preferred.
- Code in English (variables, classes, functions); UI strings in pt-BR.
- Views: prefer CBV; Models include `created_at`/`updated_at` fields.
- Imports grouped and ordered; avoid commented-out code.
- See `docs/coding-guidelines.md` for detailed patterns.

## Testing Guidelines
- Framework: Django `TestCase` via `manage.py test`.
- Naming: files `test_*.py`; classes `Test*`; methods `test_*`.
- Scope: unit tests per app under `app/tests/` or `app/tests/test_*.py`.
- Run all: `python manage.py test`; run one: `python manage.py test accounts.tests.test_auth`

## Commit & Pull Request Guidelines
- Conventional commits: `tipo(escopo): mensagem`.
  - tipos: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
  - Ex: `feat(performance): add athlete model`.
- PRs must include:
  - Clear description and rationale; reference issues (e.g., `Closes #12`).
  - Screenshots/GIFs for UI changes.
  - Migration files when models change.
  - Checklist: lint/style, tests added/updated, docs touched when relevant.

## Security & Configuration Tips
- Never commit secrets. Use env vars via Django settings patterns in `core/`.
- Use separate settings per environment when introduced; default DB is SQLite for dev.

For broader context and decisions, start at `docs/README.md` and `PRD.md`.
