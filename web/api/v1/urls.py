from django.urls import include, path

app_name = 'v1'

urlpatterns = [
    path('auth/', include('api.v1.auth_app.urls')),
    path('article/', include('api.v1.blog.urls')),
    path('contact/', include('api.v1.contact_us.urls')),
]
