from django.urls import path
from .views import (
    UserSignupView,
    LoginView,
    ForgotPasswordView,
    PasswordResetConfirmView,
    VerifyEmailView
)

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('password-reset-confirm/<str:uid>/<str:token>/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('verify-email/<str:uid>/<str:token>/', VerifyEmailView.as_view(), name='verify-email'),
]
