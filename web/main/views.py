from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

User = get_user_model()


class TemplateAPIView(APIView):
    permission_classes = (AllowAny,)
    template_name = ''

    def get(self, request):
        return Response()


class UserView(GenericAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), id=self.request.user.id)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request):
        """Current user view

            Using this construction you can load related fields (select_related and prefetch_related) in queryset
        """

        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)


class IndexView(TemplateAPIView):
    template_name = 'index.html'
