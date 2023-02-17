from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

es = Elasticsearch('http://127.0.0.1:9200')


class ElasticLoader:
    def load(self, data):
        """"Принимает генератор словарей и пачками загружает данные в Elasticsearch"""
        bulk(es, data)
