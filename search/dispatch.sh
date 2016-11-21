#!/bin/bash
#
# dispatch.sh:
#
# Runs a KafkaConsumer on incoming search data every second.

while true; do
    dockerize -wait tcp://elasticsearch:9200 \
        -wait tcp://kafka:9092 \
        python indexer.py
done
