from django.urls import include, path
from rest_framework import routers

from .views import ArtistViewSet, CategoryViewSet, SongSearchAPIView, SongViewSet

router = routers.DefaultRouter()
router.register(r"category", CategoryViewSet, basename="category")
router.register(r"artist", ArtistViewSet, basename="artist")
router.register(r"song", SongViewSet, basename="song")


urlpatterns = [
    path("", include(router.urls)),
    path("song-search", SongSearchAPIView.as_view(), name="song-search"),
]
