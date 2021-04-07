import logging

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount import app_settings
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialApp
from django.conf import settings

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
        # Ignore existing social accounts, just do this stuff for new ones
        if sociallogin.is_existing:
            return
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
