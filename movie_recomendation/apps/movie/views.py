from movie_recomendation.apps.movie.models import (
    Genre,
    Movie
)
from movie_recomendation.apps.movie.serializers import (
    GenreSerializer,
    MovieSerializer
)


from rest_framework import (
    mixins,
    viewsets
)


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class MovieViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        return super().get_queryset().order_by('title', '-score')
