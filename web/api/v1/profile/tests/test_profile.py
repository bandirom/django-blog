import pytest
from rest_framework.reverse import reverse

pytestmark = [pytest.mark.django_db]


@pytest.mark.skip()
def test_avatar_upload(api_client):
    url = reverse('api:v1:profile:avatar_update')
    data = {
        'avatar': 'jkh'
    }

    response = api_client.post(url, data, content_type='multipart/form-data')
    assert response.status_code == 200, response.data


