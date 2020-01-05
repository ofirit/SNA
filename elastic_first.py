from elasticsearch import Elasticsearch

es = Elasticsearch(HOST ="", port =9200)
es = Elasticsearch() # local is anyway defualt

es.indices.create(index = "first_index", ignore = 400)


print(es.indices.exists(index = "first_index"))
