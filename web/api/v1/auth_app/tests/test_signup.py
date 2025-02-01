import pytest
from django.test import Client
from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.reverse import reverse_lazy

pytestmark = [pytest.mark.django_db]

SIGN_UP_URL = reverse_lazy("api:v1:auth_app:sign-up")
