from django.urls import path

from gsauth.views import GetCurrentUserView, RegisterUserView, SendEmailAPIView


urlpatterns = [
    path('me/', GetCurrentUserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('sendmail/', SendEmailAPIView.as_view()),
]
