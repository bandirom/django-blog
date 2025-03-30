from enum import Enum
from typing import TypedDict

import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class RecaptchaValidateDTO(TypedDict):
    success: bool
    challenge_ts: str
    hostname: str
    score: float
    action: str


class ExpectedAction(Enum):
    LOGIN = 'LOGIN'


class RecaptchaException(ValidationError):
    pass


class GoogleRecaptcha:
    def __init__(self):
        self.site_key = settings.GOOGLE_RECAPTCHA_SITE_KEY
        self.secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        self.uri = 'https://www.google.com/recaptcha/api/siteverify'

    def get_result(self, token: str) -> RecaptchaValidateDTO:
        params = {
            'secret': self.secret_key,
            'response': token,
        }
        response = requests.post(self.uri, data=params)
        return response.json()

    def validate(self, token: str, expected_action: ExpectedAction, min_score: float = 0.5):
        result = self.get_result(token)
        score = result.get("score", 0.0)
        action = result.get("action", "")
        if result['success']:
            if (score < min_score) or (action != expected_action.value):
                raise RecaptchaException(
                    {"error": "Suspicious activity detected. Try again later."},
                    code='suspicious_activity',
                )
            return result
        else:
            raise RecaptchaException(f"Suspicious activity detected: {result['error-codes']}")
