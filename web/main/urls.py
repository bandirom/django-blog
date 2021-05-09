from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView
from .views import TemplateAPIView
from django.conf import settings


urlpatterns = [
]

if settings.ENABLE_RENDERING:
    urlpatterns += [path('', TemplateAPIView.as_view(template_name='index.html'), name='index')]
else:
    urlpatterns += [path('', login_required(RedirectView.as_view(pattern_name='admin:index')))]
