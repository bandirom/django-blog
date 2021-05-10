from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.db.models import Prefetch

from main.decorators import except_shell

User = get_user_model()


class UserService:

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email):
        return User.objects.get(email=email)

    @staticmethod
    def email_address_prefetch():
        return Prefetch(
            'emailaddress_set', queryset=EmailAddress.objects.filter(primary=True), to_attr='email_address'
        )
