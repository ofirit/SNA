# load package modules
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
