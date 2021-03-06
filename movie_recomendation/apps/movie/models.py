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
    tmdb = models.TextField(blank=True, null=True)
    imdb = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ('title',)


class MovieGenre(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.movie.title} - {self.genre.name}'


class MovieRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.DecimalField(decimal_places=6, max_digits=12)
    rating_counts = models.IntegerField()
    score = models.DecimalField(decimal_places=6, max_digits=12)

    class Meta:
        ordering = ('-score',)

    def __str__(self) -> str:
        return f'{self.movie.title} - Rating: {self.rating}'
