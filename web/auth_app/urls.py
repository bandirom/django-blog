from django.urls import path
from django.views.generic import TemplateView

from main.views import TemplateAPIView

app_name = 'auth_app'


urlpatterns = [
    path('login/', TemplateAPIView.as_view(template_name='auth_app/login.html'), name='login'),
    path('register/', TemplateAPIView.as_view(template_name='auth_app/sign_up.html'), name='sign_up'),
    path(
        'password-recovery/',
        TemplateAPIView.as_view(template_name='auth_app/password_reset_done.html'),
        name='reset-email-sent',
    ),
    path('password/reset/sent/', TemplateView.as_view(template_name='auth_app/reset_email_sent.html'), name='reset-email-sent'),
    path('password/reset/done/', TemplateView.as_view(template_name='auth_app/password_reset_done.html'), name='password-reset-done'),
    path('auth/confirm/', TemplateAPIView.as_view(template_name='auth_app/email_confirm.html'), name='email_confirm')

]
