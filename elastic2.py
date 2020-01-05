# load package modules
import sys, json
import os
import time
from datetime import datetime
from elasticsearch import Elasticsearch, helpers
from pprint import pprint

root_path = "C:/Users/Omer/Desktop/SN Project/"
raw_data_path = root_path + "first/venv/"
json_filename = "Tweets.json"
directory = raw_data_path + json_filename

# es = Elasticsearch(HOST =  'localhost',
#                    port = 9200)

es = Elasticsearch(
    ['https://18496c6fce9c4269a9706a445d67cb30.us-east-1.aws.found.io'],
    http_auth=('elastic', '6dD0kmM3CWq58Ag20iUVzHrs'),
    scheme="https",
    verify_certs=False,
    port=9243)

if es.ping():
    print('connected')


def send_data_to_es(data, id):
    res = es.index(index='new_index', doc_type='_doc', body=data, id=id)
    print(res)


def get_data_from_es():
    r = es.search(index='new', body={"query": {"match": {'Name': 'Omer Raviv'}}})
    print(r)
    print(type(r))


