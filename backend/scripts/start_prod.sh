#!/bin/bash

./scripts/migrate.sh
./scripts/collectstatic.sh
./scripts/test.sh
./scripts/gunicorn.sh
