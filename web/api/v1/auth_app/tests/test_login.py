import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse_lazy
from rest_framework import status

pytestmark = [pytest.mark.django_db]

LOGIN_URL = reverse_lazy("api:v1:auth_app:sign-in")


def test_login_success(client: Client, user):
    data = {
        "email": "harley.quinn@email.com",
        "password": "some_p@ssword",
    }

    response = client.post(LOGIN_URL, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.cookies.get(settings.REST_AUTH["JWT_AUTH_COOKIE"])
    assert response.cookies.get(settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"])


def test_wrong_credentials(client: Client, user):
    data = {
        "email": "harley.quinn@email.com",
        "password": "some_fail_p@ssword",
    }

    response = client.post(LOGIN_URL, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"].code == "wrong_credentials"


def test_user_inactive(client: Client, inactive_user):
    data = {
        "email": "harley.quinn@email.com",
        "password": "some_p@ssword",
    }

    response = client.post(LOGIN_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["email"].code == "not_active"
