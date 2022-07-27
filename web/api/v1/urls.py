from django.urls import path, include

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth_app.urls')),
]
