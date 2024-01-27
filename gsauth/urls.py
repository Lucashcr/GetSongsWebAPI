from django.urls import path

from gsauth.views import *


urlpatterns = [
    path('me/', GetCurrentUserView.as_view()),
    path('register/', RegisterUserView.as_view()),
    path('sendmail/', SendEmailAPIView.as_view()),
    path('forgot-password/', ForgotPasswordAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view()),
]
