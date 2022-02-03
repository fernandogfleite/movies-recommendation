from django.db import models

# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ('name',)


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.ManyToManyField(Genre)
    tmdb = models.TextField(blank=True, null=True)
    imdb = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title',)
