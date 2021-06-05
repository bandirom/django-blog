from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView
from django.conf import settings

from .views import UserView, SetUserTimeZone, IndexView


urlpatterns = [
    path('user/', UserView.as_view()),
    path('timezone/set/', SetUserTimeZone.as_view(), name='set_user_timezone'),

]

if settings.ENABLE_RENDERING:
    urlpatterns += [path('', IndexView.as_view(), name='index')]
else:
    urlpatterns += [path('', login_required(RedirectView.as_view(pattern_name='admin:index')))]
