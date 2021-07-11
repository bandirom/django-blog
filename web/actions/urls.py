from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('like-dislike/', views.LikeDislikeView.as_view(), name='like_dislike'),
    path('follow/', views.FollowView.as_view(), name='follower'),
]

urlpatterns += router.urls
