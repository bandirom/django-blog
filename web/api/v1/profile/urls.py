from django.urls import path

from . import views

app_name = 'profile'

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('avatar/update/', views.AvatarUpdateView.as_view(), name='avatar_update'),
    path('password/update/', views.ChangePasswordView.as_view(), name='change-password'),
]
