import logging

from dj_rest_auth import views as auth_views

from . import serializers


logger = logging.getLogger(__name__)


class PasswordResetView(auth_views.PasswordResetView):
    serializer_class = serializers.PasswordResetSerializer
