from django.urls import path

from main.views import TemplateAPIView

app_name = 'auth_app'

urlpatterns = [
    path('login', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('confirm', TemplateAPIView.as_view(template_name='auth_app/email_verification.html'), name='email_verify'),
    path('register', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'reset/confirm/',
        TemplateAPIView.as_view(template_name='auth_app/reset_password_confirm.html'),
        name='password_reset_confirm',
    ),
    path(
        'email-sent/verify/',
        TemplateAPIView.as_view(template_name='auth_app/verification_sent.html'),
        name='verify_email_sent',
    ),
]
