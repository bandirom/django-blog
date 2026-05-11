from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User  = get_user_model()

class UserQueryService:
    """Service class for querying User objects"""

    def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by their email address.

        Args:
            email: The email address of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        try:
            return User.objects.get(email=email)
        except ObjectDoesNotExist:
            return None

    def user_exists_by_email(self, email: str) -> bool:
        """
        Check if a user exists with the given email address.

        Args:
            email: The email address to check

        Returns:
            True if user exists, False otherwise
        """
        return User.objects.filter(email=email).exists()
