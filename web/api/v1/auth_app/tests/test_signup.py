import pytest
from django.test import Client, override_settings
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from main.models import GenderChoice

pytestmark = [pytest.mark.django_db]

SIGN_UP_URL = reverse_lazy("api:v1:auth_app:sign-up")

locmem_email_backend = override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CELERY_TASK_ALWAYS_EAGER=False,
)

@locmem_email_backend
def test_sign_up_success(client: Client, mailoutbox):
    data = {
        "email": "harley.quinn@email.com",
        "first_name": "Harley",
        "last_name": "Quinn",
        "password_1": "some_p@ssword",
        "password_2": "some_p@ssword",
        "gender": GenderChoice.MALE,
        "birthday": "1990-01-01",
    }
    response = client.post(SIGN_UP_URL, data)
    assert response.status_code == status.HTTP_201_CREATED, response.data
    assert len(mailoutbox) == 1
