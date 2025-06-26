#!/bin/bash

cd /app/backend
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn project.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 4 \
    --log-level info \
    --access-logfile /shared/logfiles/gunicorn.access.log \
    --error-logfile /shared/logfiles/gunicorn.error.log &

cd /app
nginx -g "daemon off;"
