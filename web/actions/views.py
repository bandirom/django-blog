import logging
from django.utils.translation import gettext_lazy as _
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from . import services
from . import serializers

logger = logging.getLogger(__name__)


class LikeDislikeView(GenericAPIView):
    serializer_class = serializers.LikeDislikeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data: dict = serializer.save()
        return Response(response_data, status.HTTP_200_OK)
