from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import TemplateAPIView

from . import views

app_name = 'user_profile'

router = DefaultRouter()

profile = views.ProfileViewSet.as_view({'get': 'profile'})

urlpatterns = [
    path('profile/', profile, name='profile'),
]

urlpatterns += router.urls

urlpatterns += [

]
