from django.urls import path

from . import views

app_name = 'profile'

urlpatterns = [
    path('avatar/update/', views.AvatarUpdateView.as_view(), name='avatar_update'),
]
