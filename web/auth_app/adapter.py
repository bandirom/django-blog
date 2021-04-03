import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.account.utils import setup_user_email
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter as _GoogleOAuth2Adapter
from django.conf import settings
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX,
    UNUSABLE_PASSWORD_SUFFIX_LENGTH,
    make_password,
)
from django.utils.crypto import get_random_string
from rest_framework.reverse import reverse_lazy


class AccountAdapter(DefaultAccountAdapter):

    def collect_data(self, email_confirmation) -> dict:
        data = {
            "user": email_confirmation.email_address.user.get_full_name(),
            "key": email_confirmation.key,
        }
        return data

    def send_confirmation_email(self, email_confirmation, ctx: dict):
        path = "auth_app:account_verification"
        activate_url = self.get_confirmation_url(email_confirmation, path)
        ctx.update({'activate_url': activate_url})
        email_template = 'account/email/email_confirmation'
        return self.send_mail(email_template, email_confirmation.email_address.email, ctx)

    @staticmethod
    def get_confirmation_url(email_confirmation, path):
        url = reverse_lazy(path, args=[email_confirmation.key])
        return settings.FRONTEND_SITE + str(url)


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a
        social provider, but before the login is actually processed
        (and before the pre_social_login signal is emitted).

        We're trying to solve different use cases:
        - social account already exists, just go on
        - social account has no email or email is unknown, just go on
        - social account's email exists, link social account to existing user
        """
        logging.warning(f"sociallogin.is_existing: {sociallogin.is_existing}")
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return
        logging.warning(f"'email' not in {sociallogin.account.extra_data}")

        # some social logins don't have an email address, e.g. facebook accounts
        # with mobile numbers only, but allauth takes care of this case so just
        # ignore it
        if 'email' not in sociallogin.account.extra_data:
            return

        # check if given email address already exists.
        # Note: __iexact is used to ignore cases
        try:
            email = sociallogin.account.extra_data['email'].lower()
            # email_address = EmailAddress.objects.get(email__iexact=email, verified=True)
            email_address = EmailAddress.objects.get(email__iexact=email)

        # if it does not, let allauth take care of this new social account
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        user = email_address.user
        logging.warning(f'Pre User, {user}, active {user.is_active}')
        sociallogin.connect(request, user)

    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. In case of auto-signup,
        the signup form is not available.
        """
        u = sociallogin.user
        sociallogin.save(request)
        return u

    def get_app(self, request, provider):
        if config := app_settings.PROVIDERS.get(provider, {}).get('APP'):
            app = SocialApp.objects.get_or_create(provider=provider)[0]
            for field in ['client_id', 'secret', 'key']:
                setattr(app, field, config.get(field))
            app.key = app.key or "unset"
            app.name = app.name or provider
            app.save()
        else:
            app = SocialApp.objects.get_current(provider, request)
        return app


class GoogleOAuth2Adapter(_GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, **kwargs):
        login = super().complete_login(request, app, token, **kwargs)
        user = login.user
        email_address = EmailAddress.objects.get(email=user.email)
        logging.warning(f'Email {email_address.email}, verified: {email_address.verified}')
        if not email_address.verified:
            email_address.verified = True
            email_address.save(update_fields=['verified'])
        user = email_address.user
        logging.warning(f'Complete_login, {user}, active {user.is_active}')
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
        if not login.user.password and login.user.password.startswith(UNUSABLE_PASSWORD_PREFIX):
            logging.warning('unusuble password')
            login.user.password = make_password(get_random_string(UNUSABLE_PASSWORD_SUFFIX_LENGTH))
        return login
