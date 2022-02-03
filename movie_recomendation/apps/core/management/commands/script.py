from movie_recomendation.apps.movie.models import (
    Genre,
    Movie
)
from django.core.management.base import BaseCommand

from pandas import read_csv

IMDB_LINK = 'https://www.imdb.com/title/tt'
TMDB_LINK = 'https://www.themoviedb.org/movie/'


class Command(BaseCommand):
    help = 'Run script'

    def handle(self, *args, **kwargs):

        movies = read_csv('movies-csv/movies.csv')

        unique_genres = set()

        for genres in movies['genres']:
            genre_list = genres.split('|')

            for genre in genre_list:
                unique_genres.add(genre)

        genre_instances = []

        for genre in sorted(unique_genres):
            if not Genre.objects.filter(name=genre).exists():
                genre_instances.append(
                    Genre(
                        name=genre
                    )
                )

        Genre.objects.bulk_create(genre_instances)

        movie_instances = []
        for row in range(len(movies)):
            id = movies['movieId'][row]
            title = movies['title'][row]

            if not Movie.objects.filter(id=id).exists():
                movie_instances.append(
                    Movie(
                        id=id,
                        title=title
                    )
                )

        Movie.objects.bulk_create(movie_instances)

        for row in range(len(movies)):
            id = movies['movieId'][row]
            genres = movies['genres'][row]

            try:
                movie = Movie.objects.get(id=id)

            except Movie.DoesNotExist:
                self.stdout.write(
                    f'Filme com id {id} não existe no banco de dados')
                continue

            genre_list = genres.split('|')

            ThroughModel = Movie.genres.through

            through_instances = []
            for genre in Genre.objects.filter(name__in=genre_list):
                if not movie.genres.filter(name__in=genre_list).exists():
                    through_instances.append(
                        ThroughModel(
                            genre_id=genre.id,
                            movie_id=id
                        )
                    )

            ThroughModel.objects.bulk_create(through_instances)

        links = read_csv('movies-csv/links.csv')

        movie_instances_update = []

        for row in range(len(links)):
            movie_id = links['movieId'][row]
            imdb_id = links['imdbId'][row]
            tmdb_id = links['tmdbId'][row]

            try:
                movie = Movie.objects.get(id=movie_id)

            except Movie.DoesNotExist:
                self.stdout.write(
                    f'Filme com id {id} não existe no banco de dados')
                continue

            tmdb = str(tmdb_id).split('.')[0]

            movie.imdb = f'{IMDB_LINK}{str(imdb_id)}'
            movie.tmdb = f'{TMDB_LINK}{tmdb}'

            movie_instances_update.append(movie)

        Movie.objects.bulk_update(movie_instances_update, ['imdb', 'tmdb'])
