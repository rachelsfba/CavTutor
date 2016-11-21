#!/bin/bash
#
# dispatch.sh:
#
# Runs a KafkaConsumer on incoming search data every second.
echo -e "Attempting to contact kafka and elasticsearch containers... "

echo -e "Waiting for kafka container... "
until $(ping -c1 kafka &>/dev/null); do
    printf '.'
    sleep 1
done
echo -e "Successfully pinged kafka!"

echo -e "Waiting for elasticsearch container... "
until $(ping -c1 elasticsearch &>/dev/null); do
    printf '.'
    sleep 1
done
echo -e "Successfully pinged elasticsearch!"

sleep 5

while true; do
    python indexer.py
    sleep 1
    echo -e "Relooping"
done
