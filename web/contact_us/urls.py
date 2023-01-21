from django.urls import path

from . import views
from main.views import TemplateAPIView

app_name = 'contact_us'


urlpatterns = [
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
    path('contact/', TemplateAPIView.as_view(template_name='contact_us/index.html'), name='index'),
]
