from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView, TemplateView
from .views import UserView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    # path('', login_required(RedirectView.as_view(pattern_name='admin:index'))),
    path('user/', UserView.as_view()),
]
