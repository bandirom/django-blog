from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from actions.choices import LikeIconStatus, LikeObjChoice, LikeStatus
from blog.models import Article, ArticleStatus, Category

User = get_user_model()


class LikeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data_user_1 = {'email': 'tester_1@test.com', 'password': 'StringString'}
        user_1 = User.objects.create_user(**cls.data_user_1)
        cls.data_user_2 = {'email': 'tester_2@test.com', 'password': 'String2String2'}
        user_2 = User.objects.create_user(**cls.data_user_2)

    def setUp(self):
        category = Category.objects.create(name='TestCategory')
        self.article = Article.objects.create(
            category=category, title='Test', content='TestText', status=ArticleStatus.ACTIVE
        )
        self.login_url = reverse_lazy('api:v1:auth_app:sign-in')
        data_user_1 = {'email': 'tester_1@test.com', 'password': 'StringString'}
        response = self.client.post(self.login_url, data_user_1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_create(self):
        url = reverse_lazy('api:v1:actions:like')
        data = {'model': LikeObjChoice.ARTICLE, 'object_id': self.article.id, 'vote': LikeStatus.LIKE}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['like_count'], 1)
        self.assertEqual(response.data['dislike_count'], 0)
        self.assertEqual(response.data['status'], LikeIconStatus.LIKED)
        self.assertEqual(self.article.likes(), 1)

        self.client.logout()

        login_url = reverse_lazy('api:v1:auth_app:sign-in')
        data_user_2 = {'email': 'tester_2@test.com', 'password': 'String2String2'}
        response = self.client.post(login_url, data_user_2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'model': LikeObjChoice.ARTICLE, 'object_id': self.article.id, 'vote': LikeStatus.LIKE}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['like_count'], 2)
        self.assertEqual(response.data['dislike_count'], 0)
        self.assertEqual(response.data['status'], LikeIconStatus.LIKED)
        self.assertEqual(self.article.likes(), 2)

        data = {'model': LikeObjChoice.ARTICLE, 'object_id': self.article.id, 'vote': LikeStatus.DISLIKE}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['like_count'], 1)
        self.assertEqual(response.data['dislike_count'], 1)
        self.assertEqual(response.data['status'], LikeIconStatus.DISLIKED)
        self.assertEqual(self.article.likes(), 1)
        self.assertEqual(self.article.dislikes(), 1)

        data = {'model': LikeObjChoice.ARTICLE, 'object_id': self.article.id, 'vote': LikeStatus.DISLIKE}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.article.likes(), 1)
        self.assertEqual(self.article.dislikes(), 0)
        self.assertEqual(response.data['like_count'], 1)
        self.assertEqual(response.data['dislike_count'], 0)
        self.assertEqual(response.data['status'], LikeIconStatus.EMPTY)

    def test_unauthorized_like(self):
        self.client.logout()
        url = reverse_lazy('api:v1:actions:like')
        data = {'model': LikeObjChoice.ARTICLE, 'object_id': self.article.id, 'vote': LikeStatus.LIKE}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
