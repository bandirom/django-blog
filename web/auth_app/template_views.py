from main.views import TemplateAPIView


class LoginView(TemplateAPIView):
    template_name = 'auth_app/login.html'


class SignUpView(TemplateAPIView):
    template_name = 'auth_app/sign_up.html'


class PasswordResetConfirmView(TemplateAPIView):
    template_name = 'auth_app/reset_password_confirm.html'


class VerificationEmailSentView(TemplateAPIView):
    template_name = 'auth_app/verification_sent.html'


class PasswordResetEmailSentView(TemplateAPIView):
    template_name = 'auth_app/reset_password_sent.html'


class EmailVerificationView(TemplateAPIView):
    template_name = 'auth_app/email_verification.html'
