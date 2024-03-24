from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers
from .base.factory import provider_registry


class OAuth2RedirectView(APIView):
    permission_classes = ()

    @extend_schema(parameters=[serializers.OAuth2RedirectSerializer])
    def get(self, request):
        serializer = serializers.OAuth2RedirectSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data['provider']
        provider = provider_registry.get_class(provider)
        redirect_url: str = provider().get_redirect_url(request)
        return Response(redirect_url)


class OAuth2ProviderListView(APIView):
    permission_classes = ()

    def get(self, request):
        providers = provider_registry.get_classes()
        return Response(providers)
