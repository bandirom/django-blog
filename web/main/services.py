from django.contrib.auth import get_user_model
from main.decorators import except_shell

User = get_user_model()


class UserService:

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email):
        return User.objects.get(email=email)
