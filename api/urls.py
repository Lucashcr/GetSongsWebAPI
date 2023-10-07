from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'artist', ArtistViewSet, basename='artist')
router.register(r'song', SongViewSet, basename='song')


urlpatterns = [
    path('', HomeView.as_view()),
    path('show-categories/', ShowCategoriesView.as_view()),
    path('show-artists/', ShowArtistsView.as_view()),
    path('show-songs/', ShowSongsView.as_view()),
    path('show-songs/<slug>', ShowSongsView.as_view()),
    path('', include(router.urls))
]
