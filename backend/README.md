# Pocket Galaxy / Backend

All volume bindings are located under `backend/shared/` by default:

```bash
backend/
    ...
    shared/
        staticfiles/
        mediafiles/
        logfiles/
        dbfiles/
    ...
```

The default DBMS used is SQLite3.

## Environment Variables (Required)

Example of a `.env` file (place it under `backend/`):

```bash
WEB_PORT=8001
DJANGO_SECRET_KEY=django_secret_key123
ALLOWED_HOSTS=localhost,your.domain.com
```

With this configuration, the specified `WEB_PORT` becomes the main entry point.

## Development Environment

In the development environment, source code is volume-bound and updated in real-time using Django's `runserver`.

Both static and media files are served directly by the app.

If you're setting things up for the first time, just follow the steps below in order.

### Development Build

```bash
docker-compose --project-directory . -f compose/dev.yml build
```

### Create Migrations

```bash
docker-compose --project-directory . -f compose/dev.yml run --rm app_dev python manage.py makemigrations
```

### Apply Migrations

```bash
docker-compose --project-directory . -f compose/dev.yml run --rm app_dev python manage.py migrate
```

### Create Admin User

```bash
docker-compose --project-directory . -f compose/dev.yml run --rm app_dev python manage.py createsuperuser
```

### Run Development Server

```bash
docker-compose --project-directory . -f compose/dev.yml up --build
```

## Production Environment

This project does not assume a production environment by default, but support is provided for long-running deployments or when you want to set `DEBUG=False`.

In production, the source code is baked into the Docker image and runs relatively stably. NGINX is used for serving.

### Production Build

```bash
docker-compose --project-directory . -f compose/prod.yml build
```

### Run in Production

```bash
docker-compose --project-directory . -f compose/prod.yml up -d --build
```

## Miscellaneous Tasks

Example usage of `script_example.py`. See `run_example.sh` for reference.

Note: If you use `tqdm`, it won't display properly when running via `docker-compose`.

```bash
x () {
    docker run \
        -it \
        --rm \
        --init \
        --env-file .env \
        -v "${PWD}/shared:/shared" \
        -v "${PWD}:/app" \
        pocket-galaxy-back-dev \
        "$@"
}

x python script_example.py
```
