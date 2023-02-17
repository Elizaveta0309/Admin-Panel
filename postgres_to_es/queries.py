PERSONS_QUERIES = dict(
    type='persons',
    for_ids='SELECT id FROM content.person WHERE modified > \'{date}\' ORDER BY modified;',
    for_filmworks_ids='SELECT fw.id FROM content.film_work fw LEFT JOIN content.person_film_work pfw'
                      ' ON pfw.film_work_id = fw.id WHERE pfw.person_id IN {ids} ORDER BY fw.modified;',
    for_entire_filmworks='SELECT'
                         ' fw.id as fw_id, '
                         'fw.title, '
                         'fw.description, '
                         'fw.rating, '
                         'pfw.role, '
                         'p.id as p_id, '
                         'p.full_name,'
                         ' g.name as g_name'
                         ' FROM content.film_work fw'
                         ' LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id'
                         ' LEFT JOIN content.person p ON p.id = pfw.person_id'
                         ' LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id'
                         ' LEFT JOIN content.genre g ON g.id = gfw.genre_id'
                         ' WHERE fw.id IN {ids}; '
)

GENRES_QUERIES = dict(
    type='genres',
    for_ids='SELECT id FROM content.genre WHERE modified > \'{date}\' ORDER BY modified;',
    for_filmworks_ids='SELECT fw.id FROM content.film_work fw LEFT JOIN content.genre_film_work gfw '
                      'ON gfw.film_work_id = fw.id WHERE gfw.genre_id IN {ids} ORDER BY fw.modified;',
    for_entire_filmworks='SELECT'
                         ' fw.id as fw_id, '
                         'fw.title, '
                         'fw.description, '
                         'fw.rating, '
                         'pfw.role, '
                         'p.id as p_id, '
                         'p.full_name,'
                         ' g.name as g_name'
                         ' FROM content.film_work fw'
                         ' LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id'
                         ' LEFT JOIN content.person p ON p.id = pfw.person_id'
                         ' LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id'
                         ' LEFT JOIN content.genre g ON g.id = gfw.genre_id'
                         ' WHERE fw.id IN {ids}; '
)

FILMWORKS_QUERY = dict(
    type='filmworks',
    for_entire_filmworks='SELECT'
                         ' fw.id as fw_id, '
                         'fw.title, '
                         'fw.description, '
                         'fw.rating, '
                         'pfw.role, '
                         'p.id as p_id, '
                         'p.full_name,'
                         ' g.name as g_name'
                         ' FROM content.film_work fw'
                         ' LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id'
                         ' LEFT JOIN content.person p ON p.id = pfw.person_id'
                         ' LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id'
                         ' LEFT JOIN content.genre g ON g.id = gfw.genre_id'
                         ' WHERE fw.modified > \'{date} \'ORDER BY fw.modified; '
)
