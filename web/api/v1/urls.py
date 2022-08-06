from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth_app.urls')),
    path('user/', include('api.v1.profile.urls')),
]
