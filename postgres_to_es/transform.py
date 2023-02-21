def create_dict(item: dict) -> dict:
    """Функция создания словаря """
    temp_dict = dict()
    temp_dict['id'] = item['fw_id']
    temp_dict['title'] = item['title']
    temp_dict['description'] = item['description']
    temp_dict['imdb_rating'] = item['rating']
    temp_dict['actors'] = []
    temp_dict['actors_names'] = []
    temp_dict['writers'] = []
    temp_dict['writers_names'] = []
    temp_dict['genre'] = []
    return temp_dict


def add_info_to_dict(item: dict, temp_dict: dict):
    """Функция добавления информациии в словарь"""
    for p in item['persons']:
        if p['person_role'] == 'director':
            temp_dict['director'] = p['person_name']
        elif p['person_role'] == 'actor':
            temp_dict['actors_names'].append(p['person_name'])
            temp_dict['actors'].append({"id": p['person_id'], "name": p['person_name']})
        elif p['person_role'] == 'writer':
            temp_dict['writers_names'].append(p['person_name'])
            temp_dict['writers'].append({"id": p['person_id'], "name": p['person_name']})
    for g in item['genres']:
        temp_dict['genre'].append(g)


class DataTransformer:

    def transform_data(self, data):
        """Функция приводит данные в формат, соответствующий схеме индекса в ElasticSearch
            Args: генератор словарей
        """
        for item in data:
            temp_dict = create_dict(item)
            add_info_to_dict(item, temp_dict)
            yield {
                "_index": "movies",
                "_id": item['fw_id'],
                "_source": temp_dict}
