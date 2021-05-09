from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


User = get_user_model()


class TemplateAPIView(APIView):
    permission_classes = (AllowAny,)
    template_name = ''

    @method_decorator(name='create', decorator=swagger_auto_schema(auto_schema=None))
    def get(self, request, *args, **kwargs):
        return Response()
