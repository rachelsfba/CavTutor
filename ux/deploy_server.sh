#!/bin/bash
# Script to deploy our Django instance. Calls Apache mod_wsgi_express to start
# its daemon, and populates a clean database instance with example data.
#
# This script will be called by docker-compose.yml from the parent directory.
APP_BASE=/app
DJANGO_BASE=$APP_BASE/app
WSGI_FILE=$DJANGO_BASE/core/wsgi.py

# Loads fixtures from API layer into Kafka queue
# uses dockerize to wait until api and kafka are up and ready
dockerize -wait tcp://api:8000 \
    -wait tcp://kafka:9092 \
    python $DJANGO_BASE/load_fixtures.py && \
    mod_wsgi-express start-server --reload-on-changes --log-to-terminal --working-directory $DJANGO_BASE $WSGI_FILE
