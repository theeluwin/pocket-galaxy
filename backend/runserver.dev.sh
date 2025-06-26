#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
flake8 .
coverage run manage.py test
coverage report -m
python manage.py runserver 0.0.0.0:8000
