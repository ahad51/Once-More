from django.urls import path
from .views import (
        UserSignupView,
    UserLoginView,
    PasswordResetConfirmView,
    ForgotPasswordView  
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path(
        'auth/password-reset-confirm/<str:uid>/<str:token>/',
        PasswordResetConfirmView.as_view(),
        name='password-reset-confirm',
    ),
]
