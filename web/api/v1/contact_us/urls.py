from django.urls import path

from . import views

app_name = 'contact_us'

urlpatterns = [
    path('feedback/', views.FeedbackView.as_view(), name='feedback'),
]
