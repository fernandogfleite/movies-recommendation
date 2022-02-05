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

import time


IMDB_LINK = 'https://www.imdb.com/title/tt'
TMDB_LINK = 'https://www.themoviedb.org/movie/'


class Command(BaseCommand):
    help = 'Run script'

    def handle(self, *args, **kwargs):
        start = time.time()

        movies = read_csv('movies-csv/movies.csv')

        self.register_genres_from_csv(movies_csv=movies)
        self.register_movies_from_csv(movies_csv=movies)
        self.register_movie_genres_from_csv(movies_csv=movies)
        self.register_ratings_from_csv()

        end = time.time()

        print(f'The script run in {end-start:.2f}s')

    def register_genres_from_csv(self, movies_csv: DataFrame):
        start = time.time()
        unique_genres = set()

        for genres in movies_csv['genres']:
            genre_list = genres.split('|')

            for genre in genre_list:
                unique_genres.add(genre)

        genre_instances = [
            Genre(name=genre) for genre in unique_genres
        ]

        Genre.objects.bulk_create(genre_instances)
        end = time.time()
        print(f"Created {len(genre_instances)} genres in {end-start:.2f}s")

    def register_movies_from_csv(self, movies_csv: DataFrame):
        links = read_csv('movies-csv/links.csv')
        links_df = DataFrame(links.groupby('movieId').mean())
        start = time.time()
        movie_instances = []
        for row in range(len(movies_csv)):
            id = movies_csv['movieId'][row]
            title = movies_csv['title'][row]

            imdb_id = links_df['imdbId'][id]
            tmdb_id = links_df['tmdbId'][id]

            tmdb = str(tmdb_id).split('.')[0]

            movie_instances.append(
                Movie(
                    id=id,
                    title=title,
                    imdb=f'{IMDB_LINK}{str(imdb_id)}',
                    tmdb=f'{TMDB_LINK}{tmdb}'
                )
            )

        Movie.objects.bulk_create(movie_instances)
        end = time.time()
        print(f"Created {len(movie_instances)} movies in {end-start:.2f}s")

    def register_movie_genres_from_csv(self, movies_csv: DataFrame):
        start = time.time()
        movies_genres = []
        for row in range(len(movies_csv)):
            id = movies_csv['movieId'][row]
            genres = movies_csv['genres'][row]

            genre_list = genres.split('|')

            movies_genres += [
                MovieGenre(
                    movie_id=id,
                    genre=genre
                ) for genre in Genre.objects.filter(name__in=genre_list)
            ]

        MovieGenre.objects.bulk_create(movies_genres)

        end = time.time()
        print(
            f"Registered {len(movies_genres)} movie genres in {end-start:.2f}s")

    def register_ratings_from_csv(self):
        start = time.time()

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

            movie_ratings.append(
                MovieRating(
                    movie_id=movie_id,
                    rating=rating,
                    rating_counts=rating_counts,
                    score=score
                )
            )
        MovieRating.objects.bulk_create(movie_ratings)
        end = time.time()
        print(
            f"Registered {len(movie_ratings)} movie ratings in {end-start:.2f}s")
