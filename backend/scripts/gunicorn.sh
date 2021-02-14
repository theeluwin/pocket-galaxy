#!/bin/bash

echo "Start with gunicorn"
gunicorn project.wsgi --bind 0.0.0.0:8000 --workers 4
