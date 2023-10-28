from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='post-list'),
    path('articles/new/', views.CreateArticleView.as_view(), name='new-post'),
    path('articles/<slug>/', views.ArticleDetailView.as_view(), name='post-detail'),
    path('comments/<article_slug>/', views.CommentListView.as_view(), name='comment-list'),
]
