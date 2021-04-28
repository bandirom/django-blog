from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'blog'

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('posts', views.ArticleViewSet, basename='post')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [

]

urlpatterns += router.urls
