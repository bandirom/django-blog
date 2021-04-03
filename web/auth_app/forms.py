from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse_lazy
# from main.services import CeleryService, UserService
from main.services import UserService, CeleryService


class PassResetForm(PasswordResetForm):

    def get_reset_url(self, uid, token):
        path = "auth_app:password_reset_confirm"
        url = reverse_lazy(path, kwargs={'uidb64': uid, 'token': token})
        return settings.FRONTEND_SITE + str(url)

    def save(self, domain_override=None,
             subject_template_name='account/email/password_reset_subject.txt',
             email_template_name='account/email/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name='account/email/password_reset_email.html',
             extra_email_context=None, **kwargs):
        """
        Generate a one-use only link for resetting password and send it to the user.
        """
        email = self.cleaned_data["email"]
        user = UserService.get_user(email=email)
        if not user:
            raise ValidationError({'email': _('User does not exist with this email')})
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        url = self.get_reset_url(uid=uid, token=token)

        data = {
            'to_email': email,
            'content': {
                'user': user.get_full_name(),
                'reset_url': url,
            }
        }
        CeleryService.send_password_reset(data=data)
