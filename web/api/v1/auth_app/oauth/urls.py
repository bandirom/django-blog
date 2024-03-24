from django.urls import path

from . import views
from .google.views import GoogleOAuth2CallbackView

app_name = 'oauth_app'

urlpatterns = [
    path('oauth2/redirect-url/', views.OAuth2RedirectView.as_view(), name='oauth2-redirect-url'),
    path('oauth2/providers/', views.OAuth2ProviderListView.as_view(), name='oauth2-providers'),
    path('google/sign-in/', GoogleOAuth2CallbackView.as_view(), name='google-sign-in'),
]
