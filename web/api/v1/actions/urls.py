from django.urls import path

from . import views

app_name = 'actions'

urlpatterns = [
    path('like', views.LikeDislikeView.as_view(), name='like'),
    path('follow', views.FollowView.as_view(), name='follow'),
    path('followers/', views.UserFollowersView.as_view({'get': 'user_followers'}), name='user_followers'),
    path('following/', views.UserFollowersView.as_view({'get': 'user_following'}), name='user_following'),
    path(
        'followers/<user_id>/',
        views.UserFollowersView.as_view({'get': 'user_followers_by_id'}),
        name='followers_by_user_id',
    ),
    path(
        'following/<user_id>/',
        views.UserFollowersView.as_view({'get': 'user_following_by_id'}),
        name='following_by_user_id',
    ),
    path('feed', views.FeedView.as_view(), name='feed'),
]
