""" data_generator.py: generates dummy data to input into Spark instances """
import string
import random

num_samples = 1000
num_items = 10
num_users = 20
name_length = 5

def generate_names(num_names, length):
    cur_name = list(string.ascii_lowercase)
    
    for i in range(num_names):
        random.shuffle(cur_name)    
        yield "".join(cur_name[:length])

users = list(generate_names(num_users, name_length))

for i in range(num_samples):
    random.shuffle(users)
    print(users[0], random.randint(1,num_items), sep="\t")



