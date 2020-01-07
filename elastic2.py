# load package modules
<<<<<<< HEAD
from elasticsearch import Elasticsearch


class ElasticSearchClass:

    def __init__(self):
        self.es = Elasticsearch(
            ['https://18496c6fce9c4269a9706a445d67cb30.us-east-1.aws.found.io'],
            http_auth=('elastic', '6dD0kmM3CWq58Ag20iUVzHrs'),
            scheme="https",
            verify_certs=False,
            port=9243)
        if self.es.ping():
            print('Connected To ES')

    def send_data_to_es(self, data, element_id=None, index_name='default_index'):
        res = self.es.index(index=index_name, doc_type='_doc', body=data, id=element_id)
        # print(res)

    def get_data_from_es(self):
        r = self.es.search(index='new', body={"query": {"match_all": {}}})
        print(r)
        print(type(r))
=======
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


>>>>>>> 356abe11e8a1a845bc435e82282313824d57327c
