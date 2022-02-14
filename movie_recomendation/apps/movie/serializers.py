from rest_framework import serializers

from movie_recomendation.apps.movie.models import Genre, Movie, MovieGenre


class GenresField(serializers.Field):
    def to_representation(self, data):
        genres = Genre.objects.filter(
            id__in=MovieGenre.objects.filter(
                movie=data).values_list('genre_id')
        )

        serializer = GenreSerializer(genres, many=True)

        return serializer.data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    genres = GenresField(source='*')

    class Meta:
        model = Movie
        fields = (
            'id',
            'title',
            'rating',
            'rating_counts',
            'imdb',
            'tmdb',
            'genres'
        )
