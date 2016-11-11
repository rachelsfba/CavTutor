#!/usr/bin/python3
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, requests

def handle_requests():
    consumer = KafkaConsumer(
            'new-tutor-listing-topic',
            group_id='tutor-listing-indexer',
            bootstrap_servers=['kafka:9092']
        )
    
    elasticsearch = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])

    dequeue(consumer, elasticsearch)
    
def dequeue(kafka, search):
    for message in kafka:
        new_tutor = json.loads(message.value.decode('utf-8'))
        
        search.index(index='tutor-listing-indexer', doc_type='listing', id=new_tutor['id'], body=new_tutor)
        search.indices.refresh(index="tutor-listing-indexer")

try:
    handle_requests()
except:
    pass
