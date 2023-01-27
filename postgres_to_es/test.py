from psycopg2.extensions import connection as _connection
from sqlite_to_postgres.my_conn_managers import conn_psql_context
from extract import PostgresProducer, PostgresEnricher


def load_from_postgres(pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_producer = PostgresProducer(pg_conn)
    postgres_enricher = PostgresEnricher(pg_conn)
    query_1 = 'SELECT id FROM content.person WHERE modified > \'2001-01-01\' ORDER BY modified;'

    data_1 = postgres_producer.produce(query_1)
    data_2 = postgres_enricher.enrich(data_1)
    counter_1 = 0
    counter_2 = 0
    for d in data_1:
       # print(d)
        counter_1 += 1
    #print(counter_1)

    for d in data_2:
        print(d)
        counter_2 += 1
    print(counter_2)



if __name__ == '__main__':
    dsl = {
        'dbname': 'postgres',
        'user': 'admin',
        'password': 'admin',
        'host': '127.0.0.1',
        'port': 5432}
    with conn_psql_context(dsl) as pg_conn:
        load_from_postgres(pg_conn)
