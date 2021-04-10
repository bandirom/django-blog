from main.views import TemplateAPIView


class LoginView(TemplateAPIView):
    template_name = 'auth_app/login.html'


class SignUpView(TemplateAPIView):
    template_name = 'auth_app/sign_up.html'


class PasswordRecoveryView(TemplateAPIView):
    template_name = ''
