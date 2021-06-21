from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse_lazy
from auth_app.services import CeleryService
from main.services import UserService


class PassResetForm(PasswordResetForm):

    def get_reset_url(self, uid, token):
        path = "auth_app:pass_reset_confirm"
        url = reverse_lazy(path, kwargs={'uidb64': uid, 'token': token})
        return settings.FRONTEND_SITE + str(url)

    def save(self, **kwargs):
        """
        Generate a one-use only link for resetting password and send it to the user.
        """
        email = self.cleaned_data["email"]
        user = UserService.get_user(email=email)
        if not user:
            raise ValidationError({'email': _('User does not exist with this email')})
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = self.get_reset_url(uid=uid, token=token)
        content = {
            'user': user.get_full_name(),
            'reset_url': url,
        }
        CeleryService.send_password_reset(to_email=email, content=content)
