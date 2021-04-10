from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'contact_us'

router = DefaultRouter()

urlpatterns = [
    path('feedback/', views.FeedbackView.as_view(), name='feedback')
]

urlpatterns += router.urls


if settings.ENABLE_RENDERING:
    from . import template_views as t_views

    urlpatterns += [
        path('contact/', t_views.ContactUsView.as_view(), name='index'),

    ]
