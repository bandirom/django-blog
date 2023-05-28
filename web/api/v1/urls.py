from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth_app.urls')),
    path('blog/', include('api.v1.blog.urls')),
    path('contact/', include('api.v1.contact_us.urls')),
    path('user/', include('api.v1.profile.urls')),
    path('actions/', include('api.v1.actions.urls')),
]
