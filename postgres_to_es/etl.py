import datetime
import os
import backoff


from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from elasticsearch import Elasticsearch

from extract import PostgresExtractor
from load import ElasticLoader
from queries import PERSONS_QUERIES, GENRES_QUERIES, FILMWORKS_QUERY, FILMWORKS_QUERY_BY_IDS
from sqlite_to_postgres.my_conn_managers import conn_psql_context
from state import JsonFileStorage, State
from transform import DataTransformer


def add_ids_to_query(query: str, data) -> str:
    """ Добавляет ids к строке запроса
       Args:
           query: строка запроса
           data: генератор с ids
       Returns:
           str:отформатировонная строка запроса
    """
    tuple_data = tuple(''.join(item) for item in data)
    return query.format(ids=tuple_data)


def add_date_to_query(query: str, date: str) -> str:
    """ Добавляет дату к строке запроса
        Args:
            query: строка запроса
            date: дата
        Returns:
            str: отформатировонная строка запроса
     """
    return query.format(date=date)


def is_not_empty(iterable):
    """Функция проверки генератора на непустоту"""
    try:
        first = next(iterable)
    except StopIteration:
        return False
    return True


@backoff.on_exception(backoff.expo, (ConnectionError, TimeoutError))
def extract_transform_load(conn: _connection, queries: dict, es: Elasticsearch, query=FILMWORKS_QUERY_BY_IDS):
    """Основной метод загрузки данных из Postgres в ElasticSearch
     Args:
            conn: подключение к Postgres
            es:instance of ElasticSearch
            query: итоговый запрос для получения всех данных по кинопроизведению для смежных таблиц
            queries: словарь с запросами, необходимыми для загрузки данных по персонам, жанрам или кинопроизведениям
    """
    postgres_extractor = PostgresExtractor(conn)
    data_transformer = DataTransformer()
    elastic_loader = ElasticLoader(es)
    json_file_storage = JsonFileStorage('fileStorage.txt')
    state = State(json_file_storage)
    last_modified = state.get_state('last_modified')

    if queries['type'] == 'filmworks':
        filmworks = postgres_extractor.extract_entire_filmworks(
            add_date_to_query(queries['for_entire_filmworks'], last_modified))
        filmworks_json = data_transformer.gen_json_data(filmworks)
        elastic_loader.load(filmworks_json)
        state.set_state('last_modified', str(datetime.datetime.now()))
    elif queries['type'] == 'persons' or queries['type'] == 'genres':
        ids = postgres_extractor.extract_ids(add_date_to_query(queries['for_ids'], last_modified))
        if is_not_empty(ids):
            filmworks_ids = postgres_extractor.extract_filmworks_ids(
                add_ids_to_query(queries['for_filmworks_ids'], ids))
            filmworks = postgres_extractor.extract_entire_filmworks(
                add_ids_to_query(query['for_entire_filmworks'], filmworks_ids))
            filmworks_json = data_transformer.gen_json_data(filmworks)
            elastic_loader.load(filmworks_json)
            state.set_state('last_modified', str(datetime.datetime.now()))
    else:
        print("Wrong type!")


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')}

    es = Elasticsearch(os.environ.get('ES_NAME'))

    with conn_psql_context(dsl) as pg_conn:
        extract_transform_load(pg_conn, PERSONS_QUERIES, es)
