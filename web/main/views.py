from typing import TYPE_CHECKING

from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from actions.serializers import ActionListSerializer
from actions.services import ActionsService

from .pagination import BasePageNumberPagination
from .serializers import SetTimeZoneSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


class TemplateAPIView(APIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    swagger_schema = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name: str = ''

    def get(self, request: 'Request', *args, **kwargs):
        return Response()


class GenericTemplateAPIView(GenericAPIView):
    """Help to build CMS System using DRF, JWT and Cookies
    path('some-path/', TemplateAPIView.as_view(template_name='template.html'))
    """

    swagger_schema = None
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, TemplateHTMLRenderer)
    template_name = ''

    def get(self, request, *args, **kwargs):
        return Response()


class IndexTemplateView(ListModelMixin, GenericTemplateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ActionListSerializer
    pagination_class = BasePageNumberPagination

    @property
    def template_name(self):
        if not self.request.user.is_authenticated:
            return 'index.html'
        return 'actions/index.html'

    def get_queryset(self):
        return ActionsService.get_following_actions(self.request.user)

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return super().get(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
