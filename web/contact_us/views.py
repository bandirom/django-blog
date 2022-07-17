import logging

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import FeedbackSerializer

logger = logging.getLogger(__name__)


class FeedbackView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = FeedbackSerializer
