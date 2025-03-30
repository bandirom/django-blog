import requests
from django.conf import settings


def validate_recaptcha(token):
    URIReCaptcha = 'https://www.google.com/recaptcha/api/siteverify'

    params = {
        'secret': '6Ld22e4qAAAAAFeqw3bsmJ7rZReUQp3MQtiwuEtY',
        'response': token,
    }

    response = requests.post(URIReCaptcha, data=params)

    return response.json()


class GoogleRecaptcha:
    def __init__(self):
        self.site_key = settings.GOOGLE_RECAPTCHA_SITE_KEY
        self.secret_key = settings.GOOGLE_RECAPTCHA_SECRET_KEY
        self.uri = 'https://www.google.com/recaptcha/api/siteverify'

    def validate(self, token: str):
        params = {
            'secret': self.secret_key,
            'response': token,
        }

        response = requests.post(self.uri, data=params)
        return response.json()
