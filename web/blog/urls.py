from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from main.views import TemplateAPIView

app_name = 'blog'

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('comment', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('blog/', TemplateAPIView.as_view(template_name='blog/post_list.html'), name='blog-list'),
    path(
        'blog/<str:slug>', TemplateAPIView.as_view(template_name='blog/post_detail.html'), name='blog-detail'
    ),
    path('comment/<article_id>/', views.CommentViewSet.as_view({'get': 'list'}), name='article_comments'),
    path('posts/new/', views.CreateArticleTemplateView.as_view(), name='new_post'),
]

urlpatterns += router.urls
