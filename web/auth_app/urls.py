from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = 'auth_app'

router = DefaultRouter()

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]


urlpatterns += [
    path('sign-in/', views.LoginView.as_view(), name='test_login'),
    path('sign-up/', views.SignUpView.as_view(), name='test_sign_up'),
    path('sign-up/verify/', views.VerifyEmailView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view()),
    path('logout/', views.LogoutView.as_view()),
]

urlpatterns += router.urls

urlpatterns += [
    path('password-recovery/', TemplateView.as_view(), name='password_recovery'),
    path('password-reset/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),
    path('verify-email/<key>/', TemplateView.as_view(), name='account_verification'),
]
