# Pocket Galaxy

![Luna's Pocket Galaxy](others/concept.png)

**Bang!** And lo, there came forth a *web service boilerplate* endowed with the following features:

* [Django](https://www.djangoproject.com) backend
    * on [PostgreSQL](https://www.postgresql.org/) DBMS
    * and [Redis](https://redis.io/) for cache and [channels](https://channels.readthedocs.io/en/latest/) (for websocket)
    * using [DRF](https://www.django-rest-framework.org) APIs
    * ran through [daphne](https://github.com/django/daphne) ASGI server
        * supporting hot-reload in development
    * with [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) authentication
        * supporting Cookie-based, HttpOnly token verification middleware (`./backend/project/middlewares/cookies.py`)
        * also available for channels (`./backend/project/middlewares/channels.py`)
        * where websockets are authorized via **tickets**, rather than *access tokens*
    * with [Celery](https://docs.celeryq.dev/) and [Flower](https://flower.readthedocs.io/en/latest/) for background tasks
* [Vue](https://vuejs.org/) frontend
    * with [Vuetify](https://vuetifyjs.com) design
    * supporting hot-reload in development via [Vite](https://vite.dev/)
* [nginx](https://nginx.org/) webserver
    * supporting backend, frontend, and websocket, and static/media cache

implementing:

* login
* register
* logout
* forgot password?
    * send reset email
    * reset password
* change email (username)
* change password
* fetch objects via API and bind to data table UI
* real-time chatting
    * via websocket

## Routing

All backend-related stuffs will use reverse proxy of `/api` (via nginx).

In summary, nginx will

* 80 &rightarrow; URL `/static` &rightarrow; docker container path `./shared/staticfiles` (volume bind required)
* 80 &rightarrow; URL `/media` &rightarrow; docker container path `./shared/mediafiles` (volume bind required)
* 80 &rightarrow; URL `/api` &rightarrow; Proxy 8000 (backend daphne)
    * therefore, django admin is located in URL `/api/admin`
* 80 &rightarrow; URL `/` &rightarrow; Serve frontend
    * in case of development, Proxy 5173 (frontend vite)
    * in case of production, Proxy 80 (frontend nginx)

Additionally,

* 5555 &rightarrow; Service flower

## Shared

By default, all logs are stored in `./shared/logfiles` and all DBs are stored in `./shared/dbfiles` (docker container path, thus volume bind required).

Similarly, all redis files are stored in `./shared/redisfiles`.

Django will use `./shared/staticfiles` and `./shared/mediafiles`, which will be served by nginx.

## Setting

See `.env.sample` and create `.env.dev` for development and `.env.prod` for production.

Almost all settings can be managed via this environment files, through passing as environment for docker compose, docker containers, and django stuffs.

```bash
# vue site
VITE_SITE_TITLE=Pocket Galaxy  # used for thte website title

# django site
SITE_TITLE=Pocket Galaxy  # used for email and others
PROTOCOL=http  # for SSL, you should setup by yourself
HOST=localhost  # your domain

# django admin
ADMIN_TITLE=Pocket Galaxy Admin

# django secret
SECRET_KEY=your_django_secret_key

# django locale
LANGUAGE_CODE=en-us
TIME_ZONE=UTC

# django email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_email_app_password  # use gmail app password (not your root password)

# db (for other DBMS, setup yourself)
POSTGRES_HOST=db
POSTGRES_DB=postgres
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_INITDB_ARGS=--encoding=UTF8 --locale=en_US.UTF-8

# redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# cache
CACHE_DB=0  # redis DB id

# celery
C_FORCE_ROOT=1  # TODO: this behavior is not recommended!
CELERY_BROKER_DB=1  # redis DB id
CELERY_RESULT_DB=2  # redis DB id
FLOWER_BASIC_AUTH=admin:your_flower_password  # flower is up in `HOST`:5555

# channel
CHANNEL_DB=3  # redis DB id
```

But for html meta stuffs, you should modify `./frontend/index.html` manually.

## Developement

First, we need a bash function for shorter command:

```bash
dev() {
    docker compose --env-file ./.env.dev --file ./compose/dev.yml "$@"
}
```

Then, do the following first:

```bash
dev up --build --detach
```

This will setup the database if not exists.

Then open your browser and go to `http://localhost/`.

For flower, go to `http://localhost:5555/` (username and password is set on `FLOWER_BASIC_AUTH` in the environment file).

To kill all:

```bash
dev down
```

Note that all celery results will be removed when killed (it's currently on cache).

### Backend

#### Superuser

To create a superuser for django:

```bash
dev run --rm backend python manage.py createsuperuser
```

#### Test

Testing:

```bash
dev run --rm backend ./scripts/test.sh
```

Currently, we have almost *all* possible tests, covering 99% of the source code.

#### Migrations

Whenever the django model changes:

```bash
dev run --rm backend python manage.py makemigrations
```

```bash
dev run --rm backend python manage.py migrate
```

#### Logging

You can use freely `project` logger:

```python
import logging

logger = logging.getLogger('project')
logger.info("test")
```

Then check `./shared/logfiles/django.project.log`.

See `./backend/project/settings.py` for other loggers.

### Frontend

Install packages for local development environment.

```bash
cd ./frontend/
npm install
```

Note that the folder `./frontend/src/` is volume-bound. Since it's in development mode, changes are reflected in real time.

To update packages:

```bash
dev run --rm frontend npm audit fix
```

## Production

Everything is same as development, but you use `prod` instead of `dev`.

```bash
prod() {
    docker compose --env-file ./.env.prod --file ./compose/prod.yml "$@"
}
```

In production, all codes in backend and frontend is `COPY`ed inside the docker image, so changes will not be reflected until the image is rebuilt.
