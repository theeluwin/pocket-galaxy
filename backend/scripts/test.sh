#!/bin/bash

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check
flake8 .
coverage run manage.py test
coverage report -m
