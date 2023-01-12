# Project «Grocery Assistant»

![Workflow status](https://github.com/Beloborodova-Anastasiia/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg
)
### Server data
```
IP server: http://51.250.82.140/
```


### Description

Grocery Assistant App is a website where users can post recipes, add other people's
recipes to favorites, subscribe to posts by others authors. Shopping List service
allows to create shopping list of products that need to buy for cooking selected dishes.

### Technologies

Python 3.7

Django 2.2.19

Django REST framework 3.12.4

Docker 20.10.17


### Local project run:

Clone a repository and navigate to it on the command line:

```
git clone git@github.com:Beloborodova-Anastasiia/foodgram-project.git
```

```
cd foodgram-project/infra
```

Create env-file by template:

```
MY_KEY='Key django-project'
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=PASSWORD
DB_HOST=db
DB_PORT=5432
```

Run build docker-container:

```
for Windows and Mac:
docker-compose up -d --build
```
```
for Linux:
sudo docker-compose up -d --build
```

Move data to database:

```
for Windows and Mac:
docker-compose exec web python manage.py loaddata fixtures.json
```
```
for Linux:
sudo docker-compose exec web python manage.py loaddata fixtures.json
```

Create a superuser if necessary:

```
for Windows and Mac:
docker-compose exec web python manage.py createsuperuser
```
```
for Linux:
sudo docker-compose exec web python manage.py createsuperuser
```

The project administrator's website is available at:

```
http://localhost/admin
```

Project's documentation is available at:

```
http://localhost/api/docs/
```

### API request examples

New user registration:

```
POST: /api/users/
```
```
Request body:
{
  "email": "string",
  "username": "string",
  "first_name": "string",
  "last_name": "string",
  "password": "string"
}
```
```
Response:
{
  "email": "string",
  "id": int,
  "username": "string",
  "first_name": "string",
  "last_name": "string",
}
```

Get token:
```
POST: /api/auth/token/login/
```
```
Request body:
{
  "password": "string",
  "email": "string"
}
```
```
Response:
{
  "auth_token": "string"
}
```

Get all recipes list:

```
GET: /api/recipes/
```
```
Response:
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

Creating a new recipe:

```
POST: /api/recipes/
```
```
Request:
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
Response:
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

Adding a recipe to the shopping list:

```
POST: /api/recipes/{id}/shopping_cart/
```
```
Response:
{
  "id": 0,
  "name": "string",
  "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
  "cooking_time": 1
}
```

### Author

Anastasiia Beloborodova 

anastasiia.beloborodova@gmail.com
