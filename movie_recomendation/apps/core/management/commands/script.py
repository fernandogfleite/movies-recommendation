from movie_recomendation.apps.movie.models import (
    Genre,
    Movie,
    MovieGenre
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

        movies = self.csv_to_dataframe('movies-csv/movies.csv')

        self.register_genres_from_csv(movies_csv=movies)
        self.register_movies_from_csv(movies_csv=movies)
        self.register_movie_genres_from_csv(movies_csv=movies)

        end = time.time()

        print(f'The script run in {end-start:.2f}s')

    def csv_to_dataframe(self, csv_path):
        return read_csv(csv_path)

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
        print(f"Created {len(genre_instances)} genres in {(end-start):.2f}s")

    def register_movies_from_csv(self, movies_csv: DataFrame):
        start = time.time()

        links_df = self.read_links_from_csv()
        ratings_df = self.read_ratings_from_csv()

        movie_instances = []
        for row in range(len(movies_csv)):
            id = movies_csv['movieId'][row]
            title = movies_csv['title'][row]

            imdb_id = links_df['imdbId'].get(id, None)
            tmdb_id = links_df['tmdbId'].get(id, None)

            tmdb = str(tmdb_id).split('.')[0]

            imdb = str(imdb_id).split('.')[0]

            rating = ratings_df['rating'].get(id, 0)
            rating_counts = ratings_df['rating_counts'].get(id, 0)
            score = ratings_df['score'].get(id, 0)

            movie_instances.append(
                Movie(
                    id=id,
                    title=title,
                    imdb=f'{IMDB_LINK}{imdb}',
                    tmdb=f'{TMDB_LINK}{tmdb}',
                    rating=rating,
                    rating_counts=rating_counts,
                    score=score
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
            f"Registered {len(movies_genres)} movie genres in {end-start:.2f}s"
        )

    def read_links_from_csv(self):
        links = self.csv_to_dataframe('movies-csv/links.csv')

        return DataFrame(links.groupby('movieId').mean())

    def read_ratings_from_csv(self):
        ratings = self.csv_to_dataframe('movies-csv/ratings.csv')

        ratings_df = DataFrame(ratings.groupby('movieId').rating.mean())

        ratings_df['rating_counts'] = ratings.groupby('movieId').rating.count()

        C = ratings_df['rating'].mean()

        m = ratings_df.rating_counts.min()

        def weighted_rating(x, m=m, C=C):
            v = x['rating_counts']
            R = x['rating']
            return (v/(v+m) * R) + (m/(m+v) * C)

        ratings_df['score'] = ratings_df.apply(weighted_rating, axis=1)

        return ratings_df
