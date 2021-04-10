from django.urls import path
from django.views.generic import TemplateView
from django.conf import settings
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
    path('sign-in/', views.LoginView.as_view(), name='api_login'),
    path('sign-up/', views.SignUpView.as_view(), name='api_sign_up'),
    path('sign-up/verify/', views.VerifyEmailView.as_view()),
    path('password/reset/', views.PasswordResetView.as_view()),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view()),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls

urlpatterns += [
    path('password-reset/<uidb64>/<token>/', TemplateView.as_view(), name='password_reset_confirm'),
    path('verify-email/<key>/', TemplateView.as_view(), name='account_verification'),
]

if settings.ENABLE_RENDERING:
    from . import template_views as t_views

    urlpatterns += [
        path('login/', t_views.LoginView.as_view(), name='login'),
        path('register/', t_views.SignUpView.as_view(), name='sign_up'),
        path('password-recovery/', t_views.PasswordRecoveryView.as_view(), name='password_recovery'),

    ]
