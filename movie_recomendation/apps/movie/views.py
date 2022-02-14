from movie_recomendation.apps.movie.models import (
    Genre,
    Movie
)
from movie_recomendation.apps.movie.serializers import (
    GenreSerializer,
    MovieSerializer
)

from django.db.models.query_utils import Q

from rest_framework import (
    mixins,
    viewsets
)

from functools import reduce
import operator


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query = Q()

        if self.action == 'list':
            name = str(self.request.query_params.get('name', '')).split(' ')

            if name:
                query &= (
                    reduce(
                        operator.__and__,
                        (
                            Q(name__icontains=palavra) for palavra in name
                        )
                    )
                )

        return queryset.filter(query).order_by('name')


class MovieViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        query = Q()

        if self.action == 'list':
            title = str(self.request.query_params.get('title', '')).split(' ')

            if title:
                query &= (
                    reduce(
                        operator.__and__,
                        (
                            Q(title__icontains=palavra) for palavra in title
                        )
                    )
                )

            startswith = str(self.request.query_params.get('startswith', ''))

            if startswith:
                query = Q(
                    title__istartswith=startswith
                )

        return queryset.filter(query).order_by('title', '-score')
