[![FastAPI](https://img.shields.io/badge/-FastAPI-005571?style=flat-square&logo=FastAPI)](https://fastapi.tiangolo.com/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-14354C?style=flat-square&logo=Pydantic)](https://pydantic-docs.helpmanual.io/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-336791?style=flat-square&logo=postgresql)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-f2ae30?style=flat-square&logo=alembic)](https://alembic.sqlalchemy.org/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-FCA121?style=flat-square&logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)

# Тестовое задание от компании Bewise
Для выполнения задачи был использован фреймворк FastAPI в комбинации с alembic, SQLAlchemy, Pydantic, 
PostgreSQL(psycopg2-binary)

## Содержимое

1. [Описание задачи](#task-description)
2. [Как запустить](#local-setup)
3. [Пример POST-запроса к API](#post-example)
2. [Как вести разработку](#development)
    1. [Линтеры](#linters)
    1. [Как обновить зависимости](#add-python-package-to-image)

<a name="task-description"></a>
## Описание задачи:
1. С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - 
PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, 
а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера (то есть -
использовать volume-ы для хранения файлов СУБД на хост-машине.
2. Реализовать на Python3 простой веб сервис (с помощью FastAPI или Flask, например), выполняющий следующие функции:
   - В сервисе должно быть реализовано REST API, принимающее на вход POST запросы с содержимым вида `{"questions_num": integer}`.
   - После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) 
   https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
   - Далее, полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как **минимум**
   следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки):
     - **ID вопроса**
     - **Текст вопроса**
     - **Текст ответа**
     - **Дата создания вопроса**<br>
     
   В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
   - Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.
3. В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисом из п. 2., его настройке и запуску. А также пример запроса к POST API сервиса.
4. Желательно, если при выполнении задания вы будете использовать docker-compose, SqlAalchemy,  пользоваться аннотацией типов.
       
<a name="local-setup"></a>
## Как запустить
Склонируйте репозиторий:
```
git clone https://github.com/elnarmen/bewise_test.git
cd bewise_test
```

Перед запуском Docker Compose в корне репозитория создайте файл `.env` со следующими переменными:

``` bash
POSTGRES_DB='db_name'
POSTGRES_USER='user'
POSTGRES_PASSWORD='password'
DATABASE_URL = "postgresql://user:password@postgres/db_name"
```
Скачайте и соберите докер-образы с помощью Docker Сompose:

```shell
$ docker compose pull --ignore-buildable
$ docker compose build
```

Примените миграции к базе данных:
```shell
$ docker compose run --rm app alembic upgrade head
…
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```

Запустите приложение командой:

```shell
$ docker compose up
…
[+] Running 3/3
 ✔ Container bewise_test-py-linters-1  Created                                                                                                                0.4s 
 ✔ Container bewise_test-postgres-1    Created                                                                                                                0.5s 
 ✔ Container bewise_test-app-1         Created 
```
После запуска документация будет доступна по адресу:

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

<a name="post-example"></a>
## Пример POST-запроса к API:
URL: https://127.0.0.1:8000/questions

Headers: {'Content-Type': 'application/json'}

Request body: {question_num: 100}

<a name="development"></a>
## Как вести разработку
<a name="linters"></a>
### Линтеры
Для того чтобы при коммите автоматически запускались линтеры, установите [pre-commit package manager](https://pre-commit.com/).
Затем в корне репозитория запустите команду для настройки хуков:

```shellw
$ pre-commit install
```
Если линтеры обнаружат проблемы в коде, коммит прервётся с сообщением об ошибке. 


Чтобы самостоятельно проверить линтером код в каталоге `/app/src/` запустите команду:

```shell
$ docker compose run --rm py-linters flake8 /app/src/
…
/app/src/migrations/env.py:19:1: E303 too many blank lines (3)
1
```

<a name="add-python-package-to-image"></a>
### Как обновить зависимости

В качестве менеджера пакетов для образа используется [Poetry](https://python-poetry.org/docs/).

Файлы Poetry `pyproject.toml` и `poetry.lock` проброшены в контейнер в виде volume, поэтому изменения 
зависимостей внутри контейнера попадают и наружу в git-репозиторий.

Например, чтобы добавить библиотеку `alembic`, запустите все контейнеры, подключитесь к уже работающему 
контейнеру `app` и внутри запустите команду `poetry add alembic`:

```shell
$ docker compose up -d
$ docker compose exec app bash
container:$ poetry add alembic
container:$ exit
```

Конфигурационные файлы `pyproject.toml` и `poetry.lock` обновятся не только внутри контейнера, но и в репозитории 
благодаря настроенным docker volumes.
 
Не забудьте обновить докер-образ, чтобы новые контейнеры тоже получали свежий набор зависимостей:
```shell
$ docker compose build app
```
