import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# views.py has two methods that will help us parse data into Kafka
from CavTutor.utilities.json import _flatten

# Get some constants we define in the settings.py file for this project
from core.settings import API_BASE, UX_BASE, KAFKA_ADDR

# Libraries for RESTful querying
import requests, json

# We need to be able to create a KafkaProducer to send data through
from kafka import KafkaProducer

# Load all fixtures into the Kafka queue by using a KafkaProducer
producer = KafkaProducer(bootstrap_servers=KAFKA_ADDR)

# Fetch all tutor listings from the API.
tutor_data = requests.get(API_BASE + 'tutors/?format=json')

# Iterate through all tutor objects in the listings.
for tutor in tutor_data.json():
    # Flatten from a 2-D into a 1-D dictionary.
    new_tutor_parsed_data = _flatten(tutor)

    # Encode JSON as bytes.
    new_tutor_encoded = json.dumps(new_tutor_parsed_data).encode('utf-8')

    # Send tutor bytes to Kafka.
    producer.send('new-tutor-listing-topic', new_tutor_encoded)

