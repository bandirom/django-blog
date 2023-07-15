from django.urls import path

from . import views


app_name = 'chat'

urlpatterns = [
    path('users/', views.UserListByIdView.as_view(), name='users_by_id'),
    path('jwt/', views.JwtUserDataView.as_view(), name='user_data_by_jwt'),
    path('chat/', views.UserListByIdView.as_view(), name='user_list_data'),
]
