#!/bin/bash

echo "Collecting static..."
python manage.py collectstatic --no-input
