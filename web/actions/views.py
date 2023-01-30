import logging

from rest_framework.generics import ListAPIView

from . import serializers
from .services import ActionsService
from main.pagination import BasePageNumberPagination

logger = logging.getLogger(__name__)


class ActionListView(ListAPIView):
    serializer_class = serializers.ActionListSerializer
    pagination_class = BasePageNumberPagination

    def get_queryset(self):
        return ActionsService.get_following_actions(self.request.user)
