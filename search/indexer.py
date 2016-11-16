#!/usr/bin/python3
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, requests

def handle_requests():
    consumer = KafkaConsumer(
            group_id='tutor-listing-indexer',
            bootstrap_servers=['kafka:9092'],
            value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        )
    
    elasticsearch = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

    elasticsearch.indices.create(index='tutor-listing-indexer', ignore=400)

    consumer.subscribe(['new-tutor-listing-topic',])
    dequeue(consumer, elasticsearch)
    
def dequeue(consumer, elasticsearch):
    for message in consumer:
        #new_tutor = json.loads(message.value.decode('utf-8'))
        new_tutor = message.value
        
        elasticsearch.index(index='tutor-listing-indexer', doc_type='listing', id=new_tutor['id'], body=new_tutor)
        elasticsearch.indices.refresh(index="tutor-listing-indexer")

try:
    handle_requests()
except:
    pass
