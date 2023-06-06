from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from .services import UserDataHandler


class UserListByIdView(GenericAPIView):
    serializer_class = serializers.UserListByIdSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        handler = UserDataHandler()
        user_data: dict = handler.get_user_data(user_ids=serializer.validated_data['user_ids'])
        return Response(user_data)
