from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('like-dislike/', views.LikeDislikeView.as_view(), name='like_dislike'),
    path('follow/', views.FollowView.as_view(), name='follower'),
    path('followers/', views.UserFollowersView.as_view({'get': 'user_followers'}), name='user_followers'),
    path('following/', views.UserFollowersView.as_view({'get': 'user_following'}), name='user_following'),
    path('followers/<user_id>/', views.UserFollowersView.as_view({'get': 'user_followers_by_id'}),
         name='user_followers_by_user_id'),
    path('following/<user_id>/', views.UserFollowersView.as_view({'get': 'user_following_by_id'}),
         name='user_following_by_user_id'),
    path('actions/', views.ActionListView.as_view(), name='action_list'),
]

urlpatterns += router.urls
