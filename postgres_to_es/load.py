from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class ElasticLoader:

    def __init__(self, es: Elasticsearch):
        self.es = es

    def load(self, data):
        """"Принимает генератор словарей и пачками загружает данные в Elasticsearch"""
        bulk(self.es, data)
