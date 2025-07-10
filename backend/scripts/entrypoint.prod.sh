#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check
daphne \
    -b 0.0.0.0 \
    -p 8000 \
    project.asgi:application \
    1>> /shared/logfiles/daphne.access.log \
    2>> /shared/logfiles/daphne.error.log
