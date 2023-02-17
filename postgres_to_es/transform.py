def add_dict(result_list: list, item: dict, current_id: int):
    """Функция добавления словаря в результирующий список по current_id"""
    result_list.append(dict())
    result_list[current_id]['id'] = item['fw_id']
    result_list[current_id]['title'] = item['title']
    result_list[current_id]['description'] = item['description']
    result_list[current_id]['imdb_rating'] = item['rating']
    result_list[current_id]['actors'] = []
    result_list[current_id]['actors_names'] = []
    result_list[current_id]['writers'] = []
    result_list[current_id]['writers_names'] = []
    result_list[current_id]['genre'] = []


def add_info_to_dict(result_list: list, item: dict, current_id: int):
    """Функция добавления  информации в словарь результирующего списка по current_id"""
    if item['g_name'] not in result_list[current_id]['genre']:
        result_list[current_id]['genre'].append(item['g_name'])
    if item['role'] == 'director':
        result_list[current_id]['director'] = item['full_name']
    elif item['role'] == 'actor':
        actor_dict = {'id': item['p_id'], 'name': item['full_name']}
        if actor_dict not in result_list[current_id]['actors']:
            result_list[current_id]['actors'].append(actor_dict)
        if item['full_name'] not in result_list[current_id]['actors_names']:
            result_list[current_id]['actors_names'].append(item['full_name'])
    elif item['role'] == 'writer':
        writer_dict = {'id': item['p_id'], 'name': item['full_name']}
        if writer_dict not in result_list[current_id]['writers']:
            result_list[current_id]['writers'].append(writer_dict)
        if item['full_name'] not in result_list[current_id]['writers_names']:
            result_list[current_id]['writers_names'].append(item['full_name'])


class DataTransformer:

    def transform_data(self, data):
        """Функция приводит данные в формат, соответствующий схеме индекса в ElasticSearch
            Args: генератор словарей
        """
        list_data = [item for item in data]
        list_data.sort(key=lambda dictionary: dictionary['fw_id'])
        result_list = []
        current_id = 0
        for item in list_data:
            if not result_list or result_list[current_id]['id'] != item['fw_id']:
                if result_list:
                    current_id += 1
                add_dict(result_list, item, current_id)
                add_info_to_dict(result_list, item, current_id)
            else:
                add_info_to_dict(result_list, item, current_id)

        return result_list

    def gen_json_data(self, data):
        """Функция генерирует из списка данные для загрузки в ElasticSearch"""
        list_data = self.transform_data(data)
        for item in list_data:
            yield {
                "_index": "movies",
                "_id": item['id'],
                "_source": item}
