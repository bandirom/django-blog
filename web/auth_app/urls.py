from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from main.views import TemplateAPIView

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
    path('password/reset/', views.PasswordResetView.as_view(), name='api_forgot_password'),
    path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='reset_confirm'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]

urlpatterns += router.urls

if settings.ENABLE_RENDERING:
    urlpatterns += [
        path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
        path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
        path('email-sent/verify/', TemplateAPIView.as_view(template_name='auth_app/reset_password_confirm.html'),
             name='verify_email_sent'),
        path('email-sent/reset/', TemplateAPIView.as_view(template_name='auth_app/verification_sent.html'),
             name='reset_email_sent'),
        path('password-reset/<uidb64>/<token>/',
             TemplateAPIView.as_view(template_name='auth_app/reset_password_sent.html'), name='pass_reset_confirm'),
        path('verify-email/<key>/', TemplateAPIView.as_view(template_name='auth_app/email_verification.html'),
             name='account_verification'),
    ]
