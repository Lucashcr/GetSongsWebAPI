from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.decorators.csrf import csrf_protect

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'hymnary', HymnaryViewSet, basename='hymnary')

urlpatterns = [
    path('', HomeView.as_view()),
    path('about', AboutView.as_view()),
    path('contact', ContactView.as_view()),
    path('thanks-contact', ThanksContactView.as_view()),
    path('hymnary', login_required(ListHymnaries.as_view())),
    path("hymnary/new/<hymnary_name>", login_required(new_hymnary)),
    path('hymnary/<int:hymnary_id>', login_required(ShowHymnary.as_view())),
    path('hymnary/<int:hymnary_id>/delete',
         login_required(DeleteHymnary.as_view())),
    path('hymnary/<int:hymnary_id>/edit',
         login_required(EditHymnary.as_view())),
    path('hymnary/<int:hymnary_id>/export',
         login_required(export_hymnary)),
    path('hymnary/<int:hymnary_id>/save',
         login_required(csrf_protect(save_hymnary))),

#     path('api/hymnary', ListHymanariesAPIView.as_view()),
#     path('api/hymnary/<int:hymnary_id>', DetailHymnaryAPIView.as_view()),
    path('api/hymnary/<int:hymnary_id>/add', AddSongToHymnaryAPIView.as_view()),
    path('api/', include(router.urls)),
]
