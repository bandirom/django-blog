from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from main.views import TemplateAPIView

app_name = 'actions'

router = DefaultRouter()

urlpatterns = [
    path('feed', TemplateAPIView.as_view(template_name='actions/feed.html'), name='feed'),
    path('actions/', views.ActionListView.as_view(), name='action_list'),
]

urlpatterns += router.urls
