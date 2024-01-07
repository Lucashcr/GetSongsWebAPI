"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import GetCurrentUserView, RegisterUserView


def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', include('core.urls')),
    path('sentry-debug/', trigger_error),

    path('user/', include([
        path('me/', GetCurrentUserView.as_view()),
        path('register/', RegisterUserView.as_view()),
        path("token/", TokenObtainPairView.as_view(), name="token"),
        path("refresh_token/", TokenRefreshView.as_view(), name="refresh_token"),
    ])),
]
