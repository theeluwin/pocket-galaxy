#!/bin/bash

./scripts/migrate.sh
./scripts/collectstatic.sh
./scripts/test.sh
./scripts/runserver.sh
