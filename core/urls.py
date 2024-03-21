from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'hymnary', HymnaryViewSet, basename='hymnary')

urlpatterns = [
    path('', include(router.urls)),
]
