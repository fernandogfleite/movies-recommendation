
from django.http import Http404
from django.http.response import JsonResponse
from django.core.paginator import Paginator

from movie_recomendation.apps.movie.models import (
    Genre,
    MovieGenre,
    MovieRating
)


def list_movies_by_genre(request, genre_id):

    page = request.GET.get('page', 1)

    try:
        genre = Genre.objects.get(id=genre_id)
    except Genre.DoesNotExist:
        raise Http404

    movies = MovieGenre.objects.filter(genre=genre).values_list('movie')

    movies_ratings = MovieRating.objects.filter(
        movie_id__in=movies).order_by('-rating')

    p = Paginator(movies_ratings, 10)

    if isinstance(page, str):
        if page.isnumeric():
            page = int(page)

    if not isinstance(page, int) or page not in p.page_range:
        page = 1

    paginate = p.page(page)

    previous = paginate.previous_page_number() if \
        paginate.has_previous() else None

    next = paginate.next_page_number() if paginate.has_next() else None

    genre_info = {
        'genre': {
            'id': genre.id,
            'name': genre.name,
            'movies': []
        },
        'actual_page': page,
        'previous': previous,
        'next': next,
        'total_pages': p.num_pages
    }

    for movie_rating in paginate.object_list:
        genre_info['genre']['movies'].append(
            {
                'id': movie_rating.movie.id,
                'title': movie_rating.movie.title,
                'imdb': movie_rating.movie.imdb,
                'tmdb': movie_rating.movie.tmdb,
                'rating': movie_rating.rating,
                'rating_counts': movie_rating.rating_counts
            }
        )

    return JsonResponse(genre_info)


def list_all_genres(request):

    genres = Genre.objects.all()

    genres_list = []
    for genre in genres:
        genres_list.append(
            {
                'id': genre.id,
                'name': genre.name
            }
        )

    return JsonResponse({'genres': genres_list})
