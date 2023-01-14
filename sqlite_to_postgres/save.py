from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch
from dataclasses import astuple


class PostgresSaver:
    def __init__(self, connection: _connection):
        self.conn = connection
        self.curs = connection.cursor()
        self.curs.execute("SET search_path TO content;")

    def save_data(self, query: str, data):
        """Принимает в качестве аргументов генератор объектов dateclass"""
        all_data = (astuple(item) for item in data)
        execute_batch(self.curs, query, all_data)
        self.conn.commit()
