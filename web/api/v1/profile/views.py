from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from user_profile.services import UserProfileService

from . import serializers


class JwtUserDataView(GenericAPIView):
    serializer_class = serializers.JwtUserDataSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class UserChatListView(GenericAPIView):
    serializer_class = serializers.UserChatListSerializer

    def get_queryset(self):
        return UserProfileService.user_queryset()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = UserProfileService.get_users_by_list_id(serializer.validated_data['user_ids'])
        r_serializer = serializers.UserShortInfoSerializer(queryset, many=True)
        return Response(r_serializer.data, status=status.HTTP_200_OK)


class AvatarUpdateView(GenericAPIView):
    serializer_class = serializers.UserImageSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data, instance=request.user.profile)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
