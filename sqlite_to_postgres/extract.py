from my_dataclasses import FilmWork, Person, Genre, GenreFilmWork, PersonFilmWork


class Extractor:
    def __init__(self, connection):
        self.conn = connection
        self.curs = connection.cursor()

    def extract(self, query: str, table: str):
        """Возвращает генератор объектов dataclass"""
        self.curs.execute(query)
        while True:
            results = self.curs.fetchmany(100)
            if not results:
                break
            for result in results:
                if table == 'film_work':
                    yield FilmWork(**dict(result))
                elif table == 'genre':
                    yield Genre(**dict(result))
                elif table == 'person':
                    yield Person(**dict(result))
                elif table == 'person_film_work':
                    yield PersonFilmWork(**dict(result))
                elif table == 'genre_film_work':
                    yield GenreFilmWork(**dict(result))
