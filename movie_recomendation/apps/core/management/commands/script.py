from movie_recomendation.apps.movie.models import (
    Genre,
    Movie,
    MovieGenre,
    MovieRating
)
from django.core.management.base import BaseCommand

from pandas import (
    DataFrame,
    read_csv
)


IMDB_LINK = 'https://www.imdb.com/title/tt'
TMDB_LINK = 'https://www.themoviedb.org/movie/'


class Command(BaseCommand):
    help = 'Run script'

    def handle(self, *args, **kwargs):

        movies = read_csv('movies-csv/movies.csv')

        self.register_genres_from_csv(movies_csv=movies)
        self.register_movies_from_csv(movies_csv=movies)
        self.register_movie_genres_from_csv(movies_csv=movies)
        self.register_movie_links_from_csv()
        self.register_ratings_from_csv()

    def register_genres_from_csv(self, movies_csv: DataFrame):
        unique_genres = set()

        for genres in movies_csv['genres']:
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

    def register_movies_from_csv(self, movies_csv: DataFrame):
        movie_instances = []
        for row in range(len(movies_csv)):
            id = movies_csv['movieId'][row]
            title = movies_csv['title'][row]

            if not Movie.objects.filter(id=id).exists():
                movie_instances.append(
                    Movie(
                        id=id,
                        title=title
                    )
                )

        Movie.objects.bulk_create(movie_instances)

    def register_movie_genres_from_csv(self, movies_csv: DataFrame):
        for row in range(len(movies_csv)):
            id = movies_csv['movieId'][row]
            genres = movies_csv['genres'][row]

            try:
                movie = Movie.objects.get(id=id)

            except Movie.DoesNotExist:
                self.stdout.write(
                    f'Filme com id {id} não existe no banco de dados')
                continue

            genre_list = genres.split('|')

            movie_genres = []
            for genre in Genre.objects.filter(name__in=genre_list):
                if not MovieGenre.objects.filter(movie=movie,
                                                 genre=genre).exists():
                    movie_genres.append(
                        MovieGenre(
                            movie=movie,
                            genre=genre
                        )
                    )

            MovieGenre.objects.bulk_create(movie_genres)

    def register_movie_links_from_csv(self):
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

    def register_ratings_from_csv(self):
        ratings = read_csv('movies-csv/ratings.csv')

        ratings_df = DataFrame(ratings.groupby('movieId').rating.mean())

        ratings_df['rating_counts'] = ratings.groupby('movieId').rating.count()

        C = ratings_df['rating'].mean()

        m = ratings_df.rating_counts.min()

        def weighted_rating(x, m=m, C=C):
            v = x['rating_counts']
            R = x['rating']
            return (v/(v+m) * R) + (m/(m+v) * C)

        ratings_df['score'] = ratings_df.apply(weighted_rating, axis=1)

        movie_ratings = []

        for index in ratings_df.index:
            rating = ratings_df['rating'][index]
            movie_id = index
            rating_counts = ratings_df['rating_counts'][index]
            score = ratings_df['score'][index]

            try:
                movie = Movie.objects.get(id=movie_id)

            except Movie.DoesNotExist:
                self.stdout.write(
                    f'Filme com id {movie_id} não existe no banco de dados')
                continue

            if not MovieRating.objects.filter(movie=movie).exists():

                movie_ratings.append(
                    MovieRating(
                        movie=movie,
                        rating=rating,
                        rating_counts=rating_counts,
                        score=score
                    )
                )
        MovieRating.objects.bulk_create(movie_ratings)
