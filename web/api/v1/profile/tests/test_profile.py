from base64 import b64decode

import pytest
from django.core.files.base import ContentFile
from django.test.client import MULTIPART_CONTENT
from rest_framework.reverse import reverse

pytestmark = [pytest.mark.django_db]

raw_avatar: str = (
    'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAQMAAAAl21bKAAA'
    'AA1BMVEUAAACnej3aAAAAAXRSTlMAQObYZgAAAApJREFUCNdjYAAAAAIAAeIhvDMAAAAASUVORK5CYII='
)


def test_avatar_upload(api_client, user):
    _format, imgstr = raw_avatar.split(';base64,')
    ext = _format.split('/')[-1]
    avatar = ContentFile(b64decode(imgstr), name='avatar.' + ext)
    url = reverse('api:v1:profile:avatar_update')
    data = {'avatar': avatar}
    response = api_client.post(url, data, content_type=MULTIPART_CONTENT)
    assert response.status_code == 200, response.data
    assert user.profile.avatar is not None
