# Backend Technical

A project demonstrating django api development using two apps:

- increment: Create and list key-value pairs. Increment the value of a provided key
- dogs: Fetch dog images from an external api. Retrieve a random dog image along with a modified copy and the image metadata

# Technologies

- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pillow](https://pillow.readthedocs.io/en/stable/#)

# Usage

## Starting the development server

### From Source

1. Download or clone the latest version of the application
2. In a terminal, navigate to the project root
3. Build the services

```
docker-compose build
```

4. Migrate the database

```
docker-compose run -p 8000:8000 web python manage.py makemigrations
docker-compose run -p 8000:8000 web python manage.py migrate
```

5. Populate database with dog pictures

```
docker-compose run -p 8000:8000 web python manage.py populate_db
```

6. Launch the server

```
docker-compose run -p 8000:8000 web
```

7. Access the server from [http://localhost:8000](http://localhost:8000)

## API Endpoints

### Key-Value Pairs

- List key-value pairs: GET `/api/increment/keyvaluepairs/`
- Create new key-value pair: POST `/api/increment/keyvaluepairs/`  
  JSON Data `{key:string, value:integer}`
- Increment a value: POST `/api/increment/keyvaluepairs/increment/`  
  JSON Data `{key:string}`

### Dog Images

- Get dog image, modified image, and metadata: GET `/api/dogs/random/`
