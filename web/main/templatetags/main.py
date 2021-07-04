from datetime import datetime
from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def microservice_title():
    return settings.MICROSERVICE_TITLE


@register.simple_tag
def github_link():
    return settings.GITHUB_URL


@register.filter(name='date_time')
def date(value: str):
    """ 2021-04-11T18:02:37.066850Z """
    time = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
    return time.strftime('%b %dth, %Y')


@register.simple_tag
def timezone_cookie_name():
    return getattr(settings, 'TIMEZONE_COOKIE_NAME', 'timezone')
