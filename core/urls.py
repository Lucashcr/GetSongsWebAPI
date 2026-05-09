from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import HymnaryViewSet, TagViewSet

router = DefaultRouter()
router.register(r"hymnary", HymnaryViewSet, basename="hymnary")
router.register(r"tag", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
]
