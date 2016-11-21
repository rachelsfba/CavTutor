#!/usr/bin/python3

""" Get kafka-python library loaded. """
from kafka import KafkaConsumer

""" Load ElasticSearch library. """
from elasticsearch import Elasticsearch

""" JSON and requests libraries. """
import json, requests

def dequeue(consumer, elasticsearch):
    for message in consumer:

        try:
            new_tutor = json.loads(message.value.decode('utf-8'))
            elasticsearch.index(index='tutor-listing-indexer', doc_type='listing', id=new_tutor['id'], body=new_tutor)
        except ValueError:
            continue

        elasticsearch.indices.refresh(index="tutor-listing-indexer")

consumer = KafkaConsumer(
        group_id='tutor-listing-indexer',
        bootstrap_servers=['kafka:9092'],
    )


consumer.subscribe(['new-tutor-listing-topic',])
elasticsearch = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

print("---1---")

while not elasticsearch.indices.exists('tutor-listing-indexer'):
    elasticsearch.indices.create(index='tutor-listing-indexer', ignore=400)

print("---2---")
dequeue(consumer, elasticsearch)
print("---3---")
