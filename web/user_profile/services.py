from django.conf import settings
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()


class UserProfileService:

    @staticmethod
    def get_user_profile(user_id):
        return User.objects.select_related('profile').get(id=user_id)
