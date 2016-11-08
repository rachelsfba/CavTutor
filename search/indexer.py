#!/usr/bin/python3
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, requests

consumer = KafkaConsumer('new-tutor-listing-topic', group_id='tutor-listing-indexer', bootstrap_servers=['kafka:9092'])
elasticsearch = Elasticsearch([{'host': 'elasticsearch', 'port': 9200}])


for message in consumer:
    new_tutor = json.loads(message.value.decode('utf-8'))
    
    
    print(message)
    
    
    ret = elasticsearch.index(index='tutor-listing-indexer', doc_type='listing', id=new_tutor['id'], body=new_tutor)
    elasticsearch.indices.refresh(index="tutor-listing-indexer")

    print("hello from the indexer")
    