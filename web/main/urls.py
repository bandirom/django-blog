from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView

from .views import SetUserTimeZone, TemplateAPIView

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='index.html'), name='index'),
    # path('', login_required(RedirectView.as_view(pattern_name='admin:index'))),
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),
]
