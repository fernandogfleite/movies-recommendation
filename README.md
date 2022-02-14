# Movie Recommendations API

### Dependencies (versions used in development)
- Python 3.10.2 
- Docker 20.10.12
- Docker Compose 1.29.2

## How to run the application

### [Clone the repository](https://github.com/fernandogfleite/movies-recommendation)


### Define an .env file with the following variables:
- SECRET_KEY
- DEBUG
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- DB_HOST


### Build the container with docker-compose:
```
docker-compose -d --buld
```

### Create a superuser:
```
docker-compose run server sh -c "python manage.py createsuperuser"
```

### Download the CSVs with movies informations in [MovieLens](https://grouplens.org/datasets/movielens/25m/).


### Create a dir in project root with create a directory named movies-csv and and extract the following files:
- links.csv
- movies.csv
- ratings.csv


### Run the script to populate the database:
```
docker-compose run server sh -c "python manage.py script"
```

### Run the server:
```
docker-compose up
```

### Open the browser in localhost:8000 and the application is running.

## Contributors
- Fernando Leite
