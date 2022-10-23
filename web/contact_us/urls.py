from django.urls import path

from main.views import TemplateAPIView

app_name = 'contact_us'


urlpatterns = [
    path('contact/', TemplateAPIView.as_view(template_name='contact_us/index.html'), name='index'),
]
