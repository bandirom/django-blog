from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'blog'

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='categories')

urlpatterns = [

]

urlpatterns += router.urls


if settings.ENABLE_RENDERING:
    from . import template_views as t_views

    urlpatterns += [
        path('posts/', t_views.BlogListView.as_view(), name='post_list'),
        path('posts/<slug>/', t_views.BlogDetailView.as_view(), name='post_detail'),

    ]
