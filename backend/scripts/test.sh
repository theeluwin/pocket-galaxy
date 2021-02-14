#!/bin/bash

echo "Testing..."
flake8 .
coverage run manage.py test
coverage report -m
