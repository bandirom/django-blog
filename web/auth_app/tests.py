import re
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import SimpleCookie
from django.test import TestCase, override_settings
from django.core import mail

from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status

from auth_app.serializers import error_messages
from main.services import UserService

User = get_user_model()

locmem_email_backend = override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    CELERY_TASK_ALWAYS_EAGER=False,
)


# refresh_from_db()


class AuthApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        data = {
            'email': 'bandirom@ukr.net',
            'password': make_password('tester26')
        }
        cls.user = User.objects.create(**data, is_active=False)
        cls.user.emailaddress_set.create(email=cls.user.email, primary=True, verified=False)

    def test_login(self):
        login_url = reverse_lazy('auth_app:api_login')
        user_url = reverse_lazy('user_profile:profile')

        data = {
            'email': self.user.email,
            'password': 'tester26',
        }
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        self.assertEqual(response.json(), {'email': [error_messages['not_verified']]})
        email = self.user.emailaddress_set.get(primary=True)
        email.verified = True
        email.save()
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        self.assertEqual(response.json(), {'email': [error_messages['not_active']]})
        self.user.is_active = True
        self.user.save()
        data['password'] = 'wrong_password'
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.content)
        self.assertEqual(response.json(), {'email': [error_messages['wrong_credentials']]})
        data['password'] = 'tester26'
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)
        self.client.cookies = SimpleCookie({settings.JWT_AUTH_COOKIE: response.data['access_token']})
        response = self.client.get(user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.content)

    @locmem_email_backend
    def test_sign_up(self):
        url = reverse_lazy('auth_app:api_sign_up')
        data = {
            'email': 'new_user@test.com',
            'first_name': 'Nazarii',
            'last_name': 'bandirom',
            'password1': 'tester26',
            'password2': 'tester27',
        }
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        data['password2'] = 'tester26'
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(len(mail.outbox), 1)
        response = self.client.post(path=url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)
        self.assertEqual(response.json(), {'email': [error_messages['already_registered']]})
        user = UserService.get_user(email=data['email'])
        self.assertFalse(user.is_active)
        self.assertFalse(user.email_verified())
        string = str(mail.outbox[0].message())
        pattern = r'(http?://[^\"\s]+)'
        result = re.findall(pattern, string)
        activate_url = result[0]
        key = activate_url.split('/')
        url = reverse_lazy('auth_app:api_sign_up_verify')
        data = {'key': key[5]}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        user = UserService.get_user('new_user@test.com')
        self.assertTrue(user.is_active)
        self.assertTrue(user.email_verified())

    @locmem_email_backend
    def test_password_reset(self):
        url = reverse_lazy('auth_app:api_forgot_password')
        data = {'email': self.user.email}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(mail.outbox), 1)

    def test_logout(self):
        # url = reverse_lazy('auth_app:logout')
        pass
