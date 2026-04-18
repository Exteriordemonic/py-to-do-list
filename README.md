# py-to-do-list

> Multi-user task list built with Django

A small web application for managing personal tasks: create items with optional deadlines and tags, mark them done, search your list, and keep tags organized per account. Each user only sees their own data, so it works well as a learning project or a private to-do board.

## Installing / Getting started

You need **Python 3.10+** (compatible with Django 5.2). From the project root:

```shell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in a browser. Register a normal account at `/accounts/register/`, or sign in as the superuser you created. After login you are redirected to the task list.

**django-select2** (and its supporting packages such as **django-appconf**) are pinned in `requirements.txt`, so a single `pip install -r requirements.txt` is enough for the tag widget and `/select2/` endpoints.

### Initial configuration

- **Database:** SQLite (`db.sqlite3` in the project root) is configured by default—no extra database server is required.
- **Secret key:** `config/settings.py` contains a development `SECRET_KEY`. Before any real deployment, generate a new secret and load it from the environment (for example with `django-environ`), set `DEBUG = False`, and configure `ALLOWED_HOSTS`.
- **Admin:** Django admin is available at `/admin/` for users with staff access.

## Developing

Clone the repository and install dependencies inside a virtual environment:

```shell
git clone https://github.com/exteriordemonic/py-to-do-list.git
cd py-to-do-list
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Apply migrations so the schema matches the models:

```shell
python manage.py migrate
```

Start the development server:

```shell
python manage.py runserver
```

With `DEBUG = True`, the project includes **django-debug-toolbar** (request timing, SQL, etc.) and **django-browser-reload** at `/__reload__/` for automatic page refresh during template and static changes.

### Building

There is no separate compile step. Static files live under `static/`; collect them for production:

```shell
python manage.py collectstatic
```

That copies assets into `STATIC_ROOT` once you define it for deployment (not required for local `runserver` with `STATICFILES_DIRS`).

### Deploying / Publishing

This tree is set up for **local development** (`DEBUG`, insecure defaults). For production, follow [Django’s deployment checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/): environment-based settings, HTTPS, a production WSGI/ASGI server (e.g. Gunicorn + reverse proxy), and a managed database if you outgrow SQLite.

Example outline (commands vary by host):

```shell
export DJANGO_SETTINGS_MODULE=config.settings
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

Replace with your process manager, secrets, and static file serving strategy.

## Features

- **Accounts:** registration, login, logout (`/accounts/…`).
- **Tasks:** create, update, delete; optional deadline (cannot be in the past); ordering shows incomplete items first, then by creation time.
- **Completion:** mark tasks complete or undo completion via POST actions.
- **Tags:** per-user tags with unique name per user; full CRUD under `/tags/`.
- **Tag picker on tasks:** **django-select2** widget—search existing tags or create new ones while editing a task.
- **Search:** filter tasks by text in the content field (`/search/?q=…`).
- **UI:** Bootstrap 5 forms via **django-crispy-forms** and **crispy-bootstrap5**.

## Configuration

Main knobs live in `config/settings.py`:

| Setting | Role |
|--------|------|
| `SECRET_KEY` | Cryptographic signing; must be unique and secret in production. |
| `DEBUG` | Enables toolbar, browser reload, and verbose errors; must be `False` in production. |
| `ALLOWED_HOSTS` | Hostnames the site may serve; required when `DEBUG` is `False`. |
| `DATABASES` | Default SQLite path `BASE_DIR / "db.sqlite3"`. |
| `LANGUAGE_CODE` / `TIME_ZONE` | `en-us` and `Europe/Warsaw` by default. |
| `AUTH_USER_MODEL` | Custom user app: `users.User`. |
| `LOGIN_REDIRECT_URL` | After login: task list (`tasks:index`). |
| `LOGOUT_REDIRECT_URL` | After logout: login page. |
| `INTERNAL_IPS` | Includes `127.0.0.1` for the debug toolbar. |

Environment-specific overrides can use **django-environ** (already in requirements) once you wire a `.env` file in settings.

#### Search query `q`

Type: `string`  
Default: none (empty or missing `q` still renders the search view; behavior depends on template handling of empty results).

Used in: `GET /search/?q=<substring>` — matches task `content` with a case-insensitive contains filter for the logged-in user.

## Contributing

Contributions are welcome. Fork the repository, create a branch for your change, and open a pull request with a short description of what you fixed or added. Keep commits focused; match existing Django and template style. If you add behavior, consider adding tests under `tasks/` or `users/` and run:

```shell
python manage.py test
```

(`pytest` / `pytest-django` are listed in `requirements.txt` for optional use once you add a `pytest.ini` or configure the test runner.)

## Links

- **Repository:** replace with your Git remote, e.g. `https://github.com/exteriordemonic/py-to-do-list/`
- **Issue tracker:** same host, `/issues` on the repository URL
- **Django documentation:** https://docs.djangoproject.com/en/stable/

For security-sensitive reports, contact the maintainer privately instead of filing a public issue.

