from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import FeedbackSerializer


class FeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer
