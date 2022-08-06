from urllib.parse import urljoin

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class SetTimeZoneSerializer(serializers.Serializer):
    timezone = serializers.ChoiceField(choices=pytz.common_timezones)
