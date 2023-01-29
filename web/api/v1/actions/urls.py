from django.urls import path

from . import views

app_name = 'actions'

urlpatterns = [
    path('like', views.LikeDislikeView.as_view(), name='like'),
    path('follow', views.FollowView.as_view(), name='follow'),
]
