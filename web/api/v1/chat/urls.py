from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
    path('users/', views.UserListByIdView.as_view(), name='users_by_id'),
]
