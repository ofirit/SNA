from elasticsearch import Elasticsearch

es = Elasticsearch(HOST ="https://18496c6fce9c4269a9706a445d67cb30.us-east-1.aws.found.io", port =9243)
es = Elasticsearch() # local is anyway defualt

print(es.indices.create(index = "second_index4", ignore = 400))


print(es.indices.exists(index = "first_index"))
