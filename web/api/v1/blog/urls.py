from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('articles/', views.ArticleListView.as_view(), name='post-list'),
    path('articles/new/', views.CreateArticleView.as_view(), name='new-post'),
    path('articles/<slug>/', views.ArticleDetailView.as_view(), name='post-detail'),
    path('comments/', views.CreateCommentView.as_view(), name='create-comment'),
    path('comments/<article_slug>/', views.CommentListView.as_view(), name='comment-list'),
    path('tags/', views.TagListView.as_view(), name='tag-list'),
]
