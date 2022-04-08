from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings

from .views import IndexTemplateView, SetUserTimeZone, JwtUserDataView

urlpatterns = [
    path('timezone/', SetUserTimeZone.as_view(), name='set_user_timezone'),
    path('user/jwt/', JwtUserDataView.as_view(), name='user_data_by_jwt'),

]

if settings.ENABLE_RENDERING:
    urlpatterns += [path('', IndexTemplateView.as_view(), name='index')]
else:
    urlpatterns += [path('', login_required(RedirectView.as_view(pattern_name='admin:index')))]
