# Проект «Продуктовый помощник»

![Workflow status](https://github.com/Beloborodova-Anastasiia/
foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Описание

Приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. Сервис «Список покупок» позволяет пользователям создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

### Технологии

Python 3.7

Django 2.2.19

Docker 20.10.17

### Данные проекта на сервере
```
IP сервера: http://51.250.82.140/
```
```
Логин администратора: admin
```
```
Пароль администратора: ljv3693954
```

### Как запустить проект локально:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Beloborodova-Anastasiia/foodgram-project-react.git
```

```
cd foodgram-project-react/infra
```

Создать env-файл по следующему шаблону:

```
MY_KEY='Key django-project'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=PASSWORD
DB_HOST=db
DB_PORT=5432
```

Запустить сборку docker-контейнера:

```
для Windows и Mac:
docker-compose up -d --build
```
```
дляLinux:
sudo docker-compose up -d --build
```

Перенести данные в базу данных:

```
для Windows и Mac:
docker-compose exec web python manage.py loaddata fixtures.json
```
```
дляLinux:
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

При необходимости создать суперюзера следующей командой:

```
для Windows и Mac:
docker-compose exec web python manage.py createsuperuser
```
```
дляLinux:
sudo docker-compose exec web python manage.py createsuperuser
```

Сайт администратора проекта доступен по адресу:

```
http://localhost/admin
```

Документация проекта доступна по адресуЖ

```
http://localhost/api/docs/
```

### Примеры запросов к API

Регистрация нового пользователя:

```
POST: /api/users/
```
```
Тело запроса:
{
  "email": "string",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}
```
```
Ответ:
{
  "email": "string",
  "id": int,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
}
```

Получение токена:
```
POST: /api/auth/token/login/
```
```
Тело запроса:
{
  "password": "string",
  "email": "string"
}
```
```
Ответ:
{
  "auth_token": "string"
}
```

Получение списка всех рецептов:

```
GET: /api/recipes/
```
```
Ответ:
{
  "count": 123,
  "next": "http://foodgram.example.org/api/recipes/?page=4",
  "previous": "http://foodgram.example.org/api/recipes/?page=2",
  "results": [
    {
      "id": 0,
      "tags": [
        {
          "id": 0,
          "name": "Завтрак",
          "color": "#E26C2D",
          "slug": "breakfast"
        }
      ],
      "author": {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
      },
      "ingredients": [
        {
          "id": 0,
          "name": "Картофель отварной",
          "measurement_unit": "г",
          "amount": 1
        }
      ],
      "is_favorite": true,
      "is_in_shopping_cart": true,
      "name": "string",
      "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
      "text": "string",
      "cooking_time": 1
    }
  ]
}
```

Создание нового рецепта:

```
POST: /api/recipes/
```
```
Запрос:
{
  "ingredients": [
    {
      "id": 1123,
      "amount": 10
    }
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "string",
  "text": "string",
  "cooking_time": 1
}
```
```
Ответ:
{
    "id": 0,
    "tags": [
    {
        "id": 0,
        "name": "Завтрак",
        "color": "#E26C2D",
        "slug": "breakfast"
    }
    ],
    "author": {
    "email": "user@example.com",
    "id": 0,
    "username": "string",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "is_subscribed": false
    },
    "ingredients": [
    {
        "id": 0,
        "name": "Картофель отварной",
        "measurement_unit": "г",
        "amount": 1
    }
    ],
    "is_favorite": true,
    "is_in_shopping_cart": true,
    "name": "string",
    "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
    "text": "string",
    "cooking_time": 1
}
```

Добавление рецепта в список покупок:

```
POST: /api/recipes/{id}/shopping_cart/
```
```
Ответ:
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```

### Автор

Белобородова Анастасия  beloborodova.anastasiia@yandex.ru