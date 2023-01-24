from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from . import serializers
from .services import LikeService


class LikeDislikeView(GenericAPIView):
    serializer_class = serializers.LikeDislikeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = LikeService(
            user=request.user,
            vote=serializer.validated_data['vote'],
            model=serializer.validated_data['model'],
            object_id=serializer.validated_data['object_id'],
        )

        response_data: dict = service.make_like()
        return Response(response_data, status.HTTP_200_OK)
