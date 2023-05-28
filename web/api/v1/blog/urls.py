from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path('articles/', views.ArticleListView.as_view(), name='post-list'),
    path('articles/<slug>/', views.ArticleDetailView.as_view(), name='post-detail'),
]
