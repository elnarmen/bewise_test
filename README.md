<a name="local-setup"></a>
## Как развернуть local-окружение

Для запуска приложения вам понадобятся Docker и Docker Compose. Инструкции по их установке ищите на официальных сайтах:

- [Install Docker Desktop](https://www.docker.com/get-started/)
- [Install Docker Compose](https://docs.docker.com/compose/install/)

Склонируйте репозиторий.

Для того, чтобы автоматически запускать линтеры перед началом разработки установите [pre-commit package manager](https://pre-commit.com/).

Затем в корне репозитория запустите команду для настройки хуков:

```shellw
$ pre-commit install
```

В дальнейшем при коммите автоматически будут запускаться линтеры. Есть линтеры обнаружат проблемы в коде,
то коммит прервётся с сообщением об ошибке.

Перед запуском Docker Compose в корне репозитория создайте файл `.env` со следующими переменными:

``` bash
POSTGRES_DB='db_name'
POSTGRES_USER='user'
POSTGRES_PASSWORD='password'
Значения переменных замените на параметры вашей БД
```
Скачайте и соберите докер-образы с помощью Docker Сompose:

```shell
$ docker compose pull --ignore-buildable
$ docker compose build
```
