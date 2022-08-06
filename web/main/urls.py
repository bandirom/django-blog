from django.urls import path

from .views import SetUserTimeZone, TemplateAPIView

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='index.html'), name='index'),
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),
]
