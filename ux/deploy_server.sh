#!/bin/bash
# Script to deploy our Django instance. Calls Apache mod_wsgi_express to start
# its daemon, and populates a clean database instance with example data.
#
# This script will be called by docker-compose.yml from the parent directory.
APP_BASE=/app
DJANGO_BASE=$APP_BASE/app
WSGI_FILE=$DJANGO_BASE/core/wsgi.py

# No database-level commands are used outside of our API µ-service.

#python $DJANGO_BASE/manage.py flush
#python $DJANGO_BASE/manage.py makemigrations
#python $DJANGO_BASE/manage.py migrate
#python $DJANGO_BASE/manage.py loaddata $APP_BASE/db.json

# Loads fixtures from API layer into Kafka queue
echo -e "Attempting to load fixture data into Kafka. Waiting on containers...."

echo -e "Waiting for api container... (1/3)" 
until $(ping -c1 api &>/dev/null); do
    printf '.'
    sleep 1
done
echo -e "Successfully pinged api!"

echo -e "Waiting for kafka container... (2/3)" 
until $(ping -c1 kafka &>/dev/null); do
    printf '.'
    sleep 1
done
echo -e "Successfully pinged kafka!"

echo -e "Waiting for search_controller container... (3/3)" 
until $(ping -c1 search_controller &>/dev/null); do
    printf '.'
    sleep 1
done
echo -e "Successfully pinged search_controller!"

echo -e "All dependency containers loaded! (3/3)"

# for now manually making us sleep for a few seconds
sleep 10

python $DJANGO_BASE/load_fixtures.py

echo -e "Called load_fixtures.py script."
mod_wsgi-express start-server --reload-on-changes --log-to-terminal --working-directory $DJANGO_BASE $WSGI_FILE
