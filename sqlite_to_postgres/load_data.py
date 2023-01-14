import sqlite3
import os
from psycopg2.extensions import connection as _connection
from my_conn_managers import conn_sqlite3_context, conn_psql_context
from dotenv import load_dotenv
from extract import Extractor
from save import PostgresSaver


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = Extractor(connection)

    extract_info = (
        ('SELECT id, title, description,rating, type, created_at AS created, updated_at AS modified FROM film_work;',
         'film_work'),
        ('SELECT id, full_name, created_at AS created, updated_at AS modified FROM person;',
         'person'),
        ('SELECT id, name, description, created_at AS created, updated_at AS modified FROM genre;',
         'genre'),
        ('SELECT id, film_work_id, genre_id, created_at AS created FROM genre_film_work;',
         'genre_film_work'),
        ('SELECT id, film_work_id, person_id, role, created_at AS created FROM person_film_work;',
         'person_film_work'))

    save_info = (
        "INSERT INTO film_work(title, description, type, created, modified, rating, id)"
        "VALUES (%s,%s,%s,%s,%s,%s,%s)"
        "ON CONFLICT (id) DO NOTHING;",
        "INSERT INTO person(full_name, created, modified, id)"
        "VALUES (%s,%s,%s,%s)"
        "ON CONFLICT (id) DO NOTHING;",
        "INSERT INTO genre(name, description, created, modified, id)"
        "VALUES (%s,%s,%s,%s,%s)"
        "ON CONFLICT (id) DO NOTHING;",
        "INSERT INTO genre_film_work(film_work_id, genre_id, created, id)"
        "VALUES (%s,%s,%s,%s)"
        "ON CONFLICT (id) DO NOTHING;",
        "INSERT INTO person_film_work(film_work_id, person_id, role, created, id)"
        " VALUES (%s,%s,%s,%s,%s)"
        "ON CONFLICT (id) DO NOTHING;")

    for i in range(5):
        data = sqlite_extractor.extract(*extract_info[i])
        postgres_saver.save_data(save_info[i], data)


if __name__ == '__main__':
    load_dotenv()
    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': '127.0.0.1',
        'port': 5432}
    with conn_sqlite3_context('db.sqlite') as sqlite_conn, conn_psql_context(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
