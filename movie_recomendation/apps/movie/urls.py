from movie_recomendation.apps.movie import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('genres', views.GenreViewSet)
router.register('movies', views.MovieViewSet)

urlpatterns = [
    path('', include(router.urls))
]
