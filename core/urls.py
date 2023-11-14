from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.csrf import csrf_protect

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'hymnary', HymnaryViewSet, basename='hymnary')
router.register(r'hymnarysong', HymnarySongViewSet, basename='hymnarysong')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/hymnary/<int:hymnary_id>/export', ExportHymnaryAPIView.as_view()),
    path('api/hymnary/<int:hymnary_id>/reorder/', ReorderSongsAPIView.as_view()),
]
