from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'contact_us'

router = DefaultRouter()

urlpatterns = [
    path('feedback/', views.FeedbackView.as_view(), name='feedback')
]

urlpatterns += router.urls

urlpatterns += [
    path('contact/', TemplateView.as_view(template_name='contact_us/index.html'), name='index'),

]
