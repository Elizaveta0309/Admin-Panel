import sqlite3
import psycopg2
from contextlib import contextmanager


@contextmanager
def conn_sqlite3_context(db_path: str):
    """Принимает в качестве аргумента путь к файлу db.sqlite"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    yield conn
    conn.cursor().close()
    conn.close()


@contextmanager
def conn_psql_context(dsl: dict):
    """Принимает в качестве аргумента словарь с параметрами подключения."""
    conn = psycopg2.connect(**dsl)
    yield conn
    conn.cursor().close()
    conn.close()
