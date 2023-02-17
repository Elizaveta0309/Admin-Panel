import psycopg2.extras


class PostgresExtractor:
    def __init__(self, connection):
        self.conn = connection
        self.curs = connection.cursor()

    def extract(self, query: str, dict_param: bool):
        """ Извлекает данные из Postgres по запросу
              Args:
                  query: строка запроса
                  dict_param: указывает приводить извлеченные данные в формат словаря или нет
              Returns:
                  генератор извлеченных данных
           """
        self.curs.execute(query)
        while True:
            results = self.curs.fetchmany(100)
            if not results:
                break
            for result in results:
                if dict_param:
                    yield dict(result)
                else:
                    yield result

    def extract_ids(self, query: str):
        """Извлекает ids измененных записей по персонам или жанрам"""
        return self.extract(query, False)

    def extract_filmworks_ids(self, query: str):
        """Извлекает ids, связанных с измененными персонами или жанрами кинопроизведений """
        return self.extract(query, False)

    def extract_entire_filmworks(self, query: str):
        """Извлекает всю необходимую  для загрузки в ElasticSearch информаицию по кинопроизведениям """
        self.curs = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return self.extract(query, True)
