from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import TemplateAPIView

from . import views

app_name = 'user_profile'

router = DefaultRouter()

profile = views.ProfileViewSet.as_view({'get': 'profile', 'put': 'update'})

urlpatterns = [
    path('profile/', profile, name='profile'),
    path(
        "profile/avatar/update/",
        views.ProfileViewSet.as_view({'post': 'image_update'}),
        name='api_avatar_update',
    ),
    # path("user/avatar/delete/", views.ProfileViewSet.as_view({'delete': 'image_delete'}), name='api_avatar_delete'),
    path(
        'profile/password/change/',
        views.ProfileViewSet.as_view({'post': 'change_password'}),
        name='api_change_pass',
    ),
    path('user/list/', views.UserListView.as_view(), name='user_list'),
    path('user/chat/', views.UserChatListView.as_view(), name='users_in_chat'),
    path('user/<user_id>/', views.UserProfileByIdView.as_view(), name='user_by_id'),
]

urlpatterns += router.urls

urlpatterns += []
