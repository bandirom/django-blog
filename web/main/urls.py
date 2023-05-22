from django.urls import path

from .views import TemplateAPIView

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='index.html'), name='index'),
]
