![Foodgram test and deploy workflow](https://github.com/smirnov-andrey/foodgram-project-react/actions/workflows/foodgram_master_workflow.yml/badge.svg)
# Проект Foodgram, «Продуктовый помощник»

## Описание
Сервис "Продуктовый помощник", на котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Технологии
В проекте использованы технологии:

>Django==4.1.6   
django-cors-headers==3.13.0   
django-filter==22.1   
djangorestframework==3.14.0   
djoser==2.1.0   
psycopg2-binary==2.9.5   
python-dotenv==1.0.0   
Pillow==9.4.0   
sentry-sdk==1.16.0   
gunicorn==20.1.0   

## Установка в Docker Compose
Клонировать репозиторий и перейти в него в командной строке:

```commandline
git clone https://github.com/smirnov-andrey/foodgram-project-react.git
```

```commandline
cd foodgram-project-react/infra
```

Скопировать docker образ приложения:

```commandline
docker pull aesmirnov/foodgram_frontend:latest
docker pull aesmirnov/foodgram_backend:latest
```

Разверните приложение:

```commandline
docker-compose up -d --build
```

Выполнить миграции:

```commandline
docker-compose exec web python manage.py migrate
```

Выполнить процедуру сбора статики:

```commandline
docker-compose exec web python manage.py collectstatic --no-input
```

Создать учетную запись администратора-суперпользователя:

```commandline
docker-compose exec web python manage.py createsuperuser
```
--------------------------------------------------------------------------
## Автор:

**Андрей Смирнов**  
Студент Яндекс Практикум   
GitHub: https://github.com/smirnov-andrey
