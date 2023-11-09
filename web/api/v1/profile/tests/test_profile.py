import pytest
from django.test.client import MULTIPART_CONTENT
from rest_framework.reverse import reverse

pytestmark = [pytest.mark.django_db]


def test_avatar_upload(api_client, user, image_content_file):
    url = reverse('api:v1:profile:avatar_update')
    data = {'avatar': image_content_file}
    response = api_client.post(url, data, content_type=MULTIPART_CONTENT)
    assert response.status_code == 200
    assert user.avatar is not None


def test_unauthorized_access(client, user, image_content_file):
    url = reverse('api:v1:profile:avatar_update')
    data = {'avatar': image_content_file}
    response = client.post(url, data, content_type=MULTIPART_CONTENT)
    assert response.status_code == 401
