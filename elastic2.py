# load package modules
from elasticsearch import Elasticsearch


class ElasticSearchClass:

    def __init__(self):
        self.es = Elasticsearch(
            ['https://e30431821c454f2f90228517bdef935d.us-east-1.aws.found.io:9243'],
            http_auth=('elastic', 'nZt3e5rgXmS094LThRRXCe9N'),
            scheme="https",
            verify_certs=False,
            port=9243)
        if self.es.ping():
            print('Connected To ES')
        else:
            print('Error connecting to ES')
            exit(-1)

    def check_if_tweet_exists(self, index_name, data=None):
        res = self.es.search(index=index_name, body={"query": {"match": {"id": data.id}}})
        if res['hits']['total']['value'] <= 0:
            return False
        else:
            return True

    def send_data_to_es(self, data, element_id=None, index_name='default_index'):
        # check if tweet id already in DB
        self.es.index(index=index_name, doc_type='_doc', body=data, id=element_id)

    def get_data_from_es(self):
        r = self.es.search(index='new', body={"query": {"match_all": {}}})
        print(r)
        print(type(r))
