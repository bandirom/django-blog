from django.urls import path

from . import views

app_name = 'profile'

urlpatterns = [
    path('jwt/', views.JwtUserDataView.as_view(), name='user_data_by_jwt'),
    path('chat/', views.JwtUserDataView.as_view(), name='user_list_data'),
]
