from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'artist', ArtistViewSet)
router.register(r'song', SongViewSet)


urlpatterns = [
    path('', HomeView.as_view()),
    path('show-categories/', ShowCategoriesView.as_view()),
    path('show-artists/', ShowArtistsView.as_view()),
    path('show-songs/', ShowSongsView.as_view()),
    path('show-songs/<slug>', ShowSongsView.as_view()),
    path('', include(router.urls))
    # path('category/', CategoryViewSet.as_view({'get': 'retrieve'})),
    # path('artist/', ArtistViewSet.as_view({'get': 'list'})),
    # path('song/', SongViewSet.as_view({'get': 'list'})),
]
