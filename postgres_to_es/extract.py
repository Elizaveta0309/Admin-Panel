

class PostgresProducer:
    def __init__(self, connection):
        self.conn = connection
        self.curs = connection.cursor()

    def produce(self, query: str):
        self.curs.execute(query)
        while True:
            results = self.curs.fetchmany(100)
            if not results:
                break
            for result in results:
                yield result


class PostgresEnricher:
    def __init__(self, connection):
        self.conn = connection
        self.curs = connection.cursor()

    def enrich(self, data):
        tuple_data = tuple(''.join(item) for item in data)
        query_2 = "SELECT fw.id FROM content.film_work fw LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = " \
                  "fw.id WHERE pfw.person_id IN {ids} ORDER BY fw.modified; ".format(ids=tuple_data)
        print(query_2)
        self.curs.execute(query_2)
        while True:
            results = self.curs.fetchmany(100)
            if not results:
                break
            for result in results:
                yield result


class PostgresMerger:
    pass
