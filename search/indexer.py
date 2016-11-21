#!/usr/bin/python
""" Get kafka-python library loaded. """
from kafka import KafkaConsumer

""" Load ElasticSearch library. """
from elasticsearch import Elasticsearch

""" JSON and requests libraries. """
import json, requests

consumer = KafkaConsumer(
        'new-tutor-listing-topic',
        group_id='tutor-listing-indexer',
        bootstrap_servers=['kafka:9092'],
    )

elasticsearch = Elasticsearch(['elasticsearch'])

if not elasticsearch.indices.exists('tutor-listing-indexer'):
    elasticsearch.indices.create(index='tutor-listing-indexer')

for message in consumer:
    print("Received", message.value, "\n\n\n")
    new_tutor = json.loads(message.value.decode('utf-8'))
    elasticsearch.index(index='tutor-listing-indexer', doc_type='listing', id=new_tutor['id'], body=new_tutor)

    elasticsearch.indices.refresh(index="tutor-listing-indexer")


