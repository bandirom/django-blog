from datetime import datetime

from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def project_title() -> str:
    return settings.PROJECT_TITLE


@register.simple_tag
def github_link():
    return settings.GITHUB_URL


@register.simple_tag
def google_recaptcha_site_key() -> str:
    return settings.GOOGLE_RECAPTCHA_SITE_KEY


@register.filter(name='date_time')
def date(value: str):
    """2021-04-11T18:02:37.066850Z"""
    time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
    # time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z')
    return time.strftime('%b %dth, %Y')


@register.simple_tag
def timezone_cookie_name() -> str:
    return getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')


@register.simple_tag
def chat_proxy():
    return settings.CHAT_PROXY
