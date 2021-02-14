#!/bin/bash

echo "Migrating..."
python manage.py migrate --noinput
