![Typing SVG](https://readme-typing-svg.herokuapp.com?font=betapi&size=40&pause=1000&color=F7F7F7&width=435&lines=The+Bet+API)

## Used technology
- Python 3.10;
- FastApi ( Web framework for building APIs );
- Docker and Docker Compose ( containerization );
- PostgreSQL ( database );
- SQLAlchemy ( working with database from Python );
- RabbitMQ ( Queue )
- Alembic ( database migrations made easy );
- Pydantic ( models )

<hr/>

![image](templates/img.png)

<hr/>

### Установка и запуск

1. Клонировать проект в удобное место:

```sh
git clone https://github.com/Whitev2/bet-test-api.git
```

2. Собрать и запустить контейнеры:
```sh
docker-compose build
```
```sh
docker-compose up
```
<hr/>

### Дополнительные команды


1. Создание файла миграций:
```sh
docker-compose exec bet_maker alembic revision --autogenerate -m "init"
```

2. Обновление базы данных:
```sh
docker-compose exec bet_maker alembic upgrade head
```

3. Остановка контейнеров:
```sh
docker-compose down
```

4. Запуск контейнеров:
```sh
docker-compose up
```

<hr/>

### API: Документация

- Provider_URL: http://localhost:8001
- Maker_URL: http://localhost:8000
- 
- Provider Swagger UI: http://localhost:8001/docs
- Maker ReDoc UI: http://localhost:8000/redoc

<hr/>

### Описание функционала
- Maker получает активные ивенты из Provider через endpoint url
- При изменении состояния со стороны Provider - меняется статус у ставки
- Обмен данными для изменения состояний реализован через aio-pika и RabbitMQ
- Все сервисы собираются в Docker Compose
- Возможна интеграция с k8s













