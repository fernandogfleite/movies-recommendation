from django.contrib import admin

from movie_recomendation.apps.movie.models import (
    Genre,
    Movie,
    MovieGenre,
    MovieRating
)

# Register your models here.


class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    class Meta:
        model = Genre


class MovieAdmin(admin.ModelAdmin):
    search_fields = ('title',)

    class Meta:
        model = Movie


class MovieGenreAdmin(admin.ModelAdmin):
    autocomplete_fields = ('genre', 'movie',)
    list_filter = ('genre', )
    search_fields = ('genre__name', 'movie__title')

    class Meta:
        model = MovieGenre


class MovieRatingAdmin(admin.ModelAdmin):
    autocomplete_fields = ('movie',)
    search_fields = ('movie__title',)

    class Meta:
        model = MovieRating


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieGenre, MovieGenreAdmin)
admin.site.register(MovieRating, MovieRatingAdmin)
