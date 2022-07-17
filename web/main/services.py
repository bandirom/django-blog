from django.contrib.auth import get_user_model

from main.decorators import except_shell
from src.celery import app

User = get_user_model()


class CeleryService:
    @staticmethod
    def send_password_reset(self, data: dict):
        pass

    @staticmethod
    def send_email_confirm(user):
        key = ''
        kwargs = {
            'to_email': user.email,
            'content': {
                'user': user.get_full_name(),
                'activate_url': key,
            },
        }
        print(kwargs)


class UserService:
    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email):
        return User.objects.get(email=email)
