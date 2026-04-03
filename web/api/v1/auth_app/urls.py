from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = 'auth_app'

urlpatterns = [
    path('sign-in/', views.LoginView.as_view(), name='sign-in'),
    path('sign-up/', views.SignUpView.as_view(), name='sign-up'),
    path('sign-up/verify/', views.VerifyEmailView.as_view(), name='sign-up-verify'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('password/reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('password/reset/confirm/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmPageView.as_view(), name='password-reset-confirm-page'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]
