# Pocket Galaxy / Backend

## Development Environment

In the development environment, source code is volume-bound and updated in real-time using Django's `runserver`.

If you're setting things up for the first time, just follow the steps below in order.

### Environment Variables

Create a `./.env.dev` and `./.env.prod` file (see `./.env.sample`):

```bash
SECRET_KEY=django_secret_key
PROTOCOL=https
HOST=yourdomain.com
LANGUAGE_CODE=en-us
TIME_ZONE=UTC
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Build Development Image

Only needed for the first time and when packages change.

```bash
./scripts/build.sh
```

### Create Admin User

Only needed like, almost once.

```bash
./scripts/createsuperuser.sh
```

### Create Migrations

Whenever required.

```bash
./scripts/makemigrations.sh
```

### Migrate

Whenever required.

```bash
./scripts/migrate.sh
```

### Collect Static

Whenever required.

```bash
./scripts/collectstatic.sh
```

### Test

Whenever required.

```bash
./scripts/test.sh
```

### Check

Whenever required.

```bash
./scripts/check.sh
```

## Miscellaneous Tasks

Refer to `./script_example.py` and `./script_example.sh` for examples.
A Django-aware script should include the correct paths to the Django project and should be executed within an appropriate Docker environment.

###Logging

See `./project/settings.py`.

We have a `project` logger as project-level logger.

```python
import logging

logger = logging.getLogger('project')
logger.info("log test")
```

### Run Development Server

See the root `/README.md`.

Not that this will run `migrate`, `collecstatic`, `test`, then `runserver` (see `runserver.dev.sh`).

## Production Environment

See the root `/README.md`.
