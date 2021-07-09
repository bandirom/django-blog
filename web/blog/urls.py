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
    path('comment/<article_id>/', views.CommentViewSet.as_view({'get': 'list'}), name='article_comments'),
    path('posts/new/', views.NewArticleView.as_view(), name='new_post'),

]

urlpatterns += router.urls
