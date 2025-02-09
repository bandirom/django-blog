from django.test import Client
from rest_framework import status
import pytest
from rest_framework.reverse import reverse_lazy

from conftest import celery_runtime_tasks

pytestmark = [pytest.mark.django_db]

RESET_CONFIRM_URL = reverse_lazy('api:v1:auth_app:reset-password-confirm')
PASSWORD_RESET_URL = reverse_lazy('api:v1:auth_app:reset-password')
LOGIN_URL = reverse_lazy('api:v1:auth_app:sign-in')


class TestPasswordReset:

    @celery_runtime_tasks
    @pytest.mark.parametrize(
        ['email', 'status_code', 'code', 'email_count'], (
            ('harley.quinn@email.com', 200, None, 1),
            ('wrong_email', 400, 'invalid', 0),
            ('wrong_email@email.com', 200, None, 0),
        )
    )
    def test_password_reset(
        self,
        client: Client,
        mailoutbox,
        user,
        email: str,
        code: str,
        status_code: int,
        email_count: int,
    ):
        data = {'email': email}
        response = client.post(PASSWORD_RESET_URL, data)
        assert response.status_code == status_code
        if code:
            assert response.data['email'][0].code == code
        assert len(mailoutbox) == email_count


class TestPasswordResetConfirm:

    def test_reset_successful(self, client, user, user_uid_and_token):
        data = {
            'password_1': 'tester26',
            'password_2': 'tester26',
            'uid': user_uid_and_token.uid,
            'token': user_uid_and_token.token,
        }

        response = client.post(RESET_CONFIRM_URL, data)

        assert response.status_code == status.HTTP_200_OK
        user.refresh_from_db()
        assert user.check_password(data['password_1'])

    def test_validate_password(self, client, user, user_uid_and_token):
        data = {
            'password_1': 'tester26',
            'password_2': 'tester26',
            'uid': user_uid_and_token.uid,
            'token': user_uid_and_token.token,
        }
        response = client.post(RESET_CONFIRM_URL, data)
