from rest_framework.exceptions import ValidationError


class OAuth2Error(ValidationError):
    pass
