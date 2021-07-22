# Shop REST API



## Setup
Get source from github:
```
git clone git@github.com:minthf/e-shop.git
```

To create virtual environment:
```
pipenv shell
```

To build container:
```
docker-compose build
```

To migrate database:
```
docker-compose run web python manage.py migrate
```

To create superuser:
```
docker-compose run web python manage.py createsuperuser
```

## Tests

To run tests:
```
docker-compose run web python manage.py test
```

## Postman Collection

https://www.getpostman.com/collections/a0ac67ea56eac5a1b766

## Heroku

https://e-shop-mint.herokuapp.com/

