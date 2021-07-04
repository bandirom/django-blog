from django.apps import AppConfig


class AuthAppConfig(AppConfig):
    name = 'auth_app'

    def ready(self):
        import auth_app.signals
