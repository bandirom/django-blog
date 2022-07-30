from django.urls import path
from django.views.generic import TemplateView

from main.views import TemplateAPIView

app_name = 'auth_app'

urlpatterns = [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'reset/confirm/',
        TemplateView.as_view(template_name='auth_app/reset_password_confirm.html'),
        name='password_reset_confirm',
    ),
    path('verify-email/', TemplateView.as_view(), name='account_verification'),
]

urlpatterns += [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'email-sent/verify/',
        TemplateAPIView.as_view(template_name='auth_app/verification_sent.html'),
        name='verify_email_sent',
    ),
    path(
        'email-sent/reset/',
        TemplateAPIView.as_view(template_name='auth_app/reset_password_sent.html'),
        name='reset_email_sent',
    ),
    path(
        'verify-email/<key>/',
        TemplateAPIView.as_view(template_name='auth_app/email_verification.html'),
        name='account_verification',
    ),
]
