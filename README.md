<a name="local-setup"></a>
## Как развернуть local-окружение

Для запуска приложения вам понадобятся Docker и Docker Compose. Инструкции по их установке ищите на официальных сайтах:

- [Install Docker Desktop](https://www.docker.com/get-started/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

Склонируйте репозиторий.

Перед запуском Docker Compose в корне репозитория создайте файл `.env` со следующими переменными:

``` bash
POSTGRES_DB='db_name'
POSTGRES_USER='user'
POSTGRES_PASSWORD='password'
DATABASE_URL = "postgresql://user:password@postgres/db_name"
Значения переменных замените на параметры вашей БД. url базы данных должен соответствовать шаблону:
postgres://<user>:<password>@db/<database_name>
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

<a name="development"></a>
## Как вести разработку

Для того, чтобы автоматически запускать линтеры перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

Затем в корне репозитория запустите команду для настройки хуков:

```shellw
$ pre-commit install
```

В дальнейшем при коммите автоматически будут запускаться линтеры. Коммит прервётся с сообщением об ошибке, если
линтеры обнаружат проблемы в коде.

<a name="add-python-package-to-django-image"></a>
### Как установить python-пакет в образ

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

<a name="run-python-linters"></a>
### Как запустить линтеры Python

Линтеры запускаются в отдельном docker-контейнере, а код подключается к нему с помощью volume. 
Например, чтобы проверить линтером код в каталоге `/app/src/` запустите команду:

```shell
$ docker compose run --rm py-linters flake8 /app/src/
…
/app/src/migrations/env.py:19:1: E303 too many blank lines (3)
```