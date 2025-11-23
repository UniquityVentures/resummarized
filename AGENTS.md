# AGENTS.md

This document outlines essential information for agents working on the `resummarized_django` codebase.

## Project Type
This is a Python Django project with a TailwindCSS frontend. It is designed for Dockerized deployment.

## Essential Commands

### Python/Django Commands (using `uv`)
*   **Install Dependencies**: `uv sync`
*   **Run Development Server**: `uv run manage.py runserver`
*   **Create Migrations**: `uv run manage.py makemigrations <app_name>`
*   **Apply Migrations**: `uv run manage.py migrate`
*   **Run Tests**: `uv run manage.py test`
*   **Collect Static Files**: `uv run manage.py collectstatic --noinput`
*   **TailwindCSS Install (Django Integration)**: `uv run manage.py tailwind install`
*   **TailwindCSS Build (Django Integration)**: `uv run manage.py tailwind build`
*   **TailwindCSS Start (Development)**: `uv run manage.py tailwind start`
*   **Start Celery Worker**: `uv run celery -A resummarized_django worker`

### Frontend (TailwindCSS) Commands (using `npm` in `theme/static_src/`)
*   **Install Node.js Dependencies**: `npm install` (run in `theme/static_src/` directory)
*   **Develop (Watch for changes)**: `npm run dev` (run in `theme/static_src/` directory)
*   **Build for Production**: `npm run build` (run in `theme/static_src/` directory)
*   **Clean Build Output**: `npm run build:clean` (run in `theme/static_src/` directory)
*   **Build TailwindCSS**: `npm run build:tailwind` (run in `theme/static_src/` directory)

### Docker Commands
*   **Build Docker Image**: `./build_docker.sh` (uses the `Dockerfile`)
    *   Alternatively: `docker build . --file Dockerfile -o local --tag resummarized:$(date +%s)`
*   **Run Docker Container (Example)**: `docker run -p 8080:8080 resummarized:<tag>`

## Code Organization and Structure

*   **Django Project Root**: `resummarized_django/` contains the core Django project settings (`settings.py`), URL configurations (`urls.py`), Celery setup (`celery.py`), and main `views.py`.
*   **Django Applications**:
    *   `articles/`: Manages article-related functionality.
    *   `users/`: Handles user authentication and profiles.
    *   Each app generally follows the standard Django structure with `models.py`, `views.py`, `urls.py`, `admin.py`, `templates/`, `migrations/`, and `components/`.
*   **Django Components**: The project extensively uses `django-components`.
    *   Global components are in the `components/` directory at the project root.
    *   App-specific components are located within `app_name/components/` (e.g., `articles/components/`).
    *   Each component typically consists of a Python file (e.g., `card.py`) and an associated HTML template (e.g., `card.html`).
*   **Templates**:
    *   Global base templates: `resummarized_django/templates/`.
    *   App-specific templates: `app_name/templates/`.
*   **Static Files**:
    *   `theme/static_src/`: Contains raw source files for TailwindCSS (e.g., `src/styles.css`) and Node.js `package.json` for frontend build tools.
    *   `theme/static/css/dist/styles.css`: Compiled TailwindCSS output.
    *   `theme/static/js/`: Project-specific JavaScript files.

## Naming Conventions and Style Patterns

*   **Python**: Adheres to PEP 8 guidelines for code style.
*   **Django**: Follows standard Django project and application structuring.
*   **HTML Templates**: Django templates utilize `django-components` with `{% load component_tags %}` and `{% component "component_name" %}` syntax.
*   **TailwindCSS**: Employs a utility-first CSS approach directly in HTML templates or via `@apply` in `src/styles.css`.

## Testing Approach and Patterns

*   **Django's Built-in Testing**: Tests for Django applications are located in `app_name/tests.py` files (e.g., `articles/tests.py`, `users/tests.py`).
*   Agents should use `uv run manage.py test` to execute tests.

## Important Gotchas or Non-Obvious Patterns

*   **Python Environment Management**: The project exclusively uses `uv` for managing Python dependencies and running Python commands. **Do not use `pip` or `python` directly for package installation or script execution.** Always use `uv sync` for installing dependencies and `uv run <command>` for running Python-related commands.
*   **TailwindCSS Workflow**: TailwindCSS styling requires a build step.
    *   For local development with live reloading, `uv run manage.py tailwind start` or `npm run dev` (in `theme/static_src/`) should be used.
    *   For production builds, `uv run manage.py tailwind build` or `npm run build` (in `theme/static_src/`) is necessary.
*   **Docker Entrypoint**: The `entrypoint.sh` script in the root directory is responsible for starting both the Celery worker and the Django development server when the Docker container launches. In a production environment, `manage.py runserver` would typically be replaced by a production-ready WSGI server like Gunicorn.
*   **Celery Background Tasks**: Tasks that need to run in the background are handled by Celery. Ensure the Celery worker is running (`uv run celery -A resummarized_django worker`) if working with background tasks locally.
