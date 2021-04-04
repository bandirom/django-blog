from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'blog'

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = [

]

urlpatterns += router.urls

urlpatterns += [
    path('posts/', TemplateView.as_view(template_name='blog/post_list.html'), name='post_list'),
    path('posts/<slug>/', TemplateView.as_view(template_name='blog/detail.html'), name='post_detail'),

]
