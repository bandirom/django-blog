from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('actions/', views.ActionListView.as_view(), name='action_list'),
]

urlpatterns += router.urls
