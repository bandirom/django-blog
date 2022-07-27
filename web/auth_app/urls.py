from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from main.views import TemplateAPIView

from . import views

app_name = 'auth_app'


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),
]

urlpatterns += [
    path('password/reset/', views.PasswordResetView.as_view()),
    # path('sign-up/verify/', views.VerifyEmailView.as_view(), name='api_sign_up_verify'),
    path('password/reset/', views.PasswordResetView.as_view(), name='api_forgot_password'),
    # path('password/reset/confirm/', views.PasswordResetConfirmView.as_view(), name='reset_confirm'),
]

urlpatterns += [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path('password-recovery/', TemplateAPIView.as_view(template_name=''), name='password_recovery'),
    path('password-reset/confirm/', TemplateView.as_view(), name='password_reset_confirm'),
    path('verify-email/', TemplateView.as_view(), name='account_verification'),
]

urlpatterns += [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path('email-sent/verify/', TemplateAPIView.as_view(template_name='auth_app/verification_sent.html'),
         name='verify_email_sent'),
    path('email-sent/reset/', TemplateAPIView.as_view(template_name='auth_app/reset_password_sent.html'),
         name='reset_email_sent'),
    path('password-reset/<uidb64>/<token>/',
         TemplateAPIView.as_view(template_name='auth_app/reset_password_confirm.html'), name='pass_reset_confirm'),
    path('verify-email/<key>/', TemplateAPIView.as_view(template_name='auth_app/email_verification.html'),
         name='account_verification'),
]
