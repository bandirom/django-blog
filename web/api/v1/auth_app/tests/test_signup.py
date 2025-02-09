from datetime import date

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from conftest import celery_runtime_tasks

from main.models import GenderChoice

pytestmark = [pytest.mark.django_db]

SIGN_UP_URL = reverse_lazy("api:v1:auth_app:sign-up")
User = get_user_model()


@celery_runtime_tasks
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
    new_user = User.objects.get(email=data['email'])
    assert new_user.is_active is False
    assert new_user.full_name == 'Harley Quinn'
    assert new_user.gender == GenderChoice.MALE
    assert new_user.birthday == date(1990, 1, 1)
    assert len(mailoutbox) == 1
