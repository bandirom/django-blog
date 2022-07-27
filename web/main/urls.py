from django.urls import path

from .views import TemplateAPIView, SetUserTimeZone, JwtUserDataView

urlpatterns = [
    path('', TemplateAPIView.as_view(template_name='index.html'), name='index'),
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),
    path('user/jwt/', JwtUserDataView.as_view(), name='user_data_by_jwt'),
]
