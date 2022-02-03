from django.contrib import admin

from movie_recomendation.apps.movie.models import Genre, Movie

# Register your models here.


class GenreAdmin(admin.ModelAdmin):
    search_fields = ('name',)

    class Meta:
        model = Genre


class MovieAdmin(admin.ModelAdmin):
    autocomplete_fields = ('genres', )
    search_fields = ('title',)
    list_filter = ('genres',)

    class Meta:
        model = Movie


admin.site.register(Genre, GenreAdmin)
admin.site.register(Movie, MovieAdmin)
