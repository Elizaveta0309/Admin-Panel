import datetime
import os
import time
from functools import wraps

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection

from extract import PostgresExtractor
from load import ElasticLoader
from queries import PERSONS_QUERIES, GENRES_QUERIES, FILMWORKS_QUERY
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


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """ Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
     Args:
          param start_sleep_time: начальное время повтора
          param factor: во сколько раз нужно увеличить время ожидания
          param border_sleep_time: граничное время ожидания
     Returns:
          результат выполнения функции
    """
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            tries = 1  # номер попытки выполнения функции
            t = start_sleep_time
            while tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(e)
                    if t < border_sleep_time:
                        t = start_sleep_time * factor ** tries
                    elif t >= border_sleep_time:
                        t = border_sleep_time
                    time.sleep(t)
                    tries += 1

        return inner

    return func_wrapper


@backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10)
def extract_transform_load(conn: _connection, queries: dict):
    """Основной метод загрузки данных из Postgres в ElasticSearch
     Args:
            conn: подключение к Postgres
            queries: словарь с запросами, необходимыми для загрузки данных по персонам, жанрам или кинопроизведениям
    """
    postgres_extractor = PostgresExtractor(conn)
    data_transformer = DataTransformer()
    elastic_loader = ElasticLoader()
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
                add_ids_to_query(queries['for_entire_filmworks'], filmworks_ids))
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
        'host': '127.0.0.1',
        'port': 5432}
    with conn_psql_context(dsl) as pg_conn:
        extract_transform_load(pg_conn, PERSONS_QUERIES)
