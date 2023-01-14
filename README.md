Чтобы запустить проект:

- cd docker_compose
- docker-compose up
- docker exec -i -t docker_compose_service_1 python manage.py migrate (для админики)
- docker exec -i -t docker_compose_service_1 python manage.py createsuperuser
- psql -h 127.0.0.1 -U admin -d postgresql -f movies_database.ddl 
